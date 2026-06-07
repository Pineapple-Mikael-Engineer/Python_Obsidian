---
title: np/operaciones/trigonometricas — funciones trigonometricas e hiperbolicas (ufuncs)
tags:
  - numpy
  - indice
draft: false
---

# np/operaciones/trigonometricas — funciones trigonometricas e hiperbolicas (ufuncs)

Las 9 [[concepto_ufuncs|ufuncs]] trigonometricas e hiperbolicas de NumPy. Operan **elemento a elemento** sobre arrays de cualquier shape. **Todas trabajan en radianes**, tanto en entrada como en salida.

> [!warning] Radianes, no grados
> La entrada se interpreta en radianes. Para convertir grados a radianes usa `np.deg2rad(angulo)` o `angulo * np.pi / 180`.

## Tabla de funciones

| Grupo | ufunc | Descripcion | Dominio entrada | Rango salida |
|---|---|---|---|---|
| **Trigonometricas principales** | [[np.sin]] | seno | todos los reales | [-1, 1] |
| | [[np.cos]] | coseno | todos los reales | [-1, 1] |
| | [[np.tan]] | tangente | todos los reales | (-inf, +inf) |
| **Inversas** | [[np.arcsin]] | arcoseno | [-1, 1] | [-pi/2, pi/2] |
| | [[np.arccos]] | arcocoseno | [-1, 1] | [0, pi] |
| | [[np.arctan]] | arcotangente | todos los reales | (-pi/2, pi/2) |
| **Hiperbolicas** | [[np.sinh]] | seno hiperbolico | todos los reales | (-inf, +inf) |
| | [[np.cosh]] | coseno hiperbolico | todos los reales | [1, +inf) |
| | [[np.tanh]] | tangente hiperbolica | todos los reales | (-1, 1) |

## Uso basico

```python
import numpy as np

angulos = np.array([0, np.pi/6, np.pi/4, np.pi/3, np.pi/2])

np.sin(angulos)   # [0.   0.5  0.707  0.866  1.  ]
np.cos(angulos)   # [1.   0.866  0.707  0.5  6.12e-17]
np.tan(angulos)   # [0.   0.577  1.   1.732  1.63e+16]
```

### Conversion grados → radianes

```python
grados = np.array([0, 30, 45, 60, 90])
radianes = np.deg2rad(grados)
np.sin(radianes)   # [0.  0.5  0.707  0.866  1.]
```

### Funciones inversas

```python
valores = np.array([-1.0, 0.0, 0.5, 1.0])
np.arcsin(valores)   # [-pi/2  0.  pi/6  pi/2]
np.arccos(valores)   # [pi  pi/2  pi/3  0.]
np.arctan(valores)   # [-pi/4  0.  pi/6_aprox  pi/4]
```

### Broadcasting

```python
M = np.linspace(0, np.pi, 12).reshape(3, 4)
np.sin(M)   # sin elemento a elemento sobre shape (3, 4)
```

## Notas de este grupo

- [[np.sin]]
- [[np.cos]]
- [[np.tan]]
- [[np.arcsin]]
- [[np.arccos]]
- [[np.arctan]]
- [[np.sinh]]
- [[np.cosh]]
- [[np.tanh]]

## Notas relacionadas

- [[concepto_ufuncs]]
- [[concepto_broadcasting]]
- [[Librerias/Numpy/np/operaciones/index|np/operaciones — ufuncs element-wise]]
