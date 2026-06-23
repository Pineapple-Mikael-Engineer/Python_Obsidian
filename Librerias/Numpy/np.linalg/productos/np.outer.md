---
title: np.outer — producto externo, todas las parejas de dos vectores
aliases:
  - outer
  - np.outer
  - producto externo
tags:
  - numpy
  - api/funcion
  - algebra/matricial
lib: numpy
mod: np
tipo: funcion
retorna: ndarray
inplace: false
requiere:
  - concepto_shape
draft: false
---

# np.outer — producto externo, todas las parejas de dos vectores

`np.outer(a, b)` **aplana** ambas entradas a 1D y multiplica **todas las parejas**: el resultado es
la rejilla $C_{ij} = a_i\,b_j$, una matriz donde cada elemento es el producto de un valor de `a` por
un valor de `b`. A diferencia de [[np.inner]] (que **contrae** un eje sumando), `np.outer` **no suma
nada**: crea una dimensión nueva por cada operando. Es la operación detrás de las mallas, las
matrices de rango 1 y las tablas de multiplicar.

## La idea en una fórmula

`np.outer` toma un vector de longitud $m$ y otro de longitud $n$ y produce la matriz $m\times n$ de
todos sus productos cruzados. Lo primero que hace es **aplanar** (`ravel`) cada entrada a 1D.

**El mapa de shapes** — tras aplanar a $(m,)$ y $(n,)$:

$$
(m,),\ (n,)\ \longrightarrow\ (m,\, n)
$$

No desaparece ningún eje (no hay contracción); al contrario, **aparecen los dos**: el de `a` como
filas y el de `b` como columnas. La **fórmula por índices** es un producto sin sumatorio:

$$
C_{ij} \;=\; a_i\, b_j \qquad i = 0,\dots,m-1 \quad j = 0,\dots,n-1
$$

Cada **fila** $i$ es el vector `b` escalado por $a_i$; cada **columna** $j$ es `a` escalado por $b_j$.
Por eso $C$ siempre tiene **rango 1**. Visualmente, es una rejilla fila × columna:

$$
C = \begin{bmatrix}
a_0 b_0 & a_0 b_1 & a_0 b_2 \\
a_1 b_0 & a_1 b_1 & a_1 b_2 \\
a_2 b_0 & a_2 b_1 & a_2 b_2
\end{bmatrix}
\qquad C_{ij} = a_i\, b_j
$$

`b` se reparte por columnas y `a` por filas; shape `(3, 3)` = `(len a)` × `(len b)`.

## Firma

```python
np.outer(a, b, out=None) -> ndarray
```

## Los parámetros en detalle

### `a`, `b` — los dos operandos
`array_like`. **Se aplanan a 1D** antes de operar: si pasas un array N-D, NumPy lo lee como
`a.ravel()` (orden C). No hay restricción de forma entre ellos —cualquier `(m,)` × `(n,)` vale—,
porque no se contrae nada.

```python
A = np.array([[1, 2], [3, 4]])   # se aplana a [1, 2, 3, 4]  (longitud 4)
b = np.array([10, 20])           # longitud 2
np.outer(A, b).shape             # (4, 2)  → ¡A se aplanó!, no se respetó su forma 2x2
```

> [!warning] Las entradas N-D se aplanan, no se difunden
> `np.outer` **nunca** hace broadcasting ni respeta los ejes de un array N-D: lo primero que hace es
> `ravel()`. Si necesitas el producto externo conservando estructura N-D, usa broadcasting explícito
> (`a[..., :, None] * b[..., None, :]`) o [[np.einsum]]. `np.outer` es estrictamente vector × vector.

### `out` — buffer de salida
`ndarray` preasignado con shape exacto `(a.size, b.size)` y `dtype` compatible. Evita asignar memoria
nueva; útil al repetir el producto externo en un bucle.

```python
buf = np.empty((3, 2))
np.outer([1, 2, 3], [10, 20], out=buf)   # escribe en buf en vez de crear un array
```

## El caso N-D

`np.outer` **no tiene** comportamiento N-D propio: cualquier entrada con más de un eje se **aplana**
primero, así que la salida es **siempre 2D** de shape `(a.size, b.size)`. Esto la distingue del resto
de productos: no hay ejes de lote ni contracción configurable.

| `a` original | `b` original | tras `ravel` | salida |
|--------------|--------------|--------------|--------|
| `(m,)` | `(n,)` | `(m,)`, `(n,)` | `(m, n)` |
| `(2, 3)` | `(4,)` | `(6,)`, `(4,)` | `(6, 4)` |
| escalar | `(n,)` | `(1,)`, `(n,)` | `(1, n)` |

Si lo que querías era un producto externo **por lotes** (conservando ejes), no es `np.outer`: usa
broadcasting (`a[:, None] * b[None, :]` por lote) o [[np.einsum]] con la firma adecuada.

## Vectorización

`np.outer` reemplaza el doble bucle que llena la rejilla de productos. Las dos versiones dan lo mismo,
pero la vectorizada recorre la matriz en C en vez de en el intérprete:

```python
# Doble bucle Python (explícito, lento):
def outer_lento(a, b):
    out = np.empty((len(a), len(b)))
    for i in range(len(a)):
        for j in range(len(b)):
            out[i, j] = a[i] * b[j]
    return out

# Vectorizado: producto externo en una operación
np.outer(a, b)
# Equivale a difundir las formas: a[:, None] * b[None, :]
```
El equivalente idiomático `a[:, None] * b[None, :]` lo deja claro: es puro
[[concepto_broadcasting]] —`a` como columna `(m, 1)` y `b` como fila `(1, n)` se alinean y multiplican
elemento a elemento, generando la rejilla `(m, n)`—. `np.outer` es el atajo nombrado de ese patrón.

## Valor de retorno

| `a.size` | `b.size` | salida (shape) | tipo |
|----------|----------|----------------|------|
| `m` | `n` | `(m, n)` | `ndarray` (**siempre 2D**) |

- Siempre devuelve un `ndarray` 2D, nunca un escalar (aun con `a` y `b` de un solo elemento: `(1, 1)`).
- El `dtype` sigue la **promoción** habitual: `int` × `float` → `float`, etc. La matriz resultante
  tiene **rango 1** (todas sus filas/columnas son proporcionales).

## Casos de uso

### Tabla de multiplicar
```python
np.outer(np.arange(1, 4), np.arange(1, 4))
# [[1, 2, 3],
#  [2, 4, 6],
#  [3, 6, 9]]
```

### Matriz de rango 1 a partir de un vector
```python
v = np.array([1., 2., 3.])
np.outer(v, v)        # v vᵀ: matriz simétrica de rango 1
# [[1, 2, 3],
#  [2, 4, 6],
#  [3, 6, 9]]
```

### Construir una malla (producto cartesiano de escalas)
```python
x = np.linspace(0, 1, 3)     # [0. , 0.5, 1. ]
ones = np.ones(4)
np.outer(x, ones)            # repite x como columnas → base de un meshgrid
# [[0. , 0. , 0. , 0. ],
#  [0.5, 0.5, 0.5, 0.5],
#  [1. , 1. , 1. , 1. ]]
```

### Entradas N-D: se aplanan (con valores)
```python
A = np.array([[1, 2],
              [3, 4]])       # se aplana a [1, 2, 3, 4]
b = np.array([1, 10])
np.outer(A, b)
# [[ 1, 10],     1·1=1   1·10=10
#  [ 2, 20],     2·1=2   2·10=20
#  [ 3, 30],     3·1=3   3·10=30
#  [ 4, 40]]     4·1=4   4·10=40   → shape (4, 2): A.size × b.size
```
La forma `(2, 2)` de `A` se pierde: el resultado es `(4, 2)` porque `A` se aplana a longitud 4. Esa
es la diferencia clave con cualquier producto que respete ejes.

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| La forma N-D de la entrada se "pierde" | `np.outer` **aplana** a 1D antes de operar | usar `a[..., :, None] * b[..., None, :]` o [[np.einsum]] para conservar ejes |
| Esperar un escalar (producto punto) | `outer` no suma; crea la matriz de todas las parejas | para el producto punto usar [[np.inner]] o `a @ b` |
| Resultado 2D inesperado con entradas grandes | `(m, n)` puede ser enorme (`m·n` elementos) | comprobar tamaños antes; el producto externo no reduce |
| Confundir `outer` con `multiply` | `*` exige formas broadcasteables (elemento a elemento); `outer` cruza todas las parejas | ver [[np.multiply]] |

## Notas relacionadas

- [[concepto_shape]] — el producto externo como mapa de shapes `(m,),(n,) → (m,n)`
- [[concepto_broadcasting]] — `np.outer` es el atajo de `a[:, None] * b[None, :]`
- [[np.inner]] — la operación inversa en espíritu: contrae un eje en vez de crearlos
- [[np.multiply]] · [[np.matmul]] · [[np.einsum]]
