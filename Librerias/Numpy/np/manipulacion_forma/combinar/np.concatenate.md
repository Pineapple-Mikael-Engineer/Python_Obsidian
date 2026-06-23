---
title: np.concatenate — une arrays a lo largo de un eje existente
aliases:
  - concatenate
  - np.concatenate
  - concatenar
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
  - concepto_axis_parametro

draft: false
---

# np.concatenate — une arrays a lo largo de un eje existente

`np.concatenate` es la operación **base** de combinar: toma una secuencia de arrays y los pega a lo largo de un **eje que ya existe**. No crea dimensiones nuevas (para eso está [[np.stack]]): se limita a hacer crecer un eje sumando las longitudes que cada array aporta en él. La pregunta al usarla siempre es la misma: **¿qué eje crece?** Ese es `axis`, y es el único en el que los shapes pueden diferir.

## La idea en una fórmula

Todos los arrays comparten shape salvo en el eje `axis`, cuya longitud se **suma**. Para dos arrays que coinciden en todo menos en `axis=p` (donde valen $a$ y $b$):

$$
(n_0,\dots,n_{p-1},\,a,\,n_{p+1},\dots,n_{k-1}),\;(n_0,\dots,n_{p-1},\,b,\,n_{p+1},\dots,n_{k-1})\;\xrightarrow{\ \text{axis}=p\ }\;(n_0,\dots,n_{p-1},\,a+b,\,n_{p+1},\dots,n_{k-1})
$$

El `ndim` **no cambia**: solo el tamaño del eje `p` pasa de $a$ y $b$ a $a+b$. Con $r$ arrays, el eje resultante mide la suma de las $r$ longitudes. Visto en $2\times2$ sobre el eje 0:

$$
\begin{bmatrix} 1 & 2 \\ 3 & 4 \end{bmatrix},\;\begin{bmatrix} 5 & 6 \end{bmatrix}\;\xrightarrow{\ \text{axis}=0\ }\;\begin{bmatrix} 1 & 2 \\ 3 & 4 \\ 5 & 6 \end{bmatrix}\qquad (2,2),(1,2)\to(3,2)
$$

## Firma

```python
np.concatenate(
    (a1, a2, ...),   # secuencia de array_like del mismo ndim
    axis=0,          # int | None: eje (existente) a lo largo del cual unir
    out=None,        # ndarray: destino preasignado del resultado
    dtype=None,      # dtype: tipo del resultado (NumPy >= 1.20)
    casting="same_kind",  # regla de conversión cuando se fuerza dtype
) -> ndarray
```

## Los parámetros en detalle

### `(a1, a2, ...)` — la secuencia de arrays
Tupla o lista de `array_like`. **Todos deben tener el mismo `ndim`** y coincidir en todos los ejes salvo en `axis`. No se crean ejes nuevos: mezclar 1D con 2D falla (iguala antes con [[concepto_shape|reshape/expand_dims]] o usa [[np.stack]]).

### `axis` — el eje que crece
`int` (defecto `0`) o `None`. Es el único eje en el que las longitudes pueden diferir; su tamaño de salida es la suma. Acepta ejes negativos (`axis=-1` = último). Con `axis=None`, **aplana** todos los arrays y concatena en 1D:

```python
a = np.array([[1, 2], [3, 4]])
b = np.array([[5, 6], [7, 8]])
np.concatenate((a, b), axis=None)   # [1 2 3 4 5 6 7 8]  → (8,)
```

### `out` — escribir en un buffer existente
`ndarray` preasignado con el shape y dtype **exactos** de la salida. Evita una asignación de memoria; útil en bucles. Si se da, su dtype manda salvo que también se pase `dtype`.

### `dtype` — tipo del resultado
Fuerza el [[concepto_dtype|dtype]] de salida sin una conversión posterior. No puede usarse junto con `out`. Disponible desde NumPy 1.20.

### `casting` — regla de conversión
Controla qué conversiones se permiten al aplicar `dtype` (`"no"`, `"equiv"`, `"safe"`, `"same_kind"` por defecto, `"unsafe"`). Solo importa cuando fuerzas `dtype` y quieres impedir conversiones con pérdida.

## El caso N-D

La regla es mecánica: **se suma el eje `axis`, los demás deben coincidir exactamente**. En cualquier número de dimensiones, basta verificar que todos los shapes son idénticos salvo en la posición de `axis`:

| Shapes de entrada | `axis` | Salida | Lectura |
|---|---|---|---|
| `(3,)`, `(2,)` | `0` | `(5,)` | un vector más largo |
| `(2,3)`, `(4,3)` | `0` | `(6,3)` | más filas |
| `(2,3)`, `(2,5)` | `1` | `(2,8)` | más columnas |
| `(2,3,4)`, `(2,3,4)` | `0` | `(4,3,4)` | apila dos lotes |
| `(2,3,4)`, `(2,5,4)` | `1` | `(2,8,4)` | crece el eje central |

```python
# Dos lotes de "imágenes" (lote, alto, ancho) unidos por el eje del lote:
A = np.zeros((2, 3, 4))
B = np.zeros((5, 3, 4))
np.concatenate((A, B), axis=0).shape   # (7, 3, 4)  → 2+5 lotes
np.concatenate((A, A), axis=2).shape   # (2, 3, 8)  → crece el ancho
```

## Vectorización

`concatenate` reserva el buffer de salida una sola vez (de tamaño $a_0 + a_1 + \dots$) y copia cada array en su tramo en C. El antipatrón es **concatenar dentro de un bucle**, que reasigna y recopia todo en cada paso ($O(n^2)$ en memoria movida):

```python
# Mal: copia el acumulado en cada iteración
out = np.empty((0, 4))
for b in bloques:
    out = np.concatenate((out, b), axis=0)   # O(n^2)

# Bien: acumula en una lista Python y concatena UNA vez
out = np.concatenate(bloques, axis=0)        # O(n)
```

Es el mismo principio de [[concepto_vectorizacion]]: una sola operación sobre todos los datos en vez de muchas pequeñas en el intérprete.

## Valor de retorno

Siempre un **nuevo** `ndarray` (copia; no existe versión vista al fusionar buffers independientes). El `ndim` es el de las entradas; el dtype es la promoción común de todas, salvo que se fije `dtype`.

| Entradas | `axis` | Salida (shape) | dtype |
|---|---|---|---|
| `(m,n)`, `(p,n)` | `0` | `(m+p, n)` | promoción común |
| `(m,n)`, `(m,q)` | `1` | `(m, n+q)` | promoción común |
| `(m,n)`, `(p,q)` | `None` | `(m·n + p·q,)` | promoción común |
| varios `int8` + `int64` | cualquiera | suma en `axis` | `int64` (promoción) |

## Casos de uso

### Unir dos matrices por filas
Dos bloques `(2,2)` unidos por `axis=0` apilan sus filas en una `(4,2)`:

$$
\begin{bmatrix} 1 & 2 \\ 3 & 4 \end{bmatrix},\;\begin{bmatrix} 5 & 6 \\ 7 & 8 \end{bmatrix}\;\xrightarrow{\ \text{axis}=0\ }\;\begin{bmatrix} 1 & 2 \\ 3 & 4 \\ 5 & 6 \\ 7 & 8 \end{bmatrix}\qquad (2,2),(2,2)\to(4,2)
$$

```python
A = np.array([[1, 2], [3, 4]]); B = np.array([[5, 6], [7, 8]])
np.concatenate((A, B), axis=0)   # → (4, 2)
np.concatenate((A, B), axis=1)   # → (2, 4)  → crece el ancho
```

### Añadir columnas a una matriz
```python
X = np.ones((100, 3))
nueva = np.zeros((100, 1))
X = np.concatenate((X, nueva), axis=1)   # (100, 4)
```

### 4D: unir dos lotes de imágenes por el eje del lote
Dos lotes 4D `(8,3,32,32)` y `(4,3,32,32)` coinciden en canal, alto y ancho; solo crece `axis=0` (el lote):

```python
lote_a = np.random.rand(8, 3, 32, 32)   # 8 imágenes
lote_b = np.random.rand(4, 3, 32, 32)   # 4 imágenes
todo = np.concatenate((lote_a, lote_b), axis=0)   # (12, 3, 32, 32)  → 4D
# ejes: (lote=8+4=12, canal=3, alto=32, ancho=32)
```

### 5D: alargar un lote de vídeos por el eje de frames
Dos tensores 5D `(4,10,3,32,32)` (vídeo, frame, canal, alto, ancho) unidos por `axis=1` suman sus frames sin tocar los demás ejes:

```python
v1 = np.random.rand(4, 10, 3, 32, 32)   # 4 vídeos de 10 frames
v2 = np.random.rand(4,  6, 3, 32, 32)   # los mismos 4 vídeos, 6 frames más
largo = np.concatenate((v1, v2), axis=1)   # (4, 16, 3, 32, 32)  → 5D
# ejes: (vídeo=4, frame=10+6=16, canal=3, alto=32, ancho=32)
```

## Errores comunes

| Error | Causa | Solución |
|---|---|---|
| `all the input array dimensions except for the concatenation axis must match exactly` | shapes difieren en un eje que no es `axis` | revisar/ajustar los demás ejes |
| `zero-dimensional arrays cannot be concatenated` | se pasaron escalares (0D) | `np.atleast_1d` antes |
| `all the input arrays must have same number of dimensions` | se mezcló 1D con 2D | igualar `ndim` (`reshape`/`expand_dims`) o usar [[np.stack]] |
| Rendimiento pésimo | concatenar en bucle | acumular en lista y unir una vez |
| Aparece un eje de más | querías un eje **nuevo** | usar [[np.stack]], no `concatenate` |

## Notas relacionadas

- [[concepto_shape]] — qué shapes son compatibles para unir
- [[concepto_axis_parametro]] — qué significa el eje que crece
- [[np.stack]] — la alternativa que crea un eje nuevo
- [[np.vstack]] · [[np.hstack]] · [[np.dstack]] — atajos por eje fijo
- [[np.split]] — la operación inversa
