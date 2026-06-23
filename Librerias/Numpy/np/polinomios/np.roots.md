---
title: np.roots — raíces de un polinomio vía autovalores de la matriz companion
aliases:
  - roots
  - np.roots
  - raices
tags:
  - numpy
  - api/funcion
  - polinomios
lib: numpy
mod: np
tipo: funcion
retorna: ndarray
inplace: false
requiere:
  - concepto_dtype
draft: false
---

# np.roots — raíces de un polinomio vía autovalores de la matriz companion

`np.roots` calcula las **raíces** de un polinomio: los valores de $x$ donde $p(x) = 0$. Un polinomio de grado $n$ tiene $n$ raíces (contando multiplicidad), que pueden ser **reales o complejas**. NumPy no busca las raíces analíticamente: construye la **matriz companion** del polinomio y devuelve sus **autovalores**, porque las raíces de $p$ son exactamente los autovalores de esa matriz. El cálculo se delega en [[np.linalg.eigvals]].

## La idea

Para un polinomio mónico (se normaliza dividiendo por $c_0$)

$$
p(x) = x^{n} + a_{1}x^{n-1} + a_{2}x^{n-2} + \dots + a_{n-1}x + a_{n}
$$

se forma su **matriz companion** $C$, una matriz $n\times n$ cuyos autovalores son precisamente las raíces de $p$:

$$
C \;=\;
\begin{bmatrix}
-a_{1} & -a_{2} & \dots & -a_{n-1} & -a_{n} \\
1 & 0 & \dots & 0 & 0 \\
0 & 1 & \dots & 0 & 0 \\
\vdots & & \ddots & & \vdots \\
0 & 0 & \dots & 1 & 0
\end{bmatrix}
$$

Su polinomio característico cumple $\det(C - x I) = (-1)^{n}\,p(x)$, de modo que

$$
p(x) = 0 \iff x \ \text{es autovalor de } C.
$$

Así, hallar raíces se reduce a un problema de **autovalores**, que [[np.linalg.eigvals]] resuelve de forma robusta. Por eso las raíces pueden salir complejas aunque los coeficientes sean reales.

## Firma

```python
np.roots(p) -> ndarray
```

## Los parámetros en detalle

### `p` — coeficientes del polinomio
`array_like` 1D (o un objeto [[np.poly1d]]) en orden **descendente** de potencias: `[1, -5, 6]` representa $x^2 - 5x + 6$. Los ceros iniciales (coeficientes de mayor grado nulos) se recortan; los ceros finales se interpretan como raíces en el origen ($x = 0$). El grado efectivo determina cuántas raíces se devuelven.

```python
import numpy as np
# x² - 5x + 6 = (x-2)(x-3)
np.roots([1, -5, 6])     # array([3., 2.])

# x² + 1 → raíces complejas conjugadas
np.roots([1, 0, 1])      # array([0.+1.j, 0.-1.j])
```

## Casos de uso

### Resolver una ecuación polinómica
```python
# 2x³ - 3x² - 11x + 6 = 0
np.roots([2, -3, -11, 6])     # array([ 3. , -2. ,  0.5])
```

### Puntos críticos de un polinomio (derivada = 0)
```python
p = np.poly1d([1, 0, -3, 0])   # x³ - 3x
criticos = np.roots(np.polyder(p))   # donde la pendiente se anula
```

### Filtrar solo las raíces reales
```python
r = np.roots([1, 0, 1, 0])     # mezcla de reales y complejas
reales = r[np.isreal(r)].real  # quedarse con las reales
```

### Equivalencia con poly1d
```python
p = np.poly1d([1, -5, 6])
p.r                            # array([3., 2.])  → idéntico a np.roots(p.c)
```

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| Raíces complejas inesperadas | el polinomio no tiene todas reales | filtrar con `np.isreal` / `r.real` |
| Parte imaginaria residual diminuta | error numérico del cálculo de autovalores | tomar `.real` si la imaginaria es despreciable |
| Faltan o sobran raíces | ceros iniciales/finales en `p` cambian el grado efectivo | revisar el vector de coeficientes |
| Resultados imprecisos con grados altos o raíces múltiples | mal condicionamiento de la companion | reducir el grado o usar `np.polynomial` (API moderna) |

## Notas relacionadas

- [[np.linalg.eigvals]] — los autovalores de la matriz companion que son las raíces
- [[concepto_dtype]] — por qué el retorno puede promover a complejo
- [[np.poly1d]] — el atributo `p.r` equivale a `np.roots`
- [[np.polyder]] — raíces de la derivada para hallar extremos
- [[np.polyfit]] — raíces de un polinomio ajustado
- [[index]] — API legacy de polinomios
