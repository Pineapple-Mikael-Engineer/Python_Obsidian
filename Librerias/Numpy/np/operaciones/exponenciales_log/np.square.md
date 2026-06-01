---
title: np.square — Cuadrado elemento a elemento (ufunc)
aliases:
  - square
  - np.square
  - cuadrado
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

# np.square — Cuadrado elemento a elemento (ufunc)

## Firma de la función

```python
np.square(x, /, out=None, *, where=True, dtype=None) -> ndarray
```

## Valor de retorno

Devuelve `x²` elemento a elemento. Equivale a `np.power(x, 2)` o `x * x`, pero más rápida y legible.

| `x` | Resultado |
|-----|-----------|
| `[1, 2, 3]` | `[1, 4, 9]` |
| `-3` | `9` |

```python
import numpy as np
np.square([1, 2, 3, 4])   # array([ 1,  4,  9, 16])
```

## Parámetros en detalle

`x` cualquiera; `out`, `where`, `dtype` como toda ufunc (ver [[np.add]]).

## Casos de uso

### Suma de cuadrados (energía, MSE)

```python
mse = np.mean(np.square(prediccion - objetivo))
```

## Buenas prácticas

1. Más rápida y clara que `x ** 2` o [[np.power]] con `2`.
2. El inverso (para `x ≥ 0`) es [[np.sqrt]].
3. Vigila el **overflow** con enteros grandes.

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| Overflow | enteros grandes al cuadrado | `dtype=float64` |

## Limitaciones

- Solo cuadrado; para otras potencias usa [[np.power]].

## Notas relacionadas

- [[concepto_ufuncs]]
- [[np.sqrt]]
- [[np.power]]
