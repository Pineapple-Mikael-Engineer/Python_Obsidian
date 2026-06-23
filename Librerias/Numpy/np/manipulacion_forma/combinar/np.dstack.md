---
title: np.dstack — apila en profundidad (eje 2), atajo de concatenate
aliases:
  - dstack
  - np.dstack
  - apilar profundidad
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

# np.dstack — apila en profundidad (eje 2), atajo de concatenate

`np.dstack` une una secuencia de arrays **a lo largo del tercer eje** (la profundidad, `axis=2`). Es un **atajo de [[np.concatenate]] sobre el eje 2**, con promoción previa: lleva cada entrada a al menos 3D insertando los ejes que falten, de modo que un `(m, n)` se trata como `(m, n, 1)` y un `(n,)` como `(1, n, 1)`. Es la forma natural de componer capas 2D en un volumen: canales RGB, mapas apilados en profundidad.

## La idea en una fórmula

Tras promover a 3D, concatena por el eje 2, que se **suma**:

$$
(m,\,n,\,a),(m,\,n,\,b)\;\xrightarrow{\ \text{dstack}\ }\;(m,\,n,\,a+b)\qquad\text{con}\qquad \underbrace{(m,\,n)}_{2\text{D}}\;\xrightarrow{\ \text{promoción}\ }\;(m,\,n,\,1)
$$

Así, $r$ matrices `(m, n)` apiladas dan `(m, n, r)`: cada matriz es una capa de profundidad. Equivale a `np.concatenate(map(np.atleast_3d, arrays), axis=2)`, y cuando las entradas son 2D del mismo shape coincide con `np.stack(arrays, axis=-1)`.

## Firma

```python
np.dstack(
    tup,   # secuencia de array_like
) -> ndarray
```

## Los parámetros en detalle

### `tup` — la secuencia de arrays
Tupla o lista de `array_like`. Cada entrada se promueve a 3D: `(n,)` → `(1, n, 1)`, `(m, n)` → `(m, n, 1)`. Tras la promoción deben coincidir en los dos primeros ejes (filas y columnas); se unen en profundidad.

## El caso N-D

| Entrada | Tras promoción | Salida | Equivale a |
|---|---|---|---|
| dos `(2,3)` | dos `(2,3,1)` | `(2,3,2)` | `stack(axis=-1)` |
| dos `(3,)` | dos `(1,3,1)` | `(1,3,2)` | `concatenate(axis=2)` |
| `(2,3,2)`, `(2,3,4)` | igual | `(2,3,6)` | `concatenate(axis=2)` |

```python
a = np.array([[1, 2], [3, 4]])
b = np.array([[5, 6], [7, 8]])
np.dstack((a, b)).shape   # (2, 2, 2)  → cada matriz es una capa
```

## Vectorización

Como atajo de concatenate, reserva el buffer `(m, n, suma)` una vez y copia cada capa en su rebanada de profundidad. Apilar en bucle recopia el acumulado: acumula en lista y une una vez ([[concepto_vectorizacion]]).

## Valor de retorno

Un **nuevo** `ndarray` (copia) de al menos 3D, con el eje 2 sumado. dtype: promoción común de las entradas.

## Casos de uso

### Componer canales de color en una imagen
Dos matrices `(2,2)` se promueven a `(2,2,1)` y se apilan en profundidad como `(2,2,2)`:

$$
\begin{bmatrix} 1 & 2 \\ 3 & 4 \end{bmatrix},\;\begin{bmatrix} 5 & 6 \\ 7 & 8 \end{bmatrix}\;\xrightarrow{\ \text{dstack}\ }\;(2,2,2)\quad\text{con capa 0}=\begin{bmatrix} 1 & 2 \\ 3 & 4 \end{bmatrix},\ \text{capa 1}=\begin{bmatrix} 5 & 6 \\ 7 & 8 \end{bmatrix}
$$

```python
r = np.zeros((100, 100))
g = np.ones((100, 100))
b = np.zeros((100, 100))
rgb = np.dstack((r, g, b))      # (100, 100, 3)  → cada canal una capa
```

### Apilar mapas 2D como volumen
```python
capas = [np.full((4, 4), k) for k in range(3)]
vol = np.dstack(capas)          # (4, 4, 3)
vol[:, :, 1]                    # la capa 1, llena de 1, shape (4, 4)
```

### 4D: crecer el eje 2 de un tensor
Sobre arrays ya 3D/4D, dstack une por `axis=2` **sin promover nada**, y exige que todos los demás ejes coincidan. Sobre dos tensores 4D `(N, H, W, C)`, el eje 2 es el ancho:

```python
a = np.random.rand(8, 32, 16, 3)   # lote 8, alto 32, ancho 16, 3 canales
b = np.random.rand(8, 32,  8, 3)   # 8 columnas más de ancho
todo = np.dstack((a, b))           # (8, 32, 24, 3)  → 4D
# ejes: (lote=8, alto=32, ancho=16+8=24, canal=3)  → suma el eje 2
```

### 5D: crecer el eje 2 en un lote de vídeos
Sobre tensores 5D `(V, F, H, W, C)`, dstack toca `axis=2`, que aquí es el alto; los demás ejes deben coincidir:

```python
v1 = np.random.rand(4, 10, 16, 32, 3)   # alto=16
v2 = np.random.rand(4, 10,  8, 32, 3)   # 8 filas más de alto
todo = np.dstack((v1, v2))              # (4, 10, 24, 32, 3)  → 5D
# ejes: (vídeo=4, frame=10, alto=16+8=24, ancho=32, canal=3)  → suma el eje 2
```

## Errores comunes

| Error | Causa | Solución |
|---|---|---|
| `dimensions must match` | filas o columnas distintas | igualar los dos primeros ejes |
| Eje extra inesperado | confundir con [[np.hstack]] | recordar que une en profundidad (eje 2) |
| Querías otro eje | dstack fija `axis=2` | usar [[np.stack]] / [[np.concatenate]] |

## Notas relacionadas

- [[concepto_shape]] — la promoción a `(m, n, 1)`
- [[np.concatenate]] — la función base (dstack = `axis=2`)
- [[np.stack]] — `stack(axis=-1)` coincide para 2D del mismo shape
- [[np.vstack]] · [[np.hstack]] · [[np.column_stack]] — los otros atajos
