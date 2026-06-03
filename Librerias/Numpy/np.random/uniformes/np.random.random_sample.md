---
title: np.random.random_sample — Alias de np.random.random (uniforme [0,1))
aliases:
  - random_sample
  - random.random_sample
  - np.random.random_sample
tags:
  - numpy
  - api/funcion
  - aleatorio
lib: numpy
mod: np.random
tipo: funcion
retorna: ndarray o float
inplace: false
draft: false
---

# np.random.random_sample — Alias de np.random.random (uniforme [0,1))

## Firma de la función

```python
np.random.random_sample(size=None) -> ndarray
# size = entero o TUPLA (shape completo)
```

`random_sample` es un **alias exacto** de [[np.random.random]]: misma implementación, misma firma (`size` como tupla) y mismo comportamiento. Genera valores **uniformes en `[0, 1)`**. Usa la forma canónica `np.random.random` salvo que prefieras este nombre por compatibilidad.

## Valor de retorno

| Entrada | Retorno | Ejemplo |
|---------|---------|---------|
| `random_sample()` | `float` escalar | `0.487...` |
| `random_sample(3)` | ndarray `(3,)` | `[0.10, 0.55, 0.93]` |
| `random_sample((2, 3))` | ndarray `(2, 3)` | matriz 2×3 |

```python
import numpy as np
np.random.random_sample((2, 2))
# array([[0.211, 0.808],
#        [0.394, 0.512]])
```

## Parámetros en detalle

### `size` — el shape como tupla

Idéntico al de la función canónica: entero (1D) o **tupla** para el [[concepto_shape|shape]] nD. Toma una tupla, **no** dimensiones sueltas (eso es [[np.random.rand]]).

```python
np.random.random_sample(5)         # (5,)
np.random.random_sample((3, 4))    # (3, 4)
np.random.random_sample(size=(2,)) # por keyword
```

## Buenas prácticas

1. Prefiere `np.random.random` como forma canónica; `random_sample` es solo un nombre alternativo.
2. Para rango arbitrario `[low, high)`, usa `np.random.uniform`.

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| `TypeError` con args sueltos | `random_sample(2, 3)` | usar tupla: `random_sample((2, 3))` |
| Esperabas `[low, high)` | solo da `[0, 1)` | usar `np.random.uniform` |

## Notas relacionadas

- [[np.random.random]]
- [[np.random.ranf]]
- [[np.random.sample]]
