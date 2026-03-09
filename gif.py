import os
from PIL import Image
from pathlib import Path

# ======================================
# CONFIGURACION
# ======================================

carpeta = Path(r"C:\Users\dell\explosion-software\versiones-resultados\nivel 1\v5")  # <-- cambia esto

fps = 24

# duración por frame en milisegundos
duracion_frame = int(1000 / fps)

# nombre del gif final
nombre_gif = "animacion.gif"

# ======================================
# CARGAR IMAGENES
# ======================================

imagenes = []

# extensiones válidas
extensiones = (".png", ".jpg", ".jpeg", ".bmp")

# obtener lista ordenada
archivos = sorted([
    f for f in os.listdir(carpeta)
    if f.lower().endswith(extensiones)
])

for archivo in archivos:
    ruta = os.path.join(carpeta, archivo)
    img = Image.open(ruta)
    imagenes.append(img)

# ======================================
# CREAR GIF
# ======================================

if imagenes:

    salida = os.path.join(carpeta, nombre_gif)

    imagenes[0].save(
        salida,
        save_all=True,
        append_images=imagenes[1:],
        duration=duracion_frame,
        loop=0
    )

    print("GIF creado en:", salida)

else:
    print("No se encontraron imágenes.")