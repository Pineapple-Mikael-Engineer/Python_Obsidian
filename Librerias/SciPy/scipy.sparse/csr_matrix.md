---
title: csr_matrix — matriz dispersa comprimida por filas (CSR)
aliases:
  - csr_matrix
  - scipy.sparse.csr_matrix
  - Compressed Sparse Row
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

# csr_matrix — matriz dispersa comprimida por filas (CSR)

Matriz dispersa en formato **Compressed Sparse Row**: almacena solo los elementos NO nulos en tres arrays paralelos (`data`, `indices`, `indptr`) que comprimen la informacion por **filas**. Es el **formato de calculo por defecto** de SciPy: rapido en producto matriz-vector, en slicing por filas y en aritmetica. Su contrapartida es que cambiar la estructura (asignar posiciones nuevas) es caro.

El panorama de formatos y cuando usar cada uno esta en [[scipy.sparse.operaciones]].

## Como almacena (los tres arrays)

| Array | Longitud | Contenido |
|-------|----------|-----------|
| `data` | `nnz` | Valores no nulos, en orden por filas |
| `indices` | `nnz` | Indice de columna de cada valor de `data` |
| `indptr` | `n_filas + 1` | Punteros: `data[indptr[i]:indptr[i+1]]` son los no nulos de la fila `i` |

Para la fila `i`, sus columnas no nulas son `indices[indptr[i]:indptr[i+1]]` y sus valores `data[indptr[i]:indptr[i+1]]`. De ahi que recorrer/operar **por filas** sea inmediato.

## Construccion

```python
import numpy as np
from scipy.sparse import csr_matrix, coo_matrix

# 1) Desde un array denso (toma solo los no nulos)
A = csr_matrix(np.array([[0, 0, 3], [4, 0, 0]]))
A.nnz                         # -> 2

# 2) Desde (data, (row, col)): tripletes COO comprimidos a CSR
data = [3, 4]
row  = [0, 1]
col  = [2, 0]
B = csr_matrix((data, (row, col)), shape=(2, 3))

# 3) Desde una COO ya construida (flujo recomendado: construir en COO, operar en CSR)
C = coo_matrix((data, (row, col)), shape=(2, 3)).tocsr()
```

> La forma `(data, (row, col))` permite **duplicados**: las entradas que caen en la misma posicion se **suman** al comprimir a CSR.

## Atributos clave

| Atributo | Significado |
|----------|-------------|
| `data` | Valores no nulos (orden por filas) |
| `indices` | Indices de columna de cada valor |
| `indptr` | Punteros de inicio de cada fila |
| `nnz` | Numero de elementos almacenados (no nulos) |
| `shape` | Dimensiones `(filas, columnas)` |
| `dtype` | Tipo de los valores |
| `T` | Transpuesta (una CSR transpuesta es, conceptualmente, una CSC) |

## Operaciones tipicas

```python
A.toarray()        # -> ndarray denso (cuidado: materializa todo)
A @ v              # producto matriz-vector: la operacion estrella de CSR
A + B              # aritmetica elemento a elemento (mismo shape)
A[0]               # slicing por FILA: barato en CSR
A.tocsc()          # conversion a CSC (para operaciones por columna)
A.sum(axis=1)      # reduccion por filas
```

## Fortalezas y debilidades

| Operacion | CSR |
|-----------|-----|
| Producto matriz-vector `A @ v` | Muy rapido (fuerte) |
| Slicing por filas `A[i]` | Rapido (fuerte) |
| Aritmetica `+`, `*`, `@` | Rapida (fuerte) |
| Slicing por columnas `A[:, j]` | Lento -> prefiere CSC |
| Asignar elementos nuevos `A[i, j] = x` | Caro: reestructura los arrays (debil) |

> Si necesitas **modificar la estructura** muchas veces, construye en COO o LIL y convierte a CSR solo al final. Asignar sobre una CSR emite un `SparseEfficiencyWarning`.

## Casos de uso

- Resolver sistemas dispersos grandes `Ax = b` con `scipy.sparse.linalg.spsolve` (CSR o CSC).
- Grafos como matrices de adyacencia: recorridos y productos por filas.
- Algebra lineal iterativa (`eigs`, `cg`) donde domina el producto matriz-vector.

## Errores comunes

| Error | Causa | Solucion |
|-------|-------|----------|
| `SparseEfficiencyWarning` al asignar | Modificas estructura de una CSR | Construye en COO/LIL y `.tocsr()` al final |
| Memoria desbordada con `.toarray()` | Materializas una matriz enorme | Opera disperso; densifica solo bloques pequeños |
| Slicing por columna lentisimo | CSR no esta optimizada por columnas | Convierte con `.tocsc()` |
| `*` no es producto matricial en `*_array` | API moderna usa `*` elemento a elemento | Usa `@` para producto matricial |

## Notas relacionadas

- [[scipy.sparse.operaciones]]
- [[csc_matrix]]
- [[coo_matrix]]
