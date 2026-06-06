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
        _, _, actual = heapq.heappop(open_list)
        
        # MANDAMOS EL ESTADO ACTUAL EN TIEMPO REAL AL NAVEGADOR
        yield "PASO", actual
        
        if meta_func(actual):
            camino = []
            while actual is not None:
                camino.append(actual)
                actual = padre[actual]
            
            # MANDAMOS LA SOLUCIÓN FINAL ENCONTRADA
            yield "SOLUCION", camino[::-1]
            return
        
        if actual in closed:
            continue
        closed.add(actual)
        
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
                
    yield "FIN", None