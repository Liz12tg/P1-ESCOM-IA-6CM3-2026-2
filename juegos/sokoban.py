import json
from collections import deque
from algoritmos.Aestrella import a_estrella
from algoritmos.GBFS import gbfs

class Sokoban:
    def __init__(self, nivel=1):
        # Mapas extraídos con total precisión de tus capturas de pantalla
        self.niveles = {
            1: [ 
                [" "," ","#","#","#","#","#"," "],
                ["#","#","#"," "," "," ","#"," "],
                ["#",".","@","$"," "," ","#"," "],
                ["#","#","#"," ","$",".","#"," "],
                ["#",".","#","#","$"," ","#"," "],
                ["#"," ","#"," ","."," ","#"," "],
                ["#","$"," ","$","$","$",".","#"],
                ["#"," "," "," ","."," "," ","#"],
                ["#","#","#","#","#","#","#","#"]
            ],
            2: [ 
                [" "," "," "," ","#","#","#","#","#"," "," "," "," "," "," "," "," "," "," "," "," "," "," "],
                [" "," "," "," ","#"," "," "," ","#"," "," "," "," "," "," "," "," "," "," "," "," "," "," "],
                [" "," "," "," ","#","$"," "," ","#"," "," "," "," "," "," "," "," "," "," "," "," "," "," "],
                [" "," ","#","#","#"," "," ","$","#","#","#"," "," "," "," "," "," "," "," "," "," "," "," "],
                [" "," ","#"," "," ","$"," "," ","$"," ","#"," "," "," "," "," "," "," "," "," "," "," "," "],
                ["#","#","#"," ","#"," ","#","#","#"," ","#"," "," "," "," "," ","#","#","#","#","#","#","#"],
                ["#"," "," "," ","#"," ","#","#","#"," ","#","#","#","#","#","#","#"," "," "," ",".",".","#"],
                ["#"," ","$"," "," ","$"," "," "," "," "," "," "," "," "," "," "," "," "," "," ",".",".","#"],
                ["#","#","#","#","#"," ","#","#","#","#"," ","#","@","#","#","#","#"," "," "," ",".",".","#"],
                [" "," "," "," ","#"," "," "," "," "," "," ","#","#","#"," "," ","#","#","#","#","#","#","#"],
                [" "," "," "," ","#","#","#","#","#","#","#","#"," "," "," "," "," "," "," "," "," "," ","#"]
            ],
            3: [ 
                ["#","#","#","#","#","#","#","#","#","#","#","#"," "," "],
                ["#",".","."," "," ","#"," "," "," "," "," ","#","#","#"],
                ["#",".","."," "," ","#"," ","$"," "," ","$"," "," ","#"],
                ["#",".","."," "," ","#","$","#","#","#","#"," "," ","#"],
                ["#",".","."," "," "," "," ","@"," ","#","#"," "," ","#"],
                ["#",".","."," "," ","#"," ","#"," "," ","$"," ","#","#"],
                ["#","#","#","#","#","#"," ","#","#","$"," ","$"," ","#"],
                [" "," ","#"," ","$"," "," ","$"," ","$"," ","$"," ","#"],
                [" "," ","#"," "," "," "," ","#"," "," "," "," "," ","#"],
                [" "," ","#","#","#","#","#","#","#","#","#","#","#","#"]
            ]
        }
        self.mapa_inicial = self.niveles.get(nivel, self.niveles[1])
        self.jugador_inicial, self.metas, self.paredes, cajas_iniciales = self.procesar_mapa()
        
        self.zonas_muertas = self.calcular_zonas_muertas()
        self.estado_inicial = (self.jugador_inicial, tuple(sorted(cajas_iniciales)))

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
                elif val == '*':
                    metas.add((r, c))
                    cajas.add((r, c))
        return jugador, frozenset(metas), frozenset(paredes), tuple(sorted(cajas))

    def calcular_zonas_muertas(self):
        muertas = set()
        max_r = len(self.mapa_inicial)
        max_c = len(self.mapa_inicial[0])
        for r in range(max_r):
            for c in range(max_c):
                if (r, c) in self.paredes or (r, c) in self.metas:
                    continue
                arriba = (r-1, c) in self.paredes
                abajo = (r+1, c) in self.paredes
                izq = (r, c-1) in self.paredes
                der = (r, c+1) in self.paredes
                if (arriba or abajo) and (izq or der):
                    muertas.add((r, c))
        return muertas

    def es_deadlock(self, cajas):
        for caja in cajas:
            if caja in self.zonas_muertas:
                return True
        return False

    def obtener_vecinos(self, estado):
        jugador, cajas = estado
        cajas_set = set(cajas)
        movimientos = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        proximos_estados = []

        r, c = jugador
        for dr, dc in movimientos:
            nr, nc = r + dr, c + dc
            
            if (nr, nc) not in self.paredes and (nr, nc) not in cajas_set:
                proximos_estados.append((((nr, nc), cajas), 1))
            
            elif (nr, nc) in cajas_set:
                destino_caja_r, destino_caja_c = nr + dr, nc + dc
                if (destino_caja_r, destino_caja_c) not in self.paredes and (destino_caja_r, destino_caja_c) not in cajas_set:
                    nuevas_cajas = list(cajas)
                    nuevas_cajas.remove((nr, nc))
                    nuevas_cajas.append((destino_caja_r, destino_caja_c))
                    
                    if not self.es_deadlock(nuevas_cajas):
                        estado_cajas = tuple(sorted(nuevas_cajas))
                        proximos_estados.append((((nr, nc), estado_cajas), 1))

        return proximos_estados

    def calcular_heuristica(self, estado):
        jugador, cajas = estado
        total_h = 0
        
        # 1. Distancia de las cajas a las metas (multiplicada para darle más prioridad sobre el movimiento del jugador)
        for caja in cajas:
            distancias = [abs(meta[0] - caja[0]) + abs(meta[1] - caja[1]) for meta in self.metas]
            total_h += (min(distancias) * 5) if distancias else 0
            
        # 2. PENALIZACIÓN DINÁMICA: Si el jugador camina alejándose de las cajas, el estado se vuelve carísimo.
        # Esto evita que explore pasillos vacíos y lo obliga a quedarse pegado empujando cajas.
        if cajas:
            distancia_al_bloque = min([abs(jugador[0] - caja[0]) + abs(jugador[1] - caja[1]) for caja in cajas])
            total_h += distancia_al_bloque
            
        return total_h

    def es_meta(self, estado):
        _, cajas = estado
        return self.metas.issubset(set(cajas))

    def resolver_para_web(self, algoritmo_nombre):
        grafo_dinamico = {}
        heuristica_dinamica = {}
        heuristica_dinamica[self.estado_inicial] = self.calcular_heuristica(self.estado_inicial)
        
        nodos_explorados = [0]
        
        def funcion_grafo(nodo):
            nodos_explorados[0] += 1
            if nodo not in grafo_dinamico:
                vecinos = self.obtener_vecinos(nodo)
                grafo_dinamico[nodo] = vecinos
                for vecino, _ in vecinos:
                    if vecino not in heuristica_dinamica:
                        heuristica_dinamica[vecino] = self.calcular_heuristica(vecino)
            return grafo_dinamico[nodo]

        if algoritmo_nombre == "A_ESTRELLA":
            generador_busqueda = a_estrella(funcion_grafo, heuristica_dinamica, self.estado_inicial, self.es_meta)
        else:
            generador_busqueda = gbfs(funcion_grafo, heuristica_dinamica, self.estado_inicial, self.es_meta)

        for evento, datos in generador_busqueda:
            if evento == "PASO":
                jugador, cajas = datos
                yield f"data: {json.dumps({'evento': 'paso', 'jugador': list(jugador), 'cajas': [list(c) for c in cajas], 'metas': [list(m) for m in self.metas], 'paredes': [list(p) for p in self.paredes]})}\n\n"
            
            elif evento == "SOLUCION":
                camino_json = [{"jugador": list(j), "cajas": [list(c) for c in cb]} for j, cb in datos]
                yield f"data: {json.dumps({'evento': 'solucion', 'pasos': camino_json})}\n\n"
            
            elif evento == "FIN":
                yield f"data: {json.dumps({'evento': 'error'})}\n\n"