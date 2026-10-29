from EjePostres import (
    Postre, clave, limpiar, crear_postre, insertar_ordenado,
    lista_de_ingredientes, mostrar_estructura,
)


def datos_con_repetidos():
    postres = []
    flan = crear_postre("Flan", ["leche", "huevo", "azúcar", "vainilla"])
    brownie = crear_postre("Brownie", ["chocolate", "harina", "huevo", "mantequilla"])

    flan_repetido = crear_postre("Flan", ["leche", "huevo", "caramelo"])

    gelatina = crear_postre("Gelatina", ["grenetina", "agua", "azúcar"])
    gelatina_repetida = crear_postre("gelatina", ["grenetina", "agua", "azúcar"])

    brownie_compartido = Postre("Brownie")
    brownie_compartido.primero = brownie.primero

    arroz = crear_postre("Arroz con leche", ["arroz", "leche", "canela"])

    for postre in (flan, brownie, flan_repetido, gelatina, gelatina_repetida,
                   brownie_compartido, arroz):
        insertar_ordenado(postres, postre)
    return postres


def eliminar_repetidos(postres):
    conservados = []
    eliminados = []
    vistos = {}

    for elemento in postres:
        if not isinstance(elemento, Postre) or limpiar(str(elemento.nombre)) == "":
            print("  ! Elemento inválido o sin nombre, se omite:", repr(elemento))
            continue

        nombre_clave = clave(elemento.nombre)
        if nombre_clave in vistos:
            eliminados.append((elemento, vistos[nombre_clave]))
        else:
            vistos[nombre_clave] = elemento
            conservados.append(elemento)

    conservados.sort(key=lambda postre: clave(postre.nombre))
    postres[:] = conservados
    return eliminados


def reportar_eliminados(eliminados):
    if not eliminados:
        print("  No había postres repetidos; no se eliminó nada.")
        return
    for repetido, conservado in eliminados:
        ing_repetido = lista_de_ingredientes(repetido)
        ing_conservado = lista_de_ingredientes(conservado)
        print(f"  * '{repetido.nombre}' (repetido) -> se elimina; se conserva '{conservado.nombre}'")
        if repetido.primero is conservado.primero and repetido.primero is not None:
            print("      Comparte la MISMA lista enlazada que el conservado: "
                  "no se pierde nada,")
            print("      la lista sigue accesible desde el postre que se conserva.")
            continue
        perdidos = [i for i in ing_repetido
                    if clave(i) not in [clave(c) for c in ing_conservado]]
        if not ing_repetido:
            print("      No tenía ingredientes: no se pierde nada.")
        elif not perdidos:
            print("      Sus ingredientes ya estaban en el conservado: no se pierde nada.")
        else:
            print("      Ingredientes que se pierden con la eliminación:", ", ".join(perdidos))


def ejecutar_prueba(titulo, postres):
    print("\n" + "=" * 60)
    print(titulo)
    print("=" * 60)
    try:
        mostrar_estructura(postres, "ANTES")
        eliminados = eliminar_repetidos(postres)
        print("\nPostres repetidos encontrados:", len(eliminados))
        reportar_eliminados(eliminados)
        mostrar_estructura(postres, "DESPUÉS")
    except Exception as error:
        print(f"  ! Ocurrió un error y se controló: {type(error).__name__}: {error}")


def main():
    postres = datos_con_repetidos()
    ejecutar_prueba("PRUEBA 1: estructura con postres repetidos", postres)

    posicion = [clave(p.nombre) for p in postres].index("brownie")
    print("\nComprobación: Brownie conservado ->",
          ", ".join(lista_de_ingredientes(postres[posicion])))

    ejecutar_prueba("PRUEBA 2: segunda ejecución, ya sin repetidos", postres)

    ejecutar_prueba("PRUEBA 3: estructura vacía", [])

    dañado = [crear_postre("Flan", ["leche"]), None, crear_postre("Flan", ["huevo"])]
    ejecutar_prueba("PRUEBA 4: arreglo con un elemento dañado", dañado)


if __name__ == "__main__":
    main()