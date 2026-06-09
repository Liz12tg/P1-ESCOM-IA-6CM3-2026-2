import heapq #para la cola de prioridad

# usa la funcion f(n)=g(n)+h(n)
# aqui ya se tiene en cuenta el costo del recorrido y la distasncia estimada
# hace el recorrido completo y es optimo dependiendo de la heuristica
# pero ocupa mas tiempo y mas memoria 


def a_estrella(grafo, heuristica, inicio, meta_func):
    open_list = []
    contador = 0
    g = {inicio: 0} #costo acumulado
    f = {inicio: heuristica[inicio]} #funcion de evaluacion
    heapq.heappush(open_list, (f[inicio], contador, inicio))
    padre = {inicio: None}
    closed = set()
    while open_list:
        _, _, actual = heapq.heappop(open_list) #pafa obtener el menor f(n)
        if actual in closed:
            continue
        closed.add(actual)
        yield "PASO", actual
        if meta_func(actual):
            camino = []
            while actual is not None:
                camino.append(actual)
                actual = padre[actual]
            yield "SOLUCION", camino[::-1]
            return
        for vecino, costo in grafo(actual):
            if vecino in closed:
                continue
            costo_temp = g[actual] + costo
            if vecino in g and costo_temp >= g[vecino]:
                continue
            padre[vecino] = actual
            g[vecino] = costo_temp
            f[vecino] = g[vecino] + heuristica[vecino]
            contador += 1
            heapq.heappush(open_list, (f[vecino], contador, vecino))
    yield "FIN", None
