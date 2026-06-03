---
title: csc_matrix — matriz dispersa comprimida por columnas (CSC)
aliases:
  - csc_matrix
  - scipy.sparse.csc_matrix
  - Compressed Sparse Column
tags:
  - scipy
  - api/clase
  - matrices-dispersas
lib: scipy
tipo: clase
mod: scipy.sparse
requiere:
  - concepto_ndarray
  - scipy.sparse.operaciones
draft: false
---

# csc_matrix — matriz dispersa comprimida por columnas (CSC)

Matriz dispersa en formato **Compressed Sparse Column**: el analogo exacto de CSR pero comprimido por **columnas**. Almacena los no nulos en `data`, `indices` (indices de **fila**) e `indptr` (punteros por **columna**). Comparte API con la clase comprimida por filas; cambia solo el eje que resulta barato.

El cuadro completo de formatos esta en [[scipy.sparse.operaciones]].

## Como almacena (los tres arrays)

| Array | Longitud | Contenido |
|-------|----------|-----------|
| `data` | `nnz` | Valores no nulos, en orden por columnas |
| `indices` | `nnz` | Indice de **fila** de cada valor de `data` |
| `indptr` | `n_columnas + 1` | Punteros: `data[indptr[j]:indptr[j+1]]` son los no nulos de la columna `j` |

Para la columna `j`, sus filas no nulas son `indices[indptr[j]:indptr[j+1]]`. Por eso operar **por columnas** es inmediato.

## Construccion

```python
import numpy as np
from scipy.sparse import csc_matrix

# Desde array denso
A = csc_matrix(np.array([[0, 0, 3], [4, 0, 0]]))

# Desde (data, (row, col)) — duplicados se suman al comprimir
A = csc_matrix(([3, 4], ([0, 1], [2, 0])), shape=(2, 3))

# Conversion desde CSR/COO (lo habitual)
B = A.tocsr().tocsc()
```

## Atributos clave

Identicos en nombre a la clase por filas, pero con semantica de columna:

| Atributo | Significado |
|----------|-------------|
| `data` | Valores no nulos (orden por columnas) |
| `indices` | Indices de **fila** de cada valor |
| `indptr` | Punteros de inicio de cada columna |
| `nnz` | Numero de no nulos almacenados |
| `shape` | Dimensiones `(filas, columnas)` |
| `T` | Transpuesta (una CSC transpuesta es, conceptualmente, una CSR) |

## Mismo API que la matriz por filas

```python
A.toarray()        # -> ndarray denso
A @ v              # producto matriz-vector
A[:, 0]            # slicing por COLUMNA: barato en CSC
A.tocsr()          # conversion a CSR
A.sum(axis=0)      # reduccion por columnas
```

## Cuando CSC vs CSR

| Necesitas... | Usa |
|--------------|-----|
| Producto matriz-vector, aritmetica, slicing por filas | CSR |
| Slicing por columnas `A[:, j]` | CSC |
| Factorizaciones/solvers orientados a columna | CSC |

La regla practica: **elige el formato segun el eje dominante de tus operaciones**. Las dos son rapidas en producto y aritmetica; difieren en que eje de slicing es barato y en que algoritmos las prefieren.

## Caso de uso central: solvers por columnas

`scipy.sparse.linalg.splu` (factorizacion LU dispersa) trabaja internamente en CSC; si le pasas una CSR, convierte primero. Pasarle directamente una CSC evita esa conversion:

```python
from scipy.sparse.linalg import splu

lu = splu(A.tocsc())   # factorizacion LU; A debe ser cuadrada y CSC
x = lu.solve(b)        # resuelve A x = b reutilizando la factorizacion
```

> `splu` y los solvers directos de columnas son el motivo principal para elegir CSC. Para `spsolve` puntual, CSR o CSC sirven (internamente usa CSC).

## Errores comunes

| Error | Causa | Solucion |
|-------|-------|----------|
| Slicing por fila lento | CSC no esta optimizada por filas | Convierte con `.tocsr()` |
| `splu` reconvierte y avisa | Pasaste CSR a un solver de columnas | Pasa `A.tocsc()` |
| `SparseEfficiencyWarning` al asignar | Modificas estructura de una CSC | Construye en COO/LIL y `.tocsc()` al final |

## Notas relacionadas

- [[scipy.sparse.operaciones]]
- [[csr_matrix]]
- [[coo_matrix]]
