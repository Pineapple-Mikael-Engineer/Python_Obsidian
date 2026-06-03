---
title: ndarray.swapaxes — Intercambiar dos ejes (método)
aliases:
  - swapaxes
  - ndarray.swapaxes
tags:
  - numpy
  - api/metodo
  - shape
lib: numpy
obj: ndarray
tipo: metodo
retorna: ndarray
inplace: false
draft: false
---

# ndarray.swapaxes — Intercambiar dos ejes (método)

## Firma del método

```python
ndarray.swapaxes(axis1, axis2) -> ndarray
```

## Valor de retorno

Devuelve una [[concepto_views_vs_copias|vista]] con los ejes `axis1` y `axis2` intercambiados; el resto conserva su posición. **No copia datos**: solo reordena `strides`.

| Shape entrada | Llamada | Shape salida |
|---------------|---------|--------------|
| `(2, 3)` | `arr.swapaxes(0, 1)` | `(3, 2)` |
| `(2, 3, 4)` | `arr.swapaxes(0, 2)` | `(4, 3, 2)` |
| `(2, 3, 4)` | `arr.swapaxes(1, 2)` | `(2, 4, 3)` |

## Equivalencia con np.swapaxes

Versión "bound" de la función: `arr.swapaxes(i, j) == np.swapaxes(arr, i, j)`. Ver [[np.swapaxes]].

```python
arr.swapaxes(1, 2)        # método
np.swapaxes(arr, 1, 2)    # función → mismo resultado
```

## Parámetros en detalle

`axis1`, `axis2` son los dos ejes a intercambiar. Aceptan índices negativos (cuentan desde el final). Frente a `transpose`, swapaxes solo toca **dos** ejes, lo que lo hace más expresivo cuando esa es la intención:

```python
T = np.ones((2, 3, 4))
T.swapaxes(1, 2).shape           # (2, 4, 3)
T.transpose(0, 2, 1).shape       # (2, 4, 3) — equivalente, menos legible
T.swapaxes(-1, -2).shape         # (2, 4, 3) — ejes negativos
```

## Casos de uso

```python
# Intercambiar las dos últimas dimensiones de un batch de matrices:
batch = np.random.rand(10, 4, 5)
batch.swapaxes(-1, -2).shape     # (10, 5, 4)

# Equivalente a transponer una matriz 2D:
M = np.arange(6).reshape(2, 3)
M.swapaxes(0, 1)                 # == M.T
```

## Buenas prácticas

1. Úsalo cuando solo intercambias **dos** ejes: comunica mejor que `transpose`.
2. Usa índices negativos para operar sobre los últimos ejes de un batch.
3. Es una vista: escribir en el resultado modifica el original.

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| `AxisError: axis N is out of bounds` | `axis1`/`axis2` fuera de rango | usar índice válido (incluido negativo) |
| Resultado no contiguo rompe otra función | vista con strides reordenados | `np.ascontiguousarray(resultado)` |

## Notas relacionadas

- [[np.swapaxes]]
- [[ndarray.transpose]]
- [[concepto_views_vs_copias]]
- [[concepto_shape]]
