import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.layers import Dense, GlobalAveragePooling2D, Dropout
from tensorflow.keras.models import Model
import matplotlib.pyplot as plt
import os
import numpy as np # Para manejar las semillas si es necesario

# --- Sección de Configuración ---
BASE_DATASET_PATH = "./dataset_rps"  # MODIFICA ESTA RUTA si tu dataset está en otro lugar
IMG_WIDTH, IMG_HEIGHT = 224, 224     # Tamaño de entrada para MobileNetV2
BATCH_SIZE = 32                      # Número de imágenes a procesar en cada lote
EPOCHS = 20                          # Número de veces que el modelo verá todo el dataset
                                     # Puedes empezar con 15-25 y ajustar según los resultados

# Semilla para reproducibilidad (opcional, pero bueno para consistencia)
# tf.random.set_seed(42)
# np.random.seed(42)

# --- 1. Preparar Generadores de Datos ---
print("Preparando generadores de datos...")
train_datagen = ImageDataGenerator(
    rescale=1./255,
    rotation_range=30,
    width_shift_range=0.2,
    height_shift_range=0.2,
    shear_range=0.2,
    zoom_range=0.2,
    horizontal_flip=True,
    fill_mode='nearest',
    validation_split=0.2
)

train_generator = train_datagen.flow_from_directory(
    BASE_DATASET_PATH,
    target_size=(IMG_WIDTH, IMG_HEIGHT),
    batch_size=BATCH_SIZE,
    class_mode='categorical',
    subset='training',
    shuffle=True
)

validation_datagen = ImageDataGenerator(
    rescale=1./255,
    validation_split=0.2
)

validation_generator = validation_datagen.flow_from_directory(
    BASE_DATASET_PATH,
    target_size=(IMG_WIDTH, IMG_HEIGHT),
    batch_size=BATCH_SIZE,
    class_mode='categorical',
    subset='validation',
    shuffle=False
)

num_classes = train_generator.num_classes
class_names_found = list(train_generator.class_indices.keys())
print(f"Se encontraron {num_classes} clases: {class_names_found}")

if num_classes == 0:
    print(f"Error: No se encontraron imágenes o clases en la ruta '{BASE_DATASET_PATH}'. Verifica la ruta y la estructura de carpetas.")
    exit()
elif num_classes != 4: 
    print(f"Advertencia: Se esperaban 4 clases (Piedra, Papel, Tijera, Nada), pero se encontraron {num_classes}. Revisa la estructura de tu carpeta de dataset.")

# --- 2. Construir el Modelo usando Transfer Learning (MobileNetV2) ---
print("Construyendo el modelo...")
base_model = MobileNetV2(weights='imagenet', include_top=False,
                         input_shape=(IMG_WIDTH, IMG_HEIGHT, 3))
base_model.trainable = False

x = base_model.output
x = GlobalAveragePooling2D()(x)
x = Dense(128, activation='relu')(x)
x = Dropout(0.5)(x)
predictions_layer = Dense(num_classes, activation='softmax')(x)

model = Model(inputs=base_model.input, outputs=predictions_layer)

# --- 3. Compilar el Modelo ---
print("Compilando el modelo...")
model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=0.001),
              loss='categorical_crossentropy',
              metrics=['accuracy'])
model.summary()

# --- 4. Entrenar el Modelo ---
print("\nIniciando entrenamiento del modelo...")
if train_generator.samples == 0 or validation_generator.samples == 0:
    print("Error: Uno de los generadores de datos (entrenamiento o validación) está vacío.")
    print(f"Muestras de entrenamiento: {train_generator.samples}, Muestras de validación: {validation_generator.samples}")
    print("Por favor, verifica que tengas suficientes imágenes en tus carpetas de clase y que el BASE_DATASET_PATH sea correcto.")
    exit()

# Cálculo de steps_per_epoch y validation_steps
# Asegura que no sean cero si hay pocas muestras en relación al batch_size
steps_per_epoch = train_generator.samples // BATCH_SIZE
if steps_per_epoch == 0:
    steps_per_epoch = 1 # Ejecutar al menos 1 step si hay datos

validation_steps = validation_generator.samples // BATCH_SIZE
if validation_steps == 0 and validation_generator.samples > 0 : # Si hay datos de validación pero menos que un batch
    validation_steps = 1


history = model.fit(
    train_generator,
    epochs=EPOCHS,
    validation_data=validation_generator,
    steps_per_epoch=steps_per_epoch,
    validation_steps=validation_steps 
)
print("Entrenamiento del modelo completado.")

# --- 5. Evaluar el Modelo (Opcional) ---
if validation_generator.samples > 0:
    print("\nEvaluando modelo con datos de validación:")
    loss, accuracy = model.evaluate(validation_generator, steps=validation_steps)
    print(f"Pérdida en validación: {loss:.4f}")
    print(f"Precisión en validación: {accuracy*100:.2f}%")
else:
    print("\nNo hay suficientes datos de validación para evaluar.")


# --- 6. Graficar Historial de Entrenamiento (Opcional) ---
def plot_history(training_history):
    # Comprobar si las métricas están disponibles en el historial
    acc_exists = 'accuracy' in training_history.history
    val_acc_exists = 'val_accuracy' in training_history.history
    loss_exists = 'loss' in training_history.history
    val_loss_exists = 'val_loss' in training_history.history

    epochs_range = range(len(training_history.history[list(training_history.history.keys())[0]])) # Tomar longitud de la primera métrica disponible

    plt.figure(figsize=(12, 5))

    if acc_exists and val_acc_exists:
        plt.subplot(1, 2, 1)
        plt.plot(epochs_range, training_history.history['accuracy'], label='Precisión (Entrenamiento)')
        plt.plot(epochs_range, training_history.history['val_accuracy'], label='Precisión (Validación)')
        plt.legend(loc='lower right')
        plt.title('Precisión de Entrenamiento y Validación')
        plt.xlabel('Épocas')
        plt.ylabel('Precisión')
    elif acc_exists: # Solo mostrar accuracy de entrenamiento si no hay de validación
        plt.subplot(1, 2, 1)
        plt.plot(epochs_range, training_history.history['accuracy'], label='Precisión (Entrenamiento)')
        plt.legend(loc='lower right')
        plt.title('Precisión de Entrenamiento')
        plt.xlabel('Épocas')
        plt.ylabel('Precisión')


    if loss_exists and val_loss_exists:
        plt.subplot(1, 2, 2)
        plt.plot(epochs_range, training_history.history['loss'], label='Pérdida (Entrenamiento)')
        plt.plot(epochs_range, training_history.history['val_loss'], label='Pérdida (Validación)')
        plt.legend(loc='upper right')
        plt.title('Pérdida de Entrenamiento y Validación')
        plt.xlabel('Épocas')
        plt.ylabel('Pérdida')
    elif loss_exists: # Solo mostrar loss de entrenamiento
        plt.subplot(1, 2, 2)
        plt.plot(epochs_range, training_history.history['loss'], label='Pérdida (Entrenamiento)')
        plt.legend(loc='upper right')
        plt.title('Pérdida de Entrenamiento')
        plt.xlabel('Épocas')
        plt.ylabel('Pérdida')
    
    if (acc_exists and val_acc_exists) or (loss_exists and val_loss_exists) or acc_exists or loss_exists:
        plt.tight_layout()
        plt.show()
    else:
        print("No hay suficientes datos en el historial para graficar.")

if hasattr(history, 'history') and history.history:
    plot_history(history)
else:
    print("No se generó historial de entrenamiento para graficar (posiblemente no hubo datos de validación o el entrenamiento fue muy corto).")

# --- 7. Guardar el Modelo Entrenado ---
MODEL_SAVE_PATH = "./mi_modelo_rps.h5"  # Puedes cambiar a .keras si prefieres el nuevo formato
model.save(MODEL_SAVE_PATH)
print(f"\nModelo guardado exitosamente en {os.path.abspath(MODEL_SAVE_PATH)}")
print("Ahora puedes usar este archivo .h5 para predicciones o conversiones futuras.")