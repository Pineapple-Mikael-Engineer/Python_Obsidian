---
title: np.random.shuffle — Baraja un array in-place (devuelve None)
aliases:
  - shuffle
  - random.shuffle
  - np.random.shuffle
tags:
  - numpy
  - api/funcion
  - aleatorio
lib: numpy
mod: np.random
tipo: funcion
retorna: None
inplace: true
draft: false
---

# np.random.shuffle — baraja el array in-place

`np.random.shuffle` reordena los elementos de `x` **al azar y en su lugar**: muta el array original y devuelve `None`. Es la contraparte mutante de [[np.random.permutation]] (que devuelve una copia y deja el original intacto). Como toda operación in-place de NumPy, ahorra la copia en memoria pero **destruye el orden previo**. Al igual que `permutation`, solo reordena a lo largo del **primer eje**.

## La idea en una fórmula

`shuffle` aplica una permutación $\sigma$ del primer eje **sobre el propio buffer** de `x`. Para un array de [[concepto_shape|shape]] $(n_0, n_1, \dots, n_{k-1})$:

$$ x_{\,i,\;\dots} \;\leftarrow\; x_{\,\sigma(i),\;\dots} \qquad \sigma \in S_{n_0} $$

El shape **no cambia** (no se crea nada nuevo); lo que cambia es el contenido de `x` en el sitio. La flecha es de asignación (`←`), no de mapeo a una salida nueva: ahí está toda la diferencia con `permutation`.

## Firma de la función

```python
np.random.shuffle(
    x,   # ndarray: array MUTABLE a barajar in-place (no acepta int)
) -> None
```

## Valor de retorno

No devuelve nada (`None`). **Modifica `x` in-place**, reordenando sus elementos al azar a lo largo del **primer eje**.

| `x` | Efecto | Eje barajado |
|-----|--------|--------------|
| array 1D | reordena sus elementos in-place | único eje |
| array N-D | reordena las **filas** in-place | eje 0 |

```python
import numpy as np
np.random.seed(0)

a = np.array([10, 20, 30, 40])
np.random.shuffle(a)
a
# array([20, 40, 10, 30])   → 'a' quedó modificado
np.random.shuffle(a)         # ← devuelve None, no reasignes
```

> [!warning] No acepta un entero
> A diferencia de [[np.random.permutation]], `shuffle` **no** admite un `int`. `np.random.shuffle(5)` lanza `TypeError`: necesita un array existente que mutar. Para barajar `arange(n)` usa `np.random.permutation(n)`.

## Parámetros en detalle

### `x` — el array a barajar in-place

`ndarray` (de cualquier shape) que será **mutado**. Debe ser un array real y mutable: una lista de Python también se acepta (se baraja in-place como lista), pero lo idiomático es un `ndarray`. En N-D se barajan las **filas** (primer eje); el contenido interno de cada fila no se altera.

```python
M = np.arange(9).reshape(3, 3)
np.random.shuffle(M)
# las filas de M quedan reordenadas; M cambia in-place
```

## El eje y el caso N-D

Igual que `permutation`: **solo el eje 0**. Cada sub-tensor de shape $(n_1,\dots,n_{k-1})$ se mueve entero.

```python
T = np.arange(24).reshape(2, 3, 4)
np.random.shuffle(T)         # reordena los 2 bloques del eje 0, in-place
T.shape                      # (2, 3, 4)  → shape intacto

# ¿barajar TODOS los elementos? aplanar, barajar, devolver la forma:
A = np.arange(9).reshape(3, 3)
flat = A.ravel(); np.random.shuffle(flat)
A = flat.reshape(3, 3)

# ¿barajar por otro eje? la API moderna lo permite:
rng = np.random.default_rng(0)
rng.shuffle(A, axis=1)       # baraja dentro de cada fila, in-place
```

## Casos de uso

### Barajar un dataset sin copia extra

```python
np.random.shuffle(datos)             # ahorra memoria, no crea copia
```

### Mezclar features y etiquetas de forma coordinada

```python
idx = np.arange(len(X))
np.random.shuffle(idx)
X, y = X[idx], y[idx]                # mismo orden en ambos
```

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| `TypeError` con un entero | `shuffle` no acepta `int` | usar `np.random.permutation(n)` |
| `b = np.random.shuffle(a)` deja `b = None` | es in-place, devuelve `None` | leer `a` tras la llamada, no reasignar |
| Solo se mezclan las filas en una matriz | solo baraja el eje 0 | barajar `ravel()`, o `rng.shuffle(x, axis=...)` |
| Perdiste el orden original | mutación in-place | copiar antes, o usar [[np.random.permutation]] |
| Resultado no reproducible | sin semilla | [[np.random.seed]] antes, o `np.random.default_rng(s)` |

## Notas relacionadas

- [[np.random.permutation]] — la versión que devuelve copia (no muta)
- [[np.random.default_rng]] — `rng.shuffle` (con `axis`) en la API moderna
- [[np.random.seed]] — reproducibilidad del barajado
- [[concepto_shape]] — qué eje se reordena
- [[concepto_views_vs_copias]] — por qué aquí sí se destruye el original
