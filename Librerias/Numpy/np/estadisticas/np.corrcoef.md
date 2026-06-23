---
title: np.corrcoef — Matriz de correlación de Pearson
aliases:
  - corrcoef
  - np.corrcoef
  - correlacion
tags:
  - numpy
  - api/funcion
  - estadistica

# --- Clasificación ---
lib: numpy
mod: np
tipo: funcion

# --- Comportamiento ---
retorna: ndarray
inplace: false

# --- Dependencias ---
requiere:
  - concepto_axis_parametro
  - concepto_shape

draft: false
---

# np.corrcoef — Matriz de correlación de Pearson

`np.corrcoef` devuelve la **matriz de correlación de Pearson**: la matriz de covarianza de
[[np.cov]] **normalizada** para que cada entrada caiga en `[-1, 1]`. El elemento `[i, j]` mide la
fuerza y el signo de la **relación lineal** entre las variables `i` y `j`, con la **diagonal siempre
igual a 1** (toda variable correlaciona perfectamente consigo misma). Al ser adimensional es mucho
más interpretable que la covarianza: el `0.92` de dos features es comparable sin importar sus
escalas. Como [[np.cov]], la pregunta clave es **"¿filas o columnas son las variables?"** (`rowvar`).

## La idea en una fórmula

La correlación es la covarianza dividida por el producto de las desviaciones típicas de cada
variable: estandariza la covarianza para quitarle las unidades.

$$
\rho_{ij}=\frac{C_{ij}}{\sigma_i\,\sigma_j}\in[-1,\ 1]
\qquad\text{donde}\quad \sigma_i=\sqrt{C_{ii}}
$$

Como $\rho_{ii}=C_{ii}/(\sigma_i\sigma_i)=\sigma_i^2/\sigma_i^2=1$, la **diagonal es siempre 1**.
El divisor ($n-1$ vs $n$ de [[np.cov]]) se **cancela** en el cociente, así que la correlación no
depende de él.

**Mapa de shapes** — idéntico a [[np.cov]]: de $m$ variables × $n$ observaciones a una matriz
variable × variable:

$$
(m,\ n)\ \xrightarrow{\ \text{corrcoef, rowvar=True}\ }\ (m,\ m)
$$

Para dos variables ($m=2$) la matriz es simétrica, con **unos en la diagonal** y el coeficiente
$\rho$ fuera de ella:

$$
R=\begin{bmatrix} 1 & \rho_{12} \\ \rho_{12} & 1 \end{bmatrix}
\qquad \rho_{12}\in[-1,\ 1]
$$

Interpretación de $\rho_{12}$:

| Valor | Relación lineal |
|-------|-----------------|
| `+1` | perfecta positiva (recta ascendente) |
| `0` | sin correlación **lineal** (no implica independencia) |
| `-1` | perfecta negativa (recta descendente) |

## Firma

```python
np.corrcoef(
    x,                 # array_like: variables (filas) × observaciones (columnas)
    y=None,            # array_like: variables extra a apilar con x
    rowvar=True,       # bool: True → filas = variables; False → columnas = variables
    *,
    dtype=None,        # dtype: tipo del resultado (p. ej. np.float32)
) -> ndarray
```

> Los antiguos `bias` y `ddof` siguen aceptándose pero **no tienen efecto** (el divisor se cancela
> al normalizar) y están deprecados. No los uses.

## Los parámetros en detalle

### `x` — las variables de entrada
`array_like`. La matriz de datos, misma convención que `m` en [[np.cov]]: por defecto
(`rowvar=True`) **cada fila es una variable** y cada columna una observación. Un 1D es una sola
variable y devuelve `1.0`.

### `y` — variables adicionales
`array_like` opcional. Se **apila** con `x` para incluir más variables. `np.corrcoef(a, b)` da una
`(2, 2)` cuyo `[0, 1]` es el coeficiente entre las dos series.

### `rowvar` — quién es una variable (clave)
`bool`. Igual que en [[np.cov]]: `True` (defecto) → filas = variables; `False` → columnas =
variables. Los datos `(n_muestras, n_features)` necesitan `rowvar=False`:

```python
datos = np.random.rand(100, 4)        # 100 muestras, 4 features
np.corrcoef(datos).shape              # (100, 100)  ← mal: cada muestra como variable
np.corrcoef(datos, rowvar=False).shape  # (4, 4)     ← correlación entre features
```

### `dtype` — tipo del resultado
`dtype` (keyword-only). Fija el tipo de la matriz de salida, p. ej. `np.float32` para ahorrar
memoria en matrices grandes. Por defecto `float64`.

## El caso N-D

Como [[np.cov]], solo admite entradas **1D o 2D**; no tiene `axis`. La orientación se controla con
`rowvar`, que decide qué eje son las observaciones que se contraen (ver
[[concepto_axis_parametro]]):

| Entrada | `rowvar` | Variables | Salida |
|---------|----------|-----------|--------|
| `(n,)` 1D | — | 1 | `1.0` (0-d) |
| `(m, n)` | `True` | `m` (filas) | `(m, m)` |
| `(m, n)` | `False` | `n` (columnas) | `(n, n)` |

Entradas 3D+ lanzan error.

## Valor de retorno

Siempre **`ndarray` flotante**, cuadrado, simétrico, con diagonal 1:

| Entrada | `rowvar` | salida (shape) | tipo |
|---------|----------|----------------|------|
| `(n,)` 1D | cualquiera | `()` 0-d → `1.0` | `np.float64` |
| `(m, n)` | `True` | `(m, m)` | `ndarray` float |
| `(m, n)` | `False` | `(n, n)` | `ndarray` float |
| `x` + `y` (dos series) | `True` | `(2, 2)` | `ndarray` float |

- **Diagonal = 1** siempre; entradas en `[-1, 1]`; matriz **simétrica**.
- Por redondeo de coma flotante puede aparecer `1.0000000002`; clipar con `np.clip(R, -1, 1)` si hace
  falta exactitud.
- Una **variable constante** tiene $\sigma=0$ → división por cero → `nan` en su fila/columna.

## Casos de uso

### Correlación entre dos series
```python
x = np.array([1., 2., 3., 4.])
y = np.array([2., 4., 6., 8.])     # y = 2x → relación lineal perfecta
np.corrcoef(x, y)
# [[1., 1.],
#  [1., 1.]]
r = np.corrcoef(x, y)[0, 1]        # 1.0
```

### Matriz de correlación entre features (rowvar=False)
```python
datos = np.random.rand(100, 4)     # 100 muestras, 4 features
R = np.corrcoef(datos, rowvar=False)   # matriz 4×4, diagonal de unos
```

### Correlación negativa
```python
a = np.array([1., 2., 3., 4.])
b = np.array([4., 3., 2., 1.])     # decrece cuando a crece
np.corrcoef(a, b)[0, 1]            # -1.0
```

### De covarianza a correlación (la normalización a mano)
```python
C = np.cov(datos, rowvar=False)
d = np.sqrt(np.diag(C))            # desviaciones típicas σ_i
R = C / np.outer(d, d)            # equivale a np.corrcoef(datos, rowvar=False)
```

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| Matriz mal dimensionada (`(100, 100)`) | `rowvar` incorrecto | `rowvar=False` con datos `(muestras, features)` |
| Correlación `0` pese a una relación clara | la relación **no es lineal** (p. ej. parabólica) | Pearson solo capta lo lineal; inspeccionar con un gráfico |
| `nan` en la matriz | variable **constante** → varianza 0 → división por 0 | eliminar/revisar esa variable |
| Valor fuera de `[-1, 1]` por épsilon | redondeo de coma flotante | `np.clip(R, -1, 1)` |

## Notas relacionadas

- [[np.cov]] — la covarianza sin normalizar de la que se deriva esta matriz
- [[np.std]] — las desviaciones típicas $\sigma_i$ del denominador
- [[concepto_axis_parametro]] — `rowvar` decide qué eje son las observaciones
- [[concepto_shape]] · [[np.mean]]
