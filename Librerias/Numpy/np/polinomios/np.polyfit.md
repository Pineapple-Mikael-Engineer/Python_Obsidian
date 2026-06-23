---
title: np.polyfit — ajusta un polinomio de grado deg por mínimos cuadrados
aliases:
  - polyfit
  - np.polyfit
  - ajuste polinomial
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
  - concepto_shape
draft: false
---

# np.polyfit — ajusta un polinomio de grado `deg` por mínimos cuadrados

`np.polyfit` busca el polinomio de grado `deg` que **mejor ajusta** una nube de puntos $(x_i, y_i)$ en el sentido de los **mínimos cuadrados**: minimiza la suma de los cuadrados de los residuos. Devuelve los coeficientes (en orden descendente de potencias), listos para pasar a [[np.polyval]] o a [[np.poly1d]]. Por dentro plantea un sistema lineal con la matriz de **Vandermonde** y lo resuelve con [[np.linalg.lstsq]]. Es la regresión polinómica de NumPy.

## La idea

Se busca el polinomio $p(x) = \sum_{j=0}^{n} c_j\,x^{\,n-j}$ (grado $n = \text{deg}$) que minimiza el error cuadrático sobre los $m+1$ datos:

$$
\min_{c}\ \sum_{i=0}^{m} \big(\,p(x_i) - y_i\,\big)^2
\;=\;
\min_{c}\ \lVert V\mathbf{c} - \mathbf{y}\rVert_2^{2}
$$

donde $V$ es la **matriz de Vandermonde** que evalúa cada potencia en cada punto. Para $m+1$ puntos y grado $n$:

$$
V \;=\;
\begin{bmatrix}
x_0^{\,n} & x_0^{\,n-1} & \dots & x_0 & 1 \\
x_1^{\,n} & x_1^{\,n-1} & \dots & x_1 & 1 \\
\vdots    & \vdots      &       & \vdots & \vdots \\
x_m^{\,n} & x_m^{\,n-1} & \dots & x_m & 1
\end{bmatrix}
\qquad
V\mathbf{c} =
\begin{bmatrix} p(x_0) \\ p(x_1) \\ \vdots \\ p(x_m) \end{bmatrix}
$$

El sistema $V\mathbf{c} = \mathbf{y}$ está **sobredeterminado** (más filas que columnas cuando hay más datos que coeficientes), así que no tiene solución exacta: [[np.linalg.lstsq]] devuelve el $\mathbf{c}$ que minimiza el residuo. Esos coeficientes son justo lo que retorna `polyfit`.

## Firma

```python
np.polyfit(
    x,                 # array_like 1D: abscisas de los datos
    y,                 # array_like (M,) o (M, K): ordenadas (K ajustes a la vez)
    deg,               # int: grado del polinomio a ajustar
    rcond=None,        # float: corte de valores singulares (regularización de rango)
    full=False,        # bool: si True, devuelve también diagnósticos del lstsq
    w=None,            # array_like (M,): pesos por punto
    cov=False,         # bool|str: si True, devuelve la matriz de covarianza
) -> ndarray            # coeficientes (mayor→menor grado); o tupla si full/cov
```

## Los parámetros en detalle

### `x`, `y` — los datos
`x` es `array_like` 1D de shape `(M,)`. `y` es `(M,)` o `(M, K)`: con `(M, K)` ajusta **`K` polinomios a la vez** compartiendo las mismas abscisas (cada columna es un conjunto de ordenadas). El número de filas $M$ debe coincidir.

### `deg` — grado del polinomio
`int`. El retorno tiene `deg + 1` coeficientes. Conviene tener $M \ge \text{deg}+1$ puntos; con grados altos el ajuste **sobreajusta** (oscilaciones de Runge) y la Vandermonde se mal condiciona.

| `deg` | Retorno | Modelo |
|-------|---------|--------|
| `1` | `[m, b]` | recta $m\,x + b$ |
| `2` | `[a, b, c]` | parábola $a\,x^2 + b\,x + c$ |

### `rcond` — corte de valores singulares
`float`. Los valores singulares de $V$ menores que `rcond * s.max()` se descartan, estabilizando el ajuste cuando $V$ es casi degenerada. Por defecto `len(x)*eps`. Es el mismo `rcond` de [[np.linalg.lstsq]].

### `w` — pesos por punto
`array_like` de shape `(M,)`. Cada residuo se multiplica por `w[i]`; los puntos con más peso pesan más en el ajuste. Para ponderar por incertidumbre $\sigma_i$, se usa `w = 1/sigma`.

### `full` — devolver diagnósticos del solver
`bool` (defecto `False`). Si `True`, devuelve `(coef, residuals, rank, singular_values, rcond)` —los extras vienen directos de [[np.linalg.lstsq]]— útil para comprobar el rango y el residuo.

### `cov` — matriz de covarianza
`bool` o `'unscaled'`. Si `True`, devuelve `(coef, cov)` con la covarianza estimada de los coeficientes, base para barras de error. Incompatible con `full=True`.

## Casos de uso

### Ajuste de una parábola
```python
import numpy as np
x = np.array([0, 1, 2, 3])
y = np.array([1, 3, 7, 13])
coef = np.polyfit(x, y, 2)        # [1., 1., 1.] → x² + x + 1
```

### Regresión lineal simple (recta)
```python
m, b = np.polyfit(x, y, 1)        # pendiente, intercepto
```

### Ajustar y evaluar (flujo completo)
```python
coef = np.polyfit(x, y, 3)
x_fino = np.linspace(x.min(), x.max(), 200)
y_fino = np.polyval(coef, x_fino)     # curva suave
p = np.poly1d(coef)                   # o como objeto manipulable
```

### Tendencia de una serie temporal
```python
pendiente = np.polyfit(np.arange(len(serie)), serie, 1)[0]
```

### Diagnóstico con full=True
```python
coef, resid, rank, sv, rc = np.polyfit(x, y, 2, full=True)
resid            # suma de residuos al cuadrado
rank             # rango efectivo de la Vandermonde
```

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| `RankWarning: Polyfit may be poorly conditioned` | grado alto o `x` sin escalar | bajar `deg`, normalizar `x`, o usar la API moderna |
| Predicciones absurdas fuera del rango | extrapolación | no extrapolar lejos de los datos |
| Coeficientes en orden inesperado al evaluar | mezclar con la API moderna (orden ascendente) | mantener todo en `np.poly*` (descendente) |
| Sobreajuste (curva que oscila entre puntos) | `deg` demasiado alto | usar el grado mínimo que capture la tendencia |
| `TypeError`/error de shape | `x` e `y` de distinta longitud | asegurar `len(x) == len(y)` |

## Notas relacionadas

- [[np.linalg.lstsq]] — el solver de mínimos cuadrados que resuelve $V\mathbf{c}=\mathbf{y}$
- [[concepto_shape]] — el sistema sobredeterminado $(M, \text{deg}+1)$
- [[np.polyval]] — evaluar el polinomio ajustado
- [[np.poly1d]] — envolver `coef` en un objeto manipulable
- [[np.roots]] — raíces del polinomio ajustado
- [[index]] — API legacy de polinomios
