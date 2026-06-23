---
title: np.argmax — índice (no valor) del máximo a lo largo de un eje
aliases:
  - argmax
  - np.argmax
tags:
  - numpy
  - api/funcion
  - reducciones

# --- Clasificación ---
lib: numpy
mod: np
tipo: funcion

# --- Comportamiento ---
retorna: ndarray | int
inplace: false

# --- Dependencias ---
requiere:
  - concepto_axis_parametro
  - concepto_indexing

draft: false
---

# np.argmax — índice (no valor) del máximo a lo largo de un eje

`np.argmax` es una **reducción que devuelve posiciones, no valores**: recorre un eje y lo colapsa,
pero en lugar de quedarse con el máximo se queda con el **índice entero** donde está ese máximo.
Es la operación que responde "¿*dónde* está el mayor?" en vez de "¿*cuánto* vale el mayor?". El
shape de salida es idéntico al de [[np.sum]] sobre el mismo eje (el eje desaparece), pero el
**contenido** son índices en el rango `[0, n_axis)`, no sumas. La pregunta al usarla es doble: "¿qué
eje desaparece?" y, sobre todo, "¿este índice está referido a ese eje o al array **aplanado**?".

## La idea en una fórmula

`argmax` colapsa un eje devolviendo el **argumento** (el índice) que maximiza a lo largo de él. Para
una matriz $A$ de shape $(m, n)$, sobre el eje `0` produce un vector indexado por la columna $j$
cuyo valor es la **fila** ganadora:

$$
\text{argmax}_j \;=\; \arg\max_{i\in[0,m)} A_{ij} \qquad \text{(axis=0, desaparece el eje } i\text{)}
$$

y sobre el eje `1`, un vector indexado por la fila $i$ cuyo valor es la **columna** ganadora:

$$
\text{argmax}_i \;=\; \arg\max_{j\in[0,n)} A_{ij} \qquad \text{(axis=1, desaparece el eje } j\text{)}
$$

**El mapa de shapes** es el de cualquier reducción sobre el eje $p$ (ver [[concepto_axis_parametro]]),
con la salvedad de que el rango de los valores de salida es el **tamaño del eje reducido**:

$$
(n_0,\dots,n_k)\ \xrightarrow{\ \text{argmax, axis}=p\ }\ (n_0,\dots,n_{p-1},\,n_{p+1},\dots,n_k)
\quad\text{con valores en } [0,\,n_p)
$$

Y el caso por defecto `axis=None` **aplana primero** el tensor y devuelve un único índice escalar en
el rango $[0,\ \prod_i n_i)$ — un índice sobre el array de 1D, no una posición N-D:

$$
(n_0,\dots,n_k)\ \xrightarrow{\ \text{argmax, axis=None}\ }\ (\,)\ \text{escalar} \in [0,\ n_0\cdots n_k)
$$

## Firma

```python
np.argmax(
    a,                 # array_like: el tensor de entrada
    axis=None,         # None | int: eje a lo largo del cual buscar el máximo
    out=None,          # ndarray: destino preasignado (dtype entero)
    *,
    keepdims=False,    # bool: conservar el eje reducido con tamaño 1
) -> ndarray | intp
```

## Los parámetros en detalle

### `a` — el tensor de entrada
`array_like` (ndarray, lista, escalar). Se convierte a `ndarray` si no lo es. Sobre sus elementos se
compara para encontrar el máximo; el `dtype` de `a` no afecta al de la salida (que siempre es entero).

### `axis` — eje de búsqueda (y la trampa del aplanado)
El parámetro central, pero con **una sola dirección** a la vez (no acepta tupla, a diferencia de
`np.sum`). Valores válidos: `None` (defecto), un `int` o un eje negativo.

- `None`: **aplana** `a` y devuelve **un** índice escalar sobre esa versión 1D. Es la fuente del
  bug más común: en un array 2D+, ese número **no** es una fila ni una columna, es la posición en el
  recorrido fila-por-fila (orden C). Para recuperar la posición N-D real hay que traducirlo con
  `np.unravel_index` (ver más abajo).
- `int`: reduce ese eje; la salida tiene índices en `[0, a.shape[axis])`.

```python
M = np.array([[1, 9, 3],
              [7, 2, 8]])
np.argmax(M, axis=0)   # [1, 0, 1]  → fila ganadora por columna (índices en [0,2))
np.argmax(M, axis=1)   # [1, 2]     → columna ganadora por fila  (índices en [0,3))
np.argmax(M)           # 1          → índice APLANADO (el 9 está en la posición 1)
```

### `out` — escribir en un buffer existente
`ndarray` preasignado, con el **shape de salida** y un `dtype` **entero** (`np.intp`). Evita una
asignación de memoria; útil en bucles. Debe encajar exactamente con la forma del resultado.

### `keepdims` — conservar el eje reducido como tamaño 1
Argumento **solo por palabra clave** (`*`). Si `True`, el eje reducido no desaparece: queda con
tamaño 1, de modo que la salida sigue siendo **broadcasteable** contra `a`. Es lo que permite usar
los índices con `np.take_along_axis` para recuperar los valores sin perder la alineación.

```python
M = np.array([[1, 9, 3],
              [7, 2, 8]])
idx = np.argmax(M, axis=1, keepdims=True)   # shape (2, 1) → [[1],[2]]
np.take_along_axis(M, idx, axis=1)          # [[9],[8]]  → los valores máximos
```

## El eje y el caso N-D

La regla de forma es la misma que en cualquier reducción: **el eje de `axis` desaparece**; los demás
quedan en orden. Lo que cambia frente a `np.sum` es la **interpretación del contenido**: cada número
de la salida es "la posición ganadora **dentro del eje que se colapsó**".

| `a.shape` | `axis` | salida (shape) | lectura del contenido |
|-----------|--------|----------------|------------------------|
| `(n,)` | `0` o `None` | `()` escalar | índice del máximo (en `[0, n)`) |
| `(m, n)` | `0` | `(n,)` | por **columna**: qué fila gana (en `[0, m)`) |
| `(m, n)` | `1` | `(m,)` | por **fila**: qué columna gana (en `[0, n)`) |
| `(m, n)` | `None` | `()` | índice **aplanado** (en `[0, m·n)`) |
| `(b, m, n)` | `0` | `(m, n)` | por celda `(i,j)`: qué lámina del lote gana |
| `(b, m, n)` | `-1` | `(b, m)` | por fila de cada matriz: qué columna gana |

```python
T = np.array([[[ 1, 50,  3],
               [ 4,  5,  6]],
              [[40,  8,  9],
               [10, 11, 99]]])           # shape (2, 2, 3)

T.argmax(axis=0).shape   # (2, 3)
T.argmax(axis=0)
# [[1, 0, 1],     ← por cada (fila, col): qué lámina (0 ó 1) tiene el máximo
#  [1, 1, 1]]

T.argmax(axis=-1)        # qué columna gana en cada fila de cada lámina
# [[1, 2],        ← lámina 0: fila0 gana col1 (50), fila1 gana col2 (6)
#  [0, 2]]        ← lámina 1: fila0 gana col0 (40), fila1 gana col2 (99)
```

### `axis=None` y `np.unravel_index`

Con el defecto `axis=None`, el índice es plano y **no se puede indexar directamente** un array N-D
con él en sentido posicional. `np.unravel_index(idx, a.shape)` lo convierte en la tupla de
coordenadas N-D (ver [[concepto_indexing]]):

```python
M = np.array([[1, 9, 3],
              [7, 2, 8]])
plano = np.argmax(M)                       # 1   → índice en el array aplanado
fila, col = np.unravel_index(plano, M.shape)  # (0, 1)
M[fila, col]                               # 9   → el máximo, recuperado por posición
```

## Vectorización

`np.argmax` reemplaza un bucle de "llevar el mejor visto hasta ahora". Las dos versiones dan lo
mismo, pero la vectorizada recorre el eje en C, sin objetos Python por elemento:

```python
# Bucle Python (lento, explícito): argmax por fila de una matriz
def argmax_filas(M):
    m, n = M.shape
    out = np.empty(m, dtype=np.intp)
    for i in range(m):
        mejor, pos = M[i, 0], 0
        for j in range(1, n):
            if M[i, j] > mejor:     # ">" estricto → conserva el PRIMER máximo
                mejor, pos = M[i, j], j
        out[i] = pos
    return out

# Vectorizado (NumPy recorre el eje 1 en C):
M.argmax(axis=1)
```

El `>` estricto del bucle explica la semántica de empates: el primer índice gana. Es el mismo
principio de [[concepto_vectorizacion]]: describes *qué* eje recorrer, no *cómo* iterar.

## Valor de retorno

`argmax` **nunca devuelve el valor máximo**, siempre un **índice entero** (`np.intp`, el entero de
tamaño puntero de la plataforma). El shape depende de `axis` y `keepdims`:

| Entrada | `axis` | `keepdims` | salida (shape) | tipo |
|---------|--------|------------|----------------|------|
| `(m, n)` | `None` | `False` | `()` | **escalar** `np.intp` (índice aplanado) |
| `(m, n)` | `int` | `False` | shape sin ese eje | `ndarray` de `intp` |
| `(m, n)` | `int` | `True` | ese eje en tamaño 1 | `ndarray` de `intp` |
| `(n,)` | `0` | `False` | `()` | escalar `np.intp` |

El contenido es siempre un índice en `[0, a.shape[axis])` (o en `[0, a.size)` si `axis=None`).

## Casos de uso

### Clase predicha (clasificación)
```python
logits = np.array([0.1, 0.7, 0.2])
np.argmax(logits)        # 1  → la clase con mayor score
```

### Recuperar el valor desde el índice
```python
arr = np.array([3, 1, 9, 2])
i = np.argmax(arr)       # 2
arr[i]                   # 9
```

### Posición del pico de una señal
```python
indice_pico = np.argmax(senal)   # muestra donde la señal es máxima
```

### N-D trabajado: la posición global con `unravel_index`
```python
A = np.array([[ 2, 11,  7],
              [ 9,  4, 30]])     # shape (2, 3)
plano = A.argmax()               # 5   → índice aplanado del 30
np.unravel_index(plano, A.shape) # (1, 2)
A[1, 2]                          # 30
```

### Empates: gana el primero
```python
np.argmax([5, 1, 5, 5])          # 0  → hay tres "5", devuelve el primero
```

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| Índice "raro" en 2D+ | con `axis=None` el índice es **aplanado**, no una fila/columna | `np.unravel_index(idx, a.shape)` |
| Apunta a un `NaN` | `NaN` se compara como el mayor y "gana" | usar [[np.nanargmax]] |
| Se esperaba el valor, no la posición | `argmax` devuelve el **índice** | indexar `a[idx]` o usar [[np.max]] |
| `axis=(0, 1)` falla | `argmax` **no** acepta tupla de ejes | reducir un eje, o `argmax` sobre el aplanado |
| Empate "mal resuelto" | siempre gana el **primer** máximo, no el último | revertir el eje (`a[::-1]`) si se quiere el último |

## Notas relacionadas

- [[concepto_axis_parametro]] — qué eje se colapsa y cómo queda el shape
- [[concepto_indexing]] — `np.unravel_index` para traducir el índice aplanado
- [[np.argmin]] — el análogo para el mínimo
- [[np.max]] · [[np.nanargmax]] · [[np.take_along_axis]]
