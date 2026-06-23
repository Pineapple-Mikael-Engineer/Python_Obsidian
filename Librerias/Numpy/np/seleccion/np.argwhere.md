---
title: np.argwhere — coordenadas de los no nulos como array (N, k)
aliases:
  - argwhere
  - np.argwhere
tags:
  - numpy
  - api/funcion
  - seleccion

# --- Clasificación ---
lib: numpy
mod: np
tipo: funcion

# --- Comportamiento ---
retorna: ndarray
inplace: false

# --- Dependencias ---
requiere:
  - concepto_indexing

draft: false
---

# np.argwhere — coordenadas de los no nulos como array (N, k)

`np.argwhere` localiza los elementos no-cero de un array y devuelve sus **coordenadas agrupadas por
elemento**: un array 2D donde cada **fila** es la coordenada completa de un no-cero y cada **columna**
es un eje. Es la misma información que [[np.nonzero]] pero con el formato traspuesto: nonzero da una
tupla "por eje", argwhere da un array "por elemento". De hecho la relación es literal,
`argwhere(a) == transpose(nonzero(a))`. Se usa cuando quieres **iterar sobre las coordenadas** o
tenerlas como una tabla `(N, k)`, no cuando quieres indexar (para eso, nonzero).

## La idea en una fórmula

Para una entrada de $k$ ejes con $N$ elementos no-cero, la salida es un array $(N, k)$: una fila por
no-cero, una columna por eje.

$$ a\ \text{de shape}\ (n_0,\dots,n_{k-1}) \ \xrightarrow{\ \text{argwhere}\ }\ \text{array de shape}\ (N,\ k) $$

donde la fila $m$ es la coordenada completa del $m$-ésimo no-cero:

$$ \text{out}[m] \;=\; \big(\,i_0^{(m)},\,i_1^{(m)},\,\dots,\,i_{k-1}^{(m)}\,\big) $$

La relación con [[np.nonzero]] es una **traspuesta** exacta —nonzero apila las coordenadas por eje
(tupla de $k$ vectores de longitud $N$), argwhere las apila por elemento ($N$ filas de $k$ columnas)—:

$$ \texttt{np.argwhere(a)} \;=\; \texttt{np.transpose(np.nonzero(a))} $$

## Firma

```python
np.argwhere(
    a,    # array_like: el tensor de entrada (cualquier dtype)
) -> ndarray  # shape (N, a.ndim)
```

## Los parámetros en detalle

### `a` — el tensor de entrada
`array_like` de cualquier `dtype`. Igual que en [[np.nonzero]], "cero" es el neutro del tipo (`0`,
`0.0`, `False`, `''`, `0+0j`); el resto se reporta. Lo habitual es pasarle una **máscara booleana**
(`a > umbral`), cuyos `True` son los no-cero. `np.nan` cuenta como no-cero (`nan != 0`).

## El caso N-D

El número de **columnas** de la salida es siempre `a.ndim`; el de **filas** es el número de no-ceros.
Cada fila se lee directamente como una coordenada:

```python
# 1D → columna única (cada fila es un índice)
np.argwhere(np.array([0, 3, 0, 5]))
# [[1],
#  [3]]                    → shape (2, 1)

# 2D → dos columnas (fila, columna)
M = np.array([[0, 5], [3, 0]])
np.argwhere(M)
# [[0, 1],
#  [1, 0]]                 → shape (2, 2): coordenadas (0,1) y (1,0)

# 3D → tres columnas
T = np.array([[[0, 5], [0, 0]],
              [[7, 0], [0, 9]]])     # shape (2, 2, 2)
np.argwhere(T)
# [[0, 0, 1],
#  [1, 0, 0],
#  [1, 1, 1]]              → shape (3, 3): una fila por no-cero
```

Como cada fila es una coordenada completa, iterar el resultado da las posiciones directamente:

```python
for z, f, c in np.argwhere(T):
    print((z, f, c), T[z, f, c])     # (0,0,1) 5 · (1,0,0) 7 · (1,1,1) 9
```

## Vectorización

`argwhere` evita el bucle anidado que acumularía coordenadas en una lista de listas:

```python
# Bucle Python (lento, explícito):
coords = []
for i in range(M.shape[0]):
    for j in range(M.shape[1]):
        if M[i, j] != 0:
            coords.append([i, j])
coords = np.array(coords)

# Vectorizado:
coords = np.argwhere(M)
```

Por debajo se apoya en [[concepto_vectorizacion]] vía `nonzero` (recorre el buffer en C) y traspone
el resultado; no hay iteración en Python por elemento.

## Valor de retorno

Siempre un **`ndarray` 2D**, nunca una tupla (esa es la diferencia con [[np.nonzero]]):

| Entrada (shape) | Salida (shape) | Lectura | dtype |
|-----------------|----------------|---------|-------|
| `(n,)` | `(N, 1)` | una columna de índices | `intp` |
| `(m, n)` | `(N, 2)` | filas = `(fila, col)` | `intp` |
| `(n_0,…,n_{k-1})` | `(N, k)` | una fila por no-cero, $k$ columnas | `intp` |

`N = np.count_nonzero(a)`. Si no hay no-ceros, la salida es `(0, k)` (2D vacío, no escalar). El
`dtype` es `intp`.

> [!warning] No sirve para indexar directamente
> `a[np.argwhere(cond)]` **no** recupera los valores que cumplen `cond` (interpreta el array `(N, k)`
> como índices del primer eje). Para indexar usa la **tupla** de [[np.nonzero]]: `a[np.nonzero(cond)]`,
> o la máscara directa `a[cond]`. `argwhere` es para **leer/iterar coordenadas**, no para indexar.

## Casos de uso

### Obtener las coordenadas como tabla
```python
M = np.array([[0, 5], [3, 0]])
np.argwhere(M > 0)         # [[0, 1], [1, 0]]  → tabla de posiciones
```

### Iterar sobre las posiciones que cumplen algo
```python
for i, j in np.argwhere(imagen > umbral):
    marcar(i, j)           # cada fila ya es la coordenada
```

### Caja contenedora (bounding box) de la región activa
```python
coords = np.argwhere(mascara)        # (N, k)
minimos = coords.min(axis=0)         # esquina inferior por eje
maximos = coords.max(axis=0) + 1     # esquina superior (+1 para slice)
recorte = imagen[minimos[0]:maximos[0], minimos[1]:maximos[1]]
```

### N-D: posiciones de los activos en un volumen
```python
vol = np.zeros((4, 4, 4)); vol[1, 2, 3] = vol[0, 0, 1] = 1
np.argwhere(vol)
# [[0, 0, 1],
#  [1, 2, 3]]              → shape (2, 3), una fila por voxel activo
```

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| `a[np.argwhere(cond)]` da basura | `argwhere` no es formato de índice | usar `a[np.nonzero(cond)]` o `a[cond]` |
| Esperar una tupla por eje | `argwhere` devuelve **un array** `(N, k)` | usar [[np.nonzero]] si quieres la tupla |
| Sorpresa con `(N, 1)` en 1D | siempre es 2D, una columna por eje | aplanar con `.ravel()` si quieres 1D |
| `nan` aparece como coordenada | `nan != 0` es `True` | filtrar `nan` antes |

## Notas relacionadas

- [[np.nonzero]] — la misma información como tupla por eje (`argwhere = transpose(nonzero)`)
- [[concepto_indexing]] — por qué para **indexar** se usa nonzero, no argwhere
- [[np.where]] · [[np.extract]] · [[np.count_nonzero]]
