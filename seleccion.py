# seleccion.py
# Ordenamiento por el Método de Selección (Selection Sort)
# Ejercicio: Ordenar el peso de paquetes de un almacén de menor a mayor

# Lista con los pesos originales de los 6 paquetes (en kilogramos)
pesos = [14.5, 3.2, 22.0, 8.7, 1.5, 17.3]

print("=== MÉTODO DE ORDENAMIENTO POR SELECCIÓN ===")
print(f"Pesos originales: {pesos}")

# Creamos una copia de la lista para no modificar la original
lista = pesos.copy()

# Obtenemos el número de elementos en la lista
n = len(lista)

# Bucle externo: en cada iteración se coloca el mínimo en su posición final
# La variable i representa el inicio de la parte sin ordenar
for i in range(n - 1):

    # Suponemos que el primer elemento de la parte sin ordenar es el mínimo
    indice_minimo = i

    # Recorremos el resto de la parte sin ordenar para buscar un valor menor
    for j in range(i + 1, n):

        # Si encontramos un elemento menor al mínimo actual, actualizamos el índice
        if lista[j] < lista[indice_minimo]:
            indice_minimo = j

    # Si el mínimo encontrado no es el que ya estaba en la posición i,
    # intercambiamos el mínimo encontrado con el elemento en la posición i
    if indice_minimo != i:
        lista[i], lista[indice_minimo] = lista[indice_minimo], lista[i]

print(f"Pesos ordenados:  {lista}")
print("\nOrden de despacho por peso (de menor a mayor):")
for num_paquete, peso in enumerate(lista, start=1):
    print(f"  Paquete {num_paquete}: {peso} kg")