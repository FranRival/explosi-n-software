import os
import math
import random
import numpy as np
from PIL import Image
from noise import pnoise2


# ==========================
# EJECUCION
# C:\Users\dell\explosion_env\Scripts\python.exe C:\Users\dell\explosion-software\explosion.py
# ==========================


# ==========================
# VERSION 3 – ESTRUCTURADA
# ==========================

WIDTH = 512
HEIGHT = 512
FRAMES = 40
DURATION = 1.2

# --------------------------
# NUEVAS VARIABLES CLAVE
# --------------------------

RADIUS_CORE = 40
RADIUS_INNER = 80
RADIUS_OUTER = 120

EXPANSION_SPEED = 220

INTENSITY_CORE = 1.8

NOISE_SCALE = 0.008
NOISE_STRENGTH = 0.45

SMOKE_OPACITY = 120
SMOKE_SCALE = 0.004

PARTICLE_COUNT = 120
PARTICLE_SPEED = (120, 300)
PARTICLE_DRAG = 0.96

SEED = 42
random.seed(SEED)

os.makedirs("output", exist_ok=True)


# ==========================
# PERLIN FRACTAL
# ==========================

def perlin(x, y, t, scale):
    return pnoise2(
        x * scale,
        y * scale + t * 2.0,
        octaves=4,
        persistence=0.5,
        lacunarity=2.0,
        repeatx=1024,
        repeaty=1024,
        base=SEED
    )


# ==========================
# PARTÍCULAS MEJORADAS
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
        self.vx *= PARTICLE_DRAG
        self.vy *= PARTICLE_DRAG
        self.age += dt

    def alive(self):
        return self.age < self.life


particles = [Particle() for _ in range(PARTICLE_COUNT)]


# ==========================
# MAIN LOOP
# ==========================

for frame in range(FRAMES):

    t = frame / FRAMES
    dt = DURATION / FRAMES

    img = np.zeros((HEIGHT, WIDTH, 4), dtype=np.uint8)

    center_x = WIDTH // 2
    center_y = HEIGHT // 2

    base_radius = EXPANSION_SPEED * t

    core_radius = RADIUS_CORE + base_radius
    inner_radius = RADIUS_INNER + base_radius
    outer_radius = RADIUS_OUTER + base_radius

    for y in range(HEIGHT):
        for x in range(WIDTH):

            dx = x - center_x
            dy = y - center_y
            dist = math.sqrt(dx * dx + dy * dy)

            # Noise para deformar bordes
            noise_val = perlin(x, y, t, NOISE_SCALE)
            distortion = 1 + noise_val * NOISE_STRENGTH

            # --------------------------
            # NÚCLEO BLANCO
            # --------------------------
            if dist < core_radius * distortion:
                fade = 1 - (dist / (core_radius * distortion))
                intensity = min(255, int(255 * fade * INTENSITY_CORE))
                img[y, x] = (intensity, intensity, intensity, 255)

            # --------------------------
            # FUEGO INTERNO
            # --------------------------
            elif dist < inner_radius * distortion:
                fade = 1 - (dist / (inner_radius * distortion))
                r = 255
                g = int(200 * fade)
                b = int(60 * fade)
                img[y, x] = (r, g, b, 255)

            # --------------------------
            # FUEGO EXTERNO
            # --------------------------
            elif dist < outer_radius * distortion:
                fade = 1 - (dist / (outer_radius * distortion))
                r = int(200 * fade)
                g = int(60 * fade)
                b = int(20 * fade)
                img[y, x] = (r, g, b, 255)

    # ==========================
    # HUMO MEJORADO
    # ==========================

    smoke_radius = outer_radius * 1.5

    for y in range(HEIGHT):
        for x in range(WIDTH):

            dx = x - center_x
            dy = y - center_y - t * 80
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

    # ==========================
    # PARTÍCULAS
    # ==========================

    for p in particles:
        if p.alive():
            p.update(dt)
            px = int(p.x)
            py = int(p.y)

            if 0 <= px < WIDTH and 0 <= py < HEIGHT:
                img[py, px] = (255, 200, 80, 255)

    # ==========================
    # EXPORT
    # ==========================

    Image.fromarray(img, 'RGBA').save(f"output/frame_{frame:03}.png")

print("Explosión versión 3 generada en /output")