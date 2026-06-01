---
title: np.linalg.matrix_transpose — Transpone los dos últimos ejes (por lotes)
aliases:
  - matrix_transpose
  - linalg.matrix_transpose
  - np.linalg.matrix_transpose
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

# np.linalg.matrix_transpose — Transpone los dos últimos ejes (por lotes)

## Firma de la función

```python
np.linalg.matrix_transpose(x) -> ndarray
```

## Valor de retorno

Devuelve `x` con sus **dos últimos ejes intercambiados**, dejando intactos los ejes anteriores (los de lote). Equivale a `np.swapaxes(x, -1, -2)`. Forma parte de la API estándar de arrays incorporada en **NumPy 2.0**.

| `x.shape` | Resultado | Interpretación |
|-----------|-----------|----------------|
| `(M, N)` | `(N, M)` | transposición de una matriz |
| `(B, M, N)` | `(B, N, M)` | transpone cada matriz del lote, conserva `B` |
| `(P, Q, M, N)` | `(P, Q, N, M)` | transposición por lotes en pilas ND |

```python
import numpy as np
A = np.arange(6).reshape(2, 3)
np.linalg.matrix_transpose(A)
# array([[0, 3],
#        [1, 4],
#        [2, 5]])   → shape (3, 2)
```

## Contraste con `.T`

| Operación | Ejes que invierte | `(B, M, N)` → |
|-----------|-------------------|---------------|
| `matrix_transpose(x)` | solo los **2 últimos** | `(B, N, M)` ✅ por lotes |
| `x.T` | **todos** los ejes (orden inverso completo) | `(N, M, B)` ⚠️ mezcla el lote |

```python
T = np.ones((10, 2, 3))   # 10 matrices 2x3
np.linalg.matrix_transpose(T).shape   # (10, 3, 2)  → correcto por lotes
T.T.shape                              # (3, 2, 10)  → invierte TODO
```

Para entender por qué difieren conviene razonar en términos de [[concepto_shape|shape]]: `.T` revierte la tupla completa, mientras `matrix_transpose` solo toca los dos ejes que representan la matriz.

## Parámetros en detalle

| Parámetro | Tipo | Descripción |
|-----------|------|-------------|
| `x` | ndarray `(..., M, N)` | Array con al menos 2 dimensiones. Los ejes de lote `...` se preservan |

### Requisitos

- `x` debe tener `ndim >= 2`; un array 1D lanza error (no hay dos ejes que intercambiar).
- Devuelve una **vista** cuando es posible (no copia datos, solo reordena strides).

## Casos de uso

### Transponer un stack de matrices sin tocar el eje de lote

```python
batch = np.random.rand(32, 4, 5)        # 32 matrices 4x5
batch_t = np.linalg.matrix_transpose(batch)   # shape (32, 5, 4)
```

### Construir productos del tipo `Aᵀ A` por lotes

```python
AtA = np.matmul(np.linalg.matrix_transpose(A), A)
```

## Buenas prácticas

1. Úsala (o el alias `np.matrix_transpose`) en lugar de `.T` cuando trabajes con **pilas** de matrices.
2. Reserva `.T` para arrays 2D, donde ambos coinciden.
3. Para matrices complejas, recuerda que esto transpone pero **no conjuga** (eso es la transpuesta conjugada / hermitiana).
4. Combínala con `np.matmul` para operaciones matriciales por lotes.

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| Usar `.T` en un stack 3D | `.T` invierte todos los ejes | usar `matrix_transpose` |
| `ValueError: ... at least 2 dimensions` | `x` es 1D | dar forma 2D antes |
| Esperar conjugado | solo transpone, no conjuga | usar transpuesta conjugada para complejos |

## Notas relacionadas

- [[concepto_shape]]
- [[np.linalg.dot]]
- [[np.linalg.matrix_power]]
