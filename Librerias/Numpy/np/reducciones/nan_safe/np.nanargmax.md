---
title: np.nanargmax — Posición del máximo ignorando NaN
aliases:
  - nanargmax
  - np.nanargmax
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

# np.nanargmax — Posición del máximo ignorando NaN

## Firma de la función

```python
np.nanargmax(
    a,
    axis=None,
    out=None,
    keepdims=False
) -> ndarray | int
```

## Valor de retorno

Versión de [[np.argmax]] que **ignora los `NaN`**: devuelve el índice del valor máximo entre los válidos. Mientras `np.argmax` podría apuntar a un NaN, `nanargmax` no.

| Entrada | `np.argmax` | `np.nanargmax` |
|---------|-------------|----------------|
| `[1, nan, 9, 2]` | `1` (el NaN) | `2` (el 9) |

```python
import numpy as np
np.nanargmax([1, np.nan, 9, 2])   # 2
```

## Parámetros en detalle

Igual que [[np.argmax]]: `axis` (ver [[concepto_axis_parametro]]); el índice referencia el array original (ver [[concepto_indexing]]).

## Casos de uso

### Clase predicha tolerando NaN en logits

```python
clase = np.nanargmax(logits)
```

## Buenas prácticas

1. Para el **valor**, usa [[np.nanmax]].
2. Si un eje es **todo NaN**, lanza `ValueError` (no hay máximo válido).

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| `ValueError: All-NaN slice encountered` | eje completamente NaN | filtrar esos ejes antes |

## Limitaciones

- A diferencia de `nanmax` (que devuelve NaN), un eje todo-NaN aquí **lanza error**.

## Notas relacionadas

- [[concepto_axis_parametro]]
- [[concepto_indexing]]
- [[np.argmax]]
- [[np.nanmax]]
- [[np.nanargmin]]
