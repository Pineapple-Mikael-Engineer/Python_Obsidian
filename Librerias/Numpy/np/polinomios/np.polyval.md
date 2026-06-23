---
title: np.polyval — evalúa un polinomio de coeficientes en uno o varios puntos
aliases:
  - polyval
  - np.polyval
tags:
  - numpy
  - api/funcion
  - polinomios
lib: numpy
mod: np
tipo: funcion
retorna: ndarray | escalar
inplace: false
requiere:
  - concepto_broadcasting
draft: false
---

# np.polyval — evalúa un polinomio de coeficientes en uno o varios puntos

`np.polyval` toma un vector de coeficientes `p` (en orden descendente de potencias) y lo **evalúa** en los puntos `x`. Es la pareja natural de [[np.polyfit]] (ajustar → evaluar) y lo que hace por dentro un objeto [[np.poly1d]] cuando se llama con `p(x)`. Está **vectorizado**: si `x` es un array, devuelve un array del mismo shape con el polinomio evaluado elemento a elemento, sin bucle Python.

## La idea

Dados los coeficientes $c = [c_0, c_1, \dots, c_n]$ (mayor a menor grado), el valor del polinomio en un punto $x$ es

$$
p(x) \;=\; c_0\,x^{n} + c_1\,x^{n-1} + \dots + c_{n-1}\,x + c_n \;=\; \sum_{i=0}^{n} c_i\,x^{\,n-i}
$$

Por estabilidad, NumPy no eleva potencias por separado: usa el **esquema de Horner**, que reescribe la suma anidando multiplicaciones,

$$
p(x) = \big(\dots\big((c_0\,x + c_1)\,x + c_2\big)\,x + \dots\big)\,x + c_n
$$

con $n$ multiplicaciones y $n$ sumas en vez de calcular cada $x^k$ aparte.

## Firma

```python
np.polyval(p, x) -> ndarray | escalar
```

## Los parámetros en detalle

### `p` — coeficientes del polinomio
`array_like` 1D (o un objeto [[np.poly1d]]) en orden **descendente** de potencias: `[1, 0, -1]` representa $x^2 - 1$. El elemento `p[0]` es el coeficiente del término de mayor grado. La longitud `len(p)` menos 1 es el grado.

### `x` — punto(s) de evaluación
Escalar, `array_like` o incluso una matriz/`poly1d`. El resultado **hereda el shape de `x`** (cada elemento se evalúa de forma independiente por [[concepto_broadcasting|broadcasting]]). Con `x` escalar el retorno es un escalar; con `x` array, un `ndarray` del mismo shape.

```python
import numpy as np
p = [1, 0, -1]                 # x² - 1
np.polyval(p, 2)               # 3        → escalar (2² - 1)
np.polyval(p, [0, 1, 2])       # array([-1, 0, 3])  → un valor por punto
np.polyval(p, np.zeros((2, 2)))  # array de shape (2, 2), todo -1
```

## Casos de uso

### Predecir con un ajuste
```python
coef = np.polyfit(x, y, 3)
y_pred = np.polyval(coef, x_nuevo)   # mismos coeficientes, evaluados
```

### Curva suave para graficar
```python
x_fino = np.linspace(x.min(), x.max(), 500)
y_fino = np.polyval(coef, x_fino)    # 500 puntos vectorizados
```

### Equivalencia con poly1d
```python
p = np.poly1d([2, -3, 1])    # 2x² - 3x + 1
p(4)                         # 21
np.polyval([2, -3, 1], 4)    # 21  → idénticos; p(x) llama a polyval
```

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| Resultado invertido / absurdo | coeficientes en orden ascendente | la convención es **descendente** (mayor → menor grado) |
| Esperar un escalar y recibir array | `x` era un array de un elemento | el shape del retorno copia el de `x` |
| Confundir con `np.polynomial.polyval` | la API moderna usa orden **ascendente** | no mezclar las dos APIs |

## Notas relacionadas

- [[concepto_broadcasting]] — cómo `x` array produce salida del mismo shape
- [[np.polyfit]] — de dónde salen los coeficientes
- [[np.poly1d]] — `p(x)` equivale a `polyval(p, x)`
- [[index]] — API legacy de polinomios
