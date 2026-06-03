---
title: np.vstack — Apilar arrays verticalmente (por filas)
aliases:
  - vstack
  - np.vstack
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

# np.vstack — Apilar arrays verticalmente (por filas)

## Firma de la función

```python
np.vstack(tup) -> ndarray
```

## Valor de retorno

Devuelve un nuevo array apilando la secuencia **a lo largo del eje 0** (filas). Es un atajo de [[np.concatenate]] con `axis=0`, pero promueve antes los arrays 1D a 2D (los trata como filas).

| Entrada | Shapes | Salida |
|---------|--------|--------|
| dos `(3,)` | 1D | `(2, 3)` |
| `(2, 3)` y `(1, 3)` | 2D | `(3, 3)` |

```python
import numpy as np
a = np.array([1, 2, 3])
b = np.array([4, 5, 6])
np.vstack((a, b))
# array([[1, 2, 3],
#        [4, 5, 6]])      # (2, 3)
```

## Equivalencias

```python
np.vstack((a, b))                      # cómodo
np.concatenate((a, b), axis=0)         # si ya son 2D
np.stack((a, b), axis=0)               # si quieres forzar eje nuevo desde 1D
```

A diferencia de `concatenate`, `vstack` **convierte 1D en filas** automáticamente: `(3,)` → `(1, 3)`.

## Parámetros en detalle

### `tup` — secuencia de arrays

Tupla o lista. Deben coincidir en todas las dimensiones **salvo la primera** (tras la promoción a 2D).

## Casos de uso

### Apilar filas de observaciones

```python
filas = [np.random.rand(4) for _ in range(5)]
matriz = np.vstack(filas)      # (5, 4)
```

### Añadir una fila a una matriz

```python
M = np.ones((3, 4))
nueva = np.zeros(4)
M = np.vstack((M, nueva))      # (4, 4)
```

## Buenas prácticas

1. Úsalo para crecer "hacia abajo" (más filas); para "a lo ancho" usa [[np.hstack]].
2. Como cualquier apilado en bucle es costoso: acumula en lista y llama una sola vez.
3. Si controlas el `ndim` y no quieres promoción automática, prefiere [[np.concatenate]].

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| `dimensions ... must match exactly` | nº de columnas distinto | igualar la última dimensión |
| Forma inesperada con escalares | se pasaron 0D | usar `np.atleast_2d` |

## Limitaciones

- Fija el eje de unión en 0; para otros ejes usa [[np.concatenate]].
- Siempre copia.

## Notas relacionadas

- [[concepto_shape]]
- [[np.concatenate]]
- [[np.hstack]]
- [[np.stack]]
