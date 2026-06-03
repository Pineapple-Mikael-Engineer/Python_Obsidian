---
title: np.nanmin — Mínimo ignorando NaN
aliases:
  - nanmin
  - np.nanmin
tags:
  - numpy
  - api/funcion
  - reducciones

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

# np.nanmin — Mínimo ignorando NaN

## Firma de la función

```python
np.nanmin(
    a,
    axis=None,
    out=None,
    keepdims=False
) -> ndarray | escalar
```

## Valor de retorno

Versión de [[np.min]] que **ignora los `NaN`**, devolviendo el menor de los valores válidos.

| Entrada | `np.min` | `np.nanmin` |
|---------|----------|-------------|
| `[3, nan, 1, 2]` | `nan` | `1.0` |

```python
import numpy as np
np.nanmin([3, np.nan, 1, 2])   # 1.0
```

## Parámetros en detalle

Igual que [[np.min]]: `axis` (ver [[concepto_axis_parametro]]), `keepdims`.

## Casos de uso

### Suelo de los datos tolerando huecos

```python
np.nanmin(matriz, axis=0)
```

## Buenas prácticas

1. Para la **posición** del mínimo válido, usa [[np.nanargmin]].
2. Un eje todo-NaN devuelve NaN con warning.

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| `RuntimeWarning: All-NaN slice` | eje todo NaN | filtrar |

## Limitaciones

- Eje todo NaN → NaN.

## Notas relacionadas

- [[concepto_axis_parametro]]
- [[np.min]]
- [[np.nanmax]]
- [[np.nanargmin]]
