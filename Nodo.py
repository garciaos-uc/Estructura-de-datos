class Nodo:
    def __init__(self):
        self.info = None   # INFO: dato que se almacena
        self.liga = None   # LIGA: apuntador al siguiente nodo (NIL = None)


# ---------------------------------------------------------
# 1. Crear lista agregando al INICIO
# ---------------------------------------------------------
def crear_inicio():
    p = Nodo()                                        # Crear (P)
    p.info = input("Ingrese el dato del nodo: ")      # Leer P^.INFO
    p.liga = None                                     # P^.LIGA <- NIL

    res = int(input("¿Desea ingresar más nodos a la lista? Sí: 1, No: 0: "))

    while res == 1:
        q = Nodo()                                    # Crear (Q)
        q.info = input("Ingrese el dato del nodo: ")  # Leer Q^.INFO
        q.liga = p                                    # Q^.LIGA <- P
        p = q                                         # P <- Q
        res = int(input("¿Desea ingresar más nodos a la lista? Sí: 1, No: 0: "))

    return p  # P apunta al inicio de la lista


# ---------------------------------------------------------
# 2. Crea_final: agregar al FINAL
# ---------------------------------------------------------
def crea_final():
    p = Nodo()                                        # Crear (P)
    p.info = input("Ingrese el dato del nodo: ")      # Leer P^.INFO
    p.liga = None                                     # P^.LIGA <- NIL
    t = p                                             # T <- P (último nodo)

    res = int(input("¿Desea ingresar más nodos a la lista? Sí: 1, No: 0: "))

    while res == 1:
        q = Nodo()                                    # Crear (Q)
        q.info = input("Ingrese el dato del nodo: ")  # Leer Q^.INFO
        q.liga = None                                 # Q^.LIGA <- NIL
        t.liga = q                                    # T^.LIGA <- Q
        t = q                                         # T <- Q
        res = int(input("¿Desea ingresar más nodos a la lista? Sí: 1, No: 0: "))

    return p  # P sigue apuntando al inicio de la lista


# ---------------------------------------------------------
# 3. Búsqueda_recursivo (P, X)
# ---------------------------------------------------------
def busqueda_recursivo(p, x):
    # 1. Si (P ≠ NIL)
    if p is not None:
        # 1.1 Si (P^.INFO = X)
        if p.info == x:
            print("El elemento se encuentra en la lista")
        else:
            busqueda_recursivo(p.liga, x)
    # 1.2 si no
    else:
        print("El elemento no se encuentra en la lista")


# ---------------------------------------------------------
# 4. Inserta_inicio (P, DATO)
# ---------------------------------------------------------
def inserta_inicio(p, dato):
    q = Nodo()          # 1. Crear (Q)
    q.info = dato       # 2. Q^.INFO <- DATO
    q.liga = p          #    Q^.LIGA <- P
    p = q               #    P <- Q
    return p            # P ahora apunta al nuevo primer nodo


# ---------------------------------------------------------
# 5. Inserta_final (P, DATO)
# ---------------------------------------------------------
def inserta_final(p, dato):
    q = Nodo()                  # 4. Crear (Q)
    q.info = dato               # 5. Q^.INFO <- DATO
    q.liga = None               #    Q^.LIGA <- NIL

    # Caso extra: si la lista está vacía, el nuevo nodo es el primero
    if p is None:
        return q

    t = p                       # 1. T <- P
    while t.liga is not None:   # 2. Mientras (T^.LIGA ≠ NIL) Repetir
        t = t.liga              #    T <- T^.LIGA
    # 3. Fin del ciclo

    t.liga = q                  #    T^.LIGA <- Q
    return p                    # P sigue apuntando al inicio


# ---------------------------------------------------------
# 6. Elimina_inicio (P)
# ---------------------------------------------------------
def elimina_inicio(p):
    # Caso extra: si la lista está vacía no hay nada que eliminar
    if p is None:
        print("La lista está vacía, no hay nada que eliminar.")
        return p

    q = p               # 1. Q <- P
    p = q.liga          # 2. P <- Q^.LIGA (si había un solo nodo, P queda en NIL)
    q = None            # 3. Quitar (Q) (se libera el nodo)
    return p            # P apunta al nuevo inicio de la lista


# ---------------------------------------------------------
# 7. Elimina_último (P)
# ---------------------------------------------------------
def elimina_ultimo(p):
    # Caso extra: si la lista está vacía no hay nada que eliminar
    if p is None:
        print("La lista está vacía, no hay nada que eliminar.")
        return p

    q = p                           # 1. Q <- P

    if p.liga is None:              # 2. Si (P^.LIGA = NIL) (solo un nodo)
        p = None                    #    P <- NIL
    else:                           #    si no
        t = None
        while q.liga is not None:   # 2.1 Mientras (Q^.LIGA ≠ NIL) Repetir
            t = q                   #     T <- Q
            q = q.liga              #     Q <- Q^.LIGA
        # 2.2 Fin del ciclo
        t.liga = None               #     T^.LIGA <- NIL

    q = None                        # 4. Quitar (Q)
    return p                        # P sigue apuntando al inicio


# ---------------------------------------------------------
# 8. Recorrido (P)
# ---------------------------------------------------------
def recorrido(p):
    q = p                           # 1. Q <- P
    while q is not None:            # 2. Mientras (Q ≠ NIL) Repetir
        print(q.info)               #    Escribir Q^.INFO
        q = q.liga                  #    Q <- Q^.LIGA (siguiente nodo)
    # 3. Fin del ciclo


# ---------------------------------------------------------
# 9. Inserta_antes_X (P, DATO, X)
#    "ref" es el contenido del nodo de referencia (X en el título)
#    y "x" es el nodo nuevo.
# ---------------------------------------------------------
def inserta_antes_x(p, dato, ref):
    # Caso extra: lista vacía
    if p is None:
        print("La lista está vacía, no hay nodo de referencia.")
        return p

    q = p                                   # 1. Q <- P
    t = None                                #    (T guarda el nodo anterior a Q)
    band = 1                                #    BAND <- 1

    # 2. Mientras ((Q^.INFO ≠ X) y (BAND = 1)) Repetir
    while q.info != ref and band == 1:
        if q.liga is not None:              # 2.1 Si (Q^.LIGA ≠ NIL)
            t = q                           #     T <- Q
            q = q.liga                      #     Q <- Q^.LIGA
        else:                               #     si no
            band = 0                        #     BAND <- 0
    # 3. Fin del ciclo

    if band == 1:                           # 4. Si (BAND = 1)
        x = Nodo()                          #    Crear (X)
        x.info = dato                       #    X^.INFO <- DATO
        if p is q:                          # 4.1 Si (P = Q) (referencia es el primero)
            x.liga = p                      #     X^.LIGA <- P
            p = x                           #     P <- X
        else:                               #     si no
            t.liga = x                      #     T^.LIGA <- X
            x.liga = q                      #     X^.LIGA <- Q
    else:
        print("El elemento de referencia no se encuentra en la lista")

    return p


# ---------------------------------------------------------
# 10. Inserta_después_X (P, DATO, X)
# ---------------------------------------------------------
def inserta_despues_x(p, dato, ref):
    # Caso extra: lista vacía
    if p is None:
        print("La lista está vacía, no hay nodo de referencia.")
        return p

    q = p                                   # 1. Q <- P
    band = 1                                #    BAND <- 1

    # 2. Mientras ((Q^.INFO ≠ X) y (BAND = 1)) Repetir
    while q.info != ref and band == 1:
        if q.liga is not None:              # 2.1 Si (Q^.LIGA ≠ NIL)
            q = q.liga                      #     Q <- Q^.LIGA
        else:                               #     si no
            band = 0                        #     BAND <- 0
    # 3. Fin del ciclo

    if band == 1:                           # 4. Si (BAND = 1)
        t = Nodo()                          #    Crear (T)
        t.info = dato                       #    T^.INFO <- DATO
        t.liga = q.liga                     #    T^.LIGA <- Q^.LIGA
        q.liga = t                          #    Q^.LIGA <- T
    else:                                   #    si no
        print("El nodo dado como referencia no se encuentra en la lista")
    # 5. Fin del condicional

    return p                                # P no cambia


# ---------------------------------------------------------
# 11. Elimina_X (P, X)
# ---------------------------------------------------------
def elimina_x(p, ref):
    # Caso extra: lista vacía
    if p is None:
        print("La lista está vacía, no hay nada que eliminar.")
        return p

    q = p                                   # 1. Q <- P
    t = None                                #    (T guarda el nodo anterior a Q)
    band = 1                                #    BAND <- 1

    # 2. Mientras ((Q^.INFO ≠ X) y (BAND = 1)) Repetir
    while q.info != ref and band == 1:
        if q.liga is not None:              # 2.1 Si (Q^.LIGA ≠ NIL)
            t = q                           #     T <- Q
            q = q.liga                      #     Q <- Q^.LIGA
        else:                               #     si no
            band = 0                        #     BAND <- 0
    # 3. Fin del ciclo

    if band == 0:                           # 4. Si (BAND = 0)
        print("El elemento con información X no se encuentra en la lista")
    else:                                   #    si no
        if p is q:                          # 4.1 Si (P = Q) (es el primero)
            p = q.liga                      #     P <- Q^.LIGA
        else:                               #     si no
            t.liga = q.liga                 #     T^.LIGA <- Q^.LIGA
        # 4.2 Fin del condicional
        q = None                            #     Quitar (Q)
    # 5. Fin del condicional

    return p


# ---------------------------------------------------------
# 12. Elimina_antes_X (P, X)
# ---------------------------------------------------------
def elimina_antes_x(p, ref):
    # Caso extra: lista vacía
    if p is None:
        print("La lista está vacía, no hay nada que eliminar.")
        return p

    # 1. Si (P^.INFO = X)
    if p.info == ref:
        print("No existe un nodo que preceda al que contiene a X")
    else:                                   #    si no
        q = p                               #    Q <- P
        t = p                               #    T <- P
        r = None                            #    (R guarda el nodo anterior a T)
        band = 1                            #    BAND <- 1

        # 1.1 Mientras ((Q^.INFO ≠ X) y (BAND = 1)) Repetir
        while q.info != ref and band == 1:
            if q.liga is not None:          # 1.1.1 Si (Q^.LIGA ≠ NIL)
                r = t                       #       R <- T
                t = q                       #       T <- Q
                q = q.liga                  #       Q <- Q^.LIGA
            else:                           #       si no
                band = 0                    #       BAND <- 0
        # 1.1.2 Fin del condicional
        # 1.2 Fin del ciclo

        if band == 0:                       # 1.3 Si (BAND = 0)
            print("El elemento no se encuentra en la lista")
        else:                               #     si no
            if p.liga is q:                 # 1.3.1 Si (P^.LIGA = Q) (el nodo a eliminar es el primero)
                p = q                       #       P <- Q
            else:                           #       si no
                r.liga = q                  #       R^.LIGA <- Q
            # 1.3.2 Fin del condicional
            t = None                        #     Quitar (T)
        # 1.4 Fin del condicional del paso 1.3
    # 2. Fin del condicional del paso 1

    return p


# ---------------------------------------------------------
# 13. Búsqueda_desordenada (P, X)
# ---------------------------------------------------------
def busqueda_desordenada(p, x):
    q = p                                   # 1. Q <- P

    # 2. Mientras ((Q ≠ NIL) y (Q^.INFO ≠ X))
    while q is not None and q.info != x:
        q = q.liga                          #    Q <- Q^.LIGA
    # 3. Fin del ciclo

    if q is None:                           # 4. Si (Q = NIL)
        print("El elemento no se encuentra en la lista")
    else:                                   #    si no
        print("El elemento sí se encuentra en la lista")
    # 5. Fin del condicional


# ---------------------------------------------------------
# Auxiliares para comparar datos en la búsqueda ordenada.
# Los datos se leen como texto; si ambos son números se comparan
# como números (así "10" no queda antes que "9"), y si no, como texto.
# ---------------------------------------------------------
def _comparables(a, b):
    try:
        return float(a), float(b)
    except ValueError:
        return a, b


def _menor(a, b):
    a, b = _comparables(a, b)
    return a < b


def _mayor(a, b):
    a, b = _comparables(a, b)
    return a > b


# ---------------------------------------------------------
# 14. Búsqueda_ordenada (P, X)
#     La lista debe estar ordenada de forma ASCENDENTE.
# ---------------------------------------------------------
def busqueda_ordenada(p, x):
    q = p                                   # 1. Q <- P

    # 2. Mientras ((Q ≠ NIL) y (Q^.INFO < X))
    while q is not None and _menor(q.info, x):
        q = q.liga                          #    Q <- Q^.LIGA
    # 3. Fin del ciclo

    # 4. Si ((Q = NIL) o (Q^.INFO > X))
    if q is None or _mayor(q.info, x):
        print("El elemento no se encuentra en la lista")
    else:                                   #    si no
        print("El elemento sí se encuentra en la lista")
    # 5. Fin del condicional


# ---------------------------------------------------------
# Auxiliar: imprimir la lista en formato de flechas
# ---------------------------------------------------------
def imprimir_lista(p):
    print("\nContenido de la lista:")
    actual = p
    while actual is not None:
        print(actual.info, end=" -> ")
        actual = actual.liga
    print("NIL")


# ---------------------------------------------------------
# Programa principal
# ---------------------------------------------------------
lista = None

while True:
    print("\n===== MENÚ =====")
    print("1. Crear lista agregando al inicio")
    print("2. Crear lista agregando al final (Crea_final)")
    print("3. Buscar un elemento (recursivo)")
    print("4. Insertar un nodo al inicio (Inserta_inicio)")
    print("5. Insertar un nodo al final (Inserta_final)")
    print("6. Eliminar el primer nodo (Elimina_inicio)")
    print("7. Eliminar el último nodo (Elimina_último)")
    print("8. Recorrer la lista (Recorrido)")
    print("9. Insertar antes de un nodo dado (Inserta_antes_X)")
    print("10. Insertar después de un nodo dado (Inserta_después_X)")
    print("11. Eliminar un nodo con información X (Elimina_X)")
    print("12. Eliminar el nodo anterior a X (Elimina_antes_X)")
    print("13. Búsqueda en lista desordenada (Búsqueda_desordenada)")
    print("14. Búsqueda en lista ordenada ascendente (Búsqueda_ordenada)")
    print("15. Mostrar lista con flechas")
    print("0. Salir")
    opcion = input("Elige una opción: ")

    if opcion == "1":
        lista = crear_inicio()
        imprimir_lista(lista)
    elif opcion == "2":
        lista = crea_final()
        imprimir_lista(lista)
    elif opcion == "3":
        if lista is None:
            print("Primero crea una lista (opción 1 o 2).")
        else:
            x = input("Ingrese el elemento a buscar: ")
            busqueda_recursivo(lista, x)
    elif opcion == "4":
        dato = input("Ingrese el dato a insertar al inicio: ")
        lista = inserta_inicio(lista, dato)
        imprimir_lista(lista)
    elif opcion == "5":
        dato = input("Ingrese el dato a insertar al final: ")
        lista = inserta_final(lista, dato)
        imprimir_lista(lista)
    elif opcion == "6":
        lista = elimina_inicio(lista)
        imprimir_lista(lista)
    elif opcion == "7":
        lista = elimina_ultimo(lista)
        imprimir_lista(lista)
    elif opcion == "8":
        print("\nRecorrido de la lista:")
        recorrido(lista)
    elif opcion == "9":
        dato = input("Ingrese el dato a insertar: ")
        ref = input("Ingrese el dato del nodo de referencia (X): ")
        lista = inserta_antes_x(lista, dato, ref)
        imprimir_lista(lista)
    elif opcion == "10":
        dato = input("Ingrese el dato a insertar: ")
        ref = input("Ingrese el dato del nodo de referencia (X): ")
        lista = inserta_despues_x(lista, dato, ref)
        imprimir_lista(lista)
    elif opcion == "11":
        ref = input("Ingrese el dato (X) del nodo a eliminar: ")
        lista = elimina_x(lista, ref)
        imprimir_lista(lista)
    elif opcion == "12":
        ref = input("Ingrese el dato (X): se eliminará el nodo anterior a él: ")
        lista = elimina_antes_x(lista, ref)
        imprimir_lista(lista)
    elif opcion == "13":
        x = input("Ingrese el elemento a buscar (X): ")
        busqueda_desordenada(lista, x)
    elif opcion == "14":
        x = input("Ingrese el elemento a buscar (X): ")
        busqueda_ordenada(lista, x)
    elif opcion == "15":
        imprimir_lista(lista)
    elif opcion == "0":
        print("Fin del programa.")
        break
    else:
        print("Opción no válida.")