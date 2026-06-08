from flask import Flask, render_template, jsonify, request, Response
from juegos.frozen_lake import FrozenLake
from juegos.ocho_reinas import OchoReinas
from juegos.sokoban import Sokoban

app = Flask(__name__, template_folder="interfaz", static_folder="recursos")

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

if __name__ == "__main__":
    app.run(debug=True)