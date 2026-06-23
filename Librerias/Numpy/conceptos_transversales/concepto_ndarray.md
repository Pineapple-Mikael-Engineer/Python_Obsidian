---
title: ndarray — La estructura base de NumPy
aliases:
  - array
  - arreglo
  - ndarray
tags:
  - numpy
  - concepto
  - estructura
lib: numpy
tipo: concepto
requiere:
  - none
draft: false
---

# ndarray — La estructura base de NumPy

## Definición fundamental

Un `ndarray` es un **buffer de bytes contiguo en memoria** acompañado de un puñado de metadatos que le dicen a NumPy cómo *interpretar* ese buffer como un tensor multidimensional. No es una lista de listas anidadas: es **un único bloque lineal** de RAM más una descripción de cómo recorrerlo.

Toda operación de NumPy, de la más simple a la más compleja, manipula uno o más `ndarray`, y casi siempre lo hace **tocando los metadatos en vez de mover los datos**. Esa es la idea que hay que interiorizar.

## Por qué existe: separar los datos de su interpretación

Un `ndarray` divide deliberadamente dos cosas:

- **Los datos**: una secuencia plana de bytes, igual que un array de C. Compacta, contigua, cache-friendly.
- **La interpretación**: tres metadatos —`shape`, `dtype`, `strides`— que dicen cuántos elementos hay por eje, de qué tipo son y cuántos bytes hay que saltar para avanzar en cada eje.

Esta separación es la que hace que `a.T`, `a.reshape(...)` o un slice `a[1:, ::2]` puedan devolver una **vista** (otro `ndarray` que apunta al *mismo* buffer con metadatos distintos) sin copiar un solo byte. La estructura del dato es barata de reinterpretar; el dato en sí no se toca.

## La estructura: buffer + 3 metadatos

Un `ndarray` se compone del bloque de datos y tres descriptores. Los strides son la pieza clave, pero conviene verlos juntos.

| Componente | Qué es | Atributo |
|---|---|---|
| Buffer de datos | Bloque contiguo de bytes con los valores brutos | `ndarray.data` |
| `shape` | Tupla $(n_0,\dots,n_{k-1})$ con el tamaño de cada eje | `ndarray.shape` |
| `dtype` | Tipo uniforme de los elementos (define el `itemsize`) | `ndarray.dtype` |
| `strides` | Tupla $(s_0,\dots,s_{k-1})$: bytes a saltar por paso en cada eje | `ndarray.strides` |

El `shape` se desarrolla en [[concepto_shape]] y el `dtype` en [[concepto_dtype]]. Aquí el protagonista son los **strides**, porque son los que explican *por qué NumPy es rápido y por qué tantas operaciones no copian*.

## La clave: los strides y la fórmula del offset

Un `strides` es una tupla $(s_0,\dots,s_{k-1})$ donde $s_d$ son los **bytes que hay que avanzar en el buffer para incrementar en 1 el índice del eje $d$**. Con eso, localizar cualquier elemento es una sola cuenta aritmética —no una búsqueda anidada—:

$$ \text{offset}(i_0,\dots,i_{k-1}) \;=\; \sum_{d=0}^{k-1} i_d \cdot s_d $$

donde el offset son los bytes desde el inicio del buffer hasta el elemento $A[i_0, i_1, \dots, i_{k-1}]$. Esta fórmula lineal es **todo el modelo de acceso** de un `ndarray`, y de ella se desprenden las tres consecuencias importantes:

- **`a.T` no copia.** Transponer es simplemente **invertir la tupla de strides** (y la de shape). El buffer no se mueve; solo cambia el orden en que se interpretan los ejes. Por eso `a.T` es $O(1)$.
- **El slicing es una vista.** Un slice ajusta el puntero de inicio y los strides (p. ej. `a[::2]` duplica el stride del eje), pero sigue apuntando al mismo buffer. Ver [[concepto_views_vs_copias]].
- **El recorrido es rápido.** Cuando los strides hacen que los elementos consecutivos estén contiguos en memoria (C-order), la CPU explota la **localidad de caché** y la prebúsqueda. Ese es el corazón de la ventaja de rendimiento.

### Cómo se calculan los strides en C-order

En el orden por defecto (C-order, *row-major*), el último eje es el contiguo, y el stride de un eje es el `itemsize` multiplicado por el **producto de los tamaños de los ejes posteriores**:

$$ s_d \;=\; \text{itemsize} \cdot \prod_{j=d+1}^{k-1} n_j $$

El último eje siempre tiene $s_{k-1} = \text{itemsize}$ (producto vacío $= 1$).

## Ejemplo N-D concreto: un `(2, 3, 4)` de `int64`

Tomemos un tensor de shape $(2, 3, 4)$ y `dtype` `int64`, de modo que `itemsize = 8` bytes.

```python
import numpy as np
A = np.arange(24, dtype=np.int64).reshape(2, 3, 4)
A.shape      # (2, 3, 4)
A.itemsize   # 8
A.strides    # (96, 32, 8)
```

De dónde sale cada número, aplicando $s_d = \text{itemsize}\cdot\prod_{j>d} n_j$:

| Eje $d$ | Tamaño $n_d$ | Ejes posteriores | $\prod_{j>d} n_j$ | $s_d = 8\cdot\prod$ |
|---|---|---|---|---|
| 0 | 2 | $(3, 4)$ | $3\cdot 4 = 12$ | $8\cdot 12 = 96$ |
| 1 | 3 | $(4,)$ | $4$ | $8\cdot 4 = 32$ |
| 2 | 4 | — | $1$ | $8\cdot 1 = 8$ |

Lectura: para pasar a la siguiente "matriz" (eje 0) saltas 96 bytes (una matriz $3\times4$ entera = 12 elementos); para bajar una fila (eje 1) saltas 32 bytes (4 elementos); para avanzar una columna (eje 2) saltas 8 bytes (un `int64`). Y el offset del elemento `A[1, 2, 3]` es, en bytes:

$$ 1\cdot 96 + 2\cdot 32 + 3\cdot 8 \;=\; 96 + 64 + 24 \;=\; 184 \;=\; 23 \cdot 8 $$

es decir, el elemento número 23 del buffer —exactamente el último, como cabía esperar de `arange(24)`.

## Propiedades derivadas

Todo lo demás se calcula a partir de los cuatro componentes:

| Atributo | Fórmula | Ejemplo `(2, 3, 4)` int64 |
|---|---|---|
| `ndarray.ndim` | $k = \text{len(shape)}$ | `3` |
| `ndarray.size` | $\prod_i n_i$ | `24` |
| `ndarray.itemsize` | `dtype.itemsize` | `8` |
| `ndarray.nbytes` | `size × itemsize` | `192` |
| `ndarray.T` | strides y shape invertidos | shape `(4, 3, 2)` |

## Orden de almacenamiento: C-order vs F-order

El mismo `shape` admite dos formas de tender los datos en el buffer, y la diferencia vive **enteramente en los strides**:

| Orden | Eje contiguo | Strides de `(m, n)` | Uso |
|---|---|---|---|
| C-order (*row-major*) | el último | `(n·itemsize, itemsize)` | por defecto en NumPy |
| F-order (*column-major*) | el primero | `(itemsize, m·itemsize)` | interoperar con Fortran / BLAS |

```python
c = np.array([[1, 2, 3], [4, 5, 6]], dtype=np.int64)            # C-order
f = np.array([[1, 2, 3], [4, 5, 6]], dtype=np.int64, order='F') # F-order
c.strides   # (24, 8)  → fila contigua
f.strides   # (8, 16)  → columna contigua
c.flags.c_contiguous   # True
f.flags.f_contiguous   # True
```

La contigüidad (que el recorrido lineal del buffer respete los strides sin huecos) se detalla en [[concepto_contiguidad_memoria]] y es lo que decide si un `reshape` puede ser vista o se ve forzado a copiar.

## Casos que fallan (errores típicos)

| Error | Por qué | Realidad |
|---|---|---|
| Asumir que `a.T` copia | Transponer solo invierte los strides | `a.T` es una **vista** $O(1)$; modificarla modifica `a` |
| Asumir que `a.reshape(...)` siempre copia | Si el array es contiguo, solo reescribe shape/strides | Devuelve una **vista** salvo que la nueva forma exija reordenar memoria |
| Confundir `(3,)` con `(3, 1)` | Tienen los mismos valores pero distinto `ndim` | `(3,)` es 1D; `(3, 1)` es 2D (columna) → afecta a [[concepto_broadcasting]] |
| Mezclar tipos en un mismo array | El `dtype` es **homogéneo** por construcción | Para datos heterogéneos: dtype estructurado |

> [!warning] La trampa de la vista
> Como `a.T`, los slices y muchos `reshape` comparten el buffer con el original, escribir en ellos
> **muta el array de partida**. Si necesitas independencia, copia explícitamente con `.copy()`.

## Relación con otros conceptos

- [[concepto_shape]]
- [[concepto_dtype]]
- [[concepto_contiguidad_memoria]]
- [[concepto_views_vs_copias]]
- [[concepto_broadcasting]]
- [[concepto_vectorizacion]]
