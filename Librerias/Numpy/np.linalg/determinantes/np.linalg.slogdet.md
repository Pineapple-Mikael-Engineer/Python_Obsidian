---
title: np.linalg.slogdet — Signo y log del determinante (estable)
aliases:
  - slogdet
  - linalg.slogdet
  - np.linalg.slogdet
tags:
  - numpy
  - api/funcion
  - algebra/matricial

# --- Clasificación ---
lib: numpy
mod: np.linalg
tipo: funcion

# --- Comportamiento ---
retorna: tuple (sign, logabsdet)
inplace: false

draft: false
---

# np.linalg.slogdet — Signo y log del determinante (estable)

## Firma de la función

```python
np.linalg.slogdet(a) -> tuple[ndarray, ndarray]   # (sign, logabsdet)
```

## Valor de retorno

Devuelve una **tupla** `(sign, logabsdet)` que codifica el determinante de forma **numéricamente estable**, evitando el desbordamiento que sufre [[np.linalg.det]] con matrices grandes. El determinante se reconstruye como `sign * exp(logabsdet)`.

| Elemento | Tipo | Significado |
|----------|------|-------------|
| `sign` | `float`/`ndarray` | signo del determinante: `-1`, `0` o `1` (complejo de módulo 1 si `a` es complejo) |
| `logabsdet` | `float`/`ndarray` | logaritmo natural del valor absoluto del determinante |

Casos especiales del par devuelto:

| Situación | `sign` | `logabsdet` |
|-----------|--------|-------------|
| `det` positivo | `1.0` | `log(det)` |
| `det` negativo | `-1.0` | `log(|det|)` |
| matriz singular (`det = 0`) | `0.0` | `-inf` |

```python
import numpy as np
A = np.array([[1, 2],
              [3, 4]])
sign, logabsdet = np.linalg.slogdet(A)
sign                       # -1.0
sign * np.exp(logabsdet)   # -2.0  → reconstruye det(A)
```

## Parámetros en detalle

### `a` — array de entrada

Matriz cuadrada `(M, M)` o **pila** de matrices `(..., M, M)`. Con pilas, tanto `sign` como `logabsdet` son `ndarray` con la forma de las dimensiones iniciales (ver [[concepto_shape]]).

```python
batch = np.array([[[1., 2.], [3., 4.]],
                  [[2., 0.], [0., 2.]]])
sign, logabsdet = np.linalg.slogdet(batch)
sign        # [-1.,  1.]
logabsdet   # [0.693..., 1.386...]
```

## Casos de uso

### Determinantes que desbordarían con det()

```python
M = np.eye(2000) * 10.0       # det = 10**2000 → overflow en det()
sign, logabsdet = np.linalg.slogdet(M)
sign, logabsdet               # (1.0, 4605.17...)  → estable
```

### Verosimilitud gaussiana (log-densidad)

```python
# log|Σ| aparece en la log-verosimilitud multivariante
Sigma = np.array([[2.0, 0.3], [0.3, 1.0]])
_, log_det = np.linalg.slogdet(Sigma)   # usar log_det directamente
```

## Buenas prácticas

1. En estadística/ML trabaja con `logabsdet` directamente; rara vez necesitas reconstruir el determinante real.
2. Detecta singularidad comprobando `sign == 0` o `logabsdet == -inf`.
3. Prefiere `slogdet` sobre `det` siempre que la matriz sea grande o los valores muy dispares.
4. No reconstruyas con `sign * exp(logabsdet)` si el objetivo es evitar overflow: pierdes la ventaja.

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| `LinAlgError: Last 2 dimensions ... must be square` | matriz no cuadrada | reformar a `(M, M)` |
| Olvidar que devuelve 2 valores | tratar la salida como escalar | desempacar `sign, logabsdet = ...` |
| Reconstruir y volver a desbordar | `sign * exp(logabsdet)` con det enorme | usar `logabsdet` sin exponenciar |
| No detectar singularidad | esperar excepción | comprobar `sign == 0` / `logabsdet == -inf` |

## Notas relacionadas

- [[concepto_shape]]
- [[np.linalg.det]]
- [[np.linalg.inv]]
- [[np.linalg.solve]]
