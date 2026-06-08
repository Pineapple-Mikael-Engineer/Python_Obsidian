---
title: np/operaciones — ufuncs element-wise
tags:
  - numpy
  - indice
draft: false
---

# np/operaciones — ufuncs element-wise

`operaciones/` agrupa las [[concepto_ufuncs|ufuncs]] (universal functions) de NumPy que operan **elemento a elemento** sobre arrays de cualquier shape. Son funciones compiladas en C — no bucles Python — y comparten una interfaz uniforme que las distingue de cualquier funcion de Python puro.

## Que hace a una ufunc diferente

Cualquier operacion aritmetica o matematica que se escribe con operadores Python (`+`, `-`, `*`, `/`, `**`, `%`) tiene su ufunc equivalente (`np.add`, `np.subtract`, etc.). La diferencia no es el resultado — es la interfaz:

- **`out=`** — escribe el resultado directamente en un buffer preasignado, sin crear un array nuevo. Critico en bucles de calculo iterativo o animacion donde cada allocation importa.
- **`where=`** — aplica la operacion solo donde una mascara booleana es `True`. Los demas elementos del array `out` quedan intactos.
- **Broadcasting automatico** — alinean shapes sin copiar datos, identico al comportamiento de los operadores.

## Subcarpetas

| Subcarpeta | Funciones |
|---|---|
| [[Librerias/Numpy/np/operaciones/aritmeticas/index\|aritmeticas/]] | `add`, `subtract`, `multiply`, `divide`, `power`, `mod` — las 6 operaciones basicas como ufuncs |
| [[Librerias/Numpy/np/operaciones/trigonometricas/index\|trigonometricas/]] | `sin`, `cos`, `tan`, `arcsin`, `arccos`, `arctan`, `sinh`, `cosh`, `tanh` — trabajan en radianes |
| [[Librerias/Numpy/np/operaciones/exponenciales_log/index\|exponenciales_log/]] | `exp`, `expm1`, `log`, `log2`, `log10`, `sqrt`, `square` — incluye variantes numericamente estables |
| [[Librerias/Numpy/np/operaciones/redondeo_signo/index\|redondeo_signo/]] | `abs`, `fabs`, `sign`, `ceil` — valor absoluto, signo y redondeo hacia arriba |

## Notas relacionadas

- [[concepto_ufuncs]]
- [[concepto_broadcasting]]
