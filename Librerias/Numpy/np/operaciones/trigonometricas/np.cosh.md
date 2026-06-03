---
title: np.cosh — Coseno hiperbólico (ufunc)
aliases:
  - cosh
  - np.cosh
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

# np.cosh — Coseno hiperbólico (ufunc)

## Firma de la función

```python
np.cosh(x, /, out=None, *, where=True, dtype=None) -> ndarray
```

## Valor de retorno

Aplica el **coseno hiperbólico** `cosh(x) = (eˣ + e⁻ˣ)/2` elemento a elemento. Su mínimo es `1` en `x=0`; crece exponencialmente a ambos lados (forma de catenaria).

| `x` | Resultado |
|-----|-----------|
| `0` | `1.0` |
| `1` | `1.543` |
| `5` | `74.2` |

```python
import numpy as np
np.cosh([0, 1, 2])   # array([1., 1.543, 3.762])
```

## Parámetros en detalle

`x` cualquier real; `out`, `where`, `dtype` como toda ufunc (ver [[np.add]]).

## Casos de uso

### Perfil de un cable colgante (catenaria)

```python
x = np.linspace(-5, 5, 100)
y = np.cosh(x)
```

## Buenas prácticas

1. Siempre `≥ 1`; crece exponencialmente (vigila overflow).
2. El inverso es `np.arccosh` (dominio `x ≥ 1`).

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| Overflow | `x` muy grande | acotar el dominio |

## Limitaciones

- No acotada superiormente.

## Notas relacionadas

- [[concepto_ufuncs]]
- [[np.sinh]]
- [[np.tanh]]
- [[np.cos]]
