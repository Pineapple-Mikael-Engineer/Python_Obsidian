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
mod: np.ndarray
tipo: atributo
draft: false
---

# ndarray.real — Parte real de un array complejo

Devuelve la **parte real** de cada elemento del array. Sobre un array complejo extrae el componente real como **vista** de la misma memoria; sobre un array real devuelve el propio array (su parte real es él mismo). Por ser vista, **asignar** a `real` modifica el buffer del array original. La teoría de los tipos complejos vive en [[concepto_dtype]].

## Tipo y lectura/escritura

| Aspecto | Valor |
|---------|-------|
| Tipo devuelto | `ndarray` con el dtype real subyacente (`float32`/`float64`) |
| Lectura/escritura | **Asignable** (`a.real = ...`) |
| Sobre array complejo | **Vista** de la componente real |
| Sobre array real | El mismo array (su parte real) |

## En detalle

El `dtype` de `real` es el flotante que respalda al complejo: `complex128 → float64`, `complex64 → float32`. Como es una vista, asignarle valores reescribe la parte real in situ sin tocar la imaginaria.

```python
import numpy as np

z = np.array([1+2j, 3+4j])
z.real          # → array([1., 3.])  (vista, dtype float64)
z.imag          # → array([2., 4.])

z.real = [9, 9]
z               # → array([9.+2.j, 9.+4.j])  (asignación in-place)

r = np.array([1.0, 2.0])
r.real          # → array([1., 2.])  (el array completo)
```

## Casos de uso

- Separar el espectro de una FFT en magnitud real e imaginaria para graficar o filtrar.
- Modificar la parte real de una señal compleja sin reconstruir el array (`z.real *= 2`).
- Descartar el residuo imaginario tras una operación que debería ser real: `z.real`.

## Notas relacionadas

- [[ndarray.imag]]
- [[concepto_dtype]]
