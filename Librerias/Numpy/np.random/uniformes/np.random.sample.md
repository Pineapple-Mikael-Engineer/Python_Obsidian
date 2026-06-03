---
title: np.random.sample — Alias de np.random.random (uniforme [0,1))
aliases:
  - sample
  - random.sample
  - np.random.sample
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

# np.random.sample — Alias de np.random.random (uniforme [0,1))

## Firma de la función

```python
np.random.sample(size=None) -> ndarray
# size = entero o TUPLA (shape completo)
```

`sample` es un **alias exacto** de [[np.random.random]]: misma implementación, misma firma (`size` como tupla) y mismo comportamiento. Genera valores **uniformes en `[0, 1)`**. Usa la forma canónica `np.random.random` salvo necesidad de compatibilidad.

> ⚠️ No confundir con `random.sample` de la **librería estándar** de Python (que muestrea sin reemplazo de una secuencia). Aquí `np.random.sample` es solo otro nombre de `np.random.random`.

## Valor de retorno

| Entrada | Retorno | Ejemplo |
|---------|---------|---------|
| `sample()` | `float` escalar | `0.359...` |
| `sample(3)` | ndarray `(3,)` | `[0.80, 0.12, 0.47]` |
| `sample((2, 3))` | ndarray `(2, 3)` | matriz 2×3 |

```python
import numpy as np
np.random.sample((2, 2))
# array([[0.305, 0.677],
#        [0.149, 0.920]])
```

## Parámetros en detalle

### `size` — el shape como tupla

Idéntico al canónico: entero (1D) o **tupla** para el [[concepto_shape|shape]] nD. Toma una tupla, no dimensiones sueltas.

```python
np.random.sample(5)        # (5,)
np.random.sample((3, 4))   # (3, 4)
```

## Buenas prácticas

1. Prefiere `np.random.random`; `sample` es solo un alias.
2. Para un rango arbitrario `[low, high)`, usa `np.random.uniform`.

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| `TypeError` con args sueltos | `sample(2, 3)` | usar tupla: `sample((2, 3))` |
| Confundir con `random.sample` de stdlib | nombres iguales | son funciones distintas |
| Esperabas `[low, high)` | solo da `[0, 1)` | usar `np.random.uniform` |

## Notas relacionadas

- [[np.random.random]]
- [[np.random.random_sample]]
- [[np.random.ranf]]
