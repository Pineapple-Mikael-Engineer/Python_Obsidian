---
title: np.linalg.inv — Inversa de una matriz cuadrada
aliases:
  - inv
  - linalg.inv
  - np.linalg.inv
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

# np.linalg.inv — Inversa de una matriz cuadrada

## Firma de la función

```python
np.linalg.inv(a) -> ndarray
```

## Valor de retorno

Devuelve la inversa `a⁻¹` tal que `a @ a⁻¹ == I` (identidad). Requiere que `a` sea **cuadrada** y **no singular** (determinante distinto de cero). Acepta pilas de matrices: si la entrada tiene shape `(..., M, M)`, invierte cada matriz `M×M` del último par de ejes.

| Entrada | Retorno | Ejemplo |
|---------|---------|---------|
| `(M, M)` no singular | `(M, M)` inversa | `inv([[1,2],[3,4]])` → `[[-2, 1],[1.5,-0.5]]` |
| `(K, M, M)` pila | `(K, M, M)` cada inversa | invierte las `K` matrices |
| matriz singular | — | lanza `LinAlgError` |
| matriz no cuadrada | — | lanza `LinAlgError` |

```python
import numpy as np
A = np.array([[1., 2.],
              [3., 4.]])
Ainv = np.linalg.inv(A)
Ainv               # [[-2. ,  1. ], [ 1.5, -0.5]]
A @ Ainv           # [[1., 0.], [0., 1.]]  → identidad (salvo error numérico)
```

## Parámetros en detalle

### `a` — matriz a invertir

Array de shape `(..., M, M)`. El último par de ejes debe formar una matriz cuadrada. El [[concepto_shape|shape]] determina si se procesa una sola matriz o una pila de ellas.

```python
pila = np.random.rand(5, 3, 3)
np.linalg.inv(pila).shape   # (5, 3, 3)  → 5 inversas de 3×3
```

## Casos de uso

### Invertir una matriz de coeficientes

```python
A = np.array([[2., 1.],
              [1., 3.]])
np.linalg.inv(A)   # [[ 0.6, -0.2], [-0.2,  0.4]]
```

### Verificar inversibilidad antes de invertir

```python
A = np.array([[1., 2.],
              [2., 4.]])      # filas proporcionales → singular
np.linalg.det(A)             # 0.0  → no invertible
# np.linalg.inv(A)           # LinAlgError: Singular matrix
```

## Buenas prácticas

1. Para resolver un sistema `Ax = b` **no** calcules `inv(A) @ b`; usa [[np.linalg.solve]], que es más rápido y numéricamente más estable.
2. Reserva `inv` para cuando necesites la matriz inversa explícita (p. ej. matrices de covarianza, transformaciones repetidas).
3. Si la matriz puede ser singular o rectangular, usa la pseudo-inversa [[np.linalg.pinv]] en su lugar.
4. Comprueba el condicionamiento con `np.linalg.cond(A)`: valores muy altos avisan de inversa numéricamente inestable.

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| `LinAlgError: Singular matrix` | determinante = 0 (filas/columnas dependientes) | usar `pinv` o revisar el sistema |
| `LinAlgError: Last 2 dimensions must be square` | matriz no cuadrada | usar `pinv` para rectangulares |
| Resultado impreciso | matriz mal condicionada (`cond` alto) | reformular; preferir `solve`/`lstsq` |
| Lento e inestable al resolver sistemas | usar `inv(A) @ b` | usar `solve(A, b)` |

## Limitaciones

- Solo matrices cuadradas; para rectangulares o singulares, usar pseudo-inversa.
- Calcular la inversa para resolver sistemas es ineficiente: factoriza LU de todos modos.

## Notas relacionadas

- [[np.linalg.solve]]
- [[np.linalg.pinv]]
- [[np.linalg.det]]
- [[concepto_shape]]
