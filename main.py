#para correrlo abre una terminal y ejecuta "python main.py"
# abre el navegador pon "http://localhost:5000"

from flask import Flask, render_template, jsonify, request
from juegos.frozen_lake import FrozenLake
from juegos.ocho_reinas import OchoReinas

app = Flask(__name__, template_folder="interfaz", static_folder="recursos")

@app.route("/")
def inicio():
    return render_template("index.html")

@app.route("/bfs")
def ejecutar_bfs():
    juego = FrozenLake()
    camino = juego.resolver_bfs()
    camino_json = [[fila, col] for fila, col in camino]
    return jsonify({"camino": camino_json})

@app.route("/reinas")
def ejecutar_reinas():
    algoritmo = request.args.get("algoritmo", "estricto")
    enfriamiento = request.args.get("enfriamiento", "exponencial")
    
    juego = OchoReinas()
    resultado = juego.resolver_juego(variante=algoritmo, enfriamiento=enfriamiento)
    
    return jsonify(resultado)

if __name__ == "__main__":
    app.run(debug=True)
