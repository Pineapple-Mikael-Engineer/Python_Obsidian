---
title: np/operaciones/exponenciales_log — exponenciales, logaritmos, potencias y raíces (ufuncs)
tags:
  - numpy
  - indice
draft: false
---

# np/operaciones/exponenciales_log — exponenciales, logaritmos, potencias y raíces (ufuncs)

Este grupo reúne las [[concepto_ufuncs|ufuncs]] **unarias element-wise** de NumPy para
**exponenciales**, **logaritmos**, **potencias** y **raíces**. Todas aplican una función escalar a
cada elemento de forma independiente, **conservan el shape** y heredan los parámetros comunes de
ufunc (`out`, `where`, `dtype`, `casting`). Son la base del cálculo numérico, los cambios de escala y
la estabilidad numérica. Varias vienen en pares **inverso** (una deshace a la otra) y algunas tienen
variantes "numéricamente seguras" para valores cercanos a cero.

## Pares inversos

Cada exponencial tiene su logaritmo, y cada potencia su raíz. Leer la tabla en horizontal es leer
"una función y la que la deshace":

| Directa | Inversa | Relación |
|---|---|---|
| [[np.exp]] ($e^x$) | [[np.log]] ($\ln x$) | $\log(\exp x) = x$ |
| [[np.exp2]] ($2^x$) | [[np.log2]] ($\log_2 x$) | base 2 |
| [[np.expm1]] ($e^x - 1$) | [[np.log1p]] ($\ln(1+x)$) | precisión cerca de $x=0$ |
| [[np.square]] ($x^2$) | [[np.sqrt]] ($\sqrt{x}$) | inversa para $x \ge 0$ |
| (cubo $x^3$) | [[np.cbrt]] ($\sqrt[3]{x}$) | la raíz cúbica admite negativos |
| potencia general $x^y$ → [[np.power]] | — | exponente arbitrario |
| [[np.reciprocal]] ($1/x$) | (autoinversa) | $1/(1/x) = x$ |

## Nota sobre el dominio

- [[np.log]], [[np.log2]], [[np.log10]] y [[np.sqrt]] **no están definidas para negativos en reales**:
  devuelven `nan` con `RuntimeWarning` (y `log(0)` da `-inf`). Para raíces de negativos hay que usar
  entrada compleja o `dtype=complex`.
- [[np.cbrt]] es la excepción útil: toma la **raíz real**, así que sí admite negativos
  (`np.cbrt(-8) == -2.0`), donde `(-8) ** (1/3)` da `nan`.
- [[np.reciprocal]] con **enteros** hace división entera (casi todo `0`); usa floats.
- Las variantes [[np.expm1]] / [[np.log1p]] existen para conservar **precisión en valores pequeños**,
  donde `exp(x) - 1` o `log(1 + x)` pierden dígitos por cancelación catastrófica.

## Notas de este grupo

- **Exponenciales** — [[np.exp]] · [[np.exp2]] · [[np.expm1]]
- **Logaritmos** — [[np.log]] · [[np.log2]] · [[np.log10]] · [[np.log1p]]
- **Potencias** — [[np.power]] · [[np.square]] · [[np.reciprocal]]
- **Raíces** — [[np.sqrt]] · [[np.cbrt]]

## Notas relacionadas

- [[concepto_ufuncs]] — el motor element-wise del que todas heredan
- [[concepto_broadcasting]] — cómo se alinean las entradas
- [[Librerias/Numpy/np/operaciones/index\|np/operaciones — ufuncs element-wise]]
