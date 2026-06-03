---
title: np.sqrt — Raíz cuadrada (ufunc)
aliases:
  - sqrt
  - np.sqrt
  - raiz cuadrada
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

# np.sqrt — Raíz cuadrada (ufunc)

## Firma de la función

```python
np.sqrt(x, /, out=None, *, where=True, dtype=None) -> ndarray
```

## Valor de retorno

Aplica la **raíz cuadrada** elemento a elemento. **Dominio (reales):** `x ≥ 0`. Equivale a `np.power(x, 0.5)` pero más rápida y precisa.

| `x` | Resultado |
|-----|-----------|
| `4` | `2.0` |
| `2` | `1.414` |
| `-1` | `nan` + warning |

```python
import numpy as np
np.sqrt([1, 4, 9, 16])   # array([1., 2., 3., 4.])
```

## ⚠️ Negativos

Con reales, `x < 0` da `nan`. Para raíces complejas usa `np.emath.sqrt` o entrada compleja:

```python
np.sqrt(-1)                 # nan + warning
np.sqrt(-1 + 0j)            # 1j
```

## Parámetros en detalle

`x ≥ 0`; `out`, `where`, `dtype` como toda ufunc (ver [[np.add]]).

## Casos de uso

### Norma euclídea / distancia

```python
dist = np.sqrt(np.sum((a - b)**2))
```

### Desviación a partir de la varianza

```python
desv = np.sqrt(varianza)
```

## Buenas prácticas

1. Más eficiente que `x ** 0.5` o [[np.power]] con `0.5`.
2. Para raíces de negativos, usa entrada compleja o `np.emath.sqrt`.

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| `nan` + warning | `x < 0` | usar complejos o `np.emath.sqrt` |

## Limitaciones

- En reales, solo `x ≥ 0`.

## Notas relacionadas

- [[concepto_ufuncs]]
- [[np.square]]
- [[np.power]]
- [[np.abs]]
