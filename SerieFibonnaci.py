def fibonacci(n):
    serie = []
    a, b = 0, 1              # Valor inicial 
    for _ in range(n):
        serie.append(a)      # se guarda el número actual
        a, b = b, a + b      # avanza el siguiente es la suma de los dos anteriores
    return serie


def main():
    n = int(input("¿Cuántos números de la serie quieres ver? "))
    if n <= 0:
        print("Ingresa un número mayor que 0.")
    else:
        print("Serie de Fibonacci:", *fibonacci(n))


if __name__ == "__main__":
    main()