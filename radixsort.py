def ordenar_por_digito(lista, posicion_decimal):
    n = len(lista)
    salida = [0] * n
    # Arreglo de conteo para los dígitos del 0 al 9
    conteo = [0] * 10

    # Contamos cuántas veces aparece cada dígito en la posición actual
    for i in range(n):
        indice = (lista[i] // posicion_decimal) % 10
        conteo[indice] += 1

    # Acumulamos los conteos para saber las posiciones reales en la lista de salida
    for i in range(1, 10):
        conteo[i] += conteo[i - 1]

    # Construimos la lista ordenada recorriendo de derecha a izquierda para mantener estabilidad
    i = n - 1
    while i >= 0:
        indice = (lista[i] // posicion_decimal) % 10
        salida[conteo[indice] - 1] = lista[i]
        conteo[indice] -= 1
        i -= 1

    # Copiamos el resultado parcial de vuelta a la lista original
    for i in range(n):
        lista[i] = salida[i]


def radix_sort(lista):
    if len(lista) == 0:
        return

    # Encontramos manualmente el número mayor para saber cuántas cifras tiene
    maximo = lista[0]
    for num in lista:
        if num > maximo:
            maximo = num

    # Aplicamos el ordenamiento por conteo para cada posición decimal (1, 10, 100...)
    posicion_decimal = 1
    while maximo // posicion_decimal > 0:
        ordenar_por_digito(lista, posicion_decimal)
        posicion_decimal *= 10


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
    print("Nota: Este algoritmo trabaja con números enteros positivos (0 o mayores).")
    for i in range(cantidad):
        while True:
            try:
                num = int(input(f"Ingresa el número {i + 1}: "))
                if num < 0:
                    print("Por favor, ingresa un número entero positivo o cero.")
                    continue
                numeros.append(num)
                break
            except ValueError:
                print("Entrada no válida. Ingresa un número entero.")
    return numeros


def menu():
    while True:
        print("\n--- MENÚ DE ORDENAMIENTO: RADIX SORT ---")
        print("1. Ingresar números y ordenar")
        print("2. Salir")
        opcion = input("Selecciona una opción (1-2): ")

        if opcion == "1":
            originales = solicitar_datos()
            ordenados = [x for x in originales]
            radix_sort(ordenados)

            print("\n--- RESULTADOS ---")
            print("Lista original:", originales)
            print("Lista ordenada:", ordenados)
        elif opcion == "2":
            print("Saliendo del programa Radix Sort...")
            break
        else:
            print("Opción no válida. Intenta de nuevo.")


if __name__ == "__main__":
    menu()