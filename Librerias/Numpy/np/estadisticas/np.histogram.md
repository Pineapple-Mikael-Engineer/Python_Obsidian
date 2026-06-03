---
title: np.histogram — Conteo de valores en intervalos (bins)
aliases:
  - histogram
  - np.histogram
  - histograma
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

# np.histogram — Conteo de valores en intervalos (bins)

## Firma de la función

```python
np.histogram(
    a,
    bins=10,
    range=None,
    density=False,
    weights=None
) -> tuple[ndarray, ndarray]
```

## Valor de retorno

Devuelve una **tupla** `(hist, bin_edges)`: el conteo por intervalo y los bordes de los intervalos. Calcula el histograma pero **no lo dibuja** (para graficar, `plt.hist` o `plt.bar`).

| Salida | Longitud | Contenido |
|--------|----------|-----------|
| `hist` | `n_bins` | nº de valores en cada bin |
| `bin_edges` | `n_bins + 1` | bordes de los bins |

```python
import numpy as np
datos = np.array([1, 2, 1, 3, 5, 2, 1])
hist, edges = np.histogram(datos, bins=4)
# hist  = [3, 2, 1, 1]
# edges = [1., 2., 3., 4., 5.]
```

## Parámetros en detalle

### `bins` — número o bordes

| Tipo | Significado |
|------|-------------|
| entero | nº de bins iguales (por defecto 10) |
| secuencia | bordes explícitos `[0, 1, 5, 10]` |
| string | regla automática (`'auto'`, `'sturges'`, `'fd'`...) |

### `range` — rango a considerar

Tupla `(min, max)`; ignora valores fuera.

### `density` — normalizar

Si `True`, devuelve la **densidad de probabilidad** (el área integra 1) en vez de conteos.

### `weights` — pesos por valor

Cada valor aporta su peso al bin en lugar de 1.

## Casos de uso

### Distribución de datos

```python
hist, edges = np.histogram(muestras, bins='auto', density=True)
centros = (edges[:-1] + edges[1:]) / 2
```

## Buenas prácticas

1. `bin_edges` tiene **un elemento más** que `hist`: usa los centros para graficar.
2. `bins='auto'` elige un número razonable de bins automáticamente.
3. Para asignar cada valor a su bin, usa [[np.digitize]].
4. Para enteros no negativos contados directamente, [[np.bincount]] es más simple.

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| Desfase al graficar | `edges` tiene N+1 elementos | usar centros `(edges[:-1]+edges[1:])/2` |
| Esperar un array | devuelve **tupla** | desempaquetar `hist, edges = ...` |

## Limitaciones

- No grafica; solo cuenta.
- Solo 1D (para 2D/ND ver [[np.histogram2d]] / [[np.histogramdd]]).

## Notas relacionadas

- [[concepto_shape]]
- [[np.histogram2d]]
- [[np.bincount]]
- [[np.digitize]]
- [[np.percentile]]
