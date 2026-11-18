def amontonar(lista, n, i):
    # Inicializamos el nodo más grande como la raíz del subárbol
    mayor = i
    izquierda = 2 * i + 1
    derecha = 2 * i + 2

    # Verificamos si el hijo izquierdo existe y es mayor que la raíz
    if izquierda < n and lista[izquierda] > lista[mayor]:
        mayor = izquierda

    # Verificamos si el hijo derecho existe y es mayor que el mayor actual
    if derecha < n and lista[derecha] > lista[mayor]:
        mayor = derecha

    # Si el mayor no es la raíz, intercambiamos y seguimos ajustando el subárbol
    if mayor != i:
        lista[i], lista[mayor] = lista[mayor], lista[i]
        amontonar(lista, n, mayor)


def heap_sort(lista):
    n = len(lista)

    # Paso 1: Construir un montículo máximo (Max-Heap) reorganizando la lista
    for i in range(n // 2 - 1, -1, -1):
        amontonar(lista, n, i)

    # Paso 2: Extraer los elementos uno por uno desde el montículo
    for i in range(n - 1, 0, -1):
        # Movemos la raíz actual (el número más grande) al final de la lista
        lista[i], lista[0] = lista[0], lista[i]
        # Reajustamos el montículo reducido para volver a subir el siguiente mayor
        amontonar(lista, i, 0)


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
        print("\n--- MENÚ DE ORDENAMIENTO: HEAPSORT ---")
        print("1. Ingresar números y ordenar")
        print("2. Salir")
        opcion = input("Selecciona una opción (1-2): ")

        if opcion == "1":
            originales = solicitar_datos()
            ordenados = [x for x in originales]
            heap_sort(ordenados)

            print("\n--- RESULTADOS ---")
            print("Lista original:", originales)
            print("Lista ordenada:", ordenados)
        elif opcion == "2":
            print("Saliendo del programa Heapsort...")
            break
        else:
            print("Opción no válida. Intenta de nuevo.")


if __name__ == "__main__":
    menu()