---
title: np.array — construye un ndarray a partir de datos existentes
aliases:
  - array
  - np.array
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
  - concepto_ndarray
  - concepto_dtype

draft: false
---

# np.array — construye un ndarray a partir de datos existentes

`np.array` es **el constructor principal**: toma datos de Python (listas, tuplas, secuencias anidadas, escalares u otro array) y devuelve un nuevo [[concepto_ndarray|ndarray]]. Su trabajo es doble: **inferir la forma** a partir del anidamiento de las listas e **inferir el dtype** promoviendo al tipo común de los elementos. La idea clave que la distingue de su hermana [[np.asarray]] es que **por defecto siempre copia** los datos (`copy=True`): el array resultante es independiente de la entrada.

## La idea

Construir un array es **leer la estructura anidada de una secuencia y aplanarla a un buffer contiguo**, anotando en el `shape` cuántos elementos hay por nivel de anidamiento. Cada nivel de corchetes añade un eje:

$$ \underbrace{[\,\cdots\,]}_{\text{nivel 0} \to \text{eje } 0}\ \supset\ \underbrace{[\,\cdots\,]}_{\text{nivel 1} \to \text{eje } 1}\ \supset\ \cdots $$

Una lista plana de $n$ números da un `(n,)`; una lista de $m$ listas de $n$ números da un `(m, n)`; y así sucesivamente. El requisito es que las sublistas de cada nivel sean **regulares** (todas de la misma longitud); si no, NumPy no puede formar un tensor rectangular y cae a un `object` array (o lanza error). El `dtype` se decide por la regla de promoción de [[concepto_dtype]]: gana el tipo más amplio capaz de representar todos los elementos.

## Firma

```python
np.array(
    object,            # array_like: datos de entrada (lista, tupla, escalar, ndarray...)
    dtype=None,        # dtype | None: tipo de los elementos; None = inferir
    *,
    copy=True,         # bool: True (defecto) = SIEMPRE copia; False = copia solo si hace falta
    order='K',         # {'K', 'A', 'C', 'F'}: layout en memoria del resultado
    subok=False,       # bool: conservar subclases (p. ej. np.matrix) o degradar a ndarray
    ndmin=0,           # int: nº mínimo de ejes (rellena con ejes de tamaño 1 por la izquierda)
    like=None,         # array_like: array de referencia para crear con otra librería (array API)
) -> ndarray
```

## Los parámetros en detalle

### `object` — los datos de entrada

`array_like`: lista, tupla, secuencia anidada, escalar u otro `ndarray`. El **anidamiento define los ejes** y las longitudes deben ser regulares por nivel.

```python
np.array([1, 2, 3])              # (3,)    una lista plana → 1 eje
np.array([[1, 2, 3], [4, 5, 6]]) # (2, 3)  lista de listas → 2 ejes
np.array(5)                      # ()      escalar → array 0-D
np.array([[1, 2], [3, 4, 5]])    # listas IRREGULARES → object array o error
```

### `dtype` — tipo de los elementos

Si se omite (`None`), NumPy lo **infiere** promoviendo al tipo común (ver [[concepto_dtype]]). Especificarlo fuerza el tipo (y puede truncar o castear).

```python
np.array([1, 2, 3], dtype=np.float64)  # [1., 2., 3.]
np.array([1.9, 2.9], dtype=np.int32)   # [1, 2]   → trunca hacia 0, NO redondea
```

### `copy` — copiar o reutilizar (la diferencia clave)

| Valor | Comportamiento |
|-------|----------------|
| `True` (**defecto**) | **siempre** crea un buffer nuevo: el resultado es independiente de la entrada |
| `False` | copia **solo si es imprescindible**; si la entrada ya es un ndarray compatible, lo reutiliza (vista) |

```python
original = np.array([1, 2, 3])
c = np.array(original)               # copia → buffer propio, independiente
b = np.array(original, copy=False)   # reutiliza si puede (comparte memoria)
np.shares_memory(original, c)        # False
np.shares_memory(original, b)        # True
```

Como `copy=True` es el defecto, `np.array` es la opción **segura por defecto**. Si lo que quieres es justo lo contrario (no copiar si ya es array), usa [[np.asarray]]. La distinción entre compartir y duplicar memoria se desarrolla en [[concepto_views_vs_copias]].

> [!warning] `copy=False` ya no significa "nunca copies"
> En NumPy ≥ 2.0, `copy=False` lanza `ValueError` si la copia es **inevitable** (p. ej. la entrada es una lista, que obliga a materializar un buffer). Para el sentido permisivo de "copia solo si hace falta", usa [[np.asarray]].

### `ndmin` — número mínimo de ejes

Garantiza al menos `ndmin` dimensiones, insertando ejes de tamaño 1 **por la izquierda**.

```python
np.array([1, 2, 3], ndmin=2).shape   # (1, 3)  → de 1-D a 2-D
np.array(5, ndmin=1).shape           # (1,)    → de escalar a vector
```

### `order` — layout en memoria

Controla cómo se tienden los datos en el buffer: `'C'` (filas contiguas, *row-major*), `'F'` (columnas contiguas, *column-major*), `'A'` (`'F'` si la entrada es F-contigua, si no `'C'`) y `'K'` (defecto: conserva el orden de la entrada lo más posible). Afecta al rendimiento del recorrido, no a los valores. Ver [[concepto_ndarray]] para los strides.

### `subok` — conservar subclases

Si `True`, conserva el tipo de subclase de la entrada (p. ej. `np.matrix`, `np.ma.MaskedArray`); si `False` (defecto), **degrada** el resultado a un `ndarray` base.

### `like` — referencia de array API

`array_like` de referencia para crear el resultado con la **misma librería** que el objeto pasado (protocolo array API, p. ej. crear un array de CuPy/Dask). Rara vez se usa en código NumPy puro.

## El caso N-D

El `shape` sale **directo del anidamiento**: la profundidad de corchetes es el `ndim` y la longitud en cada nivel es el tamaño de ese eje. Construyamos un array **4-D** desde listas anidadas (4 niveles de corchetes → shape `(2, 2, 2, 3)`) y leamos su forma:

```python
datos_4d = [
    [   # eje 0, índice 0
        [[ 0,  1,  2], [ 3,  4,  5]],   # eje 1, índice 0  → (2, 3)
        [[ 6,  7,  8], [ 9, 10, 11]],   # eje 1, índice 1  → (2, 3)
    ],
    [   # eje 0, índice 1
        [[12, 13, 14], [15, 16, 17]],
        [[18, 19, 20], [21, 22, 23]],
    ],
]

T = np.array(datos_4d)
T.shape   # (2, 2, 2, 3)   → 4 niveles de corchetes = 4 ejes
T.ndim    # 4
T.size    # 24             → 2·2·2·3
T.dtype   # int64          → inferido de los enteros
```

La lectura del shape `(2, 2, 2, 3)` por nivel:

$$ \underbrace{2}_{\text{eje }0}\ \times\ \underbrace{2}_{\text{eje }1}\ \times\ \underbrace{2}_{\text{eje }2}\ \times\ \underbrace{3}_{\text{eje }3}\ =\ 24\ \text{elementos} $$

Cada eje corresponde a un nivel de anidamiento: 2 bloques, cada uno con 2 matrices, cada matriz de 2 filas y 3 columnas. Si cualquier sublista de un nivel tuviera longitud distinta, NumPy no podría formar este tensor rectangular y caería a `object`.

## Casos de uso

### Construir desde datos de Python

```python
temperaturas = [20.5, 21.0, 19.8, 22.3]
arr = np.array(temperaturas)   # ahora soporta operaciones vectorizadas
arr.mean()                     # 20.9
```

### Fijar el dtype para ahorrar memoria

```python
# Píxeles 0..255 → uint8 ocupa 8x menos que float64
img = np.array([[0, 128], [255, 64]], dtype=np.uint8)
```

### Matriz a partir de filas

```python
filas = [[1, 0, 0],
         [0, 1, 0],
         [0, 0, 1]]
I = np.array(filas)   # matriz identidad 3x3, shape (3, 3)
```

### Promoción de dtype al mezclar tipos

```python
np.array([1, 2, 3]).dtype        # int64
np.array([1, 2.0, 3]).dtype      # float64  → promoción (ver concepto_dtype)
np.array([1, 2, "x"]).dtype      # <U21     → todo a texto
```

### La trampa de las listas irregulares

```python
np.array([[1, 2, 3], [4, 5]])    # ValueError en NumPy ≥ 1.24 (o object array)
np.array([[1, 2, 3], [4, 5]], dtype=object)  # array de 2 listas Python, 1-D
```

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| `ValueError: inhomogeneous shape` o dtype `object` | sublistas de distinta longitud | regularizar las listas, o `dtype=object` a propósito |
| `int` donde se esperaba `float` | datos enteros sin punto decimal | pasar `dtype=float` |
| `float` truncado a `int` sin redondeo | `dtype=int` trunca hacia 0 | `np.round(...).astype(int)` |
| Copia innecesaria de un array grande | `copy=True` por defecto | usar [[np.asarray]] si no hace falta copiar |
| `ValueError` con `copy=False` | la copia era inevitable (NumPy ≥ 2.0) | usar [[np.asarray]] para el sentido permisivo |
| Memoria excesiva | `float64`/`int64` por defecto | declarar un `dtype` más estrecho |

## Notas relacionadas

- [[concepto_ndarray]] — qué es exactamente lo que se construye (buffer + shape + dtype + strides)
- [[concepto_dtype]] — la regla de promoción que decide el tipo inferido
- [[np.asarray]] — el mismo constructor pero sin copiar si ya es un array
- [[concepto_views_vs_copias]] — qué significa que `copy=True` devuelva memoria independiente
- [[np.zeros]] · [[np.ones]] · [[np.full]] · [[np.arange]] · [[np.linspace]]
