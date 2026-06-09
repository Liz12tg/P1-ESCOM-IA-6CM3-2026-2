from collections import deque
#exploración por niveles

def bfs(inicio, meta, obtener_vecinos):
    cola = deque([inicio]) #estructura principal cola FIFO
    visitados = {inicio}
    padres = {}
    while cola: # mientras haya nodos 
        actual = cola.popleft() #sale el primero
        if actual == meta: #si encontro la meta reconstruye el camino
            camino = [] 
            while actual in padres:
                camino.append(actual)
                actual = padres[actual]
            camino.append(inicio)
            return camino[::-1]
        for vecino in obtener_vecinos(actual): #expandir nodos
            if vecino not in visitados: #y si no es visitado
                visitados.add(vecino) #se marca como visitado
                padres[vecino] = actual #se guarda el padre
                cola.append(vecino) #y se agrega a la cola
    return []


#encuentra el camino más corto pero consume mucha energía
#lo encientra porque explora cada nivel comletamnete antes de avanzar 
