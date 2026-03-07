u

### Nivel 0 y 1
v1-1-1 - Campo de densidad - densidad continua en lugar de limites radiales
<a href="https://imgbox.com/7Kb6GuTa" target="_blank"><img src="https://images2.imgbox.com/da/d6/7Kb6GuTa_o.gif" alt="image host"/></a>

v2-1-2 - Campo de densidad - influencia de distancia radial
<a href="https://imgbox.com/BKk1ivWW" target="_blank"><img src="https://images2.imgbox.com/3d/4f/BKk1ivWW_o.gif" alt="image host"/></a>

v3-1-3 - Campo de densidad - Influencia de altura (ascenso de la explosion)
<a href="https://imgbox.com/uRA1Ju5I" target="_blank"><img src="https://images2.imgbox.com/c0/c2/uRA1Ju5I_o.gif" alt="image host"/></a>

v4-1-4 - Campo de densidad - compresión interna de masa
<a href="https://imgbox.com/TDtyXqmB" target="_blank"><img src="https://images2.imgbox.com/59/72/TDtyXqmB_o.gif" alt="image host"/></a>

### Nivel 2
v2-2-1 - Ruido fractal avanzado - Fractal Brownian Motion (fBm)
<a href="https://imgbox.com/OO5iXlzN" target="_blank"><img src="https://images2.imgbox.com/0f/c3/OO5iXlzN_o.gif" alt="image host"/></a>

v2-2-2 - Ruido fractal avanzado - 6–8 octavas de ruido
<a href="https://imgbox.com/IjiCTUGG" target="_blank"><img src="https://images2.imgbox.com/8b/6f/IjiCTUGG_o.gif" alt="image host"/></a>


v2-2-3 - Ruido fractal avanzado - Escalas múltiples
<a href="https://imgbox.com/Cl9EUieX" target="_blank"><img src="https://images2.imgbox.com/35/ee/Cl9EUieX_o.gif" alt="image host"/></a>

v2-2-4 - Ruido fractal avanzado - Macroforma + microdetalle
<a href="https://imgbox.com/hgP7L5gp" target="_blank"><img src="https://images2.imgbox.com/ad/e8/hgP7L5gp_o.gif" alt="image host"/></a>


#### 3. Distorcion temporal

v1-3-1 - Distorcion temporal - Evolucion del campo de densidad en el tiempo
<a href="https://imgbox.com/1fTKb5Po" target="_blank"><img src="https://images2.imgbox.com/1b/27/1fTKb5Po_o.gif" alt="image host"/></a>

v1-3-2 - Distorcion temporal - Turbulencia dinamica
<a href="https://imgbox.com/avV4E33A" target="_blank"><img src="https://images2.imgbox.com/6d/18/avV4E33A_o.gif" alt="image host"/></a>


#### 4. Masa volumetrica

v1-4-1 - Masa volumetrica
<a href="https://imgbox.com/3l85ukc5" target="_blank"><img src="https://images2.imgbox.com/fe/10/3l85ukc5_o.gif" alt="image host"/></a>

v2-4-1 - Masa volumetrica - Formacion de bultos tipo hongo
<a href="https://imgbox.com/vYMhdi7r" target="_blank"><img src="https://images2.imgbox.com/8a/36/vYMhdi7r_o.gif" alt="image host"/></a>

v3-4-2 - Masa volumetrica - Estructura irregular interna
<a href="https://imgbox.com/aTskBi3O" target="_blank"><img src="https://images2.imgbox.com/72/76/aTskBi3O_o.gif" alt="image host"/></a>

v4-4-3 - Masa volumetrica - Volumen aparente
<a href="https://imgbox.com/EczjX0FO" target="_blank"><img src="https://images2.imgbox.com/68/4d/EczjX0FO_o.gif" alt="image host"/></a>

---

### Nivel 0 — Base física de la explosión
	•	- Sistema de partículas
	•	- Dirección radial desde el centro
	•	- Velocidad inicial aleatoria
	•	- Movimiento con vectores vx, vy
	•	- Decaimiento de velocidad (drag)
	•	- Tiempo de vida de cada partícula (life, age)
	•	- Método alive() para verificar partículas activas

⸻

### Nivel 1 — Control estructural y artístico - aqui estamos 

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

### Nivel 2 — Campo de densidad volumétrica (2.5D)

#### Campo de densidad
	•	- Densidad continua en lugar de límites radiales: densidad continua + influencia radial + influencia vertical + compresion interna + ruido dentro del campo de densidad
	•	- Influencia de distancia radial: densidad continua + influencia radial + elevacion vertical + ruido procedural
	•	- Influencia de altura (ascenso de la explosión)
	•	- Compresión interna de masa: densidad continua + influencia radial + influencia de altura + ruido procedural + compresión interna de masa

#### Ruido fractal avanzado
	•	- Fractal Brownian Motion (fBm): masas irregulares + turbulencia interna + bordes complejos + estructuras tipo hongo / volumétricas
	•	- 6–8 octavas de ruido: macro deformación de masa + bultos tipo hongo + micro turbulencia + bordes complejos + detalle interno granular
	•	- Escalas múltiples: 1️⃣ Perlin base + 2️⃣ fBm macro + 3️⃣ fBm detalle + 4️⃣ fBm profundo (8 octavas) + 5️⃣ super-macro deformación + 6️⃣ micro detalle fino
	•	- Macroforma + microdetalle: 1️⃣ Perlin base + 2️⃣ fBm macro + 3️⃣ fBm detalle + 4️⃣ fBm profundo (8 octavas) + 5️⃣ multi-scale super macro + 6️⃣ multi-scale fine + 7️⃣ macroforma estructural + 8️⃣ microdetalle granular

#### Distorsión temporal
	•	- Evolución del campo de densidad en el tiempo: vorticidad + 	remolinos reales + turbulencia física + ruptura de la expansión radial
	•	- Turbulencia dinámica: remolinos + rotación del gas + ruptura del patrón radial + estructuras tipo hongo nuclear

#### Masa volumétrica
	•	- Formación de bultos tipo hongo: lóbulos verticales + bultos de gas caliente + estructura tipo nube nuclear
	•	- Estructura irregular interna: grumos internos + cavidades + mezcla turbulenta
	•	- Volumen aparente: centro más sólido + bordes más suaves + mejor sensación de nube

⸻

### Nivel 3 — Modelo térmico y sombreado volumétrico

#### Modelo térmico continuo
	•	- Temperatura derivada de la densidad
	•	- Gradiente térmico continuo: núcleo blanco > amarillo > naranja > rojo > humo.
	•	- Transición física entre núcleo y periferia: núcleo blanco > amarillo brillante > naranja > rojo oscuro > humo

#### Iluminación volumétrica falsa
	•	- Cálculo de gradiente de densidad: bordes del fuego mucho más definidos + humo con volumen real + 	iluminación más natural
	•	- Aproximación de normales
	•	- Dirección de luz simulada

#### Auto-sombreado
	•	- Oscurecimiento interno
	•	- Volumen perceptual
	•	- Profundidad visual

⸻

### Nivel 4 — Composición visual y post-procesado

#### Bloom
	•	- Desenfoque de zonas brillantes
	•	- Expansión de luminancia

#### Compresión tonal
	•	- Ajuste de rango dinámico
	•	- Balance de brillo y contraste

#### Suavizado
	•	- Difuminado volumétrico
	•	- Eliminación de bordes duros

#### Corrección de color
	•	- Ajuste de gradientes térmicos
	•	- Intensificación de colores de fuego

⸻

### Nivel 5 — Sistema procedural completo

#### Variabilidad procedural
	•	- Generación de múltiples estilos de explosión
	•	- Parámetros configurables

#### Presets de explosión
	•	- Explosión realista
	•	Explosión estilizada
	•	Explosión cinematográfica
	•	Explosión abstracta

#### Control artístico
	•	Modificación de forma global
	•	Modificación de intensidad energética
	•	Modificación de dinámica temporal

#### Exportación
	•	Secuencias PNG
	•	GIF animado
	•	Sprite sheets para motores de juego


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