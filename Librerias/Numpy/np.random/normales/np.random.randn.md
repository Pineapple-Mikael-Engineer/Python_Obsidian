---
title: np.random.randn — Muestras de la normal estándar (args sueltos)
aliases: [randn, random.randn, np.random.randn]
tags:
  - numpy
  - api/funcion
  - aleatorio
lib: numpy
mod: np.random
tipo: funcion
retorna: ndarray o float
inplace: false
draft: false
---

# np.random.randn — Muestras de la normal estándar (args sueltos)

## Firma de la función

```python
np.random.randn(d0, d1, ..., dn) -> ndarray | float
```

Las dimensiones se pasan como **argumentos separados** (no como tupla). Sin argumentos devuelve un único `float`.

## Valor de retorno

Devuelve muestras de la distribución **normal estándar** (media `0`, desviación `1`). Si se pasa al menos una dimensión, devuelve un [[concepto_ndarray|ndarray]] `float64` con ese [[concepto_shape|shape]]; sin argumentos devuelve un escalar `float`.

| Llamada | Shape | dtype | Contenido |
|---------|-------|-------|-----------|
| `np.random.randn()` | `()` (escalar) | `float` | un valor ~ N(0,1) |
| `np.random.randn(3)` | `(3,)` | `float64` | vector de 3 muestras |
| `np.random.randn(2, 3)` | `(2, 3)` | `float64` | matriz 2×3 |
| `np.random.randn(2, 3, 4)` | `(2, 3, 4)` | `float64` | tensor |

```python
import numpy as np
np.random.seed(0)
np.random.randn(2, 3)
# array([[ 1.76405235,  0.40015721,  0.97873798],
#        [ 2.2408932 ,  1.86755799, -0.97727788]])
```

## Parámetros en detalle

### `d0, d1, ..., dn` — dimensiones como args sueltos

Cada entero es el tamaño de un eje. **No es una tupla**: se escriben separados por comas. Esta es la diferencia de firma frente a [[np.random.standard_normal]], que recibe el shape como tupla.

```python
np.random.randn(5)        # (5,)      vector
np.random.randn(2, 3)     # (2, 3)    matriz
np.random.randn()         # escalar float
```

Pasar una tupla es un error frecuente: `randn((2, 3))` falla porque interpreta la tupla como una dimensión.

## Casos de uso

### Ruido gaussiano sobre una señal

```python
señal = np.linspace(0, 1, 100)
ruido = 0.1 * np.random.randn(100)   # N(0, 0.1²)
observado = señal + ruido
```

### Inicialización de pesos (estilo redes neuronales)

```python
W = np.random.randn(784, 256) * 0.01   # escala pequeña
```

### Escalar la estándar a una normal arbitraria

```python
media, desv = 50, 5
muestras = media + desv * np.random.randn(1000)   # N(50, 25)
```

Esta fórmula `media + desv * randn(...)` es equivalente a [[np.random.normal]]`(loc=media, scale=desv, size=...)`.

## Buenas prácticas

1. Recuerda: dimensiones como **args sueltos**, no como tupla.
2. Si tu shape ya está en una variable tupla, usa [[np.random.standard_normal]]`(shape)` o `randn(*shape)`.
3. Para media/desviación distintas de 0/1, prefiere [[np.random.normal]] en vez de escalar a mano.
4. Fija `np.random.seed(...)` para resultados reproducibles.

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| `TypeError`/shape inesperado con `randn((2,3))` | se pasó una tupla en vez de args sueltos | `randn(2, 3)` o `randn(*(2, 3))` |
| Esperaba media≠0 o desv≠1 | `randn` siempre es N(0,1) | escalar `media + desv*randn(...)` o usar `np.random.normal` |
| Resultados no reproducibles | falta semilla | `np.random.seed(0)` antes |

## Notas relacionadas

- [[concepto_shape]]
- [[np.random.standard_normal]]
- [[np.random.normal]]
- [[np.random.seed]]
