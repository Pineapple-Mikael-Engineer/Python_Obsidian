---
title: np.linalg.norm — norma (tamaño) de un vector o una matriz
aliases:
  - norm
  - linalg.norm
  - np.linalg.norm
tags:
  - numpy
  - api/funcion
  - algebra/matricial
lib: numpy
mod: np.linalg
tipo: funcion
retorna: escalar | ndarray
inplace: false
requiere:
  - concepto_axis_parametro
  - concepto_shape
draft: false
---

# np.linalg.norm — norma (tamaño) de un vector o una matriz

`np.linalg.norm` mide el **tamaño** de un tensor: colapsa los valores de `x` en una sola magnitud
escalar. Es la función más rica del grupo porque **una misma llamada calcula normas de vector o de
matriz** según `ord` y `axis`: con un eje 1D da la longitud de un vector; con dos ejes 2D da una
norma matricial (Frobenius, espectral, nuclear...). La pregunta al usarla no es "¿qué norma?" sino
**"¿qué ejes se reducen y con qué fórmula?"**. Para normalizar muchos vectores apilados sin bucle,
combina `axis` con `keepdims`; ver [[concepto_axis_parametro]].

## La idea en una fórmula

Una norma reduce el/los eje(s) indicados por `axis` y devuelve la magnitud. **El mapa de shapes**
(la relación entrada → salida) depende de cuántos ejes consume `ord`/`axis`:

$$
(\underbrace{n_0,\dots,n_{k-1}}_{\text{lote}},\, n)\ \xrightarrow{\ \text{axis}=k\ \text{(norma de vector)}}\ (\underbrace{n_0,\dots,n_{k-1}}_{\text{lote}})
\qquad
(\underbrace{n_0,\dots,n_{k-1}}_{\text{lote}},\, m,\, n)\ \xrightarrow{\ \text{axis}=(i,j)\ \text{(norma de matriz)}}\ (\underbrace{n_0,\dots,n_{k-1}}_{\text{lote}})
$$

Sin `axis`, `x` 1D se trata como un vector entero y `x` 2D como una matriz entera; en ambos casos
se reducen **todos** los ejes a un escalar de shape `()`. Con `keepdims=True` el/los eje(s)
reducidos quedan en tamaño $1$.

**Las fórmulas de vector** (un eje de tamaño $n$), según `ord`:

$$
\lVert x\rVert_2 = \sqrt{\textstyle\sum_i x_i^2}
\quad
\lVert x\rVert_1 = \textstyle\sum_i |x_i|
\quad
\lVert x\rVert_\infty = \max_i |x_i|
\quad
\lVert x\rVert_{-\infty} = \min_i |x_i|
$$

$$
\lVert x\rVert_p = \Big(\textstyle\sum_i |x_i|^p\Big)^{1/p}
\qquad
\lVert x\rVert_0 = \#\{\,i : x_i \neq 0\,\}\ \text{(no es una norma; cuenta no nulos)}
$$

**Las fórmulas de matriz** (dos ejes $m\times n$), con $\sigma_i$ los valores singulares de la
[[np.linalg.svd|SVD]]:

$$
\lVert A\rVert_F = \sqrt{\textstyle\sum_{ij} A_{ij}^2} = \sqrt{\textstyle\sum_i \sigma_i^2}
\quad
\lVert A\rVert_* = \textstyle\sum_i \sigma_i
\quad
\lVert A\rVert_2 = \sigma_{\max}
$$

$$
\lVert A\rVert_1 = \max_j \textstyle\sum_i |A_{ij}|\ \text{(máx. suma de columna)}
\qquad
\lVert A\rVert_\infty = \max_i \textstyle\sum_j |A_{ij}|\ \text{(máx. suma de fila)}
$$

## Firma

```python
np.linalg.norm(
    x,                 # array_like: vector, matriz o pila de ellos
    ord=None,          # None | int | float | inf | 'fro' | 'nuc': tipo de norma
    axis=None,         # None | int | tuple[int, int]: eje(s) sobre los que normar
    keepdims=False,    # bool: conservar los ejes reducidos con tamaño 1
) -> escalar | ndarray
```

## Los parámetros en detalle

### `x` — el tensor de entrada
`array_like`. Su forma y `axis` deciden si la norma es **de vector** (un eje) o **de matriz** (dos
ejes). Sin `axis`: 1D → norma de vector, 2D → norma de matriz; con más de 2 ejes y sin `axis` es
error (hay que indicar qué ejes forman la matriz/vector).

### `ord` — el tipo de norma
El parámetro clave, y **el mismo valor significa cosas distintas** según se norme un vector o una
matriz. `None` (defecto) da la euclídea ($L_2$) para vectores y la de Frobenius para matrices.

| `ord` | Vector (1 eje) | Matriz (2 ejes) |
|-------|----------------|-----------------|
| `None` | euclídea $\lVert x\rVert_2$ | Frobenius $\lVert A\rVert_F$ |
| `2` | euclídea $\lVert x\rVert_2$ | espectral $\sigma_{\max}$ (vía SVD, costosa) |
| `1` | $\sum_i |x_i|$ | máx. suma de columna |
| `np.inf` | $\max_i |x_i|$ | máx. suma de fila |
| `-np.inf` | $\min_i |x_i|$ | mín. suma de fila |
| `-1` / `-2` | $p$-norma con $p<0$ | mín. suma de columna / $\sigma_{\min}$ |
| `0` | nº de elementos no nulos | — |
| otro `p` (float) | $(\sum_i |x_i|^p)^{1/p}$ | — |
| `'fro'` | — | Frobenius $\lVert A\rVert_F$ |
| `'nuc'` | — | nuclear $\sum_i \sigma_i$ |

```python
v = np.array([3, 4])
np.linalg.norm(v)            # 5.0      → euclídea √(9+16)
np.linalg.norm(v, ord=1)     # 7.0      → suma de |componentes|
np.linalg.norm(v, ord=np.inf)# 4.0      → mayor |componente|

M = np.array([[1, 2], [3, 4]])
np.linalg.norm(M)            # 5.477...  → Frobenius
np.linalg.norm(M, ord='nuc') # 5.830...  → suma de valores singulares
np.linalg.norm(M, ord=2)     # 5.464...  → espectral (σ_max)
```

### `axis` — qué eje(s) se reducen
Decide **sobre qué ejes** se calcula la norma (y por tanto si es de vector o de matriz):

- `None` (defecto): norma de todo `x` (vector si es 1D, matriz si es 2D).
- `int`: norma de **vector** a lo largo de ese eje. Útil para "la norma de cada fila/columna".
- `tuple[int, int]`: norma de **matriz** sobre ese par de ejes; el resto son ejes de lote. Solo
  válido con `ord` de matriz (`'fro'`, `'nuc'`, `1`, `2`, `inf`...).

El eje (o el par) indicado **se colapsa**; los demás sobreviven (ver [[concepto_axis_parametro]]).

```python
P = np.array([[3, 4], [6, 8]])
np.linalg.norm(P, axis=1)    # [5., 10.]  → una norma por fila (vector)
np.linalg.norm(P, axis=0)    # [6.7, 8.9] → una norma por columna
```

### `keepdims` — conservar el eje reducido
Si `True`, el/los eje(s) reducidos quedan con tamaño 1 en su posición original, lo que mantiene el
resultado **broadcasteable** contra `x` (ver [[concepto_broadcasting]]). Es lo que permite
normalizar filas dividiendo el array por su norma:

```python
P = np.array([[3., 4.], [6., 8.]])
P / np.linalg.norm(P, axis=1, keepdims=True)   # cada fila a magnitud 1
# [[0.6, 0.8], [0.6, 0.8]]
```

## El caso N-D / axis

La regla es la de toda reducción: **el/los eje(s) de `axis` desaparecen del shape**; los demás
quedan como **lote**. Un `int` reduce un eje (norma de vector); una tupla de dos reduce ese par
(norma de matriz), tratando todo lo anterior como pila.

| `x.shape` | `axis` | `ord` | salida | lectura |
|-----------|--------|-------|--------|---------|
| `(n,)` | `None` | `None` | `()` | norma del vector entero |
| `(m, n)` | `None` | `None` | `()` | Frobenius de la matriz entera |
| `(m, n)` | `1` | vector | `(m,)` | una norma por **fila** |
| `(m, n)` | `0` | vector | `(n,)` | una norma por **columna** |
| `(b, m, n)` | `(1, 2)` | `'fro'` | `(b,)` | una norma de matriz por elemento del lote |
| `(b, m, n)` | `2` | vector | `(b, n)` | norma de vector a lo largo del eje medio |
| `(b, m, n)` | `1` | vector | `(b,) keepdims→(b,1,1)` | reduce un eje, conserva si `keepdims` |

```python
# Lote de 100 vectores de dimensión 3: la norma de cada uno (axis=1)
V = np.random.rand(100, 3)
np.linalg.norm(V, axis=1).shape       # (100,)  → 100 longitudes, sin bucle

# Lote de 8 matrices 3x3: la Frobenius de cada matriz (axis=(1,2))
B = np.random.rand(8, 3, 3)
np.linalg.norm(B, axis=(1, 2)).shape  # (8,)    → una norma por matriz del lote
```

## Vectorización

`np.linalg.norm` con `axis` reemplaza un bucle Python que normaría vector a vector. La versión
vectorizada recorre el eje en C (y delega en BLAS las normas matriciales que usan SVD), sin saltar
al intérprete por cada fila:

```python
# Bucle Python: una norma por fila, explícito y lento
def normas_por_fila(M):
    out = np.empty(M.shape[0])
    for i in range(M.shape[0]):
        out[i] = np.linalg.norm(M[i])
    return out

# Vectorizado: NumPy recorre el eje 1 en C
np.linalg.norm(M, axis=1)
```

Mismo resultado; describes *qué* eje normar, no *cómo* iterar. Es el mismo principio de
[[concepto_vectorizacion]]: una operación, un eje, una dirección.

## Valor de retorno

| Entrada | `axis` | `keepdims` | salida (shape) | tipo |
|---------|--------|------------|----------------|------|
| `(n,)` | `None` | `False` | `()` | **escalar de NumPy** (`np.float64`) |
| `(m, n)` | `None` | `False` | `()` | escalar (norma matricial) |
| `(m, n)` | `int`/`tuple` | `False` | shape sin esos ejes | `ndarray` |
| cualquiera | cualquiera | `True` | esos ejes en tamaño 1 | `ndarray` |

- El resultado es siempre **flotante** (`float64`), aunque `x` sea entero: una norma implica raíces
  y sumas de cuadrados.
- Con `axis=None` el retorno es un **escalar** de NumPy (0-d), no un `ndarray`; con `axis` indicado
  es un `ndarray` (posiblemente 0-d si `x` queda sin ejes supervivientes).

```python
type(np.linalg.norm([3, 4]))               # numpy.float64  → escalar
type(np.linalg.norm([[3, 4]], axis=1))     # numpy.ndarray
```

## Casos de uso

### Distancia euclídea entre dos puntos
```python
a = np.array([1, 2]); b = np.array([4, 6])
np.linalg.norm(a - b)        # 5.0   → ‖a-b‖₂
```

### Normalizar un vector a magnitud 1
```python
v = np.array([3., 4.])
v / np.linalg.norm(v)        # [0.6, 0.8]  → vector unitario
```

### Error residual de un ajuste
```python
residuo = A @ x - b
np.linalg.norm(residuo)      # ‖Ax - b‖₂  → cuánto falla la solución
```

### N-D: norma de cada fila de una pila de vectores
```python
X = np.array([[3., 4., 0.],
              [0., 0., 5.],
              [1., 2., 2.]])
np.linalg.norm(X, axis=1)            # [5., 5., 3.]   → una norma por fila
np.linalg.norm(X, axis=1, keepdims=True).shape   # (3, 1)  → listo para dividir
X / np.linalg.norm(X, axis=1, keepdims=True)     # cada fila a norma 1
```

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| Norma matricial inesperada | `ord=2` en matriz da la espectral (SVD), no la euclídea elemento a elemento | usar `'fro'` para Frobenius |
| `ValueError: Invalid norm order` | `ord` incompatible con la dim (`'fro'` en vector, `0` en matriz) | elegir un `ord` acorde a si es vector o matriz |
| `'fro'`/`'nuc'` falla con `axis=int` | esas normas son **matriciales**: necesitan un par de ejes | pasar `axis=(i, j)` o dejar `x` 2D |
| Resultado escalar cuando se esperaba por fila | falta `axis` | pasar `axis=0`/`axis=1` |
| Broadcasting falla al normalizar | se perdió el eje reducido | `keepdims=True` |

## Notas relacionadas

- [[concepto_axis_parametro]] — qué eje se reduce al normar
- [[concepto_vectorizacion]] — `axis` en vez del bucle por vector
- [[np.linalg.cond]] · [[np.linalg.matrix_rank]] · [[np.linalg.svd]] · [[np.linalg.inv]]
- [[normas_condiciones/index|normas y condiciones]] — la nota madre del grupo
