---
title: Shape — La forma dimensional de un array
aliases:
  - shape
  - forma
  - dimensiones
tags:
  - numpy
  - concepto
  - shape
lib: numpy
tipo: concepto
requiere:
  - concepto_ndarray
draft: false
---

# Shape — La forma dimensional de un array

## Definición fundamental

El **shape** es la tupla de enteros no negativos $(n_0, n_1, \dots, n_{k-1})$ que describe cuántos elementos hay en cada eje de un [[concepto_ndarray|ndarray]]. Es el metadato que convierte un buffer lineal de memoria en un tensor navegable: dice cómo *interpretar* los bytes, no los almacena.

De él se derivan las dos magnitudes que se usan a todas horas:

$$ \text{ndim} \;=\; k \;=\; \text{len(shape)} \qquad\qquad \text{size} \;=\; \prod_{i=0}^{k-1} n_i $$

`ndim` es el número de ejes (el *rango* del tensor) y `size` es el total de elementos. El mismo buffer puede llevar shapes distintos sin copiar un solo byte, porque cambiar el shape solo reescribe esta tupla (y los `strides` asociados).

## Por qué existe: el espacio lógico sobre el buffer

Sin shape, un `ndarray` sería una secuencia plana de números. El shape es lo que le da una **estructura de coordenadas**: con $(2, 3)$ el buffer `[0,1,2,3,4,5]` se lee como una matriz $2\times3$; con $(6,)$ como un vector; con $(1,2,3)$ como un tensor. Mismos bytes, distinto espacio lógico.

```python
import numpy as np

base = np.arange(6)               # buffer [0,1,2,3,4,5]
base.reshape(6).shape             # (6,)      → vector
base.reshape(2, 3).shape          # (2, 3)    → matriz 2×3
base.reshape(1, 2, 3).shape       # (1, 2, 3) → tensor
```

Por eso, **toda operación de NumPy se razona preguntando primero qué le pasa al shape**: ese es el propósito del "mapa de shapes".

## La regla central: la notación $(n_0,\dots,n_k)$ y el mapa de shapes

El resto de notas describe cada función con un **mapa de shapes**: una transformación explícita de la forma de entrada en la forma de salida, escrita en notación general

$$ (n_0, n_1, \dots, n_{k-1}) \;\xrightarrow{\ \text{operación}\ }\; (\text{shape de salida}). $$

Esta es la herramienta que hace *predecible* el comportamiento N-D. Las tres familias básicas:

**Reducción — quita un eje.** Una reducción a lo largo del eje $p$ (`sum`, `mean`, `max`...) colapsa ese eje y lo elimina:

$$ (n_0,\dots,n_{p-1},\,n_p,\,n_{p+1},\dots,n_{k-1}) \;\xrightarrow{\ \text{axis}=p\ }\; (n_0,\dots,n_{p-1},\,n_{p+1},\dots,n_{k-1}) $$

Con `keepdims=True` el eje no desaparece, queda en tamaño 1: $\dots,n_{p-1},\,1,\,n_{p+1},\dots$

**Reshape — reorganiza con $\prod$ constante.** Cambia la tupla siempre que el producto (el `size`) se conserve; no toca el orden de los datos en memoria:

$$ (n_0,\dots,n_{k-1}) \;\xrightarrow{\ \text{reshape}\ }\; (m_0,\dots,m_{r-1}) \quad\text{sujeto a}\quad \prod_i n_i = \prod_j m_j $$

**Transpose — permuta los ejes.** Reordena la tupla según una permutación $\pi$; el `size` es el mismo, cambia solo la disposición:

$$ (n_0,\dots,n_{k-1}) \;\xrightarrow{\ \text{transpose}\ }\; (n_{\pi(0)},\dots,n_{\pi(k-1)}) $$

| Operación | Mapa de shapes | Ejemplo |
|---|---|---|
| `reshape` | redistribuye con $\prod$ constante | `(12,) → (3, 4)` |
| `ravel` / `flatten` | aplana a 1D | `(3, 4) → (12,)` |
| `transpose` / `.T` | permuta (invierte) los ejes | `(3, 4) → (4, 3)` |
| `expand_dims` / `newaxis` | inserta un eje de tamaño 1 | `(3,) → (1, 3)` |
| `squeeze` | elimina ejes de tamaño 1 | `(1, 3, 1) → (3,)` |
| reducción (`sum`, `mean`) | quita el eje `axis` | `(2, 3) → (3,)` con `axis=0` |

## La diferencia crucial: `(3,)` vs `(3, 1)` vs `(1, 3)`

Tres tuplas con los mismos tres valores, pero **distinto `ndim` y, por tanto, distinto comportamiento**. Esto es el origen del error más común con shapes, y la razón vive en [[concepto_broadcasting]], que alinea los shapes **por la derecha**.

| Shape | `ndim` | Es | Al alinear por la derecha |
|---|---|---|---|
| `(3,)` | 1 | vector | se completa a `(1, 3)` → actúa como **fila** |
| `(1, 3)` | 2 | matriz fila | una fila, 3 columnas |
| `(3, 1)` | 2 | matriz columna | 3 filas, una columna |

```python
np.zeros((3,)).ndim     # 1  → vector
np.zeros((1, 3)).ndim   # 2  → fila
np.zeros((3, 1)).ndim   # 2  → columna

# La consecuencia en broadcasting:
fila    = np.array([1, 2, 3])            # (3,)   → se ve como (1, 3)
columna = np.array([[1], [2], [3]])      # (3, 1)
(fila + columna).shape                   # (3, 3) → producto externo de formas
```

`(3,)` y `(3, 1)` **no son intercambiables**: una operación que espera una columna y recibe un vector 1D (o al revés) o bien falla, o bien hace broadcasting silencioso a un shape que no querías.

## Ejemplos progresivos

### Nivel 1: inspeccionar y validar

```python
arr = np.array([[1, 2, 3],
                [4, 5, 6]])
arr.shape   # (2, 3)
arr.ndim    # 2
arr.size    # 6

assert arr.shape == (2, 3)   # validar la forma antes de operar
```

### Nivel 2: añadir y quitar ejes

```python
v = np.array([1, 2, 3])      # (3,)

columna = v[:, np.newaxis]   # (3, 1)
fila    = v[np.newaxis, :]   # (1, 3)
columna.squeeze().shape      # (3,)  → elimina el eje de tamaño 1
```

### Nivel 3 (N-D): leer el shape de un tensor de imágenes

Un lote de imágenes en color se suele representar con un shape de 4 ejes $(\text{lote}, \text{alto}, \text{ancho}, \text{canales})$. Leer el shape *es* entender el dato:

```python
imgs = np.zeros((32, 128, 256, 3))   # (lote, alto, ancho, canales)
imgs.shape    # (32, 128, 256, 3)
imgs.ndim     # 4
imgs.size     # 32*128*256*3 = 3_145_728

# Interpretación eje por eje:
#   eje 0 = 32   → 32 imágenes en el lote
#   eje 1 = 128  → 128 filas de píxeles (alto)
#   eje 2 = 256  → 256 columnas de píxeles (ancho)
#   eje 3 = 3    → 3 canales de color (R, G, B)

imgs[5]            # shape (128, 256, 3)  → la imagen nº 5
imgs[:, :, :, 0]   # shape (32, 128, 256) → solo el canal rojo de todas
imgs.mean(axis=(1, 2))   # (32, 3) → color medio por imagen (reduce alto y ancho)
```

El último ejemplo es un mapa de shapes en acción: $(32, 128, 256, 3) \xrightarrow{\ \text{mean, axis}=(1,2)\ } (32, 3)$, porque la reducción **quita** los ejes 1 y 2.

## Casos que fallan (errores típicos)

### Error 1: reshape con `size` incompatible

```python
np.arange(10).reshape(3, 4)
# ValueError: cannot reshape array of size 10 into shape (3,4)
# 3*4 = 12 ≠ 10  → el producto no se conserva
```

### Error 2: confundir el vector `(n,)` con la matriz columna `(n, 1)`

```python
v = np.array([1, 2, 3])   # (3,)
v.shape == (3, 1)         # False → NO es una columna
# Para una columna real: v.reshape(-1, 1) o v[:, np.newaxis]
```

### Error 3: perder un eje y romper el broadcasting

```python
A = np.ones((4, 3))   # (4, 3)
c = np.ones((4,))     # (4,)  → se alinea por la derecha como (1, 4)
A + c                 # ValueError: la última dim 3 no casa con 4
A + c[:, np.newaxis]  # OK → c pasa a (4, 1), compatible con (4, 3)
```

El fallo no es de `c`, sino de su shape: al alinearse por la derecha, `(4,)` choca contra el eje de tamaño 3. Recuperar el eje correcto con `np.newaxis` lo arregla.

### Error 4: asumir que `.T` afecta a un vector 1D

```python
v = np.array([1, 2, 3])   # (3,)
v.T.shape                 # (3,)  → transponer un 1D no hace nada
```

Transponer permuta ejes; con un solo eje no hay nada que permutar. Para volverlo columna hay que **añadir** un eje, no transponer.

## Shape y memoria

Cambiar el shape con `reshape` normalmente **no mueve datos**: solo reescribe la tupla shape y los `strides`, devolviendo una vista sobre el mismo buffer (ver [[concepto_views_vs_copias]]). Por eso es una operación barata. La excepción es cuando el array no es contiguo y la nueva forma obliga a reordenar memoria, en cuyo caso NumPy copia.

```python
arr = np.arange(12)
vista = arr.reshape(3, 4)
vista[0, 0] = 99
arr[0]   # 99  → comparten el buffer
```

## Relación con otros conceptos

- [[concepto_ndarray]]
- [[concepto_broadcasting]]
- [[concepto_views_vs_copias]]
- [[concepto_axis_parametro]]
- [[np.reshape]]
- [[np.newaxis]]
