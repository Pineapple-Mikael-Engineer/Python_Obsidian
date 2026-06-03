---
title: np.arctan — Arcotangente (inverso de la tangente, ufunc)
aliases:
  - arctan
  - np.arctan
  - arcotangente
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

# np.arctan — Arcotangente (inverso de la tangente, ufunc)

## Firma de la función

```python
np.arctan(x, /, out=None, *, where=True, dtype=None) -> ndarray
```

## Valor de retorno

Devuelve el ángulo (en **radianes**) cuya tangente es `x`. Inverso de [[np.tan]]. **Dominio:** todo `ℝ`; **rango:** `(-π/2, π/2)`.

| `x` | Resultado (rad) |
|-----|-----------------|
| `0` | `0.0` |
| `1` | `π/4 ≈ 0.785` |
| `∞` | `→ π/2` |

```python
import numpy as np
np.arctan(1)   # 0.7854 (π/4)
```

## ⚠️ arctan vs arctan2

`arctan` solo distingue 2 cuadrantes (rango `(-π/2, π/2)`). Para el ángulo correcto en los **4 cuadrantes** a partir de `(y, x)`, usa `np.arctan2(y, x)`:

```python
np.arctan(1/1)        # π/4
np.arctan2(-1, -1)    # -3π/4  → cuadrante correcto
```

## Parámetros en detalle

`x` cualquier real; `out`, `where`, `dtype` como toda ufunc (ver [[np.add]]). Resultado en radianes.

## Casos de uso

### Ángulo de una pendiente

```python
angulo = np.rad2deg(np.arctan(dy / dx))
```

## Buenas prácticas

1. Para ángulos de un punto `(x, y)`, usa `np.arctan2(y, x)` (cuadrante correcto, sin división por cero).
2. Acepta todo `ℝ` (sin restricción de dominio, a diferencia de arcsin/arccos).

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| Cuadrante incorrecto | `arctan(y/x)` pierde el signo | usar `np.arctan2(y, x)` |

## Limitaciones

- Rango limitado a `(-π/2, π/2)`: no distingue cuadrantes.

## Notas relacionadas

- [[concepto_ufuncs]]
- [[np.tan]]
- [[np.arcsin]]
