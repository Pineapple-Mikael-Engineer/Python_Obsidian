---
title: np.histogram2d — Histograma bidimensional
aliases:
  - histogram2d
  - np.histogram2d
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

# np.histogram2d — Histograma bidimensional

## Firma de la función

```python
np.histogram2d(
    x,
    y,
    bins=10,
    range=None,
    density=False,
    weights=None
) -> tuple[ndarray, ndarray, ndarray]
```

## Valor de retorno

Devuelve `(H, xedges, yedges)`: cuenta cuántos pares `(x, y)` caen en cada celda de una rejilla 2D. Versión 2D de [[np.histogram]].

| Salida | Shape | Contenido |
|--------|-------|-----------|
| `H` | `(nx, ny)` | conteo por celda |
| `xedges` | `(nx+1,)` | bordes en X |
| `yedges` | `(ny+1,)` | bordes en Y |

```python
import numpy as np
x = np.random.rand(1000)
y = np.random.rand(1000)
H, xe, ye = np.histogram2d(x, y, bins=20)
# H.shape == (20, 20)
```

## Parámetros en detalle

### `x`, `y` — coordenadas

Dos arrays 1D de la misma longitud (un par por elemento).

### `bins` — número o bordes

Entero (igual en ambos ejes), `[nx, ny]`, o secuencias de bordes.

### `density`, `weights`

Como en [[np.histogram]].

## Casos de uso

### Mapa de densidad de puntos

```python
H, xe, ye = np.histogram2d(lon, lat, bins=50)
# graficar con plt.imshow(H.T, origin='lower')
```

## Buenas prácticas

1. Al graficar con `imshow`, suele hacer falta transponer `H` y `origin='lower'`.
2. Para más de 2 dimensiones, usa [[np.histogramdd]].

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| Imagen "girada" | orientación de `H` | usar `H.T` y `origin='lower'` |
| `x` e `y` de distinto largo | deben emparejarse | igualar longitudes |

## Limitaciones

- Exactamente 2D; para ND ver [[np.histogramdd]].

## Notas relacionadas

- [[concepto_shape]]
- [[np.histogram]]
- [[np.histogramdd]]
