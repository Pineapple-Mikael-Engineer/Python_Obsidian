---
title: np.arcsin — Arcoseno (inverso del seno, ufunc)
aliases:
  - arcsin
  - np.arcsin
  - arcoseno
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

# np.arcsin — Arcoseno (inverso del seno, ufunc)

## Firma de la función

```python
np.arcsin(x, /, out=None, *, where=True, dtype=None) -> ndarray
```

## Valor de retorno

Devuelve el ángulo (en **radianes**) cuyo seno es `x`. Inverso de [[np.sin]]. **Dominio:** `x ∈ [-1, 1]`; **rango:** `[-π/2, π/2]`.

| `x` | Resultado (rad) |
|-----|-----------------|
| `0` | `0.0` |
| `1` | `π/2 ≈ 1.571` |
| `-1` | `-π/2` |

```python
import numpy as np
np.arcsin(1)              # 1.5708 (π/2)
np.rad2deg(np.arcsin(0.5))  # 30.0 grados
```

## ⚠️ Dominio restringido

Valores fuera de `[-1, 1]` devuelven `nan` con warning:

```python
np.arcsin(1.5)   # nan + RuntimeWarning
```

## Parámetros en detalle

`x` en `[-1, 1]`; `out`, `where`, `dtype` como toda ufunc (ver [[np.add]]). El resultado está en radianes (convierte con `np.rad2deg`).

## Casos de uso

### Recuperar un ángulo desde un seno

```python
angulo = np.arcsin(cateto_opuesto / hipotenusa)
```

## Buenas prácticas

1. Recorta a `[-1, 1]` con [[np.clip]] si el cálculo numérico puede excederlo ligeramente.
2. El resultado está en radianes.

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| `nan` + warning | `x` fuera de `[-1, 1]` | `np.clip(x, -1, 1)` |

## Limitaciones

- Solo cubre el rango `[-π/2, π/2]`.

## Notas relacionadas

- [[concepto_ufuncs]]
- [[np.sin]]
- [[np.arccos]]
- [[np.clip]]
