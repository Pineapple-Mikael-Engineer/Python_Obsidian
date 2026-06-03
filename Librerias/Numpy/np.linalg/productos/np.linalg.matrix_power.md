---
title: np.linalg.matrix_power — Potencia entera de una matriz cuadrada
aliases:
  - matrix_power
  - linalg.matrix_power
  - np.linalg.matrix_power
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

# np.linalg.matrix_power — Potencia entera de una matriz cuadrada

## Firma de la función

```python
np.linalg.matrix_power(a, n) -> ndarray
```

## Valor de retorno

Eleva una matriz **cuadrada** `a` a la potencia entera `n`, es decir `a @ a @ ... @ a` (`n` veces). Es la versión matricial de `**` con producto matricial, no elemento a elemento.

| `n` | Resultado | Significado |
|-----|-----------|-------------|
| `n > 0` | `a @ a @ ... @ a` | producto matricial repetido `n` veces |
| `n == 0` | `I` | matriz identidad del mismo tamaño |
| `n < 0` | `inv(a) @ ... @ inv(a)` | potencia de la inversa (`abs(n)` veces) |

```python
import numpy as np
A = np.array([[2, 0],
              [0, 3]])

np.linalg.matrix_power(A, 3)   # array([[8, 0], [0, 27]])
np.linalg.matrix_power(A, 0)   # array([[1, 0], [0, 1]])  → identidad
np.linalg.matrix_power(A, -1)  # array([[0.5, 0. ], [0. , 0.333...]])  → inversa
```

## No confundir con potencia elemento a elemento

```python
A ** 2                         # eleva cada elemento al cuadrado (Hadamard)
np.linalg.matrix_power(A, 2)   # A @ A  → producto matricial
```

Igual que con `@` frente a `*` (ver [[np.multiply]]), `matrix_power` actúa en el sentido del álgebra matricial, no posición a posición.

## Parámetros en detalle

| Parámetro | Tipo | Descripción |
|-----------|------|-------------|
| `a` | ndarray cuadrado `(..., M, M)` | Matriz a elevar. Admite pilas: los 2 últimos ejes deben ser cuadrados |
| `n` | int | Exponente entero (positivo, cero o negativo). No admite floats |

### Requisitos

- `a` debe ser **cuadrada** en sus dos últimos ejes (ver [[concepto_shape|shape]] `(..., M, M)`).
- Para `n < 0`, `a` debe ser **invertible** (no singular); internamente usa `np.linalg.inv`.
- `n` debe ser un **entero** de Python/NumPy; un float lanza error.

## Casos de uso

### Iteración de sistemas dinámicos / cadenas de Markov

```python
P = np.array([[0.9, 0.1],
              [0.5, 0.5]])
estado_t10 = np.linalg.matrix_power(P, 10)   # transición tras 10 pasos
```

### Identidad rápida de tamaño adecuado

```python
I = np.linalg.matrix_power(A, 0)   # identidad MxM coherente con A
```

## Buenas prácticas

1. Verifica que la matriz sea cuadrada antes de llamar.
2. Para `n` negativo, confirma que la matriz es invertible (evita matrices singulares).
3. Recuerda que `n=0` siempre devuelve la identidad, sea cual sea `a` (si es cuadrada).
4. No uses `**` esperando potencia matricial: eso es elemento a elemento.

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| `LinAlgError: Last 2 dimensions ... must be square` | matriz no cuadrada | usar `(M, M)` |
| `TypeError: exponent must be an integer` | `n` es float | pasar un entero |
| `LinAlgError: Singular matrix` | `n<0` con matriz no invertible | usar `n>=0` o matriz regular |
| Resultado elemento a elemento | se usó `**` | usar `matrix_power` |

## Notas relacionadas

- [[np.linalg.dot]]
- [[np.multiply]]
- [[np.linalg.matrix_transpose]]
