from juegos.tic_tac_toe import terminal, evaluar, movimientos

# minimax supone que ambos jugadores juegan perfecto 
#construye un arbol completo
#max es la IA y min es el humano 
#MAX escoge el mayor valor y min el menor
#si existe victoria la encuentra y si existe empate lo garantiza


#asume que ambos jugadores juegan perfecto

def minimax(tablero, es_max): #tablero es el estado actual y es_max quien juega 
    #si es true la IA y si es false el humano
    if terminal(tablero): #si el juego acabó devuelve el resultado
        return evaluar(tablero)
    if es_max: #si es la IA
        mejor = -999 #porque mas quiere el valo rmas grnade
        for m in movimientos(tablero): #recorre  todas las posibles jugadas 
            tablero[m] = "X"
            valor = minimax(tablero, False) #ahora juega el rival 
            tablero[m] = "" #deshace el mov
            mejor = max(mejor, valor) #y escoge el mejor resultado
        return mejor
    else: #nodo min, es decir el humano
        mejor = 999
        for m in movimientos(tablero): #simula
            tablero[m] = "O"
            valor = minimax(tablero, True)
            tablero[m] = ""
            mejor = min(mejor, valor)
        return mejor

def mejor_movimiento(tablero): #para encontra la jugada real
    #se prueba cada movimiento 
    mejor_valor = -999 
    mejor_mov = None
    for m in movimientos(tablero):
        tablero[m] = "X" #simula
        valor = minimax(tablero, False) #evalua 
        tablero[m] = ""
        if valor > mejor_valor: #si es mejor actualiza
            mejor_valor = valor 
            mejor_mov = m
    return mejor_mov

