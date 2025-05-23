import threading
import time
import random
import logging
import queue
import os
import json
import signal
import sys
from datetime import datetime
from statistics import mean, stdev

# Configuração do sistema de logging
def setup_logging():
    # Criar diretório de logs se não existir
    if not os.path.exists('logs'):
        os.makedirs('logs')
    
    # Nome do arquivo de log com timestamp
    log_file = f'logs/sensor_monitoring_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log'
    
    # Configurar o logger
    logger = logging.getLogger('SensorMonitor')
    logger.setLevel(logging.DEBUG)
    
    # Formato das mensagens de log
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - [%(threadName)s] - %(message)s')
    
    # Handler para arquivo
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)
    
    # Handler para console
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)
    
    # Adicionar handlers ao logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    return logger

class SensorReading:
    def __init__(self, sensor_id, sensor_type, value, unit, timestamp=None):
        self.sensor_id = sensor_id
        self.sensor_type = sensor_type
        self.value = value
        self.unit = unit
        self.timestamp = timestamp or datetime.now()
    
    def to_dict(self):
        return {
            'sensor_id': self.sensor_id,
            'sensor_type': self.sensor_type,
            'value': self.value,
            'unit': self.unit,
            'timestamp': self.timestamp.strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
        }
    
    def __str__(self):
        return f"{self.sensor_type} (ID:{self.sensor_id}): {self.value}{self.unit}"

class Sensor:
    def __init__(self, sensor_id, sensor_type, min_value, max_value, unit, interval, data_queue, logger):
        self.sensor_id = sensor_id
        self.sensor_type = sensor_type
        self.min_value = min_value
        self.max_value = max_value
        self.unit = unit
        self.interval = interval  # em segundos
        self.data_queue = data_queue
        self.logger = logger
        self.running = True
        self.readings = []
        
        # Valores para simular drift e variação
        self.current_value = random.uniform(min_value, max_value)
        self.drift_factor = random.uniform(-0.1, 0.1)
    
    def simulate_reading(self):
        # Simular drift gradual com variação aleatória
        self.current_value += random.uniform(-0.5, 0.5) + self.drift_factor
        
        # Manter valor dentro dos limites
        self.current_value = max(self.min_value, min(self.max_value, self.current_value))
        
        # Arredondar para 1 casa decimal
        return round(self.current_value, 1)
    
    def run(self):
        self.logger.info(f"Sensor {self.sensor_type} (ID:{self.sensor_id}) iniciado - intervalo de leitura: {self.interval}s")
        
        read_count = 0
        
        try:
            while self.running:
                start_time = time.time()
                
                # Simular leitura do sensor
                value = self.simulate_reading()
                reading = SensorReading(self.sensor_id, self.sensor_type, value, self.unit)
                
                # Armazenar leitura no histórico local do sensor
                self.readings.append(reading)
                if len(self.readings) > 100:  # Manter apenas as 100 últimas leituras
                    self.readings.pop(0)
                
                # Adicionar leitura à fila para processamento
                self.data_queue.put(reading)
                
                read_count += 1
                self.logger.debug(f"Leitura #{read_count} do sensor {self.sensor_type} (ID:{self.sensor_id}): {value}{self.unit}")
                
                # Calcular tempo necessário para atingir o intervalo correto
                elapsed = time.time() - start_time
                sleep_time = max(0, self.interval - elapsed)
                
                if sleep_time > 0:
                    time.sleep(sleep_time)
                else:
                    self.logger.warning(f"Sensor {self.sensor_id} está atrasado: processamento levou {elapsed:.3f}s")
        
        except Exception as e:
            self.logger.error(f"Erro no sensor {self.sensor_id}: {e}", exc_info=True)
        finally:
            self.logger.info(f"Sensor {self.sensor_type} (ID:{self.sensor_id}) finalizado após {read_count} leituras")
    
    def get_statistics(self):
        if not self.readings:
            return {"count": 0}
        
        values = [r.value for r in self.readings]
        return {
            "count": len(values),
            "last": values[-1],
            "min": min(values),
            "max": max(values),
            "avg": round(mean(values), 2),
            "std_dev": round(stdev(values), 2) if len(values) > 1 else 0
        }

class SensorMonitor:
    def __init__(self):
        self.logger = setup_logging()
        self.data_queue = queue.Queue()
        self.sensors = []
        self.sensor_threads = []
        self.running = True
        self.data_processor_thread = None
        self.display_thread = None
        
        # Configurações
        self.save_interval = 60  # segundos entre salvamentos de dados
        self.data_file = "sensor_data.json"
        
        # Interceptar sinais para encerramento elegante
        signal.signal(signal.SIGINT, self.signal_handler)
        
        self.logger.info("Sistema de monitoramento de sensores IoT iniciado")
    
    def signal_handler(self, sig, frame):
        self.logger.info("Sinal de interrupção recebido. Iniciando encerramento...")
        self.stop()
    
    def create_sensors(self):
        # Definir vários tipos de sensores com características diferentes
        sensor_types = [
            # ID, Tipo, Min, Max, Unidade, Intervalo
            (1, "Temperatura", 15.0, 35.0, "°C", 2.0),
            (2, "Umidade", 20.0, 95.0, "%", 3.0),
            (3, "Pressão", 980.0, 1030.0, "hPa", 5.0),
            (4, "CO2", 400.0, 1500.0, "ppm", 4.0),
            (5, "Luminosidade", 0.0, 1000.0, "lux", 1.5),
            (6, "Bateria", 0.0, 100.0, "%", 10.0),
            (7, "Ruído", 30.0, 90.0, "dB", 2.5)
        ]
        
        for sensor_id, sensor_type, min_val, max_val, unit, interval in sensor_types:
            sensor = Sensor(sensor_id, sensor_type, min_val, max_val, unit, interval, self.data_queue, self.logger)
            self.sensors.append(sensor)
            self.logger.info(f"Sensor criado: {sensor_type} (ID:{sensor_id}) - faixa: {min_val}{unit} a {max_val}{unit}")
    
    def start_monitoring(self):
        self.logger.info("Iniciando monitoramento de sensores...")
        
        # Criar sensores
        self.create_sensors()
        
        # Iniciar thread de processamento de dados
        self.data_processor_thread = threading.Thread(
            target=self.process_data, 
            name="DataProcessor"
        )
        self.data_processor_thread.daemon = True
        self.data_processor_thread.start()
        
        # Iniciar thread de exibição
        self.display_thread = threading.Thread(
            target=self.display_stats, 
            name="DisplayStats"
        )
        self.display_thread.daemon = True
        self.display_thread.start()
        
        # Iniciar threads de sensores
        for sensor in self.sensors:
            thread = threading.Thread(
                target=sensor.run, 
                name=f"Sensor-{sensor.sensor_id}"
            )
            thread.daemon = True
            self.sensor_threads.append(thread)
            thread.start()
            
            # Pequeno intervalo para evitar que todos os sensores leiam ao mesmo tempo
            time.sleep(0.5)
        
        self.logger.info(f"{len(self.sensors)} sensores iniciados em threads separadas")
        
        try:
            # Manter a thread principal em execução
            while self.running:
                time.sleep(1)
        except KeyboardInterrupt:
            self.logger.info("Interrupção do teclado detectada")
        finally:
            self.stop()
    
    def process_data(self):
        """Thread para processar os dados dos sensores na fila"""
        self.logger.info("Processador de dados iniciado")
        
        data_to_save = []
        last_save_time = time.time()
        
        while self.running:
            try:
                # Coletar leituras por um período antes de processar em lote
                current_time = time.time()
                elapsed = current_time - last_save_time
                
                # Processar leituras disponíveis
                while not self.data_queue.empty():
                    reading = self.data_queue.get()
                    data_to_save.append(reading.to_dict())
                    self.data_queue.task_done()
                
                # Salvar dados periodicamente se houver dados para salvar
                if elapsed >= self.save_interval and data_to_save:
                    self.save_data(data_to_save)
                    self.logger.info(f"Dados salvos: {len(data_to_save)} leituras")
                    data_to_save = []
                    last_save_time = current_time
                
                time.sleep(1)
            except Exception as e:
                self.logger.error(f"Erro no processamento de dados: {e}", exc_info=True)
    
    def display_stats(self):
        """Thread para exibir estatísticas dos sensores"""
        self.logger.info("Thread de exibição de estatísticas iniciada")
        
        while self.running:
            try:
                time.sleep(10)  # Atualizar a cada 10 segundos
                
                print("\n" + "="*80)
                print(f"ESTATÍSTICAS DOS SENSORES - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
                print("="*80)
                
                for sensor in self.sensors:
                    stats = sensor.get_statistics()
                    status = "OK"
                    
                    # Determinar status com base nos valores
                    if stats["count"] == 0:
                        status = "SEM DADOS"
                    elif sensor.sensor_type == "Temperatura" and stats["last"] > 30:
                        status = "ALERTA: TEMPERATURA ALTA"
                    elif sensor.sensor_type == "CO2" and stats["last"] > 1200:
                        status = "ALERTA: CO2 ELEVADO"
                    elif sensor.sensor_type == "Bateria" and stats["last"] < 20:
                        status = "ALERTA: BATERIA BAIXA"
                    
                    print(f"Sensor {sensor.sensor_type} (ID:{sensor.sensor_id}):")
                    print(f"  Último valor: {stats.get('last', 'N/A')}{sensor.unit}")
                    print(f"  Min: {stats.get('min', 'N/A')}{sensor.unit}, " +
                          f"Máx: {stats.get('max', 'N/A')}{sensor.unit}, " +
                          f"Média: {stats.get('avg', 'N/A')}{sensor.unit}")
                    print(f"  Leituras: {stats['count']} | Status: {status}")
                    print("-"*80)
                
                # Estatísticas de sistema
                total_readings = sum(len(s.readings) for s in self.sensors)
                queue_size = self.data_queue.qsize()
                
                print(f"Total de leituras: {total_readings} | Leituras na fila: {queue_size}")
                print("="*80)
                
            except Exception as e:
                self.logger.error(f"Erro ao exibir estatísticas: {e}")
    
    def save_data(self, data):
        """Salva os dados em arquivo JSON"""
        try:
            # Carregar dados existentes, se houver
            existing_data = []
            if os.path.exists(self.data_file):
                with open(self.data_file, 'r') as f:
                    existing_data = json.load(f)
            
            # Adicionar novos dados
            all_data = existing_data + data
            
            # Limitar tamanho para evitar arquivos muito grandes
            max_records = 10000
            if len(all_data) > max_records:
                all_data = all_data[-max_records:]
                self.logger.warning(f"Arquivo de dados limitado a {max_records} registros")
            
            # Salvar no arquivo
            with open(self.data_file, 'w') as f:
                json.dump(all_data, f, indent=2)
            
            self.logger.debug(f"Dados salvos em {self.data_file}: {len(data)} novos registros")
        
        except Exception as e:
            self.logger.error(f"Erro ao salvar dados: {e}", exc_info=True)
    
    def stop(self):
        """Para todas as threads e o sistema de monitoramento"""
        self.logger.info("Parando o sistema de monitoramento...")
        self.running = False
        
        for sensor in self.sensors:
            sensor.running = False
        
        for thread in self.sensor_threads:
            thread.join()
        
        remaining_data = []
        while not self.data_queue.empty():
            reading = self.data_queue.get()
            remaining_data.append(reading.to_dict())
            self.data_queue.task_done()
        
        if remaining_data:
            self.logger.info(f"Salvando {len(remaining_data)} leituras restantes...")
            self.save_data(remaining_data)
        
        self.logger.info("Sistema de monitoramento encerrado")
        logging.shutdown()

if __name__ == "__main__":
    monitor = SensorMonitor()
    monitor.start_monitoring()