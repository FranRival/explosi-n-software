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