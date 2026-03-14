# ==========================
# EJECUCION
# C:\Users\dell\explosion_env\Scripts\python.exe C:\Users\dell\explosion-software\explosion.py
# ===============BASE DESDE AQUI

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

# =========================================================
# FASE 3 — MAPAS GEOMÉTRICOS PRECOMPUTADOS
# =========================================================

x_coords = np.arange(WIDTH)
y_coords = np.arange(HEIGHT)

X, Y = np.meshgrid(x_coords, y_coords)

DX = X - CENTER_X
DY = Y - CENTER_Y

DIST_MAP = np.sqrt(DX**2 + DY**2)
ANGLE_MAP = np.arctan2(DY, DX)

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
# CAMPO DE DENSIDAD BASE
# =========================================================

def base_density_field(dist, base_radius):

    ratio = dist / base_radius

    if ratio >= 1:
        return 0

    density = 1 - ratio
    density = density ** DENSITY_FALLOFF

    return density



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
# FORMACIÓN DE BULTO TIPO HONGO
# =========================================================

MUSHROOM_SCALE = 0.004
MUSHROOM_STRENGTH = 1.1

MUSHROOM_VERTICAL_BIAS = 1.6
MUSHROOM_CAP_RADIUS = 0.65


# =========================================================
# ESTRUCTURA IRREGULAR INTERNA
# =========================================================

INTERNAL_STRUCTURE_SCALE = 0.008
INTERNAL_STRUCTURE_STRENGTH = 0.8

INTERNAL_CAVITY_SCALE = 0.015
INTERNAL_CAVITY_STRENGTH = 0.6


# =========================================================
# VOLUMEN APARENTE
# =========================================================

APPARENT_VOLUME_STRENGTH = 1.3
APPARENT_VOLUME_POWER = 1.6
APPARENT_VOLUME_RADIUS = 0.75

# =========================================================
# NIVEL 3 — MODELO TÉRMICO
# =========================================================

TEMPERATURE_CORE = 1.8
TEMPERATURE_DECAY = 1.4
TEMPERATURE_NOISE_SCALE = 0.01
TEMPERATURE_NOISE_STRENGTH = 0.35

HEAT_BUOYANCY = 1.2

# relación densidad → temperatura
DENSITY_TO_TEMPERATURE = 1.6
TEMPERATURE_DENSITY_POWER = 1.2

# difusión térmica
THERMAL_GRADIENT_SCALE = 0.008
THERMAL_GRADIENT_STRENGTH = 0.6

# transición núcleo → periferia
THERMAL_TRANSITION_RADIUS = 0.65
THERMAL_TRANSITION_POWER = 2.0
THERMAL_COOLING_RATE = 0.7

# =========================================================
# SOMBREADO VOLUMÉTRICO
# =========================================================

LIGHT_DIR_X = -0.6
LIGHT_DIR_Y = -0.8

SHADOW_STRENGTH = 0.7
SCATTER_STRENGTH = 0.5
ABSORPTION = 0.6

# =========================================================
# ILUMINACIÓN VOLUMÉTRICA FALSA
# =========================================================

VOLUME_LIGHT_STRENGTH = 0.9
VOLUME_LIGHT_FALLOFF = 1.8
VOLUME_LIGHT_RADIUS = 0.7

# =========================================================
# AUTO SOMBREADO VOLUMÉTRICO
# =========================================================

SELF_SHADOW_STEPS = 6
SELF_SHADOW_STEP_SIZE = 6
SELF_SHADOW_STRENGTH = 1.4


# tamaño del paso para gradiente
DENSITY_GRADIENT_STEP = 2


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
# GENERADOR DE CAMPOS DE RUIDO (FASE 4)
# =========================================================

def generate_noise_field(scale, t, offset_x=0, offset_y=0):

    field = np.zeros((HEIGHT, WIDTH), dtype=np.float32)

    for y in range(HEIGHT):
        for x in range(WIDTH):

            field[y, x] = pnoise2(
                (x + offset_x) * scale,
                (y + offset_y) * scale + t * 2.0,
                repeatx=1024,
                repeaty=1024,
                base=SEED
            )

    return field

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


# =========================================================
# FORMACIÓN DE BULTO TIPO HONGO
# =========================================================

def mushroom_lobes(x, y, t, dist, base_radius):

    # ruido base que crea lóbulos
    lobe_noise = fbm(x + 15000, y + 15000, t, MUSHROOM_SCALE)

    # sesgo vertical (el hongo sube)
    vertical = (CENTER_Y - y) / HEIGHT
    vertical = max(0, vertical)
    vertical *= MUSHROOM_VERTICAL_BIAS

    # región de la "cúpula" del hongo
    cap_zone = dist / base_radius

    if cap_zone < MUSHROOM_CAP_RADIUS:
        cap_factor = 1 - cap_zone
    else:
        cap_factor = 0

    cap_factor = cap_factor ** 2

    return lobe_noise * vertical * cap_factor * MUSHROOM_STRENGTH


# =========================================================
# ESTRUCTURA IRREGULAR INTERNA
# =========================================================

def internal_structure(x, y, t):

    # masa irregular
    structure = fbm(x + 18000, y + 18000, t, INTERNAL_STRUCTURE_SCALE)

    # cavidades internas
    cavities = fbm_deep(x - 18000, y - 18000, t, INTERNAL_CAVITY_SCALE)

    structure *= INTERNAL_STRUCTURE_STRENGTH
    cavities *= INTERNAL_CAVITY_STRENGTH

    # las cavidades restan densidad
    return structure - abs(cavities)


# =========================================================
# VOLUMEN APARENTE
# =========================================================

def apparent_volume(dist, base_radius):

    ratio = dist / base_radius

    if ratio < APPARENT_VOLUME_RADIUS:
        volume = 1 - ratio
    else:
        volume = 0

    volume = volume ** APPARENT_VOLUME_POWER

    return volume * APPARENT_VOLUME_STRENGTH


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

    ix = x
    iy = y

    dx = x - CENTER_X
    dy = y - CENTER_Y

    # distorsión temporal

    flow_x, flow_y = temporal_flow(x, y, t)
    detail_x, detail_y = temporal_detail(x, y, t)

    x += flow_x + detail_x
    y += flow_y + detail_y

    # turbulencia dinámica

    turb_x, turb_y = dynamic_turbulence(x, y, t)
    turb_dx, turb_dy = dynamic_turbulence_detail(x, y, t)

    x += turb_x + turb_dx
    y += turb_y + turb_dy

    dy_lift = dy + t * DENSITY_HEIGHT_LIFT
    dist = math.sqrt(dx * dx + dy_lift * dy_lift)

    # influencia radial
    # densidad base

    base_density = base_density_field(dist, base_radius)
    radial = radial_modifier(dist, base_radius)

    base_density *= radial

    # ruido procedural

    noise = perlin(x, y, t, DENSITY_NOISE_SCALE)
    noise_density = noise * DENSITY_NOISE_STRENGTH

    # fractal brownian motion

    
    fbm_macro = noise_macro[iy, ix]
    fbm_detail = noise_detail[iy, ix]
    fbm_value = (fbm_macro * 0.7 + fbm_detail * 0.3) * FBM_STRENGTH

    # ruido fractal profundo

    fbm_micro = noise_micro[iy, ix]
    fbm_micro *= FBM_DEEP_STRENGTH

    # multi scale noise

    fbm_super = noise_super[iy, ix]
    fbm_super *= FBM_SUPER_MACRO_STRENGTH

    fbm_fine = noise_fine[iy, ix]
    fbm_fine *= FBM_FINE_STRENGTH

    # macro forma

    macro_shape = noise_macro_shape[iy, ix]
    macro_shape *= MACRO_SHAPE_STRENGTH

    # micro detalle

    micro_detail = noise_micro_detail[iy, ix]
    micro_detail *= MICRO_DETAIL_STRENGTH

    # influencia de altura

    height_component = height_density(y, t)

    # compresión interna

    compression = mass_compression(dist, base_radius)

    # masa volumétrica

    volume_mass = volumetric_mass(x, y, t)

    # bultos tipo hongo

    mushroom = mushroom_lobes(x, y, t, dist, base_radius)

    # estructura irregular interna

    internal = internal_structure(x, y, t)

    # volumen aparente

    apparent = apparent_volume(dist, base_radius)

    # densidad final

    density = (
        base_density
        + noise_density
        + height_component
        + compression
        + volume_mass
        + mushroom
        + internal
        + apparent
        + fbm_value
        + fbm_micro
        + fbm_super
        + fbm_fine
        + macro_shape
        + micro_detail
    )

    return max(0, density)

# =========================================================
# CAMPO DE TEMPERATURA
# =========================================================


def temperature_field(x, y, t, dist, base_radius, density):

    # temperatura base radial
    r = dist / (base_radius + 1e-5)

    if r > 1:
        return 0

    radial_temp = (1 - r) ** TEMPERATURE_DECAY
    radial_temp *= TEMPERATURE_CORE

    # temperatura derivada de la densidad
    density_temp = (density ** TEMPERATURE_DENSITY_POWER) * DENSITY_TO_TEMPERATURE

    # ruido térmico
    heat_noise = fbm(x + 21000, y + 21000, t, TEMPERATURE_NOISE_SCALE)
    heat_noise *= TEMPERATURE_NOISE_STRENGTH

    # flotabilidad del calor
    vertical = max(0, (CENTER_Y - y) / HEIGHT)
    buoyancy = vertical * HEAT_BUOYANCY

    # gradiente térmico continuo
    gradient = thermal_gradient(x, y, t)
    
    transition = thermal_transition(dist, base_radius)
    temperature = (
        radial_temp
    	+ density_temp
		+ heat_noise
        + buoyancy
    	+ gradient
	) * transition

    return max(0, temperature)
    


# =========================================================
# GRADIENTE TÉRMICO CONTINUO
# =========================================================

def thermal_gradient(x, y, t):

    # difusión del calor en el fluido
    gradient = fbm(x + 26000, y + 26000, t, THERMAL_GRADIENT_SCALE)

    gradient *= THERMAL_GRADIENT_STRENGTH

    return gradient
    

# =========================================================
# TRANSICIÓN TÉRMICA NÚCLEO → PERIFERIA
# =========================================================

def thermal_transition(dist, base_radius):

    ratio = dist / (base_radius + 1e-5)

    if ratio > 1:
        return 0

    # región del núcleo
    if ratio < THERMAL_TRANSITION_RADIUS:
        core = 1 - ratio / THERMAL_TRANSITION_RADIUS
        core = core ** THERMAL_TRANSITION_POWER
        return core

    # región de enfriamiento
    outer = (1 - ratio)
    outer = outer ** THERMAL_COOLING_RATE

    return outer
    

# =========================================================
# GRADIENTE DE DENSIDAD
# =========================================================

def density_gradient(x, y, density_map):

    step = DENSITY_GRADIENT_STEP

    x1 = min(WIDTH - 1, x + step)
    x2 = max(0, x - step)

    y1 = min(HEIGHT - 1, y + step)
    y2 = max(0, y - step)

    d1 = density_map[y, x1]
    d2 = density_map[y, x2]

    d3 = density_map[y1, x]
    d4 = density_map[y2, x]

    grad_x = (d1 - d2) / (2 * step)
    grad_y = (d3 - d4) / (2 * step)

    return grad_x, grad_y
    

# =========================================================
# APROXIMACIÓN DE NORMALES VOLUMÉTRICAS
# =========================================================

def density_normal(x, y, density_map):

    grad_x, grad_y = density_gradient(x, y, density_map)

    nx = -grad_x
    ny = -grad_y

    length = math.sqrt(nx * nx + ny * ny) + 1e-5

    nx /= length
    ny /= length

    return nx, ny
    

# =========================================================
# DIRECCIÓN DE LUZ SIMULADA (DESDE EL NÚCLEO)
# =========================================================

def simulated_light_direction(x, y):

    lx = DX[y, x]
    ly = DY[y, x]

    length = math.sqrt(lx * lx + ly * ly) + 1e-5

    lx /= length
    ly /= length

    return lx, ly
    
    
    
# =========================================================
# AUTO SOMBREADO VOLUMÉTRICO
# =========================================================

def volumetric_self_shadow(x, y, density_map):

    light_x, light_y = simulated_light_direction(x, y)

    shadow_density = 0.0

    for i in range(1, SELF_SHADOW_STEPS + 1):

        sx = int(x - light_x * i * SELF_SHADOW_STEP_SIZE)
        sy = int(y - light_y * i * SELF_SHADOW_STEP_SIZE)

        if sx < 0 or sx >= WIDTH or sy < 0 or sy >= HEIGHT:
            continue

        shadow_density += density_map[sy, sx]

    shadow = math.exp(-shadow_density * SELF_SHADOW_STRENGTH)

    return shadow
# =========================================================
# SOMBREADO VOLUMÉTRICO
# =========================================================


def volumetric_shading(x, y, density_map, density):

    normal_x, normal_y = density_normal(x, y, density_map)

    light_x, light_y = simulated_light_direction(x, y)

    light = normal_x * light_x + normal_y * light_y
    light = max(0, light)

    shadow = (1 - light) * SHADOW_STRENGTH

    scatter = density * SCATTER_STRENGTH

    shade = light + scatter - shadow * ABSORPTION

    return max(0, shade)
    

# =========================================================
# ILUMINACIÓN VOLUMÉTRICA FALSA
# =========================================================

def fake_volumetric_light(dist, base_radius, density):

    ratio = dist / (base_radius + 1e-5)

    if ratio > 1:
        return 0

    # intensidad cerca del núcleo
    core_light = max(0, 1 - ratio / VOLUME_LIGHT_RADIUS)

    core_light = core_light ** VOLUME_LIGHT_FALLOFF

    # la luz depende también de la densidad del gas
    light = core_light * density * VOLUME_LIGHT_STRENGTH

    return light
# =========================================================
# COLOR FÍSICO DE FUEGO
# =========================================================

def fire_color(temperature):

    if temperature > 1.2:
        return 255, 255, 255

    elif temperature > 0.9:
        return 255, 220, 120

    elif temperature > 0.6:
        return 255, 150, 60

    elif temperature > 0.3:
        return 200, 70, 30

    else:
        return 120, 40, 20
        
# =========================================================
# MODIFICADOR RADIAL
# =========================================================

def radial_modifier(dist, base_radius):

    radial = max(0, 1 - dist / base_radius)

    radial = radial ** RADIAL_DENSITY_POWER

    radial *= RADIAL_DENSITY_WEIGHT

    return radial
    

# =========================================================
# CURVA DE ENERGÍA DE LA EXPLOSIÓN
# =========================================================

def energy_curve(t):

    peak = math.exp(-4 * t) * ENERGY_PEAK
    rebound = ENERGY_REBOUND * math.sin(10 * t) * math.exp(-2 * t)

    return peak + rebound


# =========================================================
# MÁSCARA ANGULAR (FORMA DE ABANICO)
# =========================================================

def fan_mask(angle):

    return abs(angle) < FAN_OPENING


# =========================================================
# PESO ANGULAR (SESGO HACIA ARRIBA)
# =========================================================

def angular_weight(angle):

    up = (math.sin(angle) + 1) * 0.5
    return 1 + (up * (ANGULAR_BIAS_UP - 1))


# =========================================================
# FORMA DE DESGARRO
# =========================================================

def tear_shape(angle):

    return 1 + (math.sin(angle) * 0.35 * TEAR_FACTOR)

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
    
    # =====================================================
	# FASE 4 — CAMPOS DE RUIDO POR FRAME
	# =====================================================
    
    noise_macro = generate_noise_field(FBM_SCALE_MACRO, t)
    noise_detail = generate_noise_field(FBM_SCALE_DETAIL, t, 500, 500)
    noise_micro = generate_noise_field(FBM_DEEP_SCALE, t, 1200, 1200)
    
    noise_super = generate_noise_field(FBM_SUPER_MACRO_SCALE, t, -800, -800)
    noise_fine = generate_noise_field(FBM_FINE_SCALE, t, 2000, 2000)
    
    noise_macro_shape = generate_noise_field(MACRO_SHAPE_SCALE, t, -3000, -3000)
    noise_micro_detail = generate_noise_field(MICRO_DETAIL_SCALE, t, 3500, 3500)


    img = np.zeros((HEIGHT, WIDTH, 4), dtype=np.uint8)
    density_map = np.zeros((HEIGHT, WIDTH), dtype=np.float32)

    base_radius = BASE_SPEED * t * energy_curve(t)

    core_radius = RADIUS_CORE + base_radius
    inner_radius = RADIUS_INNER + base_radius
    outer_radius = RADIUS_OUTER + base_radius


    # =====================================================
    # PASS 1 — CALCULAR DENSIDAD
    # =====================================================

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

            density_map[y, x] = density


    # =====================================================
    # PASS 2 — SHADING Y COLOR
    # =====================================================

    for y in range(HEIGHT):
        for x in range(WIDTH):

            density = density_map[y, x]

            if density <= 0:
                continue

            dist = DIST_MAP[y, x]

            temperature = temperature_field(
                x, y, t,
                dist,
                outer_radius,
                density
            )

            shade = volumetric_shading(x, y, density_map, density)
            
            self_shadow = volumetric_self_shadow(x, y, density_map)

            volume_light = fake_volumetric_light(dist, outer_radius, density)

            r, g, b = fire_color(temperature)

            brightness = 1.2

            light_factor = shade + volume_light

            r = clamp(r * light_factor * density * brightness)
            g = clamp(g * light_factor * density * brightness)
            b = clamp(b * light_factor * density * brightness)

            img[y, x] = (r, g, b, 255)


    # =====================================================
    # BURST SECUNDARIO
    # =====================================================

    if t > SECONDARY_BURST_TIME:

        burst_radius = base_radius * 0.6

        for y in range(HEIGHT):
            for x in range(WIDTH):

                dx = x - CENTER_X
                dy = y - CENTER_Y
                dist = math.sqrt(dx * dx + dy * dy)

                if abs(dist - burst_radius) < 3:
                    img[y, x] = (255, 220, 100, 255)


    # =====================================================
    # HUMO
    # =====================================================

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


    # =====================================================
    # PARTICULAS
    # =====================================================

    for p in particles:

        if p.alive():

            p.update(dt, t)

            px = int(p.x)
            py = int(p.y)

            if 0 <= px < WIDTH and 0 <= py < HEIGHT:
                img[py, px] = (255, 200, 80, 255)


    Image.fromarray(img, "RGBA").save(f"output/frame_{frame:03}.png")


print("Nivel 0 + Nivel 1 + Nivel 2 + Nivel 3 (Modelo térmico continuo) generado.")