---
title: np.subtract — Resta elemento a elemento (ufunc)
aliases:
  - subtract
  - np.subtract
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
  - concepto_broadcasting

draft: false
---

# np.subtract — Resta elemento a elemento (ufunc)

## Firma de la función

```python
np.subtract(x1, x2, /, out=None, *, where=True, dtype=None) -> ndarray
```

## Valor de retorno

Devuelve `x1 - x2` elemento a elemento, con [[concepto_broadcasting|broadcasting]]. Es la [[concepto_ufuncs|ufunc]] del operador `-`.

| `x1` | `x2` | Resultado |
|------|------|-----------|
| `[5, 7, 9]` | `[1, 2, 3]` | `[4, 5, 6]` |
| `(3, 4)` | `(4,)` | broadcasting → `(3, 4)` |

```python
import numpy as np
np.subtract([5, 7, 9], 2)   # array([3, 5, 7])
```

## Parámetros en detalle

Idénticos a [[np.add]]: `out` (salida in-place), `where` (máscara), `dtype`.

## Casos de uso

### Centrar datos restando la media

```python
centrado = np.subtract(datos, datos.mean(axis=0))
```

### Diferencia entre matrices

```python
error = np.subtract(prediccion, objetivo)
```

## Buenas prácticas

1. Usa el operador `-` salvo que necesites `out`/`where`.
2. Cuidado con enteros **sin signo**: `a - b` con `uint` puede dar overflow (wrap-around).

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| Valores enormes con `uint` | resta negativa desborda | convertir a `int`/`float` |
| `could not be broadcast` | shapes incompatibles | revisar dimensiones |

## Limitaciones

- Resta elemento a elemento; para diferencias consecutivas usa [[np.diff]].

## Notas relacionadas

- [[concepto_ufuncs]]
- [[np.add]]
- [[np.multiply]]
- [[np.diff]]
