from collections import deque

def bfs(inicio, meta, obtener_vecinos):
    cola = deque([inicio])
    visitados = {inicio}
    padres = {}
    while cola:
        actual = cola.popleft()
        if actual == meta:
            camino = []
            while actual in padres:
                camino.append(actual)
                actual = padres[actual]
            camino.append(inicio)
            return camino[::-1]
        for vecino in obtener_vecinos(actual):
            if vecino not in visitados:
                visitados.add(vecino)
                padres[vecino] = actual
                cola.append(vecino)
    return []