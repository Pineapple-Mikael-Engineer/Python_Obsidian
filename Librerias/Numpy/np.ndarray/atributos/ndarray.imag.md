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
mod: np.ndarray
tipo: atributo
draft: false
---

# ndarray.imag — Parte imaginaria de un array complejo

Devuelve la **parte imaginaria** de cada elemento del array. Sobre un array complejo extrae el coeficiente imaginario como **vista** de la misma memoria; sobre un array real devuelve un array de **ceros** con la misma forma. Por ser vista, **asignar** a `imag` modifica el buffer original. La teoría de los tipos complejos vive en [[concepto_dtype]].

## Tipo y lectura/escritura

| Aspecto | Valor |
|---------|-------|
| Tipo devuelto | `ndarray` con el dtype real subyacente (`float32`/`float64`) |
| Lectura/escritura | **Asignable** (`a.imag = ...`) |
| Sobre array complejo | **Vista** de la componente imaginaria |
| Sobre array real | Array de **ceros** (misma shape) |

## En detalle

El `dtype` de `imag` es el flotante que respalda al complejo (`complex128 → float64`). Sobre un array real no hay parte imaginaria almacenada, así que NumPy devuelve ceros y **no** es asignable (no hay buffer donde escribir).

```python
import numpy as np

z = np.array([1+2j, 3+4j])
z.imag          # → array([2., 4.])  (vista, dtype float64)

z.imag = [0, 0]
z               # → array([1.+0.j, 3.+0.j])  (asignación in-place)

r = np.array([1.0, 2.0])
r.imag          # → array([0., 0.])  (array real: todo ceros)
```

## Casos de uso

- Comprobar si el residuo imaginario de un cálculo es despreciable: `np.allclose(z.imag, 0)`.
- Anular la parte imaginaria conservando el dtype complejo: `z.imag = 0`.
- Construir o editar una señal compleja por componentes (`z.real`, `z.imag`).

## Notas relacionadas

- [[ndarray.real]]
- [[concepto_dtype]]
