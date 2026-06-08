import random
import math

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
    T_inicial=2.0,
    T_min=0.01,
    alfa=0.5,
    iteraciones_por_paso=100,
):
    """
    Recocido Simulado para el problema de las N-reinas.
    Permite movimientos "cuesta abajo" con una probabilidad que decrece
    conforme la temperatura baja.
    Parámetros
    ----------
    reinas_iniciales      : estado inicial (lista de 8 enteros 0-7)
    funcion_puntaje       : función que evalúa un estado (mayor = mejor)
    tipo_enfriamiento     : "exponencial" | "lineal" | "logaritmico"
    T_inicial             : temperatura de inicio
    T_min                 : temperatura mínima para detener
    alfa                  : factor de enfriamiento
                            · exponencial: T_{k+1} = alfa * T_k          (0 < alfa < 1)
                            · lineal     : T_{k+1} = T_k - alfa           (alfa > 0)
                            · logaritmico: T_k = T_0 / log(1 + k)
    iteraciones_por_paso  : intentos de movimiento por nivel de temperatura

    Retorna
    -------
    historial_pasos : lista de estados visitados (incluye estado inicial)
    """
    actual = list(reinas_iniciales)
    puntaje_actual = funcion_puntaje(actual)
    historial_pasos = [list(actual)]
    T = T_inicial
    paso = 1

    while T > T_min and puntaje_actual < 8:
        for _ in range(iteraciones_por_paso):
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
        elif tipo_enfriamiento == "lineal":
            T = max(T - alfa, T_min)
        elif tipo_enfriamiento == "logaritmico":
            T = T_inicial / math.log(1 + paso)
        else:
            raise ValueError(
                f"tipo_enfriamiento '{tipo_enfriamiento}' no reconocido. "
                "Usa 'exponencial', 'lineal' o 'logaritmico'."
            )
        paso += 1
    return historial_pasos
