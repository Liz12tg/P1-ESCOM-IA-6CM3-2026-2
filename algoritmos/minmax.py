from juegos.tic_tac_toe import terminal, evaluar, movimientos

def minimax(tablero, es_max):
    if terminal(tablero):
        return evaluar(tablero)
    if es_max:
        mejor = -999
        for m in movimientos(tablero):
            tablero[m] = "X"
            valor = minimax(tablero, False)
            tablero[m] = ""
            mejor = max(mejor, valor)
        return mejor
    else:
        mejor = 999
        for m in movimientos(tablero):
            tablero[m] = "O"
            valor = minimax(tablero, True)
            tablero[m] = ""
            mejor = min(mejor, valor)
        return mejor

def mejor_movimiento(tablero):
    mejor_valor = -999
    mejor_mov = None
    for m in movimientos(tablero):
        tablero[m] = "X"
        valor = minimax(tablero, False)
        tablero[m] = ""
        if valor > mejor_valor:
            mejor_valor = valor
            mejor_mov = m
    return mejor_mov

