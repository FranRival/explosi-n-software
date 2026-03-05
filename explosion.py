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

RADIAL_DENSITY_WEIGHT = 1.4
RADIAL_DENSITY_POWER = 1.6

SEED = 42
random.seed(SEED)

os.makedirs("output", exist_ok=True)


# =========================================================
# PARÁMETROS NIVEL 1
# =========================================================

ANGULAR_BIAS_UP = 1.6
FAN_OPENING = math.pi * 0.9
TEAR_FACTOR = 1.4
RADIAL_HOLE = 25

BASE_SPEED = 220
ENERGY_PEAK = 2.0
ENERGY_REBOUND = 0.35

SECONDARY_BURST_TIME = 0.45
MICRO_WAVE_FREQ = 10

RADIUS_CORE = 40
RADIUS_INNER = 85
RADIUS_OUTER = 130

INTENSITY_CORE = 2.0

NOISE_SCALE = 0.008
NOISE_STRENGTH = 0.5

SMOKE_OPACITY = 130
SMOKE_SCALE = 0.004

PARTICLE_COUNT = 180
PARTICLE_SPEED = (140, 300)
PARTICLE_DRAG = 0.96


# =========================================================
# PARÁMETROS NIVEL 2 (CAMPO DE DENSIDAD)
# =========================================================

DENSITY_FALLOFF = 2.0
DENSITY_HEIGHT_LIFT = 120
DENSITY_NOISE_SCALE = 0.01
DENSITY_NOISE_STRENGTH = 0.6

HEIGHT_DENSITY_WEIGHT = 1.7
HEIGHT_DENSITY_POWER = 1.4

# compresión interna de masa
MASS_COMPRESSION = 1.8
MASS_CORE_RADIUS = 0.35

# =========================================================
# RUIDO FRACTAL AVANZADO (fBm)
# =========================================================

FBM_OCTAVES = 6
FBM_GAIN = 0.5
FBM_LACUNARITY = 2.0

FBM_SCALE_MACRO = 0.004
FBM_SCALE_DETAIL = 0.02

FBM_STRENGTH = 0.65

# ruido fractal profundo (6-8 octavas)
FBM_DEEP_OCTAVES = 8
FBM_DEEP_GAIN = 0.55
FBM_DEEP_LACUNARITY = 2.1

FBM_DEEP_SCALE = 0.015
FBM_DEEP_STRENGTH = 0.45

# =========================================================
# MULTI SCALE FRACTAL (ESCALAS MULTIPLES)
# =========================================================

FBM_SUPER_MACRO_SCALE = 0.0015
FBM_SUPER_MACRO_STRENGTH = 0.55

FBM_FINE_SCALE = 0.04
FBM_FINE_STRENGTH = 0.35

# =========================================================
# MACROFORMA + MICRODETALLE
# =========================================================

MACRO_SHAPE_SCALE = 0.002
MACRO_SHAPE_STRENGTH = 0.7

MICRO_DETAIL_SCALE = 0.06
MICRO_DETAIL_STRENGTH = 0.25


# =========================================================
# DISTORSIÓN TEMPORAL (EVOLUCIÓN DEL CAMPO DE DENSIDAD)
# =========================================================

TEMPORAL_FLOW_SCALE = 0.003
TEMPORAL_FLOW_STRENGTH = 80

TEMPORAL_DETAIL_SCALE = 0.01
TEMPORAL_DETAIL_STRENGTH = 35

# =========================================================
# TURBULENCIA DINÁMICA
# =========================================================

TURBULENCE_SCALE = 0.006
TURBULENCE_STRENGTH = 45

TURBULENCE_DETAIL_SCALE = 0.02
TURBULENCE_DETAIL_STRENGTH = 18

# =========================================================
# MASA VOLUMÉTRICA
# =========================================================

VOLUME_MASS_SCALE = 0.003
VOLUME_MASS_STRENGTH = 1.2

VOLUME_MASS_DETAIL_SCALE = 0.01
VOLUME_MASS_DETAIL_STRENGTH = 0.6


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
    
    
# =========================================================
# FRACTAL BROWNIAN MOTION
# =========================================================

def fbm(x, y, t, scale):

    value = 0.0
    amplitude = 1.0
    frequency = scale

    for i in range(FBM_OCTAVES):

        n = pnoise2(
            x * frequency,
            y * frequency + t * 2.0,
            repeatx=1024,
            repeaty=1024,
            base=SEED + i
        )

        value += n * amplitude

        frequency *= FBM_LACUNARITY
        amplitude *= FBM_GAIN

    return value
    

# =========================================================
# FRACTAL BROWNIAN MOTION PROFUNDO (8 OCTAVAS)
# =========================================================

def fbm_deep(x, y, t, scale):

    value = 0.0
    amplitude = 1.0
    frequency = scale

    for i in range(FBM_DEEP_OCTAVES):

        n = pnoise2(
            x * frequency,
            y * frequency + t * 2.0,
            repeatx=1024,
            repeaty=1024,
            base=SEED + 200 + i
        )

        value += n * amplitude

        frequency *= FBM_DEEP_LACUNARITY
        amplitude *= FBM_DEEP_GAIN

    return value
    
    
# =========================================================
# MULTI SCALE FRACTAL NOISE
# =========================================================

def fbm_super_macro(x, y, t):

    return fbm(x, y, t, FBM_SUPER_MACRO_SCALE)


def fbm_fine_detail(x, y, t):

    return fbm_deep(x, y, t, FBM_FINE_SCALE)
    
    
# =========================================================
# MACROFORMA
# =========================================================

def macro_shape_noise(x, y, t):

    return fbm(x, y, t, MACRO_SHAPE_SCALE)


# =========================================================
# MICRO DETALLE
# =========================================================

def micro_detail_noise(x, y, t):

    return fbm_deep(x, y, t, MICRO_DETAIL_SCALE)
    
    
    
# =========================================================
# DISTORSIÓN TEMPORAL DEL CAMPO DE DENSIDAD
# =========================================================

def temporal_flow(x, y, t):

    flow_x = fbm(x + 4000, y + 4000, t, TEMPORAL_FLOW_SCALE)
    flow_y = fbm(x - 4000, y - 4000, t, TEMPORAL_FLOW_SCALE)

    flow_x *= TEMPORAL_FLOW_STRENGTH
    flow_y *= TEMPORAL_FLOW_STRENGTH

    return flow_x, flow_y


def temporal_detail(x, y, t):

    detail_x = fbm_deep(x + 6000, y + 6000, t, TEMPORAL_DETAIL_SCALE)
    detail_y = fbm_deep(x - 6000, y - 6000, t, TEMPORAL_DETAIL_SCALE)

    detail_x *= TEMPORAL_DETAIL_STRENGTH
    detail_y *= TEMPORAL_DETAIL_STRENGTH

    return detail_x, detail_y
    
    
# =========================================================
# TURBULENCIA DINÁMICA
# =========================================================

def dynamic_turbulence(x, y, t):

    # campo base
    n1 = fbm(x + 8000, y + 8000, t, TURBULENCE_SCALE)
    n2 = fbm(x - 8000, y - 8000, t, TURBULENCE_SCALE)

    vx = -n2
    vy = n1

    vx *= TURBULENCE_STRENGTH
    vy *= TURBULENCE_STRENGTH

    return vx, vy


def dynamic_turbulence_detail(x, y, t):

    n1 = fbm_deep(x + 10000, y + 10000, t, TURBULENCE_DETAIL_SCALE)
    n2 = fbm_deep(x - 10000, y - 10000, t, TURBULENCE_DETAIL_SCALE)

    vx = -n2
    vy = n1

    vx *= TURBULENCE_DETAIL_STRENGTH
    vy *= TURBULENCE_DETAIL_STRENGTH

    return vx, vy
    
    
# =========================================================
# MASA VOLUMÉTRICA
# =========================================================

def volumetric_mass(x, y, t):

    # masa base
    base_mass = fbm(x + 12000, y + 12000, t, VOLUME_MASS_SCALE)

    # detalle interno
    detail_mass = fbm_deep(x - 12000, y - 12000, t, VOLUME_MASS_DETAIL_SCALE)

    base_mass *= VOLUME_MASS_STRENGTH
    detail_mass *= VOLUME_MASS_DETAIL_STRENGTH

    return base_mass + detail_mass
    
    
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
# INFLUENCIA DE ALTURA
# =========================================================

def height_density(y, t):

    lift = t * DENSITY_HEIGHT_LIFT

    height_factor = (CENTER_Y - y + lift) / HEIGHT

    height_factor = max(0, height_factor)

    height_factor = height_factor ** HEIGHT_DENSITY_POWER

    return height_factor * HEIGHT_DENSITY_WEIGHT


# =========================================================
# COMPRESIÓN INTERNA DE MASA
# =========================================================

def mass_compression(dist, base_radius):

    core_limit = base_radius * MASS_CORE_RADIUS

    if dist < core_limit:

        compression = 1 - (dist / core_limit)

        compression = compression ** MASS_COMPRESSION

        return compression

    return 0
# =========================================================
# CAMPO DE DENSIDAD
# =========================================================

def density_field(x, y, t, base_radius):

    dx = x - CENTER_X
    dy = y - CENTER_Y
    
    # -----------------------------
	# distorsión temporal
	# -----------------------------
    flow_x, flow_y = temporal_flow(x, y, t)
    detail_x, detail_y = temporal_detail(x, y, t)
    
    x = x + flow_x + detail_x
    y = y + flow_y + detail_y
    
    # -----------------------------
	# turbulencia dinámica
	# -----------------------------
    turb_x, turb_y = dynamic_turbulence(x, y, t)
    turb_dx, turb_dy = dynamic_turbulence_detail(x, y, t)
    
    x = x + turb_x + turb_dx
    y = y + turb_y + turb_dy

    dy_lift = dy + t * DENSITY_HEIGHT_LIFT

    dist = math.sqrt(dx * dx + dy_lift * dy_lift)

    # -----------------------------
    # influencia radial
    # -----------------------------

    radial = max(0, 1 - dist / base_radius)
    radial = radial ** RADIAL_DENSITY_POWER
    radial *= RADIAL_DENSITY_WEIGHT

    # -----------------------------
    # densidad base
    # -----------------------------

    base_density = radial ** DENSITY_FALLOFF

    # -----------------------------
    # ruido procedural
    # -----------------------------

    noise = perlin(x, y, t, DENSITY_NOISE_SCALE)
    noise_density = noise * DENSITY_NOISE_STRENGTH
    
    
    # -----------------------------
	# fractal brownian motion
	# -----------------------------
    fbm_macro = fbm(x, y, t, FBM_SCALE_MACRO)
    fbm_detail = fbm(x + 500, y + 500, t, FBM_SCALE_DETAIL)
    fbm_value = (fbm_macro * 0.7 + fbm_detail * 0.3) * FBM_STRENGTH
    
    # -----------------------------
	# ruido fractal profundo
	# -----------------------------
    fbm_micro = fbm_deep(x + 1200, y + 1200, t, FBM_DEEP_SCALE)
    
    fbm_micro *= FBM_DEEP_STRENGTH

	# -----------------------------
	# multi scale noise
	# -----------------------------
    fbm_super = fbm_super_macro(x - 800, y - 800, t)
    fbm_super *= FBM_SUPER_MACRO_STRENGTH
    
    fbm_fine = fbm_fine_detail(x + 2000, y + 2000, t)
    fbm_fine *= FBM_FINE_STRENGTH
    
    
    # -----------------------------
	# macro forma
	# -----------------------------
    macro_shape = macro_shape_noise(x - 3000, y - 3000, t)
    macro_shape *= MACRO_SHAPE_STRENGTH


	# -----------------------------
	# micro detalle
	# -----------------------------
    micro_detail = micro_detail_noise(x + 3500, y + 3500, t)
    micro_detail *= MICRO_DETAIL_STRENGTH

    # -----------------------------
    # influencia de altura
    # -----------------------------

    height_component = height_density(y, t)

	# ----------------------
    # compresión interna
    # ---------------------
    compression = mass_compression(dist, base_radius)
    
    # -----------------------------
	# masa volumétrica
	# -----------------------------
	volume_mass = volumetric_mass(x, y, t)
  
    # -----------------------------
    # densidad final
    # -----------------------------
    density = base_density + noise_density + height_component + compression + volume_mass + fbm_value + fbm_micro + fbm_super + fbm_fine + macro_shape + micro_detail
    return max(0, density)


# =========================================================
# PARTICULAS
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

            density = density_field(x, y, t, outer_radius)

            if density <= 0:
                continue

            ang = angular_weight(angle)
            tear = tear_shape(angle)

            wave = 1 + 0.12 * math.sin(MICRO_WAVE_FREQ * dist - frame * 0.4)

            noise_val = perlin(x, y, t, NOISE_SCALE)

            distortion = (1 + noise_val * NOISE_STRENGTH) * wave * tear * ang

            final_radius = outer_radius * distortion * (1 + density)

            if dist > final_radius:
                continue

            if dist < core_radius * distortion:

                fade = 1 - (dist / (core_radius * distortion))
                intensity = clamp(255 * fade * INTENSITY_CORE * density)

                img[y, x] = (intensity, intensity, intensity, 255)

            elif dist < inner_radius * distortion:

                fade = 1 - (dist / (inner_radius * distortion))

                img[y, x] = (
                    clamp(255 * fade * density),
                    clamp(200 * fade * density),
                    clamp(70 * fade * density),
                    255
                )

            else:

                fade = 1 - (dist / final_radius)

                img[y, x] = (
                    clamp(200 * fade * density),
                    clamp(60 * fade * density),
                    clamp(20 * fade * density),
                    255
                )

    if t > SECONDARY_BURST_TIME:

        burst_radius = base_radius * 0.6

        for y in range(HEIGHT):
            for x in range(WIDTH):

                dx = x - CENTER_X
                dy = y - CENTER_Y
                dist = math.sqrt(dx * dx + dy * dy)

                if abs(dist - burst_radius) < 3:
                    img[y, x] = (255, 220, 100, 255)

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

    for p in particles:

        if p.alive():

            p.update(dt, t)

            px = int(p.x)
            py = int(p.y)

            if 0 <= px < WIDTH and 0 <= py < HEIGHT:
                img[py, px] = (255, 200, 80, 255)

    Image.fromarray(img, "RGBA").save(f"output/frame_{frame:03}.png")


print("Nivel 0 + Nivel 1 + Nivel 2 (ruido fractal avanzado) generado.")