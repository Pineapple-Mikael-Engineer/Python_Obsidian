---
title: np/polinomios — API legacy de polinomios
tags:
  - numpy
  - indice
draft: false
---

# np/polinomios — API legacy de polinomios

Este grupo cubre la API clasica de NumPy para trabajar con polinomios. La representacion es simple: un array de coeficientes en orden descendente de potencias. Por ejemplo, `3x^2 + 2x + 1` se escribe `[3, 2, 1]` — el primer elemento siempre es el coeficiente del termino de mayor grado.

Es una API **legacy**: NumPy recomienda `numpy.polynomial` para codigo nuevo porque tiene mejor condicionamiento numerico y soporta distintas bases (Chebyshev, Legendre, Hermite). Pero la API de `np.poly*` sigue siendo ampliamente usada, es suficiente para la mayoria de problemas de ingenieria, y aparece frecuentemente en codigo existente.

## Notas de la carpeta

- [[np.poly1d]] — objeto que encapsula un polinomio y lo hace tratable como una funcion Python. Soporta evaluacion con `p(x)`, suma `p1 + p2`, multiplicacion `p1 * p2` y derivacion `p.deriv()`. Es el punto de entrada de la API: las demas funciones aceptan tanto arrays de coeficientes como objetos `poly1d`.
- [[np.polyfit]] — ajusta un polinomio de grado `deg` a datos `(x, y)` por minimos cuadrados. Devuelve los coeficientes del polinomio ajustado. Equivale a regresion polinomial; para grados altos puede ser numericamente inestable.
- [[np.polyval]] — evalua el polinomio `p` (array de coeficientes o `poly1d`) en los valores `x`. Para un objeto `poly1d`, equivale a llamar `p(x)` directamente; util cuando se trabaja con coeficientes crudos sin crear el objeto.
- [[np.polyder]] — calcula la derivada de orden `m` del polinomio `p`. Devuelve los coeficientes de la derivada como array — no usa diferenciacion numerica, es calculo exacto sobre los coeficientes.
- [[np.polyint]] — calcula la integral indefinida de orden `m` del polinomio `p`. La constante de integracion es cero por defecto; se puede especificar con `k=`. Tambien exacto sobre coeficientes.
- [[np.roots]] — calcula las raices del polinomio `p` (los valores de x donde p(x) = 0). Puede devolver raices complejas si el polinomio no tiene todas las raices reales. Internamente construye la matriz companera y calcula sus eigenvalues.
