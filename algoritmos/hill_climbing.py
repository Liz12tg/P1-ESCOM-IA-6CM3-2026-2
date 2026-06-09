import random
import math

#aqui esta tanto hill climbing
# como recocido simulado
#recocido esta basado en metalurgia
#permite movimientos peores temporalmente y usa propabilidad
#P=eΔE/T
#cuando la temperatura es alta acepta muchos errores
#y si es baja se vuelve mas estricto 
#se usan 3 enfriamentos 
#Exponencial Tk+1​=αTk​ Más usado.
# Lineal Tk+1​=Tk​−α que es mas agresivo
# Logaritimico Tk​=T0/log(1+k)​​ que es muy lento y tiene mayor probabilidad de encontrar optimos 

def hill_climbing_estricto(reinas_iniciales, funcion_puntaje):
    """
    Hill Climbing estricto (steepest ascent).
    En cada paso elige el mejor vecino de todos los posibles.
    Retorna una lista con los estados intermedios visitados.
    """
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

def recocido_simulado(
    reinas_iniciales,
    funcion_puntaje,
    tipo_enfriamiento="exponencial",
    T_inicial=100.0,
    T_min=0.001,
    alfa=0.99,
):
    """
    Recocido Simulado para el problema de las N-reinas.
    """
    actual = list(reinas_iniciales)
    puntaje_actual = funcion_puntaje(actual)
    historial_pasos = [list(actual)]
    T = T_inicial
    paso = 1

    while T > T_min and puntaje_actual < 8:
        columna_elegida = random.randint(0, 7)
        nueva_fila = random.randint(0, 6)
        if nueva_fila >= actual[columna_elegida]:
            nueva_fila += 1
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
            return historial_pasos
            
        if tipo_enfriamiento == "exponencial":
            T = alfa * T
        elif tipo_enfriamiento == "logaritmico":
            T = 2 / math.log(1 + paso)
        else:
            raise ValueError(
                f"tipo_enfriamiento '{tipo_enfriamiento}' no reconocido. "
                "Usa 'exponencial', 'lineal' o 'logaritmico'."
            )
        paso += 1
    return historial_pasos
