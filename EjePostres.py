import unicodedata


class NodoIngrediente:
    def __init__(self, nombre):
        self.nombre = nombre
        self.siguiente = None


class Postre:
    def __init__(self, nombre):
        self.nombre = nombre
        self.primero = None


def limpiar(texto):
    return " ".join(texto.split())


def clave(texto):
    texto = limpiar(texto).casefold()
    texto = unicodedata.normalize("NFD", texto)
    return "".join(c for c in texto if unicodedata.category(c) != "Mn")


def lista_de_ingredientes(postre):
    nombres = []
    nodo = postre.primero
    while nodo is not None:
        nombres.append(nodo.nombre)
        nodo = nodo.siguiente
    return nombres


def existe_ingrediente(postre, nombre):
    nodo = postre.primero
    while nodo is not None:
        if clave(nodo.nombre) == clave(nombre):
            return True
        nodo = nodo.siguiente
    return False


def agregar_ingrediente(postre, nombre, mostrar=True):
    nombre = limpiar(nombre)
    if nombre == "":
        if mostrar:
            print("  ! El nombre del ingrediente no puede estar vacío.")
        return False
    if existe_ingrediente(postre, nombre):
        if mostrar:
            print(f"  ! '{nombre}' ya está en {postre.nombre}; no se repite.")
        return False

    nuevo = NodoIngrediente(nombre)
    if postre.primero is None:
        postre.primero = nuevo
    else:
        ultimo = postre.primero
        while ultimo.siguiente is not None:
            ultimo = ultimo.siguiente
        ultimo.siguiente = nuevo
    if mostrar:
        print(f"  + '{nombre}' agregado a {postre.nombre}.")
    return True


def eliminar_ingrediente(postre, nombre):
    nombre = limpiar(nombre)
    if nombre == "":
        print("  ! El nombre del ingrediente no puede estar vacío.")
        return False
    if postre.primero is None:
        print(f"  ! {postre.nombre} no tiene ingredientes que eliminar.")
        return False

    anterior = None
    actual = postre.primero
    while actual is not None and clave(actual.nombre) != clave(nombre):
        anterior = actual
        actual = actual.siguiente

    if actual is None:
        print(f"  ! '{nombre}' no pertenece a la lista de {postre.nombre}.")
        return False

    if anterior is None:
        postre.primero = actual.siguiente
    else:
        anterior.siguiente = actual.siguiente
    print(f"  - '{actual.nombre}' eliminado de {postre.nombre}.")
    return True


def buscar_postre(postres, nombre):
    for posicion in range(len(postres)):
        if clave(postres[posicion].nombre) == clave(nombre):
            return posicion
    return -1


def insertar_ordenado(postres, nuevo):
    posicion = 0
    while posicion < len(postres) and clave(postres[posicion].nombre) <= clave(nuevo.nombre):
        posicion += 1
    postres.insert(posicion, nuevo)
    return posicion


def crear_postre(nombre, ingredientes):
    postre = Postre(limpiar(nombre))
    for ingrediente in ingredientes:
        agregar_ingrediente(postre, ingrediente, mostrar=False)
    return postre


def datos_de_ejemplo():
    postres = []
    datos = [
        ("Flan", ["leche", "huevo", "azúcar", "vainilla"]),
        ("Brownie", ["chocolate", "harina", "huevo", "mantequilla"]),
        ("Gelatina", ["grenetina", "agua", "azúcar"]),
        ("Arroz con leche", ["arroz", "leche", "canela"]),
        ("Pastel vacío", []),
    ]
    for nombre, ingredientes in datos:
        insertar_ordenado(postres, crear_postre(nombre, ingredientes))
    return postres


def mostrar_estructura(postres, titulo="POSTRES"):
    print(f"\n--- {titulo} ({len(postres)} postres) ---")
    if len(postres) == 0:
        print("  (estructura vacía)")
    for posicion in range(len(postres)):
        if not isinstance(postres[posicion], Postre):
            print(f"  [{posicion}] (elemento inválido: {postres[posicion]!r})")
            continue
        ingredientes = lista_de_ingredientes(postres[posicion])
        if ingredientes:
            texto = " -> ".join(ingredientes)
        else:
            texto = "(sin ingredientes)"
        print(f"  [{posicion}] {postres[posicion].nombre}: {texto}")


def pedir_texto(mensaje):
    return limpiar(input(mensaje))


def pedir_postre_existente(postres):
    if len(postres) == 0:
        print("  ! No hay postres registrados.")
        return -1
    nombre = pedir_texto("Nombre del postre: ")
    if nombre == "":
        print("  ! El nombre del postre no puede estar vacío.")
        return -1
    posicion = buscar_postre(postres, nombre)
    if posicion == -1:
        print(f"  ! El postre '{nombre}' no existe.")
    return posicion


def opcion_consultar(postres):
    posicion = pedir_postre_existente(postres)
    if posicion == -1:
        return
    postre = postres[posicion]
    ingredientes = lista_de_ingredientes(postre)
    if not ingredientes:
        print(f"  {postre.nombre} no tiene ingredientes registrados.")
        return
    print(f"  Ingredientes de {postre.nombre}:")
    for numero, ingrediente in enumerate(ingredientes, start=1):
        print(f"    {numero}. {ingrediente}")


def opcion_agregar(postres):
    posicion = pedir_postre_existente(postres)
    if posicion == -1:
        return
    postre = postres[posicion]
    agregados = 0
    while True:
        ingrediente = pedir_texto("Ingrediente a agregar (Enter para terminar): ")
        if ingrediente == "":
            break
        if agregar_ingrediente(postre, ingrediente):
            agregados += 1
    if agregados == 0:
        print("  No se agregó ningún ingrediente.")


def opcion_eliminar_ingrediente(postres):
    posicion = pedir_postre_existente(postres)
    if posicion == -1:
        return
    postre = postres[posicion]
    if postre.primero is None:
        print(f"  ! {postre.nombre} no tiene ingredientes que eliminar.")
        return
    print("  Ingredientes actuales:", ", ".join(lista_de_ingredientes(postre)))
    ingrediente = pedir_texto("Ingrediente a eliminar: ")
    eliminar_ingrediente(postre, ingrediente)


def opcion_alta(postres):
    nombre = pedir_texto("Nombre del postre nuevo: ")
    if nombre == "":
        print("  ! El nombre del postre no puede estar vacío.")
        return
    if buscar_postre(postres, nombre) != -1:
        print(f"  ! El postre '{nombre}' ya existe; no se permiten duplicados.")
        return
    nuevo = Postre(nombre)
    print("  Escribe sus ingredientes (Enter vacío para terminar):")
    while True:
        ingrediente = pedir_texto("    Ingrediente: ")
        if ingrediente == "":
            break
        agregar_ingrediente(nuevo, ingrediente)
    if nuevo.primero is None:
        print("  (El postre se registrará sin ingredientes.)")
    posicion = insertar_ordenado(postres, nuevo)
    print(f"  Postre '{nuevo.nombre}' dado de alta en la posición {posicion}.")


def opcion_baja(postres):
    posicion = pedir_postre_existente(postres)
    if posicion == -1:
        return
    postre = postres[posicion]
    total = len(lista_de_ingredientes(postre))
    respuesta = pedir_texto(f"¿Eliminar '{postre.nombre}' y sus {total} ingredientes? (s/n): ")
    if respuesta.lower() != "s":
        print("  Operación cancelada.")
        return

    del postres[posicion]
    print(f"  Postre '{postre.nombre}' dado de baja junto con sus ingredientes.")


def menu():
    postres = datos_de_ejemplo()
    while True:
        print("\n===== MENÚ POSTRES =====")
        print("1. Consultar ingredientes de un postre")
        print("2. Agregar ingredientes a un postre")
        print("3. Eliminar un ingrediente de un postre")
        print("4. Dar de alta un postre")
        print("5. Dar de baja un postre")
        print("6. Ver todos los postres")
        print("0. Salir")
        opcion = input("Elige una opción: ").strip()

        if opcion == "1":
            opcion_consultar(postres)
        elif opcion == "2":
            opcion_agregar(postres)
        elif opcion == "3":
            opcion_eliminar_ingrediente(postres)
        elif opcion == "4":
            opcion_alta(postres)
        elif opcion == "5":
            opcion_baja(postres)
        elif opcion == "6":
            mostrar_estructura(postres)
        elif opcion == "0":
            print("Hasta luego.")
            break
        else:
            print("  ! Opción no válida. Elige un número del menú.")


if __name__ == "__main__":
    try:
        menu()
    except (EOFError, KeyboardInterrupt):
        print("\nPrograma terminado.")