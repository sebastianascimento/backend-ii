import threading
import time
import logging
import random
import os
from datetime import datetime
from queue import Queue

def setup_logging():
    if not os.path.exists('logs'):
        os.makedirs('logs')
    
    log_filename = f"logs/test_run_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - [%(threadName)s] - %(message)s',
        handlers=[
            logging.FileHandler(log_filename),
            logging.StreamHandler()
        ]
    )
    
    return logging.getLogger()

def test_func_api(test_name):
    logger = logging.getLogger()
    logger.info(f"Iniciando teste API: {test_name}")
    
    duration = random.uniform(0.5, 2.0)
    time.sleep(duration)
    
    success = random.random() > 0.2
    
    if success:
        logger.info(f"Teste API {test_name} passou! ({duration:.2f}s)")
        return True
    else:
        logger.error(f"Teste API {test_name} falhou! ({duration:.2f}s)")
        return False

def test_func_ui(test_name):
    logger = logging.getLogger()
    logger.info(f"Iniciando teste UI: {test_name}")
    
    duration = random.uniform(1.0, 3.0)
    time.sleep(duration)
    
    success = random.random() > 0.3
    
    if success:
        logger.info(f"Teste UI {test_name} passou! ({duration:.2f}s)")
        return True
    else:
        logger.error(f"Teste UI {test_name} falhou! ({duration:.2f}s)")
        return False

def test_func_performance(test_name):
    logger = logging.getLogger()
    logger.info(f"Iniciando teste de Performance: {test_name}")
    
    duration = random.uniform(2.0, 4.0)
    time.sleep(duration)
    
    rps = random.uniform(100, 500)
    latency = random.uniform(50, 300)
    
    success = rps > 200 and latency < 200
    
    if success:
        logger.info(f"Teste Performance {test_name} passou! RPS: {rps:.2f}, Latência: {latency:.2f}ms ({duration:.2f}s)")
        return True
    else:
        logger.error(f"Teste Performance {test_name} falhou! RPS: {rps:.2f}, Latência: {latency:.2f}ms ({duration:.2f}s)")
        return False

class SimpleTestRunner:
    def __init__(self, max_workers=4):
        self.max_workers = max_workers
        self.test_queue = Queue()
        self.results = {'passed': 0, 'failed': 0, 'total': 0}
        self.lock = threading.Lock()
        self.logger = logging.getLogger()
    
    def add_test(self, test_func, test_name):
        self.test_queue.put((test_func, test_name))
    
    def worker(self):
        while not self.test_queue.empty():
            try:
                test_func, test_name = self.test_queue.get(block=False)
                
                result = test_func(test_name)
                
                with self.lock:
                    self.results['total'] += 1
                    if result:
                        self.results['passed'] += 1
                    else:
                        self.results['failed'] += 1
                
                self.test_queue.task_done()
            
            except Exception as e:
                self.logger.error(f"Erro ao executar teste: {e}")
    
    def run_tests(self):
        total_tests = self.test_queue.qsize()
        if total_tests == 0:
            self.logger.warning("Nenhum teste para executar!")
            return
        
        self.logger.info(f"Iniciando execução de {total_tests} testes com {self.max_workers} threads")
        start_time = time.time()
        
        threads = []
        for i in range(min(self.max_workers, total_tests)):
            thread = threading.Thread(target=self.worker, name=f"TestWorker-{i+1}")
            thread.daemon = True
            threads.append(thread)
            thread.start()
        
        for thread in threads:
            thread.join()
        
        end_time = time.time()
        duration = end_time - start_time
        
        self.logger.info(f"Todos os testes concluídos em {duration:.2f} segundos")
        self.logger.info(f"Resultados: {self.results['passed']} passaram, {self.results['failed']} falharam de {self.results['total']} testes")
        
        if self.results['total'] > 0:
            success_rate = (self.results['passed'] / self.results['total']) * 100
            self.logger.info(f"Taxa de sucesso: {success_rate:.2f}%")

def main():
    logger = setup_logging()
    logger.info("=== Iniciando execução de testes paralelos ===")
    
    runner = SimpleTestRunner(max_workers=3)
    
    for i in range(5):
        runner.add_test(test_func_api, f"Login-API-{i+1}")
        runner.add_test(test_func_api, f"UserData-API-{i+1}")
    
    for i in range(3):
        runner.add_test(test_func_ui, f"Login-UI-{i+1}")
        runner.add_test(test_func_ui, f"Dashboard-UI-{i+1}")
    
    runner.add_test(test_func_performance, "Homepage-Load")
    runner.add_test(test_func_performance, "API-Response-Time")
    
    runner.run_tests()
    
    logger.info("=== Execução de testes finalizada ===")

if __name__ == "__main__":
    main()