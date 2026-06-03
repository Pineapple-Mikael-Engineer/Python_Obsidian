---
title: np.linalg.eig — Autovalores y autovectores de matriz general
aliases:
  - eig
  - linalg.eig
  - np.linalg.eig
tags:
  - numpy
  - api/funcion
  - algebra/matricial
lib: numpy
mod: np.linalg
tipo: funcion
retorna: tuple (w, v)
inplace: false
draft: false
---

# np.linalg.eig — Autovalores y autovectores de matriz general

## Firma de la función

```python
np.linalg.eig(a) -> EigResult(eigenvalues, eigenvectors)
```

Donde `a` es una matriz **cuadrada general** (no necesariamente simétrica) de [[concepto_shape|shape]] `(..., M, M)`.

## Valor de retorno

Devuelve una **tupla** (named tuple `EigResult`) de dos arrays: los autovalores y los autovectores derechos. Resuelve `a @ v[:, i] == w[i] * v[:, i]`.

| Posición | Nombre | Shape | Contenido |
|----------|--------|-------|-----------|
| `w` (índice 0) | `eigenvalues` | `(..., M)` | Autovalores, **1D**, sin ordenar. Pueden ser **complejos** aunque `a` sea real |
| `v` (índice 1) | `eigenvectors` | `(..., M, M)` | Matriz cuyas **columnas** son los autovectores; `v[:, i]` corresponde a `w[i]` |

> [!warning] Las **columnas** de `v` son los autovectores, no las filas. El autovector i-ésimo es `v[:, i]`, normalizado a norma 1.

```python
import numpy as np
a = np.array([[2.0, 0.0],
              [0.0, 3.0]])
w, v = np.linalg.eig(a)
w            # array([2., 3.])      → autovalores
v            # array([[1., 0.],     → columnas = autovectores
             #        [0., 1.]])
v[:, 0]      # array([1., 0.])      → autovector de w[0]=2

# Autovalores complejos aunque la matriz sea REAL (rotación):
r = np.array([[0.0, -1.0],
              [1.0,  0.0]])
np.linalg.eig(r).eigenvalues   # array([0.+1.j, 0.-1.j])
```

## Parámetros en detalle

### `a` — matriz de entrada

Array de shape `(..., M, M)`: una o varias matrices cuadradas apiladas. No requiere simetría. Se acepta dtype real o complejo; con entrada real el resultado puede ser complejo.

```python
lote = np.random.rand(5, 3, 3)      # 5 matrices 3×3
w, v = np.linalg.eig(lote)
w.shape    # (5, 3)      → autovalores por matriz
v.shape    # (5, 3, 3)   → autovectores por matriz
```

## Valor de retorno — verificar la descomposición

```python
a = np.array([[4.0, 1.0],
              [2.0, 3.0]])
w, v = np.linalg.eig(a)
# Reconstruir: a = v @ diag(w) @ inv(v)
np.allclose(a @ v, v @ np.diag(w))   # True
```

## Casos de uso

| Caso | Idea |
|------|------|
| Estabilidad de sistemas | Si todo `Re(w) < 0` el sistema lineal `x' = a·x` es estable |
| Modos / frecuencias propias | Autovalores = frecuencias; autovectores = formas de los modos |
| Cadenas de Markov | El autovalor 1 y su autovector dan la distribución estacionaria |
| Diagonalización | `a = v · diag(w) · v⁻¹` para potencias `a**n` baratas |

```python
# Potencia de matriz vía diagonalización
a = np.array([[2.0, 0.0], [0.0, 0.5]])
w, v = np.linalg.eig(a)
a_n = v @ np.diag(w**10) @ np.linalg.inv(v)
```

## Buenas prácticas

1. Si la matriz es **simétrica/Hermitiana** (covarianzas, matrices de Gram), usa [[np.linalg.eigh]]: es más rápida, estable y devuelve autovalores reales y ordenados.
2. Si solo necesitas los autovalores (no los vectores), usa [[np.linalg.eigvals]]: evita calcular `v`.
3. Recuerda indexar por **columnas**: `v[:, i]` es el autovector de `w[i]` (error clásico usar `v[i]`).
4. No asumas orden en `w`: con `eig` los autovalores no vienen ordenados.

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| `LinAlgError: Last 2 dimensions must be square` | matriz no cuadrada | comprobar `a.shape[-1] == a.shape[-2]` |
| Autovector equivocado | usar `v[i]` (fila) en vez de `v[:, i]` (columna) | indexar por columna |
| Resultado complejo inesperado | matriz real con autovalores complejos | es correcto; usar `eigh` si la matriz es simétrica |
| Autovalores en orden raro | `eig` no ordena | ordenar con `np.argsort(w)` o usar `eigh` |
| Imprecisión / lentitud en simétricas | usar `eig` en matriz simétrica | usar [[np.linalg.eigh]] |

## Notas relacionadas

- [[np.linalg.eigvals]]
- [[np.linalg.eigh]]
- [[np.linalg.eigvalsh]]
- [[concepto_shape]]
