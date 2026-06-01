---
title: np.nanargmin — Posición del mínimo ignorando NaN
aliases:
  - nanargmin
  - np.nanargmin
tags:
  - numpy
  - api/funcion
  - reducciones

# --- Clasificación ---
lib: numpy
mod: np
tipo: funcion

# --- Comportamiento ---
retorna: ndarray o int
inplace: false

# --- Dependencias ---
requiere:
  - concepto_axis_parametro
  - concepto_indexing

draft: false
---

# np.nanargmin — Posición del mínimo ignorando NaN

## Firma de la función

```python
np.nanargmin(
    a,
    axis=None,
    out=None,
    keepdims=False
) -> ndarray | int
```

## Valor de retorno

Versión de [[np.argmin]] que **ignora los `NaN`**: devuelve el índice del valor mínimo entre los válidos.

| Entrada | `np.argmin` | `np.nanargmin` |
|---------|-------------|----------------|
| `[nan, 5, 1, 3]` | `0` (el NaN) | `2` (el 1) |

```python
import numpy as np
np.nanargmin([np.nan, 5, 1, 3])   # 2
```

## Parámetros en detalle

Igual que [[np.argmin]]: `axis` (ver [[concepto_axis_parametro]]); el índice referencia el array original (ver [[concepto_indexing]]).

## Casos de uso

### Vecino más cercano tolerando distancias NaN

```python
mas_cercano = np.nanargmin(distancias)
```

## Buenas prácticas

1. Para el **valor**, usa [[np.nanmin]].
2. Un eje **todo NaN** lanza `ValueError`.

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| `ValueError: All-NaN slice encountered` | eje completamente NaN | filtrar antes |

## Limitaciones

- Eje todo-NaN → `ValueError` (a diferencia de `nanmin`, que da NaN).

## Notas relacionadas

- [[concepto_axis_parametro]]
- [[concepto_indexing]]
- [[np.argmin]]
- [[np.nanmin]]
- [[np.nanargmax]]
