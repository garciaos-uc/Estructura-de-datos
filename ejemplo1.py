"""
Ejercicio 1: Sistema de Gestión de Turnos en un Banco (Cola Simple)

¿QUÉ ES UNA COLA?
-----------------
Una cola (queue) es una estructura de datos lineal que sigue la regla FIFO:
"First In, First Out" (el primero en entrar es el primero en salir),
igual que la fila de un banco.

Operaciones básicas:
    - encolar (enqueue): agrega un elemento AL FINAL de la cola.
    - desencolar (dequeue): saca el elemento del FRENTE de la cola.
    - frente (peek): consulta quién va al frente sin sacarlo.
    - esta_vacia (is_empty): indica si ya no hay elementos.

¿QUÉ ESTRUCTURA USAMOS Y POR QUÉ ES EFICIENTE?
----------------------------------------------
Si usáramos una lista de Python y sacáramos con list.pop(0), cada extracción
costaría O(n), porque todos los elementos se recorren una posición.
Con collections.deque (lista doblemente enlazada por bloques) tanto encolar
como desencolar cuestan O(1).

¿CÓMO RESOLVEMOS LA PRIORIDAD?
------------------------------
Alternativa lenta: una sola cola e insertar al prioritario "después del último
prioritario" -> O(n) por inserción.

Alternativa óptima (la que usamos): DOS COLAS FIFO
    - cola_prioritaria  (tercera edad / discapacidad)
    - cola_normal
Al atender: si la cola prioritaria tiene gente, se atiende de ahí; si no,
de la normal. Así:
    * los prioritarios pasan antes que los normales,
    * entre prioritarios se respeta el orden de llegada (es FIFO),
    * entre normales también,
    * todas las operaciones son O(1).
"""

from collections import deque
from dataclasses import dataclass
from itertools import count


# ---------------------------------------------------------------------------
# Modelo de datos
# ---------------------------------------------------------------------------
@dataclass(frozen=True)
class Cliente:
    turno: int      # número de turno (orden real de llegada)
    nombre: str
    tipo: str       # "normal" o "prioritario"
    motivo: str = ""  # información extra (tercera edad, discapacidad, etc.)

    def __str__(self) -> str:
        marca = "★" if self.tipo == "prioritario" else " "
        extra = f" ({self.motivo})" if self.motivo else ""
        return f"[{marca}] Turno #{self.turno:02d} - {self.nombre} - {self.tipo}{extra}"


# ---------------------------------------------------------------------------
# Cola FIFO simple
# ---------------------------------------------------------------------------
class Cola:
    """Cola FIFO sobre deque: encolar y desencolar en O(1)."""

    def __init__(self) -> None:
        self._items: deque[Cliente] = deque()

    def encolar(self, elemento: Cliente) -> None:
        self._items.append(elemento)          # entra por el final

    def desencolar(self) -> Cliente:
        if self.esta_vacia():
            raise IndexError("La cola está vacía")
        return self._items.popleft()          # sale por el frente

    def frente(self) -> Cliente:
        if self.esta_vacia():
            raise IndexError("La cola está vacía")
        return self._items[0]

    def esta_vacia(self) -> bool:
        return not self._items

    def __len__(self) -> int:
        return len(self._items)

    def __iter__(self):
        return iter(self._items)


# ---------------------------------------------------------------------------
# Sistema de turnos
# ---------------------------------------------------------------------------
class SistemaTurnos:
    def __init__(self) -> None:
        self._prioritarios = Cola()
        self._normales = Cola()
        self._contador = count(1)             # genera turnos 1, 2, 3, ...
        self.historial: list[Cliente] = []    # orden real de atención

    def llegada(self, nombre: str, tipo: str = "normal", motivo: str = "") -> Cliente:
        tipo = tipo.lower()
        if tipo not in ("normal", "prioritario"):
            raise ValueError("tipo debe ser 'normal' o 'prioritario'")
        cliente = Cliente(next(self._contador), nombre, tipo, motivo)
        (self._prioritarios if tipo == "prioritario" else self._normales).encolar(cliente)
        print(f"  ➜ Llega: {cliente}")
        return cliente

    def atender(self) -> Cliente | None:
        """Atiende al siguiente: primero prioritarios, luego normales."""
        if not self._prioritarios.esta_vacia():
            cliente = self._prioritarios.desencolar()
        elif not self._normales.esta_vacia():
            cliente = self._normales.desencolar()
        else:
            print("  (No hay clientes en espera)")
            return None
        self.historial.append(cliente)
        print(f"  ✔ Atendiendo: {cliente}")
        return cliente

    def hay_clientes(self) -> bool:
        return not (self._prioritarios.esta_vacia() and self._normales.esta_vacia())

    def mostrar_colas(self) -> None:
        pri = [c.nombre for c in self._prioritarios]
        nor = [c.nombre for c in self._normales]
        print(f"    Cola prioritaria: {pri}")
        print(f"    Cola normal     : {nor}")


# ---------------------------------------------------------------------------
# Simulación
# ---------------------------------------------------------------------------
def simular() -> None:
    banco = SistemaTurnos()

    # Cada evento: ("llega", nombre, tipo, motivo) o ("atiende",)
    # Se intercalan llegadas y atenciones para ver cómo actúa la prioridad.
    eventos = [
        ("llega", "Carlos Pérez",     "normal",      ""),
        ("llega", "María López",      "normal",      ""),
        ("llega", "Doña Rosa",        "prioritario", "tercera edad"),
        ("llega", "Jorge Ramírez",    "normal",      ""),
        ("atiende",),
        ("llega", "Luis Hernández",   "prioritario", "discapacidad"),
        ("llega", "Ana Torres",       "normal",      ""),
        ("atiende",),
        ("llega", "Don Pedro",        "prioritario", "tercera edad"),
        ("llega", "Sofía Martínez",   "normal",      ""),
        ("atiende",),
        ("atiende",),
        ("llega", "Elena Castillo",   "prioritario", "discapacidad"),
        ("llega", "Miguel Ángel Díaz", "normal",     ""),
        ("atiende",),
    ]

    print("=" * 66)
    print(" SIMULACIÓN: BANCO - GESTIÓN DE TURNOS")
    print("=" * 66)

    paso = 1
    for ev in eventos:
        print(f"\nPaso {paso}:")
        if ev[0] == "llega":
            banco.llegada(*ev[1:])
        else:
            banco.atender()
        banco.mostrar_colas()
        paso += 1

    print("\n" + "-" * 66)
    print(" Se cierra la llegada de clientes: se atiende a los que quedan")
    print("-" * 66)
    while banco.hay_clientes():
        banco.atender()

    print("\n" + "=" * 66)
    print(" ORDEN FINAL DE ATENCIÓN")
    print("=" * 66)
    for pos, c in enumerate(banco.historial, start=1):
        print(f" {pos:2d}. {c}")


if __name__ == "__main__":
    simular()