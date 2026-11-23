# Archivo: intercalacion_sucursales.py

def crear_archivos_iniciales():
    # Datos previamente ordenados de forma ascendente en cada sucursal
    codigos_norte = [102, 115, 130, 148, 205]
    codigos_sur = [105, 115, 140, 190, 210, 250]

    with open("sucursal_norte.txt", "w", encoding="utf-8") as f_norte:
        for codigo in codigos_norte:
            f_norte.write(f"{codigo}\n")

    with open("sucursal_sur.txt", "w", encoding="utf-8") as f_sur:
        for codigo in codigos_sur:
            f_sur.write(f"{codigo}\n")


def leer_datos(nombre_archivo):
    with open(nombre_archivo, "r", encoding="utf-8") as archivo:
        return [int(linea.strip()) for linea in archivo if linea.strip()]


def intercalar_archivos(archivo_a, archivo_b, archivo_salida):
    lista_a = leer_datos(archivo_a)
    lista_b = leer_datos(archivo_b)

    i = 0  # Índice para sucursal_norte
    j = 0  # Índice para sucursal_sur

    with open(archivo_salida, "w", encoding="utf-8") as f_salida:
        # Compara elemento por elemento mientras ambos archivos tengan datos
        while i < len(lista_a) and j < len(lista_b):
            if lista_a[i] <= lista_b[j]:
                f_salida.write(f"{lista_a[i]}\n")
                i += 1
            else:
                f_salida.write(f"{lista_b[j]}\n")
                j += 1

        # Copia los elementos restantes del archivo que aún no termina
        while i < len(lista_a):
            f_salida.write(f"{lista_a[i]}\n")
            i += 1

        while j < len(lista_b):
            f_salida.write(f"{lista_b[j]}\n")
            j += 1


def main():
    crear_archivos_iniciales()
    intercalar_archivos("sucursal_norte.txt", "sucursal_sur.txt", "inventario_consolidado.txt")
    resultado = leer_datos("inventario_consolidado.txt")
    print("Inventario consolidado ordenado:", resultado)


if __name__ == "__main__":
    main()