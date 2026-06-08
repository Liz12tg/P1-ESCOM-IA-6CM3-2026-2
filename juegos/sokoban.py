import json
from collections import deque
from algoritmos.Aestrella import a_estrella
from algoritmos.GBFS import gbfs

#Algortimos de busqueda informada
#Aqui ya se usa heuristica 
#es la funcion que estima que tan lejos se esta de la meta 
#se usa distancia Manhattan
#h(n)=∣x1​−x2​∣+∣y1​−y2​∣

#el mejor algoritmo para este juego es A* porque sokobam tiene muchos estados engañosos y 
#GBFS puede acercarse a una meta y generar bloqueos
#mientras que A* considera el costo acumulado y evita muchas malas decisiones

class Sokoban:
    def __init__(self, nivel=1):
        # MAPAS ORIGINALES TOTALMENTE INTACTOS
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
        self.max_r = len(self.mapa_inicial)
        self.jugador_inicial, self.metas, self.paredes, cajas_iniciales = self.procesar_mapa()
        
        self.espacio_valido = self.calcular_espacio_valido()
        self.zonas_muertas = self.calcular_zonas_muertas()
        
        # El estado ahora es: (posición_jugador, tupla_de_cajas)
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

    def calcular_espacio_valido(self):
        validos = set([self.jugador_inicial])
        cola = deque([self.jugador_inicial])
        while cola:
            r, c = cola.popleft()
            for dr, dc in [(-1,0), (1,0), (0,-1), (0,1)]:
                nr, nc = r + dr, c + dc
                if 0 <= nr < self.max_r and 0 <= nc < len(self.mapa_inicial[nr]):
                    if (nr, nc) not in self.paredes and (nr, nc) not in validos:
                        validos.add((nr, nc))
                        cola.append((nr, nc))
        return validos

    def calcular_zonas_muertas(self):
        muertas = set()
        for (r, c) in self.espacio_valido:
            if (r, c) in self.metas: continue
            arriba = (r-1, c) in self.paredes
            abajo = (r+1, c) in self.paredes
            izq = (r, c-1) in self.paredes
            der = (r, c+1) in self.paredes
            if (arriba or abajo) and (izq or der):
                muertas.add((r, c))
        return muertas

    def es_deadlock(self, cajas_set):
        for cr, cc in cajas_set:
            if (cr, cc) in self.zonas_muertas: return True
            if (cr, cc) in self.metas: continue
            for dr, dc in [(-1, -1), (-1, 1), (1, -1), (1, 1)]:
                if (cr+dr, cc) in self.paredes and (cr, cc+dc) in self.paredes: return True
                if (cr+dr, cc) in cajas_set and (cr, cc+dc) in cajas_set: return True
        return False

    def obtener_vecinos(self, estado):
        jugador, cajas = estado
        cajas_set = set(cajas)
        proximos = []
        
        # Encontrar todas las celdas accesibles por el jugador sin mover cajas
        accesibles = set([jugador])
        cola = deque([jugador])
        while cola:
            r, c = cola.popleft()
            for dr, dc in [(-1,0), (1,0), (0,-1), (0,1)]:
                nr, nc = r + dr, c + dc
                if (nr, nc) in self.espacio_valido and (nr, nc) not in cajas_set and (nr, nc) not in accesibles:
                    accesibles.add((nr, nc))
                    cola.append((nr, nc))
                    
        # Generar movimientos únicamente si el jugador está adyacente a una caja y puede empujarla
        for cr, cc in cajas:
            for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                pos_jugador = (cr - dr, cc - dc)
                if pos_jugador in accesibles:
                    destino_r, destino_c = cr + dr, cc + dc
                    if (destino_r, destino_c) in self.espacio_valido and (destino_r, destino_c) not in cajas_set:
                        nuevas = set(cajas)
                        nuevas.remove((cr, cc))
                        nuevas.add((destino_r, destino_c))
                        if not self.es_deadlock(nuevas):
                            # El nuevo estado guarda la posición donde queda el jugador (la antigua posición de la caja)
                            proximos.append((((cr, cc), tuple(sorted(nuevas))), 1))
        return proximos

    def calcular_heuristica(self, estado):
        _, cajas = estado
        total = 0
        
        # Copiamos las metas globales para ir descartándolas una vez asignadas
        metas_disponibles = list(self.metas)
        
        # Ordenamos las cajas que faltan por acomodar para evaluarlas con consistencia
        cajas_fuera = [c for c in cajas if c not in self.metas]
        
        for caja in cajas_fuera:
            if metas_disponibles:
                # Buscamos la meta más cercana exclusivamente entre las que siguen libres
                dist_min = min(abs(m[0] - caja[0]) + abs(m[1] - caja[1]) for m in metas_disponibles)
                total += dist_min
                
                # Encontramos cuál era esa meta y la removemos para que otra caja no la sume
                for m in metas_disponibles:
                    if (abs(m[0] - caja[0]) + abs(m[1] - caja[1])) == dist_min:
                        metas_disponibles.remove(m)
                        break
        return total

    def es_meta(self, estado):
        return self.metas.issubset(set(estado[1]))

    def resolver_para_web(self, algoritmo_nombre):
        grafo_dinamico = {}
        heuristica_dinamica = {self.estado_inicial: self.calcular_heuristica(self.estado_inicial)}
        
        def funcion_grafo(nodo):
            if nodo not in grafo_dinamico:
                grafo_dinamico[nodo] = self.obtener_vecinos(nodo)
                for v, _ in grafo_dinamico[nodo]:
                    if v not in heuristica_dinamica:
                        heuristica_dinamica[v] = self.calcular_heuristica(v)
            return grafo_dinamico[nodo]

        gen = a_estrella(funcion_grafo, heuristica_dinamica, self.estado_inicial, self.es_meta) if algoritmo_nombre == "A_ESTRELLA" else gbfs(funcion_grafo, heuristica_dinamica, self.estado_inicial, self.es_meta)
        for ev, dat in gen:
            if ev == "PASO": yield f"data: {json.dumps({'evento': 'paso', 'jugador': list(dat[0]), 'cajas': [list(c) for c in dat[1]], 'metas': [list(m) for m in self.metas], 'paredes': [list(p) for p in self.paredes]})}\n\n"
            elif ev == "SOLUCION": yield f"data: {json.dumps({'evento': 'solucion', 'pasos': [{'jugador': list(j), 'cajas': [list(c) for c in cb]} for j, cb in dat]})}\n\n"
            elif ev == "FIN": yield f"data: {json.dumps({'evento': 'error'})}\n\n"