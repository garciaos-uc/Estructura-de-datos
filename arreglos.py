MESES = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
         "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]

DEPARTAMENTOS = ["Ropa", "Deportes", "Jugueteria"]

# Arreglo bidimensional: filas = meses (0-11), columnas = departamentos (0-2)
ventas = [[0 for _ in range(3)] for _ in range(12)]


# 1. Insertar un elemento en el arreglo
def insertar_venta(mes, departamento, valor):
    ventas[mes][departamento] = valor
    print(f"Venta insertada: {MESES[mes]} - {DEPARTAMENTOS[departamento]} = {valor}")


# 2. Buscar un elemento en particular
def buscar_venta(mes, departamento):
    valor = ventas[mes][departamento]
    print(f"Venta encontrada en {MESES[mes]} - {DEPARTAMENTOS[departamento]}: {valor}")
    return valor


# 3. Eliminar una venta en particular de algún departamento
def eliminar_venta(mes, departamento):
    ventas[mes][departamento] = 0
    print(f"Venta eliminada en {MESES[mes]} - {DEPARTAMENTOS[departamento]}")


# Muestra la tabla completa de ventas (meses x departamentos)
def mostrar_tabla():
    print(f"\n{'':<12}{'Ropa':<10}{'Deportes':<10}{'Jugueteria':<10}")
    for i in range(12):
        print(f"{MESES[i]:<12}{ventas[i][0]:<10}{ventas[i][1]:<10}{ventas[i][2]:<10}")


def elegir_mes():
    print("\nMeses:")
    for i, m in enumerate(MESES):
        print(f"{i}. {m}")
    while True:
        entrada = input("Elige el numero o nombre del mes: ").strip()
        if entrada.isdigit() and 0 <= int(entrada) < 12:
            return int(entrada)
        for i, m in enumerate(MESES):
            if entrada.lower() == m.lower():
                return i
        print("Mes invalido, intenta de nuevo.")


def elegir_departamento():
    print("\nDepartamentos:")
    for i, d in enumerate(DEPARTAMENTOS):
        print(f"{i}. {d}")
    while True:
        entrada = input("Elige el numero o nombre del departamento: ").strip()
        if entrada.isdigit() and 0 <= int(entrada) < 3:
            return int(entrada)
        for i, d in enumerate(DEPARTAMENTOS):
            if entrada.lower() == d.lower():
                return i
        print("Departamento invalido, intenta de nuevo.")


def menu():
    while True:
        print("\n----- MENU -----")
        print("1. Insertar venta")
        print("2. Buscar venta")
        print("3. Eliminar venta")
        print("4. Ver tabla de ventas")
        print("5. Salir")
        opcion = input("Elige una opcion: ")

        if opcion == "1":
            mes = elegir_mes()
            depto = elegir_departamento()
            valor = float(input("Valor de la venta: "))
            insertar_venta(mes, depto, valor)
            mostrar_tabla()

        elif opcion == "2":
            mes = elegir_mes()
            depto = elegir_departamento()
            buscar_venta(mes, depto)

        elif opcion == "3":
            mes = elegir_mes()
            depto = elegir_departamento()
            eliminar_venta(mes, depto)
            mostrar_tabla()

        elif opcion == "4":
            mostrar_tabla()

        elif opcion == "5":
            print("Saliendo del programa...")
            break

        else:
            print("Opcion invalida, intenta de nuevo.")


if __name__ == "__main__":
    menu()