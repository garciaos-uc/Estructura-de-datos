import tkinter as tk
from tkinter import ttk
from collections import deque


# ----------------------------------------------------------------------
# LÓGICA DEL ÁRBOL BINARIO DE BÚSQUEDA
# ----------------------------------------------------------------------
class Nodo:
    def __init__(self, valor):
        self.valor = valor
        self.izq = None
        self.der = None


class ArbolBinarioBusqueda:
    def __init__(self):
        self.raiz = None

    def esta_vacio(self):
        return self.raiz is None

    def limpiar(self):
        self.raiz = None

    def buscar(self, valor):
        actual = self.raiz
        while actual is not None:
            if valor == actual.valor:
                return actual
            actual = actual.izq if valor < actual.valor else actual.der
        return None

    def insertar(self, valor):
        """Devuelve (exito, mensaje)."""
        if self.raiz is None:
            self.raiz = Nodo(valor)
            return True, f"{valor} se insertó como RAÍZ del árbol (nivel 0)."

        actual = self.raiz
        nivel = 0
        while True:
            if valor == actual.valor:
                return False, f"El número {valor} ya existe en el árbol. No se permiten duplicados."
            nivel += 1
            if valor < actual.valor:
                if actual.izq is None:
                    actual.izq = Nodo(valor)
                    return True, (f"{valor} < {actual.valor}: se insertó como hijo IZQUIERDO "
                                  f"de {actual.valor} (nivel {nivel}).")
                actual = actual.izq
            else:
                if actual.der is None:
                    actual.der = Nodo(valor)
                    return True, (f"{valor} > {actual.valor}: se insertó como hijo DERECHO "
                                  f"de {actual.valor} (nivel {nivel}).")
                actual = actual.der

    def eliminar(self, valor):
        """Devuelve (exito, mensaje)."""
        nodo = self.buscar(valor)
        if nodo is None:
            return False, f"El número {valor} no existe en el árbol."

        if nodo.izq is None and nodo.der is None:
            detalle = "era una hoja"
        elif nodo.izq is None or nodo.der is None:
            detalle = "tenía un hijo, que ocupó su lugar"
        else:
            sucesor = self._minimo(nodo.der)
            detalle = (f"tenía dos hijos, fue reemplazado por su sucesor inorden "
                       f"({sucesor.valor}), el menor de su rama derecha")

        self.raiz = self._eliminar(self.raiz, valor)
        return True, f"Se eliminó el {valor} ({detalle})."

    def _minimo(self, nodo):
        """Nodo con el valor más pequeño de un subárbol (el más a la izquierda)."""
        while nodo.izq is not None:
            nodo = nodo.izq
        return nodo

    def _eliminar(self, nodo, valor):
        if nodo is None:
            return None

        if valor < nodo.valor:
            nodo.izq = self._eliminar(nodo.izq, valor)
        elif valor > nodo.valor:
            nodo.der = self._eliminar(nodo.der, valor)
        else:
            # Caso 1 y 2: sin hijos o con un solo hijo
            if nodo.izq is None:
                return nodo.der
            if nodo.der is None:
                return nodo.izq

            # Caso 3: dos hijos -> sucesor inorden (mínimo de la rama derecha)
            sucesor = self._minimo(nodo.der)
            nodo.valor = sucesor.valor                          # copiar el valor del sucesor
            nodo.der = self._eliminar(nodo.der, sucesor.valor)  # quitar el sucesor de su lugar
        return nodo

    # ---------------- Recorridos ----------------
    def preorden(self):
        res = []

        def rec(n):
            if n:
                res.append(n.valor)
                rec(n.izq)
                rec(n.der)
        rec(self.raiz)
        return res

    def inorden(self):
        res = []

        def rec(n):
            if n:
                rec(n.izq)
                res.append(n.valor)
                rec(n.der)
        rec(self.raiz)
        return res

    def posorden(self):
        res = []

        def rec(n):
            if n:
                rec(n.izq)
                rec(n.der)
                res.append(n.valor)
        rec(self.raiz)
        return res

    def por_niveles(self):
        res = []
        if self.raiz is None:
            return res
        cola = deque([self.raiz])
        while cola:
            n = cola.popleft()
            res.append(n.valor)
            if n.izq:
                cola.append(n.izq)
            if n.der:
                cola.append(n.der)
        return res

    # ---------------- Datos para dibujar ----------------
    def posiciones(self):
        """Devuelve {valor: (columna, nivel)}; la columna es el índice inorden."""
        pos = {}
        contador = [0]

        def rec(n, nivel):
            if n is None:
                return
            rec(n.izq, nivel + 1)
            pos[n.valor] = (contador[0], nivel)
            contador[0] += 1
            rec(n.der, nivel + 1)
        rec(self.raiz, 0)
        return pos

    def aristas(self):
        """Devuelve lista de (padre, hijo, 'izq'|'der')."""
        lista = []

        def rec(n):
            if n is None:
                return
            if n.izq:
                lista.append((n.valor, n.izq.valor, "izq"))
            if n.der:
                lista.append((n.valor, n.der.valor, "der"))
            rec(n.izq)
            rec(n.der)
        rec(self.raiz)
        return lista


# ----------------------------------------------------------------------
# INTERFAZ GRÁFICA
# ----------------------------------------------------------------------
class AplicacionABB:
    RADIO = 22
    SEP_X = 58
    SEP_Y = 80
    MARGEN = 45

    COLOR_NODO = {
        "normal": "#bbdefb",
        "nuevo": "#ce93d8",
        "actual": "#ff7043",
        "visitado": "#ffd54f",
    }
    COLOR_BORDE = "#0d47a1"
    COLOR_IZQ = "#1565c0"
    COLOR_DER = "#2e7d32"

    def __init__(self, root):
        self.root = root
        self.root.title("Árbol Binario de Búsqueda - Visualizador")
        self.root.geometry("1050x720")
        self.root.minsize(820, 560)

        self.arbol = ArbolBinarioBusqueda()
        self.estados = {}        # valor -> "nuevo" | "actual" | "visitado"
        self.animando = False
        self.botones = []

        ttk.Style().theme_use("clam")
        self._crear_controles()
        self._crear_leyenda()
        self._crear_canvas()
        self._crear_resultados()
        self.mostrar_estado("Bienvenido. Escribe un número y presiona «Agregar».", "info")
        self.dibujar()

    # ---------------- Construcción de la interfaz ----------------
    def _crear_controles(self):
        marco = ttk.LabelFrame(self.root, text=" Controles ", padding=8)
        marco.pack(fill="x", padx=10, pady=(10, 4))

        fila1 = ttk.Frame(marco)
        fila1.pack(fill="x")
        ttk.Label(fila1, text="Número:").pack(side="left")
        self.entrada = ttk.Entry(fila1, width=12, font=("Arial", 12))
        self.entrada.pack(side="left", padx=6)
        self.entrada.bind("<Return>", lambda e: self.agregar())
        self.entrada.focus()

        self.botones.append(self._boton(fila1, "Agregar", self.agregar))
        self.botones.append(self._boton(fila1, "Eliminar", self.eliminar))
        self.botones.append(self._boton(fila1, "Limpiar árbol", self.limpiar))

        self.velocidad = tk.Scale(fila1, from_=200, to=1500, resolution=100,
                                  orient="horizontal", length=170,
                                  label="Pausa del recorrido (ms)")
        self.velocidad.set(700)
        self.velocidad.pack(side="right")

        fila2 = ttk.Frame(marco)
        fila2.pack(fill="x", pady=(8, 0))
        ttk.Label(fila2, text="Recorridos:").pack(side="left")
        recorridos = [
            ("Preorden", "Preorden (Raíz, Izq, Der)", self.arbol.preorden),
            ("Inorden", "Inorden (Izq, Raíz, Der)", self.arbol.inorden),
            ("Posorden", "Posorden (Izq, Der, Raíz)", self.arbol.posorden),
            ("Por niveles", "Por niveles (anchura)", self.arbol.por_niveles),
        ]
        for texto, titulo, funcion in recorridos:
            b = self._boton(fila2, texto,
                            lambda t=titulo, f=funcion: self.recorrer(t, f))
            self.botones.append(b)

    def _boton(self, padre, texto, comando):
        b = ttk.Button(padre, text=texto, command=comando)
        b.pack(side="left", padx=4)
        return b

    def _crear_leyenda(self):
        marco = ttk.Frame(self.root)
        marco.pack(fill="x", padx=12, pady=2)

        def item(color, texto, linea=False):
            c = tk.Canvas(marco, width=30, height=16, highlightthickness=0)
            if linea:
                c.create_line(2, 8, 28, 8, fill=color, width=3)
            else:
                c.create_oval(8, 1, 24, 15, fill=color, outline=self.COLOR_BORDE)
            c.pack(side="left")
            ttk.Label(marco, text=texto).pack(side="left", padx=(0, 12))

        item(self.COLOR_IZQ, "Rama izquierda (I)", linea=True)
        item(self.COLOR_DER, "Rama derecha (D)", linea=True)
        item(self.COLOR_NODO["nuevo"], "Nodo nuevo")
        item(self.COLOR_NODO["actual"], "Nodo actual")
        item(self.COLOR_NODO["visitado"], "Nodo visitado")

    def _crear_canvas(self):
        marco = ttk.Frame(self.root)
        marco.pack(fill="both", expand=True, padx=10, pady=4)
        marco.rowconfigure(0, weight=1)
        marco.columnconfigure(0, weight=1)

        self.canvas = tk.Canvas(marco, bg="white", highlightthickness=1,
                                highlightbackground="#90a4ae")
        sb_x = ttk.Scrollbar(marco, orient="horizontal", command=self.canvas.xview)
        sb_y = ttk.Scrollbar(marco, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(xscrollcommand=sb_x.set, yscrollcommand=sb_y.set)
        self.canvas.grid(row=0, column=0, sticky="nsew")
        sb_y.grid(row=0, column=1, sticky="ns")
        sb_x.grid(row=1, column=0, sticky="ew")
        self.canvas.bind("<Configure>", lambda e: self.dibujar())

    def _crear_resultados(self):
        marco = ttk.LabelFrame(self.root, text=" Resultados ", padding=6)
        marco.pack(fill="x", padx=10, pady=(4, 10))

        self.lbl_estado = tk.Label(marco, text="", anchor="w", justify="left",
                                   font=("Arial", 10, "bold"), wraplength=980)
        self.lbl_estado.pack(fill="x")

        self.texto = tk.Text(marco, height=3, wrap="word", font=("Consolas", 12),
                             state="disabled", bg="#f5f5f5")
        self.texto.pack(fill="x", pady=(4, 0))

    # ---------------- Utilidades de interfaz ----------------
    def mostrar_estado(self, mensaje, tipo="info"):
        colores = {"ok": "#2e7d32", "error": "#c62828", "info": "#37474f"}
        self.lbl_estado.config(text=mensaje, fg=colores.get(tipo, "#37474f"))

    def mostrar_resultado(self, texto):
        self.texto.config(state="normal")
        self.texto.delete("1.0", "end")
        self.texto.insert("1.0", texto)
        self.texto.config(state="disabled")

    def bloquear(self, bloqueado):
        self.animando = bloqueado
        estado = "disabled" if bloqueado else "normal"
        for b in self.botones:
            b.config(state=estado)
        self.entrada.config(state=estado)

    def leer_numero(self):
        texto = self.entrada.get().strip()
        try:
            return int(texto)
        except ValueError:
            self.mostrar_estado("Entrada inválida: escribe un número entero (ej. 25 o -7).", "error")
            self.entrada.focus()
            return None

    # ---------------- Operaciones ----------------
    def agregar(self):
        if self.animando:
            return
        valor = self.leer_numero()
        if valor is None:
            return
        exito, mensaje = self.arbol.insertar(valor)
        self.estados = {valor: "nuevo"} if exito else {}
        self.mostrar_estado(mensaje, "ok" if exito else "error")
        self.entrada.delete(0, "end")
        self.entrada.focus()
        self.dibujar()

    def eliminar(self):
        if self.animando:
            return
        valor = self.leer_numero()
        if valor is None:
            return
        exito, mensaje = self.arbol.eliminar(valor)
        self.estados = {}
        self.mostrar_estado(mensaje, "ok" if exito else "error")
        self.entrada.delete(0, "end")
        self.entrada.focus()
        self.dibujar()

    def limpiar(self):
        if self.animando:
            return
        self.arbol.limpiar()
        self.estados = {}
        self.mostrar_resultado("")
        self.mostrar_estado("El árbol fue limpiado por completo.", "info")
        self.dibujar()

    # ---------------- Recorridos animados ----------------
    def recorrer(self, titulo, funcion):
        if self.animando:
            return
        if self.arbol.esta_vacio():
            self.mostrar_estado("El árbol está vacío. Agrega números antes de recorrerlo.", "error")
            return
        orden = funcion()
        self.estados = {}
        self.mostrar_resultado("")
        self.mostrar_estado(f"Recorrido {titulo}...", "info")
        self.bloquear(True)
        self._paso(titulo, orden, 0)

    def _paso(self, titulo, orden, i):
        if i > 0:
            self.estados[orden[i - 1]] = "visitado"

        if i >= len(orden):
            self.mostrar_resultado(f"{titulo}:\n" + "  →  ".join(map(str, orden)))
            self.mostrar_estado(f"Recorrido {titulo} completado.", "ok")
            self.dibujar()
            self.bloquear(False)
            return

        self.estados[orden[i]] = "actual"
        self.mostrar_resultado(f"{titulo}:\n" + "  →  ".join(map(str, orden[:i + 1])))
        self.dibujar()
        self.root.after(self.velocidad.get(), self._paso, titulo, orden, i + 1)

    # ---------------- Dibujo del árbol ----------------
    def dibujar(self):
        c = self.canvas
        c.delete("all")
        ancho_vista = max(c.winfo_width(), 200)
        alto_vista = max(c.winfo_height(), 200)

        if self.arbol.esta_vacio():
            c.configure(scrollregion=(0, 0, ancho_vista, alto_vista))
            c.create_text(ancho_vista / 2, alto_vista / 2,
                          text="El árbol está vacío.\nAgrega un número para comenzar.",
                          font=("Arial", 16), fill="#90a4ae", justify="center")
            return

        pos = self.arbol.posiciones()
        columnas = max(p[0] for p in pos.values()) + 1
        niveles = max(p[1] for p in pos.values()) + 1

        ancho_arbol = (columnas - 1) * self.SEP_X
        ancho_total = max(ancho_arbol + 2 * self.MARGEN, ancho_vista)
        alto_total = max(niveles * self.SEP_Y + 2 * self.MARGEN, alto_vista)
        desplazamiento = (ancho_total - ancho_arbol) / 2

        coords = {v: (desplazamiento + col * self.SEP_X, self.MARGEN + niv * self.SEP_Y)
                  for v, (col, niv) in pos.items()}
        c.configure(scrollregion=(0, 0, ancho_total, alto_total))

        # Líneas primero (quedan debajo de los círculos)
        for padre, hijo, lado in self.arbol.aristas():
            x1, y1 = coords[padre]
            x2, y2 = coords[hijo]
            color = self.COLOR_IZQ if lado == "izq" else self.COLOR_DER
            c.create_line(x1, y1, x2, y2, fill=color, width=3)
            mx, my = (x1 + x2) / 2, (y1 + y2) / 2
            dx = -10 if lado == "izq" else 10
            c.create_text(mx + dx, my, text="I" if lado == "izq" else "D",
                          fill=color, font=("Arial", 9, "bold"))

        # Nodos
        r = self.RADIO
        for valor, (x, y) in coords.items():
            relleno = self.COLOR_NODO[self.estados.get(valor, "normal")]
            c.create_oval(x - r, y - r, x + r, y + r, fill=relleno,
                          outline=self.COLOR_BORDE, width=2)
            fuente = ("Arial", 11, "bold") if len(str(valor)) <= 3 else ("Arial", 8, "bold")
            c.create_text(x, y, text=str(valor), font=fuente)


if __name__ == "__main__":
    ventana = tk.Tk()
    AplicacionABB(ventana)
    ventana.mainloop()