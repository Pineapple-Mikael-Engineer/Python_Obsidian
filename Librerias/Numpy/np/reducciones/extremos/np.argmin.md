---
title: np.argmin — Posición del valor mínimo
aliases:
  - argmin
  - np.argmin
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

# np.argmin — Posición del valor mínimo

## Firma de la función

```python
np.argmin(
    a,
    axis=None,
    out=None,
    keepdims=False
) -> ndarray | int
```

## Valor de retorno

Devuelve el **índice** del mínimo a lo largo del [[concepto_axis_parametro|eje]]. Contraparte de [[np.argmax]]. Con `axis=None`, índice en el array aplanado.

| Entrada | `axis` | Salida |
|---------|--------|--------|
| `[3, 1, 9, 2]` | `None` | `1` (posición del 1) |
| `(2, 3)` | `1` | índice de columna del mínimo por fila |

```python
import numpy as np
np.argmin([3, 1, 9, 2])   # 1
M = np.array([[1, 9, 3],
              [7, 2, 8]])
np.argmin(M, axis=1)      # [0, 1]
```

## Parámetros en detalle

### `axis` y empates

Igual que [[np.argmax]]: `None` aplana; en empate devuelve el **primer** índice.

## Casos de uso

### Vecino más cercano (mínima distancia)

```python
distancias = np.linalg.norm(puntos - query, axis=1)
mas_cercano = np.argmin(distancias)
```

### Época con menor pérdida

```python
mejor_epoca = np.argmin(historial_loss)
```

## Buenas prácticas

1. Para el **valor**, usa [[np.min]]; `argmin` da la posición.
2. Con NaN, usa [[np.nanargmin]].
3. En 2D+ con `axis=None`, traduce con `np.unravel_index`.

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| Apunta a NaN | NaN se trata como menor en algunas rutas | [[np.nanargmin]] |
| Índice aplanado inesperado | `axis=None` en 2D | `np.unravel_index` |

## Limitaciones

- Solo el primer mínimo en empate; no fiable con NaN.

## Notas relacionadas

- [[concepto_axis_parametro]]
- [[concepto_indexing]]
- [[np.argmax]]
- [[np.min]]
- [[np.nanargmin]]
