---
title: np.cov — Matriz de covarianza entre variables
aliases:
  - cov
  - np.cov
  - covarianza
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

# np.cov — Matriz de covarianza entre variables

`np.cov` toma un conjunto de **variables** medidas sobre las mismas **observaciones** y devuelve la
**matriz de covarianza**: una matriz cuadrada y simétrica donde el elemento `[i, j]` es la
covarianza entre la variable `i` y la `j`, y la **diagonal son las varianzas**. No es una reducción
elemento a elemento como [[np.mean]]: de `m` variables produce siempre una matriz `(m, m)`, sin
importar cuántas observaciones haya. La pregunta clave al usarla es **"¿quién es una variable, las
filas o las columnas?"** — eso lo decide `rowvar`.

## La idea en una fórmula

La covarianza entre dos variables mide cuánto **varían juntas** respecto a sus medias. Para una
matriz $X$ de shape $(m, n)$ —$m$ variables, $n$ observaciones— se centra cada variable restando su
media $\bar{x}_i$ y se promedia el producto cruzado sobre las $n$ observaciones (con divisor
$n-1$ por defecto):

$$
C_{ij}=\frac{1}{n-1}\sum_{k=0}^{n-1}(x_{ik}-\bar{x}_i)\,(x_{jk}-\bar{x}_j)
$$

El índice $k$ (las observaciones) **aparece en el sumatorio y desaparece**; lo que sobrevive es el
par de variables $(i, j)$. De ahí que la salida sea $(m, m)$.

**Mapa de shapes** — de $m$ variables × $n$ observaciones a una matriz variable × variable:

$$
(m,\ n)\ \xrightarrow{\ \text{cov, rowvar=True}\ }\ (m,\ m)
$$

Para dos variables ($m=2$) la matriz resultado es simétrica, con las **varianzas en la diagonal** y
la **covarianza cruzada** fuera de ella:

$$
C=\begin{bmatrix} \sigma_1^2 & \sigma_{12} \\ \sigma_{12} & \sigma_2^2 \end{bmatrix}
$$

donde $\sigma_i^2=C_{ii}$ es la varianza de la variable $i$ y $\sigma_{12}=C_{01}=C_{10}$ la
covarianza entre ambas. Si $\sigma_{12}>0$ crecen juntas; si $<0$ una sube cuando la otra baja.

## Firma

```python
np.cov(
    m,                 # array_like: variables (filas) × observaciones (columnas)
    y=None,            # array_like: variables extra a apilar con m
    rowvar=True,       # bool: True → filas = variables; False → columnas = variables
    bias=False,        # bool: True → divisor N (sesgada); False → N-1 (insesgada)
    ddof=None,         # int | None: sobreescribe el divisor (N - ddof)
    fweights=None,     # array_like[int]: pesos de frecuencia por observación
    aweights=None,     # array_like[float]: pesos de fiabilidad por observación
) -> ndarray
```

## Los parámetros en detalle

### `m` — las variables de entrada
`array_like`. La matriz de datos. Por defecto (`rowvar=True`) **cada fila es una variable** y cada
columna una observación. Un 1D se trata como **una sola variable** y devuelve un escalar 0-d (su
varianza).

### `y` — variables adicionales
`array_like` opcional. Se **apila** con `m` para incluir más variables en la misma matriz; debe
compartir el número de observaciones. `np.cov(x, y)` calcula la covarianza de dos series y devuelve
una `(2, 2)` cuyo `[0, 1]` es la covarianza cruzada.

### `rowvar` — quién es una variable (¡el parámetro clave!)
`bool`. Decide la orientación de los datos, y es la fuente número uno de errores:

| `rowvar` | Interpretación | Salida para shape `(a, b)` |
|----------|----------------|----------------------------|
| `True` (defecto) | cada **fila** es una variable; columnas = observaciones | `(a, a)` |
| `False` | cada **columna** es una variable; filas = observaciones | `(b, b)` |

Los datos en formato **`(n_muestras, n_features)`** (lo habitual en ML / pandas) tienen las
variables en columnas → necesitan `rowvar=False`:

```python
datos = np.random.rand(100, 3)   # 100 muestras, 3 features
np.cov(datos).shape              # (100, 100)  ← ¡trató cada muestra como variable!
np.cov(datos, rowvar=False).shape  # (3, 3)     ← correcto: covarianza entre features
```

### `bias` — divisor N vs N−1
`bool`. `False` (defecto) usa el divisor **insesgado** $n-1$ (corrección de Bessel). `True` usa $n$
(estimador de máxima verosimilitud, sesgado). Lo ignora `ddof` si este se especifica.

### `ddof` — control fino del divisor
`int | None`. Sobreescribe a `bias`: el divisor pasa a ser $n-\text{ddof}$. `ddof=1` ≡ `bias=False`
(insesgada); `ddof=0` ≡ `bias=True`. Úsalo cuando quieras un divisor distinto de los dos defectos.

### `fweights` — pesos de frecuencia
`array_like[int]`, uno por observación. Indica **cuántas veces se repite** cada observación; equivale
a duplicar columnas. Útil con datos agregados (tablas de frecuencias).

### `aweights` — pesos de fiabilidad (importancia)
`array_like[float]`, uno por observación. Pondera observaciones por su **fiabilidad/relevancia** (más
peso = más influencia en la media y la covarianza). Se combina con `fweights` si ambos están.

## El caso N-D

`np.cov` **no** es una reducción N-D al estilo de [[concepto_axis_parametro]]: solo acepta entradas
1D o 2D. No tiene parámetro `axis`; la orientación se controla **únicamente con `rowvar`**, que hace
el papel de "qué eje son las observaciones que se contraen":

| Entrada | `rowvar` | Variables | Observaciones | Salida |
|---------|----------|-----------|---------------|--------|
| `(n,)` 1D | — | 1 | `n` | `()` 0-d (la varianza) |
| `(m, n)` | `True` | `m` (filas) | `n` (columnas) | `(m, m)` |
| `(m, n)` | `False` | `n` (columnas) | `m` (filas) | `(n, n)` |

Pasar un tensor 3D+ lanza error. Para covarianza por lotes hay que iterar o reestructurar a 2D.

```python
X = np.array([[0, 1, 2, 3],     # variable 0
              [3, 2, 1, 0],     # variable 1 (anticorrelada con la 0)
              [1, 1, 1, 1]])    # variable 2 (constante)
np.cov(X).shape   # (3, 3)  → 3 variables, se contraen las 4 observaciones
```

## Valor de retorno

Siempre **`ndarray` flotante** (la división lo fuerza), cuadrado y simétrico:

| Entrada | `rowvar` | salida (shape) | tipo |
|---------|----------|----------------|------|
| `(n,)` 1D | cualquiera | `()` 0-d | `np.float64` |
| `(m, n)` | `True` | `(m, m)` | `ndarray` float |
| `(m, n)` | `False` | `(n, n)` | `ndarray` float |
| `m` + `y` (dos series) | `True` | `(2, 2)` | `ndarray` float |

- La **diagonal** `C[i, i]` coincide con [[np.var]] de la variable `i` (con el mismo `ddof`).
- La matriz es **simétrica**: `C[i, j] == C[j, i]`.
- Una variable constante da varianza `0` en su diagonal (fila/columna de ceros salvo si covaría, que
  no puede).

## Casos de uso

### Covarianza entre dos series
```python
x = np.array([1., 2., 3., 4.])
y = np.array([2., 4., 6., 8.])     # y = 2x
C = np.cov(x, y)
# [[1.667, 3.333],
#  [3.333, 6.667]]
C[0, 1]   # 3.333  → covarianza cruzada (positiva: crecen juntas)
```

### Datos en formato (muestras, features) → rowvar=False
```python
datos = np.random.rand(100, 3)   # 100 muestras, 3 features
np.cov(datos, rowvar=False)      # matriz 3×3 de covarianza entre features
```

### La diagonal son las varianzas
```python
X = np.array([[1., 2., 3., 4.],
              [10., 20., 30., 40.]])
C = np.cov(X)
np.diag(C)               # [1.667, 166.7]
np.var(X, axis=1, ddof=1)  # [1.667, 166.7]  → coincide con la diagonal
```

### Estimador sesgado (divisor N)
```python
np.cov(X, bias=True)     # divide entre N en vez de N-1
np.cov(X, ddof=0)        # idéntico
```

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| Matriz del tamaño equivocado (p. ej. `(100, 100)`) | `rowvar` mal puesto | `rowvar=False` para datos `(muestras, features)` |
| Valores enormes/incomparables entre variables | sensible a la **escala** de cada variable | normalizar, o usar [[np.corrcoef]] (escala fija) |
| Diagonal no coincide con la varianza esperada | distinto `ddof`/`bias` | igualar el divisor (`ddof=1` ≡ `np.var(..., ddof=1)`) |
| Entrada 3D falla | `np.cov` solo admite 1D/2D | reestructurar a 2D o iterar el lote |

## Notas relacionadas

- [[np.corrcoef]] — la covarianza **normalizada** a `[-1, 1]` (correlación de Pearson)
- [[np.var]] — coincide con la diagonal de la matriz de covarianza
- [[concepto_axis_parametro]] — `rowvar` hace el papel de "qué eje son las observaciones"
- [[concepto_shape]] · [[np.mean]] · [[np.std]]
