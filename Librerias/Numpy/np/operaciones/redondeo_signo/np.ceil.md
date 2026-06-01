---
title: np.ceil — Redondeo hacia arriba (ufunc)
aliases:
  - ceil
  - np.ceil
  - techo
tags:
  - numpy
  - api/funcion
  - transformaciones

# --- Clasificación ---
lib: numpy
mod: np
tipo: funcion

# --- Comportamiento ---
retorna: ndarray
inplace: false

# --- Dependencias ---
requiere:
  - concepto_ufuncs

draft: false
---

# np.ceil — Redondeo hacia arriba (ufunc)

## Firma de la función

```python
np.ceil(x, /, out=None, *, where=True, dtype=None) -> ndarray
```

## Valor de retorno

Devuelve el **menor entero ≥ x** (techo) elemento a elemento, como **flotante**.

| `x` | Resultado |
|-----|-----------|
| `2.1` | `3.0` |
| `2.9` | `3.0` |
| `-2.1` | `-2.0` |

```python
import numpy as np
np.ceil([1.2, 2.7, -1.5])   # array([ 2.,  3., -1.])
```

## La familia de redondeo

| Función | Comportamiento | `2.7` | `-2.7` |
|---------|----------------|-------|--------|
| `np.ceil` | hacia arriba | `3` | `-2` |
| `np.floor` | hacia abajo | `2` | `-3` |
| `np.trunc` | hacia cero | `2` | `-2` |
| `np.round` | al más cercano (par) | `3` | `-3` |

## Parámetros en detalle

`x` real; `out`, `where`, `dtype` como toda ufunc (ver [[np.add]]). El resultado es flotante (castea con `.astype(int)` si quieres enteros).

## Casos de uso

### Número de lotes/páginas necesarios

```python
paginas = np.ceil(total / por_pagina).astype(int)
```

## Buenas prácticas

1. Devuelve float: convierte con `.astype(int)` si necesitas enteros.
2. Para los otros sentidos, `np.floor`, `np.trunc`, `np.round`.

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| Esperar int y recibir float | `ceil` devuelve float | `.astype(int)` |
| Confundir con `floor` en negativos | `ceil(-2.7) = -2` | revisar la tabla de redondeo |

## Limitaciones

- Salida flotante; redondea solo hacia arriba.

## Notas relacionadas

- [[concepto_ufuncs]]
- [[np.sign]]
- [[np.abs]]
