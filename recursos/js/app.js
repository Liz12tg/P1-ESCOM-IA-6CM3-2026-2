const mapa = [
    ["S","F","F","F"],
    ["F","H","F","H"],
    ["F","F","F","H"],
    ["H","F","F","G"]
];

function seleccionarJuego(juego){
    const contenido = document.getElementById("contenido");
    if(juego === "frozen_lake"){
        contenido.innerHTML = `
            <h2>Frozen Lake</h2>
            <div id="tablero"></div>
            <button class="boton-jugar"onclick="ejecutarBFS()"> Jugar</button>
            <h3>Cola BFS</h3>
            <pre id="cola"></pre>
        `;
        dibujarMapa();
    }
}

function dibujarMapa(){
    const tablero = document.getElementById("tablero");
    tablero.innerHTML = "";
    for(let fila=0; fila<mapa.length; fila++){
        for(let col=0; col<mapa[fila].length; col++){
            const celda = document.createElement("div");
            celda.classList.add("celda");
            const valor = mapa[fila][col];
            celda.textContent = valor;
            if(valor==="S")
                celda.classList.add("inicio");
            else if(valor==="G")
                celda.classList.add("meta");
            else if(valor==="H")
                celda.classList.add("agujero");
            else
                celda.classList.add("hielo");
            tablero.appendChild(celda);
        }
    }
}

async function ejecutarBFS(){
    const respuesta = await fetch("/bfs");
    const datos = await respuesta.json();
    const camino = datos.camino;
    const celdas = document.querySelectorAll(".celda");
    for(const paso of camino){
        const fila = paso[0];
        const col = paso[1];
        const indice = fila * 4 + col;
        celdas[indice]
            .classList
            .add("camino");
        await new Promise(
            resolve => setTimeout(resolve,700)
        );
    }
}