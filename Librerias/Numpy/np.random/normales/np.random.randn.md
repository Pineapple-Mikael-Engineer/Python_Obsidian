---
title: np.random.randn — muestrea la normal estándar N(0, 1) con las dimensiones como argumentos sueltos
aliases:
  - randn
  - np.random.randn
  - random.randn
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

# np.random.randn — muestrea la normal estándar N(0, 1) con las dimensiones como argumentos sueltos

`np.random.randn` extrae muestras de la **normal estándar** $N(0, 1)$, exactamente como [[np.random.standard_normal]], pero recibe las dimensiones de salida como **argumentos sueltos** (`randn(2, 3)`) en lugar de una tupla. Es una función de **conveniencia heredada** de estilo MATLAB: cómoda para teclear shapes pequeños a mano, pero atada al estado global. En código moderno la forma recomendada es `rng.standard_normal(...)` (ver más abajo).

## La idea

`randn` muestrea la campana de Gauss centrada en 0 con desviación 1. Su densidad de probabilidad (PDF) es la normal con $\mu=0,\ \sigma=1$:

$$ f(x) = \frac{1}{\sqrt{2\pi}}\, e^{-x^2/2} $$

Como toda normal estándar, es el bloque base del muestreo gaussiano: una muestra de $N(\mu,\sigma^2)$ se obtiene desplazando y escalando,

$$ x = \mu + \sigma\, z, \qquad z = \texttt{randn()} \sim N(0,1) $$

La distribución es idéntica a la de [[np.random.standard_normal]]; lo único que cambia es **cómo se pasa la forma**: `randn(2, 3)` (sueltas) frente a `standard_normal((2, 3))` (tupla). La media muestral (vía [[np.mean]]) debe rondar 0 y la desviación (vía [[np.std]]) debe rondar 1.

> [!tip] Versión moderna
> `np.random.randn` usa el **estado global** del generador y no tiene equivalente directo en la API nueva (no hay `rng.randn`). La forma recomendada hoy es [[np.random.default_rng]] con su método `standard_normal`, pasando la forma como **tupla**:
> ```python
> rng = np.random.default_rng()        # o default_rng(seed) para reproducir
> rng.standard_normal((2, 3))          # sustituye a np.random.randn(2, 3)
> ```
> En código nuevo prefiere `rng.standard_normal(...)`; `randn` se queda como atajo legacy.

## Firma

```python
np.random.randn(
    d0, d1, ..., dn    # int (0 o más): tamaño de cada eje, como args sueltos
) -> ndarray | float
```

## Los parámetros en detalle

### `d0, d1, ..., dn` — las dimensiones como argumentos sueltos
Cada entero es el tamaño de un eje, escritos **separados por comas**, no como una tupla. Sin argumentos devuelve un escalar `float`. Esta es la única diferencia de firma frente a [[np.random.standard_normal]], que recibe la forma como un solo argumento tupla.

```python
np.random.randn()         # escalar float
np.random.randn(5)        # (5,)    vector
np.random.randn(2, 3)     # (2, 3)  matriz
np.random.randn(2, 3, 4)  # (2, 3, 4)  tensor
```

Pasar una **tupla** es el error clásico: `randn((2, 3))` falla, porque interpreta la tupla como un único valor de dimensión. Si la forma ya está en una variable, hay que desempaquetarla con `*`: `randn(*forma)`, o mejor usar `standard_normal(forma)`.

## size y la forma de salida

Aquí no hay un parámetro `size`: la forma se construye con las dimensiones sueltas, pero el efecto es el mismo. Cada posición recibe una muestra independiente de $N(0,1)$ y el mapa es la identidad sobre la forma:

$$ \texttt{randn}(d_0,\dots,d_{k-1}) \ \xrightarrow{\ \text{N(0,1)}\ }\ \texttt{salida.shape}=(d_0,\dots,d_{k-1}) $$

| Llamada | Shape de salida | dtype | Contenido |
|---------|-----------------|-------|-----------|
| `np.random.randn()` | `()` escalar | `float` | un valor ~ N(0,1) |
| `np.random.randn(3)` | `(3,)` | `float64` | vector de 3 muestras |
| `np.random.randn(2, 3)` | `(2, 3)` | `float64` | matriz 2×3 |
| `np.random.randn(2, 3, 4)` | `(2, 3, 4)` | `float64` | tensor 3D |

También admite formas altas: un lote 4D de 2 tensores de 3 canales y 64×64 se pide con las cuatro dimensiones sueltas:

```python
import numpy as np
z = np.random.randn(2, 3, 64, 64)
z.shape      # (2, 3, 64, 64)  → 4D: lote=2, canales=3, alto=64, ancho=64
z.size       # 2*3*64*64 = 24_576 muestras independientes ~ N(0,1)

# 5D: lote de clips de vídeo (lote, tiempo, canales, alto, ancho)
v = np.random.randn(4, 8, 3, 32, 32)
v.shape      # (4, 8, 3, 32, 32)
```

A partir de 4-5 dimensiones, teclear tantos argumentos sueltos es más frágil que una tupla; ahí `standard_normal((...))` o `rng.standard_normal((...))` suelen leerse mejor.

## Casos de uso

### Ruido gaussiano sobre una señal
```python
señal = np.linspace(0, 1, 100)
ruido = 0.1 * np.random.randn(100)   # N(0, 0.1²)
observado = señal + ruido
```

### Inicialización de pesos (estilo redes neuronales)
```python
W = np.random.randn(784, 256) * 0.01   # pesos pequeños
```

### Escalar la estándar a una normal arbitraria
```python
media, desv = 50, 5
muestras = media + desv * np.random.randn(1000)   # N(50, 25)
```
La fórmula `media + desv * randn(...)` equivale a [[np.random.normal]]`(loc=media, scale=desv, size=...)`.

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| `TypeError`/shape raro con `randn((2, 3))` | se pasó una tupla en vez de args sueltos | `randn(2, 3)` o `randn(*(2, 3))` |
| Esperaba media≠0 o desv≠1 | `randn` siempre es N(0,1) | escalar `media + desv*randn(...)` o usar [[np.random.normal]] |
| Resultados no reproducibles | falta semilla (estado global) | usar `rng = np.random.default_rng(seed)` |

## Notas relacionadas

- [[concepto_shape]] — la forma de salida construida con las dimensiones
- [[np.random.default_rng]] — el generador moderno (`rng.standard_normal`)
- [[np.random.standard_normal]] — misma distribución, forma como tupla
- [[np.random.normal]] — la normal general N(μ, σ²)
- [[np.mean]] · [[np.std]] — verificar μ≈0 y σ≈1
- [[np.random.seed]] — reproducibilidad en la API legacy
