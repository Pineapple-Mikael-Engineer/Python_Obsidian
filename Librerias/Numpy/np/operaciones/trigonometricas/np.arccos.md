---
title: np.arccos — Arcocoseno (inverso del coseno, ufunc)
aliases:
  - arccos
  - np.arccos
  - arcocoseno
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

# np.arccos — Arcocoseno (inverso del coseno, ufunc)

## Firma de la función

```python
np.arccos(x, /, out=None, *, where=True, dtype=None) -> ndarray
```

## Valor de retorno

Devuelve el ángulo (en **radianes**) cuyo coseno es `x`. Inverso de [[np.cos]]. **Dominio:** `x ∈ [-1, 1]`; **rango:** `[0, π]`.

| `x` | Resultado (rad) |
|-----|-----------------|
| `1` | `0.0` |
| `0` | `π/2` |
| `-1` | `π` |

```python
import numpy as np
np.arccos(0)   # 1.5708 (π/2)
```

## Parámetros en detalle

`x` en `[-1, 1]` (fuera → `nan`); `out`, `where`, `dtype` como toda ufunc (ver [[np.add]]). Resultado en radianes.

## Casos de uso

### Ángulo entre dos vectores (coseno de similitud)

```python
cos_sim = np.dot(u, v) / (np.linalg.norm(u) * np.linalg.norm(v))
angulo = np.arccos(np.clip(cos_sim, -1, 1))
```

## Buenas prácticas

1. **Siempre** recorta con [[np.clip]] a `[-1, 1]`: errores de redondeo en productos escalares pueden dar `1.0000001` → `nan`.
2. Resultado en radianes.

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| `nan` por `1.0000001` | redondeo en cos_sim | `np.clip(x, -1, 1)` |

## Limitaciones

- Rango `[0, π]`.

## Notas relacionadas

- [[concepto_ufuncs]]
- [[np.cos]]
- [[np.arcsin]]
- [[np.clip]]
