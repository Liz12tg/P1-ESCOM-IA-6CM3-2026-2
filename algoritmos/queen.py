import random

def puntaje(reinas):
    conteo_filas = {}
    conteo_diag_principal = {}
    conteo_diag_secundaria = {}
    
    for columna, fila in enumerate(reinas):
        diag_p = fila - columna
        diag_s = fila + columna
        conteo_filas[fila] = conteo_filas.get(fila, 0) + 1
        conteo_diag_principal[diag_p] = conteo_diag_principal.get(diag_p, 0) + 1
        conteo_diag_secundaria[diag_s] = conteo_diag_secundaria.get(diag_s, 0) + 1
        
    reinas_seguras = 0
    for columna, fila in enumerate(reinas):
        if (conteo_filas[fila] == 1 and 
            conteo_diag_principal[fila - columna] == 1 and 
            conteo_diag_secundaria[fila + columna] == 1):
            reinas_seguras += 1
            
    return reinas_seguras

def imprimir_tablero(reinas):
    for fila in range(8):
        for columna in range(8):
            print(' R ' if reinas[columna] == fila else ' . ', end='')
        print('')
    print(f"Estado: {reinas} | Reinas sin conflicto: {puntaje(reinas)}\n")

def hill_climbing(reinas_iniciales):
    actual = list(reinas_iniciales)
    puntaje_actual = puntaje(actual)
    
    print("=== ESTADO INICIAL ===")
    imprimir_tablero(actual)
    
    paso = 1
    while True:
        mejor_vecino = None
        mejor_puntaje_vecino = puntaje_actual
        
        for i in range(8):
            for nueva_fila in range(8):
                if nueva_fila != actual[i]:
                    vecino = list(actual)
                    vecino[i] = nueva_fila
                    puntaje_vecino = puntaje(vecino)
                    
                    if puntaje_vecino > mejor_puntaje_vecino:
                        mejor_puntaje_vecino = puntaje_vecino
                        mejor_vecino = vecino
                        
        if mejor_vecino is None:
            print("=== OPTIMO LOCAL ALCANZADO ===")
            print("No hay vecinos mejores. Fin del algoritmo.")
            break
            
        actual = mejor_vecino
        puntaje_actual = mejor_puntaje_vecino
        
        print(f"=== PASO {paso} ===")
        imprimir_tablero(actual)
        paso += 1
        
    return actual

reinas_aleatorias = [random.randint(0, 7) for _ in range(8)]
tablero_final = hill_climbing(reinas_aleatorias)
