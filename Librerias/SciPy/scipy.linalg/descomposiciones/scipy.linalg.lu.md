---
title: scipy.linalg.lu — factorizacion LU con pivoteo (P, L, U)
aliases:
  - lu
  - scipy.linalg.lu
  - factorizacion LU
tags:
  - scipy
  - api/funcion
  - algebra-lineal
lib: scipy
tipo: funcion
mod: scipy.linalg
retorna: tuple (ndarray, ndarray, ndarray)
requiere:
  - numpy
draft: false
---

# scipy.linalg.lu — factorizacion LU con pivoteo (P, L, U)

Factoriza una matriz `a` como `a = P·L·U` mediante **eliminacion gaussiana con pivoteo parcial de filas** (rutina LAPACK `getrf`). `P` es una matriz de permutacion, `L` es **triangular inferior con diagonal unitaria** y `U` es **triangular superior**. Por defecto devuelve la **tupla** `(P, L, U)`. Es la base para resolver sistemas, calcular determinantes e invertir matrices de forma estable.

> Nota transversal: esta funcion **no existe en `numpy.linalg`**. `scipy.linalg` corre siempre sobre LAPACK y es un superset de `numpy.linalg`; ver [[concepto_relacion_numpy]]. Si necesitas LU, usa SciPy.

## Firma

```python
scipy.linalg.lu(
    a,                   # array_like: matriz (M, N) a factorizar
    permute_l=False,     # bool: True -> devuelve (PL, U) en vez de (P, L, U)
    overwrite_a=False,   # bool: permite sobrescribir 'a' (ahorra memoria)
    check_finite=True,   # bool: valida ausencia de NaN/inf (False = mas rapido)
    p_indices=False,     # bool: True -> P se devuelve como vector de indices
) -> tuple
```

## Valor de retorno

Con `permute_l=False` (por defecto) devuelve **tres arrays**:

| Posicion | Nombre | Forma | Significado |
|----------|--------|-------|-------------|
| `[0]` | `P` | `(M, M)` | Matriz de permutacion (o vector de indices si `p_indices=True`) |
| `[1]` | `L` | `(M, K)` | Triangular inferior, diagonal unitaria (`K = min(M, N)`) |
| `[2]` | `U` | `(K, N)` | Triangular superior |

Con `permute_l=True` devuelve **dos arrays**:

| Posicion | Nombre | Forma | Significado |
|----------|--------|-------|-------------|
| `[0]` | `PL` | `(M, K)` | Producto `P·L` ya combinado |
| `[1]` | `U` | `(K, N)` | Triangular superior |

```python
P, L, U = lu(a)                  # desempaquetado tipico
PL, U   = lu(a, permute_l=True)  # forma combinada
```

## Formas basicas de llamada

| Objetivo | Llamada |
|----------|---------|
| Factorizacion estandar | `lu(A)` -> `(P, L, U)` |
| Forma combinada P·L | `lu(A, permute_l=True)` -> `(PL, U)` |
| P como indices de fila | `lu(A, p_indices=True)` |
| Sin validar finitud (rapido) | `lu(A, check_finite=False)` |

## Parametros en detalle

### `a` (obligatorio)

Matriz `(M, N)`, real o compleja. No tiene que ser cuadrada: para `M != N` las formas se ajustan con `K = min(M, N)`.

```python
import numpy as np
from scipy.linalg import lu

A = np.array([[4.0, 3.0],
              [6.0, 3.0]])
P, L, U = lu(A)
np.allclose(P @ L @ U, A)   # → True   (reconstruccion exacta)
```

### `permute_l`

Si `True`, premultiplica `L` por `P` y devuelve solo `(PL, U)`. Util cuando solo se quiere reconstruir `a = PL·U` sin manejar la permutacion por separado.

### `p_indices`

Si `True`, `P` se devuelve como un **vector de indices de fila** (`(M,)`) en lugar de la matriz densa de permutacion; mas eficiente para reordenar filas con indexado avanzado.

### `overwrite_a`, `check_finite`

`overwrite_a=True` deja que LAPACK reutilice el buffer de `a` (mas rapido, destruye la entrada). `check_finite=False` salta la validacion de `NaN`/`inf`: acelera pero asume datos limpios.

## Casos de uso

### Resolver A·x = b reutilizando la factorizacion

Para **varios lados derechos** con la misma `A`, la pareja eficiente es `lu_factor` + `lu_solve`: factorizas una vez (`O(n^3)`) y cada resolucion cuesta solo `O(n^2)`.

```python
import numpy as np
from scipy.linalg import lu_factor, lu_solve

A = np.array([[3.0, 1.0], [1.0, 2.0]])
lu_piv = lu_factor(A)            # factoriza una sola vez

x1 = lu_solve(lu_piv, [9.0, 8.0])   # → [2., 3.]
x2 = lu_solve(lu_piv, [1.0, 0.0])   # reutiliza la misma factorizacion
```

### Determinante via U

El determinante de `a` es `(-1)^(num_swaps) · prod(diag(U))`, porque `det(P)=±1` y `det(L)=1`.

```python
P, L, U = lu(A)
det = np.linalg.det(P) * np.prod(np.diag(U))
```

## Buenas practicas

1. Para **un solo** sistema usa `solve`; para **multiples RHS** con la misma matriz, factoriza con `lu_factor` y reutiliza con `lu_solve`.
2. Usa `lu` (que da `P, L, U` explicitos) cuando necesites las matrices en si (didactica, determinante, analisis). Usa `lu_factor` cuando solo vayas a resolver sistemas: es mas compacto.
3. `p_indices=True` evita construir la matriz densa `P` cuando solo reordenas filas.
4. En bucles criticos activa `overwrite_a=True` y `check_finite=False` para minimizar copias y validaciones.

## Errores comunes

| Error | Causa | Solucion |
|-------|-------|----------|
| Esperar que `L` tenga la diagonal de `a` | `L` siempre tiene diagonal **unitaria** | Los valores van en `U`, no en `L` |
| `P @ L @ U != A` aparente | Orden de factores incorrecto | Es `a = P·L·U`, en ese orden |
| Buscar `numpy.linalg.lu` | No existe en NumPy | Usar `scipy.linalg.lu` |
| Refactorizar en cada RHS | Desperdicia `O(n^3)` por iteracion | `lu_factor` una vez + `lu_solve` por RHS |
| Pasar matriz con NaN sin avisar | `check_finite=False` no valida | Mantener `check_finite=True` si los datos no estan limpios |

## Limitaciones

- No comprueba ni explota simetria/definicion positiva: para matrices SPD, Cholesky es ~2x mas rapido.
- El pivoteo es **parcial** (solo filas); no hay pivoteo completo.
- Para resolver sistemas, `lu` por si sola es menos comoda que la pareja `lu_factor`/`lu_solve`.

## Notas relacionadas

- [[scipy.linalg.qr]]
- [[scipy.linalg.cholesky]]
- [[scipy.linalg.svd]]
- [[concepto_relacion_numpy]]
