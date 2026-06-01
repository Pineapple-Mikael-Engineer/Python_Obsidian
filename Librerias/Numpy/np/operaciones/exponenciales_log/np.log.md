---
title: np.log — Logaritmo natural (ln, ufunc)
aliases:
  - log
  - np.log
  - logaritmo natural
  - ln
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

# np.log — Logaritmo natural (ln, ufunc)

## Firma de la función

```python
np.log(x, /, out=None, *, where=True, dtype=None) -> ndarray
```

## Valor de retorno

Aplica el **logaritmo natural** (base `e`) elemento a elemento. Inverso de [[np.exp]]. **Dominio:** `x > 0`.

| `x` | Resultado |
|-----|-----------|
| `1` | `0.0` |
| `e ≈ 2.718` | `1.0` |
| `0` | `-inf` + warning |
| `<0` | `nan` + warning |

```python
import numpy as np
np.log([1, np.e, np.e**2])   # array([0., 1., 2.])
```

## ⚠️ Dominio: x > 0

```python
np.log(0)    # -inf + RuntimeWarning
np.log(-1)   # nan  + RuntimeWarning
```

## Parámetros en detalle

`x > 0`; `out`, `where`, `dtype` como toda ufunc (ver [[np.add]]).

## Casos de uso

### Log-verosimilitud / cross-entropy

```python
loss = -np.log(np.clip(probs, 1e-12, 1.0))   # evita log(0)
```

### Para log(1+x) con x pequeño

```python
np.log1p(x)   # más preciso que np.log(1 + x)
```

## Buenas prácticas

1. Recorta con [[np.clip]] a un epsilon para evitar `log(0) = -inf`.
2. Para otras bases usa [[np.log2]], [[np.log10]] o `np.log(x)/np.log(base)`.
3. Para `log(1+x)` con `x→0`, usa `np.log1p`.

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| `-inf` | `x == 0` | `np.clip(x, eps, None)` |
| `nan` | `x < 0` | revisar el dominio |

## Limitaciones

- Solo `x > 0` en reales.

## Notas relacionadas

- [[concepto_ufuncs]]
- [[np.exp]]
- [[np.log2]]
- [[np.log10]]
