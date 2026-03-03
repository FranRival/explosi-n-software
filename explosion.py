
# ==========================
# EJECUCION
# C:\Users\dell\explosion_env\Scripts\python.exe C:\Users\dell\explosion-software\explosion.py
# ==========================
import os
import math
import random
import numpy as np
from PIL import Image
from noise import pnoise2

# =========================================================
# NIVEL 1 COMPLETO – CONTROL ANGULAR + ENERGÍA + RITMO
# =========================================================

WIDTH = 512
HEIGHT = 512
FRAMES = 60
DURATION = 1.4

CENTER_X = WIDTH // 2
CENTER_Y = HEIGHT // 2

SEED = 42
random.seed(SEED)

os.makedirs("output", exist_ok=True)

# -------------------------------
# PARÁMETROS DE FORMA ANGULAR
# -------------------------------

ANGULAR_BIAS_UP = 1.5       # más densidad arriba
FAN_OPENING = math.pi * 0.8 # explosión en abanico
TEAR_FACTOR = 1.3           # forma lágrima
RADIAL_HOLE = 20            # hueco central

# -------------------------------
# ENERGÍA
# -------------------------------

BASE_SPEED = 280
ENERGY_PEAK = 1.8
ENERGY_REBOUND = 0.25

# -------------------------------
# RITMO TEMPORAL
# -------------------------------

SECONDARY_BURST_TIME = 0.35
MICRO_WAVE_FREQUENCY = 12

# -------------------------------
# RUIDO
# -------------------------------

NOISE_SCALE = 0.006
NOISE_STRENGTH = 0.55

# -------------------------------
# PARTÍCULAS
# -------------------------------

PARTICLE_COUNT = 250
PARTICLE_DRAG = 0.97


# =========================================================
# FUNCIONES
# =========================================================

def perlin(x, y, t, scale):
    return pnoise2(
        x * scale,
        y * scale + t * 2.0,
        octaves=5,
        persistence=0.5,
        lacunarity=2.0,
        repeatx=1024,
        repeaty=1024,
        base=SEED
    )


def energy_curve(t):
    # Pico inicial fuerte + rebote secundario
    peak = math.exp(-4 * t) * ENERGY_PEAK
    rebound = ENERGY_REBOUND * math.sin(8 * t) * math.exp(-2 * t)
    return peak + rebound


def angular_weight(angle):
    # Más densidad arriba
    up_weight = (math.sin(angle) + 1) * 0.5
    return 1 + (up_weight * (ANGULAR_BIAS_UP - 1))


def fan_mask(angle):
    return abs(angle) < FAN_OPENING


def tear_shape(angle):
    return 1 + (math.sin(angle) * 0.3 * TEAR_FACTOR)


# =========================================================
# PARTICULAS AVANZADAS
# =========================================================

class Particle:
    def __init__(self):
        self.angle = random.uniform(-math.pi, math.pi)

        self.delay = random.uniform(0.0, 0.15)
        self.life = random.uniform(0.6, 1.2)

        self.speed = random.uniform(BASE_SPEED * 0.6, BASE_SPEED)

        self.x = CENTER_X
        self.y = CENTER_Y
        self.age = 0

    def update(self, dt, global_t):

        if global_t < self.delay:
            return

        local_t = global_t - self.delay

        e = energy_curve(local_t)

        vx = math.cos(self.angle) * self.speed * e
        vy = math.sin(self.angle) * self.speed * e

        self.x += vx * dt
        self.y += vy * dt

        self.speed *= PARTICLE_DRAG
        self.age += dt

    def alive(self):
        return self.age < self.life


particles = [Particle() for _ in range(PARTICLE_COUNT)]

# =========================================================
# MAIN LOOP
# =========================================================

for frame in range(FRAMES):

    t = frame / FRAMES
    dt = DURATION / FRAMES

    img = np.zeros((HEIGHT, WIDTH, 4), dtype=np.uint8)

    # Radio base con curva energética
    radius_base = BASE_SPEED * t * energy_curve(t)

    for y in range(HEIGHT):
        for x in range(WIDTH):

            dx = x - CENTER_X
            dy = y - CENTER_Y

            dist = math.sqrt(dx * dx + dy * dy)
            angle = math.atan2(dy, dx)

            if not fan_mask(angle):
                continue

            if dist < RADIAL_HOLE:
                continue

            # Peso angular
            ang_weight = angular_weight(angle)

            # Forma lágrima
            tear = tear_shape(angle)

            # Micro-oleadas
            wave = 1 + 0.1 * math.sin(MICRO_WAVE_FREQUENCY * dist - frame * 0.5)

            # Ruido
            noise_val = perlin(x, y, t, NOISE_SCALE)

            distortion = (1 + noise_val * NOISE_STRENGTH) * wave * tear * ang_weight

            final_radius = radius_base * distortion

            # Estructura radial por anillos
            inner_ring = final_radius * 0.4
            mid_ring = final_radius * 0.7

            if dist < inner_ring:
                fade = 1 - (dist / inner_ring)
                intensity = int(255 * fade * 1.8)
                img[y, x] = (intensity, intensity, intensity, 255)

            elif dist < mid_ring:
                fade = 1 - (dist / mid_ring)
                img[y, x] = (255, int(200 * fade), int(50 * fade), 255)

            elif dist < final_radius:
                fade = 1 - (dist / final_radius)
                img[y, x] = (int(200 * fade), int(70 * fade), int(20 * fade), 255)

    # -------------------------
    # ESTALLIDO SECUNDARIO
    # -------------------------

    if t > SECONDARY_BURST_TIME:
        burst_radius = radius_base * 0.6
        for y in range(HEIGHT):
            for x in range(WIDTH):
                dx = x - CENTER_X
                dy = y - CENTER_Y
                dist = math.sqrt(dx * dx + dy * dy)

                if abs(dist - burst_radius) < 4:
                    img[y, x] = (255, 220, 100, 255)

    # -------------------------
    # PARTICULAS
    # -------------------------

    for p in particles:
        if p.alive():
            p.update(dt, t)
            px = int(p.x)
            py = int(p.y)

            if 0 <= px < WIDTH and 0 <= py < HEIGHT:
                img[py, px] = (255, 200, 80, 255)

    Image.fromarray(img, 'RGBA').save(f"output/frame_{frame:03}.png")

print("Nivel 1 completo generado.")