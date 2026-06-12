---
title: sympy.calculus/series — series
tags:
  - sympy
  - indice
draft: false
---

# series

Los **desarrollos en serie** en SymPy: aproximar una funcion por una suma de terminos mas simples, con coeficientes exactos. Hay dos enfoques bien distintos segun lo que se quiera aproximar, y esta carpeta los reune para decidir entre ellos: la serie de **Taylor/Laurent** (aproximacion **local**, en potencias de `x`) y la serie de **Fourier** (aproximacion **global** de funciones periodicas, en armonicos seno/coseno).

A diferencia del resto de `sympy.calculus`, aqui el patron funcion-vs-clase-sin-evaluar no aplica de la forma habitual: las dos herramientas son funciones que evaluan. [[sympy.series]] devuelve una `Expr` truncada con un termino de orden `O(...)`; [[sympy.fourier_series]] devuelve un objeto `FourierSeries` **perezoso** (suma infinita) que se materializa con `.truncate(n)`.

```python
from sympy import symbols, exp, fourier_series, pi
x = symbols("x")

exp(x).series(x, 0, 4)               # 1 + x + x**2/2 + x**3/6 + O(x**4)   -> Taylor local
fourier_series(x, (x, -pi, pi)).truncate(3)  # 2*sin(x) - sin(2*x) + 2*sin(3*x)/3   -> Fourier global
```

## Como se relacionan

| Aspecto | `series` (Taylor/Laurent) | `fourier_series` (Fourier) |
|---------|---------------------------|----------------------------|
| Aproxima | una funcion **cerca de un punto** `x0` | una funcion **periodica** en todo el periodo |
| Base | potencias `(x - x0)**n` | armonicos `sin(n*x)`, `cos(n*x)` |
| Alcance | **local** (mejor cuanto mas cerca de `x0`) | **global** sobre el periodo `(a, b)` |
| Devuelve | `Expr` truncada + termino `O(...)` | `FourierSeries` perezoso; `.truncate(n)` |
| Cuando usarla | linealizar, aproximar local, calcular limites | descomponer señales periodicas (onda cuadrada, sierra) |
| Polo en `x0` | pasa a **Laurent** (potencias negativas) | no aplica |

Regla practica: si quieres una aproximacion **alrededor de un punto** (o linealizar un modelo) usa `series`; si la funcion es **periodica** y quieres descomponerla en sus frecuencias usa `fourier_series`. Ambas dan coeficientes exactos y se compilan a numerico con [[sympy.lambdify]] tras quitar el resto (`.removeO()` o `.truncate(n)`).

## Notas

- [[sympy.series | sympy.series]] — desarrollo de Taylor (o Laurent si hay polo) alrededor de `x0`; aproximacion local en potencias de `x`.
- [[sympy.fourier_series | sympy.fourier_series]] — desarrollo de Fourier de una funcion periodica; aproximacion global en armonicos seno/coseno.

## Notas relacionadas

- [[sympy.calculus/index | sympy.calculus]]
