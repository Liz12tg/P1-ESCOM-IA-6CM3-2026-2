from algoritmos.bfs import bfs

class FrozenLake:

    def __init__(self):
        self.mapa = [
            ['S','F','F','F'],
            ['F','H','F','H'],
            ['F','F','F','H'],
            ['H','F','F','G']
        ]
        self.inicio = (0,0)
        self.meta = (3,3)

    def obtener_vecinos(self, estado):
        fila, col = estado
        movimientos = [
            (-1,0),
            (1,0),
            (0,-1),
            (0,1)
        ]
        vecinos = []
        for df, dc in movimientos:
            nf = fila + df
            nc = col + dc
            if (0<=nf<len(self.mapa) and 0<=nc<len(self.mapa[0])):
                if self.mapa[nf][nc] != 'H':
                    vecinos.append((nf,nc))
        return vecinos

    def resolver_bfs(self):
        return bfs(
            self.inicio,
            self.meta,
            self.obtener_vecinos
        )