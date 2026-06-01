---
title: np.histogramdd — Histograma N-dimensional
aliases:
  - histogramdd
  - np.histogramdd
tags:
  - numpy
  - api/funcion
  - estadistica

# --- Clasificación ---
lib: numpy
mod: np
tipo: funcion

# --- Comportamiento ---
retorna: tuple
inplace: false

# --- Dependencias ---
requiere:
  - concepto_shape

draft: false
---

# np.histogramdd — Histograma N-dimensional

## Firma de la función

```python
np.histogramdd(
    sample,
    bins=10,
    range=None,
    density=False,
    weights=None
) -> tuple[ndarray, list[ndarray]]
```

## Valor de retorno

Devuelve `(H, edges)`: el histograma en `D` dimensiones y la **lista** de bordes (uno por dimensión). Generaliza [[np.histogram]] (1D) y [[np.histogram2d]] (2D) a cualquier `D`.

| Salida | Contenido |
|--------|-----------|
| `H` | array `D`-dimensional de conteos |
| `edges` | lista de `D` arrays de bordes |

```python
import numpy as np
datos = np.random.rand(1000, 3)   # 1000 puntos en 3D
H, edges = np.histogramdd(datos, bins=(5, 5, 5))
# H.shape == (5, 5, 5)
```

## Parámetros en detalle

### `sample` — datos `(N, D)`

`N` puntos en `D` dimensiones (una columna por dimensión).

### `bins`

Entero, secuencia por dimensión, o lista de bordes por dimensión.

### `density`, `weights`

Como en [[np.histogram]].

## Casos de uso

### Densidad en un espacio de features

```python
H, edges = np.histogramdd(X, bins=10, density=True)
```

## Buenas prácticas

1. `sample` debe tener forma `(N, D)`: filas = puntos, columnas = dimensiones.
2. Para 1D y 2D, prefiere las versiones específicas (más cómodas).

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| Forma de `sample` incorrecta | espera `(N, D)` | transponer si está al revés |
| Memoria alta | muchas dimensiones × bins | reducir `bins` o `D` |

## Limitaciones

- El número de celdas crece como `bins^D` (maldición de la dimensionalidad).

## Notas relacionadas

- [[concepto_shape]]
- [[np.histogram]]
- [[np.histogram2d]]
