---
title: np/polinomios — API legacy de polinomios
tags:
  - numpy
  - indice
draft: false
---

# np/polinomios — API legacy de polinomios

`polinomios/` agrupa la API clasica de NumPy para trabajar con polinomios representados como arrays de coeficientes en orden descendente de potencias. Es la API **legacy**: NumPy recomienda `numpy.polynomial` para codigo nuevo, pero esta sigue siendo ampliamente usada y suficiente para la mayoria de casos de ingenieria.

> La representacion es un array `[a_n, a_{n-1}, ..., a_1, a_0]` donde el primer elemento es el coeficiente del termino de mayor grado.

## Tabla de decision

| Necesito… | Funcion |
|-----------|---------|
| Crear un objeto polinomio desde coeficientes | [[np.poly1d]] |
| Ajustar un polinomio a datos (minimos cuadrados) | [[np.polyfit]] |
| Evaluar un polinomio en uno o varios puntos | [[np.polyval]] |
| Derivar un polinomio | [[np.polyder]] |
| Integrar un polinomio | [[np.polyint]] |
| Encontrar las raices de un polinomio | [[np.roots]] |

## Ejemplo completo

```python
import numpy as np

# Definir p(x) = 2x^2 - 3x + 1
coefs = [2, -3, 1]
p = np.poly1d(coefs)

print(p)          # muestra la expresion algebraica
p(2)              # evaluar en x=2:  2*4 - 3*2 + 1 = 3
np.polyval(coefs, 2)   # equivalente sin poly1d

# Derivada: p'(x) = 4x - 3
dp = np.polyder(p)

# Integral: P(x) = (2/3)x^3 - (3/2)x^2 + x + C
P = np.polyint(p)

# Raices de p(x) = 0
np.roots(coefs)    # [1. , 0.5]

# Ajuste a datos
x = np.array([0, 1, 2, 3])
y = np.array([1, 0, 3, 10])
coefs_fit = np.polyfit(x, y, deg=2)   # polinomio de grado 2
```

## Nota sobre la API moderna

Para necesidades mas avanzadas (mejor condicionamiento numerico, distintas bases como Chebyshev o Legendre), usar `numpy.polynomial.polynomial.Polynomial` en su lugar.

## Notas de la carpeta

- [[np.poly1d]] — objeto que encapsula un polinomio y permite operaciones algebraicas
- [[np.polyfit]] — ajuste polinomial por minimos cuadrados
- [[np.polyval]] — evaluacion de un polinomio en puntos dados
- [[np.polyder]] — derivacion simbolica de un polinomio
- [[np.polyint]] — integracion simbolica de un polinomio
- [[np.roots]] — calculo de las raices de un polinomio
