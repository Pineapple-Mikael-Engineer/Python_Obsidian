---
title: np.nanstd — Desviación estándar ignorando NaN
aliases:
  - nanstd
  - np.nanstd
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

# np.nanstd — Desviación estándar ignorando NaN

## Firma de la función

```python
np.nanstd(
    a,
    axis=None,
    dtype=None,
    out=None,
    ddof=0,
    keepdims=False
) -> ndarray | escalar
```

## Valor de retorno

Versión de [[np.std]] que **excluye los `NaN`** del cálculo de dispersión.

| Entrada | `np.std` | `np.nanstd` |
|---------|----------|-------------|
| `[2, 4, nan, 6]` | `nan` | dispersión de 2,4,6 |

```python
import numpy as np
np.nanstd([2, 4, np.nan, 6])   # 1.633
```

## Parámetros en detalle

Igual que [[np.std]], incluido **`ddof`** (0 = poblacional, 1 = muestral) y `axis` (ver [[concepto_axis_parametro]]).

## Casos de uso

### Dispersión por feature con datos faltantes

```python
desv = np.nanstd(matriz, axis=0, ddof=1)
```

## Buenas prácticas

1. Recuerda `ddof=1` para desviación muestral.
2. Un eje todo-NaN devuelve NaN con warning.

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| Valor distinto al esperado | `ddof` por defecto 0 | usar `ddof=1` |
| `RuntimeWarning` | eje todo NaN | filtrar |

## Limitaciones

- Si todo el eje es NaN, el resultado es NaN.

## Notas relacionadas

- [[concepto_axis_parametro]]
- [[np.std]]
- [[np.nanvar]]
- [[np.nanmean]]
