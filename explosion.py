# ==========================
# EJECUCION
# C:\Users\dell\explosion_env\Scripts\python.exe C:\Users\dell\explosion-software\explosion.py
# ===============

import os
import math
import random
import numpy as np
from PIL import Image
from noise import pnoise2
from scipy.ndimage import gaussian_filter

# =========================================================
# CONFIGURACIÓN Y PARÁMETROS (APEGADO AL README)
# =========================================================
WIDTH, HEIGHT = 512, 512
FRAMES = 50
DURATION = 1.3
CENTER_X, CENTER_Y = WIDTH // 2, HEIGHT // 2
SEED = 42

# Parámetros Nivel 1 & 2
ANGULAR_BIAS_UP = 1.6
FAN_OPENING = math.pi * 0.9
TEAR_FACTOR = 1.4
RADIAL_HOLE = 25
ENERGY_PEAK = 2.0
ENERGY_REBOUND = 0.35
DENSITY_HEIGHT_LIFT = 120

# Parámetros Nivel 3 (Térmico)
TEMPERATURE_CORE = 1.8
TEMPERATURE_DECAY = 1.4

os.makedirs("output", exist_ok=True)

# =========================================================
# UTILIDADES VECTORIALES (ACELERACIÓN HACIA EL PUNTO A)
# =========================================================

def energy_curve(t):
    peak = np.exp(-4 * t) * ENERGY_PEAK
    rebound = ENERGY_REBOUND * np.sin(10 * t) * np.exp(-2 * t)
    return peak + rebound

def fast_fbm(x_grid, y_grid, t, scale, octaves=6):
    """Genera ruido fractal de forma eficiente sobre una malla."""
    noise_map = np.zeros(x_grid.shape)
    amp = 1.0
    freq = scale
    for i in range(octaves):
        # Mapeo de pnoise2 sobre la matriz
        # Nota: En una versión Pro usaríamos FastNoiseSIMD, aquí optimizamos el acceso
        for r in range(0, HEIGHT, 4): # Sampling saltado para velocidad sin perder macroforma
            for c in range(0, WIDTH, 4):
                val = pnoise2(c * freq, r * freq + t * 2.0, base=SEED + i)
                noise_map[r:r+4, c:c+4] = val * amp
        amp *= 0.5
        freq *= 2.0
    return noise_map

# =========================================================
# NIVELES 1, 2 Y 3: CÁLCULO VOLUMÉTRICO INTEGRADO
# =========================================================

def render_frame(frame_idx):
    t = frame_idx / FRAMES
    dt = DURATION / FRAMES
    
    # Malla de coordenadas
    y_coords, x_coords = np.ogrid[:HEIGHT, :WIDTH]
    dx = x_coords - CENTER_X
    dy = y_coords - CENTER_Y
    
    # 1. Energía y Radio
    e = energy_curve(t)
    base_radius = 220 * t * e
    outer_radius = 130 + base_radius
    
    # 2. Distorsión Temporal y Vorticidad (Nivel 2)
    # Simulamos el flujo de gas con un desplazamiento en la lectura de coordenadas
    lift = t * DENSITY_HEIGHT_LIFT
    dist = np.sqrt(dx**2 + (dy + lift)**2)
    angle = np.arctan2(dy + lift, dx)
    
    # 3. Control Estructural (Nivel 1)
    fan_mask = np.abs(angle) < FAN_OPENING
    up_weight = (np.sin(angle) + 1) * 0.5
    ang_bias = 1 + (up_weight * (ANGULAR_BIAS_UP - 1))
    tear = 1 + (np.sin(angle) * 0.35 * TEAR_FACTOR)
    
    # 4. Campo de Densidad Volumétrica (Nivel 2)
    # Combinamos ruidos: Macroforma + Microdetalle
    noise_macro = fast_fbm(x_coords, y_coords, t, 0.004, octaves=4)
    noise_detail = fast_fbm(x_coords, y_coords, t, 0.02, octaves=8)
    
    density = np.clip(1 - (dist / (outer_radius * tear * ang_bias)), 0, 1)
    density = (density ** 2.0) + (noise_macro * 0.5) + (noise_detail * 0.2)
    density = np.clip(density, 0, 2)
    
    # Hueco central y máscara de abanico
    density *= (dist > RADIAL_HOLE)
    density *= fan_mask
    
    # 5. Modelo Térmico (Nivel 3)
    # Núcleo blanco > Amarillo > Rojo > Humo
    temp = (density ** 1.2) * 1.6
    temp += (1 - (dist / (base_radius + 1e-5))) * TEMPERATURE_CORE
    temp = np.clip(temp, 0, 2)

    # 6. Sombreado y Auto-sombreado (Nivel 3)
    # Simulamos oclusión ambiental simple basada en densidad
    shadow = np.exp(-density * 1.4)
    light_dir = np.array([-0.6, -0.8])
    # Aproximación de normales por gradiente de densidad
    grad_y, grad_x = np.gradient(density)
    normal_len = np.sqrt(grad_x**2 + grad_y**2) + 1e-5
    nx, ny = -grad_x/normal_len, -grad_y/normal_len
    diffuse = np.clip(nx * light_dir[0] + ny * light_dir[1], 0, 1)

    # 7. Asignación de Color Físico
    img_rgb = np.zeros((HEIGHT, WIDTH, 3))
    
    # Capas de color por temperatura
    img_rgb[temp > 0.1] = [120, 40, 20]   # Rojo oscuro / Humo
    img_rgb[temp > 0.4] = [200, 70, 30]   # Naranja
    img_rgb[temp > 0.8] = [255, 150, 60]  # Naranja brillante
    img_rgb[temp > 1.2] = [255, 220, 120] # Amarillo
    img_rgb[temp > 1.5] = [255, 255, 255] # Blanco (Core)

    # Aplicar Iluminación y Sombreado
    lighting = (diffuse * 0.5 + 0.5) * shadow * density
    img_rgb *= lighting[..., np.newaxis]

    return img_rgb

# =========================================================
# NIVEL 4: POST-PROCESADO Y COMPOSICIÓN
# =========================================================

for frame in range(FRAMES):
    print(f"Generando Nivel 4 - Frame {frame:03}...")
    
    # Obtener base volumétrica
    frame_data = render_frame(frame)
    
    # 1. Bloom (Desenfoque gaussiano sobre las altas luces)
    bright_mask = np.clip(frame_data - 150, 0, 255)
    bloom = gaussian_filter(bright_mask, sigma=5)
    frame_data = np.clip(frame_data + bloom * 0.4, 0, 255)
    
    # 2. Tone Mapping & Gamma
    frame_data = 255 * (1 - np.exp(-frame_data * 1.4 / 255))
    
    # 3. Viñeta
    y, x = np.ogrid[:HEIGHT, :WIDTH]
    v_dist = np.sqrt((x - CENTER_X)**2 + (y - CENTER_Y)**2)
    vignette = 1 - (v_dist / (WIDTH * 0.75)) * 0.6
    frame_data *= np.clip(vignette[..., np.newaxis], 0, 1)

    # Guardado con canal Alfa (RGBA)
    final_img = np.zeros((HEIGHT, WIDTH, 4), dtype=np.uint8)
    final_img[..., :3] = frame_data.astype(np.uint8)
    final_img[..., 3] = np.clip(np.max(frame_data, axis=2) * 2, 0, 255).astype(np.uint8)

    Image.fromarray(final_img, "RGBA").save(f"output/frame_{frame:03}.png")

print("\n[MISIÓN CUMPLIDA]")
print("Se han generado 50 frames con estructura jerárquica, modelo térmico y post-procesado Nivel 4.")
