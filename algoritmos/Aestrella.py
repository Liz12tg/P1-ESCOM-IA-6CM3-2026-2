import heapq

def a_estrella(grafo, heuristica, inicio, meta_func):
    open_list = []
    contador = 0
    
    g = {inicio: 0}
    f = {inicio: heuristica[inicio]}
    heapq.heappush(open_list, (f[inicio], contador, inicio))
    
    padre = {inicio: None}
    closed = set()
    
    while open_list:
        # Extraemos el nodo con menor F(n)
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
        for vecino, costo in grafo(actual):
            if vecino in closed:
                continue
            
            costo_temp = g[actual] + costo
            
            if vecino not in g or costo_temp < g[vecino]:
                padre[vecino] = actual
                g[vecino] = costo_temp
                f[vecino] = g[vecino] + heuristica[vecino]
                contador += 1
                heapq.heappush(open_list, (f[vecino], contador, vecino))
                
    return None