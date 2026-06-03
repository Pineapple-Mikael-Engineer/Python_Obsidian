---
title: np.linalg.solve — Resolver el sistema lineal Ax = b
aliases:
  - solve
  - linalg.solve
  - np.linalg.solve
tags:
  - numpy
  - api/funcion
  - algebra/matricial
lib: numpy
mod: np.linalg
tipo: funcion
retorna: ndarray
inplace: false
draft: false
---

# np.linalg.solve — Resolver el sistema lineal Ax = b

## Firma de la función

```python
np.linalg.solve(a, b) -> ndarray
```

## Valor de retorno

Resuelve el sistema lineal `a @ x = b` y devuelve `x`, con `a` **cuadrada** y **no singular**. Internamente usa factorización LU con pivoteo: es más rápida y numéricamente más estable que invertir y multiplicar. Es la función **preferida** frente a [[np.linalg.inv]].

| Entrada `a` | Entrada `b` | Retorno `x` | Caso |
|-------------|-------------|-------------|------|
| `(M, M)` | `(M,)` | `(M,)` | un único término independiente |
| `(M, M)` | `(M, K)` | `(M, K)` | `K` sistemas con la misma matriz |
| `(..., M, M)` | `(..., M)` | `(..., M)` | pila de sistemas (broadcasting) |
| singular | cualquiera | — | lanza `LinAlgError` |

```python
import numpy as np
A = np.array([[3., 1.],
              [1., 2.]])
b = np.array([9., 8.])
x = np.linalg.solve(A, b)
x                  # [2., 3.]
A @ x              # [9., 8.]  → recupera b
```

## Parámetros en detalle

### `a` — matriz de coeficientes

Array de shape `(..., M, M)`. Debe ser cuadrada y no singular. El último par de ejes forma la matriz; los ejes previos permiten pilas de sistemas.

### `b` — términos independientes

Array de shape `(..., M)` o `(..., M, K)`. Cada columna de `b` es un término independiente distinto que comparte la misma matriz `a`; el [[concepto_shape|shape]] del resultado sigue el de `b`.

```python
A = np.array([[2., 0.],
              [0., 4.]])
B = np.array([[2., 6.],
              [4., 8.]])         # dos sistemas a la vez
np.linalg.solve(A, B)           # [[1., 3.], [1., 2.]]
```

## Casos de uso

### Sistema 3×3

```python
A = np.array([[1., 2., 3.],
              [2., 5., 3.],
              [1., 0., 8.]])
b = np.array([6., 4., 9.])
np.linalg.solve(A, b)   # solución única del sistema
```

### Resolver varios sistemas con la misma matriz

```python
A = np.array([[4., 3.],
              [6., 3.]])
B = np.column_stack([[7., 9.], [1., 3.]])
np.linalg.solve(A, B)   # cada columna de la salida resuelve una columna de B
```

## Buenas prácticas

1. Usa `solve(A, b)` en lugar de `inv(A) @ b`: misma respuesta, más rápida y estable.
2. Para varios términos independientes con la misma `A`, pásalos juntos como columnas de `b` (una sola factorización).
3. Si `A` es singular o rectangular, recurre a mínimos cuadrados con [[np.linalg.lstsq]].
4. Para la versión tensorial N-dimensional, usa [[np.linalg.tensorsolve]].

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| `LinAlgError: Singular matrix` | `a` no invertible (det = 0) | usar `lstsq` o revisar el sistema |
| `LinAlgError: Last 2 dimensions must be square` | `a` no cuadrada | usar `lstsq` |
| `ValueError` de dimensiones | shapes de `a` y `b` incompatibles | alinear: `a` `(M, M)`, `b` `(M,)` o `(M, K)` |
| Resultado inestable | `a` mal condicionada | revisar `np.linalg.cond(a)` |

## Limitaciones

- Solo sistemas cuadrados y compatibles determinados; para sobredeterminados, usar `lstsq`.
- No detecta sistemas casi singulares: vigila el condicionamiento.

## Notas relacionadas

- [[np.linalg.inv]]
- [[np.linalg.lstsq]]
- [[np.linalg.tensorsolve]]
- [[concepto_shape]]
