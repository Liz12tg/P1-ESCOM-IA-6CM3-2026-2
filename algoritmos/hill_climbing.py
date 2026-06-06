import random
import math

def hill_climbing_estricto(reinas_iniciales, funcion_puntaje):
    """ Hill Climbing estricto. Retorna una lista con estados intermedios. """
    actual = list(reinas_iniciales)
    puntaje_actual = funcion_puntaje(actual)
    historial_pasos = [list(actual)]
    
    while True:
        mejor_vecino = None
        mejor_puntaje_vecino = puntaje_actual
        
        for i in range(8):
            for nueva_fila in range(8):
                if nueva_fila != actual[i]:
                    vecino = list(actual)
                    vecino[i] = nueva_fila
                    puntaje_vecino = funcion_puntaje(vecino)
                    
                    if puntaje_vecino > mejor_puntaje_vecino:
                        mejor_puntaje_vecino = puntaje_vecino
                        mejor_vecino = vecino
                        
        if mejor_vecino is None:
            break
            
        actual = mejor_vecino
        puntaje_actual = mejor_puntaje_vecino
        historial_pasos.append(list(actual))
        
    return historial_pasos


def recocido_simulado(reinas_iniciales, funcion_puntaje, tipo_enfriamiento="exponencial"):
    """
    Recocido Simulado. Permite movimientos cuesta abajo basados en una temperatura decreciente.
    """
    actual = list(reinas_iniciales)
    puntaje_actual = funcion_puntaje(actual)
    historial_pasos = [list(actual)]
    
    T = 10.0
    T_min = 0.01
    iteraciones_por_paso = 5
    alfa = 0.95
    paso = 1

    while T > T_min and puntaje_actual < 8:
        for _ in range(iteraciones_por_paso):
            columna_elegida = random.randint(0, 7)
            nueva_fila = random.randint(0, 7)
            while nueva_fila == actual[columna_elegida]:
                nueva_fila = random.randint(0, 7)
                
            vecino = list(actual)
            vecino[columna_elegida] = nueva_fila
            puntaje_vecino = funcion_puntaje(vecino)
            
            delta_E = puntaje_vecino - puntaje_actual
            
            if delta_E > 0:
                actual = vecino
                puntaje_actual = puntaje_vecino
                historial_pasos.append(list(actual))
            else:
                probabilidad = math.exp(delta_E / T)
                if random.random() < probabilidad:
                    actual = vecino
                    puntaje_actual = puntaje_vecino
                    historial_pasos.append(list(actual))
                    
            if puntaje_actual == 8:
                break
                
        if tipo_enfriamiento == "exponencial":
            T = T * alfa
        elif tipo_enfriamiento == "lineal":
            T = T - 0.5
        elif tipo_enfriamiento == "inversa":
            T = 10.0 / (1 + 0.5 * paso)
            
        paso += 1

    if historial_pasos[-1] != actual:
        historial_pasos.append(list(actual))
        
    return historial_pasos
