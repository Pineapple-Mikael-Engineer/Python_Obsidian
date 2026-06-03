---
title: np.dstack — Apilar arrays en profundidad (eje 2)
aliases:
  - dstack
  - np.dstack
tags:
  - numpy
  - api/funcion
  - manipulacion

# --- Clasificación ---
lib: numpy
mod: np
tipo: funcion

# --- Comportamiento ---
retorna: ndarray
inplace: false

# --- Dependencias ---
requiere:
  - concepto_shape

draft: false
---

# np.dstack — Apilar arrays en profundidad (eje 2)

## Firma de la función

```python
np.dstack(tup) -> ndarray
```

## Valor de retorno

Devuelve un array apilando la secuencia a lo largo del **tercer eje** (profundidad, `axis=2`). Promueve antes los arrays a 3D. Atajo de [[np.concatenate]] sobre el eje 2.

| Entrada | Shapes | Salida |
|---------|--------|--------|
| dos `(2, 3)` | 2D | `(2, 3, 2)` |
| dos `(3,)` | 1D | `(1, 3, 2)` |

```python
import numpy as np
a = np.array([[1, 2], [3, 4]])
b = np.array([[5, 6], [7, 8]])
np.dstack((a, b)).shape   # (2, 2, 2)
```

## Parámetros en detalle

### `tup` — secuencia de arrays

Tupla o lista; deben coincidir en filas y columnas (se unen en profundidad).

## Casos de uso

### Componer canales de color en una imagen

```python
r = np.zeros((100, 100))
g = np.ones((100, 100))
b = np.zeros((100, 100))
rgb = np.dstack((r, g, b))      # (100, 100, 3)
```

### Apilar mapas 2D como capas

```python
capas = np.dstack([capa1, capa2, capa3])   # (H, W, 3)
```

## Buenas prácticas

1. Equivale a `np.stack(..., axis=-1)` cuando las entradas son 2D del mismo shape.
2. Para canales de imagen, suele ser más legible que `stack` o `concatenate`.
3. Verifica que filas y columnas coinciden entre todas las entradas.

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| `dimensions must match` | filas/columnas distintas | igualar los dos primeros ejes |
| Forma con eje extra inesperado | confundir con `hstack` | recordar que une en profundidad (eje 2) |

## Limitaciones

- Fija el eje de unión en 2; para otros ejes, [[np.stack]] / [[np.concatenate]].

## Notas relacionadas

- [[concepto_shape]]
- [[np.stack]]
- [[np.concatenate]]
- [[np.column_stack]]
