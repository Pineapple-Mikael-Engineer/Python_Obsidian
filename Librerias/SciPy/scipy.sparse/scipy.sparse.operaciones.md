---
title: scipy.sparse — formatos y operaciones de matrices dispersas
aliases:
  - scipy.sparse operaciones
  - matrices dispersas scipy
  - formatos sparse
tags:
  - scipy
  - concepto
  - matrices-dispersas
lib: scipy
tipo: concepto
mod: scipy.sparse
requiere:
  - concepto_relacion_numpy
draft: false
---

# scipy.sparse — formatos y operaciones de matrices dispersas

## Idea central

Una **matriz dispersa** almacena solo los elementos NO nulos. Cuando la mayoria de las entradas son cero, esto supone un ahorro masivo de **memoria** y de **computo** frente a un array denso de NumPy. `scipy.sparse` ofrece varios formatos: cada uno optimiza una cosa distinta, asi que lo normal es **construir** en un formato y **operar** en otro.

Estas matrices conviven con el ecosistema de NumPy pero no son `ndarray`; la relacion capa-algoritmo se trata en [[concepto_relacion_numpy]].

## Tabla comparativa de formatos

| Formato | Nombre | Fuerte en | Uso tipico |
|---------|--------|-----------|------------|
| CSR | Compressed Sparse Row | Producto matriz-vector, aritmetica, slicing por filas | Formato de calculo por defecto |
| CSC | Compressed Sparse Column | Slicing por columnas, solvers/factorizaciones de columna | `splu`, operaciones por columna |
| COO | COOrdinate (tripletes) | Construccion incremental, conversion a CSR/CSC | Ensamblar desde tripletes (FEM) |
| LIL | List of Lists | Asignacion incremental fila a fila, cambios de estructura | Construir editando posiciones |
| DIA | Diagonal | Matrices con pocas diagonales (bandeadas) | Diferencias finitas, tridiagonales |
| BSR | Block Sparse Row | Bloques densos repetidos | Sistemas con grados de libertad por nodo |

## Como elegir formato

La regla de oro tiene dos fases:

1. **Construir** en un formato flexible: COO (desde tripletes, con duplicados que se suman) o LIL (editando posiciones una a una).
2. **Convertir y operar** en un formato comprimido: CSR (eje fila / producto) o CSC (eje columna / solvers).

> Construir directamente sobre CSR/CSC es caro: cada nueva posicion reestructura los arrays internos y emite `SparseEfficiencyWarning`. Construye flexible, comprime una vez.

## Operaciones disponibles

```python
import numpy as np
from scipy.sparse import coo_matrix

A = coo_matrix(([3, 4, 5], ([0, 1, 1], [2, 0, 2])), shape=(2, 3)).tocsr()

A @ np.array([1, 1, 1])   # producto matriz-vector -> array([3, 9])
A + A                     # aritmetica elemento a elemento
A * 2                     # escalado (en *_matrix, * sobre escalar)
A.tocsc()                 # conversion a CSC
A.toarray()              # densificar a ndarray (cuidado con el tamaño)
A.nnz                     # numero de no nulos almacenados
```

### Densidad

La densidad es `nnz / (filas * columnas)`. Disperso compensa cuando es baja (tipicamente < 10 %); con densidad alta, el array denso es mas rapido y simple.

```python
densidad = A.nnz / (A.shape[0] * A.shape[1])
```

## Resolver sistemas dispersos: scipy.sparse.linalg

El algebra lineal dispersa vive en el submodulo `scipy.sparse.linalg`, no en la matriz:

| Funcion | Para que |
|---------|----------|
| `spsolve` | Resolver `A x = b` directo (sistema disperso) |
| `splu` | Factorizacion LU dispersa reutilizable (trabaja en CSC) |
| `eigs` / `eigsh` | Autovalores/autovectores de matrices dispersas grandes |
| `cg`, `gmres` | Solvers iterativos (dominados por el producto matriz-vector) |

```python
from scipy.sparse.linalg import spsolve
x = spsolve(A_csr, b)     # A debe ser cuadrada; CSR o CSC
```

## Aviso de migracion: *_matrix vs *_array

SciPy esta migrando de las clases `*_matrix` a las clases `*_array` (`csr_array`, `csc_array`, `coo_array`, ...):

| | `*_matrix` (legado) | `*_array` (moderno, recomendado) |
|--|---------------------|----------------------------------|
| Semantica | Tipo `np.matrix` | Tipo `ndarray` |
| `*` | Producto **matricial** | Producto **elemento a elemento** |
| `@` | Producto matricial | Producto matricial |
| Dimensiones | Siempre 2-D | Soporta tambien 1-D |
| Estado | Mantenido pero no preferido | API futura |

> El cambio mas peligroso al migrar es `*`: en `*_matrix` es producto matricial, en `*_array` es elemento a elemento. Para producto matricial usa siempre `@`, que es inequivoco en ambas APIs.

## Errores comunes

| Error | Causa | Solucion |
|-------|-------|----------|
| `SparseEfficiencyWarning` | Modificas estructura de una CSR/CSC | Construye en COO/LIL y comprime al final |
| `MemoryError` en `.toarray()` | Densificas una matriz enorme | Opera disperso; densifica solo bloques |
| `*` da resultado inesperado | Confundes `*_matrix` y `*_array` | Usa `@` para producto matricial |
| `A @ v` falla en COO | COO no opera directamente | `.tocsr()` antes de operar |

## Notas relacionadas

- [[concepto_relacion_numpy]]
- [[csr_matrix]]
- [[csc_matrix]]
- [[coo_matrix]]
