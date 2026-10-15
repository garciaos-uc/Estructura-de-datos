import time

OPCIONES_DISCOS = (5, 10, 30, 64)
TORRES = ("A", "B", "C")


def movimientos_minimos(n):
    return 2 ** n - 1


def formatear_tiempo(seg):
    if seg < 1e-3:
        return f"{seg * 1e6:,.2f} µs"
    if seg < 1:
        return f"{seg * 1e3:,.3f} ms"
    if seg < 60:
        return f"{seg:,.3f} s"
    if seg < 3600:
        return f"{seg / 60:,.2f} minutos"
    if seg < 86400:
        return f"{seg / 3600:,.2f} horas"
    if seg < 365.25 * 86400:
        return f"{seg / 86400:,.2f} días"
    return f"{seg / (365.25 * 86400):,.2f} años"


class TorreHanoi:
    def __init__(self, n):
        self.n = n
        self.reiniciar()

    def reiniciar(self):
        self.torres = {"A": list(range(self.n, 0, -1)), "B": [], "C": []}
        self.movimientos = 0

    def mover(self, origen, destino):
        if origen not in self.torres or destino not in self.torres:
            raise ValueError("Torres válidas: A, B, C.")
        if origen == destino:
            raise ValueError("El origen y el destino son la misma torre.")
        if not self.torres[origen]:
            raise ValueError(f"La torre {origen} está vacía.")
        disco = self.torres[origen][-1]
        if self.torres[destino] and self.torres[destino][-1] < disco:
            raise ValueError("No puedes poner un disco grande sobre uno más pequeño.")
        self.torres[destino].append(self.torres[origen].pop())
        self.movimientos += 1

    def esta_resuelto(self):
        return len(self.torres["C"]) == self.n

    def dibujar(self):
        ancho = 2 * self.n + 3
        for nivel in range(self.n - 1, -1, -1):
            fila = ""
            for t in TORRES:
                if nivel < len(self.torres[t]):
                    d = self.torres[t][nivel]
                    fila += ("#" * (2 * d - 1)).center(ancho)
                else:
                    fila += "|".center(ancho)
            print(fila)
        print("".join(t.center(ancho) for t in TORRES))
        print(f"Movimientos: {self.movimientos}")

    def resolver_recursivo(self, n=None, origen="A", destino="C", auxiliar="B", callback=None):
        if n is None:
            n = self.n
        if n == 0:
            return
        self.resolver_recursivo(n - 1, origen, auxiliar, destino, callback)
        self.mover(origen, destino)
        if callback:
            callback()
        self.resolver_recursivo(n - 1, auxiliar, destino, origen, callback)

    def resolver_iterativo(self, callback=None):
        t = self.torres
        total = movimientos_minimos(self.n)
        ciclo = ["A", "C", "B"] if self.n % 2 else ["A", "B", "C"]
        pos = 0
        for paso in range(1, total + 1):
            if paso % 2 == 1:
                origen = ciclo[pos]
                pos = (pos + 1) % 3
                destino = ciclo[pos]
            else:
                a, b = [p for p in TORRES if p != ciclo[pos]]
                if not t[a]:
                    origen, destino = b, a
                elif not t[b]:
                    origen, destino = a, b
                elif t[a][-1] < t[b][-1]:
                    origen, destino = a, b
                else:
                    origen, destino = b, a
            self.mover(origen, destino)
            if callback:
                callback()


def jugar_manual(n):
    juego = TorreHanoi(n)
    print(f"\nModo manual con {n} discos. Mínimo posible: {movimientos_minimos(n):,} movimientos.")
    print("Escribe 'A C' para mover de A a C | 'r' reiniciar | 's' salir.")
    inicio = time.perf_counter()
    while not juego.esta_resuelto():
        print()
        juego.dibujar()
        entrada = input("Movimiento> ").strip().upper()
        if entrada == "S":
            return
        if entrada == "R":
            juego.reiniciar()
            inicio = time.perf_counter()
            continue
        partes = entrada.split()
        if len(partes) != 2:
            print("Formato inválido. Ejemplo: A C")
            continue
        try:
            juego.mover(partes[0], partes[1])
        except ValueError as e:
            print("Movimiento inválido:", e)
    duracion = time.perf_counter() - inicio
    print()
    juego.dibujar()
    print(f"¡Resuelto! Tardaste {formatear_tiempo(duracion)} en {juego.movimientos:,} movimientos.")
    if juego.movimientos == movimientos_minimos(n):
        print("Lo hiciste con el número mínimo de movimientos.")


def animar(n):
    juego = TorreHanoi(n)
    pausa = 0.4 if n <= 5 else 0.05

    def paso():
        print()
        juego.dibujar()
        time.sleep(pausa)

    print(f"\nAnimación con {n} discos (método recursivo).")
    juego.dibujar()
    inicio = time.perf_counter()
    juego.resolver_recursivo(callback=paso)
    total = time.perf_counter() - inicio
    print(f"\nTerminó en {juego.movimientos:,} movimientos "
          f"(tiempo total con pausas de animación: {formatear_tiempo(total)}).")


def medir_velocidad():
    juego = TorreHanoi(20)
    inicio = time.perf_counter()
    juego.resolver_iterativo()
    seg = time.perf_counter() - inicio
    return juego.movimientos / seg


def resolver_y_medir(n):
    total = movimientos_minimos(n)
    print(f"\n{n} discos -> {total:,} movimientos mínimos.")

    ejecutar_real = n <= 10
    if n == 30:
        r = input("30 discos reales pueden tardar varios minutos. ¿Ejecutar de verdad? (s = sí / n = solo estimar): ")
        ejecutar_real = r.strip().lower() == "s"

    if ejecutar_real:
        for nombre, metodo in (("recursivo", "resolver_recursivo"), ("iterativo", "resolver_iterativo")):
            juego = TorreHanoi(n)
            inicio = time.perf_counter()
            getattr(juego, metodo)()
            seg = time.perf_counter() - inicio
            assert juego.esta_resuelto() and juego.movimientos == total
            print(f"  Método {nombre:<9}: {formatear_tiempo(seg)}")
        return

    print("  Midiendo la velocidad de tu computadora...")
    mps = medir_velocidad()
    print(f"  Velocidad medida: {mps:,.0f} movimientos/segundo")
    print(f"  Tiempo estimado en esta computadora : {formatear_tiempo(total / mps)}")
    print(f"  Tiempo a 1 movimiento por segundo   : {formatear_tiempo(total * 1.0)}")
    if n == 64:
        print("  (64 discos NO se pueden ejecutar de verdad: el universo tiene ~13,800 millones de años.)")


def menu():
    print("=== TORRE DE HANOI ===")
    n = 5
    while True:
        print(f"\nDiscos actuales: {n}")
        print("1) Elegir número de discos (5, 10, 30, 64)")
        print("2) Jugar manualmente (solo 5 y 10)")
        print("3) Ver animación (solo 5 y 10)")
        print("4) Resolver y medir tiempo")
        print("0) Salir")
        op = input("Opción> ").strip()
        if op == "1":
            try:
                v = int(input("Discos (5/10/30/64)> "))
            except ValueError:
                print("Escribe un número.")
                continue
            if v in OPCIONES_DISCOS:
                n = v
            else:
                print("Solo se permiten 5, 10, 30 o 64.")
        elif op == "2":
            if n > 10:
                print("Manual solo con 5 o 10 discos (con más sería imposible).")
            else:
                jugar_manual(n)
        elif op == "3":
            if n > 10:
                print("La animación solo es práctica con 5 o 10 discos.")
            else:
                animar(n)
        elif op == "4":
            resolver_y_medir(n)
        elif op == "0":
            print("¡Hasta luego!")
            break
        else:
            print("Opción inválida.")


if __name__ == "__main__":
    menu()