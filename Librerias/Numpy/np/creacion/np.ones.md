---
title: np.ones — crea un array de la shape dada con todos los elementos a uno
aliases:
  - ones
  - np.ones
  - unos
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

# np.ones — crea un array de la shape dada con todos los elementos a uno

`np.ones` fabrica un [[concepto_ndarray|ndarray]] nuevo con la **forma** que le pidas y **todos sus elementos a `1`**. Es el gemelo de [[np.zeros]]: misma firma, mismo comportamiento, solo cambia el valor de relleno. Se usa para vectores de sesgo, columnas de unos en matrices de diseño, factores de escala neutros y, en general, cualquier inicialización al elemento neutro de la **multiplicación**. La pregunta sigue siendo **"¿qué [[concepto_shape|shape]] y qué [[concepto_dtype|dtype]] quiero a la salida?"**.

## La idea

`np.ones` materializa el tensor descrito por `shape` lleno de unos. El mapa de forma es directo: lo que pides es lo que sale.

$$ \text{shape} = (n_0, n_1, \dots, n_{k-1}) \;\xrightarrow{\ \text{ones}\ }\; \text{array de } \textstyle\prod_i n_i \text{ unos con esa forma} $$

`ndim` de salida es la longitud de la tupla `shape` y `size` es el producto de sus componentes. No hay transformación: la forma de salida **es** el argumento `shape`.

## Firma

```python
np.ones(
    shape,             # int | tuple[int]: la forma del array de salida
    dtype=None,        # dtype: tipo de los unos (None ⇒ float64)
    order='C',         # {'C', 'F'}: disposición en memoria
    *,
    like=None,         # array_like: referencia para crear con otra librería compatible
) -> ndarray
```

## Los parámetros en detalle

### `shape` — la forma del array de salida
El único obligatorio. **Entero** → vector 1D; **tupla** → un eje por componente. Es el [[concepto_shape|shape]] exacto del resultado.

```python
np.ones(4)        # (4,)     vector de 4 unos
np.ones((3, 3))   # (3, 3)   matriz 3×3 de unos
np.ones((2, 3, 4))  # (2, 3, 4)  tensor de rango 3
```

### `dtype` — tipo de los unos
`None` (defecto) equivale a `float64`, así que `np.ones(3)` da `[1., 1., 1.]` (flotantes). Fíjalo si necesitas enteros u otro tipo (ver [[concepto_dtype]]).

```python
np.ones(3).dtype             # float64   ← el 1 es 1.0
np.ones(3, dtype=np.int32)   # [1, 1, 1]
np.ones(2, dtype=bool)       # [True, True]
```

### `order` — disposición en memoria
`'C'` (filas contiguas, por defecto) o `'F'` (columnas contiguas). Solo afecta al rendimiento en 2D+ según el patrón de recorrido. No cambia forma ni valores.

### `like` — prototipo de otra librería
Solo-palabra-clave (`*`). Crea un array del **mismo tipo de objeto** que `like` (CuPy, Dask…) si este implementa el protocolo de array de NumPy. Poco frecuente.

## El caso N-D

La forma de salida es la tupla `shape` tal cual. Lo interesante es leer el papel de cada eje.

| `shape` | salida | `ndim` | lectura típica |
|---------|--------|--------|----------------|
| `4` | `(4,)` | 1 | vector de 4 |
| `(3, 3)` | `(3, 3)` | 2 | matriz 3×3 |
| `(2, 3, 4)` | `(2, 3, 4)` | 3 | 2 matrices 3×4 |
| `(8, 16, 3, 64, 64)` | igual | 5 | lote de vídeo |

```python
# 4D real: un tensor de pesos (filtros, canales_entrada, alto, ancho) en CNN
w = np.ones((2, 3, 4, 5))   # 4D: (filtros, canal, alto, ancho)
w.shape   # (2, 3, 4, 5)  → 2 filtros, cada uno 3 canales de 4×5
w.ndim    # 4
w.size    # 120

# 5D real: máscara de "todo activo" sobre un lote de vídeo
v = np.ones((8, 16, 3, 64, 64))  # 5D: (lote, frames, canal, alto, ancho) de vídeo
v.shape   # (8, 16, 3, 64, 64)  → 8 clips, 16 frames, RGB, 64×64
v.ndim    # 5
v.sum()   # 8*16*3*64*64 = 1_572_864  → todos valen 1, así que la suma cuenta los elementos
```

El `(2, 3, 4, 5)` se lee igual que cualquier tensor 4D: el primer eje cuenta los **filtros**, el segundo los **canales** de cada filtro, y los dos últimos su rejilla **alto × ancho**. Inicializar a unos un tensor así es habitual como punto de partida neutro para una multiplicación o como máscara "todo activo".

## Casos de uso

### Vector de sesgo / bias
```python
bias = np.ones(10)            # término independiente en una capa lineal
```

### Factor de escala neutro
```python
escala = np.ones((3, 3))      # neutro de la multiplicación elemento a elemento
ajustado = datos * escala     # no cambia nada hasta que modifiques `escala`
```

### Columna de unos para una matriz de diseño (mínimos cuadrados)
```python
x = np.array([1.0, 2.0, 3.0])
A = np.column_stack([np.ones_like(x), x])   # [[1, x0], [1, x1], [1, x2]]
```

### Construir un valor constante (con matiz)
```python
cincos = np.ones(5) * 5       # [5., 5., 5., 5., 5.]
# Más directo y claro: np.full(5, 5)
```

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| Aparecen floats donde esperabas ints | el `dtype` por defecto es `float64` | `np.ones(n, dtype=int)` |
| `np.ones(2, 3)` da `TypeError` | el `3` se interpreta como `dtype` | pasar una **tupla**: `np.ones((2, 3))` |
| `np.ones(n) * k` poco claro | rodeo para un valor constante | usar [[np.full]]`(n, k)` |
| Memoria mayor de la prevista | `float64` ocupa 8 bytes/elemento | declarar un `dtype` más estrecho |

## Notas relacionadas

- [[concepto_shape]] — la forma de salida es el argumento `shape`
- [[concepto_dtype]] — el defecto es `float64`
- [[np.zeros]] · [[np.full]] · [[np.empty]] — las otras creaciones por forma
- [[np.ones_like]] — misma shape/dtype que otro array de referencia
- [[np.array]] — crear desde datos existentes
