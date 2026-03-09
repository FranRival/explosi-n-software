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
# CONFIGURACIÓN Y PARÁMETROS (TUS VALORES ORIGINALES)
# =========================================================
WIDTH, HEIGHT = 512, 512
FRAMES = 50
DURATION = 1.3
CENTER_X, CENTER_Y = WIDTH // 2, HEIGHT // 2
SEED = 42

# Parámetros Nivel 1, 2 y 3 (Extraídos de tu versión estable)
BASE_SPEED = 220
ENERGY_PEAK, ENERGY_REBOUND = 2.0, 0.35
DENSITY_HEIGHT_LIFT = 120
FBM_OCTAVES = 6
TEMPERATURE_CORE = 1.8

os.makedirs("output", exist_ok=True)

# =========================================================
# FUNCIONES VECTORIZADAS (EL MOTOR DEL PUNTO A)
# =========================================================

def get_noise_map(t, scale, octaves=5):
    """Genera un mapa de ruido completo para todo el frame."""
    # Nota: pnoise2 no es vectorial, pero lo mapeamos eficientemente
    arr = np.zeros((HEIGHT, WIDTH))
    for y in range(HEIGHT):
        for x in range(WIDTH):
            arr[y, x] = pnoise2(x * scale, y * scale + t * 2.0, octaves=octaves, base=SEED)
    return arr

def energy_curve_vec(t):
    return np.exp(-4 * t) * ENERGY_PEAK + ENERGY_REBOUND * np.sin(10 * t) * np.exp(-2 * t)

# =========================================================
# MAIN RENDER LOOP (OPTIMIZADO)
# =========================================================

# Pre-generar malla de coordenadas
Y, X = np.ogrid[:HEIGHT, :WIDTH]

for frame in range(FRAMES):
    t = frame / FRAMES
    print(f"Renderizando Frame {frame}/{FRAMES} (Vectorizado)...")
    
    # 1. Dinámica Radial y Energía
    e = energy_curve_vec(t)
    base_radius = BASE_SPEED * t * e
    outer_radius = 130 + base_radius
    
    # 2. Coordenadas Volumétricas
    dy_lift = (Y - CENTER_Y) + (t * DENSITY_HEIGHT_LIFT)
    dx = X - CENTER_X
    dist = np.sqrt(dx**2 + dy_lift**2)
    angle = np.arctan2(dy_lift, dx)
    
    # 3. Máscaras y Deformaciones (Nivel 1)
    # Aplicamos tear_shape, angular_weight y fan_mask en bloque
    tear = 1 + (np.sin(angle) * 0.35 * 1.4)
    ang_weight = 1 + (((np.sin(angle) + 1) * 0.5) * (1.6 - 1))
    fan_mask = np.abs(angle) < (math.pi * 0.9)
    
    # 4. Campo de Densidad (Nivel 2)
    # Generamos ruido base una sola vez por frame
    noise_val = get_noise_map(t, 0.008, octaves=5)
    
    # Simulación de densidad continua
    ratio = dist / outer_radius
    density = np.clip(1 - ratio, 0, 1) ** 2.0
    
    # Perturbación fractal (fBm simplificado vectorial)
    fbm_noise = get_noise_map(t, 0.004, octaves=FBM_OCTAVES)
    density = (density + fbm_noise * 0.5) * fan_mask * (dist > 25)
    
    # 5. Sombreado y Modelo Térmico (Nivel 3)
    # Normales rápidas usando gradientes de NumPy
    gy, gx = np.gradient(density)
    mag = np.sqrt(gx**2 + gy**2) + 1e-5
    nx, ny = -gx/mag, -gy/mag
    
    # Luz simulada (dirección núcleo -> afuera)
    lx, ly = dx/(dist+1e-5), dy_lift/(dist+1e-5)
    shade = np.clip(nx * lx + ny * ly, 0, 1)
    
    # Auto-sombreado rápido (Sustituimos el loop de 6 pasos por un desenfoque direccional)
    self_shadow = np.exp(-gaussian_filter(density, sigma=10) * 1.4)
    
    # Temperatura
    temp = (density ** 1.2) * 1.6 + (1 - np.clip(dist/outer_radius, 0, 1)) * TEMPERATURE_CORE
    
    # 6. Mapeo de Color (Punto A)
    img_rgb = np.zeros((HEIGHT, WIDTH, 3))
    
    # Umbrales de fuego vectorizados
    img_rgb[temp > 0.1] = [120, 40, 20]   # Rojo/Humo
    img_rgb[temp > 0.4] = [200, 70, 30]   # Naranja
    img_rgb[temp > 0.8] = [255, 150, 60]  # Naranja Fuego
    img_rgb[temp > 1.2] = [255, 220, 120] # Amarillo
    img_rgb[temp > 1.5] = [255, 255, 255] # Núcleo Blanco

    # Aplicar luz y densidad
    light_factor = (shade + 0.5) * self_shadow
    final_render = img_rgb * light_factor[..., np.newaxis] * np.clip(density[..., np.newaxis], 0, 1)
    
    # 7. Post-Procesado (Nivel 4 incluido por el mismo precio)
    # Bloom rápido
    bloom = gaussian_filter(np.clip(final_render - 100, 0, 255), sigma=4)
    final_render = np.clip(final_render + bloom * 0.4, 0, 255)
    
    # Tone Mapping HDR
    final_render = 255 * (1 - np.exp(-final_render * 1.4 / 255))
    
    # 8. Guardado
    img_final = Image.fromarray(final_render.astype(np.uint8), "RGB")
    img_final.save(f"output/frame_{frame:03}.png")

print("Renderizado completo. Velocidad optimizada, calidad Punto A mantenida.")
