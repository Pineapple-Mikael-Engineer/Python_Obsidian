---
title: ndarray.imag — Parte imaginaria de un array complejo
aliases:
  - imag
  - ndarray.imag
tags:
  - numpy
  - api/atributo
  - dtype
lib: numpy
obj: ndarray
tipo: atributo
draft: false
---

# ndarray.imag — Parte imaginaria de un array complejo

## Qué representa

Devuelve la **parte imaginaria** de cada elemento del array. En arrays complejos extrae el coeficiente imaginario como vista sobre la misma memoria; en arrays reales devuelve un array de ceros con la misma forma. Al ser una vista en arrays complejos, asignar a `imag` modifica el buffer original.

## Tipo y acceso

| Aspecto | Valor |
|---------|-------|
| Tipo devuelto | `ndarray` (dtype real subyacente: `float32`/`float64`) |
| Acceso | **ASIGNABLE** |
| Sobre array complejo | Vista de la componente imaginaria |
| Sobre array real | Array de ceros (misma shape) |

## Ejemplos

```python
import numpy as np

z = np.array([1+2j, 3+4j])
z.imag          # → array([2., 4.])

z.imag = [0, 0]
z               # → array([1.+0.j, 3.+0.j])  (asignacion in-place)

r = np.array([1.0, 2.0])
r.imag          # → array([0., 0.])
```

## Notas relacionadas

- [[ndarray.real]]
- [[concepto_dtype]]
