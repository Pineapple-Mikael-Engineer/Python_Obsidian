---
title: np.exp — Exponencial e^x (ufunc)
aliases:
  - exp
  - np.exp
  - exponencial
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

# np.exp — Exponencial e^x (ufunc)

## Firma de la función

```python
np.exp(x, /, out=None, *, where=True, dtype=None) -> ndarray
```

## Valor de retorno

Aplica `e^x` (con `e ≈ 2.71828`) elemento a elemento. Es la [[concepto_ufuncs|ufunc]] inversa de [[np.log]]; siempre positiva, crece muy rápido.

| `x` | Resultado |
|-----|-----------|
| `0` | `1.0` |
| `1` | `2.718` |
| `10` | `22026.5` |

```python
import numpy as np
np.exp([0, 1, 2])   # array([1., 2.718, 7.389])
```

## Parámetros en detalle

`x` cualquier real; `out`, `where`, `dtype` como toda ufunc (ver [[np.add]]).

## Casos de uso

### Softmax (estable)

```python
z = z - z.max()             # estabiliza evitando overflow
probs = np.exp(z) / np.exp(z).sum()
```

### Decaimiento exponencial

```python
y = np.exp(-t / tau)
```

## Buenas prácticas

1. **Overflow**: `np.exp(800)` da `inf`. En softmax, resta el máximo antes.
2. Para `exp(x) - 1` con `x` pequeño, usa [[np.expm1]] (más preciso).
3. El inverso es [[np.log]].

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| `inf` / `RuntimeWarning: overflow` | `x` grande | restar el máximo / acotar |
| Pérdida de precisión cerca de 0 | `exp(x)-1` | usar [[np.expm1]] |

## Limitaciones

- Overflow rápido para `x` moderadamente grande (ver [[concepto_dtype]]).

## Notas relacionadas

- [[concepto_ufuncs]]
- [[np.log]]
- [[np.expm1]]
- [[np.power]]
