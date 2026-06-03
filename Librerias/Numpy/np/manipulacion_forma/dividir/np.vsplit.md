---
title: np.vsplit — Dividir por filas (eje 0)
aliases:
  - vsplit
  - np.vsplit
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

# np.vsplit — Dividir por filas (eje 0)

## Firma de la función

```python
np.vsplit(
    ary,
    indices_or_sections
) -> list[ndarray]
```

## Valor de retorno

Devuelve una lista de sub-arrays cortando `ary` **verticalmente** (a lo largo del eje 0, filas). Es un atajo de [[np.split]] con `axis=0`. Inverso de [[np.vstack]].

| Entrada | `indices_or_sections` | Salida |
|---------|------------------------|--------|
| `(6, 4)` | `3` | 3 arrays de `(2, 4)` |
| `(6, 4)` | `[1, 4]` | `(1,4)`, `(3,4)`, `(2,4)` |

```python
import numpy as np
M = np.arange(12).reshape(4, 3)
partes = np.vsplit(M, 2)   # dos bloques de (2, 3)
```

## Parámetros en detalle

### `ary` — array de **al menos 2D**

`vsplit` requiere `ndim >= 2`.

### `indices_or_sections`

Entero (N partes iguales, exige divisibilidad) o lista de índices de corte.

## Casos de uso

### Separar un dataset en bloques de filas

```python
datos = np.random.rand(100, 8)
bloques = np.vsplit(datos, 5)   # 5 bloques de (20, 8)
```

## Buenas prácticas

1. Más legible que `split(..., axis=0)` para matrices.
2. Si no es divisible, usa `np.array_split(ary, n, axis=0)`.
3. Para cortar por columnas, usa [[np.hsplit]].

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| `vsplit only works on arrays of 2 or more dimensions` | array 1D | usar [[np.split]] |
| división no exacta | tamaño no divisible | `np.array_split` |

## Limitaciones

- Solo opera en el eje 0 y requiere 2D+.

## Notas relacionadas

- [[concepto_shape]]
- [[np.split]]
- [[np.hsplit]]
- [[np.vstack]]
