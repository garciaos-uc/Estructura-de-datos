def particion(lista, inicio, fin):
    # Elegimos el último elemento de la sublista como pivote
    pivote = lista[fin]
    # Índice del elemento más pequeño
    i = inicio - 1

    for j in range(inicio, fin):
        # Si el elemento actual es menor o igual al pivote, lo movemos a la izquierda
        if lista[j] <= pivote:
            i += 1
            lista[i], lista[j] = lista[j], lista[i]

    # Colocamos el pivote en su posición definitiva (entre menores y mayores)
    lista[i + 1], lista[fin] = lista[fin], lista[i + 1]
    return i + 1


def quick_sort(lista, inicio, fin):
    # Caso base: mientras la sublista tenga al menos dos elementos
    if inicio < fin:
        # Obtenemos el índice donde quedó ubicado el pivote
        indice_pivote = particion(lista, inicio, fin)
        # Ordenamos recursivamente la mitad izquierda y la mitad derecha
        quick_sort(lista, inicio, indice_pivote - 1)
        quick_sort(lista, indice_pivote + 1, fin)


def solicitar_datos():
    while True:
        try:
            cantidad = int(input("\n¿Cuántos números deseas ordenar?: "))
            if cantidad <= 0:
                print("Por favor, ingresa una cantidad mayor a cero.")
                continue
            break
        except ValueError:
            print("Entrada no válida. Ingresa un número entero.")

    numeros = []
    for i in range(cantidad):
        while True:
            try:
                num = int(input(f"Ingresa el número {i + 1}: "))
                numeros.append(num)
                break
            except ValueError:
                print("Entrada no válida. Ingresa un número entero.")
    return numeros


def menu():
    while True:
        print("\n--- MENÚ DE ORDENAMIENTO: QUICKSORT ---")
        print("1. Ingresar números y ordenar")
        print("2. Salir")
        opcion = input("Selecciona una opción (1-2): ")

        if opcion == "1":
            originales = solicitar_datos()
            ordenados = [x for x in originales]
            quick_sort(ordenados, 0, len(ordenados) - 1)

            print("\n--- RESULTADOS ---")
            print("Lista original:", originales)
            print("Lista ordenada:", ordenados)
        elif opcion == "2":
            print("Saliendo del programa Quicksort...")
            break
        else:
            print("Opción no válida. Intenta de nuevo.")


if __name__ == "__main__":
    menu()