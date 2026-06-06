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
    else if(juego === "ocho_reinas"){
        contenido.innerHTML = `
            <h2>Problema de las 8 Reinas</h2>
            <div id="tablero-reinas" class="tablero-ajedrez"></div>
            <div class="controles">
                <button class="boton-jugar" onclick="ejecutarReinas()">Resolver Hill Climbing</button>
            </div>
            <h3 id="estado-reinas">Presiona Jugar para iniciar</h3>
        `;
        dibujarTableroVacio();
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


//----------------------------
//---- funciones 8 reinas ----
//----------------------------

function dibujarTableroVacio(){
    const tablero = document.getElementById("tablero-reinas");
    tablero.innerHTML = "";
    
    tablero.style.display = "grid";
    tablero.style.gridTemplateColumns = "repeat(8, 45px)";
    tablero.style.gridTemplateRows = "repeat(8, 45px)";
    tablero.style.width = "360px"; 
    tablero.style.margin = "20px auto";
    tablero.style.border = "3px solid #222";
    tablero.style.boxShadow = "0 4px 15px rgba(0,0,0,0.3)";
    
    for(let fila=0; fila<8; fila++){
        for(let col=0; col<8; col++){
            const celda = document.createElement("div");
            celda.classList.add("celda");
            
            // Estilos base de la celda
            celda.style.width = "45px";
            celda.style.height = "45px";
            celda.style.boxSizing = "border-box";
            celda.style.display = "flex";
            celda.style.alignItems = "center";
            celda.style.justifyContent = "center";
            celda.style.fontSize = "26px";
            celda.style.transition = "all 0.2s ease"; 
            celda.dataset.fila = fila;
            celda.dataset.col = col;
            
            if((fila + col) % 2 === 0) {
                celda.classList.add("celda-blanca");
                celda.style.backgroundColor = "#f0d9b5";
            } else {
                celda.classList.add("celda-negra");
                celda.style.backgroundColor = "#b58863";
            }
            
            tablero.appendChild(celda);
        }
    }
}

function obtenerConflictos(reinas) {
    let conflictos = Array(8).fill(false);
    for (let i = 0; i < 8; i++) {
        for (let j = i + 1; j < 8; j++) {
            if (reinas[i] === reinas[j] || Math.abs(reinas[i] - reinas[j]) === Math.abs(i - j)) {
                conflictos[i] = true;
                conflictos[j] = true;
            }
        }
    }
    return conflictos;
}

function actualizarTableroReinas(reinas) {
    const celdas = document.querySelectorAll("#tablero-reinas .celda");
    const listaConflictos = obtenerConflictos(reinas);
    
    celdas.forEach(c => {
        c.textContent = "";
        c.style.boxShadow = "none";
        const f = parseInt(c.dataset.fila);
        const col = parseInt(c.dataset.col);
        c.style.backgroundColor = (f + col) % 2 === 0 ? "#f0d9b5" : "#b58863";
    });   
    
    for(let col=0; col<8; col++) {
        let fila = reinas[col];
        let indice = fila * 8 + col;
        
        if(celdas[indice]) {
            celdas[indice].textContent = "R";
            
            if (listaConflictos[col]) {
                celdas[indice].style.backgroundColor = "rgba(255, 99, 71, 0.7)";
                celdas[indice].style.boxShadow = "inset 0 0 10px #ff0000";
            } else {
                celdas[indice].style.backgroundColor = "rgba(144, 238, 144, 0.7)";
                celdas[indice].style.boxShadow = "inset 0 0 10px #00aa00";
            }
        }
    }
}

async function ejecutarReinas(){
    const textoEstado = document.getElementById("estado-reinas");
    textoEstado.textContent = "Calculando ruta óptima en el servidor...";
    
    try {
        const respuesta = await fetch("/reinas");
        const datos = await respuesta.json();
        const pasos = datos.pasos;
        
        const celdas = document.querySelectorAll("#tablero-reinas .celda");
        
        actualizarTableroReinas(pasos[0]);
        await new Promise(resolve => setTimeout(resolve, 1000));
        
        for(let i = 1; i < pasos.length; i++){
            textoEstado.textContent = `Buscando mejoras... Evaluando Paso ${i}`;
            
            const estadoAnterior = pasos[i-1];
            const estadoActual = pasos[i];
            
            let colCambiada = -1;
            for(let c=0; c<8; c++) {
                if(estadoAnterior[c] !== estadoActual[c]) {
                    colCambiada = c;
                    break;
                }
            }
            
            if(colCambiada !== -1) {
                const filaOrigen = estadoAnterior[colCambiada];
                const filaDestino = estadoActual[colCambiada];
                
                for(let f = 0; f < 8; f++) {
                    if (f === filaOrigen) continue; 
                    
                    let indiceFantasma = f * 8 + colCambiada;
                    
                    celdas[indiceFantasma].textContent = "R";
                    celdas[indiceFantasma].style.color = "rgba(0, 0, 0, 0.5)";
                    
                    await new Promise(resolve => setTimeout(resolve, 80)); 
                    
                    if (f !== filaDestino) {
                        celdas[indiceFantasma].textContent = "";
                        celdas[indiceFantasma].style.color = "";
                    }
                }
            }
            
            actualizarTableroReinas(estadoActual);
            await new Promise(resolve => setTimeout(resolve, 800));
        }
        
        if(datos.efectivo) {
            textoEstado.innerHTML = "<span style='color: #00aa00; font-weight: bold;'>¡Éxito! Solución global óptima (0 conflictos).</span>";
        } else {
            textoEstado.innerHTML = "<span style='color: #ff3333; font-weight: bold;'>Algoritmo terminado. Atascado en un Óptimo Local (Existen conflictos irreducibles).</span>";
        }
    } catch (error) {
        console.error(error);
        textoEstado.textContent = "Error al conectar con el servidor.";
    }
}
