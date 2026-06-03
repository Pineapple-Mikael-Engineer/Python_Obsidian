---
title: np.tanh — Tangente hiperbólica (ufunc)
aliases:
  - tanh
  - np.tanh
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

# np.tanh — Tangente hiperbólica (ufunc)

## Firma de la función

```python
np.tanh(x, /, out=None, *, where=True, dtype=None) -> ndarray
```

## Valor de retorno

Aplica la **tangente hiperbólica** `tanh(x) = sinh/cosh` elemento a elemento. A diferencia de [[np.tan]], es **suave y acotada** en `(-1, 1)`, con forma de S (sigmoide).

| `x` | Resultado |
|-----|-----------|
| `0` | `0.0` |
| `1` | `0.762` |
| `±∞` | `→ ±1` |

```python
import numpy as np
np.tanh([-2, 0, 2])   # array([-0.964, 0., 0.964])
```

## Parámetros en detalle

`x` cualquier real; `out`, `where`, `dtype` como toda ufunc (ver [[np.add]]).

## Casos de uso

### Función de activación en redes neuronales

```python
salida = np.tanh(z)   # acota a (-1, 1), centrada en 0
```

## Buenas prácticas

1. Muy usada como activación: acotada, suave y centrada en 0.
2. Satura cerca de `±1` para `|x|` grande (gradiente ≈ 0).
3. El inverso es `np.arctanh` (dominio `(-1, 1)`).

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| Gradiente nulo en entrenamiento | saturación para `|x|` grande | normalizar las entradas |

## Limitaciones

- Satura (gradiente desvaneciente) en los extremos.

## Notas relacionadas

- [[concepto_ufuncs]]
- [[np.sinh]]
- [[np.cosh]]
- [[np.tan]]
