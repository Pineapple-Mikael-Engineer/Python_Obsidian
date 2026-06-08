---
title: np/operaciones/trigonometricas — funciones trigonometricas e hiperbolicas (ufuncs)
tags:
  - numpy
  - indice
draft: false
---

# np/operaciones/trigonometricas — funciones trigonometricas e hiperbolicas (ufuncs)

Las 9 [[concepto_ufuncs|ufuncs]] trigonometricas e hiperbolicas de NumPy. Son la base de cualquier calculo periodico, de senales o geometrico. **Trabajan en radianes**, tanto en entrada como en salida — para convertir: `np.deg2rad(angulos)` o `angulos * np.pi / 180`.

## Funciones de este grupo

| Grupo | ufunc | Descripcion |
|---|---|---|
| **Principales** | [[np.sin]] | seno; rango de salida [-1, 1] |
| | [[np.cos]] | coseno; rango de salida [-1, 1] |
| | [[np.tan]] | tangente; tiene singularidades en pi/2 + n*pi donde devuelve valores muy grandes pero no lanza error |
| **Inversas** | [[np.arcsin]] | arcoseno; dominio [-1, 1], rango [-pi/2, pi/2] |
| | [[np.arccos]] | arcocoseno; dominio [-1, 1], rango [0, pi] |
| | [[np.arctan]] | arcotangente, rango (-pi/2, pi/2); para el angulo correcto en todos los cuadrantes usar `np.arctan2(y, x)` |
| **Hiperbolicas** | [[np.sinh]] | seno hiperbolico; crece exponencialmente, para x grande puede dar overflow |
| | [[np.cosh]] | coseno hiperbolico; siempre >= 1 |
| | [[np.tanh]] | tangente hiperbolica; rango (-1, 1), muy usada como funcion de activacion en redes neuronales |

## Notas relacionadas

- [[concepto_ufuncs]]
- [[concepto_broadcasting]]
- [[Librerias/Numpy/np/operaciones/index\|np/operaciones — ufuncs element-wise]]
