import random
import statistics

# Generar lista de 50 números aleatorios entre 1 y 100
numeros = [random.randint(250, 350) for _ in range(50)]

print("Lista generada:")
print(numeros)

# Cálculos
media = statistics.mean(numeros)
mediana = statistics.median(numeros)
moda = statistics.mode(numeros)
varianza = statistics.variance(numeros)
desviacion = statistics.stdev(numeros)

print("\n--- Resultados ---")
print(f"Media = {media:.2f}")
print(f"Mediana = {mediana:.2f}")
print(f"Moda = {moda}")
print(f"Varianza = {varianza:.2f}")
print(f"Desviación estándar = {desviacion:.2f}")