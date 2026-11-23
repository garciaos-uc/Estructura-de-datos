# Archivo: mezcla_directa_folios.py

def crear_archivo_folios(nombre_archivo):
    folios = [4508, 1023, 8912, 3340, 2150, 7641, 5019, 1290, 6432]
    with open(nombre_archivo, "w", encoding="utf-8") as archivo:
        for folio in folios:
            archivo.write(f"{folio}\n")


def leer_datos(nombre_archivo):
    with open(nombre_archivo, "r", encoding="utf-8") as archivo:
        return [int(linea.strip()) for linea in archivo if linea.strip()]


def escribir_datos(nombre_archivo, datos):
    with open(nombre_archivo, "w", encoding="utf-8") as archivo:
        for dato in datos:
            archivo.write(f"{dato}\n")


def particionar(archivo_principal, aux1, aux2, particion):
    datos = leer_datos(archivo_principal)
    lista_aux1 = []
    lista_aux2 = []
    turno_aux1 = True

    # Distribuye bloques de tamaño fijo (particion) alternando entre aux1 y aux2
    for i in range(0, len(datos), particion):
        bloque = datos[i:i + particion]
        if turno_aux1:
            lista_aux1.extend(bloque)
        else:
            lista_aux2.extend(bloque)
        turno_aux1 = not turno_aux1

    escribir_datos(aux1, lista_aux1)
    escribir_datos(aux2, lista_aux2)


def fusionar(archivo_principal, aux1, aux2, particion):
    datos_aux1 = leer_datos(aux1)
    datos_aux2 = leer_datos(aux2)
    resultado = []

    idx1 = 0
    idx2 = 0

    # Fusiona pares de bloques ordenados de tamaño 'particion'
    while idx1 < len(datos_aux1) or idx2 < len(datos_aux2):
        limite1 = min(idx1 + particion, len(datos_aux1))
        limite2 = min(idx2 + particion, len(datos_aux2))

        while idx1 < limite1 and idx2 < limite2:
            if datos_aux1[idx1] <= datos_aux2[idx2]:
                resultado.append(datos_aux1[idx1])
                idx1 += 1
            else:
                resultado.append(datos_aux2[idx2])
                idx2 += 1

        while idx1 < limite1:
            resultado.append(datos_aux1[idx1])
            idx1 += 1

        while idx2 < limite2:
            resultado.append(datos_aux2[idx2])
            idx2 += 1

    escribir_datos(archivo_principal, resultado)


def mezcla_directa(archivo_principal):
    total = len(leer_datos(archivo_principal))
    particion = 1

    # Duplica el tamaño de partición en cada pasada hasta cubrir todo el archivo
    while particion < total:
        particionar(archivo_principal, "aux1.txt", "aux2.txt", particion)
        fusionar(archivo_principal, "aux1.txt", "aux2.txt", particion)
        particion *= 2


def main():
    archivo = "folios_facturas.txt"
    crear_archivo_folios(archivo)
    print("Folios originales:", leer_datos(archivo))

    mezcla_directa(archivo)
    print("Folios ordenados: ", leer_datos(archivo))


if __name__ == "__main__":
    main()
    