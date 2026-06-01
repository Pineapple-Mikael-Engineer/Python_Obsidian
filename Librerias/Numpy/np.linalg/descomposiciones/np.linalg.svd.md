---
title: np.linalg.svd — Descomposición en Valores Singulares (SVD)
aliases:
  - svd
  - linalg.svd
  - np.linalg.svd
tags:
  - numpy
  - api/funcion
  - algebra/matricial
lib: numpy
mod: np.linalg
tipo: funcion
retorna: tuple (U, S, Vh) o ndarray (S)
inplace: false
draft: false
---

# np.linalg.svd — Descomposición en Valores Singulares (SVD)

Factoriza una matriz `a` en tres componentes tales que `a = U @ diag(S) @ Vh`. Es la descomposición más general y numéricamente estable del álgebra lineal: existe para **cualquier** matriz (cuadrada o no, singular o no) y es la base de PCA, la pseudo-inversa, la compresión de datos y el cálculo de rango.

## Firma de la función

```python
np.linalg.svd(
    a,
    full_matrices=True,
    compute_uv=True,
    hermitian=False
) -> tuple[ndarray, ndarray, ndarray] | ndarray
```

## Valor de retorno

Con `compute_uv=True` (por defecto) devuelve una **tupla de 3 arrays**. Para una entrada `a` de [[concepto_shape|shape]] `(M, N)` y `K = min(M, N)`:

| Elemento | Nombre | Shape (`full_matrices=True`) | Shape (`full_matrices=False`) | Significado |
|----------|--------|------------------------------|-------------------------------|-------------|
| `U` | Vectores singulares izquierdos | `(M, M)` | `(M, K)` | Columnas ortonormales; base del espacio columna |
| `S` | Valores singulares | `(K,)` | `(K,)` | Vector 1D, **reales ≥ 0, en orden descendente** |
| `Vh` | Vectores singulares derechos (conjugada-traspuesta) | `(N, N)` | `(K, N)` | Filas ortonormales; ya es `V.conj().T`, no `V` |

Con `compute_uv=False` devuelve **solo** `S` (un único ndarray `(K,)`), sin la tupla.

```python
import numpy as np
A = np.array([[1.0, 2.0, 3.0],
              [4.0, 5.0, 6.0]])      # shape (2, 3)

U, S, Vh = np.linalg.svd(A)
U.shape    # (2, 2)
S.shape    # (2,)   → [9.508, 0.773] aprox, descendente
Vh.shape   # (3, 3)

# Reconstrucción: a = U @ diag(S) @ Vh
Sigma = np.zeros((2, 3))
Sigma[:2, :2] = np.diag(S)
np.allclose(A, U @ Sigma @ Vh)        # True
```

**Cuidado con la tupla:** el tercer elemento es `Vh` (ya transpuesto/conjugado), no `V`. Para obtener `V` usa `Vh.conj().T`.

## Parámetros en detalle

### `a` — matriz de entrada

Array de shape `(..., M, N)`. Admite **stacks**: las dimensiones iniciales se tratan como lote (batch) y la SVD se aplica a cada matriz `(M, N)` final.

```python
lote = np.random.rand(5, 3, 4)   # 5 matrices 3×4
U, S, Vh = np.linalg.svd(lote)
S.shape                          # (5, 3)  → un vector singular por matriz
```

### `full_matrices` — tamaño de `U` y `Vh`

Si `True` (defecto), `U` y `Vh` son cuadradas y completas `(M, M)` / `(N, N)`. Si `False`, se recortan a `(M, K)` / `(K, N)`: la **forma reducida (thin SVD)**, más barata y suficiente para reconstruir `a`.

```python
A = np.random.rand(100, 5)
U, S, Vh = np.linalg.svd(A, full_matrices=False)
U.shape    # (100, 5)  en vez de (100, 100)  → mucho más ligero
```

### `compute_uv` — calcular vectores singulares

Si `False`, omite `U` y `Vh` y devuelve solo `S`. Útil cuando solo necesitas los valores singulares (rango, norma 2, número de condición).

```python
S = np.linalg.svd(A, compute_uv=False)   # devuelve un solo array, no tupla
rango = np.sum(S > 1e-10)                # rango numérico
cond  = S[0] / S[-1]                      # número de condición
```

### `hermitian` — optimización para matrices hermíticas

Si `True`, asume que `a` es hermítica (simétrica si es real) y usa un algoritmo más eficiente y preciso.

## Casos de uso

### Pseudo-inversa de Moore-Penrose

```python
A = np.random.rand(4, 3)
U, S, Vh = np.linalg.svd(A, full_matrices=False)
A_pinv = Vh.conj().T @ np.diag(1.0 / S) @ U.conj().T
# equivalente directo: np.linalg.pinv(A)
```

### Compresión / aproximación de rango bajo

```python
U, S, Vh = np.linalg.svd(imagen, full_matrices=False)
k = 20                                  # conservar 20 componentes
aprox = U[:, :k] @ np.diag(S[:k]) @ Vh[:k, :]
```

### Rango numérico y número de condición

```python
S = np.linalg.svd(M, compute_uv=False)
rango = np.count_nonzero(S > S.max() * 1e-12)
```

## Buenas prácticas

1. Usa `full_matrices=False` cuando `M` y `N` difieran mucho: evita construir matrices enormes e innecesarias.
2. Si solo te interesan los valores singulares, usa `compute_uv=False` (más rápido y devuelve un solo array).
3. Recuerda que el retorno es `Vh`, **no** `V`: para reconstruir o proyectar usa `Vh` directamente o `Vh.conj().T` para obtener `V`.
4. Los valores singulares en `S` ya vienen ordenados de forma **descendente**: `S[0]` es el mayor.
5. La SVD existe siempre; prefierela frente a la diagonalización cuando la matriz no sea cuadrada o esté mal condicionada.

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| `LinAlgError: SVD did not converge` | datos con `NaN`/`inf` o caso patológico | limpiar entradas; comprobar `np.isfinite(a).all()` |
| Reconstrucción no coincide | usar `V` en vez de `Vh`, o `diag(S)` mal dimensionado | reconstruir con `U @ diag(S) @ Vh` y `Sigma` del shape correcto |
| `U`/`Vh` demasiado grandes en memoria | `full_matrices=True` con matriz muy rectangular | `full_matrices=False` |
| `ValueError` al desempaquetar | `compute_uv=False` devuelve solo `S`, no una tupla | asignar a una sola variable |
| `LinAlgError: Last 2 dimensions...` | entrada con menos de 2 dimensiones | pasar al menos una matriz 2D |

## Notas relacionadas

- [[concepto_shape]]
- [[np.linalg.qr]]
- [[np.linalg.cholesky]]
- [[np.linalg.pinv]]
- [[np.linalg.eig]]
- [[np.linalg.matrix_rank]]
