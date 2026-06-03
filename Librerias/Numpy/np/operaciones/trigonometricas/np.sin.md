---
title: np.sin — Seno (en radianes, ufunc)
aliases:
  - sin
  - np.sin
  - seno
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
  - concepto_vectorizacion

draft: false
---

# np.sin — Seno (en radianes, ufunc)

## Firma de la función

```python
np.sin(x, /, out=None, *, where=True, dtype=None) -> ndarray
```

## Valor de retorno

Aplica el **seno** elemento a elemento. El argumento se interpreta en **radianes**; el resultado está en `[-1, 1]`. Es una [[concepto_ufuncs|ufunc]] [[concepto_vectorizacion|vectorizada]].

| `x` (rad) | Resultado |
|-----------|-----------|
| `0` | `0.0` |
| `π/2` | `1.0` |
| `π` | `~0` (≈1.2e-16) |

```python
import numpy as np
np.sin(np.array([0, np.pi/2, np.pi]))   # [0., 1., ~0.]
```

## ⚠️ Radianes, no grados

Convierte grados a radianes con `np.deg2rad` (o `np.radians`):

```python
np.sin(np.deg2rad(90))   # 1.0
np.sin(90)               # 0.894...  → 90 radianes, casi seguro un error
```

## Parámetros en detalle

### `x` — ángulos en radianes

Array o escalar.

### `out`, `where`, `dtype`

Como en toda ufunc (ver [[np.add]]).

## Casos de uso

### Generar una onda senoidal

```python
t = np.linspace(0, 2*np.pi, 1000)
onda = np.sin(t)
```

## Buenas prácticas

1. Trabaja siempre en radianes; convierte con `np.deg2rad` si tienes grados.
2. Cerca de `π`, el resultado no es exactamente 0 por redondeo flotante.
3. El inverso es [[np.arcsin]].

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| Resultados sin sentido | se pasaron grados | usar `np.deg2rad` |
| Esperar 0 exacto en π | redondeo flotante | comparar con `np.isclose` |

## Limitaciones

- Entrada en radianes obligatoria.

## Notas relacionadas

- [[concepto_ufuncs]]
- [[np.cos]]
- [[np.tan]]
- [[np.arcsin]]
