#para correrlo abre una terminal y ejecuta "python main.py"
# abre el navegador pon "http://localhost:5000"

from flask import Flask, render_template, jsonify
from juegos.frozen_lake import FrozenLake

app = Flask(__name__, template_folder="interfaz",static_folder="recursos")

@app.route("/")
def inicio():
    return render_template("index.html")

@app.route("/bfs")
def ejecutar_bfs():
    juego = FrozenLake()
    camino = juego.resolver_bfs()
    camino_json = []
    for fila, col in camino:
        camino_json.append([fila, col])
    return jsonify({
        "camino": camino_json
    })

if __name__ == "__main__":
    app.run(debug=True)