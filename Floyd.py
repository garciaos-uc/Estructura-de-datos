INF = float('inf')

distancias = [
    [0,   4,   2,   INF, INF],
    [4,   0,   1,   5,   INF],
    [2,   1,   0,   8,   10],
    [INF, 5,   8,   0,   2],
    [INF, INF, 10,  2,   0]
]

vertices = ['A', 'B', 'C', 'D', 'E']
n = len(distancias)

print("MATRIZ INICIAL")
for fila in distancias:
    print(fila)

for k in range(n):
    for i in range(n):
        for j in range(n):
            nuevo = distancias[i][k] + distancias[k][j]

            if nuevo < distancias[i][j]:
                distancias[i][j] = nuevo

print("\nMATRIZ FINAL DE DISTANCIAS MINIMAS")
print("    ", vertices)

for i in range(n):
    print(vertices[i], distancias[i])