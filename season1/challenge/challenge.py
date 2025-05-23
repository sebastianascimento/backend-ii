def bubble_sort_otimizado(lista):
    n = len(lista)
    
    for i in range(n):
        trocou = False
        
        for j in range(0, n - i - 1):
            if lista[j] > lista[j + 1]:
                lista[j], lista[j + 1] = lista[j + 1], lista[j]
                trocou = True
        
        if not trocou:
            print(f"Lista ordenada após {i+1} passagens de {n} possíveis!")
            break
            
    return lista

lista1 = [64, 34, 25, 12, 22, 11, 90]
print("Lista original:", lista1)
bubble_sort_otimizado(lista1)
print("Lista ordenada:", lista1)

lista2 = [1, 2, 3, 5, 4]
print("\nLista quase ordenada:", lista2)
bubble_sort_otimizado(lista2)
print("Lista ordenada:", lista2)