---
title: ndarray.real — Parte real de un array complejo
aliases:
  - real
  - ndarray.real
tags:
  - numpy
  - api/atributo
  - dtype
lib: numpy
obj: ndarray
tipo: atributo
draft: false
---

# ndarray.real — Parte real de un array complejo

## Qué representa

Devuelve la **parte real** de cada elemento del array. En arrays complejos extrae el componente real; en arrays reales devuelve el propio array (su parte real es el array completo). Es una vista sobre la misma memoria del array original cuando éste es complejo, por lo que asignar a `real` modifica el buffer subyacente.

## Tipo y acceso

| Aspecto | Valor |
|---------|-------|
| Tipo devuelto | `ndarray` (dtype real subyacente: `float32`/`float64`) |
| Acceso | **ASIGNABLE** |
| Sobre array complejo | Vista de la componente real |
| Sobre array real | Devuelve el mismo array |

## Ejemplos

```python
import numpy as np

z = np.array([1+2j, 3+4j])
z.real          # → array([1., 3.])
z.imag          # → array([2., 4.])

z.real = [9, 9]
z               # → array([9.+2.j, 9.+4.j])  (asignacion in-place)

r = np.array([1.0, 2.0])
r.real          # → array([1., 2.])  (el array completo)
```

## Notas relacionadas

- [[ndarray.imag]]
- [[concepto_dtype]]
