---
title: np.linalg.cond — Número de condición de una matriz
aliases:
  - cond
  - linalg.cond
  - np.linalg.cond
tags:
  - numpy
  - api/funcion
  - algebra/matricial

# --- Clasificación ---
lib: numpy
mod: np.linalg
tipo: funcion

# --- Comportamiento ---
retorna: float
inplace: false

draft: false
---

# np.linalg.cond — Número de condición de una matriz

## Firma de la función

```python
np.linalg.cond(
    x,
    p=None
) -> float
```

## Valor de retorno

Devuelve el **número de condición** de `x`: una medida de cuán **sensible** es la solución de un sistema lineal a perturbaciones en los datos. Es la razón entre el mayor y el menor valor singular (para `p=None`/`p=2`).

| Valor | Interpretación |
|-------|----------------|
| `≈ 1` | matriz bien condicionada (estable) |
| `>> 1` | mal condicionada (cerca de singular) |
| `inf` | matriz singular (no invertible) |

```python
import numpy as np
I = np.eye(3)
np.linalg.cond(I)   # 1.0  → perfectamente condicionada
```

Regla práctica: con un condicionamiento de `10^k`, esperas perder unos `k` dígitos de precisión al resolver el sistema. Un sistema con `cond ~ 1e8` en doble precisión ya es delicado.

## Parámetros en detalle

### `x` — matriz de entrada

Matriz `(M, N)`. Para `p=2`/`None` puede no ser cuadrada (usa valores singulares); para el resto de normas debe ser cuadrada e invertible.

### `p` — norma usada para el condicionamiento

Selecciona la norma con la que se mide. Por defecto (`None`) usa la norma 2 (razón de valores singulares vía SVD).

| `p` | Norma usada |
|-----|-------------|
| `None` | norma 2 (razón de valores singulares) |
| `2` | mayor / menor valor singular |
| `-2` | menor / mayor valor singular |
| `1` | norma 1 (máxima suma de columna) |
| `np.inf` | norma infinito (máxima suma de fila) |
| `'fro'` | norma de Frobenius |

```python
A = np.array([[1.0, 2.0],
              [2.0, 4.001]])   # casi linealmente dependiente
np.linalg.cond(A)              # número enorme → mal condicionada
```

## Casos de uso

### Diagnosticar un sistema antes de resolverlo

```python
A = np.array([[1.0, 1.0], [1.0, 1.0001]])
b = np.array([2.0, 2.0001])
np.linalg.cond(A)     # ~ 4e4  → resultado sensible al ruido
x = np.linalg.solve(A, b)
```

### Comparar estabilidad de matrices candidatas

```python
np.linalg.cond(np.eye(4))            # 1.0
np.linalg.cond(np.vander([1,2,3,4])) # grande → Vandermonde mal condicionada
```

## Buenas prácticas

1. Comprueba `cond` antes de invertir o resolver sistemas con datos ruidosos.
2. Para mínimos cuadrados mal condicionados, prefiere [[np.linalg.lstsq]] o regularización en vez de `inv`.
3. Recuerda que un `cond` alto no es un error: avisa de pérdida de precisión, no la causa.
4. Usa `p=2` (default) para la interpretación estándar basada en valores singulares.

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| `cond` devuelve `inf` | matriz singular | revisar dependencias lineales; no se puede invertir |
| `LinAlgError` | `p` ≠ 2 con matriz no cuadrada o singular | usar `p=2`/`None`, que admite SVD |
| Resultados poco fiables tras resolver | `cond` muy alto ignorado | reformular el problema o regularizar |
| Esperar precisión total | confiar en sistema mal condicionado | estimar dígitos perdidos como `log10(cond)` |

## Notas relacionadas

- [[concepto_shape]]
- [[np.linalg.norm]]
- [[np.linalg.matrix_rank]]
- [[np.linalg.solve]]
- [[np.linalg.svd]]
