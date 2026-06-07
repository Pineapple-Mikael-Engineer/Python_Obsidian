---
title: np/operaciones — ufuncs element-wise
tags:
  - numpy
  - indice
draft: false
---

# np/operaciones — ufuncs element-wise

`operaciones/` agrupa las 26 [[concepto_ufuncs|ufuncs]] (universal functions) de NumPy que operan **element-wise** sobre arrays. Todas comparten la misma interfaz: reciben uno o dos arrays y devuelven un array del mismo shape (o broadcastado).

## Por que ufuncs

- **Broadcasting automatico**: alinean shapes sin copiar datos.
- **Parametros uniformes**: `out=`, `where=`, `dtype=`, `casting=` disponibles en todas.
- **Vectorizacion**: evitan bucles Python; la operacion se ejecuta en C.

## Subcarpetas

| Subcarpeta | Cantidad | Contenido |
|---|---|---|
| [[Librerias/Numpy/np/operaciones/aritmeticas/index\|aritmeticas/]] | 6 | add, subtract, multiply, divide, power, mod |
| [[Librerias/Numpy/np/operaciones/trigonometricas/index\|trigonometricas/]] | 9 | sin, cos, tan, arcsin, arccos, arctan, sinh, cosh, tanh |
| [[Librerias/Numpy/np/operaciones/exponenciales_log/index\|exponenciales_log/]] | 7 | exp, expm1, log, log2, log10, sqrt, square |
| [[Librerias/Numpy/np/operaciones/redondeo_signo/index\|redondeo_signo/]] | 4 | abs, fabs, sign, ceil |

## Patron unificador

Todas las ufuncs siguen el mismo patron: array de entrada → operacion elemento a elemento → array de salida con el mismo shape (o broadcastado):

```python
import numpy as np

a = np.array([1.0, 4.0, 9.0])
b = np.array([2.0, 2.0, 2.0])

# Todas operan igual — array → array element-wise
np.add(a, b)        # [3.  6.  11.]
np.multiply(a, b)   # [2.  8.  18.]
np.sqrt(a)          # [1.  2.  3.]
np.sin(a)           # sin de cada elemento en radianes
```

### Broadcasting entre subcarpetas

```python
M = np.ones((3, 4))
v = np.array([1, 2, 3, 4])   # shape (4,)

# Cualquier ufunc acepta broadcasting
np.add(M, v)         # suma v a cada fila → shape (3, 4)
np.multiply(M, v)    # multiplica v a cada fila → shape (3, 4)
np.power(M, v)       # eleva cada elemento de M a la potencia correspondiente
```

### Parametro `out` compartido

```python
resultado = np.empty(4)
np.add(M[0], v, out=resultado)   # escribe en buffer preasignado, sin copias
```

## Notas relacionadas

- [[concepto_ufuncs]]
- [[concepto_broadcasting]]
