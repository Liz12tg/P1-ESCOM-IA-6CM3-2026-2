#se usa busqueda adversaria
# para este juego el mejor algoritmo es el de alpha-beta
#porque tiene la misma calidad que minmax pero con menor costo

#aqui no es la ia contra el problema, sino que es contra otro jugador

def evaluar(tablero): #para saber quien ganó 
    lineas = [ #son las combinaciones con las que se pueden ganar
        [0,1,2],[3,4,5],[6,7,8],
        [0,3,6],[1,4,7],[2,5,8],
        [0,4,8],[2,4,6]
    ]
    for a,b,c in lineas: #revisamos cada linea
        if tablero[a] == tablero[b] == tablero[c] and tablero[a] != "": #verifica ganador
            if tablero[a] == "X": 
                return 1
            elif tablero[a] == "O":
                return -1
    return 0 #si nadie gana

def movimientos(tablero): #movimientos legales 
    return [i for i, v in enumerate(tablero) if v == ""] #devuelve casillas vacias o disponibles 

def terminal(tablero): #checa si ya acabó la partida
    return evaluar(tablero) != 0 or "" not in tablero #si hay ganaodr o si no hay espacios, termina el juego

