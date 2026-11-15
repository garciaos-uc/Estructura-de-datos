# ==============================================================
#  Programa de recorridos mediante grafos - 7 estados de México
#  Estados: Yucatán, Quintana Roo, Campeche, Tabasco,
#           Chiapas, Veracruz y Oaxaca
#  Costos: distancia aproximada por carretera (km) entre las
#          capitales de cada par de estados que colindan.
#  Incluye 4 opciones para elegir el estado inicial y final.
# ==============================================================

import random
import tkinter as tk
from tkinter import ttk, messagebox

# --------------------------------------------------------------
# 1. DATOS DEL GRAFO (estados, conexiones y costos)
# --------------------------------------------------------------

ESTADOS = ["Yucatán", "Quintana Roo", "Campeche", "Tabasco",
           "Chiapas", "Veracruz", "Oaxaca"]

# Solo se incluyen pares de estados que realmente colindan.
# Formato: (estado1, estado2, costo)
CONEXIONES = [
    ("Yucatán",      "Quintana Roo", 390),
    ("Yucatán",      "Campeche",     195),
    ("Quintana Roo", "Campeche",     430),
    ("Campeche",     "Tabasco",      450),
    ("Tabasco",      "Chiapas",      290),
    ("Tabasco",      "Veracruz",     650),
    ("Chiapas",      "Veracruz",     950),
    ("Chiapas",      "Oaxaca",       600),
    ("Veracruz",     "Oaxaca",       430),
]

# Posición de cada estado en el dibujo (aproximada a su ubicación real)
POSICIONES = {
    "Yucatán":      (700, 110),
    "Quintana Roo": (840, 230),
    "Campeche":     (640, 260),
    "Tabasco":      (480, 280),
    "Chiapas":      (430, 440),
    "Veracruz":     (230, 190),
    "Oaxaca":       (150, 400),
}

# Grafo como diccionario de adyacencia: {estado: {vecino: costo}}
grafo = {e: {} for e in ESTADOS}
for a, b, costo in CONEXIONES:
    grafo[a][b] = costo
    grafo[b][a] = costo

# Máximo de paradas permitidas en el recorrido del inciso B
MAX_PARADAS_B = 12


# --------------------------------------------------------------
# 2. FUNCIONES DE VALIDACIÓN Y COSTO
# --------------------------------------------------------------

def costo_recorrido(recorrido):
    """Suma el costo de cada tramo del recorrido."""
    return sum(grafo[recorrido[i]][recorrido[i + 1]]
               for i in range(len(recorrido) - 1))


def es_valido(recorrido, permitir_repetidos, inicio, fin):
    """Comprueba que: empiece en 'inicio' y termine en 'fin', todas las
    conexiones existan, se visiten los 7 estados y la repetición
    cumpla lo pedido (A: sin repetir, B: repitiendo al menos uno)."""
    if recorrido[0] != inicio or recorrido[-1] != fin:
        return False
    for i in range(len(recorrido) - 1):
        if recorrido[i + 1] not in grafo[recorrido[i]]:
            return False                       # conexión inexistente
    if set(recorrido) != set(ESTADOS):
        return False                           # faltan estados
    hay_repetidos = len(recorrido) > len(set(recorrido))
    if permitir_repetidos:
        return hay_repetidos                   # B: debe repetir alguno
    return not hay_repetidos                   # A: no debe repetir


def estados_repetidos(recorrido):
    """Devuelve los estados que aparecen más de una vez."""
    return sorted({e for e in recorrido if recorrido.count(e) > 1})


# --------------------------------------------------------------
# 3. BÚSQUEDA DE RECORRIDOS (respetando inicio y final)
# --------------------------------------------------------------

def buscar_recorrido_a(inicio, fin):
    """Inciso A: recorrido de menor costo de 'inicio' a 'fin' que visita
    los 7 estados sin repetir ninguno (búsqueda por retroceso).
    Devuelve (ruta, costo) o (None, None) si no existe."""
    mejor = {"ruta": None, "costo": float("inf")}

    def explorar(ruta, costo):
        if costo >= mejor["costo"]:
            return                              # poda: ya no mejora
        if len(ruta) == len(ESTADOS):
            if ruta[-1] == fin:                 # debe terminar en el final
                mejor["ruta"], mejor["costo"] = ruta[:], costo
            return
        if ruta[-1] == fin:
            return                              # llegó al final sin visitar todo
        for vecino, c in grafo[ruta[-1]].items():
            if vecino not in ruta:              # no repetir estados
                ruta.append(vecino)
                explorar(ruta, costo + c)
                ruta.pop()

    explorar([inicio], 0)
    if mejor["ruta"] is None:
        return None, None
    return mejor["ruta"], mejor["costo"]


def buscar_recorrido_b(inicio, fin):
    """Inciso B: recorrido de menor costo de 'inicio' a 'fin' que visita
    los 7 estados y repite al menos uno (hasta MAX_PARADAS_B paradas).
    Devuelve (ruta, costo) o (None, None) si no existe."""
    mejor = {"ruta": None, "costo": float("inf")}

    def explorar(ruta, costo):
        if costo >= mejor["costo"]:
            return
        if (ruta[-1] == fin and set(ruta) == set(ESTADOS)
                and len(ruta) > len(set(ruta))):
            mejor["ruta"], mejor["costo"] = ruta[:], costo
            return                              # seguir solo costaría más
        if len(ruta) == MAX_PARADAS_B:
            return
        for vecino, c in grafo[ruta[-1]].items():
            ruta.append(vecino)
            explorar(ruta, costo + c)
            ruta.pop()

    explorar([inicio], 0)
    if mejor["ruta"] is None:
        return None, None
    return mejor["ruta"], mejor["costo"]


# --------------------------------------------------------------
# 4. INTERFAZ VISUAL
# --------------------------------------------------------------

class App:
    def __init__(self, ventana):
        self.ventana = ventana
        ventana.title("Recorridos con grafos - 7 estados de México")

        # Estado de la aplicación
        self.inicio = None
        self.fin = None
        self.ruta_a = self.costo_a = None
        self.ruta_b = self.costo_b = None
        self.calculado = False

        # Lienzo donde se dibuja el grafo
        self.canvas = tk.Canvas(ventana, width=980, height=560, bg="white")
        self.canvas.grid(row=0, column=0, rowspan=3, padx=5, pady=5)

        # ---------- Menú de las 4 opciones de inicio/final ----------
        menu = tk.LabelFrame(ventana, text="¿Cómo elegir inicio y final?")
        menu.grid(row=0, column=1, sticky="n", padx=5, pady=5)

        self.opcion = tk.IntVar(value=1)
        opciones = [
            (1, "Opción 1: Inicio y final aleatorios"),
            (2, "Opción 2: Inicio y final manuales"),
            (3, "Opción 3: Inicio manual, final aleatorio"),
            (4, "Opción 4: Inicio aleatorio, final manual"),
        ]
        for valor, texto in opciones:
            tk.Radiobutton(menu, text=texto, variable=self.opcion,
                           value=valor, anchor="w",
                           command=self.actualizar_combos
                           ).pack(fill="x", padx=5)

        # Listas desplegables para elegir estados manualmente
        tk.Label(menu, text="Estado inicial:").pack(anchor="w", padx=5)
        self.cb_inicio = ttk.Combobox(menu, values=ESTADOS,
                                      state="readonly", width=25)
        self.cb_inicio.pack(padx=5, pady=2)
        tk.Label(menu, text="Estado final:").pack(anchor="w", padx=5)
        self.cb_fin = ttk.Combobox(menu, values=ESTADOS,
                                   state="readonly", width=25)
        self.cb_fin.pack(padx=5, pady=2)

        tk.Button(menu, text="Calcular recorridos", width=28,
                  bg="#2ecc71", command=self.calcular).pack(pady=5)

        # ---------- Botones para ver resultados ----------
        panel = tk.Frame(ventana)
        panel.grid(row=1, column=1, sticky="n", padx=5)
        tk.Button(panel, text="Ver grafo", width=14,
                  command=self.mostrar_grafo).grid(row=0, column=0, padx=2, pady=2)
        tk.Button(panel, text="Comparar", width=14,
                  command=self.mostrar_comparacion).grid(row=0, column=1, padx=2, pady=2)
        tk.Button(panel, text="Inciso A", width=14,
                  command=self.mostrar_a).grid(row=1, column=0, padx=2, pady=2)
        tk.Button(panel, text="Inciso B", width=14,
                  command=self.mostrar_b).grid(row=1, column=1, padx=2, pady=2)
        tk.Button(panel, text="Ponderaciones", width=30,
                  command=self.editar_ponderaciones).grid(row=2, column=0, columnspan=2, padx=2, pady=2)

        # Panel de texto con los resultados
        self.texto = tk.Text(ventana, width=50, height=20, wrap="word",
                             font=("Consolas", 10))
        self.texto.grid(row=2, column=1, padx=5, pady=5, sticky="n")

        self.actualizar_combos()
        self.mostrar_grafo()

    # ---------- Habilitar/deshabilitar listas según la opción ----------
    def actualizar_combos(self):
        op = self.opcion.get()
        # Inicio manual en opciones 2 y 3; final manual en opciones 2 y 4
        self.cb_inicio.config(state="readonly" if op in (2, 3) else "disabled")
        self.cb_fin.config(state="readonly" if op in (2, 4) else "disabled")

    # ---------- Elegir inicio y final según la opción ----------
    def elegir_inicio_fin(self):
        """Devuelve (inicio, fin) o None si hay un error en la selección."""
        op = self.opcion.get()
        manual_ini = self.cb_inicio.get()
        manual_fin = self.cb_fin.get()

        if op == 1:                                   # ambos aleatorios
            return tuple(random.sample(ESTADOS, 2))   # siempre distintos
        if op == 2:                                   # ambos manuales
            if not manual_ini or not manual_fin:
                messagebox.showwarning("Falta selección",
                                       "Elige el estado inicial y el final.")
                return None
            if manual_ini == manual_fin:
                messagebox.showwarning("Selección inválida",
                                       "El inicio y el final deben ser distintos.")
                return None
            return manual_ini, manual_fin
        if op == 3:                                   # inicio manual, final aleatorio
            if not manual_ini:
                messagebox.showwarning("Falta selección",
                                       "Elige el estado inicial.")
                return None
            return manual_ini, random.choice([e for e in ESTADOS if e != manual_ini])
        # op == 4: inicio aleatorio, final manual
        if not manual_fin:
            messagebox.showwarning("Falta selección", "Elige el estado final.")
            return None
        return random.choice([e for e in ESTADOS if e != manual_fin]), manual_fin

    # ---------- Calcular ambos incisos con el mismo inicio y final ----------
    def calcular(self):
        seleccion = self.elegir_inicio_fin()
        if seleccion is None:
            return
        self.inicio, self.fin = seleccion
        self.ruta_a, self.costo_a = buscar_recorrido_a(self.inicio, self.fin)
        self.ruta_b, self.costo_b = buscar_recorrido_b(self.inicio, self.fin)
        self.calculado = True

        self.dibujar()
        t = "SELECCIÓN\n"
        t += f"  Inicio : {self.inicio}\n  Destino: {self.fin}\n\n"
        t += "RESULTADOS\n"
        t += (f"  Inciso A: costo {self.costo_a}\n" if self.ruta_a
              else "  Inciso A: no existe recorrido válido\n")
        t += (f"  Inciso B: costo {self.costo_b}\n" if self.ruta_b
              else "  Inciso B: no existe recorrido válido\n")
        t += "\nUsa los botones Inciso A, Inciso B o Comparar."
        self.escribir(t)

        # Si no hay ninguna ruta, avisar y permitir elegir otra opción
        if not self.ruta_a and not self.ruta_b:
            mensaje = (f"No existe una ruta válida de {self.inicio} a {self.fin} "
                       "que visite los 7 estados.\n"
                       "Selecciona otra opción o cambia los estados.")
            self.escribir(t + "\n\n" + mensaje)
            messagebox.showwarning("Sin ruta posible", mensaje)

    # ---------- Dibujo del grafo ----------
    def dibujar(self, ruta=None, color="#e67e22"):
        """Dibuja el grafo; si se da una ruta, la resalta y numera."""
        c = self.canvas
        c.delete("all")

        # Conexiones (líneas)
        for a, b, costo in CONEXIONES:
            x1, y1 = POSICIONES[a]
            x2, y2 = POSICIONES[b]
            c.create_line(x1, y1, x2, y2, fill="#95a5a6", width=2)

        # Resaltar los tramos del recorrido
        if ruta:
            for i in range(len(ruta) - 1):
                x1, y1 = POSICIONES[ruta[i]]
                x2, y2 = POSICIONES[ruta[i + 1]]
                c.create_line(x1, y1, x2, y2, fill=color, width=5,
                              arrow=tk.LAST, arrowshape=(16, 18, 7))

        # Etiquetas de costo en el punto medio de cada línea
        for a, b, costo in CONEXIONES:
            x1, y1 = POSICIONES[a]
            x2, y2 = POSICIONES[b]
            mx, my = (x1 + x2) / 2, (y1 + y2) / 2
            c.create_rectangle(mx - 18, my - 10, mx + 18, my + 10,
                               fill="white", outline="#bdc3c7")
            c.create_text(mx, my, text=str(costo), font=("Arial", 9, "bold"))

        # Estados (círculos con nombre); inicio en verde, final en morado
        repetidos = estados_repetidos(ruta) if ruta else []
        for estado, (x, y) in POSICIONES.items():
            relleno = "#e74c3c" if estado in repetidos else "#3498db"
            borde, grosor = "#2c3e50", 2
            if estado == self.inicio:
                borde, grosor = "#27ae60", 6
            elif estado == self.fin:
                borde, grosor = "#8e44ad", 6
            c.create_oval(x - 30, y - 30, x + 30, y + 30,
                          fill=relleno, outline=borde, width=grosor)
            c.create_text(x, y, text=estado, fill="white",
                          font=("Arial", 8, "bold"), width=56)
            if estado == self.inicio:
                c.create_text(x, y + 44, text="INICIO", fill="#27ae60",
                              font=("Arial", 10, "bold"))
            elif estado == self.fin:
                c.create_text(x, y + 44, text="DESTINO", fill="#8e44ad",
                              font=("Arial", 10, "bold"))

        # Números de visita junto a cada estado (ej. "Visita: 1, 5")
        if ruta:
            for estado, (x, y) in POSICIONES.items():
                pasos = [str(i + 1) for i, e in enumerate(ruta) if e == estado]
                c.create_text(x, y - 42, text="Visita: " + ", ".join(pasos),
                              fill="#2c3e50", font=("Arial", 9, "bold"))

        # Leyenda
        c.create_text(10, 545, anchor="w", fill="#2c3e50",
                      text="Costo = km aproximados por carretera. Borde verde = inicio, "
                           "borde morado = destino, relleno rojo = estado repetido.")

    # ---------- Escribir en el panel de texto ----------
    def escribir(self, contenido):
        self.texto.delete("1.0", tk.END)
        self.texto.insert(tk.END, contenido)

    def hay_calculo(self):
        """Avisa si todavía no se han calculado los recorridos."""
        if not self.calculado:
            messagebox.showinfo("Aún no hay recorridos",
                                "Elige una opción y pulsa 'Calcular recorridos'.")
        return self.calculado

    # ---------- Editar las ponderaciones de las conexiones ----------
    def editar_ponderaciones(self):
        """Permite cambiar el costo asignado a cada conexión del grafo."""
        ventana_costos = tk.Toplevel(self.ventana)
        ventana_costos.title("Modificar ponderaciones")
        ventana_costos.transient(self.ventana)
        ventana_costos.grab_set()

        tk.Label(
            ventana_costos,
            text="Modifica el costo de cada conexión entre estados:",
            font=("Arial", 10, "bold")
        ).grid(row=0, column=0, columnspan=3, padx=10, pady=10)

        entradas = []
        for i, (a, b, costo) in enumerate(CONEXIONES):
            tk.Label(ventana_costos, text=f"{a} - {b}:").grid(
                row=i + 1, column=0, sticky="w", padx=10, pady=3
            )
            entrada = tk.Entry(ventana_costos, width=12)
            entrada.insert(0, str(costo))
            entrada.grid(row=i + 1, column=1, padx=5, pady=3)
            tk.Label(ventana_costos, text="km / unidades").grid(
                row=i + 1, column=2, sticky="w", padx=5, pady=3
            )
            entradas.append(entrada)

        def guardar_ponderaciones():
            nuevos_costos = []
            try:
                for entrada in entradas:
                    valor = float(entrada.get())
                    if valor < 0:
                        raise ValueError
                    nuevos_costos.append(int(valor) if valor.is_integer() else valor)
            except ValueError:
                messagebox.showerror(
                    "Valor inválido",
                    "Escribe un número válido y no negativo para cada conexión.",
                    parent=ventana_costos
                )
                return

            # Actualizar las conexiones y el grafo con los nuevos valores.
            for i, (a, b, _) in enumerate(CONEXIONES):
                CONEXIONES[i] = (a, b, nuevos_costos[i])

            for estado in ESTADOS:
                grafo[estado].clear()
            for a, b, costo in CONEXIONES:
                grafo[a][b] = costo
                grafo[b][a] = costo

            # Los recorridos anteriores dejan de ser válidos al cambiar costos.
            self.inicio = None
            self.fin = None
            self.ruta_a = self.costo_a = None
            self.ruta_b = self.costo_b = None
            self.calculado = False

            ventana_costos.destroy()
            self.mostrar_grafo()
            messagebox.showinfo(
                "Ponderaciones actualizadas",
                "Los costos se actualizaron correctamente. Calcula nuevamente los recorridos."
            )

        tk.Button(
            ventana_costos,
            text="Guardar cambios",
            command=guardar_ponderaciones,
            bg="#2ecc71"
        ).grid(row=len(CONEXIONES) + 1, column=0, columnspan=3, pady=12)

    # ---------- Botones ----------
    def mostrar_grafo(self):
        self.dibujar()
        t = "ESTADOS (7):\n  " + ", ".join(ESTADOS) + "\n\n"
        t += "CONEXIONES Y COSTOS:\n"
        for a, b, costo in CONEXIONES:
            t += f"  {a} - {b}: {costo}\n"
        if self.calculado:
            t += f"\nInicio: {self.inicio}\nDestino: {self.fin}"
        self.escribir(t)

    def detalle_recorrido(self, titulo, ruta, costo, mostrar_repetidos):
        """Arma el texto de un recorrido (orden, tramos y costo)."""
        t = f"{titulo}\n\nInicio : {self.inicio}\nDestino: {self.fin}\n\n"
        t += "Orden:\n  " + " -> ".join(ruta) + "\n\n"
        if mostrar_repetidos:
            t += "Estado(s) repetido(s): " + ", ".join(estados_repetidos(ruta)) + "\n\n"
        t += "Tramos:\n"
        for i in range(len(ruta) - 1):
            a, b = ruta[i], ruta[i + 1]
            t += f"  {a} -> {b}: {grafo[a][b]}\n"
        t += f"\nCosto total: {costo}\nEstados visitados: 7 de 7 (válido)"
        return t

    def mostrar_a(self):
        if not self.hay_calculo():
            return
        if not self.ruta_a or not es_valido(self.ruta_a, False, self.inicio, self.fin):
            self.dibujar()
            mensaje = (f"No existe un recorrido de {self.inicio} a {self.fin} que "
                       "visite los 7 estados sin repetir ninguno.\n"
                       "Prueba con otra opción de inicio/final.")
            self.escribir("INCISO A\n\n" + mensaje)
            messagebox.showwarning("Inciso A", mensaje)
            return
        self.dibujar(self.ruta_a, "#27ae60")
        self.escribir(self.detalle_recorrido("INCISO A (sin repetir estados)",
                                             self.ruta_a, self.costo_a, False))

    def mostrar_b(self):
        if not self.hay_calculo():
            return
        if not self.ruta_b or not es_valido(self.ruta_b, True, self.inicio, self.fin):
            self.dibujar()
            mensaje = (f"No existe un recorrido de {self.inicio} a {self.fin} que "
                       f"visite los 7 estados repitiendo al menos uno "
                       f"(máximo {MAX_PARADAS_B} paradas).\n"
                       "Prueba con otra opción de inicio/final.")
            self.escribir("INCISO B\n\n" + mensaje)
            messagebox.showwarning("Inciso B", mensaje)
            return
        self.dibujar(self.ruta_b, "#e67e22")
        self.escribir(self.detalle_recorrido("INCISO B (repitiendo estados)",
                                             self.ruta_b, self.costo_b, True))

    def mostrar_comparacion(self):
        if not self.hay_calculo():
            return
        self.dibujar()
        t = f"COMPARACIÓN DE COSTOS\nInicio: {self.inicio}  ->  Destino: {self.fin}\n\n"
        if self.ruta_a:
            t += f"Inciso A: {self.costo_a}\n  {' -> '.join(self.ruta_a)}\n\n"
        else:
            t += "Inciso A: no existe recorrido válido\n\n"
        if self.ruta_b:
            t += f"Inciso B: {self.costo_b}\n  {' -> '.join(self.ruta_b)}\n\n"
        else:
            t += "Inciso B: no existe recorrido válido\n\n"
        if self.ruta_a and self.ruta_b:
            dif = self.costo_b - self.costo_a
            if dif > 0:
                t += f"El inciso B cuesta {dif} más que el A."
            elif dif < 0:
                t += f"El inciso B cuesta {-dif} menos que el A."
            else:
                t += "Ambos recorridos tienen el mismo costo."
        else:
            t += "No se puede comparar: falta al menos un recorrido válido."
        self.escribir(t)


# --------------------------------------------------------------
# 5. PROGRAMA PRINCIPAL
# --------------------------------------------------------------
if __name__ == "__main__":
    ventana = tk.Tk()
    App(ventana)
    ventana.mainloop()