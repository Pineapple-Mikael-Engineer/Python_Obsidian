---
title: ndarray.argmin — Posición del valor mínimo a lo largo de un eje
aliases:
  - argmin
  - ndarray.argmin
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

# ndarray.argmin — Posición del valor mínimo a lo largo de un eje

## Firma del método

```python
ndarray.argmin(
    axis=None,
    out=None,
    keepdims=False
) -> int | ndarray
```

## Valor de retorno

| Entrada (`self`) | `axis` | Retorno |
|------------------|--------|---------|
| `[3, 1, 9, 2]` | `None` | `1` (índice del 1) |
| shape `(2, 3)` | `0` | índice de fila del mínimo por columna |
| shape `(2, 3)` | `1` | índice de columna del mínimo por fila |

Devuelve el **índice** (no el valor) del mínimo. Con `axis=None`, el índice en la versión **aplanada** de `self`.

```python
import numpy as np
a = np.array([3, 1, 9, 2])
a.argmin()   # 1
```

## Equivalencia con np.argmin

`a.argmin(...)` es la forma "bound" de [[np.argmin]]: `np.argmin(a, ...)`. Misma semántica de `axis` y `keepdims`, idéntico resultado. La forma de método encadena de forma fluida; la funcional acepta como primer argumento cualquier `array_like` (listas), no solo un `ndarray` ya construido.

## Parámetros en detalle

### `axis` — eje de búsqueda

`None` busca en todo `self` aplanado. Con entero, devuelve índices a lo largo de ese eje.

```python
M = np.array([[1, 9, 3],
              [7, 2, 8]])
M.argmin(axis=1)   # [0, 1]   → col del mínimo en cada fila
```

### Empates

Si hay varios mínimos, devuelve el **primer** índice donde aparece.

### Recuperar el valor / índice 2D

Para `axis=None` en arrays 2D+, convierte el índice plano con `np.unravel_index`:

```python
plano = M.argmin()                       # índice en el array aplanado
fila, col = np.unravel_index(plano, M.shape)
```

## Casos de uso

### Posición del valle de una señal

```python
indice_valle = señal.argmin()
```

### Categoría de menor coste

```python
costes = np.array([0.8, 0.3, 0.5])
elegida = costes.argmin()   # 1
```

## Buenas prácticas

1. Si quieres el **valor**, usa `self.min()`; `.argmin` da la **posición**.
2. Con NaN presente el resultado es poco fiable; usa [[np.nanargmin]].
3. Para índices 2D+ con `axis=None`, usa `np.unravel_index`.

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| Índice "raro" en 2D | con `axis=None` es índice aplanado | `np.unravel_index` |
| Apunta a un NaN | NaN distorsiona la comparación | [[np.nanargmin]] |
| Se esperaba el valor | `.argmin` da el índice | indexar `self[idx]` o `self.min()` |

## Notas relacionadas

- [[np.argmin]]
- [[concepto_axis_parametro]]
- [[ndarray.argmax]]
- [[ndarray.min]]
- [[np.nanargmin]]
