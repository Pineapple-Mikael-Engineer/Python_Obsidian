---
title: np.einsum — sumación de Einstein, el string de subíndices ES el mapa de shapes
aliases:
  - einsum
  - np.einsum
  - sumación de Einstein
  - notación de Einstein
tags:
  - numpy
  - api/funcion
  - algebra/matricial
lib: numpy
mod: np
tipo: funcion
retorna: ndarray | escalar
inplace: false
requiere:
  - concepto_shape
draft: false
---

# np.einsum — sumación de Einstein

`np.einsum` es la herramienta de contracción **más expresiva** de NumPy: un solo string de
subíndices describe transposiciones, diagonales, trazas, productos punto, externos, matriciales y por
lotes, y cualquier contracción tensorial arbitraria. La idea clave: **el string ES el mapa de
shapes**. Donde [[np.matmul]] contrae la dimensión interior y [[np.tensordot]] contrae los ejes que
le indiques, `einsum` te deja escribir letra por letra qué eje es qué y qué se suma.

## La idea en una fórmula

El string tiene la forma `'subíndices_entrada -> subíndices_salida'`. Cada letra es un eje. La regla
de la sumación de Einstein, en tres puntos:

1. **Un índice repetido entre operandos se SUMA** (se contrae). En `'ij,jk->ik'`, la `j` aparece en
   ambos operandos pero no en la salida → se suma sobre ella.
2. **Los índices que aparecen tras `->` se conservan** como ejes de la salida, en ese orden.
3. **Los índices que se omiten en la salida se suman.** Si una letra del lado izquierdo no está a la
   derecha, ese eje se reduce.

Para el caso `'ij,jk->ik'` (producto matricial), la fórmula es literalmente lo que se lee:

$$
C_{ik} \;=\; \sum_{j} A_{ij}\, B_{jk}
$$

**El mapa de shapes** se lee directamente del string: cada letra es un tamaño de eje, las repetidas
se contraen, las de la salida sobreviven:

$$
(\,i,\,j\,),(\,j,\,k\,)\ \xrightarrow{\ \text{'ij,jk->ik'}\ }\ (\,i,\,k\,)
$$

> [!tip] Modo implícito (sin `->`)
> Si omites `-> salida`, einsum aplica la convención clásica: los índices **repetidos se suman** y
> los **no repetidos** salen ordenados alfabéticamente. `'ij,jk'` ≡ `'ij,jk->ik'`; `'ii'` ≡ `'ii->'`
> (traza). Lo recomendable es ser **explícito** con `->` para que el mapa de shapes quede a la vista.

## Firma

```python
np.einsum(subscripts, *operands, out=None, dtype=None, order='K',
          casting='safe', optimize=False) -> ndarray
#   subscripts : str   → el string de subíndices, p. ej. 'ij,jk->ik'
#   *operands  : array_like  → tantos arrays como grupos separados por comas
#   optimize   : bool | str | list  → orden de contracción (ver abajo)
```

## Los parámetros en detalle

### `subscripts` — el string (el corazón de la función)
La cadena que describe la operación. Cada operando lleva una etiqueta de una letra por eje,
separados por comas; opcionalmente `-> etiqueta_salida`. Letras válidas: `a–z`, `A–Z`. El número de
letras de cada grupo debe igualar el `ndim` del operando correspondiente, y una letra repetida debe
referirse a ejes del **mismo tamaño**.

### `*operands` — los arrays
Tantos como grupos separados por comas haya en el string. `'ij,jk->ik'` necesita exactamente dos.

### `out` — buffer de salida
`ndarray` preasignado con el shape exacto del resultado. Evita asignar memoria en bucles.

### `dtype`, `order`, `casting`
- `dtype`: fuerza el tipo del cómputo y la salida (acumular en `float64`, por ejemplo).
- `order`: layout de memoria del resultado (`'C'`, `'F'`, `'K'`).
- `casting`: qué conversiones de tipo se permiten (`'safe'` por defecto).

### `optimize` — orden óptimo de contracción
Para **más de dos operandos**, el orden en que se contraen cambia drásticamente el coste. Con
`optimize=True` (o `'greedy'`/`'optimal'`), einsum calcula un orden de contracción que minimiza las
operaciones intermedias, igual que [[np.linalg.multi_dot]] hace con cadenas de matrices. Para una
cadena larga puede ser órdenes de magnitud más rápido.

```python
# Cadena de 3 tensores: el orden de contracción importa
np.einsum('ij,jk,kl->il', A, B, C, optimize=True)
```

## El caso N-D

`einsum` es N-D por diseño: añades letras por eje. El operador `...` (elipsis) representa **cualquier
número de ejes de lote** que se transportan sin tocar, alineados por la derecha como en
[[concepto_broadcasting|broadcasting]].

| String | Operación | Mapa de shapes |
|--------|-----------|----------------|
| `'ij->ji'` | transponer | `(i, j) → (j, i)` |
| `'ii->i'` | diagonal | `(i, i) → (i,)` |
| `'ii->'` | traza | `(i, i) → ()` |
| `'ij->'` | suma de todos | `(i, j) → ()` |
| `'ij->i'` | suma por filas | `(i, j) → (i,)` |
| `'ij,jk->ik'` | producto matricial | `(i,j),(j,k) → (i,k)` |
| `'i,j->ij'` | producto externo | `(i),(j) → (i,j)` |
| `'i,i->'` | producto punto | `(i),(i) → ()` |
| `'ij,ij->'` | suma de productos (Frobenius) | `(i,j),(i,j) → ()` |
| `'bij,bjk->bik'` | matmul por lotes | `(b,i,j),(b,j,k) → (b,i,k)` |
| `'...ij->...ji'` | transponer los 2 últimos ejes | `(...,i,j) → (...,j,i)` |

La elipsis es lo que hace a einsum equivalente a `matmul` en N-D: `'...ij,...jk->...ik'` es
exactamente el producto matricial por lotes con broadcasting de los ejes previos.

## Vectorización

`einsum` compila el string a un único recorrido sobre los ejes y delega los productos en código C
(y en BLAS cuando el patrón es un producto matricial). Frente al bucle Python que explicita la suma
de Einstein:

```python
# Bucle Python: producto matricial por lotes 'bij,bjk->bik'
def batch_mm(A, B):
    b, i, j = A.shape
    _, _, k = B.shape
    out = np.zeros((b, i, k))
    for bb in range(b):
        for ii in range(i):
            for kk in range(k):
                for jj in range(j):
                    out[bb, ii, kk] += A[bb, ii, jj] * B[bb, jj, kk]
    return out

# Vectorizado: el string describe la contracción, NumPy itera en C
np.einsum('bij,bjk->bik', A, B)
```

Mismo resultado; cuatro bucles anidados se vuelven una línea. Es el principio de
[[concepto_vectorizacion]] llevado al extremo: el string *es* la especificación de qué se itera y qué
se suma, sin escribir un solo `for`.

## Valor de retorno

| String | salida (shape) | tipo |
|--------|----------------|------|
| `'ii->'`, `'i,i->'`, `'ij,ij->'` | `()` | **escalar** de NumPy |
| `'ij->ji'`, `'ij,jk->ik'` | tensor según las letras de salida | `ndarray` |
| `'...ij->...ji'` | lote + ejes finales | `ndarray` |

- El shape de salida es exactamente la tupla de tamaños de las letras tras `->` (en ese orden).
- El `dtype` sigue las reglas de **promoción** salvo que fijes `dtype=`.
- Si no quedan letras en la salida (`->` vacío), el resultado es un escalar 0-d.

## Casos de uso

### Transponer, diagonal y traza
```python
M = np.arange(9).reshape(3, 3)
np.einsum('ij->ji', M)   # transpuesta
np.einsum('ii->i', M)    # [0, 4, 8]  → diagonal
np.einsum('ii->', M)     # 12         → traza (0+4+8)
```

### Productos clásicos
```python
u = np.array([1, 2, 3])
v = np.array([4, 5, 6])
np.einsum('i,i->', u, v)    # 32        → producto punto
np.einsum('i,j->ij', u, v)  # (3, 3)    → producto externo
A = np.array([[1, 2], [3, 4]])
B = np.array([[5, 6], [7, 8]])
np.einsum('ij,jk->ik', A, B)   # [[19, 22], [43, 50]]  ≡ A @ B
```

El string `'ij,jk->ik'` ES el producto matricial $C_{ik}=\sum_j A_{ij}B_{jk}$, con la `j`
contraída. Con números:

$$
\begin{bmatrix} 1 & 2 \\ 3 & 4 \end{bmatrix}
\begin{bmatrix} 5 & 6 \\ 7 & 8 \end{bmatrix}
=
\begin{bmatrix} 1\cdot5+2\cdot7 & 1\cdot6+2\cdot8 \\ 3\cdot5+4\cdot7 & 3\cdot6+4\cdot8 \end{bmatrix}
=
\begin{bmatrix} 19 & 22 \\ 43 & 50 \end{bmatrix}
$$

### Reducciones dirigidas
```python
X = np.arange(6).reshape(2, 3)
np.einsum('ij->i', X)   # [3, 12]   → suma por filas  (≡ X.sum(axis=1))
np.einsum('ij->j', X)   # [3, 5, 7] → suma por columnas (≡ X.sum(axis=0))
np.einsum('ij->', X)    # 15        → suma total
```

### Producto matricial por lotes (sin bucle)
```python
A = np.random.rand(8, 2, 3)   # 8 matrices 2x3
B = np.random.rand(8, 3, 4)   # 8 matrices 3x4
np.einsum('bij,bjk->bik', A, B).shape   # (8, 2, 4)  ≡ A @ B
```

### Proyección de canales en un tensor 4D (estilo deep learning)
Un tensor de activaciones `(N, C, H, W)` (lote, canal, alto, ancho) proyectado sobre el eje del
ancho a un nuevo tamaño `V` mediante una matriz `(W, V)`: la `w` se contrae, `n, c, h` viajan como
lote y `v` es el eje nuevo.

```python
X = np.random.rand(4, 3, 8, 8)   # (N, C, H, W) = (4, 3, 8, 8)
Wp = np.random.rand(8, 5)        # (W, V) = (8, 5)
np.einsum('nchw,wv->nchv', X, Wp).shape   # (4, 3, 8, 5)  → W=8 contraído, V=5 nuevo
```

El mapa de shapes: $(\,n,c,h,\mathbf{w}\,),(\,\mathbf{w},v\,)
\xrightarrow{\ \text{'nchw,wv->nchv'}\ } (\,n,c,h,v\,)$, con la `w` (en negrita) contraída.

### Norma de Frobenius y suma de productos elemento a elemento
```python
G = np.random.rand(4, 4)
np.einsum('ij,ij->', G, G)        # sum(G**2)  → ‖G‖²_F
# Combinando ejes: peso por fila
W = np.random.rand(3, 5)
x = np.random.rand(5)
np.einsum('ij,j->i', W, x)        # (3,)  → W @ x
```

### Elipsis: transponer solo los dos últimos ejes de un tensor de lote
```python
T = np.random.rand(10, 2, 3)      # lote de 10 matrices 2x3
np.einsum('...ij->...ji', T).shape   # (10, 3, 2)  → transpone cada matriz
```

### Bilineal y contracciones múltiples con `optimize`
```python
# x^T A y  para cada par del lote, en una expresión:
x = np.random.rand(16, 4)
A = np.random.rand(4, 4)
y = np.random.rand(16, 4)
np.einsum('bi,ij,bj->b', x, A, y, optimize=True).shape   # (16,)
```

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| `operand has more dimensions than subscripts` | nº de letras ≠ `ndim` del operando | una letra por eje (o usar `...`) |
| `dimensions ... not equal` | una letra repetida refiere ejes de distinto tamaño | revisar que los ejes contraídos coincidan |
| Eje que querías conservar desaparece | lo omitiste en la salida (regla 3) | añadir la letra tras `->` |
| Cadena de >2 operandos muy lenta | orden de contracción subóptimo | `optimize=True` |
| Salida en orden inesperado | el orden lo dan las letras tras `->`, no los operandos | reordenar las letras de la salida |
| Resultado escalar inesperado | `->` vacío o modo implícito que sumó todo | declarar las letras de salida explícitamente |

## Notas relacionadas

- [[concepto_shape]] — el string de einsum es un mapa de shapes literal
- [[concepto_vectorizacion]] — la contracción arbitraria sin bucles anidados
- [[np.matmul]] — el caso `'...ij,...jk->...ik'` con BLAS
- [[np.tensordot]] — la misma contracción por ejes, sin notación de subíndices
- [[np.matmul]] · [[np.tensordot]] · [[np.linalg.multi_dot]]
