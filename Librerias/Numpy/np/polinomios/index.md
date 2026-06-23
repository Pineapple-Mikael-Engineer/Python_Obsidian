---
title: np/polinomios — representar, evaluar, ajustar y derivar polinomios (API legacy)
tags:
  - numpy
  - indice
draft: false
---

# np/polinomios — representar, evaluar, ajustar y derivar polinomios

Esta carpeta cubre la API **clásica (legacy)** de NumPy para trabajar con polinomios de una variable. La representación es un simple array de **coeficientes en orden descendente** de potencias: `[1, -3, 2]` es

$$
1\cdot x^{2} - 3\cdot x + 2 \;=\; x^{2} - 3x + 2
$$

El primer elemento es siempre el coeficiente del término de mayor grado. Sobre esa representación, las funciones de esta carpeta permiten **representar** un polinomio como objeto ([[np.poly1d]]), **evaluarlo** ([[np.polyval]]), **ajustarlo** a datos ([[np.polyfit]]), hallar sus **raíces** ([[np.roots]]) y calcular su **derivada** e **integral** ([[np.polyder]], [[np.polyint]]).

> [!warning] Existe una API moderna recomendada: `np.polynomial.Polynomial`
> Las funciones `np.poly1d`, `np.polyfit`, `np.polyval`, etc. son **legacy**. Para código nuevo, NumPy recomienda el paquete `numpy.polynomial` (clase `np.polynomial.Polynomial` y `Polynomial.fit`), que tiene **mejor condicionamiento numérico**, soporta otras bases (Chebyshev, Legendre, Hermite) y usa orden **ascendente** de coeficientes. Aun así, la API legacy sigue siendo omnipresente en código existente y es suficiente para la mayoría de problemas; es la que se documenta aquí.

## Notas de la carpeta

| Nota | Tipo | Qué hace | Idea |
|------|------|----------|------|
| [[np.poly1d]] | clase | representa un polinomio como objeto callable y operable | `poly1d([1,-3,2])` = $x^2-3x+2$ |
| [[np.polyval]] | función | evalúa un polinomio de coeficientes en puntos `x` | $p(x)=\sum_i c_i\,x^{n-i}$, vectorizado |
| [[np.polyfit]] | función | ajusta un polinomio de grado `deg` por mínimos cuadrados | resuelve $V\mathbf{c}=\mathbf{y}$ con la Vandermonde |
| [[np.roots]] | función | raíces del polinomio ($p(x)=0$) | autovalores de la matriz companion |
| [[np.polyder]] | función | derivada del polinomio (baja el grado) | regla de la potencia, exacta |
| [[np.polyint]] | función | integral indefinida (sube el grado, constante `k`) | inversa de la derivada |

## El flujo típico

1. **Ajustar** datos: `coef = np.polyfit(x, y, deg)` — internamente plantea la matriz de Vandermonde y la resuelve con [[np.linalg.lstsq]].
2. **Evaluar** el ajuste: `y_pred = np.polyval(coef, x_nuevo)`.
3. **Manipular** como objeto: `p = np.poly1d(coef)`, y entonces `p(x)`, `p.deriv()`, `p.integ()`, `p.r`.
4. **Analizar**: [[np.roots]] para las raíces, [[np.polyder]] + [[np.roots]] para los extremos.

## Notas relacionadas

- [[np.linalg.lstsq]] — el solver de mínimos cuadrados detrás de [[np.polyfit]]
- [[np.linalg.eigvals]] — los autovalores que [[np.roots]] usa sobre la matriz companion
- [[Tree Numpy]] — árbol general de la librería
