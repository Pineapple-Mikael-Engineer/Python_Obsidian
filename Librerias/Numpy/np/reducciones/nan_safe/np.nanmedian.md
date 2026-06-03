---
title: np.nanmedian — Mediana ignorando NaN
aliases:
  - nanmedian
  - np.nanmedian
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

# np.nanmedian — Mediana ignorando NaN

## Firma de la función

```python
np.nanmedian(
    a,
    axis=None,
    out=None,
    overwrite_input=False,
    keepdims=False
) -> ndarray | escalar
```

## Valor de retorno

Versión de [[np.median]] que **excluye los `NaN`** antes de calcular el valor central. Combina robustez frente a outliers **y** tolerancia a datos faltantes.

| Entrada | `np.median` | `np.nanmedian` |
|---------|-------------|----------------|
| `[1, nan, 3, 100]` | `nan` | `3.0` |

```python
import numpy as np
np.nanmedian([1, np.nan, 3, 100])   # 3.0
```

## Parámetros en detalle

Igual que [[np.median]]: `axis`, `keepdims`, y `overwrite_input` para ahorrar memoria (destruye `a`).

## Casos de uso

### Resumen robusto de datos sucios

```python
datos = np.array([30, np.nan, 32, 500, 31])
np.nanmedian(datos)   # 31.0  (robusto a outlier y NaN)
```

## Buenas prácticas

1. La mejor opción cuando hay **outliers y NaN** a la vez.
2. Un eje todo-NaN devuelve NaN con warning.

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| `RuntimeWarning: All-NaN slice` | eje todo NaN | filtrar o aceptar NaN |

## Limitaciones

- Requiere ordenar (coste mayor que la media).

## Notas relacionadas

- [[concepto_axis_parametro]]
- [[np.median]]
- [[np.nanmean]]
