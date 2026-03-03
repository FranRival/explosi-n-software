import os
import math
import random
import numpy as np
from PIL import Image
from noise import pnoise2


# ==========================
# VERSION 2
# ==========================

# ==========================
# EJECUCION
# C:\Users\dell\explosion_env\Scripts\python.exe C:\Users\dell\explosion-software\explosion.py
# ==========================


# ==========================
# CONFIGURACIÓN
# ==========================

WIDTH = 512
HEIGHT = 512
FRAMES = 40
DURATION = 1.2

CORE_RADIUS = 80
EXPANSION_SPEED = 220
NOISE_STRENGTH = 0.35

PARTICLE_COUNT = 100
PARTICLE_SPEED = (80, 260)

SMOKE_DENSITY = 0.7
SMOKE_OPACITY = 110

SEED = 42
random.seed(SEED)

os.makedirs("output", exist_ok=True)

# ==========================
# RUIDO PROCEDURAL PROPIO
# ==========================


def perlin_fractal(x, y, t):
    scale = 0.01
    octaves = 4
    persistence = 0.5
    lacunarity = 2.0

    return pnoise2(
        x * scale,
        y * scale + t * 2.0,  # animación vertical
        octaves=octaves,
        persistence=persistence,
        lacunarity=lacunarity,
        repeatx=1024,
        repeaty=1024,
        base=SEED
    )
# ==========================
# COLOR GRADIENT
# ==========================

def color_gradient(t):
    if t < 0.2:
        return (255, 255, 255)
    elif t < 0.4:
        return (255, 220, 120)
    elif t < 0.6:
        return (255, 140, 40)
    elif t < 0.8:
        return (200, 60, 20)
    else:
        return (80, 80, 80)


# ==========================
# PARTÍCULAS
# ==========================

class Particle:
    def __init__(self):
        angle = random.uniform(0, 2 * math.pi)
        speed = random.uniform(*PARTICLE_SPEED)

        self.vx = math.cos(angle) * speed
        self.vy = math.sin(angle) * speed

        self.x = WIDTH // 2
        self.y = HEIGHT // 2

        self.life = random.uniform(0.4, 1.0)
        self.age = 0
        self.size = random.randint(2, 3)

    def update(self, dt):
        self.x += self.vx * dt
        self.y += self.vy * dt
        self.age += dt

    def alive(self):
        return self.age < self.life


# ==========================
# MAIN LOOP
# ==========================

particles = [Particle() for _ in range(PARTICLE_COUNT)]

for frame in range(FRAMES):

    t = frame / FRAMES
    dt = DURATION / FRAMES

    img = np.zeros((HEIGHT, WIDTH, 4), dtype=np.uint8)

    center_x = WIDTH // 2
    center_y = HEIGHT // 2

    radius = CORE_RADIUS + EXPANSION_SPEED * t

    # =====================
    # FIRE CORE
    # =====================

    for y in range(HEIGHT):
        for x in range(WIDTH):
            dx = x - center_x
            dy = y - center_y
            dist = math.sqrt(dx * dx + dy * dy)

            noise_val = perlin_fractal(x, y, t)
            distorted_radius = radius * (1 + noise_val * NOISE_STRENGTH)

            if dist < distorted_radius:
                fade = 1 - (dist / distorted_radius)
                color = color_gradient(t)

                img[y, x, 0] = int(color[0] * fade)
                img[y, x, 1] = int(color[1] * fade)
                img[y, x, 2] = int(color[2] * fade)
                img[y, x, 3] = int(255 * fade)

    # =====================
    # SMOKE
    # =====================

    if SMOKE_DENSITY > 0:
        smoke_radius = radius * 1.4

        for y in range(HEIGHT):
            for x in range(WIDTH):
                dx = x - center_x
                dy = y - center_y - t * 60  # humo sube
                dist = math.sqrt(dx * dx + dy * dy)

                if dist < smoke_radius:
                    fade = 1 - (dist / smoke_radius)
                    alpha = int(SMOKE_OPACITY * fade * SMOKE_DENSITY)

                    img[y, x, 0] = max(img[y, x, 0], 70)
                    img[y, x, 1] = max(img[y, x, 1], 70)
                    img[y, x, 2] = max(img[y, x, 2], 70)
                    img[y, x, 3] = max(img[y, x, 3], alpha)

    # =====================
    # PARTICLES
    # =====================

    for p in particles:
        if p.alive():
            p.update(dt)
            px = int(p.x)
            py = int(p.y)

            if 0 <= px < WIDTH and 0 <= py < HEIGHT:
                img[py, px, 0] = 255
                img[py, px, 1] = 200
                img[py, px, 2] = 80
                img[py, px, 3] = 255

    # =====================
    # EXPORT
    # =====================

    Image.fromarray(img, 'RGBA').save(f"output/frame_{frame:03}.png")

print("Explosión generada en carpeta /output")