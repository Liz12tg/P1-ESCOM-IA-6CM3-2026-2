def hill_climbing_estricto(reinas_iniciales, funcion_puntaje):
    """
    Hill Climbing clásico (Ascenso de colinas).
    Retorna una lista con cada uno de los estados intermedios.
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
