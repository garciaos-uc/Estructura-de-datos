import heapq

grafo = {
    'A': [('B', 4), ('C', 2)],
    'B': [('A', 4), ('C', 1), ('D', 5)],
    'C': [('A', 2), ('B', 1), ('D', 8), ('E', 10)],
    'D': [('B', 5), ('C', 8), ('E', 2)],
    'E': [('C', 10), ('D', 2)]
}

def dijkstra(grafo, inicio):
    distancias = {nodo: float('inf') for nodo in grafo}
    distancias[inicio] = 0

    anteriores = {}
    pendientes = [(0, inicio)]

    while pendientes:
        distancia, actual = heapq.heappop(pendientes)

        if distancia > distancias[actual]:
            continue

        for vecino, peso in grafo[actual]:
            nueva = distancia + peso

            if nueva < distancias[vecino]:
                distancias[vecino] = nueva
                anteriores[vecino] = actual
                heapq.heappush(pendientes, (nueva, vecino))

    print("\nRESULTADOS DE DIJKSTRA")
    print("Vértice inicial:", inicio)

    for nodo in grafo:
        camino = []
        actual = nodo

        while actual != inicio:
            camino.append(actual)
            actual = anteriores.get(actual)

            if actual is None:
                break

        if actual is not None:
            camino.append(inicio)
            camino.reverse()
            print(f"{inicio} -> {nodo}: {distancias[nodo]} | Camino: {' -> '.join(camino)}")

dijkstra(grafo, 'A')