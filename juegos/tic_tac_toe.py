def evaluar(tablero):
    lineas = [
        [0,1,2],[3,4,5],[6,7,8],
        [0,3,6],[1,4,7],[2,5,8],
        [0,4,8],[2,4,6]
    ]
    for a,b,c in lineas:
        if tablero[a] == tablero[b] == tablero[c] and tablero[a] != "":
            if tablero[a] == "X":
                return 1
            elif tablero[a] == "O":
                return -1
    return 0

def movimientos(tablero):
    return [i for i, v in enumerate(tablero) if v == ""]

def terminal(tablero):
    return evaluar(tablero) != 0 or "" not in tablero

