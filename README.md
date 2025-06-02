# Juego3
Trabajo de Investigación y Aplicación Práctica: Integración de Modelos de Machine Learning en Aplicaciones Web
# Piedra, Papel o Tijera ¡vs La Máquina! (con IA)

Este proyecto es una implementación web del clásico juego "Piedra, Papel o Tijera" donde juegas contra la máquina. La detección de tu jugada (piedra, papel o tijera) se realiza en tiempo real utilizando tu cámara web y un modelo de Machine Learning entrenado con Teachable Machine y ejecutado en el navegador gracias a TensorFlow.js.

Adicionalmente, este repositorio puede incluir un script (parte Bonus) para entrenar un modelo similar de forma local utilizando Python, Keras y TensorFlow, generando un archivo `.h5`.

## 🎬 Demostración (Ejemplo)
El video esta en los archivos del GitHub

## ✨ Características

* **Juego Interactivo:** Juega Piedra, Papel o Tijera contra una IA.
* **Reconocimiento de Gestos en Tiempo Real:** Utiliza tu cámara web para detectar tu elección (Piedra, Papel, Tijera, o Nada).
* **Modelo de Machine Learning en el Navegador:** El modelo de clasificación de imágenes se ejecuta directamente en tu navegador usando TensorFlow.js.
* **Interfaz de Usuario Clara:** Muestra tu cámara, la elección de la máquina, el resultado de la ronda y una tabla de puntuación.
* **Guía Visual:** Imágenes guía para ayudar al usuario a realizar las señas correctamente.
* **Sección Explicativa:** Información sobre el modelo y su entrenamiento integrada en la interfaz.
* **(Bonus)** Script para entrenamiento local de un modelo Keras (`.h5`).

## 🛠️ Tecnologías Utilizadas

**Aplicación Web Principal:**
* **HTML5:** Estructura de la página web.
* **CSS3:** Estilos y diseño visual.
* **JavaScript (ES6+):** Lógica del juego, interacción con el DOM y TensorFlow.js.
* **Teachable Machine (de Google):** Para el entrenamiento inicial del modelo de clasificación de imágenes.
* **TensorFlow.js:** Para cargar y ejecutar el modelo de Teachable Machine en el navegador.

**(Bonus) Entrenamiento Local del Modelo:**
* **Python 3:** Lenguaje de programación para el script de entrenamiento.
* **TensorFlow & Keras:** Frameworks para construir y entrenar el modelo de Machine Learning.
* **Pillow (PIL):** (Si se usa para manipulación de imágenes, aunque `ImageDataGenerator` lo maneja).
* **Matplotlib:** Para visualizar el historial de entrenamiento.
* **NumPy:** Para operaciones numéricas.
* **Google Colab:** (Opcional, como entorno de entrenamiento acelerado por GPU).

## 📂 Estructura del Proyecto (Ejemplo)

.
├── dataset_rps/             # (BONUS) Carpeta con imágenes para entrenamiento Keras
│   ├── piedra/
│   ├── papel/
│   ├── tijera/
│   └── nada/
├── imagenes/                # Imágenes para la interfaz web (guías, elección CPU)
│   ├── piedra_guia.jpg
│   ├── papel_guia.jpg
│   ├── tijera_guia.jpg
│   ├── piedra_cpu.png
│   ├── papel_cpu.png
│   ├── tijera_cpu.png
│   └── placeholder_cpu.png
├── modelo_rps/              # Modelo exportado de Teachable Machine
│   ├── model.json
│   ├── metadata.json
│   └── weights.bin
├── index.html               # Archivo principal de la aplicación web
├── style.css                # Hoja de estilos
├── script.js                # Lógica de JavaScript y TensorFlow.js
├── Entrenar_RPS.py          # (BONUS) Script de Python para entrenar modelo Keras
├── mi_modelo_rps_colab.h5   # (BONUS) Modelo Keras entrenado (ejemplo de nombre)
└── README.md                # Este archivo

## 🚀 Configuración y Uso

### Aplicación Web (Juego Piedra, Papel o Tijera)

1.  **Clonar el Repositorio (Opcional, si se descarga como ZIP, omitir):**
    bash
    git clone https://github.com/TU_USUARIO/NOMBRE_DEL_REPOSITORIO.git
    cd NOMBRE_DEL_REPOSITORIO
    
2.  **Ejecutar un Servidor Local:**
    Debido a las restricciones de seguridad del navegador (CORS) para acceder a la cámara y cargar modelos (`file:///` no funcionará), necesitas servir los archivos a través de un servidor HTTP local.
    * **Usando VS Code y la extensión "Live Server":**
        * Abre la carpeta del proyecto en VS Code.
        * Haz clic derecho en `index.html` y selecciona "Open with Live Server".
    * **Usando Python:**
        * Abre una terminal en la carpeta raíz del proyecto.
        * Ejecuta: `python -m http.server` (para Python 3) o `python3 -m http.server`.
        * Abre tu navegador y ve a `http://localhost:8000/`.
3.  **Permitir Acceso a la Cámara:** Cuando la página cargue, tu navegador te pedirá permiso para acceder a la cámara. Debes permitirlo.
4.  **¡A Jugar!**
    * Revisa las imágenes guía si es necesario.
    * Muestra tu mano haciendo la seña de Piedra, Papel o Tijera frente a la cámara.
    * El texto debajo de tu cámara indicará qué seña está detectando el modelo.
    * Presiona el botón "¡Jugar!" para que la máquina haga su elección y se determine el resultado.
    * La tabla de puntuación se actualizará.

### (Bonus) Entrenamiento del Modelo Keras Localmente

Si deseas entrenar la versión del modelo con Python y Keras:

1.  **Requisitos Previos:**
    * Python 3 instalado.
    * TensorFlow y Matplotlib instalados:
        bash
        pip install tensorflow matplotlib
        
    * Un conjunto de datos de imágenes organizado en la carpeta `dataset_rps/` con subcarpetas para cada clase (`piedra`, `papel`, `tijera`, `nada`). Puedes usar el script `renombrar_imagenes.py` (si lo incluiste) para ayudar a organizar los nombres de archivo.

2.  **Ejecutar el Script de Entrenamiento:**
    * Asegúrate de que la variable `BASE_DATASET_PATH` en el script `Entrenar_RPS.py` (o como lo hayas llamado) apunte a tu carpeta `dataset_rps`.
    * Ejecuta el script desde tu terminal:
        bash
        python Entrenar_RPS.py
        
    * El entrenamiento puede tardar. Al finalizar, se guardará un archivo `.h5` (ej. `mi_modelo_rps_colab.h5`) con el modelo entrenado y se mostrarán gráficas del historial de entrenamiento.
    * **Alternativa con Google Colab:** Puedes subir el script y tu dataset (o montarlo desde Google Drive) a un notebook de Colab para aprovechar la GPU gratuita y evitar problemas de instalación local.
    * https://colab.research.google.com/drive/1PW36FZoieMRNfTyXfiBDAin0Uox7SDuD?usp=sharing

## 🧠 Información del Modelo

### Modelo de Teachable Machine (Usado en la App Web)

* **Entrenamiento:** El modelo fue entrenado usando [Teachable Machine](https://teachablemachine.withgoogle.com/).
* **Tipo:** Modelo de Clasificación de Imágenes.
* **Clases:**
    1.  `Piedra`
    2.  `Papel`
    3.  `Tijera`
    4.  `Nada` (para cuando no se muestra una seña clara o no hay mano)
* **Recolección de Datos:** Se capturaron múltiples imágenes para cada clase usando una cámara web, intentando variar ligeramente los ángulos y la iluminación para mejorar la robustez.
* **Exportación:** El modelo fue exportado en formato TensorFlow.js para su uso en el navegador.

### (Bonus) Modelo Keras

* **Arquitectura:** (Describe brevemente la arquitectura si implementaste el bonus, ej: MobileNetV2 con transfer learning y capas personalizadas encima).
* **Dataset:** (Menciona el dataset local utilizado).
* **Entrenamiento:** (Brevemente cómo se entrenó, ej: número de épocas, optimizador).
* **Resultado:** Un archivo `.h5` que contiene el modelo entrenado.

## 📄 Documentación Adicional

Para una explicación más detallada de la investigación y el proceso de desarrollo, consulta el documento PDF entregado junto con este proyecto.

## ✒️ Autor

* **[Jose Yosimar Vergara Lucana / UkYos]**

  https://colab.research.google.com/drive/1PW36FZoieMRNfTyXfiBDAin0Uox7SDuD?usp=sharing ===>>>>> Enlace al Google Colab
