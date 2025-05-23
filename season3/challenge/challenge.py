import threading
import urllib.request
import os
import time
from urllib.parse import urlparse

def download_file(url, output_directory="downloads"):
    """
    Função para baixar um arquivo de uma URL
    """
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)
    
    parsed_url = urlparse(url)
    filename = os.path.basename(parsed_url.path)
    
    if not filename:
        filename = f"file_{int(time.time())}.dat"
    
    filepath = os.path.join(output_directory, filename)
    
    try:
        print(f"Iniciando download de: {url}")
        start_time = time.time()
        
        urllib.request.urlretrieve(url, filepath)
        
        end_time = time.time()
        download_time = end_time - start_time
        
        print(f"Download completo: {filename} em {download_time:.2f} segundos")
        return True
    
    except Exception as e:
        print(f"Erro ao baixar {url}: {e}")
        return False

def main():
    urls = [
        "https://www.iana.org/sites/default/files/iana-logo-header_0.jpg",
        "https://www.python.org/static/community_logos/python-logo.png",
        "https://docs.python.org/3/archives/python-3.9.1-docs-pdf-a4.zip",
        "https://www.gutenberg.org/files/1342/1342-0.txt", 
        "https://www.gutenberg.org/cache/epub/84/pg84.txt", 
        "https://www.gutenberg.org/files/2701/2701-0.txt"   
    ]
    
    print(f"Iniciando download de {len(urls)} arquivos...")
    
    threads = []
    
    for url in urls:
        thread = threading.Thread(target=download_file, args=(url,))
        threads.append(thread)
        thread.start()
    
    for thread in threads:
        thread.join()
    
    print("Todos os downloads foram concluídos!")

if __name__ == "__main__":
    main()