---
title: np.log10 — Logaritmo en base 10 (ufunc)
aliases:
  - log10
  - np.log10
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

# np.log10 — Logaritmo en base 10 (ufunc)

## Firma de la función

```python
np.log10(x, /, out=None, *, where=True, dtype=None) -> ndarray
```

## Valor de retorno

Aplica el **logaritmo en base 10** elemento a elemento. **Dominio:** `x > 0`. Más preciso que `np.log(x)/np.log(10)`.

| `x` | Resultado |
|-----|-----------|
| `1` | `0.0` |
| `10` | `1.0` |
| `1000` | `3.0` |

```python
import numpy as np
np.log10([1, 10, 100, 1000])   # array([0., 1., 2., 3.])
```

## Parámetros en detalle

`x > 0`; `out`, `where`, `dtype` como toda ufunc (ver [[np.add]]).

## Casos de uso

### Decibelios

```python
db = 20 * np.log10(amplitud / referencia)
```

### Órdenes de magnitud / escala log

```python
orden = np.floor(np.log10(np.abs(valores)))
```

## Buenas prácticas

1. La base natural para magnitudes físicas (dB, pH, escalas log).
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
- [[np.log2]]
