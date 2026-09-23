import random

cantidad_alumnos = 10000

materias_disponibles = [
    "Matemáticas",
    "Español",
    "Ciencias Naturales",
    "Historia",
    "Geografía",
    "Educación Física",
    "Artes",
    "Inglés",
    "Formación Cívica"
]

# Seleccionar seis materias al azar para todos los alumnos.
materias = random.sample(materias_disponibles, 6)

# Crear la matriz: 500 filas de alumnos y 6 columnas de materias.
calificaciones = []

for alumno in range(cantidad_alumnos):
    fila = []

    for materia in materias:
        fila.append(random.randint(0, 100))

    calificaciones.append(fila)

# Imprimir la tabla completa.
print("\nTABLA DE ALUMNOS Y CALIFICACIONES\n")

print(f"{'Alumno':<12}", end="")

for materia in materias:
    print(f"{materia:>20}", end="")

print()

for alumno in range(cantidad_alumnos):
    print(f"{alumno + 1:<12}", end="")

    for nota in calificaciones[alumno]:
        print(f"{nota:>20}", end="")

    print()

# Buscador simple.
while True:
    try:
        alumno = int(
            input("\nNúmero de alumno a buscar (1 a 500, 0 para salir): ")
        )
    except ValueError:
        print("Escribe un número entero.")
        continue

    if alumno == 0:
        print("Programa finalizado.")
        break

    if alumno < 1 or alumno > cantidad_alumnos:
        print("El número de alumno debe estar entre 1 y 500.")
        continue

    # Restar 1 porque las posiciones de la matriz empiezan en cero.
    print(f"\nCALIFICACIONES DEL ALUMNO {alumno}\n")
    print(f"{'Materia':<22}{'Calificación':>14}")

    for materia in range(len(materias)):
        nota = calificaciones[alumno - 1][materia]
        print(f"{materias[materia]:<22}{nota:>14}")
