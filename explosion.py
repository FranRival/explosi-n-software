# ==========================
# EJECUCION
# C:\Users\dell\explosion_env\Scripts\python.exe C:\Users\dell\explosion-software\explosion.py
# ===============

import os
import math
import numpy as np
from PIL import Image
from noise import pnoise2
from scipy.ndimage import gaussian_filter

# =========================================================
# CONFIGURACIÓN ORIGINAL (NO SE TOCA NADA)
# =========================================================
WIDTH, HEIGHT = 512, 512
FRAMES = 50
DURATION = 1.3
CENTER_X, CENTER_Y = WIDTH // 2, HEIGHT // 2
SEED = 42

# Parámetros Nivel 1 y 2
ANGULAR_BIAS_UP = 1.6
FAN_OPENING = math.pi * 0.9
TEAR_FACTOR = 1.4
RADIAL_HOLE = 25
BASE_SPEED = 220
ENERGY_PEAK = 2.0
ENERGY_REBOUND = 0.35
MICRO_WAVE_FREQ = 10
NOISE_SCALE = 0.008
NOISE_STRENGTH = 0.5

os.makedirs("output", exist_ok=True)

def energy_curve(t):
    return np.exp(-4 * t) * ENERGY_PEAK + ENERGY_REBOUND * np.sin(10 * t) * np.exp(-2 * t)

# Función de ruido optimizada pero completa
def get_noise_layer(t, scale, octaves=5):
    # Generamos el mapa de ruido Perlin exacto que pide tu fórmula
    noise_map = np.zeros((HEIGHT, WIDTH))
    for y in range(HEIGHT):
        for x in range(WIDTH):
            noise_map[y, x] = pnoise2(
                x * scale, 
                y * scale + t * 2.0, 
                octaves=octaves, 
                persistence=0.5, 
                lacunarity=2.0, 
                repeatx=1024, repeaty=1024, base=SEED
            )
    return noise_map

# =========================================================
# RENDERIZADO FIEL AL MODELO ORIGINAL
# =========================================================

Y, X = np.ogrid[:HEIGHT, :WIDTH]

for frame in range(FRAMES):
    t = frame / FRAMES
    print(f"Renderizando Frame {frame} con precisión total...")
    
    e = energy_curve(t)
    base_radius = BASE_SPEED * t * e
    outer_radius = 130 + base_radius
    
    # 1. Geometría base
    dx = X - CENTER_X
    dy = Y - CENTER_Y
    dist = np.sqrt(dx**2 + dy**2)
    angle = np.arctan2(dy, dx)
    
    # 2. Recreación de tus máscaras exactas
    mask_fan = np.abs(angle) < FAN_OPENING
    mask_hole = dist >= RADIAL_HOLE
    
    # 3. La clave del "Punto A": Las deformaciones
    ang_w = 1 + (((np.sin(angle) + 1) * 0.5) * (ANGULAR_BIAS_UP - 1))
    tear = 1 + (np.sin(angle) * 0.35 * TEAR_FACTOR)
    wave = 1 + 0.12 * np.sin(MICRO_WAVE_FREQ * dist - frame * 0.4)
    
    # Ruido Perlin (El mismo que usabas tú)
    noise_val = get_noise_layer(t, NOISE_SCALE)
    
    # 4. Cálculo de densidad y radio final (TU FÓRMULA)
    # Primero calculamos una densidad base aproximada para la forma
    ratio = dist / outer_radius
    density_base = np.clip(1 - ratio, 0, 1) ** 2.0 # DENSITY_FALLOFF = 2.0
    
    distortion = (1 + noise_val * NOISE_STRENGTH) * wave * tear * ang_w
    final_radius = outer_radius * distortion * (1 + density_base)
    
    # Máscara de presencia (Donde hay explosión)
    presence_mask = (dist <= final_radius) * mask_fan * mask_hole
    
    # 5. Color y Temperatura
    # Simplificamos a los 5 colores de tu lógica pero aplicados en bloque
    # Usamos la densidad base para el gradiente térmico
    temp = density_base * 1.6 # DENSITY_TO_TEMPERATURE
    
    img_rgb = np.zeros((HEIGHT, WIDTH, 3))
    img_rgb[temp > 0.0] = [120, 40, 20]
    img_rgb[temp > 0.3] = [200, 70, 30]
    img_rgb[temp > 0.6] = [255, 150, 60]
    img_rgb[temp > 0.9] = [255, 220, 120]
    img_rgb[temp > 1.2] = [255, 255, 255]
    
    # Aplicar la máscara de presencia y la intensidad
    final_img = img_rgb * presence_mask[..., np.newaxis] * 1.2 # brightness
    
    # 6. Post-procesado (Opcional, pero para el Punto A ayuda)
    # Lo mantenemos sutil para no borrar el detalle que buscas
    bloom = gaussian_filter(np.clip(final_img - 150, 0, 255), sigma=2)
    final_img = np.clip(final_img + bloom * 0.3, 0, 255)

    Image.fromarray(final_img.astype(np.uint8)).save(f"output/frame_{frame:03}.png")

print("Hecho. Ahora sí debe coincidir con tu estructura original.")
