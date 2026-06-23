---
title: np.unique — valores únicos, ordenados y sin repetir
aliases:
  - unique
  - np.unique
  - únicos
tags:
  - numpy
  - api/funcion
  - conjuntos

# --- Clasificación ---
lib: numpy
mod: np
tipo: funcion

# --- Comportamiento ---
retorna: ndarray | tuple
inplace: false

# --- Dependencias ---
requiere:
  - concepto_indexing

draft: false
---

# np.unique — valores únicos, ordenados y sin repetir

`np.unique` recorre todos los elementos de un array, **aplana** la entrada a 1D, descarta los
duplicados y devuelve los valores que sobreviven **ordenados de menor a mayor**. Es la base de las
operaciones de conjunto: el resultado es exactamente el "conjunto" matemático de los valores. Con
sus flags `return_*` puede además decirte **dónde** estaba cada único, **cómo reconstruir** el array
original o **cuántas veces** aparecía cada valor; y con `axis` deja de mirar elementos sueltos para
buscar **filas o sub-arrays únicos**.

## La idea

La operación de conjunto es la **deduplicación con orden**: de la multitud de valores de entrada se
queda con cada valor distinto una sola vez y los coloca ordenados.

$$ \{a_0, a_1, \dots, a_{N-1}\}\ \xrightarrow{\ \text{unique}\ }\ (u_0 < u_1 < \dots < u_{k-1}) $$

La salida base es **siempre 1D** (la entrada se aplana antes): un vector ordenado de longitud $k$ =
número de valores distintos. La única excepción es cuando se pasa `axis`: ahí los "elementos" pasan
a ser **sub-arrays** (p. ej. filas) y la salida conserva una dimensión extra — es el caso N-D real
de esta función.

## Firma

```python
np.unique(
    ar,                     # array_like: entrada (se aplana salvo que se indique axis)
    return_index=False,     # bool: añade índices de la 1ª aparición
    return_inverse=False,   # bool: añade índices para reconstruir ar
    return_counts=False,    # bool: añade el conteo de cada único
    axis=None,              # None | int: None aplana; int busca sub-arrays únicos por ese eje
) -> ndarray | tuple
```

## Los parámetros en detalle

### `ar` — el array de entrada
`array_like`. Se **aplana a 1D** antes de operar (salvo que des `axis`). Los valores deben ser
comparables y ordenables (números, strings, fechas...).

### `return_index` — dónde estaba cada único
`bool`. Si `True`, añade al retorno un array `idx` tal que `ar_aplanado[idx]` reproduce los únicos.
Es decir, la posición de la **primera aparición** de cada valor en la entrada original.

```python
u, idx = np.unique([3, 1, 2, 1, 3], return_index=True)
# u   = [1, 2, 3]
# idx = [1, 2, 0]   → el 1 apareció primero en la posición 1, el 3 en la 0
```

### `return_inverse` — cómo reconstruir el original
`bool`. Añade un array `inv` con, **por cada elemento original**, el índice de su único
correspondiente. Permite reconstruir la entrada con `u[inv]`. Es la base del *label encoding*.

```python
u, inv = np.unique(['a', 'b', 'a', 'c'], return_inverse=True)
# u   = ['a', 'b', 'c']
# inv = [0, 1, 0, 2]
u[inv]   # ['a', 'b', 'a', 'c']  → reconstruye el original
```

### `return_counts` — frecuencia de cada único
`bool`. Añade un array `counts` con el número de apariciones de cada valor único. Es la forma
general de hacer una **tabla de frecuencias** (funciona con strings, floats y fechas, a diferencia
de [[np.bincount]], que solo cuenta enteros no negativos).

```python
u, counts = np.unique([3, 1, 2, 1, 3, 3], return_counts=True)
# u      = [1, 2, 3]
# counts = [2, 1, 3]   → 1 aparece 2 veces, 2 una, 3 tres
```

### `axis` — sub-arrays únicos en vez de elementos
`None | int`. Con `None` (defecto) se aplana y se buscan **valores** únicos. Con un `int`, los
elementos a comparar pasan a ser los **sub-arrays a lo largo de ese eje**: `axis=0` busca **filas**
únicas; `axis=1`, columnas. La salida conserva la dimensionalidad de la entrada (ver el caso N-D).

## El caso N-D

Sin `axis`, no hay caso N-D: cualquier entrada se aplana y la salida es un vector 1D. El N-D real
aparece con `axis`, donde la unidad de comparación deja de ser el escalar y pasa a ser un
**sub-array entero**. Con `axis=0` sobre una matriz, dos filas son "el mismo elemento" si coinciden
en todas sus columnas:

$$ (m, n)\ \xrightarrow{\ \text{unique, axis}=0\ }\ (k, n) \qquad k = \text{nº de filas distintas} $$

```python
M = np.array([[1, 2],
              [1, 2],
              [3, 4]])
np.unique(M, axis=0)
# [[1, 2],
#  [3, 4]]      → las dos primeras filas eran iguales; queda una. Shape (2, 2)

np.unique(M)    # sin axis: aplana → [1, 2, 3, 4], shape (4,)
```

Las filas resultantes también salen **ordenadas** (lexicográficamente). Es la herramienta para
**deduplicar registros** (cada fila = una observación).

## Casos de uso

### Tabla de frecuencias
```python
etiquetas = np.array(['gato', 'perro', 'gato', 'pez', 'gato'])
valores, conteos = np.unique(etiquetas, return_counts=True)
# valores = ['gato', 'perro', 'pez'], conteos = [3, 1, 1]
```

### Codificar categorías a enteros (label encoding)
```python
textos = np.array(['rojo', 'verde', 'rojo', 'azul'])
categorias, codigos = np.unique(textos, return_inverse=True)
# categorias = ['azul', 'rojo', 'verde'], codigos = [1, 2, 1, 0]
```

### Deduplicar filas de una matriz (registros únicos)
```python
registros = np.array([[10, 0], [10, 0], [11, 1]])
np.unique(registros, axis=0)   # [[10, 0], [11, 1]]
```

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| Esperar el orden original | `unique` siempre **ordena** | usar `return_index` y reordenar por él |
| Esperar un array y recibir una tupla | algún `return_*=True` desambigua el retorno | desempaquetar: `u, c = np.unique(..., return_counts=True)` |
| `axis=0` no deduplica filas como espero | la entrada no era 2D o filas con `NaN` (nunca iguales) | revisar shape; los `NaN` no se comparan iguales |
| Querer contar enteros y mezclar con [[np.bincount]] | `bincount` solo enteros ≥ 0 | `return_counts=True` sirve para cualquier dtype |

## Notas relacionadas

- [[concepto_indexing]] — `return_inverse`/`return_index` son índices para reindexar
- [[np.bincount]] — conteo rápido pero solo para enteros no negativos
- [[Librerias/Numpy/np/conjuntos/index|operaciones de conjunto]] — la nota madre
- [[np.intersect1d]] · [[np.union1d]] · [[np.isin]]
