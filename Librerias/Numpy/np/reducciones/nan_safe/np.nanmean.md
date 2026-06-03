---
title: np.nanmean — Media ignorando NaN
aliases:
  - nanmean
  - np.nanmean
tags:
  - numpy
  - api/funcion
  - estadistica

# --- Clasificación ---
lib: numpy
mod: np
tipo: funcion

# --- Comportamiento ---
retorna: ndarray o escalar
inplace: false

# --- Dependencias ---
requiere:
  - concepto_axis_parametro

draft: false
---

# np.nanmean — Media ignorando NaN

## Firma de la función

```python
np.nanmean(
    a,
    axis=None,
    dtype=None,
    out=None,
    keepdims=False
) -> ndarray | escalar
```

## Valor de retorno

Versión de [[np.mean]] que **excluye los `NaN`**: promedia solo los valores válidos (divide por el número de no-NaN, no por el total).

| Entrada | `np.mean` | `np.nanmean` |
|---------|-----------|--------------|
| `[1, 2, nan, 5]` | `nan` | `2.667` (media de 1,2,5) |

```python
import numpy as np
np.nanmean([1, 2, np.nan, 5])   # 2.6667
```

## Parámetros en detalle

Igual que [[np.mean]]: `axis` colapsa el [[concepto_axis_parametro|eje]], `keepdims` lo conserva.

## Casos de uso

### Promedio de sensores con lecturas faltantes

```python
lecturas = np.array([[20.1, np.nan], [21.0, 19.8]])
np.nanmean(lecturas, axis=0)   # [20.55, 19.8]
```

## Buenas prácticas

1. Es la forma correcta de promediar datos con huecos sin sesgar por NaN.
2. Un eje **todo NaN** devuelve NaN y emite un `RuntimeWarning`.

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| `RuntimeWarning: Mean of empty slice` | eje completamente NaN | filtrar esos ejes o aceptar el NaN |

## Limitaciones

- Si todos los valores de un eje son NaN, el resultado es NaN (con warning).

## Notas relacionadas

- [[concepto_axis_parametro]]
- [[np.mean]]
- [[np.nansum]]
- [[np.nanstd]]
