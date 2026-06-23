---
title: np.polyint — integral indefinida de un polinomio (sube el grado)
aliases:
  - polyint
  - np.polyint
tags:
  - numpy
  - api/funcion
  - polinomios
lib: numpy
mod: np
tipo: funcion
retorna: ndarray | poly1d
inplace: false
requiere:
  - concepto_shape
draft: false
---

# np.polyint — integral indefinida de un polinomio (sube el grado)

`np.polyint` calcula la **integral indefinida** (antiderivada) de un polinomio operando de forma **exacta** sobre sus coeficientes. Es la operación inversa de [[np.polyder]]: cada integración **sube el grado en uno** e introduce una **constante de integración** `k` (por defecto `0`). Devuelve los coeficientes de la antiderivada (o un objeto [[np.poly1d]] si la entrada lo era).

## La idea

La integral de cada monomio es la regla inversa de la potencia: $\displaystyle\int x^{k}\,dx = \dfrac{x^{k+1}}{k+1}$. Para un polinomio

$$
p(x) = \sum_{i=0}^{n} c_i\,x^{\,n-i}
\qquad\Longrightarrow\qquad
P(x) = \int p(x)\,dx = \sum_{i=0}^{n} \frac{c_i}{\,n-i+1\,}\,x^{\,n-i+1} \;+\; k
$$

cada coeficiente se divide por su **nuevo** exponente y se añade la constante $k$. En forma concreta, para grado 2:

$$
p(x) = a x^{2} + b x + c
\qquad\Longrightarrow\qquad
P(x) = \frac{a}{3}x^{3} + \frac{b}{2}x^{2} + c\,x + k
$$

El array de coeficientes pasa de longitud $n+1$ a longitud $n+2$ (un grado más por cada orden de integración `m`).

## Firma

```python
np.polyint(
    p,             # array_like (mayor→menor grado) o poly1d: el polinomio
    m=1,           # int: orden de integración (cuántas veces integrar)
    k=None,        # escalar o lista: constante(s) de integración (una por orden)
) -> ndarray | poly1d
```

## Los parámetros en detalle

### `p` — el polinomio
`array_like` 1D en orden **descendente** de potencias, o un objeto [[np.poly1d]]. Si pasas un `poly1d`, el retorno también es `poly1d`; si pasas un array crudo, devuelve un `ndarray` de coeficientes.

### `m` — orden de integración
`int` no negativo (defecto `1`). Número de veces que se integra: `m=2` da la doble antiderivada. Cada unidad de `m` sube el grado en uno.

### `k` — constante(s) de integración
Escalar o lista (defecto `0` para todas). Es lo que distingue la integral indefinida: la antiderivada no es única. Con `m > 1` se pasa **una constante por cada integración** (lista de longitud `m`); estas fijan las condiciones iniciales.

```python
import numpy as np
# 3x² + 2x  →  x³ + x² + C   (C = 0 por defecto)
np.polyint([3, 2, 0])         # array([1., 1., 0., 0.])

# constante explícita: integral de 2x es x² + 5
np.polyint([2, 0], k=5)       # array([1., 0., 5.])
```

## Casos de uso

### Recuperar la posición desde la velocidad (condición inicial)
```python
v = np.poly1d([2, 1])         # velocidad: 2t + 1
x = np.polyint(v, k=[x0])     # posición con x(0) = x0
```

### Doble integración (aceleración → posición)
```python
a = np.poly1d([6, 0])         # aceleración constante reescalada
# k=[v0, x0]: una constante por cada integración
pos = np.polyint(a, m=2, k=[v0, x0])
```

### Equivalencia con poly1d
```python
p = np.poly1d([3, 2, 0])
p.integ()                     # equivale a np.polyint(p)
p.integ(k=5)                  # con constante de integración
```

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| Constante de integración perdida | no se pasó `k` (se asume `0`) | indicar `k` para la condición inicial |
| `m>1` con una sola constante | `k` debe tener `m` elementos | pasar una lista `k=[k1, k2, ...]` de longitud `m` |
| Orden de coeficientes invertido | asumir orden ascendente | la convención es **descendente** (mayor → menor grado) |

## Notas relacionadas

- [[np.polyder]] — la operación inversa (derivada, baja el grado)
- [[concepto_shape]] — el array de coeficientes gana un elemento por integración
- [[np.poly1d]] — el método `p.integ()` equivale a `np.polyint`
- [[index]] — API legacy de polinomios
