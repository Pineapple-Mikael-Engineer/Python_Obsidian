---
title: np.fabs — Valor absoluto en float (ufunc)
aliases:
  - fabs
  - np.fabs
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

# np.fabs — Valor absoluto en float (ufunc)

## Firma de la función

```python
np.fabs(x, /, out=None, *, where=True, dtype=None) -> ndarray
```

## Valor de retorno

Devuelve el valor absoluto elemento a elemento, **siempre como flotante** y **solo para reales** (no acepta complejos). Variante de [[np.abs]].

| `x` | Resultado |
|-----|-----------|
| `[-1, 2, -3]` | `[1., 2., 3.]` (float) |
| `3 + 4j` | TypeError |

```python
import numpy as np
np.fabs([-1, -2, 3])    # array([1., 2., 3.])  → float
```

## fabs vs abs

| | `np.fabs` | [[np.abs]] |
|--|-----------|-----------|
| Salida | siempre `float` | conserva dtype |
| Complejos | ❌ error | ✅ módulo |

## Parámetros en detalle

`x` real; `out`, `where`, `dtype` como toda ufunc (ver [[np.add]]).

## Casos de uso

### Forzar salida flotante

```python
np.fabs(enteros)   # garantiza float sin castear aparte
```

## Buenas prácticas

1. Úsala cuando quieras **garantizar float** y trabajes solo con reales.
2. Para complejos o conservar el dtype entero, usa [[np.abs]].

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| `TypeError` con complejos | `fabs` no los acepta | usar [[np.abs]] |

## Limitaciones

- No acepta números complejos; siempre devuelve float.

## Notas relacionadas

- [[concepto_ufuncs]]
- [[np.abs]]
- [[np.sign]]
