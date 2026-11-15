# insercion.py
# Ordenamiento por el Método de Inserción (Insertion Sort)
# Ejercicio: Ordenar calificaciones finales de alumnos de menor a mayor

# Lista con las calificaciones originales de los 7 alumnos
calificaciones = [78, 95, 61, 88, 72, 100, 55]

print("=== MÉTODO DE ORDENAMIENTO POR INSERCIÓN ===")
print(f"Calificaciones originales: {calificaciones}")

# Creamos una copia de la lista para no modificar la original
lista = calificaciones.copy()

# Obtenemos el número de elementos en la lista
n = len(lista)

# El primer elemento se considera ya ordenado.
# El bucle comienza desde el segundo elemento (índice 1)
for i in range(1, n):

    # Guardamos el elemento actual que vamos a insertar en su lugar correcto
    elemento_actual = lista[i]

    # Comenzamos a comparar desde la posición anterior al elemento actual
    j = i - 1

    # Desplazamos hacia la derecha todos los elementos de la parte ordenada
    # que sean mayores que el elemento actual, para abrir un espacio
    while j >= 0 and lista[j] > elemento_actual:
        lista[j + 1] = lista[j]  # Mueve el elemento una posición a la derecha
        j -= 1  # Avanza hacia la izquierda para seguir comparando

    # Insertamos el elemento actual en la posición correcta que se abrió
    lista[j + 1] = elemento_actual

print(f"Calificaciones ordenadas: {lista}")
print("\nCalificaciones de menor a mayor:")
for posicion, cal in enumerate(lista, start=1):
    print(f"  Posición {posicion}: {cal} puntos")