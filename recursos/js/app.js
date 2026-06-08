const MAPA_INFO = {
    1: { filas: 4, cols: 4 },
    2: { filas: 5, cols: 5 },
    3: { filas: 6, cols: 6 }
};

let evtSource = null;

const SFX = (() => {
    let ctx = null;
    let enabled = true;
    const init = () => {
        if (!ctx) {
            try { ctx = new (window.AudioContext || window.webkitAudioContext)(); }
            catch (e) { enabled = false; }
        }
        if (ctx && ctx.state === 'suspended') ctx.resume();
    };
    const tone = (freq, dur = 0.08, type = 'square', vol = 0.15, slide = 0) => {
        if (!enabled) return;
        init();
        if (!ctx) return;
        const t0 = ctx.currentTime;
        const osc = ctx.createOscillator();
        const gain = ctx.createGain();
        osc.type = type;
        osc.frequency.setValueAtTime(freq, t0);
        if (slide) osc.frequency.exponentialRampToValueAtTime(Math.max(40, freq + slide), t0 + dur);
        gain.gain.setValueAtTime(0.0001, t0);
        gain.gain.exponentialRampToValueAtTime(vol, t0 + 0.005);
        gain.gain.exponentialRampToValueAtTime(0.0001, t0 + dur);
        osc.connect(gain); gain.connect(ctx.destination);
        osc.start(t0); osc.stop(t0 + dur + 0.02);
    };
    const seq = (notes, gap = 0.08) => {
        if (!enabled) return;
        notes.forEach((n, i) => setTimeout(() => tone(n.f, n.d || 0.09, n.t || 'square', n.v || 0.14, n.s || 0), i * gap * 1000));
    };
    return {
        nav:     () => tone(440, 0.05, 'square', 0.10),
        select:  () => seq([{f:523, d:.07}, {f:784, d:.10}]),
        start:   () => seq([{f:523, d:.08}, {f:659, d:.08}, {f:784, d:.10}, {f:1046, d:.14}]),
        step:    () => tone(660, 0.04, 'square', 0.08),
        push:    () => tone(180, 0.10, 'triangle', 0.18, -40),
        win:     () => seq([{f:523, d:.10}, {f:659, d:.10}, {f:784, d:.10}, {f:1046, d:.22, v:.18}]),
        fail:    () => seq([{f:330, d:.12, s:-100}, {f:220, d:.18, s:-120}]),
        click:   () => tone(800, 0.03, 'square', 0.08),
        back:    () => tone(300, 0.08, 'square', 0.10, -100),
        toggle: (on) => { enabled = on; }
    };
})();

document.addEventListener('click', () => SFX.click && (window.__audioReady || (window.__audioReady = SFX.nav())), { once: true });

const SVG = {
    queen: `<svg class="queenSvg" viewBox="0 0 32 32" xmlns="http://www.w3.org/2000/svg">
        <defs>
            <linearGradient id="qg" x1="0" y1="0" x2="0" y2="1">
                <stop offset="0%" stop-color="#fff4c4"/>
                <stop offset="50%" stop-color="#ffc857"/>
                <stop offset="100%" stop-color="#9a6a18"/>
            </linearGradient>
        </defs>
        <path d="M6 12 L9 6 L12 11 L16 4 L20 11 L23 6 L26 12 L24 22 L8 22 Z" fill="url(#qg)" stroke="#3d2410" stroke-width="1.2" stroke-linejoin="round"/>
        <circle cx="9" cy="6" r="1.6" fill="#fff" stroke="#3d2410" stroke-width=".8"/>
        <circle cx="16" cy="4" r="1.8" fill="#ff5d6c" stroke="#3d2410" stroke-width=".8"/>
        <circle cx="23" cy="6" r="1.6" fill="#fff" stroke="#3d2410" stroke-width=".8"/>
        <rect x="6" y="22" width="20" height="3" rx="1" fill="#c89540" stroke="#3d2410" stroke-width="1"/>
        <rect x="5" y="25" width="22" height="3.5" rx="1.5" fill="#ffc857" stroke="#3d2410" stroke-width="1"/>
    </svg>`,
    box: `<svg class="boxSvg" viewBox="0 0 32 32" xmlns="http://www.w3.org/2000/svg">
        <defs>
            <linearGradient id="bg" x1="0" y1="0" x2="0" y2="1">
                <stop offset="0%" stop-color="#ffb070"/>
                <stop offset="50%" stop-color="#e07a2a"/>
                <stop offset="100%" stop-color="#8a3f10"/>
            </linearGradient>
        </defs>
        <rect x="2" y="2" width="28" height="28" rx="3" fill="url(#bg)" stroke="#2a1408" stroke-width="1.8"/>
        <rect x="5" y="5" width="22" height="22" fill="none" stroke="#2a1408" stroke-width="1.3"/>
        <line x1="5" y1="5" x2="27" y2="27" stroke="#2a1408" stroke-width="1.3"/>
        <line x1="27" y1="5" x2="5" y2="27" stroke="#2a1408" stroke-width="1.3"/>
        <rect x="2" y="2" width="28" height="4" fill="rgba(255,255,255,.3)"/>
        <rect x="2" y="26" width="28" height="2" fill="rgba(0,0,0,.25)"/>
    </svg>`,
    worker: `<svg class="workerSvg" viewBox="0 0 32 32" xmlns="http://www.w3.org/2000/svg">
        <circle cx="16" cy="9" r="5" fill="#ffd6a8" stroke="#2a1a08" stroke-width="1.4"/>
        <path d="M9 9 a7 4 0 0 1 14 0 l-1 -2 a6 3 0 0 0 -12 0 z" fill="#ffc857" stroke="#2a1a08" stroke-width="1.2"/>
        <rect x="8" y="14" width="16" height="13" rx="3" fill="#5cf0ff" stroke="#0a3a48" stroke-width="1.5"/>
        <rect x="8" y="14" width="16" height="3" fill="#3ac7d8"/>
        <rect x="11" y="27" width="3" height="4" fill="#2a1a08"/>
        <rect x="18" y="27" width="3" height="4" fill="#2a1a08"/>
        <circle cx="14" cy="9" r=".9" fill="#1a0a00"/>
        <circle cx="18" cy="9" r=".9" fill="#1a0a00"/>
    </svg>`,
    player: `<svg viewBox="0 0 32 32" width="100%" height="100%" xmlns="http://www.w3.org/2000/svg">
        <circle cx="16" cy="16" r="10" fill="#5cf0ff" stroke="#003540" stroke-width="2"/>
        <circle cx="16" cy="16" r="6" fill="#fff" opacity=".45"/>
    </svg>`
};

const GAMES = ['frozen_lake', 'ocho_reinas', 'sokoban', 'tic_tac_toe'];
let activeIndex = 0;

function getSlotWidth() {
    const cab = document.querySelector('.cabinet');
    if (!cab) return 420;
    const styles = getComputedStyle(cab);
    const w = parseFloat(styles.width) || 360;
    const trackStyles = getComputedStyle(document.getElementById('carouselTrack'));
    const gap = parseFloat(trackStyles.columnGap || trackStyles.gap) || 60;
    return w + gap;
}

function renderCarousel() {
    const track = document.getElementById('carouselTrack');
    const slot = getSlotWidth();
    track.style.transform = `translateX(${-activeIndex * slot}px)`;
    const cabinets = track.querySelectorAll('.cabinet');
    cabinets.forEach((c, i) => c.classList.toggle('active', i === activeIndex));
    const dots = document.querySelectorAll('#carouselDots .dot');
    dots.forEach((d, i) => d.classList.toggle('active', i === activeIndex));
}

function setActive(i) {
    const newIdx = (i + GAMES.length) % GAMES.length;
    if (newIdx !== activeIndex) SFX.nav();
    activeIndex = newIdx;
    renderCarousel();
}

function initCarousel() {
    const dotsWrap = document.getElementById('carouselDots');
    GAMES.forEach((_, i) => {
        const d = document.createElement('button');
        d.className = 'dot' + (i === 0 ? ' active' : '');
        d.addEventListener('click', () => setActive(i));
        dotsWrap.appendChild(d);
    });

    document.getElementById('navPrev').addEventListener('click', () => setActive(activeIndex - 1));
    document.getElementById('navNext').addEventListener('click', () => setActive(activeIndex + 1));

    document.addEventListener('keydown', (e) => {
        if (document.getElementById('contenido').children.length) return;
        if (e.key === 'ArrowLeft')  setActive(activeIndex - 1);
        if (e.key === 'ArrowRight') setActive(activeIndex + 1);
        if (e.key === 'Enter' || e.key === ' ') {
            e.preventDefault();
            seleccionarJuego(GAMES[activeIndex]);
        }
    });

    document.querySelectorAll('.pressStartBtn').forEach(btn => {
        btn.addEventListener('click', () => { SFX.start(); seleccionarJuego(btn.dataset.game); });
    });
    document.querySelectorAll('.cabinet').forEach((c, i) => {
        c.addEventListener('click', (e) => {
            if (i !== activeIndex && !e.target.closest('.pressStartBtn')) setActive(i);
        });
    });

    let startX = 0;
    const track = document.getElementById('carouselTrack');
    track.addEventListener('touchstart', (e) => startX = e.touches[0].clientX);
    track.addEventListener('touchend', (e) => {
        const dx = e.changedTouches[0].clientX - startX;
        if (Math.abs(dx) > 50) setActive(activeIndex + (dx < 0 ? 1 : -1));
    });

    window.addEventListener('resize', () => renderCarousel());

    drawPreviews();
    requestAnimationFrame(() => renderCarousel());
}

function drawPreviews() {
    const f = document.getElementById('previewFrozen');
    const q = document.getElementById('previewReinas');
    const s = document.getElementById('previewSokoban');
    const t = document.getElementById('previewTicTacToe');

if (t) {
    t.style.display = 'grid';
    t.style.gridTemplateColumns = 'repeat(3,1fr)';
    for(let i=0;i<9;i++){
        const c = document.createElement('div');
        c.className = 'screenCell';
    }
}

    for (let r = 0; r < 4; r++) for (let c = 0; c < 4; c++) {
        const cell = document.createElement('div');
        cell.className = 'screenCell';
        const ch = mapa[r][c];
        if (ch === 'S')      cell.style.background = 'linear-gradient(135deg,#8dffc4,#2db86e)';
        else if (ch === 'G') cell.style.background = 'linear-gradient(135deg,#ffe57a,#ffa83d)';
        else if (ch === 'H') cell.style.background = 'radial-gradient(circle,#0a1525,#000)';
        else                 cell.style.background = 'linear-gradient(135deg,#d9f0fa,#7cc5dc)';
        cell.style.boxShadow = 'inset 0 1px 0 rgba(255,255,255,.4)';
        cell.style.borderRadius = '3px';
        f.appendChild(cell);
    }

    for (let r = 0; r < 8; r++) for (let c = 0; c < 8; c++) {
        const cell = document.createElement('div');
        cell.className = 'screenCell';
        cell.style.background = (r + c) % 2 === 0 ? '#fff3d4' : '#2a6e8a';
        q.appendChild(cell);
        if ([0,4,7,5,2,6,1,3][c] === r) {
            cell.innerHTML = '<div style="width:65%;height:65%;background:radial-gradient(circle at 35% 30%,#fff4c4,#ffc857 60%,#9a6a18);border-radius:50% 50% 20% 20%;box-shadow:0 0 8px rgba(255,200,87,.8);"></div>';
            cell.style.display = 'flex'; cell.style.alignItems = 'center'; cell.style.justifyContent = 'center';
        }
    }

    const layout = [
        'WWWWW',
        'W.B.W',
        'W.@.W',
        'WWWWW'
    ];
    for (let r = 0; r < 4; r++) for (let c = 0; c < 5; c++) {
        const cell = document.createElement('div');
        cell.className = 'screenCell';
        const ch = layout[r][c];
        const floor = 'linear-gradient(135deg,#f0d9b8,#d8b88a)';
        if (ch === 'W')      cell.style.background = 'linear-gradient(135deg,#4a3a5a,#2a2038)';
        else if (ch === 'B') { cell.style.background = floor; cell.innerHTML = '<div style="width:80%;height:80%;background:linear-gradient(135deg,#ffb070,#8a3f10);border:1.5px solid #2a1408;border-radius:3px;box-shadow:0 0 6px rgba(255,160,92,.6);"></div>'; cell.style.display='flex';cell.style.alignItems='center';cell.style.justifyContent='center';}
        else if (ch === '@') { cell.style.background = floor; cell.innerHTML = '<div style="width:75%;height:75%;background:radial-gradient(circle at 35% 30%,#fff,#5cf0ff 60%,#0a3a48);border-radius:50%;box-shadow:0 0 8px rgba(92,240,255,.7);"></div>'; cell.style.display='flex';cell.style.alignItems='center';cell.style.justifyContent='center';}
        else                 cell.style.background = floor;
        cell.style.borderRadius = '3px';
        s.appendChild(cell);
    }
}

document.addEventListener('DOMContentLoaded', initCarousel);

function seleccionarJuego(juego) {
    const contenido = document.getElementById("contenido");
    const seleccion = document.getElementById("seleccionView");
    if (!contenido) return;
    if (evtSource) { evtSource.close(); evtSource = null; }
    seleccion.style.display = 'none';
    const themeMap = { frozen_lake: 'ice', ocho_reinas: 'chess', sokoban: 'warehouse', tic_tac_toe: 'tic' };
    const titleMap = { frozen_lake: 'FROZEN LAKE', ocho_reinas: '8 QUEENS', sokoban: 'SOKOBAN', tic_tac_toe: 'TIC TAC TOE' };
    const theme = themeMap[juego];
    let bodyHtml = '';
    if (juego === 'frozen_lake') {
        bodyHtml = `
            <div class="gameScreenWrap">
                <div class="gameScreen"><div id="tableroFrozen" class="boardFrozen"></div></div>
            </div>
            <aside class="gamePanel">
                <div>
                    <div class="panelTitle">Strategy</div>
                    <div class="controlsRow">
                        <label>Nivel</label>
                        <select id="selectFrozenNivel" class="selectInput">
                            <option value="1">Nivel 1</option>
                            <option value="2">Nivel 2</option>
                            <option value="3">Nivel 3</option>
                        </select>
                        <label>Algoritmo</label>
                        <select id="selectFrozenAlgo" class="selectInput">
                            <option value="bfs">BFS · Breadth First</option>
                            <option value="dfs">DFS · Depth First</option>
                        </select>
                        <button class="btnAction" onclick="ejecutarFrozenSimulacion()">▶ EJECUTAR</button>
                    </div>
                </div>
                <div>
                    <div class="panelTitle">Metrics</div>
                    <div class="metricsGrid">
                        <div class="metricCard"><span class="label">Algo</span><span id="frozenLblTipo" class="value">--</span></div>
                        <div class="metricCard"><span class="label">Pasos</span><span id="pasosContador" class="value">0</span></div>
                    </div>
                </div>
                <div class="terminalWrap">
                    <div class="panelTitle">Console</div>
                    <div id="colaLogs" class="terminalConsole">&gt; STANDBY...</div>
                </div>
            </aside>`;
    } else if (juego === 'ocho_reinas') {
        bodyHtml = `
            <div class="gameScreenWrap">
                <div class="gameScreen"><div id="tableroReinas" class="boardChess"></div></div>
            </div>
            <aside class="gamePanel">
                <div>
                    <div class="panelTitle">Config</div>
                    <div class="controlsRow">
                        <label>Algoritmo</label>
                        <select id="selectAlgoritmo" class="selectInput" onchange="alternarEnfriamiento()">
                            <option value="estricto">Hill Climbing</option>
                            <option value="recocido">Simulated Annealing</option>
                        </select>
                        <div id="wrapperEnfriamiento" style="display:none; flex-direction:column; gap:6px;">
                            <label>Enfriamiento</label>
                            <select id="selectEnfriamiento" class="selectInput">
                                <option value="logaritmico">Logarítmico</option>
                                <option value="exponencial">Exponencial</option>
                            </select>
                        </div>
                        <button class="btnAction" onclick="ejecutarReinasSimulacion()">▶ RESOLVER</button>
                    </div>
                </div>
                <div>
                    <div class="panelTitle">Conflict Analysis</div>
                    <div class="metricsGrid">
                        <div class="metricCard"><span class="label">Iter</span><span id="reinasIteracion" class="value">0</span></div>
                        <div class="metricCard"><span class="label">h(n)</span><span id="reinasCosto" class="value">0</span></div>
                    </div>
                </div>
                <div class="terminalWrap">
                    <div class="panelTitle">Console</div>
                    <div id="reinasLogs" class="terminalConsole">&gt; READY</div>
                </div>
            </aside>`;
    } else if (juego === 'sokoban') {
        bodyHtml = `
            <div class="gameScreenWrap">
                <div class="gameScreen"><div id="tableroSokoban" class="boardSokoban"></div></div>
            </div>
            <aside class="gamePanel">
                <div>
                    <div class="panelTitle">Heuristics</div>
                    <div class="controlsRow">
                        <label>Nivel</label>
                        <select id="sokobanNivel" class="selectInput">
                            <option value="1">Nivel 1</option>
                            <option value="2">Nivel 2</option>
                            <option value="3">Nivel 3</option>
                            
                        </select>
                        <label>Algoritmo</label>
                        <select id="sokobanAlgoritmo" class="selectInput">
                            <option value="A_ESTRELLA">A* — f=g+h</option>
                            <option value="GBFS">GBFS — f=h</option>
                        </select>
                        <button class="btnAction" onclick="ejecutarSokobanSimulacion()">▶ CALCULAR</button>
                    </div>
                </div>
                <div>
                    <div class="panelTitle">Search Tree</div>
                    <div class="metricsGrid">
                        <div class="metricCard"><span class="label">Nodos</span><span id="sokobanNodos" class="value">0</span></div>
                        <div class="metricCard"><span class="label">f(n)</span><span id="sokobanMetricasCompleta" class="value">--</span></div>
                    </div>
                </div>
                <div class="terminalWrap">
                    <div class="panelTitle">Console</div>
                    <div id="sokobanLogs" class="terminalConsole">&gt; SSE waiting...</div>
                </div>
            </aside>`;
    } else if (juego === 'tic_tac_toe') {
        bodyHtml = `
            <div class="gameScreenWrap">
                <div class="gameScreen">
                    <div id="tableroTicTacToe" class="boardTic"></div>
                    <div id="ticResultado" class="ticResultado oculto">
                        <div class="ticResultadoBox">
                            <h2 id="ticResultadoTitulo"></h2>
                            <button class="btnAction"
                                    onclick="reiniciarTicTacToe()">
                                JUGAR DE NUEVO
                            </button>
                        </div>
                    </div>
                </div>
            </div>
            <aside class="gamePanel">
                <div>
                    <div class="panelTitle">AI MODE</div>
                    <label>Algoritmo</label>
                    <select id="ticAlgoritmo" class="selectInput">
                        <option value="minimax">Minimax</option>
                        <option value="alphabeta" selected>Alpha-Beta</option>
                    </select>
                    <button class="btnAction"
                            onclick="reiniciarTicTacToe()">
                        REINICIAR
                    </button>
                </div>
            </aside>
        `;
    }

    contenido.innerHTML = `
        <div class="gameCabinet" data-theme="${theme}">
            <div class="gameTopBar">
                <button class="backBtn" onclick="volverASeleccion()">◄ BACK</button>
                <div class="gameTitle">${titleMap[juego]}</div>
                <div style="font-family:var(--f-mono); font-size:10px; color:var(--text-dim); letter-spacing:.2em;">RUNNING</div>
            </div>
            <div class="gameBody">${bodyHtml}</div>
        </div>`;

    if (juego === 'frozen_lake') dibujarMapaFrozen();
    if (juego === 'ocho_reinas') dibujarTableroReinasVacio();
    if (juego === 'sokoban')     inicializarContenedorSokobanVacio();
    if (juego === 'tic_tac_toe') cargarTicTacToe();
}

function volverASeleccion() {
    SFX.back();
    if (evtSource) { evtSource.close(); evtSource = null; }
    document.getElementById('contenido').innerHTML = '';
    document.getElementById('seleccionView').style.display = 'block';
    requestAnimationFrame(() => renderCarousel());
}

// FROZEN LAKE
function dibujarMapaFrozen(nivel = 1) {
    const cont = document.getElementById('tableroFrozen');
    cont.innerHTML = '';
    
    const mapa = {
        1: [
            ["S","F","F","F"],
            ["F","H","F","H"],
            ["F","F","F","H"],
            ["H","F","F","G"]
        ],
        2: [
            ["S","F","F","F","F"],
            ["H","H","F","H","F"],
            ["F","F","F","F","F"],
            ["F","H","H","H","F"],
            ["F","F","F","F","G"]
        ],
        3: [
            ["S","F","F","F","F","F"],
            ["H","H","F","H","F","H"],
            ["F","F","F","F","F","F"],
            ["F","H","H","H","F","F"],
            ["F","F","F","H","F","F"],
            ["H","F","F","F","F","G"]
        ]
    }[nivel];
    cont.style.display = "grid";
    cont.style.gridTemplateColumns = `repeat(${mapa[0].length}, 60px)`;
    cont.style.gridAutoRows = "60px";

    for (let f = 0; f < mapa.length; f++) {
        for (let c = 0; c < mapa[0].length; c++) {
            const cell = document.createElement('div');
            cell.classList.add('cellFrozen');

            const ch = mapa[f][c];
            if (ch === 'S') cell.classList.add('cellStart');
            else if (ch === 'G') cell.classList.add('cellGoal');
            else if (ch === 'H') cell.classList.add('cellHole');
            else cell.classList.add('cellIce');

            cont.appendChild(cell);
        }
    }
}

async function ejecutarFrozenSimulacion() {
    const metodo = document.getElementById('selectFrozenAlgo').value;
    const nivel = document.getElementById('selectFrozenNivel').value;
    const cols = MAPA_INFO[nivel].cols;
    const log = document.getElementById('colaLogs');
    const lbl = document.getElementById('frozenLblTipo');
    dibujarMapaFrozen(nivel);
    lbl.textContent = metodo.toUpperCase();
    log.innerHTML = `&gt; INIT ${metodo.toUpperCase()}<br>&gt; Scanning graph...<br>`;
    SFX.select();

    try {
        const res = await fetch(`/${metodo}?nivel=${nivel}`);
        const datos = await res.json();
        const camino = datos.camino || [];
        const cells = document.querySelectorAll('#tableroFrozen .cellFrozen');
        const cnt = document.getElementById('pasosContador');
        let n = 0;
        for (const paso of camino) {
            n++;
            cnt.textContent = n;
            const idx = paso[0] * cols + paso[1];
            if (cells[idx]) cells[idx].classList.add('cellPath');
            log.innerHTML += `&gt; Node [${paso[0]},${paso[1]}]<br>`;
            log.scrollTop = log.scrollHeight;
            SFX.step();
            await new Promise(r => setTimeout(r, 200));
        }
        log.innerHTML += '<br>&gt; <span style="color:var(--neon-green);">[DONE] Path resolved.</span>';
        SFX.win();
    } catch (e) {
        log.innerHTML = '&gt; <span style="color:var(--neon-red);">[ERR] Backend unreachable.</span>';
        SFX.fail();
    }
}

// 8 REINAS
function alternarEnfriamiento() {
    const el = document.getElementById('selectAlgoritmo').value;
    const w = document.getElementById('wrapperEnfriamiento');
    if (w) w.style.display = el === 'recocido' ? 'flex' : 'none';
}

function dibujarTableroReinasVacio() {
    const cont = document.getElementById('tableroReinas');
    if (!cont) return;
    cont.innerHTML = '';
    for (let f = 0; f < 8; f++) for (let c = 0; c < 8; c++) {
        const cell = document.createElement('div');
        cell.classList.add('cellChess', (f + c) % 2 === 0 ? 'cellChessLight' : 'cellChessDark');
        cell.dataset.fila = f; cell.dataset.columna = c;
        cont.appendChild(cell);
    }
}

function actualizarPosicionesReinas(vec) {
    const cells = document.querySelectorAll('#tableroReinas .cellChess');
    cells.forEach(c => {
        c.innerHTML = '';
        const f = +c.dataset.fila, col = +c.dataset.columna;
        c.className = 'cellChess ' + ((f + col) % 2 === 0 ? 'cellChessLight' : 'cellChessDark');
    });
    const conflict = Array(8).fill(false);
    let coste = 0;
    for (let i = 0; i < 8; i++) for (let j = i + 1; j < 8; j++) {
        if (vec[i] === vec[j] || Math.abs(vec[i] - vec[j]) === Math.abs(i - j)) {
            conflict[i] = conflict[j] = true; coste++;
        }
    }
    document.getElementById('reinasCosto').textContent = coste;
    for (let c = 0; c < 8; c++) {
        const f = vec[c], idx = f * 8 + c;
        if (cells[idx]) {
            cells[idx].innerHTML = SVG.queen;
            cells[idx].classList.add(conflict[c] ? 'cellQueenConflict' : 'cellQueenSafe');
        }
    }
}

async function ejecutarReinasSimulacion() {
    const algo = document.getElementById('selectAlgoritmo').value;
    const enf = document.getElementById('selectEnfriamiento')?.value || 'logaritmico';
    const log = document.getElementById('reinasLogs');
    const txt = document.getElementById('reinasIteracion');
    log.innerHTML = '&gt; INIT local search...<br>';
    SFX.select();
    try {
        const res = await fetch(`/reinas?algoritmo=${algo}&enfriamiento=${enf}`);
        const datos = await res.json();
        const pasos = datos.pasos;
        for (let i = 0; i < pasos.length; i++) {
            txt.textContent = i;
            actualizarPosicionesReinas(pasos[i]);
            log.innerHTML += `&gt; iter[${i}] state=[${pasos[i].join(',')}]<br>`;
            log.scrollTop = log.scrollHeight;
            if (i % 4 === 0) SFX.step();
            await new Promise(r => setTimeout(r, pasos.length > 40 ? 50 : 200));
        }
        if (datos.efectivo) { log.innerHTML += '<br>&gt; <span style="color:var(--neon-green);">[SUCCESS] Optimal solution.</span>'; SFX.win(); }
        else                { log.innerHTML += '<br>&gt; <span style="color:var(--neon-red);">[STOP] Local optimum.</span>';     SFX.fail(); }
    } catch (e) {
        log.innerHTML = '&gt; <span style="color:var(--neon-red);">[ERR] Backend failure.</span>';
        SFX.fail();
    }
}

// SOKOBAN
function inicializarContenedorSokobanVacio() {
    const cont = document.getElementById('tableroSokoban');
    if (cont) cont.innerHTML = '<div style="color:var(--text-dim); font-family:var(--f-screen); font-size:18px; padding:30px;">&gt; AWAITING DATA STREAM...</div>';
}

function redibujarSokoban(paredes, metas, jugador, cajas) {
    const cont = document.getElementById('tableroSokoban');
    if (!cont) return;
    cont.innerHTML = '';
    const sP = new Set(paredes.map(p => `${p[0]},${p[1]}`));
    const sM = new Set(metas.map(m => `${m[0]},${m[1]}`));
    const sC = new Set(cajas.map(c => `${c[0]},${c[1]}`));
    const jKey = `${jugador[0]},${jugador[1]}`;
    const maxC = Math.max(...paredes.map(p => p[1])) + 1;
    const maxF = Math.max(...paredes.map(p => p[0])) + 1;
    cont.style.gridTemplateColumns = `repeat(${maxC}, 44px)`;
    for (let r = 0; r < maxF; r++) for (let c = 0; c < maxC; c++) {
        const k = `${r},${c}`;
        const cell = document.createElement('div');
        cell.classList.add('cellSk');
        if (sP.has(k)) cell.classList.add('cellSkWall');
        else if (k === jKey) {
            cell.classList.add('cellSkFloor');
            cell.innerHTML = SVG.worker;
        } else if (sC.has(k)) {
            const onTarget = sM.has(k);
            cell.classList.add('cellSkFloor');
            if (onTarget) cell.classList.add('cellSkBoxOnTarget');
            cell.innerHTML = SVG.box;
        } else if (sM.has(k)) {
            cell.classList.add('cellSkTarget');
        } else {
            cell.classList.add('cellSkFloor');
        }
        cont.appendChild(cell);
    }
}

function ejecutarSokobanSimulacion() {
    const nivel = document.getElementById('sokobanNivel').value;
    const algo = document.getElementById('sokobanAlgoritmo').value;
    const log = document.getElementById('sokobanLogs');
    const tN = document.getElementById('sokobanNodos');
    const tM = document.getElementById('sokobanMetricasCompleta');
    if (evtSource) evtSource.close();
    let cnt = 0, cacheP = null, cacheM = null;
    log.innerHTML = '&gt; SSE link establishing...<br>';
    SFX.select();
    evtSource = new EventSource(`/sokoban?nivel=${nivel}&algoritmo=${algo}`);
    evtSource.onmessage = (event) => {
        const d = JSON.parse(event.data);
        if (d.evento === 'paso') {
            cnt++;
            tN.textContent = cnt;
            tM.textContent = algo === 'A_ESTRELLA' ? 'f=g+h' : 'f=h';
            cacheP = d.paredes; cacheM = d.metas;
            if (cnt % 40 === 0 || cnt < 15) {
                window.requestAnimationFrame(() => {
                    log.innerHTML += `&gt; Expanding node #${cnt}<br>`;
                    log.scrollTop = log.scrollHeight;
                    redibujarSokoban(d.paredes, d.metas, d.jugador, d.cajas);
                });
            }
        } else if (d.evento === 'solucion') {
            evtSource.close();
            window.requestAnimationFrame(async () => {
                log.innerHTML += '<br>&gt; <span style="color:var(--neon-green);">[FOUND] Replaying solution...</span><br>';
                for (const p of d.pasos) {
                    redibujarSokoban(cacheP, cacheM, p.jugador, p.cajas);
                    SFX.push();
                    await new Promise(r => setTimeout(r, 120));
                }
                log.innerHTML += '&gt; <span style="color:var(--neon-yellow);">[COMPLETE]</span>';
                SFX.win();
            });
        }
    };
    evtSource.onerror = () => { SFX.fail(); };
}


function dibujarTicTacToe(tablero) {
    const cont = document.getElementById('tableroTicTacToe');
    cont.innerHTML = '';
    tablero.forEach((valor, i) => {
        const celda = document.createElement('div');
        celda.className = 'cellTic';
        celda.innerHTML = valor;
        celda.onclick = () => jugarTicTacToe(i);
        cont.appendChild(celda);
    });
}

async function actualizarAlgoritmoTicTacToe(){
    const alg = document.getElementById("ticAlgoritmo").value;
    await fetch(
        `/tic_tac_toe/set_algoritmo/${alg}`
    );
}

async function jugarTicTacToe(pos) {
    await actualizarAlgoritmoTicTacToe();
    const res = await fetch(`/tic_tac_toe/jugar/${pos}`);
    const data = await res.json();
    dibujarTicTacToe(data.tablero);
    if (data.ganador === 1){
        mostrarResultadoTic("LA IA GANA");
        SFX.fail();
    }
    else if (data.ganador === -1){
        mostrarResultadoTic("GANASTE");
        SFX.win();
    }
    else if (!data.tablero.includes("")){
        mostrarResultadoTic("EMPATE");
    }
}

function actualizarTic(tablero) {
    const cells = document.querySelectorAll("#tableroTicTacToe .cellTic");
    cells.forEach((c, i) => {
        c.textContent = tablero[i];
    });
}

async function reiniciarTicTacToe() {
    await fetch('/tic_tac_toe/reiniciar');
    const modal = document.getElementById("ticResultado");
    if(modal)
        modal.classList.add("oculto");
    cargarTicTacToe();
}

async function cargarTicTacToe() {
    const res = await fetch('/tic_tac_toe/estado');
    const data = await res.json();
    dibujarTicTacToe(data.tablero);
}

function mostrarResultadoTic(texto){
    const modal = document.getElementById("ticResultado");
    const titulo = document.getElementById("ticResultadoTitulo");
    titulo.textContent = texto;
    modal.classList.remove("oculto");
}

