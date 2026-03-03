
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
# NIVEL 0 + NIVEL 1 COMPLETO – ROBUSTO
# =========================================================

WIDTH = 512
HEIGHT = 512
FRAMES = 50
DURATION = 1.3

CENTER_X = WIDTH // 2
CENTER_Y = HEIGHT // 2

SEED = 42
random.seed(SEED)

os.makedirs("output", exist_ok=True)


# =========================================================
# PARÁMETROS NIVEL 1
# =========================================================

# --- Control angular ---
ANGULAR_BIAS_UP = 1.6
FAN_OPENING = math.pi * 0.9
TEAR_FACTOR = 1.4
RADIAL_HOLE = 25

# --- Energía ---
BASE_SPEED = 220
ENERGY_PEAK = 2.0
ENERGY_REBOUND = 0.35

# --- Ritmo ---
SECONDARY_BURST_TIME = 0.45
MICRO_WAVE_FREQ = 10

# --- Capas ---
RADIUS_CORE = 40
RADIUS_INNER = 85
RADIUS_OUTER = 130

INTENSITY_CORE = 2.0

# --- Ruido ---
NOISE_SCALE = 0.008
NOISE_STRENGTH = 0.5

# --- Humo ---
SMOKE_OPACITY = 130
SMOKE_SCALE = 0.004

# --- Partículas ---
PARTICLE_COUNT = 180
PARTICLE_SPEED = (140, 300)
PARTICLE_DRAG = 0.96


# =========================================================
# UTILIDADES
# =========================================================

def clamp(value, min_val=0, max_val=255):
    return max(min_val, min(max_val, int(value)))


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
    peak = math.exp(-4 * t) * ENERGY_PEAK
    rebound = ENERGY_REBOUND * math.sin(10 * t) * math.exp(-2 * t)
    return peak + rebound


def angular_weight(angle):
    up = (math.sin(angle) + 1) * 0.5
    return 1 + (up * (ANGULAR_BIAS_UP - 1))


def fan_mask(angle):
    return abs(angle) < FAN_OPENING


def tear_shape(angle):
    return 1 + (math.sin(angle) * 0.35 * TEAR_FACTOR)


# =========================================================
# PARTICULAS CON DELAY
# =========================================================

class Particle:
    def __init__(self):
        self.angle = random.uniform(-math.pi, math.pi)
        self.delay = random.uniform(0.0, 0.18)
        self.life = random.uniform(0.6, 1.2)

        speed = random.uniform(*PARTICLE_SPEED)
        self.vx = math.cos(self.angle) * speed
        self.vy = math.sin(self.angle) * speed

        self.x = CENTER_X
        self.y = CENTER_Y
        self.age = 0

    def update(self, dt, global_t):

        if global_t < self.delay:
            return

        local_t = global_t - self.delay
        energy = energy_curve(local_t)

        self.x += self.vx * dt * energy
        self.y += self.vy * dt * energy

        self.vx *= PARTICLE_DRAG
        self.vy *= PARTICLE_DRAG

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

    base_radius = BASE_SPEED * t * energy_curve(t)

    core_radius = RADIUS_CORE + base_radius
    inner_radius = RADIUS_INNER + base_radius
    outer_radius = RADIUS_OUTER + base_radius

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

            ang = angular_weight(angle)
            tear = tear_shape(angle)

            wave = 1 + 0.12 * math.sin(MICRO_WAVE_FREQ * dist - frame * 0.4)

            noise_val = perlin(x, y, t, NOISE_SCALE)

            distortion = (1 + noise_val * NOISE_STRENGTH) * wave * tear * ang

            final_radius = outer_radius * distortion

            if dist > final_radius:
                continue

            # --------- CAPAS ESTRUCTURALES ---------

            if dist < core_radius * distortion:
                fade = 1 - (dist / (core_radius * distortion))
                intensity = clamp(255 * fade * INTENSITY_CORE)
                img[y, x] = (intensity, intensity, intensity, 255)

            elif dist < inner_radius * distortion:
                fade = 1 - (dist / (inner_radius * distortion))
                img[y, x] = (
                    clamp(255 * fade),
                    clamp(200 * fade),
                    clamp(70 * fade),
                    255
                )

            else:
                fade = 1 - (dist / final_radius)
                img[y, x] = (
                    clamp(200 * fade),
                    clamp(60 * fade),
                    clamp(20 * fade),
                    255
                )

    # =========================================================
    # ESTALLIDO SECUNDARIO
    # =========================================================

    if t > SECONDARY_BURST_TIME:
        burst_radius = base_radius * 0.6
        for y in range(HEIGHT):
            for x in range(WIDTH):
                dx = x - CENTER_X
                dy = y - CENTER_Y
                dist = math.sqrt(dx * dx + dy * dy)

                if abs(dist - burst_radius) < 3:
                    img[y, x] = (255, 220, 100, 255)

    # =========================================================
    # HUMO
    # =========================================================

    smoke_radius = outer_radius * 1.5

    for y in range(HEIGHT):
        for x in range(WIDTH):

            dx = x - CENTER_X
            dy = y - CENTER_Y - t * 80
            dist = math.sqrt(dx * dx + dy * dy)

            if dist < smoke_radius:
                smoke_noise = perlin(x, y, t, SMOKE_SCALE)
                fade = 1 - (dist / smoke_radius)
                alpha = int(SMOKE_OPACITY * fade * abs(smoke_noise))

                if alpha > 5:
                    img[y, x, 0] = max(img[y, x, 0], 70)
                    img[y, x, 1] = max(img[y, x, 1], 70)
                    img[y, x, 2] = max(img[y, x, 2], 70)
                    img[y, x, 3] = max(img[y, x, 3], alpha)

    # =========================================================
    # PARTICULAS
    # =========================================================

    for p in particles:
        if p.alive():
            p.update(dt, t)
            px = int(p.x)
            py = int(p.y)

            if 0 <= px < WIDTH and 0 <= py < HEIGHT:
                img[py, px] = (255, 200, 80, 255)

    Image.fromarray(img, 'RGBA').save(f"output/frame_{frame:03}.png")

print("Nivel 0 + Nivel 1 COMPLETO generado.")