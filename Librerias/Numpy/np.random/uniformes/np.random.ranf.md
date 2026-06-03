---
title: np.random.ranf — Alias de np.random.random (uniforme [0,1))
aliases:
  - ranf
  - random.ranf
  - np.random.ranf
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

# np.random.ranf — Alias de np.random.random (uniforme [0,1))

## Firma de la función

```python
np.random.ranf(size=None) -> ndarray
# size = entero o TUPLA (shape completo)
```

`ranf` es un **alias exacto** de [[np.random.random]]: misma implementación, misma firma (`size` como tupla) y mismo comportamiento. Genera valores **uniformes en `[0, 1)`**. Nombre heredado por compatibilidad; en código nuevo usa la forma canónica `np.random.random`.

## Valor de retorno

| Entrada | Retorno | Ejemplo |
|---------|---------|---------|
| `ranf()` | `float` escalar | `0.673...` |
| `ranf(3)` | ndarray `(3,)` | `[0.27, 0.61, 0.04]` |
| `ranf((2, 3))` | ndarray `(2, 3)` | matriz 2×3 |

```python
import numpy as np
np.random.ranf((2, 2))
# array([[0.733, 0.190],
#        [0.602, 0.418]])
```

## Parámetros en detalle

### `size` — el shape como tupla

Idéntico al canónico: entero (1D) o **tupla** para el [[concepto_shape|shape]] nD. Toma una tupla, no dimensiones sueltas.

```python
np.random.ranf(5)        # (5,)
np.random.ranf((3, 4))   # (3, 4)
```

## Buenas prácticas

1. Prefiere `np.random.random`; `ranf` es solo un alias histórico.
2. Para un rango distinto de `[0,1)`, usa `np.random.uniform`.

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| `TypeError` con args sueltos | `ranf(2, 3)` | usar tupla: `ranf((2, 3))` |
| Esperabas `[low, high)` | solo da `[0, 1)` | usar `np.random.uniform` |

## Notas relacionadas

- [[np.random.random]]
- [[np.random.random_sample]]
- [[np.random.sample]]
