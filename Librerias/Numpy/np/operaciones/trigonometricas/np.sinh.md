---
title: np.sinh — Seno hiperbólico (ufunc)
aliases:
  - sinh
  - np.sinh
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

# np.sinh — Seno hiperbólico (ufunc)

## Firma de la función

```python
np.sinh(x, /, out=None, *, where=True, dtype=None) -> ndarray
```

## Valor de retorno

Aplica el **seno hiperbólico** `sinh(x) = (eˣ − e⁻ˣ)/2` elemento a elemento. A diferencia del seno circular, **no está acotado**: crece exponencialmente.

| `x` | Resultado |
|-----|-----------|
| `0` | `0.0` |
| `1` | `1.175` |
| `5` | `74.2` |

```python
import numpy as np
np.sinh([0, 1, 2])   # array([0., 1.175, 3.627])
```

## Parámetros en detalle

`x` cualquier real; `out`, `where`, `dtype` como toda ufunc (ver [[np.add]]).

## Casos de uso

### Catenaria (cable colgante)

```python
y = a * np.cosh(x / a)
```

## Buenas prácticas

1. Crece exponencialmente: vigila el **overflow** con `x` grandes.
2. El inverso es `np.arcsinh`.

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| `inf`/overflow | `x` muy grande | acotar el dominio |

## Limitaciones

- No acotada (a diferencia de [[np.sin]]).

## Notas relacionadas

- [[concepto_ufuncs]]
- [[np.cosh]]
- [[np.tanh]]
- [[np.sin]]
