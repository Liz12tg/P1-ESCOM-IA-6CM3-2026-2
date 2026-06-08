from algoritmos.minmax import (evaluar, movimientos, terminal)

def alpha_beta(tablero, profundidad, alpha, beta, es_max):
    if terminal(tablero):
        return evaluar(tablero)
    if es_max:
        valor = -999
        for mov in movimientos(tablero):
            tablero[mov] = "X"
            valor = max(
                valor,
                alpha_beta(tablero, profundidad+1, alpha, beta, False)
            )
            tablero[mov] = ""
            alpha = max(alpha, valor)
            if beta <= alpha:
                break
        return valor
    else:
        valor = 999
        for mov in movimientos(tablero):
            tablero[mov] = "O"
            valor = min(
                valor,
                alpha_beta(tablero, profundidad+1, alpha, beta, True)
            )
            tablero[mov] = ""
            beta = min(beta, valor)
            if beta <= alpha:
                break
        return valor
    
def mejor_movimiento_alpha_beta(tablero):
    mejor = -999
    movimiento = None
    for mov in movimientos(tablero):
        tablero[mov] = "X"
        valor = alpha_beta(tablero, 0, -999, 999, False)
        tablero[mov] = ""
        if valor > mejor:
            mejor = valor
            movimiento = mov
    return movimiento