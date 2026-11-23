# Archivo: mezcla_equilibrada_temperaturas.py

def crear_archivo_temperaturas(nombre_archivo):
    # Registros en °C que contienen tramos naturalmente ordenados de forma ascendente
    lecturas = [18.5, 20.1, 22.4, 19.0, 21.3, 25.6, 27.8, 23.1, 24.0, 26.2]
    with open(nombre_archivo, "w", encoding="utf-8") as archivo:
        for temp in lecturas:
            archivo.write(f"{temp}\n")


def leer_datos(nombre_archivo):
    with open(nombre_archivo, "r", encoding="utf-8") as archivo:
        return [float(linea.strip()) for linea in archivo if linea.strip()]


def escribir_datos(nombre_archivo, datos):
    with open(nombre_archivo, "w", encoding="utf-8") as archivo:
        for dato in datos:
            archivo.write(f"{dato}\n")


def distribuir_tramos(archivo_principal, aux_a, aux_b):
    datos = leer_datos(archivo_principal)
    if not datos:
        return 0

    lista_a = []
    lista_b = []
    en_aux_a = True
    cantidad_tramos = 1

    lista_a.append(datos[0])

    # Detecta secuencias ascendentes naturales y las alterna entre aux_a y aux_b
    for i in range(1, len(datos)):
        if datos[i] < datos[i - 1]:
            en_aux_a = not en_aux_a
            cantidad_tramos += 1

        if en_aux_a:
            lista_a.append(datos[i])
        else:
            lista_b.append(datos[i])

    escribir_datos(aux_a, lista_a)
    escribir_datos(aux_b, lista_b)
    return cantidad_tramos


def obtener_fin_tramo(lista, inicio):
    fin = inicio
    while fin + 1 < len(lista) and lista[fin + 1] >= lista[fin]:
        fin += 1
    return fin


def fusionar_tramos(archivo_principal, aux_a, aux_b):
    datos_a = leer_datos(aux_a)
    datos_b = leer_datos(aux_b)
    resultado = []

    idx_a = 0
    idx_b = 0

    # Fusiona cada tramo natural de aux_a con su correspondiente tramo en aux_b
    while idx_a < len(datos_a) and idx_b < len(datos_b):
        fin_a = obtener_fin_tramo(datos_a, idx_a)
        fin_b = obtener_fin_tramo(datos_b, idx_b)

        while idx_a <= fin_a and idx_b <= fin_b:
            if datos_a[idx_a] <= datos_b[idx_b]:
                resultado.append(datos_a[idx_a])
                idx_a += 1
            else:
                resultado.append(datos_b[idx_b])
                idx_b += 1

        while idx_a <= fin_a:
            resultado.append(datos_a[idx_a])
            idx_a += 1

        while idx_b <= fin_b:
            resultado.append(datos_b[idx_b])
            idx_b += 1

    # Copia los tramos sobrantes si uno de los auxiliares tenía un tramo adicional
    while idx_a < len(datos_a):
        resultado.append(datos_a[idx_a])
        idx_a += 1

    while idx_b < len(datos_b):
        resultado.append(datos_b[idx_b])
        idx_b += 1

    escribir_datos(archivo_principal, resultado)


def mezcla_equilibrada(archivo_principal):
    while True:
        tramos = distribuir_tramos(archivo_principal, "aux_a.txt", "aux_b.txt")
        # Si solo existe 1 tramo ordenado, el archivo ya está completamente ordenado
        if tramos <= 1:
            break
        fusionar_tramos(archivo_principal, "aux_a.txt", "aux_b.txt")


def main():
    archivo = "lecturas_sensor.txt"
    crear_archivo_temperaturas(archivo)
    print("Lecturas originales:", leer_datos(archivo))

    mezcla_equilibrada(archivo)
    print("Lecturas ordenadas: ", leer_datos(archivo))


if __name__ == "__main__":
    main()