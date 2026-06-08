from algoritmos.bfs import bfs
from algoritmos.dfs import dfs

MAPAS = {
    1: [
        ["S","F","F","F"],
        ["F","H","F","H"],
        ["F","F","F","H"],
        ["H","F","F","G"]
    ],
    2: [
        ["S","F","F","F","F"],
        ["H","H","F","H","F"],
        ["F","F","F","F","F"],
        ["F","H","H","H","F"],
        ["F","F","F","F","G"]
    ],
    3: [
        ["S","F","F","F","F","F"],
        ["H","H","F","H","F","H"],
        ["F","F","F","F","F","F"],
        ["F","H","H","H","F","F"],
        ["F","F","F","H","F","F"],
        ["H","F","F","F","F","G"]
    ]
}


class FrozenLake:

    def __init__(self, nivel=1):
        self.mapa = MAPAS[nivel]

        self.inicio = self.buscar("S")
        self.meta = self.buscar("G")

        if self.inicio is None:
            raise ValueError("No se encontró el inicio 'S'")
        if self.meta is None:
            raise ValueError("No se encontró la meta 'G'")

        self.filas = len(self.mapa)
        self.cols = len(self.mapa[0])

    # -------------------------------------------------

    def buscar(self, valor):
        for i in range(len(self.mapa)):
            for j in range(len(self.mapa[i])):
                if self.mapa[i][j] == valor:
                    return (i, j)
        return None

    # -------------------------------------------------

    def obtener_vecinos(self, estado):
        fila, col = estado

        movimientos = [
            (-1, 0),
            (1, 0),
            (0, -1),
            (0, 1)
        ]

        vecinos = []

        for df, dc in movimientos:
            nf = fila + df
            nc = col + dc

            if 0 <= nf < self.filas and 0 <= nc < self.cols:
                if self.mapa[nf][nc] != "H":
                    vecinos.append((nf, nc))

        return vecinos

    # -------------------------------------------------

    def resolver_bfs(self):
        return bfs(
            self.inicio,
            self.meta,
            self.obtener_vecinos
        )

    def resolver_dfs(self):
        return dfs(
            self.inicio,
            self.meta,
            self.obtener_vecinos
        )