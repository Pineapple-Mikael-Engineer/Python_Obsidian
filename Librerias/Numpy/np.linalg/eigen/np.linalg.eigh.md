---
title: np.linalg.eigh — Autovalores/autovectores de matriz simétrica o Hermitiana
aliases:
  - eigh
  - linalg.eigh
  - np.linalg.eigh
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

# np.linalg.eigh — Autovalores/autovectores de matriz simétrica o Hermitiana

## Firma de la función

```python
np.linalg.eigh(a, UPLO='L') -> EighResult(eigenvalues, eigenvectors)
```

Donde `a` es una matriz **simétrica** (real) o **Hermitiana** (compleja) de [[concepto_shape|shape]] `(..., M, M)`. Es la versión especializada y preferida frente a [[np.linalg.eig]] cuando la matriz es simétrica.

## Valor de retorno

Devuelve una **tupla** (named tuple `EighResult`) con autovalores y autovectores. A diferencia de `eig`, los autovalores son **reales** y vienen en **orden ascendente**.

| Posición | Nombre | Shape | Contenido |
|----------|--------|-------|-----------|
| `w` (índice 0) | `eigenvalues` | `(..., M)` | Autovalores **reales**, en orden **ascendente** |
| `v` (índice 1) | `eigenvectors` | `(..., M, M)` | Matriz cuyas **columnas** son los autovectores (ortonormales); `v[:, i]` corresponde a `w[i]` |

> [!tip] Como `a` es simétrica, los autovalores son reales y `v` es **ortogonal**: `v.T @ v == I`. Las columnas de `v` son los autovectores.

```python
import numpy as np
a = np.array([[2.0, 1.0],
              [1.0, 2.0]])          # simétrica
w, v = np.linalg.eigh(a)
w            # array([1., 3.])       → reales y ascendentes
v[:, 0]      # autovector de w[0]=1
np.allclose(v.T @ v, np.eye(2))     # True → columnas ortonormales
np.allclose(a @ v, v @ np.diag(w))  # True
```

## Parámetros en detalle

### `a` — matriz simétrica/Hermitiana

Array de shape `(..., M, M)`. Solo se lee el **triángulo** indicado por `UPLO`; el otro triángulo se ignora (se asume simetría). Si pasas una matriz no simétrica, el resultado será el de su parte simétrica implícita, no un error.

### `UPLO` — triángulo a usar (`'L'` o `'U'`)

Indica qué mitad de la matriz se lee. `'L'` (por defecto) usa el triángulo **inferior**; `'U'` el **superior**.

```python
a = np.array([[2.0, 1.0],
              [9.9, 2.0]])   # triángulo superior "sucio"
np.linalg.eigh(a, UPLO='L').eigenvalues   # usa 1.0 → simétrica real
```

## Casos de uso

| Caso | Idea |
|------|------|
| PCA | `eigh` de la matriz de **covarianza** (siempre simétrica) → componentes principales |
| Matrices de Gram / kernels | Son simétricas positivas semidefinidas |
| Definir positividad | Todos `w > 0` ⇒ definida positiva (Cholesky existe) |
| Física cuántica | Hamiltonianos Hermitianos: energías (reales) = autovalores |

```python
# PCA: direcciones de máxima varianza
X = np.random.rand(100, 3)
C = np.cov(X, rowvar=False)              # covarianza 3×3 (simétrica)
w, v = np.linalg.eigh(C)
componente_principal = v[:, -1]          # mayor autovalor está al final
```

## Buenas prácticas

1. Si la matriz es simétrica/Hermitiana, usa **siempre** `eigh` en lugar de [[np.linalg.eig]]: más rápida, más estable y sin parte imaginaria espuria.
2. Aprovecha el **orden ascendente**: el mayor autovalor (y su componente principal) es `w[-1]` / `v[:, -1]`.
3. Indexa los autovectores por **columna** (`v[:, i]`), nunca por fila.
4. Si solo necesitas autovalores (test de definida positiva, etc.), usa [[np.linalg.eigvalsh]].

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| `LinAlgError: Last 2 dimensions must be square` | matriz no cuadrada | verificar shape `(..., M, M)` |
| Resultado inesperado con matriz no simétrica | `eigh` ignora medio triángulo | asegurar simetría o usar [[np.linalg.eig]] |
| Tomar `v[i]` como autovector | son **columnas**, no filas | usar `v[:, i]` |
| Buscar el mayor autovalor en `w[0]` | el orden es **ascendente** | el máximo está en `w[-1]` |
| Autovalores con parte imaginaria al usar `eig` | matriz simétrica con la función general | cambiar a `eigh` |

## Notas relacionadas

- [[np.linalg.eig]]
- [[np.linalg.eigvalsh]]
- [[np.linalg.eigvals]]
- [[concepto_shape]]
