def shell_sort(lista):
    # Obtenemos la cantidad de elementos en la lista
    n = len(lista)
    # Iniciamos el salto (gap) a la mitad del tamaño de la lista
    salto = n // 2

    # Continuamos mientras el salto sea mayor que 0
    while salto > 0:
        # Recorremos la lista desde la posición del salto hasta el final
        for i in range(salto, n):
            temp = lista[i]
            j = i
            # Comparamos y desplazamos elementos separados por el valor de 'salto'
            while j >= salto and lista[j - salto] > temp:
                lista[j] = lista[j - salto]
                j -= salto
            # Colocamos el elemento temporal en su posición correcta
            lista[j] = temp
        # Reducimos el salto a la mitad para la siguiente pasada
        salto //= 2


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
        print("\n--- MENÚ DE ORDENAMIENTO: SHELLSORT ---")
        print("1. Ingresar números y ordenar")
        print("2. Salir")
        opcion = input("Selecciona una opción (1-2): ")

        if opcion == "1":
            originales = solicitar_datos()
            # Hacemos una copia manual para conservar la lista original intacta
            ordenados = [x for x in originales]
            shell_sort(ordenados)

            print("\n--- RESULTADOS ---")
            print("Lista original:", originales)
            print("Lista ordenada:", ordenados)
        elif opcion == "2":
            print("Saliendo del programa ShellSort...")
            break
        else:
            print("Opción no válida. Intenta de nuevo.")


if __name__ == "__main__":
    menu()