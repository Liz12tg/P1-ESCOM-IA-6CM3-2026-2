import heapq

def gbfs(grafo, heuristica, inicio, meta_func):
    open_list = []
    contador = 0
    # Guardamos en la cola: (heurística, contador, nodo_actual)
    heapq.heappush(open_list, (heuristica[inicio], contador, inicio))
    
    padre = {inicio: None}
    closed = set()
    
    while open_list:
        # Extraemos el nodo con menor heurística
        _, _, actual = heapq.heappop(open_list)
        
        # Evaluamos si cumple la condición de meta usando la función de Sokoban
        if meta_func(actual):
            camino = []
            while actual is not None:
                camino.append(actual)
                actual = padre[actual]
            return camino[::-1]
        
        closed.add(actual)
        
        # ¡OJO! Se llama como función: grafo(actual)
        for vecino, _ in grafo(actual):
            if vecino in closed:
                continue
            if vecino not in padre:
                padre[vecino] = actual
                contador += 1
                heapq.heappush(open_list, (heuristica[vecino], contador, vecino))
                
    return None