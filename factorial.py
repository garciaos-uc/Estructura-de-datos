import time
inicio = time.perf_counter()
def factorial(n):
    if n == 0:
         
     return 1
    else:
     return n * factorial(n-1)
a = 5
print (factorial(a))
fin = time.perf_counter()
print (f"Tiempo de ejecución: {fin - inicio:.4f} segundos")