import tkinter as tk

pila = []
MAX = 7


def dibujar():
    c.delete("all")
    for i, v in enumerate(pila):
        y = 280 - i * 40
        c.create_rectangle(50, y, 200, y + 40, fill="skyblue", outline="black")
        c.create_text(125, y + 20, text=v, font=("Arial", 14))
    if pila:
        y = 280 - (len(pila) - 1) * 40 + 20
        c.create_text(215, y, text="← TOP", fill="red", anchor="w")
    msg.config(text=f"Tamaño: {len(pila)}")


def push():
    valor = entrada.get().strip()
    if not valor:
        return
    if len(pila) >= MAX:
        msg.config(text="¡Pila llena! (Overflow)")
        return
    pila.append(valor)
    entrada.delete(0, "end")
    dibujar()


def pop():
    if not pila:
        msg.config(text="¡Pila vacía! (Underflow)")
        return
    pila.pop()
    dibujar()


ventana = tk.Tk()
ventana.title("Pila")
c = tk.Canvas(ventana, width=300, height=330, bg="white")
c.pack()
entrada = tk.Entry(ventana)
entrada.pack(pady=5)
entrada.bind("<Return>", lambda e: push())
tk.Button(ventana, text="Push", command=push).pack(side="left", padx=20)
tk.Button(ventana, text="Pop", command=pop).pack(side="right", padx=20)
msg = tk.Label(ventana, text="Tamaño: 0")
msg.pack()
dibujar()
ventana.mainloop()