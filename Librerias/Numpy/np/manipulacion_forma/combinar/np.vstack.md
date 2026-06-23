---
title: np.vstack — apila por filas (eje 0), atajo de concatenate
aliases:
  - vstack
  - np.vstack
  - apilar vertical
tags:
  - numpy
  - api/funcion
  - manipulacion

# --- Clasificación ---
lib: numpy
mod: np
tipo: funcion

# --- Comportamiento ---
retorna: ndarray
inplace: false

# --- Dependencias ---
requiere:
  - concepto_shape

draft: false
---

# np.vstack — apila por filas (eje 0), atajo de concatenate

`np.vstack` une una secuencia de arrays **a lo largo del eje 0** (las filas). Es un **atajo de [[np.concatenate]] con `axis=0`**, con un extra cómodo: antes de unir, **promueve los arrays 1D a 2D** tratándolos como filas, de modo que un vector `(n,)` se comporta como `(1, n)`. Es la forma natural de "crecer hacia abajo": apilar observaciones, añadir filas a una matriz.

## La idea en una fórmula

Tras promover cada entrada a al menos 2D, se concatena por el eje 0, que se **suma**:

$$
(a,\,n),(b,\,n)\;\xrightarrow{\ \text{vstack}\ }\;(a+b,\,n)\qquad\text{y}\qquad \underbrace{(n,)}_{1\text{D}}\;\xrightarrow{\ \text{promoción}\ }\;(1,\,n)
$$

Así, $r$ vectores `(n,)` apilados dan `(r, n)`: cada vector es una fila. Equivale a `np.concatenate(map(np.atleast_2d, arrays), axis=0)`.

$$
\begin{bmatrix} 1 & 2 & 3 \end{bmatrix},\;\begin{bmatrix} 4 & 5 & 6 \end{bmatrix}\;\xrightarrow{\ \text{vstack}\ }\;\begin{bmatrix} 1 & 2 & 3 \\ 4 & 5 & 6 \end{bmatrix}\qquad (3,),(3,)\to(2,3)
$$

## Firma

```python
np.vstack(
    tup,         # secuencia de array_like
    *,
    dtype=None,  # dtype: tipo del resultado (NumPy reciente)
    casting="same_kind",
) -> ndarray
```

## Los parámetros en detalle

### `tup` — la secuencia de arrays
Tupla o lista de `array_like`. Los 1D se promueven a `(1, n)`; los 2D+ se dejan igual. Tras la promoción deben coincidir en todos los ejes **salvo el primero** (igual que concatenate sobre `axis=0`).

### `dtype` / `casting`
Fuerzan el [[concepto_dtype|dtype]] de salida y la regla de conversión, como en [[np.concatenate]]. Solo importan si quieres fijar el tipo del resultado.

## El caso N-D

vstack es literalmente `concatenate(..., axis=0)` tras `atleast_2d`. La equivalencia por shape:

| Entrada | Tras promoción | Salida | Equivale a |
|---|---|---|---|
| dos `(3,)` | dos `(1,3)` | `(2,3)` | `concatenate(axis=0)` |
| `(2,3)`, `(1,3)` | igual | `(3,3)` | `concatenate(axis=0)` |
| `(2,3,4)`, `(5,3,4)` | igual | `(7,3,4)` | `concatenate(axis=0)` |

```python
np.vstack((a, b))                # cómodo; promueve 1D a fila
np.concatenate((a, b), axis=0)   # equivalente si a, b ya son 2D
```

## Vectorización

Como atajo de concatenate, reserva el buffer de salida una vez y copia cada array en su banda de filas. El antipatrón sigue siendo apilar **en bucle** (recopia el acumulado cada vez): acumula en una lista y llama a `vstack` una sola vez. Es el principio de [[concepto_vectorizacion]].

## Valor de retorno

Un **nuevo** `ndarray` (copia) de al menos 2D, con el eje 0 sumado. dtype: promoción común de las entradas (o el forzado).

## Casos de uso

### Apilar dos vectores como filas
Dos `(3,)` se promueven a `(1,3)` y se apilan en `(2,3)`:

$$
\begin{bmatrix} 1 & 2 & 3 \end{bmatrix},\;\begin{bmatrix} 4 & 5 & 6 \end{bmatrix}\;\xrightarrow{\ \text{vstack}\ }\;\begin{bmatrix} 1 & 2 & 3 \\ 4 & 5 & 6 \end{bmatrix}\qquad (3,),(3,)\to(2,3)
$$

```python
filas = [np.random.rand(4) for _ in range(5)]
matriz = np.vstack(filas)      # (5, 4)  → cada vector es una fila
```

### Añadir una fila a una matriz
```python
M = np.ones((3, 4))
nueva = np.zeros(4)            # (4,)
M = np.vstack((M, nueva))      # (4, 4)  → la fila 1D se promueve
```

### 4D: unir dos lotes de imágenes por el eje 0
Sobre arrays 4D `(N,3,32,32)`, vstack es exactamente `concatenate(axis=0)`: suma el eje del lote dejando intactos canal, alto y ancho:

```python
lote_a = np.random.rand(8, 3, 32, 32)   # 8 imágenes (3,32,32)
lote_b = np.random.rand(4, 3, 32, 32)   # 4 imágenes
todo = np.vstack((lote_a, lote_b))      # (12, 3, 32, 32)  → 4D
# ejes: (lote=12, canal=3, alto=32, ancho=32)
```

### 5D: apilar lotes de vídeos por el eje 0
Sobre tensores 5D `(N,10,3,32,32)` (vídeo, frame, canal, alto, ancho), vstack apila el eje de vídeo:

```python
v1 = np.random.rand(4, 10, 3, 32, 32)   # 4 vídeos
v2 = np.random.rand(2, 10, 3, 32, 32)   # 2 vídeos más
todo = np.vstack((v1, v2))              # (6, 10, 3, 32, 32)  → 5D
# ejes: (vídeo=4+2=6, frame=10, canal=3, alto=32, ancho=32)
```

## Errores comunes

| Error | Causa | Solución |
|---|---|---|
| `dimensions ... must match exactly` | difieren las columnas (eje 1+) | igualar las demás dimensiones |
| Forma inesperada con escalares | se pasaron 0D | `np.atleast_2d` antes |
| Querías un eje nuevo y no filas | confundir con [[np.stack]] | usar `stack` si necesitas `ndim + 1` |

## Notas relacionadas

- [[concepto_shape]] — la promoción 1D a fila `(1, n)`
- [[np.concatenate]] — la función base (vstack = `axis=0`)
- [[np.hstack]] — el equivalente por columnas
- [[np.stack]] · [[np.dstack]] · [[np.column_stack]] — los otros atajos
