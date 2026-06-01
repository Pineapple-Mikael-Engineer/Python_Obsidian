---
title: ndarray.argmax — Posición del valor máximo a lo largo de un eje
aliases:
  - argmax
  - ndarray.argmax
tags:
  - numpy
  - api/metodo
  - reducciones
lib: numpy
obj: ndarray
tipo: metodo
retorna: int o ndarray
inplace: false
draft: false
---

# ndarray.argmax — Posición del valor máximo a lo largo de un eje

## Firma del método

```python
ndarray.argmax(
    axis=None,
    out=None,
    keepdims=False
) -> int | ndarray
```

## Valor de retorno

| Entrada (`self`) | `axis` | Retorno |
|------------------|--------|---------|
| `[3, 1, 9, 2]` | `None` | `2` (índice del 9) |
| shape `(2, 3)` | `0` | índice de fila del máximo por columna |
| shape `(2, 3)` | `1` | índice de columna del máximo por fila |

Devuelve el **índice** (no el valor) del máximo. Con `axis=None`, el índice en la versión **aplanada** de `self`.

```python
import numpy as np
a = np.array([3, 1, 9, 2])
a.argmax()   # 2
```

## Equivalencia con np.argmax

`a.argmax(...)` es la forma "bound" de [[np.argmax]]: `np.argmax(a, ...)`. Misma semántica de `axis` y `keepdims`, idéntico resultado. La forma de método encadena de forma fluida; la funcional acepta como primer argumento cualquier `array_like` (listas), no solo un `ndarray` ya construido.

## Parámetros en detalle

### `axis` — eje de búsqueda

`None` busca en todo `self` aplanado. Con entero, devuelve índices a lo largo de ese eje.

```python
M = np.array([[1, 9, 3],
              [7, 2, 8]])
M.argmax(axis=1)   # [1, 2]   → col del máximo en cada fila
```

### Empates

Si hay varios máximos, devuelve el **primer** índice donde aparece.

### Recuperar el valor / índice 2D

Para `axis=None` en arrays 2D+, convierte el índice plano con `np.unravel_index`:

```python
plano = M.argmax()                       # índice en el array aplanado
fila, col = np.unravel_index(plano, M.shape)
```

## Casos de uso

### Clase predicha (clasificación)

```python
logits = np.array([0.1, 0.7, 0.2])
clase = logits.argmax()   # 1
```

### Posición del pico de una señal

```python
indice_pico = señal.argmax()
```

## Buenas prácticas

1. Si quieres el **valor**, usa `self.max()`; `.argmax` da la **posición**.
2. Con NaN presente el resultado es poco fiable; usa [[np.nanargmax]].
3. Para índices 2D+ con `axis=None`, usa `np.unravel_index`.

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| Índice "raro" en 2D | con `axis=None` es índice aplanado | `np.unravel_index` |
| Apunta a un NaN | NaN se considera el mayor | [[np.nanargmax]] |
| Se esperaba el valor | `.argmax` da el índice | indexar `self[idx]` o `self.max()` |

## Notas relacionadas

- [[np.argmax]]
- [[concepto_axis_parametro]]
- [[ndarray.argmin]]
- [[ndarray.max]]
- [[np.nanargmax]]
