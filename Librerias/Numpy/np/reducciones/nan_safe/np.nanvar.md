---
title: np.nanvar — Varianza ignorando NaN
aliases:
  - nanvar
  - np.nanvar
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

# np.nanvar — Varianza ignorando NaN

## Firma de la función

```python
np.nanvar(
    a,
    axis=None,
    dtype=None,
    out=None,
    ddof=0,
    keepdims=False
) -> ndarray | escalar
```

## Valor de retorno

Versión de [[np.var]] que **excluye los `NaN`**. Es el cuadrado de [[np.nanstd]].

| Entrada | `np.var` | `np.nanvar` |
|---------|----------|-------------|
| `[2, 4, nan, 6]` | `nan` | varianza de 2,4,6 |

```python
import numpy as np
np.nanvar([2, 4, np.nan, 6])   # 2.667
```

## Parámetros en detalle

Igual que [[np.var]]: `ddof` (0 poblacional, 1 muestral) y `axis` (ver [[concepto_axis_parametro]]).

## Casos de uso

### Filtrar features sin variación tolerando huecos

```python
v = np.nanvar(datos, axis=0)
constantes = v == 0
```

## Buenas prácticas

1. Para unidades originales, usa [[np.nanstd]].
2. Elige `ddof=1` para varianza muestral.

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| Magnitud al cuadrado "rara" | varianza vs desviación | usar [[np.nanstd]] |
| `RuntimeWarning` | eje todo NaN | filtrar |

## Limitaciones

- Unidades al cuadrado; NaN total → NaN.

## Notas relacionadas

- [[concepto_axis_parametro]]
- [[np.var]]
- [[np.nanstd]]
