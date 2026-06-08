#exploración por profundidad

#basicamente es lo mismo que bfs pero usando pila 
def dfs(inicio, meta, obtener_vecinos):
    pila = [inicio] #estructura principal Pila LIFO
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
        for vecino in reversed(obtener_vecinos(actual)): #se usa este porque la pila invierte el orden 
            if vecino not in visitados:
                visitados.add(vecino)
                padres[vecino] = actual
                pila.append(vecino)
    return []

#a diferencia de bfs, no se explora completo siempre y no es del todo óptimo 
#pero ocupa menos memoria que bfs
#puede encontrar muy malos caminos