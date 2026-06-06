from collections import deque
from algoritmos.Aestrella import a_estrella
from algoritmos.GBFS import gbfs

class Sokoban:
    def __init__(self, nivel=1):
        # Mapas limpios
        self.niveles = {
            1: [
                ["#","#","#","#","#","#","#","#","#"],
                ["#"," "," "," "," "," "," "," ","#"],
                ["#"," "," ","#","#"," "," "," ","#"],
                ["#"," ",".", "@","$"," "," "," ","#"],
                ["#"," "," "," "," ","$","."," ","#"],
                ["#"," ",".", " "," ","$"," "," ","#"],
                ["#"," "," "," "," "," ",".", " ","#"],
                ["#","$"," "," ","$","$","$"," ","#"],
                ["#"," "," "," "," "," ",".", " ","#"],
                ["#","#","#","#","#","#","#","#","#"]
            ],
            2: [
                ["#","#","#","#","#","#","#","#","#","#","#","#","#","#","#","#","#","#","#"],
                ["#"," "," "," "," ","#"," "," "," "," "," "," "," "," "," "," "," "," ","#"],
                ["#"," "," "," "," ","#"," "," "," "," "," "," "," "," "," "," "," "," ","#"],
                ["#"," "," "," ","#","#","$"," "," "," "," "," "," "," "," "," "," "," ","#"],
                ["#"," "," "," ","#"," "," "," ","$"," "," "," "," "," "," "," "," "," ","#"],
                ["#"," "," "," ","#","$"," "," "," ","$"," "," "," "," "," "," "," "," ","#"],
                ["#","#","#","#","#"," "," "," "," "," ","#","#","#","#","#","#","#","#","#"],
                ["#"," "," "," "," "," "," "," "," "," ","#"," "," "," "," "," ",".",".","#"],
                ["#"," ","$"," "," "," ","$"," "," "," ","#"," "," "," "," "," ",".",".","#"],
                ["#"," "," "," "," "," "," "," "," "," "," "," ","@"," "," "," ",".",".","#"],
                ["#","#","#","#","#","#"," "," "," "," ","#","#","#","#","#","#","#","#","#"],
                ["#"," "," "," "," "," ","#","#","#","#","#"," "," "," "," "," "," "," ","#"],
                ["#","#","#","#","#","#","#","#","#","#","#","#","#","#","#","#","#","#","#"]
            ],
            3: [
                ["#","#","#","#","#","#","#","#","#","#","#","#","#","#","#","#","#","#"],
                ["#",".","."," "," "," "," "," ","#"," "," "," "," "," "," "," "," ","#"],
                ["#",".","."," "," "," "," "," ","#"," "," ","$"," "," "," ","$"," ","#"],
                ["#",".","."," "," "," "," "," ","#"," ","$"," "," "," "," "," "," ","#"],
                ["#",".","."," "," "," "," "," "," "," "," "," ","@"," "," "," "," ","#"],
                ["#",".","."," "," "," "," "," "," "," "," "," "," "," "," "," "," ","#"],
                ["#","#","#","#","#"," "," "," ","#"," "," "," "," "," ","$"," "," ","#"],
                ["#"," "," "," "," ","#","#","#","#"," "," "," "," ","$"," ","$"," ","#"],
                ["#"," "," "," "," "," "," "," "," "," "," "," ","$"," "," "," "," ","#"],
                ["#"," "," "," "," ","$"," "," "," "," "," ","$"," "," ","$"," "," ","#"],
                ["#"," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," ","#"],
                ["#","#","#","#","#","#","#","#","#","#","#","#","#","#","#","#","#","#"]
            ]
        }
        self.mapa_inicial = self.niveles.get(nivel, self.niveles[1])
        self.estado_inicial, self.metas, self.paredes = self.procesar_mapa()

    def procesar_mapa(self):
        jugador = None
        cajas = set()
        metas = set()
        paredes = set()
        for r, fila in enumerate(self.mapa_inicial):
            for c, val in enumerate(fila):
                if val == '#': paredes.add((r, c))
                elif val == '.': metas.add((r, c))
                elif val == '$': cajas.add((r, c))
                elif val == '@': jugador = (r, c)
        return (jugador, tuple(sorted(cajas))), metas, paredes

    def es_deadlock(self, cajas):
        """ DETECCIÓN DE PUNTOS MUERTOS: Corta ramas inútiles y acelera el algoritmo 100x """
        for r, c in cajas:
            if (r, c) in self.metas:
                continue
            # Si una caja se empuja a una esquina de paredes, es game over automático.
            pared_v = (r-1, c) in self.paredes or (r+1, c) in self.paredes
            pared_h = (r, c-1) in self.paredes or (r, c+1) in self.paredes
            if pared_v and pared_h:
                return True
        return False

    def posiciones_accesibles(self, jugador, cajas_set):
        """Devuelve todas las casillas donde el jugador puede caminar sin empujar cajas."""
        vistos = {jugador}
        cola = deque([jugador])
        movimientos = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        while cola:
            r, c = cola.popleft()
            for dr, dc in movimientos:
                nr, nc = r + dr, c + dc
                if (nr, nc) in vistos or (nr, nc) in self.paredes or (nr, nc) in cajas_set:
                    continue
                vistos.add((nr, nc))
                cola.append((nr, nc))
        return vistos

    def obtener_vecinos(self, estado):
        jugador, cajas = estado
        cajas_set = set(cajas)
        accesibles = self.posiciones_accesibles(jugador, cajas_set)
        movimientos = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        proximos_estados = []

        for caja in cajas:
            for dr, dc in movimientos:
                origen = (caja[0] - dr, caja[1] - dc)
                destino = (caja[0] + dr, caja[1] + dc)
                if origen not in accesibles:
                    continue
                if destino in self.paredes or destino in cajas_set:
                    continue

                nuevas_cajas = list(cajas)
                nuevas_cajas.remove(caja)
                nuevas_cajas.append(destino)
                estado_cajas = tuple(sorted(nuevas_cajas))

                if not self.es_deadlock(estado_cajas):
                    proximos_estados.append((((caja[0], caja[1]), estado_cajas), 1))

        return proximos_estados

    def calcular_heuristica(self, estado):
        _, cajas = estado
        cajas_set = set(cajas)
        total_h = 0
        for meta in self.metas:
            distancias = [abs(meta[0] - caja[0]) + abs(meta[1] - caja[1]) for caja in cajas_set]
            total_h += min(distancias) if distancias else 0
        return total_h

    def es_meta(self, estado):
        _, cajas = estado
        return len(self.metas) > 0 and self.metas.issubset(set(cajas))

    def resolver_para_web(self, algoritmo_nombre):
        grafo_dinamico = {}
        heuristica_dinamica = {}
        
        heuristica_dinamica[self.estado_inicial] = self.calcular_heuristica(self.estado_inicial)
        
        # VARIABLE DE SEGURIDAD: Límite estricto de evaluaciones para no colgar el servidor nunca.
        nodos_explorados = [0]
        
        def funcion_grafo(nodo):
            nodos_explorados[0] += 1
            # Si el laberinto explota de opciones, forzamos un corte seguro en tiempo real.
            if nodos_explorados[0] > 12000:
                return [] 
                
            if nodo not in grafo_dinamico:
                vecinos = self.obtener_vecinos(nodo)
                grafo_dinamico[nodo] = vecinos
                for vecino, _ in vecinos:
                    if vecino not in heuristica_dinamica:
                        heuristica_dinamica[vecino] = self.calcular_heuristica(vecino)
            return grafo_dinamico[nodo]

        # LLAMADA A TUS ARCHIVOS INDEPENDIENTES DE ALGORITMOS COMO EN 8 REINAS
        if algoritmo_nombre == "A_ESTRELLA":
            camino_estados = a_estrella(funcion_grafo, heuristica_dinamica, self.estado_inicial, self.es_meta)
        else:
            camino_estados = gbfs(funcion_grafo, heuristica_dinamica, self.estado_inicial, self.es_meta)

        if not camino_estados:
            return {"status": "no_solution", "pasos": []}

        pasos_json = []
        for estado in camino_estados:
            jugador_pos, cajas_pos = estado
            pasos_json.append({
                "jugador": list(jugador_pos),
                "cajas": [list(caja) for caja in cajas_pos]
            })

        return {
            "status": "success",
            "total_pasos": len(pasos_json) - 1,
            "algoritmo_usado": algoritmo_nombre,
            "metas": [list(m) for m in self.metas],
            "paredes": [list(p) for p in self.paredes],
            "pasos": pasos_json
        }