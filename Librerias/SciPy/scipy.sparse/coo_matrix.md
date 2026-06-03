---
title: coo_matrix — matriz dispersa en formato de tripletes (COO)
aliases:
  - coo_matrix
  - scipy.sparse.coo_matrix
  - COOrdinate format
  - formato de tripletes
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

# coo_matrix — matriz dispersa en formato de tripletes (COO)

Matriz dispersa en formato **COOrdinate** (de tripletes): almacena cada no nulo como una terna `(fila, columna, valor)` en tres listas paralelas (`row`, `col`, `data`). Es el formato de **construccion** por excelencia: rapido de ensamblar elemento a elemento y de convertir a CSR/CSC. A cambio, no soporta indexing ni aritmetica directos: es un formato de paso, no de calculo.

El flujo general (construir aqui, operar en formatos comprimidos) se detalla en [[scipy.sparse.operaciones]].

## Como almacena (tres listas paralelas)

| Array | Longitud | Contenido |
|-------|----------|-----------|
| `row` | `nnz` | Indice de fila de cada valor |
| `col` | `nnz` | Indice de columna de cada valor |
| `data` | `nnz` | Valor no nulo |

No hay compresion ni orden impuesto: el triplete `i` es `(row[i], col[i], data[i])`. Eso hace trivial **añadir** entradas (concatenar a las listas), pero impide acceso aleatorio eficiente.

## Construccion

```python
import numpy as np
from scipy.sparse import coo_matrix

# Desde tripletes paralelos
row  = [0, 1, 1]
col  = [2, 0, 2]
data = [3, 4, 5]
A = coo_matrix((data, (row, col)), shape=(2, 3))

# Desde array denso
B = coo_matrix(np.array([[0, 0, 3], [4, 0, 5]]))
```

## Duplicados: se SUMAN al convertir

COO **permite posiciones repetidas**. No se resuelven al construir, sino al comprimir (o al llamar `.sum_duplicates()`): las entradas que caen en la misma `(fila, columna)` se **suman**. Esto es la base del ensamblaje incremental.

```python
# Dos tripletes en la MISMA posicion (0, 0)
A = coo_matrix(([10, 5], ([0, 0], [0, 0])), shape=(1, 1))
A.toarray()        # -> array([[15]])   los duplicados se sumaron
```

## Atributos clave

| Atributo | Significado |
|----------|-------------|
| `row` | Indices de fila de los no nulos |
| `col` | Indices de columna de los no nulos |
| `data` | Valores no nulos |
| `nnz` | Numero de entradas almacenadas (incluye duplicados antes de sumarlos) |
| `shape` | Dimensiones `(filas, columnas)` |

## Flujo recomendado: construir en COO, operar en comprimido

```python
A = coo_matrix((data, (row, col)), shape=(n, n))
A_csr = A.tocsr()      # para producto matriz-vector, aritmetica, slicing por filas
A_csc = A.tocsc()      # para slicing por columnas o solvers de columnas
A.toarray()            # densificar (solo si la matriz es pequeña)
```

> COO no implementa `A @ v`, `A[i, j]` ni aritmetica: si lo intentas, conviertela antes. El patron canonico es **ensamblar en COO y `.tocsr()`/`.tocsc()` una sola vez** para operar.

## Fortalezas y debilidades

| Operacion | COO |
|-----------|-----|
| Construccion incremental desde tripletes | Muy rapida (fuerte) |
| Conversion a CSR/CSC | Muy rapida (fuerte) |
| Suma de contribuciones duplicadas | Automatica al comprimir (fuerte) |
| Indexing `A[i, j]` | No soportado (debil) |
| Aritmetica / producto matricial | No soportado directamente (debil) |

## Caso de uso central: ensamblaje por tripletes

Tipico del **metodo de elementos finitos** (FEM) y de ensamblar matrices a partir de contribuciones locales: cada elemento aporta sus tripletes a tres listas globales; al final se convierte una sola vez y los solapamientos se suman solos.

```python
rows, cols, vals = [], [], []
for elem in elementos:          # cada elemento aporta sus contribuciones
    rows.extend(elem.rows)
    cols.extend(elem.cols)
    vals.extend(elem.vals)
K = coo_matrix((vals, (rows, cols)), shape=(N, N)).tocsr()  # ensamblada y sumada
```

## Errores comunes

| Error | Causa | Solucion |
|-------|-------|----------|
| `A[i, j]` falla | COO no soporta indexing | `.tocsr()` antes de indexar |
| `A @ v` falla o avisa | COO no opera directamente | Convierte a CSR/CSC primero |
| Valores duplicados no detectados | Se suman, no se sobrescriben | Si querias sobrescribir, usa LIL o limpia antes |
| `nnz` mayor de lo esperado | Cuenta duplicados sin sumar | Llama `.sum_duplicates()` o comprime |

## Notas relacionadas

- [[scipy.sparse.operaciones]]
- [[csr_matrix]]
- [[csc_matrix]]
