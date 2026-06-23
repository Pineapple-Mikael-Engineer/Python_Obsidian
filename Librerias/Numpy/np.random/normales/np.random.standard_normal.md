---
title: np.random.standard_normal — muestrea la normal estándar N(0, 1) recibiendo size como tupla
aliases:
  - standard_normal
  - np.random.standard_normal
  - random.standard_normal
  - normal estandar
tags:
  - numpy
  - api/funcion
  - aleatorio

# --- Clasificación ---
lib: numpy
mod: np.random
tipo: funcion

# --- Comportamiento ---
retorna: ndarray | escalar
inplace: false

# --- Dependencias ---
requiere:
  - concepto_shape
draft: false
---

# np.random.standard_normal — muestrea la normal estándar N(0, 1) recibiendo size como tupla

`np.random.standard_normal` extrae muestras de la **normal estándar** $N(0, 1)$: media 0 y desviación 1. Es el caso particular de [[np.random.normal]] con `loc=0, scale=1`, y la **forma canónica** de pedir N(0,1) en NumPy moderno, porque recibe la forma como un único argumento `size` (entero o **tupla**), igual que el resto de generadores. Es idéntica en distribución a [[np.random.randn]]; lo que cambia es la firma (tupla vs dimensiones sueltas).

## La idea

La normal estándar es la campana de Gauss centrada en 0 con anchura 1. Su densidad de probabilidad (PDF) es la normal general con $\mu=0,\ \sigma=1$:

$$ f(x) = \frac{1}{\sqrt{2\pi}}\, e^{-x^2/2} $$

Es el "ladrillo" del muestreo gaussiano: cualquier $N(\mu,\sigma^2)$ se construye desplazando y escalando una estándar,

$$ x = \mu + \sigma\, z, \qquad z \sim N(0,1) $$

Por eso `standard_normal` es lo que está por debajo de [[np.random.normal]]: este último genera una estándar y le aplica `loc + scale * z`. La media muestral (vía [[np.mean]]) debe rondar 0 y la desviación (vía [[np.std]]) debe rondar 1.

> [!tip] Versión moderna
> La API legacy (`np.random.standard_normal`) usa el **estado global** del generador, compartido y modificado por `np.random.seed`. En código nuevo, crea un generador propio con [[np.random.default_rng]] y usa su método `standard_normal`:
> ```python
> rng = np.random.default_rng()        # o default_rng(seed) para reproducir
> rng.standard_normal((2, 3))
> ```
> Mismo muestreo N(0,1), sin estado global compartido.

## Firma

```python
np.random.standard_normal(
    size=None,    # None | int | tuple[int]: forma de la salida
) -> ndarray | float
```

## Los parámetros en detalle

### `size` — la forma de la salida (como tupla)
El único parámetro. A diferencia de [[np.random.randn]] (dimensiones como argumentos sueltos), aquí la forma se pasa **como un solo argumento**: un entero para 1D o una **tupla** para N-D. Con `None` (defecto) devuelve un escalar `float`. Esta firma es cómoda cuando el shape ya vive en una variable, sin tener que desempaquetarlo.

```python
np.random.standard_normal(5)        # (5,)    vector
np.random.standard_normal((2, 3))   # (2, 3)  matriz
np.random.standard_normal()         # escalar float

forma = (3, 4)
np.random.standard_normal(forma)    # acepta la tupla directamente, sin *forma
```

## size y la forma de salida

`size` se traslada **literalmente** al shape de salida: cada posición del tensor recibe una muestra independiente de $N(0,1)$. El mapa es la identidad sobre la forma:

$$ \texttt{size}=(n_0,\dots,n_{k-1}) \ \xrightarrow{\ \text{standard\_normal}\ }\ \texttt{salida.shape}=(n_0,\dots,n_{k-1}) $$

| Llamada | Shape de salida | dtype | Contenido |
|---------|-----------------|-------|-----------|
| `np.random.standard_normal()` | `()` escalar | `float` | un valor ~ N(0,1) |
| `np.random.standard_normal(3)` | `(3,)` | `float64` | vector de 3 muestras |
| `np.random.standard_normal((2, 3))` | `(2, 3)` | `float64` | matriz 2×3 |
| `np.random.standard_normal((2, 3, 4))` | `(2, 3, 4)` | `float64` | tensor 3D |

Los tensores de datos de aprendizaje automático suelen ser 4D o 5D, y `size` los crea de una vez. Un lote de 2 tensores de 3 canales y 64×64 (formato `(lote, canales, alto, ancho)`):

```python
import numpy as np
z = np.random.standard_normal((2, 3, 64, 64))
z.shape      # (2, 3, 64, 64)  → 4D: lote=2, canales=3, alto=64, ancho=64
z.size       # 2*3*64*64 = 24_576 muestras independientes ~ N(0,1)

# 5D: lote de clips de vídeo (lote, tiempo, canales, alto, ancho)
v = np.random.standard_normal((4, 8, 3, 32, 32))
v.shape      # (4, 8, 3, 32, 32)
```

## Casos de uso

### Generar con un shape almacenado en variable
```python
forma = (1000, 3)
muestras = np.random.standard_normal(forma)   # sin desempaquetar, a diferencia de randn(*forma)
```

### Escalar a una normal arbitraria
```python
media, desv = 10, 2
x = media + desv * np.random.standard_normal((500,))   # N(10, 4)
```
Equivalente a [[np.random.normal]]`(loc=media, scale=desv, size=...)`.

### Inicialización de pesos
```python
W = np.random.standard_normal((784, 256)) * 0.01   # pesos pequeños ~ N(0, 0.01²)
```

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| `TypeError` con `standard_normal(2, 3)` | se pasaron dimensiones sueltas en vez de una tupla | `standard_normal((2, 3))` |
| Esperaba media≠0 o desv≠1 | siempre es N(0,1) | escalar `μ + σ*z` o usar [[np.random.normal]] |
| Resultados no reproducibles | falta semilla (estado global) | usar `rng = np.random.default_rng(seed)` |

## Notas relacionadas

- [[concepto_shape]] — cómo `size` define la forma de salida
- [[np.random.default_rng]] — el generador moderno sin estado global
- [[np.random.normal]] — la normal general N(μ, σ²)
- [[np.random.randn]] — misma distribución, dimensiones como args sueltos
- [[np.mean]] · [[np.std]] — verificar μ≈0 y σ≈1
- [[np.random.seed]] — reproducibilidad en la API legacy
