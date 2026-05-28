from juegos.frozen_lake import FrozenLake
from juegos.ocho_reinas import OchoReinas
from juegos.sokoban import Sokoban
from juegos.tic_tac_toe import TicTacToe

def menu_():
    print("1. Frozen Lake")
    print("2. Ocho Reinas")
    print("3. Sokoban")
    print("4. Tic Tac Toe")
    print("5. Salir")

    opcion = input("Seleccione un juego:")

    if opcion == '1':
        juego = FrozenLake()
        juego.jugar()
    elif opcion == '2':
        juego = OchoReinas()
        juego.jugar()
    elif opcion == '3':
        juego = Sokoban()
        juego.jugar()
    elif opcion == '4':
        juego = TicTacToe()
        juego.jugar()
    else:
        print("Opción no válida. Intente de nuevo.")
        menu_()
