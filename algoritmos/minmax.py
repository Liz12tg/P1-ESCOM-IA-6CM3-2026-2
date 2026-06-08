def evaluar(tablero):
    lineas = [
        [0,1,2],
        [3,4,5],
        [6,7,8],

        [0,3,6],
        [1,4,7],
        [2,5,8],

        [0,4,8],
        [2,4,6]
    ]

    for a,b,c in lineas:
        if tablero[a] == tablero[b] == tablero[c]:
            if tablero[a] == "X":
                return 1
            if tablero[a] == "O":
                return -1
    return 0

def movimientos(tablero):
    return [
        i
        for i,v in enumerate(tablero)
        if v == ""
    ]
    
def terminal(tablero):
    if evaluar(tablero) != 0:
        return True
    return "" not in tablero

def minimax(tablero, es_max):
    if terminal(tablero):
        return evaluar(tablero)
    if es_max:
        mejor = -999
        for mov in movimientos(tablero):
            tablero[mov] = "X"
            valor = minimax(tablero, False)
            tablero[mov] = ""
            mejor = max(mejor, valor)
        return mejor
    else:
        mejor = 999
        for mov in movimientos(tablero):
            tablero[mov] = "O"
            valor = minimax(tablero, True)
            tablero[mov] = ""
            mejor = min(mejor, valor)
        return mejor
    
def mejor_movimiento(tablero):
    mejor_valor = -999
    mejor_mov = None
    for mov in movimientos(tablero):
        tablero[mov] = "X"
        valor = minimax(tablero, False)
        tablero[mov] = ""
        if valor > mejor_valor:
            mejor_valor = valor
            mejor_mov = mov
    return mejor_mov