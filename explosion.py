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
# CONFIGURACIÓN Y CONSTANTES DEL SISTEMA
# =========================================================
WIDTH, HEIGHT = 512, 512
FRAMES = 50
CENTER_X, CENTER_Y = WIDTH // 2, HEIGHT // 2
SEED = 42
random.seed(SEED)
os.makedirs("output", exist_ok=True)

# Parámetros Globales
BASE_SPEED = 220
ENERGY_PEAK = 2.0
FAN_OPENING = math.pi * 0.9
RADIAL_HOLE = 25
FBM_OCTAVES = 8  # Máximo detalle solicitado

# =========================================================
# NIVEL 0: SISTEMA DE PARTÍCULAS (Base Física)
# =========================================================
class Particle:
    def __init__(self):
        angle = random.uniform(-math.pi, math.pi)
        speed = random.uniform(140, 300)
        self.vx = math.cos(angle) * speed
        self.vy = math.sin(angle) * speed
        self.x, self.y = CENTER_X, CENTER_Y
        self.age, self.life = 0, random.uniform(0.6, 1.2)
        self.delay = random.uniform(0.0, 0.18)

    def update(self, dt, energy):
        self.x += self.vx * dt * energy
        self.y += self.vy * dt * energy
        self.vx *= 0.96 # Drag
        self.vy *= 0.96
        self.age += dt

    def alive(self):
        return self.age < self.life

particles = [Particle() for _ in range(180)]

# =========================================================
# NIVEL 2: RUIDO FRACTAL AVANZADO (fBm Multi-escala)
# =========================================================
def get_fbm(x, y, t, scale, octaves=6):
    value, amp, freq = 0.0, 1.0, scale
    for i in range(octaves):
        # Usamos SEED desplazada para que cada escala sea distinta
        n = pnoise2(x * freq, y * freq + t * 0.5, base=SEED + i)
        value += n * amp
        freq *= 2.0
        amp *= 0.5
    return value

# =========================================================
# NIVEL 1 & 2: CAMPO DE DENSIDAD Y CONTROL ARTÍSTICO
# =========================================================
def get_density(x, y, t, outer_radius):
    dx, dy = x - CENTER_X, y - CENTER_Y
    # Influencia de altura (Ascenso)
    dy_lift = dy + (t * 120)
    dist = math.sqrt(dx*dx + dy_lift*dy_lift)
    angle = math.atan2(dy_lift, dx)

    if abs(angle) > FAN_OPENING or dist < RADIAL_HOLE: return 0

    # 1. Influencia Radial y Vertical
    ratio = dist / outer_radius
    if ratio > 1.2: return 0
    base_den = (1 - ratio) ** 2.0
    
    # 2. Multi-Scale Fractal (Macro + Detalle + Profundo)
    macro = get_fbm(x, y, t, 0.004, 4)
    detail = get_fbm(x, y, t, 0.015, 6)
    deep = get_fbm(x, y, t, 0.04, 8)
    
    # 3. Formación de Bultos Tipo Hongo
    mushroom = max(0, (CENTER_Y - y) / HEIGHT) * get_fbm(x, y, t, 0.006, 3)
    
    # Combinación de Densidad
    den = base_den + (macro * 0.5) + (detail * 0.3) + (deep * 0.2) + mushroom
    
    # Compresión interna de masa
    if ratio < 0.35: den *= 1.8 
    
    return max(0, den)

# =========================================================
# NIVEL 3: MODELO TÉRMICO Y COLOR
# =========================================================
def get_thermal_color(density, dist, outer_radius):
    # Temperatura derivada de densidad y proximidad al núcleo
    temp = (density * 1.6) + (1 - dist/outer_radius) * 1.8
    
    if temp > 2.5: return (255, 255, 255) # Núcleo blanco
    if temp > 1.8: return (255, 220, 100) # Amarillo
    if temp > 1.2: return (255, 120, 30)  # Naranja
    if temp > 0.6: return (180, 40, 10)   # Rojo oscuro
    return (60, 60, 60) # Humo/Ceniza

# =========================================================
# RENDERIZADO POR CAPAS
# =========================================================
for frame in range(FRAMES):
    t = frame / FRAMES
    dt = 1.3 / FRAMES
    print(f"Renderizando Nivel 0-3: Frame {frame}")

    # Curva energética no lineal
    energy = math.exp(-4 * t) * 2.0 + 0.35 * math.sin(10 * t)
    outer_radius = 130 + (BASE_SPEED * t * energy)
    
    # Buffer de imagen
    img = np.zeros((HEIGHT, WIDTH, 3), dtype=np.uint8)

    # Renderizado Volumétrico (Nivel 2 y 3)
    for y in range(HEIGHT):
        for x in range(WIDTH):
            den = get_density(x, y, t, outer_radius)
            if den <= 0.1: continue
            
            # Deformación tipo lágrima y angular (Nivel 1)
            dx, dy = x - CENTER_X, y - CENTER_Y
            angle = math.atan2(dy, dx)
            dist = math.sqrt(dx*dx + dy*dy)
            
            tear = 1 + (math.sin(angle) * 0.35 * 1.4)
            ang_w = 1 + (((math.sin(angle) + 1) * 0.5) * 0.6)
            
            if dist > outer_radius * tear * ang_w * (1 + den*0.2): continue

            # Sombreado y Color (Nivel 3)
            color = get_thermal_color(den, dist, outer_radius)
            
            # Simulación de luz (Normales simplificadas)
            shade = 0.5 + 0.5 * (1 - dist/outer_radius)
            img[y, x] = [int(c * shade) for c in color]

    # Renderizado de Partículas (Nivel 0)
    for p in particles:
        if p.alive() and t > p.delay:
            p.update(dt, energy)
            px, py = int(p.x), int(p.y)
            if 0 <= px < WIDTH and 0 <= py < HEIGHT:
                img[py, px] = (255, 230, 150) # Chispas incandescentes

    # Guardado con Post-procesado (Bloom sutil)
    img_final = gaussian_filter(img, sigma=0.5) # Anti-aliasing básico
    Image.fromarray(img_final).save(f"output/frame_{frame:03}.png")

print("Explosión Completa Generada.")
