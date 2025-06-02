// URL de tu modelo de Teachable Machine (asegúrate que la ruta sea correcta)
const URL_MODELO = "./modelo_rps/"; 

let model, webcam, maxPredictions;
let playerChoice = ""; 
const opcionesJuego = ["Piedra", "Papel", "Tijera"];

// Variables para la puntuación
let playerScore = 0;
let machineScore = 0;
let tiesScore = 0; 

// Elementos del DOM
const webcamContainer = document.getElementById("webcam-container");
const playerChoiceText = document.getElementById("player-choice-text");
const machineChoiceImage = document.getElementById("machine-choice-image");
const machineChoiceText = document.getElementById("machine-choice-text");
const resultText = document.getElementById("result-text");
const playerScoreDisplay = document.getElementById("player-score");
const machineScoreDisplay = document.getElementById("machine-score");
const tiesScoreDisplay = document.getElementById("ties-score"); 
const playButton = document.getElementById("play-button");

const machineImagePaths = {
    "Piedra": "imagenes/piedra_cpu.png",
    "Papel": "imagenes/papel_cpu.png",
    "Tijera": "imagenes/tijera_cpu.png",
    "Placeholder": "imagenes/placeholder_cpu.png"
};

async function init() {
    const modelURL = URL_MODELO + "model.json";
    const metadataURL = URL_MODELO + "metadata.json";
    console.log("LOG 1: Iniciando la función init()...");

    try {
        console.log("LOG 2: Cargando modelo desde:", URL_MODELO);
        model = await tmImage.load(modelURL, metadataURL);
        maxPredictions = model.getTotalClasses();
        console.log("LOG 3: Modelo cargado, total de clases:", maxPredictions);

        const flip = true;
        webcam = new tmImage.Webcam(250, 250, flip); 
        console.log("LOG 4: Objeto Webcam creado.");

        console.log("LOG 5: Solicitando configuración de la webcam (setup)...");
        await webcam.setup({ facingMode: "user" }); 
        console.log("LOG 6: Configuración de la webcam completada.");

        console.log("LOG 7: Iniciando reproducción de la webcam (play)...");
        await webcam.play(); 

        console.log("LOG 8A: Estado del objeto webcam COMPLETO después de play():", webcam);
        if (webcam.webcam && typeof webcam.webcam.play === 'function') {
            console.log("LOG 8B: (Usando webcam.webcam) Estado del video interno - Pausado:", webcam.webcam.paused);
            console.log("LOG 8C: (Usando webcam.webcam) Estado del video interno - ReadyState:", webcam.webcam.readyState);
            // ... (otros logs 8D, 8E, 8F si los quieres mantener) ...
        } else {
            console.log("LOG 8X: webcam.webcam no está definido o no es un elemento de video.");
        }
        console.log("LOG 8: Reproducción de la webcam (supuestamente) iniciada. webcam.playing:", webcam.playing);

        if (webcamContainer) {
            console.log("LOG 9: webcamContainer encontrado. Añadiendo canvas...");
            webcamContainer.innerHTML = ''; 
            webcamContainer.appendChild(webcam.canvas);
            console.log("LOG 10: Canvas de la webcam añadido al contenedor.");
        } else {
            console.error("LOG 11: ¡ERROR CRÍTICO! No se encontró el div #webcam-container.");
            resultText.textContent = "Error: No se encontró el contenedor de la cámara.";
            if(playButton) playButton.disabled = true;
            return; 
        }
        
        resultText.textContent = "¡Muestra tu mano y presiona Jugar!";
        updateScoreboard(); // Llama para inicializar todas las puntuaciones a 0
        window.requestAnimationFrame(loop);

    } catch (e) {
        console.error("LOG 12: Error detallado en init():", e);
        resultText.textContent = "Error al cargar. Revisa la consola.";
        // ... (manejo de errores específico igual que antes) ...
        if(playButton) playButton.disabled = true; 
    }
}

async function loop() {
    if (webcam && typeof webcam.update === 'function' && webcam.canvas) {
        const isVideoPlaying = webcam.webcam && webcam.webcam.paused === false && webcam.webcam.readyState >= 3;
        if (webcam.playing === true || isVideoPlaying) { 
            webcam.update(); 
            await predict();
        }
    }
    window.requestAnimationFrame(loop);
}

async function predict() {
    if (!model || !webcam || !webcam.canvas || typeof model.predict !== 'function') return; 
    const isVideoReallyPlaying = webcam.webcam && webcam.webcam.paused === false && webcam.webcam.readyState >= 3;
    if (!(webcam.playing === true || isVideoReallyPlaying)) return;

    const prediction = await model.predict(webcam.canvas);
    let highestProb = 0;
    let currentChoice = "Nada"; 

    for (let i = 0; i < maxPredictions; i++) {
        if (prediction[i].probability > highestProb) {
            highestProb = prediction[i].probability;
            currentChoice = prediction[i].className;
        }
    }

    if (currentChoice !== "Nada" && opcionesJuego.includes(currentChoice) && highestProb > 0.80) {
        playerChoice = currentChoice;
        if (playerChoiceText) playerChoiceText.textContent = `Muestras: ${playerChoice}`;
    } else if (currentChoice === "Nada" && highestProb > 0.7) {
        playerChoice = ""; 
        if (playerChoiceText) playerChoiceText.textContent = "Muestra tu mano...";
    } else if (playerChoice === "") { 
         if (playerChoiceText) playerChoiceText.textContent = "Muestra tu mano...";
    }
}

function jugarRonda() {
    if (!playerChoice) {
        if (resultText) resultText.textContent = "¡Muestra una seña clara (Piedra, Papel o Tijera) primero!";
        return;
    }

    if (playButton) playButton.disabled = true; 

    const indiceMaquina = Math.floor(Math.random() * opcionesJuego.length);
    const eleccionMaquina = opcionesJuego[indiceMaquina];

    // Estos console.log son útiles para depurar si quieres mantenerlos
    console.log("RONDA ACTUAL -> Jugador:", playerChoice, "| Máquina:", eleccionMaquina);

    if (machineChoiceText) machineChoiceText.textContent = `Máquina eligió: ${eleccionMaquina}`;
    if (machineChoiceImage && machineImagePaths[eleccionMaquina]) {
        machineChoiceImage.src = machineImagePaths[eleccionMaquina];
    } else if (machineChoiceImage) {
        machineChoiceImage.src = machineImagePaths["Placeholder"]; 
    }
    
    let mensajeResultado = "";
    if (playerChoice === eleccionMaquina) {
        mensajeResultado = "¡Es un Empate!";
        tiesScore++; 
    } else if (
        (playerChoice === "Piedra" && eleccionMaquina === "Tijera") ||
        (playerChoice === "Papel" && eleccionMaquina === "Piedra") ||
        (playerChoice === "Tijera" && eleccionMaquina === "Papel")
    ) {
        mensajeResultado = "¡Ganaste!";
        playerScore++;
    } else {
        mensajeResultado = "¡Perdiste! Intenta de nuevo.";
        machineScore++;
    }

    console.log("Resultado de la ronda:", mensajeResultado); // Útil para depurar

    if (resultText) resultText.textContent = mensajeResultado;
    updateScoreboard(); // Actualiza todas las puntuaciones

    setTimeout(() => {
        if (machineChoiceImage) machineChoiceImage.src = machineImagePaths["Placeholder"];
        if (machineChoiceText) machineChoiceText.textContent = "Esperando...";
        if (playerChoiceText) playerChoiceText.textContent = "Muestra tu mano para la siguiente ronda...";
        playerChoice = ""; 
        if (resultText) resultText.textContent = "¡Elige tu próxima jugada!";
        if (playButton) playButton.disabled = false; 
    }, 2500); 
}

// MODIFICAR ESTA FUNCIÓN para incluir los empates
function updateScoreboard() {
    if (playerScoreDisplay) playerScoreDisplay.textContent = playerScore;
    if (machineScoreDisplay) machineScoreDisplay.textContent = machineScore;
    if (tiesScoreDisplay) tiesScoreDisplay.textContent = tiesScore; 
}

init();