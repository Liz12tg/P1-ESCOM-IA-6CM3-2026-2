from juegos.tic_tac_toe import terminal, evaluar, movimientos

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
            if beta <= alpha:
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