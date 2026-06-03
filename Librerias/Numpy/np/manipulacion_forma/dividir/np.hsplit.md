---
title: np.hsplit — Dividir por columnas (eje 1)
aliases:
  - hsplit
  - np.hsplit
tags:
  - numpy
  - api/funcion
  - manipulacion

# --- Clasificación ---
lib: numpy
mod: np
tipo: funcion

# --- Comportamiento ---
retorna: list
inplace: false

# --- Dependencias ---
requiere:
  - concepto_shape

draft: false
---

# np.hsplit — Dividir por columnas (eje 1)

## Firma de la función

```python
np.hsplit(
    ary,
    indices_or_sections
) -> list[ndarray]
```

## Valor de retorno

Devuelve una lista de sub-arrays cortando `ary` **horizontalmente** (eje 1, columnas) en 2D+, o en el eje 0 si el array es 1D. Atajo de [[np.split]]. Inverso de [[np.hstack]].

| Entrada | `indices_or_sections` | Salida |
|---------|------------------------|--------|
| `(4, 6)` | `3` | 3 arrays de `(4, 2)` |
| `(4, 6)` | `[2, 4]` | `(4,2)`, `(4,2)`, `(4,2)` |
| `(6,)` | `2` | 2 arrays de `(3,)` |

```python
import numpy as np
M = np.arange(12).reshape(3, 4)
np.hsplit(M, 2)   # dos bloques de (3, 2)
```

## Parámetros en detalle

### `ary` — array de entrada

A diferencia de [[np.vsplit]], `hsplit` acepta arrays 1D (corta en el eje 0).

### `indices_or_sections`

Entero (partes iguales) o lista de índices de corte.

## Casos de uso

### Separar columnas de variables

```python
datos = np.random.rand(100, 6)
primeras, ultimas = np.hsplit(datos, [3])   # (100,3) y (100,3)
```

## Buenas prácticas

1. Más legible que `split(..., axis=1)` para matrices.
2. Si no es divisible, usa `np.array_split(ary, n, axis=1)`.
3. Para cortar por filas, usa [[np.vsplit]].

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| división no exacta | tamaño no divisible | `np.array_split` |
| cortes en el eje equivocado | esperar filas | `hsplit` corta columnas; usar [[np.vsplit]] |

## Limitaciones

- En 2D fija el eje en 1; para control total usa [[np.split]] con `axis`.

## Notas relacionadas

- [[concepto_shape]]
- [[np.split]]
- [[np.vsplit]]
- [[np.hstack]]
