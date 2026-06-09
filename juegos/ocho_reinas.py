import random
from algoritmos.hill_climbing import hill_climbing_estricto, recocido_simulado

#se hace uso de busqueda local
#analiza todos los vecinos y escoge el mejor 
#como ventaja es rapido 
#pero el problema son los maximos locales ya que si ningun vecino mejora
#se queda atrapado si este aun no es solucion

#para este juego el mejor algoritmo es el de recocido simulado con enfriamento exponencial 
#porque escapa de los maximos locales

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

    def resolver_juego(self, variante="estricto", enfriamiento="exponencial"):
        """ Ejecuta el algoritmo solicitado y retorna el historial completo """
        if variante == "estricto":
            historial = hill_climbing_estricto(self.estado_inicial, self.calcular_puntaje)
        elif variante == "recocido":
            historial = recocido_simulado(self.estado_inicial, self.calcular_puntaje, enfriamiento)
        else:
            historial = [self.estado_inicial]
            
        return {
            "inicial": self.estado_inicial,
            "pasos": historial,
            "efectivo": self.calcular_puntaje(historial[-1]) == 8
        }
