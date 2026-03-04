

### Nivel 0 — Base física de la explosión
	•	- Sistema de partículas
	•	- Dirección radial desde el centro
	•	Velocidad inicial aleatoria
	•	- Movimiento con vectores vx, vy
	•	- Decaimiento de velocidad (drag)
	•	- Tiempo de vida de cada partícula (life, age)
	•	- Método alive() para verificar partículas activas

⸻

### Nivel 1 — Control estructural y artístico

#### Control angular
	•	- Más densidad hacia arriba (angular_weight)
	•	- Explosión en abanico (fan_mask)
	•	- Deformación tipo lágrima (tear_shape)
	•	- Hueco central (RADIAL_HOLE)

#### Curva energética no lineal
	•	- Pico inicial fuerte
	•	- Decaimiento exponencial
	•	- Rebote energético (energy_curve)

#### Ritmo temporal
	•	- Delay por partícula
	•	- Micro-oleadas internas
	•	- Estallido secundario

#### Variación radial estructural
	•	- Anillos de expansión
	•	- Núcleo diferenciado
	•	- Fuego interno
	•	- Fuego externo
	•	- Estructura jerárquica de capas

#### Otros elementos visuales
	•	- Distorsión de forma con ruido Perlin
	•	- Humo procedural
	•	- Partículas secundarias de la explosión


-----






### Cómo simulamos “volumen” en 2D

En este MVP no usamos simulación volumétrica real ni física avanzada.  
En su lugar, generamos la **ilusión de volumen** mediante técnicas matemáticas y composición en 2D.

La idea no es simular fuego real, sino simular cómo el ojo humano percibe el fuego.

---

### Técnicas utilizadas para simular volumen

#### 1. Gradientes radiales

Usamos un gradiente desde el centro hacia afuera:

- Centro brillante (blanco / amarillo)
- Transición a naranja / rojo
- Oscurecimiento progresivo
- Alpha decreciente hacia el borde

Esto genera profundidad visual básica.

---

#### 2. Ruido fractal (Perlin Noise)

Aplicamos ruido al radio de la explosión:

- Evita que la forma sea un círculo perfecto
- Crea bordes irregulares
- Simula turbulencia
- Se anima en el tiempo para dar movimiento orgánico

Sin ruido, el resultado se ve artificial.

---

#### 3. Capas superpuestas

La explosión se construye en capas:

1. Humo (fondo)
2. Bola de fuego
3. Partículas
4. Glow implícito

La superposición genera sensación de profundidad.

---

#### 4. Diferentes velocidades de expansión

Cada elemento se mueve distinto:

- Fuego: expansión rápida
- Partículas: velocidad radial independiente
- Humo: expansión lenta + ascenso

La diferencia de velocidades crea efecto tridimensional.

---

#### 5. Blend implícito mediante alpha

Se utiliza canal alpha para:

- Fusionar capas
- Suavizar bordes
- Simular energía luminosa
- Crear transición natural entre elementos

---

#### 6. Curvas no lineales de crecimiento

La expansión no es lineal.  
Se usan funciones como:

- Exponenciales
- Ease-out
- Decaimiento progresivo

Esto hace que la explosión se sienta más natural.