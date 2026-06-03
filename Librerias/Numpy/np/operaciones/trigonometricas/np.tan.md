---
title: np.tan — Tangente (en radianes, ufunc)
aliases:
  - tan
  - np.tan
  - tangente
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

# np.tan — Tangente (en radianes, ufunc)

## Firma de la función

```python
np.tan(x, /, out=None, *, where=True, dtype=None) -> ndarray
```

## Valor de retorno

Aplica la **tangente** (`sin/cos`) elemento a elemento, con `x` en **radianes**. Su rango es todo `ℝ` y **diverge** cerca de `π/2 + kπ`.

| `x` (rad) | Resultado |
|-----------|-----------|
| `0` | `0.0` |
| `π/4` | `~1.0` |
| `π/2` | valor enorme (≈1.6e16, no inf) |

```python
import numpy as np
np.tan(np.array([0, np.pi/4]))   # [0., ~1.]
```

## Parámetros en detalle

`x` en radianes; `out`, `where`, `dtype` como toda ufunc (ver [[np.add]]).

## Casos de uso

### Pendiente a partir de un ángulo

```python
pendiente = np.tan(np.deg2rad(angulo_grados))
```

## Buenas prácticas

1. Cerca de `π/2` el resultado es enorme e inestable (no exactamente `inf`): evita esos puntos.
2. Radianes obligatorios.
3. El inverso es [[np.arctan]] (o `np.arctan2` para el cuadrante correcto).

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| Valor gigantesco | `x` cerca de π/2 | evitar la asíntota |
| Resultados raros | grados | `np.deg2rad` |

## Limitaciones

- Discontinuidades en `π/2 + kπ`.

## Notas relacionadas

- [[concepto_ufuncs]]
- [[np.sin]]
- [[np.cos]]
- [[np.arctan]]
