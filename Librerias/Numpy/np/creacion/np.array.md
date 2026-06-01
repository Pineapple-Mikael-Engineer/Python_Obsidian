---
title: np.array — Crear un array desde datos existentes
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

# np.array — Crear un array desde datos existentes

## Firma de la función

```python
np.array(
    object,
    dtype=None,
    *,
    copy=True,
    order='K',
    subok=False,
    ndmin=0,
    like=None
) -> ndarray
```

## Valor de retorno

Devuelve un nuevo [[concepto_ndarray|ndarray]] cuyo `shape` y `dtype` se infieren del objeto de entrada, salvo que se especifiquen.

| Entrada | Shape resultante | dtype inferido |
|---------|------------------|----------------|
| `[1, 2, 3]` | `(3,)` | `int64` |
| `[[1, 2], [3, 4]]` | `(2, 2)` | `int64` |
| `[1.0, 2, 3]` | `(3,)` | `float64` (promoción) |
| `[1, 2, "x"]` | `(3,)` | `<U21` (texto) |
| `5` | `()` | `int64` (escalar 0D) |

```python
import numpy as np
np.array([1, 2, 3])          # array([1, 2, 3])
np.array([[1, 2], [3, 4]])   # array de shape (2, 2)
```

## Formas básicas de llamada

| Forma | Ejemplo | Descripción |
|-------|---------|-------------|
| Desde lista | `np.array([1, 2, 3])` | caso más común |
| Desde lista anidada | `np.array([[1, 2], [3, 4]])` | dimensión por nivel de anidamiento |
| Con dtype explícito | `np.array([1, 2], dtype=np.float32)` | fuerza el tipo |
| Forzando dimensiones | `np.array([1, 2], ndmin=2)` | shape `(1, 2)` |

## Parámetros en detalle

### `object` — datos de entrada

Cualquier secuencia (lista, tupla), array existente, o escalar. El anidamiento define las dimensiones: las listas deben ser **regulares** (todas las sublistas de igual longitud).

```python
np.array([[1, 2, 3], [4, 5, 6]])   # OK → (2, 3)
np.array([[1, 2], [3, 4, 5]])      # listas irregulares → dtype object o error
```

### `dtype` — tipo de los elementos

Si se omite, NumPy lo infiere promoviendo al tipo más general (ver [[concepto_dtype]]). Especificarlo evita sorpresas y ahorra memoria.

```python
np.array([1, 2, 3], dtype=np.float64)   # [1., 2., 3.]
np.array([1.9, 2.9], dtype=np.int32)    # [1, 2]  → trunca
```

### `copy` — copiar o referenciar

| Valor | Comportamiento |
|-------|----------------|
| `True` (por defecto) | siempre crea una copia nueva de los datos |
| `False` | evita copiar si es posible (devuelve vista si el objeto ya es un array compatible) |

```python
original = np.array([1, 2, 3])
b = np.array(original, copy=False)   # comparte memoria si puede
c = np.array(original)               # copia independiente
```

Para no copiar, suele preferirse [[np.asarray]].

### `ndmin` — dimensiones mínimas

Garantiza un número mínimo de ejes, insertando dimensiones de tamaño 1 al principio.

```python
np.array([1, 2, 3], ndmin=2).shape   # (1, 3)
np.array(5, ndmin=1).shape           # (1,)
```

### `order` — orden en memoria

`'C'` (filas contiguas), `'F'` (columnas contiguas), `'K'` (conserva el del origen), `'A'`. Relevante para rendimiento y compatibilidad. Ver [[concepto_contiguidad_memoria]].

## Casos de uso

### Construir desde datos de Python

```python
temperaturas = [20.5, 21.0, 19.8, 22.3]
arr = np.array(temperaturas)   # ahora soporta operaciones vectorizadas
arr.mean()                     # 20.9
```

### Definir explícitamente el dtype para imágenes

```python
# Pixeles 0..255 → uint8 ahorra 8x memoria frente a float64
img = np.array([[0, 128], [255, 64]], dtype=np.uint8)
```

### Matriz a partir de filas

```python
filas = [[1, 0, 0],
         [0, 1, 0],
         [0, 0, 1]]
I = np.array(filas)   # matriz identidad 3x3
```

## Buenas prácticas

1. Para arrays de tamaño conocido lleno de un valor, prefiere [[np.zeros]] / [[np.ones]] / [[np.full]] en vez de construir listas.
2. Especifica `dtype` cuando la memoria o la precisión importen.
3. Para rangos numéricos usa [[np.arange]] o [[np.linspace]], no listas manuales.
4. Si solo necesitas una vista sin copiar, usa [[np.asarray]] (`copy=False` implícito).
5. Verifica `arr.shape` tras crear estructuras anidadas complejas.

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| dtype inesperado `object` | sublistas de distinta longitud | regularizar las listas o usar `dtype=object` a propósito |
| `int` donde se esperaba `float` | datos enteros sin punto decimal | pasar `dtype=float` |
| Modificar el original sin querer | `copy=False` devolvió una vista | usar `copy=True` (por defecto) |
| Memoria excesiva | `float64` por defecto | declarar `dtype` más pequeño |

## Limitaciones

- Construir desde listas grandes de Python es lento; si los datos vienen de un archivo usa [[np.loadtxt]] o [[np.load]].
- No genera secuencias: para ello están [[np.arange]] y [[np.linspace]].
- Para rellenar con un valor constante, [[np.full]] es más directo y eficiente.

## Notas relacionadas

- [[concepto_ndarray]]
- [[concepto_dtype]]
- [[np.asarray]]
- [[np.zeros]]
- [[np.ones]]
- [[np.arange]]
- [[np.linspace]]
- [[np.full]]
