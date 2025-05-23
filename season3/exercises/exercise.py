import threading
import time

def print_letters():
    for letter in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
        print(f"Thread de Letras: {letter}")
        time.sleep(0.1)

def print_numbers():
    for number in range(1, 27):
        print(f"Thread de Números: {number}")
        time.sleep(0.1)

def main():
    print("Iniciando programa de threads concorrentes...")
    
    thread_letters = threading.Thread(target=print_letters, name="LettersThread")
    thread_numbers = threading.Thread(target=print_numbers, name="NumbersThread")
    
    thread_letters.start()
    thread_numbers.start()
    
    thread_letters.join()
    thread_numbers.join()
    
    print("Ambas as threads terminaram.")

if __name__ == "__main__":
    main()