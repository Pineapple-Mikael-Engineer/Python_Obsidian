---
title: np.argmin — índice (no valor) del mínimo a lo largo de un eje
aliases:
  - argmin
  - np.argmin
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

# np.argmin — índice (no valor) del mínimo a lo largo de un eje

`np.argmin` es el análogo de [[np.argmax]] para el **mínimo**: una reducción que colapsa un eje y
devuelve el **índice entero** donde está el menor valor, no el valor en sí. Responde "¿*dónde* está
el más pequeño?". El shape de salida es el de una reducción sobre ese eje (el eje desaparece, como en
[[np.sum]]), pero el **contenido** son índices en `[0, n_axis)`. Igual que `argmax`, conviene
preguntarse siempre "¿qué eje desaparece?" y "¿este índice está referido a ese eje o al array
**aplanado**?".

## La idea en una fórmula

`argmin` colapsa un eje devolviendo el **argumento** que minimiza a lo largo de él. Para una matriz
$A$ de shape $(m, n)$, sobre el eje `0` produce un vector indexado por la columna $j$ cuyo valor es
la **fila** ganadora:

$$
\text{argmin}_j \;=\; \arg\min_{i\in[0,m)} A_{ij} \qquad \text{(axis=0, desaparece el eje } i\text{)}
$$

y sobre el eje `1`, un vector indexado por la fila $i$ cuyo valor es la **columna** ganadora:

$$
\text{argmin}_i \;=\; \arg\min_{j\in[0,n)} A_{ij} \qquad \text{(axis=1, desaparece el eje } j\text{)}
$$

**El mapa de shapes** es el de cualquier reducción sobre el eje $p$ (ver [[concepto_axis_parametro]]),
con valores de salida en el rango del **tamaño del eje reducido**:

$$
(n_0,\dots,n_k)\ \xrightarrow{\ \text{argmin, axis}=p\ }\ (n_0,\dots,n_{p-1},\,n_{p+1},\dots,n_k)
\quad\text{con valores en } [0,\,n_p)
$$

Y el caso por defecto `axis=None` **aplana primero** el tensor y devuelve un único índice escalar en
$[0,\ \prod_i n_i)$ — sobre el array de 1D, no una posición N-D:

$$
(n_0,\dots,n_k)\ \xrightarrow{\ \text{argmin, axis=None}\ }\ (\,)\ \text{escalar} \in [0,\ n_0\cdots n_k)
$$

## Firma

```python
np.argmin(
    a,                 # array_like: el tensor de entrada
    axis=None,         # None | int: eje a lo largo del cual buscar el mínimo
    out=None,          # ndarray: destino preasignado (dtype entero)
    *,
    keepdims=False,    # bool: conservar el eje reducido con tamaño 1
) -> ndarray | intp
```

## Los parámetros en detalle

### `a` — el tensor de entrada
`array_like` (ndarray, lista, escalar). Se convierte a `ndarray` si no lo es. Sus elementos se
comparan para hallar el mínimo; su `dtype` no afecta al de la salida (que siempre es entero).

### `axis` — eje de búsqueda (y la trampa del aplanado)
El parámetro central, con **una sola dirección** a la vez (no acepta tupla). Valores válidos:
`None` (defecto), un `int` o un eje negativo.

- `None`: **aplana** `a` y devuelve **un** índice escalar sobre esa versión 1D. En un array 2D+ ese
  número **no** es una fila ni una columna, sino la posición en el recorrido fila-por-fila (orden C);
  hay que traducirlo con `np.unravel_index` para obtener la posición real (ver más abajo).
- `int`: reduce ese eje; la salida tiene índices en `[0, a.shape[axis])`.

```python
M = np.array([[1, 9, 3],
              [7, 2, 8]])
np.argmin(M, axis=0)   # [0, 1, 0]  → fila ganadora por columna (índices en [0,2))
np.argmin(M, axis=1)   # [0, 1]     → columna ganadora por fila  (índices en [0,3))
np.argmin(M)           # 0          → índice APLANADO (el 1 está en la posición 0)
```

### `out` — escribir en un buffer existente
`ndarray` preasignado con el **shape de salida** y un `dtype` **entero** (`np.intp`). Evita una
asignación de memoria; útil en bucles. Debe encajar exactamente con la forma del resultado.

### `keepdims` — conservar el eje reducido como tamaño 1
Argumento **solo por palabra clave** (`*`). Si `True`, el eje reducido no desaparece: queda con
tamaño 1, dejando la salida **broadcasteable** contra `a`. Permite recuperar los valores con
`np.take_along_axis` sin perder la alineación.

```python
M = np.array([[1, 9, 3],
              [7, 2, 8]])
idx = np.argmin(M, axis=1, keepdims=True)   # shape (2, 1) → [[0],[1]]
np.take_along_axis(M, idx, axis=1)          # [[1],[2]]  → los valores mínimos
```

## El eje y el caso N-D

La forma sigue la regla de toda reducción: **el eje de `axis` desaparece**; los demás quedan en
orden. El contenido se lee como "la posición ganadora **dentro del eje que se colapsó**".

| `a.shape` | `axis` | salida (shape) | lectura del contenido |
|-----------|--------|----------------|------------------------|
| `(n,)` | `0` o `None` | `()` escalar | índice del mínimo (en `[0, n)`) |
| `(m, n)` | `0` | `(n,)` | por **columna**: qué fila gana (en `[0, m)`) |
| `(m, n)` | `1` | `(m,)` | por **fila**: qué columna gana (en `[0, n)`) |
| `(m, n)` | `None` | `()` | índice **aplanado** (en `[0, m·n)`) |
| `(b, m, n)` | `0` | `(m, n)` | por celda `(i,j)`: qué lámina del lote gana |
| `(b, m, n)` | `-1` | `(b, m)` | por fila de cada matriz: qué columna gana |

```python
T = np.array([[[ 5,  1,  8],
               [ 9,  6,  2]],
              [[ 3,  7,  4],
               [ 0, 11, 10]]])           # shape (2, 2, 3)

T.argmin(axis=0).shape   # (2, 3)
T.argmin(axis=0)
# [[1, 0, 1],     ← por cada (fila, col): qué lámina (0 ó 1) tiene el mínimo
#  [1, 0, 0]]

T.argmin(axis=-1)        # qué columna gana en cada fila de cada lámina
# [[1, 2],        ← lámina 0: fila0 gana col1 (1), fila1 gana col2 (2)
#  [0, 0]]        ← lámina 1: fila0 gana col0 (3), fila1 gana col0 (0)
```

### `axis=None` y `np.unravel_index`

Con el defecto `axis=None`, el índice es plano y no representa una posición N-D directamente.
`np.unravel_index(idx, a.shape)` lo convierte en la tupla de coordenadas (ver [[concepto_indexing]]):

```python
M = np.array([[1, 9, 3],
              [7, 2, 8]])
plano = np.argmin(M)                       # 0   → índice en el array aplanado
fila, col = np.unravel_index(plano, M.shape)  # (0, 0)
M[fila, col]                               # 1   → el mínimo, recuperado por posición
```

## Vectorización

`np.argmin` reemplaza un bucle de "llevar el menor visto hasta ahora". Equivalen, pero la versión
vectorizada recorre el eje en C, sin objetos Python por elemento:

```python
# Bucle Python (lento, explícito): argmin por fila de una matriz
def argmin_filas(M):
    m, n = M.shape
    out = np.empty(m, dtype=np.intp)
    for i in range(m):
        mejor, pos = M[i, 0], 0
        for j in range(1, n):
            if M[i, j] < mejor:     # "<" estricto → conserva el PRIMER mínimo
                mejor, pos = M[i, j], j
        out[i] = pos
    return out

# Vectorizado (NumPy recorre el eje 1 en C):
M.argmin(axis=1)
```

El `<` estricto explica los empates: gana el primer índice. Es el principio de
[[concepto_vectorizacion]]: describes *qué* eje recorrer, no *cómo* iterar.

## Valor de retorno

`argmin` **nunca devuelve el valor mínimo**, siempre un **índice entero** (`np.intp`). El shape
depende de `axis` y `keepdims`:

| Entrada | `axis` | `keepdims` | salida (shape) | tipo |
|---------|--------|------------|----------------|------|
| `(m, n)` | `None` | `False` | `()` | **escalar** `np.intp` (índice aplanado) |
| `(m, n)` | `int` | `False` | shape sin ese eje | `ndarray` de `intp` |
| `(m, n)` | `int` | `True` | ese eje en tamaño 1 | `ndarray` de `intp` |
| `(n,)` | `0` | `False` | `()` | escalar `np.intp` |

El contenido es siempre un índice en `[0, a.shape[axis])` (o en `[0, a.size)` si `axis=None`).

## Casos de uso

### Vecino más cercano (mínima distancia)
```python
distancias = np.linalg.norm(puntos - query, axis=1)
mas_cercano = np.argmin(distancias)   # índice del punto más próximo
```

### Época con menor pérdida
```python
mejor_epoca = np.argmin(historial_loss)
```

### Recuperar el valor desde el índice
```python
arr = np.array([3, 1, 9, 2])
i = np.argmin(arr)       # 1
arr[i]                   # 1
```

### N-D trabajado: la posición global con `unravel_index`
```python
A = np.array([[ 2, 11,  7],
              [-5,  4, 30]])     # shape (2, 3)
plano = A.argmin()               # 3   → índice aplanado del -5
np.unravel_index(plano, A.shape) # (1, 0)
A[1, 0]                          # -5
```

### Empates: gana el primero
```python
np.argmin([5, 1, 1, 9])          # 1  → hay dos "1", devuelve el primero
```

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| Índice "raro" en 2D+ | con `axis=None` el índice es **aplanado**, no una fila/columna | `np.unravel_index(idx, a.shape)` |
| Apunta a un `NaN` | `NaN` se compara de forma poco fiable y puede "ganar" | usar [[np.nanargmin]] |
| Se esperaba el valor, no la posición | `argmin` devuelve el **índice** | indexar `a[idx]` o usar [[np.min]] |
| `axis=(0, 1)` falla | `argmin` **no** acepta tupla de ejes | reducir un eje, o `argmin` sobre el aplanado |
| Empate "mal resuelto" | siempre gana el **primer** mínimo, no el último | revertir el eje (`a[::-1]`) si se quiere el último |

## Notas relacionadas

- [[concepto_axis_parametro]] — qué eje se colapsa y cómo queda el shape
- [[concepto_indexing]] — `np.unravel_index` para traducir el índice aplanado
- [[np.argmax]] — el análogo para el máximo
- [[np.min]] · [[np.nanargmin]] · [[np.take_along_axis]]
