from algoritmos.Aestrella import a_estrella
from algoritmos.GBFS import gbfs

class Sokoban:
    def __init__(self, nivel=1):
        # Tus 3 niveles basados en tus imágenes
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
        self.diccionario_heuristica = {}

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

    def obtener_vecinos(self, estado):
        jugador, cajas = estado
        cajas_set = set(cajas)
        movimientos = {'Arriba': (-1, 0), 'Abajo': (1, 0), 'Izquierda': (0, -1), 'Derecha': (0, 1)}
        proximos_estados = []
        
        for (dr, dc) in movimientos.values():
            nr, nc = jugador[0] + dr, jugador[1] + dc
            if (nr, nc) not in self.paredes and (nr, nc) not in cajas_set:
                proximos_estados.append((((nr, nc), cajas), 1))
            elif (nr, nc) in cajas_set:
                nnr, nnc = nr + dr, nc + dc
                if (nnr, nnc) not in self.paredes and (nnr, nnc) not in cajas_set:
                    nuevas_cajas = list(cajas)
                    nuevas_cajas.remove((nr, nc))
                    nuevas_cajas.append((nnr, nnc))
                    proximos_estados.append((((nr, nc), tuple(sorted(nuevas_cajas))), 1))
        return proximos_estados

    def calcular_heuristica(self, estado):
        if estado not in self.diccionario_heuristica:
            _, cajas = estado
            total_h = 0
            for caja in cajas:
                distancias = [abs(caja[0] - m[0]) + abs(caja[1] - m[1]) for m in self.metas]
                total_h += min(distancias) if distancias else 0
            self.diccionario_heuristica[estado] = total_h
        return self.diccionario_heuristica[estado]

    def es_meta(self, estado):
        _, cajas = estado
        return set(cajas) == self.metas

    def resolver_para_web(self, algoritmo_nombre):
        # 1. Inicializamos los diccionarios de datos puros que esperan tus algoritmos
        grafo_estatico = {}
        heurísticas_estaticas = {}
        
        # Registramos el punto de partida
        heurísticas_estaticas[self.estado_inicial] = self.calcular_heuristica(self.estado_inicial)
        
        # 2. Función auxiliar que poblará los datos bajo demanda simulando el grafo
        def obtener_y_registrar_vecinos(nodo):
            if nodo not in grafo_estatico:
                # Obtenemos los movimientos válidos de Sokoban
                vecinos = self.obtener_vecinos(nodo)
                grafo_estatico[nodo] = vecinos
                
                # Precalculamos la distancia de Manhattan para cada vecino descubierto
                for vecino, _ in vecinos:
                    if vecino not in heurísticas_estaticas:
                        heurísticas_estaticas[vecino] = self.calcular_heuristica(vecino)
            return grafo_estatico[nodo]
            
        # 3. Adaptador de interfaz compatible con la sintaxis funcion() de tus algoritmos
        class WrapperGrafo:
            def __call__(self, nodo):
                return obtener_y_registrar_vecinos(nodo)

        # 4. Invocación limpia a tus archivos externos individuales
        if algoritmo_nombre == "A_ESTRELLA":
            camino_estados = a_estrella(WrapperGrafo(), heurísticas_estaticas, self.estado_inicial, self.es_meta)
        else:
            camino_estados = gbfs(WrapperGrafo(), heurísticas_estaticas, self.estado_inicial, self.es_meta)

        # 5. Si no hay solución, salimos limpiamente evitando colgar a Flask
        if not camino_estados:
            return {"status": "no_solution", "pasos": []}

        # 6. Serialización del camino para la animación en JavaScript
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
            "metas": [list(m) for m in self.metas],
            "paredes": [list(p) for p in self.paredes],
            "pasos": pasos_json
        }
        # Wrapper de heurísticas dinámicas que requiere el algoritmo independiente
        class HeuristicaDinamica:
            def __getitem__(inst, nodo): return self.calcular_heuristica(nodo)

        # Selección limpia de tus archivos .py externos
        if algoritmo_nombre == "A_ESTRELLA":
            camino_estados = a_estrella(self.obtener_vecinos, HeuristicaDinamica(), self.estado_inicial, self.es_meta)
        else:
            camino_estados = gbfs(self.obtener_vecinos, HeuristicaDinamica(), self.estado_inicial, self.es_meta)

        if not camino_estados:
            return {"status": "no_solution", "pasos": []}

        # Formateo a JSON estructurado para tu Interfaz Web
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
            "metas": [list(m) for m in self.metas],
            "paredes": [list(p) for p in self.paredes],
            "pasos": pasos_json
        }