---
title: np/operaciones/aritmeticas — operaciones aritmeticas basicas (ufuncs)
tags:
  - numpy
  - indice
draft: false
---

# np/operaciones/aritmeticas — operaciones aritmeticas basicas (ufuncs)

Las 6 operaciones aritmeticas fundamentales implementadas como [[concepto_ufuncs|ufuncs]]. Son los equivalentes funcionales de los operadores `+ - * / ** %`, pero exponen los parametros `out=`, `where=` y `dtype=` que los operadores no ofrecen.

## Tabla comparativa: operador vs ufunc

| Operador | ufunc | Descripcion |
|---|---|---|
| `a + b` | [[np.add]] | suma elemento a elemento |
| `a - b` | [[np.subtract]] | resta elemento a elemento |
| `a * b` | [[np.multiply]] | multiplicacion elemento a elemento |
| `a / b` | [[np.divide]] | division verdadera elemento a elemento |
| `a ** b` | [[np.power]] | potenciacion elemento a elemento |
| `a % b` | [[np.mod]] | modulo (resto) elemento a elemento |

## Cuando usar la ufunc en vez del operador

```python
import numpy as np

a = np.array([1.0, 2.0, 3.0])
b = np.array([4.0, 5.0, 6.0])

# Operador: forma concisa para codigo normal
resultado = a + b

# ufunc: necesario cuando se requiere out= o where=
buffer = np.zeros(3)
np.add(a, b, out=buffer)              # escribe en buffer existente, sin copias

mascara = np.array([True, False, True])
np.multiply(a, b, where=mascara, out=buffer)   # solo opera donde mascara es True
```

## Broadcasting

Todas soportan [[concepto_broadcasting|broadcasting]] identico al de sus operadores:

```python
M = np.ones((3, 4))
v = np.array([1, 2, 3, 4])   # shape (4,)

np.add(M, v)       # suma v a cada fila → (3, 4)
np.multiply(M, v)  # multiplica v a cada fila → (3, 4)
```

## Notas de este grupo

- [[np.add]]
- [[np.subtract]]
- [[np.multiply]]
- [[np.divide]]
- [[np.power]]
- [[np.mod]]

## Notas relacionadas

- [[concepto_ufuncs]]
- [[concepto_broadcasting]]
- [[Librerias/Numpy/np/operaciones/index|np/operaciones — ufuncs element-wise]]
