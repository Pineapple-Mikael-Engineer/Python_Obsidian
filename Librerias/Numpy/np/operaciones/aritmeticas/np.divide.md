---
title: np.divide — División elemento a elemento (ufunc)
aliases:
  - divide
  - np.divide
  - true_divide
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
  - concepto_dtype

draft: false
---

# np.divide — División elemento a elemento (ufunc)

## Firma de la función

```python
np.divide(x1, x2, /, out=None, *, where=True, dtype=None) -> ndarray
```

## Valor de retorno

Devuelve `x1 / x2` elemento a elemento (división **real**, siempre flotante). Es la [[concepto_ufuncs|ufunc]] del operador `/`.

| `x1` | `x2` | Resultado |
|------|------|-----------|
| `[10, 20, 30]` | `10` | `[1., 2., 3.]` |
| `[1, 2, 3]` | `[2, 2, 2]` | `[0.5, 1., 1.5]` |

```python
import numpy as np
np.divide([10, 20, 30], 10)   # array([1., 2., 3.])
```

## División entera vs real

| Operador | ufunc | Resultado |
|----------|-------|-----------|
| `/` | `np.divide` | flotante (división real) |
| `//` | `np.floor_divide` | entero (cociente) |
| `%` | [[np.mod]] | resto |

## El parámetro `where` para evitar división por cero

```python
a, b = np.array([1., 2., 3.]), np.array([0., 2., 0.])
np.divide(a, b, out=np.zeros_like(a), where=b != 0)
# [0., 1., 0.]  → no calcula donde b == 0 (sin warning)
```

## Parámetros en detalle

Idénticos a [[np.add]]: `out`, `where`, `dtype`.

## Casos de uso

### Normalizar por la suma

```python
probs = np.divide(conteos, conteos.sum())
```

## Buenas prácticas

1. Usa `where=divisor != 0` con `out` para evitar `inf`/`nan` y warnings.
2. El resultado siempre es flotante (ver [[concepto_dtype]]).
3. Para cociente entero usa `np.floor_divide` (`//`).

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| `RuntimeWarning: divide by zero` | divisor 0 | usar `where` + `out` |
| `inf`/`nan` en el resultado | división por 0 | enmascarar antes |

## Limitaciones

- Sin `where`, la división por 0 produce `inf`/`nan` con warning.

## Notas relacionadas

- [[concepto_ufuncs]]
- [[np.multiply]]
- [[np.mod]]
- [[np.add]]
