class Nodo:
    def __init__(self):
        self.info = None   # INFO: dato que se almacena
        self.liga = None   # LIGA: apuntador al siguiente nodo (NIL = None)


def crear_inicio():
    """Agrega cada nuevo nodo al INICIO de la lista."""
    # 1. Crear (P): se crea el primer nodo
    p = Nodo()

    # 2. Leer P^.INFO
    p.info = input("Ingrese el dato del nodo: ")

    # 3. P^.LIGA <- NIL
    p.liga = None

    # 4 y 5. Preguntar si desea ingresar más nodos y leer RES
    res = int(input("¿Desea ingresar más nodos a la lista? Sí: 1, No: 0: "))

    # 6. Mientras (RES = 1) Repetir
    while res == 1:
        q = Nodo()                                    # Crear (Q)
        q.info = input("Ingrese el dato del nodo: ")  # Leer Q^.INFO
        q.liga = p                                    # Q^.LIGA <- P
        p = q                                         # P <- Q
        res = int(input("¿Desea ingresar más nodos a la lista? Sí: 1, No: 0: "))
    # 7. Fin del ciclo

    return p  # P apunta al inicio de la lista


def crea_final():
    """Agrega cada nuevo nodo al FINAL de la lista."""
    # 1. Crear (P): se crea el primer nodo de la lista
    p = Nodo()

    # 2. Leer P^.INFO
    p.info = input("Ingrese el dato del nodo: ")

    # 3. P^.LIGA <- NIL  y  T <- P
    p.liga = None
    t = p                                             # T apunta al último nodo

    # 4 y 5. Preguntar si desea ingresar más nodos y leer RES
    res = int(input("¿Desea ingresar más nodos a la lista? Sí: 1, No: 0: "))

    # 6. Mientras (RES = 1) Repetir
    while res == 1:
        q = Nodo()                                    # Crear (Q)
        q.info = input("Ingrese el dato del nodo: ")  # Leer Q^.INFO
        q.liga = None                                 # Q^.LIGA <- NIL
        t.liga = q                                    # T^.LIGA <- Q
        t = q                                         # T <- Q (T apunta al último nodo)
        res = int(input("¿Desea ingresar más nodos a la lista? Sí: 1, No: 0: "))
    # 7. Fin del ciclo

    return p  # P sigue apuntando al inicio de la lista


def imprimir_lista(p):
    print("\nContenido de la lista:")
    actual = p
    while actual is not None:
        print(actual.info, end=" -> ")
        actual = actual.liga
    print("NIL")


# Programa principal
print("=== Crear lista agregando al INICIO ===")
lista1 = crear_inicio()
imprimir_lista(lista1)

print("\n=== Crear lista agregando al FINAL ===")
lista2 = crea_final()
imprimir_lista(lista2)