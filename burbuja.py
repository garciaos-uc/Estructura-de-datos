# burbuja.py
# Ordenamiento por el Método Burbuja (Bubble Sort)
# Ejercicio: Ordenar precios de artículos de una tienda deportiva de menor a mayor

# Lista con los precios originales de los 8 artículos (en pesos)
precios = [350, 120, 875, 60, 430, 210, 990, 75]

print("=== MÉTODO DE ORDENAMIENTO BURBUJA ===")
print(f"Lista original: {precios}")

# Creamos una copia de la lista para no modificar la original
lista = precios.copy()

# Obtenemos el número de elementos en la lista
n = len(lista)

# Bucle externo: controla el número de pasadas sobre la lista
# En cada pasada, el elemento más grande "burbujea" hasta el final
for i in range(n - 1):

    # Bandera para detectar si se realizó algún intercambio en esta pasada
    # Si no hubo intercambios, la lista ya está ordenada y se puede detener
    hubo_intercambio = False

    # Bucle interno: compara elementos adyacentes
    # Con cada pasada (i), los últimos i elementos ya están ordenados,
    # por eso se reduce el rango con (n - 1 - i)
    for j in range(n - 1 - i):

        # Si el elemento actual es mayor que el siguiente, se intercambian
        if lista[j] > lista[j + 1]:
            lista[j], lista[j + 1] = lista[j + 1], lista[j]
            hubo_intercambio = True  # Se registra que hubo un intercambio

    # Si no hubo ningún intercambio en esta pasada, la lista ya está ordenada
    if not hubo_intercambio:
        break  # Se detiene el algoritmo anticipadamente

print(f"Lista ordenada:  {lista}")
print("\nLos precios ordenados de menor a mayor son:")
for idx, precio in enumerate(lista, start=1):
    print(f"  Artículo {idx}: ${precio}")