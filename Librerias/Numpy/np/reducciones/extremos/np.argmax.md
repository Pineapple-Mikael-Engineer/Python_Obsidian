---
title: np.argmax — Posición del valor máximo
aliases:
  - argmax
  - np.argmax
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

# np.argmax — Posición del valor máximo

## Firma de la función

```python
np.argmax(
    a,
    axis=None,
    out=None,
    keepdims=False
) -> ndarray | int
```

## Valor de retorno

Devuelve el **índice** (no el valor) del máximo a lo largo del [[concepto_axis_parametro|eje]]. Con `axis=None`, el índice en la versión **aplanada** del array.

| Entrada | `axis` | Salida |
|---------|--------|--------|
| `[3, 1, 9, 2]` | `None` | `2` (posición del 9) |
| `(2, 3)` | `0` | índice de fila del máximo por columna |
| `(2, 3)` | `1` | índice de columna del máximo por fila |

```python
import numpy as np
np.argmax([3, 1, 9, 2])   # 2
M = np.array([[1, 9, 3],
              [7, 2, 8]])
np.argmax(M, axis=1)      # [1, 2]  → col del máximo en cada fila
```

## Recuperar el valor desde el índice

```python
arr = np.array([3, 1, 9, 2])
i = np.argmax(arr)
arr[i]   # 9
```

Para `axis=None` en arrays 2D+, convierte el índice plano con `np.unravel_index`:

```python
plano = np.argmax(M)                    # índice en el array aplanado
fila, col = np.unravel_index(plano, M.shape)
```

## Parámetros en detalle

### `axis` — eje de búsqueda

Si es `None`, busca en todo el array aplanado. Con entero, devuelve índices a lo largo de ese eje.

### Empates

Si hay varios máximos, devuelve el **primer** índice donde aparece.

## Casos de uso

### Clase predicha (clasificación)

```python
logits = np.array([0.1, 0.7, 0.2])
clase = np.argmax(logits)   # 1
```

### Posición del pico de una señal

```python
indice_pico = np.argmax(señal)
```

## Buenas prácticas

1. Si quieres el **valor**, usa [[np.max]]; `argmax` da la **posición**.
2. Con NaN presente, el resultado es poco fiable; usa [[np.nanargmax]].
3. Para índices 2D+ con `axis=None`, usa `np.unravel_index`.

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| Índice "raro" en 2D | con `axis=None` es índice aplanado | `np.unravel_index` |
| Apunta a un NaN | NaN se considera el mayor | [[np.nanargmax]] |
| Se esperaba el valor | `argmax` da el índice | indexar `a[argmax]` o usar [[np.max]] |

## Limitaciones

- Solo el primer máximo en caso de empate.
- No es fiable con NaN.

## Notas relacionadas

- [[concepto_axis_parametro]]
- [[concepto_indexing]]
- [[np.argmin]]
- [[np.max]]
- [[np.nanargmax]]
