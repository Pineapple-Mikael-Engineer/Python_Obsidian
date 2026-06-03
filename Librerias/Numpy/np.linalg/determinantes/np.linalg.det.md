---
title: np.linalg.det — Determinante de una matriz
aliases:
  - det
  - linalg.det
  - np.linalg.det
tags:
  - numpy
  - api/funcion
  - algebra/matricial

# --- Clasificación ---
lib: numpy
mod: np.linalg
tipo: funcion

# --- Comportamiento ---
retorna: float o ndarray
inplace: false

draft: false
---

# np.linalg.det — Determinante de una matriz

## Firma de la función

```python
np.linalg.det(a) -> float | ndarray
```

## Valor de retorno

Devuelve el **determinante** de `a`. Geométricamente es el factor de escala de volumen de la transformación lineal; un determinante **0 (o casi 0)** indica que la matriz es **singular** (no invertible).

| Entrada | Salida | Interpretación |
|---------|--------|----------------|
| `(M, M)` | escalar (`float`) | determinante de la matriz |
| `(..., M, M)` | `ndarray` `(...)` | un determinante por matriz apilada |
| `det ≈ 0` | — | matriz singular / casi singular |

```python
import numpy as np
A = np.array([[1, 2],
              [3, 4]])
np.linalg.det(A)   # -2.0   (1*4 - 2*3)

S = np.array([[1, 2], [2, 4]])
np.linalg.det(S)   # ~0.0  → singular (filas dependientes)
```

## Parámetros en detalle

### `a` — array de entrada

Matriz cuadrada `(M, M)` o **pila** de matrices cuadradas `(..., M, M)`. El cálculo se vectoriza sobre las dimensiones iniciales (ver [[concepto_shape]]).

```python
batch = np.array([[[1, 2], [3, 4]],
                  [[2, 0], [0, 2]]])
np.linalg.det(batch)   # [-2.,  4.]  → un determinante por matriz
```

El determinante se calcula por descomposición LU, por lo que el resultado es de tipo flotante aunque la entrada sea entera, y puede arrastrar pequeño error numérico (un determinante "exacto" 0 puede salir como `1e-16`).

## Casos de uso

### Comprobar invertibilidad antes de `inv`

```python
A = np.array([[2.0, 1.0], [1.0, 1.0]])
if not np.isclose(np.linalg.det(A), 0):
    A_inv = np.linalg.inv(A)
```

### Volumen de un paralelepípedo definido por vectores

```python
M = np.array([[1, 0, 0],
              [0, 2, 0],
              [0, 0, 3]], dtype=float)
abs(np.linalg.det(M))   # 6.0  → volumen
```

## Buenas prácticas

1. Para decidir invertibilidad, compara con `np.isclose(det, 0)`, no con `== 0` (error numérico).
2. Si los valores son muy grandes/pequeños y el determinante **desborda** o subdesborda, usa [[np.linalg.slogdet]] (estable en escala logarítmica).
3. No uses `det` para resolver sistemas (regla de Cramer): es lento e inestable; usa `solve`.
4. Para pilas de matrices, aprovecha el soporte `(..., M, M)` en lugar de un bucle.

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| `LinAlgError: Last 2 dimensions ... must be square` | matriz no cuadrada | reformar a `(M, M)` |
| `det` da `inf`/`0` por desbordamiento | valores enormes o diminutos | usar [[np.linalg.slogdet]] |
| `det == 0` exacto que falla | comparación estricta con error numérico | usar `np.isclose(det, 0)` |
| Sistema mal resuelto vía Cramer | uso de `det` para resolver | usar `np.linalg.solve` |

## Notas relacionadas

- [[concepto_shape]]
- [[np.linalg.slogdet]]
- [[np.linalg.inv]]
- [[np.linalg.solve]]
- [[np.linalg.matrix_rank]]
