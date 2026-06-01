---
title: np.log2 — Logaritmo en base 2 (ufunc)
aliases:
  - log2
  - np.log2
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

# np.log2 — Logaritmo en base 2 (ufunc)

## Firma de la función

```python
np.log2(x, /, out=None, *, where=True, dtype=None) -> ndarray
```

## Valor de retorno

Aplica el **logaritmo en base 2** elemento a elemento. **Dominio:** `x > 0`. Más preciso que `np.log(x)/np.log(2)`.

| `x` | Resultado |
|-----|-----------|
| `1` | `0.0` |
| `2` | `1.0` |
| `8` | `3.0` |

```python
import numpy as np
np.log2([1, 2, 8, 1024])   # array([ 0.,  1.,  3., 10.])
```

## Parámetros en detalle

`x > 0`; `out`, `where`, `dtype` como toda ufunc (ver [[np.add]]).

## Casos de uso

### Entropía de información (bits)

```python
entropia = -np.sum(p * np.log2(p))
```

### Número de bits necesarios

```python
bits = np.ceil(np.log2(n))
```

## Buenas prácticas

1. Para magnitudes binarias/información es la base natural.
2. Mismo dominio y cuidados que [[np.log]] (`x > 0`).

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| `-inf` / `nan` | `x ≤ 0` | recortar con [[np.clip]] |

## Limitaciones

- Solo `x > 0`.

## Notas relacionadas

- [[concepto_ufuncs]]
- [[np.log]]
- [[np.log10]]
