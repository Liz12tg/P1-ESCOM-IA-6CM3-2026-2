def dfs(inicio, meta, obtener_vecinos):
    pila = [inicio]
    visitados = {inicio}
    padres = {}
    while pila:
        actual = pila.pop()
        if actual == meta:
            camino = []
            while actual in padres:
                camino.append(actual)
                actual = padres[actual]
            camino.append(inicio)
            return camino[::-1]
        for vecino in reversed(obtener_vecinos(actual)):
            if vecino not in visitados:
                visitados.add(vecino)
                padres[vecino] = actual
                pila.append(vecino)
    return []