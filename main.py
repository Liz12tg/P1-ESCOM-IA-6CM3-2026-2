from flask import Flask, render_template, jsonify, request, Response
from juegos.frozen_lake import FrozenLake
from juegos.ocho_reinas import OchoReinas
from juegos.sokoban import Sokoban
from juegos.tic_tac_toe import evaluar, terminal
from algoritmos.minmax import mejor_movimiento
from algoritmos.PodaAlphaBeta import mejor_movimiento_alpha_beta

app = Flask(__name__, template_folder="interfaz", static_folder="recursos")
algoritmo_ttt= "alphabeta"
tablero_ttt=[""]*9

@app.route("/")
def inicio():
    return render_template("index.html")

@app.route("/bfs")
def bfs_route():
    nivel = int(
        request.args.get("nivel", 1)
    )
    juego = FrozenLake(nivel)
    camino = juego.resolver_bfs()
    return jsonify({
        "camino": camino
    })
    
@app.route("/dfs")
def dfs_route():
    nivel = int(
        request.args.get("nivel", 1)
    )
    juego = FrozenLake(nivel)
    camino = juego.resolver_dfs()
    return jsonify({
        "camino": camino
    })

@app.route("/reinas")
def ejecutar_reinas():
    algoritmo = request.args.get("algoritmo", "estricto")
    enfriamiento = request.args.get("enfriamiento", "exponencial")
    juego = OchoReinas()
    resultado = juego.resolver_juego(variante=algoritmo, enfriamiento=enfriamiento)
    return jsonify(resultado)

@app.route("/sokoban")
def ejecutar_sokoban():
    nivel = int(request.args.get("nivel", 1))
    algoritmo = request.args.get("algoritmo", "A_ESTRELLA")
    juego = Sokoban(nivel=nivel)
    
    # Transmisión directa mediante streaming
    return Response(juego.resolver_para_web(algoritmo), mimetype="text/event-stream")


@app.route("/tic_tac_toe/estado")
def ttt_estado():
    return jsonify({
        "tablero": tablero_ttt,
        "ganador": evaluar(tablero_ttt)
    })

@app.route("/tic_tac_toe/jugar/<int:pos>")
def ttt_jugar(pos):
    global tablero_ttt
    global algoritmo_ttt

    if terminal(tablero_ttt):
        return jsonify({
            "tablero": tablero_ttt,
            "ganador": evaluar(tablero_ttt)
        })

    if tablero_ttt[pos] == "":
        tablero_ttt[pos] = "O"

        if not terminal(tablero_ttt):

            if algoritmo_ttt == "minimax":
                mov = mejor_movimiento(tablero_ttt)
            else:
                mov = mejor_movimiento_alpha_beta(tablero_ttt)

            if mov is not None:
                tablero_ttt[mov] = "X"

    return jsonify({
        "tablero": tablero_ttt,
        "ganador": evaluar(tablero_ttt)
    })

@app.route("/tic_tac_toe/reiniciar")
def ttt_reiniciar():
    global tablero_ttt
    tablero_ttt = [""] * 9
    return jsonify({"ok": True})

@app.route("/tic_tac_toe/set_algoritmo/<alg>")
def set_algoritmo(alg):
    global algoritmo_ttt
    if alg in ["minimax", "alphabeta"]:
        algoritmo_ttt = alg
    return jsonify({"ok": True})



if __name__ == "__main__":
    app.run(debug=True)
    
