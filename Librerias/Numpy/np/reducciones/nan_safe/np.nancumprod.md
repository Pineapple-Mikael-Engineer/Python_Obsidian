---
title: np.nancumprod — Producto acumulado ignorando NaN
aliases:
  - nancumprod
  - np.nancumprod
tags:
  - numpy
  - api/funcion
  - reducciones

# --- Clasificación ---
lib: numpy
mod: np
tipo: funcion

# --- Comportamiento ---
retorna: ndarray
inplace: false

# --- Dependencias ---
requiere:
  - concepto_axis_parametro

draft: false
---

# np.nancumprod — Producto acumulado ignorando NaN

## Firma de la función

```python
np.nancumprod(
    a,
    axis=None,
    dtype=None,
    out=None
) -> ndarray
```

## Valor de retorno

Versión de [[np.cumprod]] que **trata los `NaN` como 1**: la acumulación multiplicativa continúa sin romperse en los huecos.

| Entrada | `np.cumprod` | `np.nancumprod` |
|---------|--------------|-----------------|
| `[2, nan, 3]` | `[2, nan, nan]` | `[2, 2, 6]` |

```python
import numpy as np
np.nancumprod([2, np.nan, 3])   # array([2., 2., 6.])
```

## Parámetros en detalle

Igual que [[np.cumprod]]: `axis` define el eje (ver [[concepto_axis_parametro]]); vigilar overflow con `dtype`.

## Casos de uso

### Factor compuesto con periodos faltantes

```python
tasas = np.array([1.05, np.nan, 1.04])
np.nancumprod(tasas)   # [1.05, 1.05, 1.092]
```

## Buenas prácticas

1. Mantiene la longitud; NaN se trata como factor 1.
2. Vigila el **overflow** como en [[np.cumprod]].

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| Overflow | crecimiento multiplicativo | `dtype` amplio |

## Limitaciones

- En la posición del NaN se muestra el producto corriente previo (NaN tratado como 1).

## Notas relacionadas

- [[concepto_axis_parametro]]
- [[np.cumprod]]
- [[np.nancumsum]]
- [[np.nanprod]]
