import heapq

#aqui solo se escoge h(n) sin considerar el costo del recorrido
#funcion f(n)=h(n)
#este algoritmo es muy rapido 
#pero puede caer en malas decisiones

def gbfs(grafo, heuristica, inicio, meta_func):
    open_list = []
    contador = 0
    heapq.heappush(open_list, (heuristica[inicio], contador, inicio))
    padre = {inicio: None}
    closed = set()
    while open_list:
        _, _, actual = heapq.heappop(open_list)
        yield "PASO", actual
        if meta_func(actual):
            camino = []
            while actual is not None:
                camino.append(actual)
                actual = padre[actual]
            yield "SOLUCION", camino[::-1]
            return
        if actual in closed:
            continue
        closed.add(actual)       
        for vecino, _ in grafo(actual):
            if vecino in closed:
                continue
            if vecino not in padre:
                padre[vecino] = actual
                contador += 1
                heapq.heappush(open_list, (heuristica[vecino], contador, vecino))               
    yield "FIN", None