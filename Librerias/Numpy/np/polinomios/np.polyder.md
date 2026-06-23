---
title: np.polyder — derivada de un polinomio (baja el grado)
aliases:
  - polyder
  - np.polyder
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

# np.polyder — derivada de un polinomio (baja el grado)

`np.polyder` calcula la **derivada** de un polinomio operando directamente sobre sus coeficientes —no es diferenciación numérica, es cálculo **exacto**—. Cada derivación **baja el grado en uno**: un polinomio de grado $n$ se convierte en uno de grado $n-1$. Devuelve los coeficientes de la derivada (o un objeto [[np.poly1d]] si la entrada lo era). Su inversa es [[np.polyint]].

## La idea

La derivada de cada monomio es la regla de la potencia: $\dfrac{d}{dx}\,x^{k} = k\,x^{k-1}$. Para un polinomio

$$
p(x) = \sum_{i=0}^{n} c_i\,x^{\,n-i}
\qquad\Longrightarrow\qquad
p'(x) = \sum_{i=0}^{n-1} (n-i)\,c_i\,x^{\,n-i-1}
$$

cada coeficiente se multiplica por su exponente y el término constante desaparece. En forma concreta, para grado 3:

$$
p(x) = a x^{3} + b x^{2} + c x + d
\qquad\Longrightarrow\qquad
p'(x) = 3a\,x^{2} + 2b\,x + c
$$

El array de coeficientes pasa de longitud $n+1$ a longitud $n$ (un grado menos por cada orden de derivación `m`).

## Firma

```python
np.polyder(
    p,             # array_like (mayor→menor grado) o poly1d: el polinomio
    m=1,           # int: orden de derivación (cuántas veces derivar)
) -> ndarray | poly1d
```

## Los parámetros en detalle

### `p` — el polinomio
`array_like` 1D en orden **descendente** de potencias, o un objeto [[np.poly1d]]. Si pasas un `poly1d`, el retorno también es `poly1d`; si pasas un array crudo, el retorno es un `ndarray` de coeficientes.

### `m` — orden de derivación
`int` no negativo (defecto `1`). Número de veces que se deriva: `m=2` da la segunda derivada. Cada unidad de `m` baja el grado en uno; si `m` supera el grado, el resultado es el polinomio cero.

```python
import numpy as np
# x³ + 2x² + 3x + 4  →  3x² + 4x + 3
np.polyder([1, 2, 3, 4])      # array([3, 4, 3])

# 2ª derivada de x³ es 6x
np.polyder([1, 0, 0, 0], 2)   # array([6, 0])
```

## Casos de uso

### Velocidad y aceleración desde una posición polinómica
```python
pos = np.poly1d(np.polyfit(t, x, 3))   # posición ajustada
vel = np.polyder(pos)                  # velocidad (poly1d)
acc = np.polyder(pos, 2)               # aceleración
```

### Encontrar extremos (derivada = 0)
```python
p = np.poly1d([1, 0, -3, 0])   # x³ - 3x
criticos = np.roots(np.polyder(p))   # x donde la pendiente se anula
```

### Equivalencia con poly1d
```python
p = np.poly1d([1, 2, 3, 4])
p.deriv()                      # equivale a np.polyder(p)
p.deriv(2)                     # segunda derivada
```

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| Orden de coeficientes invertido | asumir orden ascendente | la convención es **descendente** (mayor → menor grado) |
| Resultado cero inesperado | `m` mayor que el grado del polinomio | bajar `m` o revisar el grado de `p` |
| Esperar `poly1d` y recibir array | se pasó un array crudo, no un `poly1d` | pasar `np.poly1d(p)` si quieres objeto |

## Notas relacionadas

- [[np.polyint]] — la operación inversa (integral, sube el grado)
- [[concepto_shape]] — el array de coeficientes pierde un elemento por derivación
- [[np.poly1d]] — el método `p.deriv()` equivale a `np.polyder`
- [[np.roots]] — raíces de la derivada para hallar máximos/mínimos
- [[index]] — API legacy de polinomios
