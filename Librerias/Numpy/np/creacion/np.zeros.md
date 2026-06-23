---
title: np.zeros — crea un array de la shape dada con todos los elementos a cero
aliases:
  - zeros
  - np.zeros
  - ceros
tags:
  - numpy
  - api/funcion
  - creacion

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
  - concepto_dtype

draft: false
---

# np.zeros — crea un array de la shape dada con todos los elementos a cero

`np.zeros` fabrica un [[concepto_ndarray|ndarray]] nuevo con la **forma** que le pidas y **todos sus elementos a `0`**. Es la función de creación que más se usa para **preasignar** memoria antes de un bucle o como **acumulador** que parte de cero. La pregunta clave al usarla no es "¿qué valores tiene?" (siempre 0) sino **"¿qué [[concepto_shape|shape]] y qué [[concepto_dtype|dtype]] quiero a la salida?"**.

## La idea

`np.zeros` toma una descripción de la **forma** (un entero o una tupla) y materializa el tensor correspondiente lleno de ceros. El mapa es directo: lo que pides en `shape` es exactamente lo que sale.

$$ \text{shape} = (n_0, n_1, \dots, n_{k-1}) \;\xrightarrow{\ \text{zeros}\ }\; \text{array de } \textstyle\prod_i n_i \text{ ceros con esa forma} $$

El número de ejes de salida (`ndim`) es la longitud de la tupla `shape`, y el total de elementos (`size`) es el producto de sus componentes. No hay reducción ni transformación: la forma de salida **es** el argumento `shape`.

## Firma

```python
np.zeros(
    shape,             # int | tuple[int]: la forma del array de salida
    dtype=float,       # dtype: tipo de los ceros (¡por defecto float64!)
    order='C',         # {'C', 'F'}: disposición en memoria
    *,
    like=None,         # array_like: referencia para crear con otra librería ASARRAY-compatible
) -> ndarray
```

## Los parámetros en detalle

### `shape` — la forma del array de salida
El único obligatorio. Un **entero** produce un vector 1D; una **tupla** produce un tensor con un eje por componente. Es el [[concepto_shape|shape]] exacto del resultado.

```python
np.zeros(5)          # (5,)       vector de 5 ceros
np.zeros((3, 4))     # (3, 4)     matriz 3×4
np.zeros((2, 3, 4))  # (2, 3, 4)  tensor de rango 3
```

### `dtype` — tipo de los ceros (la trampa del defecto `float`)
A diferencia de lo que uno esperaría, **el defecto es `float64`, no entero**. Si trabajas con índices o contadores, fíjalo explícitamente o arrastrarás flotantes (ver [[concepto_dtype]]).

```python
np.zeros(3).dtype             # float64   ← el 0 es 0.0
np.zeros(3, dtype=np.int8)    # [0, 0, 0] en int8
np.zeros(2, dtype=complex)    # [0.+0.j, 0.+0.j]
np.zeros(2, dtype=bool)       # [False, False]
```

### `order` — disposición en memoria
`'C'` (filas contiguas, estilo C, por defecto) o `'F'` (columnas contiguas, estilo Fortran). Solo importa por rendimiento en 2D o más, según el patrón con el que vayas a recorrer el buffer. No cambia ni la forma ni los valores.

### `like` — prototipo de otra librería
Parámetro de solo-palabra-clave (`*`). Permite que `np.zeros` cree un array del **mismo tipo de objeto** que `like` (por ejemplo, un array de CuPy o Dask que implemente el protocolo `__array_function__`), en vez de un `ndarray` de NumPy. Raro en uso cotidiano.

## El caso N-D

La forma de salida es literalmente la tupla `shape`: no hay nada que "interpretar" como en una reducción. Lo útil es leer cada eje con su significado de dominio.

| `shape` | salida | `ndim` | lectura típica |
|---------|--------|--------|----------------|
| `5` | `(5,)` | 1 | vector de 5 |
| `(3, 4)` | `(3, 4)` | 2 | matriz 3×4 |
| `(2, 3, 4)` | `(2, 3, 4)` | 3 | 2 matrices 3×4 |
| `(2, 3, 4, 5)` | `(2, 3, 4, 5)` | 4 | lote de tensores |

```python
# 4D real: un lote de mapas de activación (lote, canal, alto, ancho)
t = np.zeros((2, 3, 4, 5))   # 4D: (lote, canal, alto, ancho)
t.shape   # (2, 3, 4, 5)  → 2 ejemplos, 3 canales, 4×5 píxeles cada uno
t.ndim    # 4
t.size    # 120  = 2*3*4*5

# 5D real: un lote de clips de vídeo
v = np.zeros((8, 16, 3, 64, 64))   # 5D: (lote, frames, canal, alto, ancho)
v.shape   # (8, 16, 3, 64, 64)  → 8 clips, 16 frames, RGB, 64×64
v.ndim    # 5

# Inicializar un acumulador con la forma del eje espacial de v:
acum = np.zeros(v.shape[2:])   # (3, 64, 64)  → un frame en blanco
```

Cada eje del `(2, 3, 4, 5)` tiene un papel: el primero es el **lote** (cuántos ejemplos), el segundo el **canal** (cuántos mapas por ejemplo), y los dos últimos la rejilla espacial **alto × ancho**. Inicializar a ceros un tensor así es el paso 0 de casi cualquier pipeline de imágenes o vídeo.

## Casos de uso

### Preasignar antes de un bucle de llenado
```python
n = 1000
resultado = np.zeros(n)        # reservar memoria una sola vez
for i in range(n):
    resultado[i] = i ** 2      # llenar in-place, sin re-asignar
```

### Acumulador que parte de cero
```python
acumulado = np.zeros((3, 3))
for matriz in lista_de_matrices:
    acumulado += matriz        # el neutro de la suma es 0
```

### Lienzo o máscara en blanco
```python
lienzo = np.zeros((100, 100), dtype=np.uint8)   # imagen negra 100×100
mascara = np.zeros((480, 640), dtype=bool)      # nada seleccionado aún
```

### Buffer N-D para un lote
```python
batch = np.zeros((32, 3, 224, 224), dtype=np.float32)  # 32 imágenes RGB 224×224
batch[0] = primera_imagen      # se rellena ejemplo a ejemplo
```

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| Aparecen floats donde esperabas ints | el `dtype` por defecto es `float64`, no `int` | `np.zeros(n, dtype=int)` |
| `np.zeros(2, 3)` da `TypeError` | el `3` se interpreta como `dtype`, no como segundo eje | pasar una **tupla**: `np.zeros((2, 3))` |
| Memoria mayor de la prevista | `float64` ocupa 8 bytes/elemento | declarar un `dtype` más estrecho |
| Inicializar a 0 cuando vas a sobrescribir todo | gasto innecesario en arrays enormes | usar [[np.empty]] |

## Notas relacionadas

- [[concepto_shape]] — la forma de salida es el argumento `shape`
- [[concepto_dtype]] — ojo al defecto `float64`
- [[np.ones]] · [[np.full]] · [[np.empty]] — las otras creaciones por forma
- [[np.zeros_like]] — misma shape/dtype que otro array de referencia
- [[np.array]] — crear desde datos existentes
