from juegos.tic_tac_toe import terminal, evaluar, movimientos

#es min max pero elimina las ramas que no sirven
#donde alpha es el mejor valor para max
#y beta el mejor valor para min
# y si β≤α entonces hay poda 
#tiene la misma respuesta que minmax pero tiene menos nodos


#alpha-beta no cambia el resultado solo evita calculos innecesarios 
#alpha representa la mejor opcion encontrada para max
#beta respresenta la mejor opcion encontrada para min

def alpha_beta(tablero, alpha, beta, es_max):
    if terminal(tablero):
        return evaluar(tablero)
    if es_max:
        valor = -999
        for m in movimientos(tablero): 
            tablero[m] = "X"
            valor = max(valor, alpha_beta(tablero, alpha, beta, False))
            tablero[m] = ""
            alpha = max(alpha, valor)
            if beta <= alpha: #si esto se cumple se hace poda
            #no importa que exista adelante, max ya tiene una opcion mejor y la rama se corta
                break
        return valor
    else:
        valor = 999
        for m in movimientos(tablero):
            tablero[m] = "O"
            valor = min(valor, alpha_beta(tablero, alpha, beta, True))
            tablero[m] = ""
            beta = min(beta, valor)
            if beta <= alpha:
                break
        return valor

def mejor_movimiento_alpha_beta(tablero):
    mejor_valor = -999
    mejor_mov = None
    for m in movimientos(tablero):
        tablero[m] = "X"
        valor = alpha_beta(tablero, -999, 999, False)
        tablero[m] = ""
        if valor > mejor_valor:
            mejor_valor = valor
            mejor_mov = m
    return mejor_mov