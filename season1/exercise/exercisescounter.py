contador_chamadas = 0

def fatorial(n):
    global contador_chamadas
    contador_chamadas += 1
    
    print(f"Chamada fatorial({n})")
    
    if n <= 1:
        return 1
    else:
        resultado = n * fatorial(n-1)
        print(f"fatorial({n}) = {n} * fatorial({n-1}) = {n} * {resultado//n} = {resultado}")
        return resultado

contador_chamadas = 0
resultado = fatorial(5)
print(f"\nResultado final: {resultado}")
print(f"Número total de chamadas: {contador_chamadas}")