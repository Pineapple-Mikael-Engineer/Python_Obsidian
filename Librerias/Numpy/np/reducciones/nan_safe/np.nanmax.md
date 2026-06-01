---
title: np.nanmax — Máximo ignorando NaN
aliases:
  - nanmax
  - np.nanmax
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

# np.nanmax — Máximo ignorando NaN

## Firma de la función

```python
np.nanmax(
    a,
    axis=None,
    out=None,
    keepdims=False
) -> ndarray | escalar
```

## Valor de retorno

Versión de [[np.max]] que **ignora los `NaN`**. Mientras `np.max` propaga NaN (el NaN "gana"), `nanmax` devuelve el mayor de los valores válidos.

| Entrada | `np.max` | `np.nanmax` |
|---------|----------|-------------|
| `[1, nan, 9, 2]` | `nan` | `9.0` |

```python
import numpy as np
np.nanmax([1, np.nan, 9, 2])   # 9.0
```

## Parámetros en detalle

Igual que [[np.max]]: `axis` colapsa el [[concepto_axis_parametro|eje]], `keepdims` lo conserva.

## Casos de uso

### Pico ignorando huecos

```python
np.nanmax(señal_con_huecos)
```

## Buenas prácticas

1. Para la **posición** del máximo válido, usa [[np.nanargmax]].
2. Un eje todo-NaN devuelve NaN con `RuntimeWarning`.

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| `RuntimeWarning: All-NaN slice` | eje todo NaN | filtrar o aceptar NaN |

## Limitaciones

- Si todo el eje es NaN, devuelve NaN.

## Notas relacionadas

- [[concepto_axis_parametro]]
- [[np.max]]
- [[np.nanmin]]
- [[np.nanargmax]]
