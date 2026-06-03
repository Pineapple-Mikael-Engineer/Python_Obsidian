---
title: np.cos — Coseno (en radianes, ufunc)
aliases:
  - cos
  - np.cos
  - coseno
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

# np.cos — Coseno (en radianes, ufunc)

## Firma de la función

```python
np.cos(x, /, out=None, *, where=True, dtype=None) -> ndarray
```

## Valor de retorno

Aplica el **coseno** elemento a elemento, con `x` en **radianes**; resultado en `[-1, 1]`. Es una [[concepto_ufuncs|ufunc]].

| `x` (rad) | Resultado |
|-----------|-----------|
| `0` | `1.0` |
| `π/2` | `~0` |
| `π` | `-1.0` |

```python
import numpy as np
np.cos(np.array([0, np.pi/2, np.pi]))   # [1., ~0., -1.]
```

## Parámetros en detalle

`x` en radianes; `out`, `where`, `dtype` como toda ufunc (ver [[np.add]]). Para grados, convierte con `np.deg2rad`.

## Casos de uso

### Coordenadas en un círculo

```python
ang = np.linspace(0, 2*np.pi, 100)
x, y = np.cos(ang), np.sin(ang)
```

## Buenas prácticas

1. Radianes obligatorios (usa `np.deg2rad`).
2. El inverso es [[np.arccos]].

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| Resultados raros | grados en vez de radianes | `np.deg2rad` |
| Esperar 0 exacto en π/2 | redondeo flotante | `np.isclose` |

## Limitaciones

- Entrada en radianes.

## Notas relacionadas

- [[concepto_ufuncs]]
- [[np.sin]]
- [[np.tan]]
- [[np.arccos]]
