
import random
from algoritmos.hill_climbing import hill_climbing_estricto

class OchoReinas:
    def __init__(self):
        self.estado_inicial = [random.randint(0, 7) for _ in range(8)]

    @staticmethod
    def calcular_puntaje(reinas):
        """ Cuenta cuántas reinas están completamente seguras (sin conflictos) """
        conteo_filas = {}
        conteo_diag_principal = {}
        conteo_diag_secundaria = {}
        
        for columna, fila in enumerate(reinas):
            diag_p = fila - columna
            diag_s = fila + columna
            conteo_filas[fila] = conteo_filas.get(fila, 0) + 1
            conteo_diag_principal[diag_p] = conteo_diag_principal.get(diag_p, 0) + 1
            conteo_diag_secundaria[diag_s] = conteo_diag_secundaria.get(diag_s, 0) + 1
            
        reinas_seguras = 0
        for columna, fila in enumerate(reinas):
            if (conteo_filas[fila] == 1 and 
                conteo_diag_principal[fila - columna] == 1 and 
                conteo_diag_secundaria[fila + columna] == 1):
                reinas_seguras += 1
        return reinas_seguras

    def resolver_hill_climbing(self, variante="estricto"):
        """ Ejecuta la variante de Hill Climbing solicitada y retorna el historial de pasos """
        if variante == "estricto":
            historial = hill_climbing_estricto(self.estado_inicial, self.calcular_puntaje)
            return {
                "inicial": self.estado_inicial,
                "pasos": historial,
                "efectivo": self.calcular_puntaje(historial[-1]) == 8
            }
        return {"inicial": self.estado_inicial, "pasos": [self.estado_inicial], "efectivo": False}
