---
title: np.random.shuffle — Baraja un array in-place
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

# np.random.shuffle — Baraja el array in-place

## Firma de la función

```python
np.random.shuffle(
    x
) -> None
```

## Valor de retorno

No devuelve nada (`None`). **Modifica `x` in-place**, reordenando sus elementos al azar a lo largo del **primer eje**. Es la contraparte mutante de [[np.random.permutation]], que en cambio devuelve una copia y deja el original intacto.

| `x` | Efecto | Eje barajado |
|-----|--------|--------------|
| array 1D | reordena sus elementos in-place | único eje |
| array nD | reordena las **filas** in-place | eje 0 |

```python
import numpy as np
np.random.seed(0)

a = np.array([10, 20, 30, 40])
np.random.shuffle(a)
a
# array([20, 40, 10, 30])   → 'a' quedó modificado
```

> [!warning] No usar con enteros
> A diferencia de [[np.random.permutation]], `shuffle` **no acepta un entero**. `np.random.shuffle(5)` lanza `TypeError`. Necesita un array existente que modificar.

## Parámetros en detalle

### `x` — array a barajar in-place

Array (de cualquier [[concepto_shape|shape]]) que será **mutado**. En nD se barajan las filas (primer eje); el contenido interno de cada fila no se altera.

```python
M = np.arange(9).reshape(3, 3)
np.random.shuffle(M)
# las filas de M quedan reordenadas; M cambia in-place
```

## Casos de uso

### Barajar un dataset sin copia extra

```python
np.random.shuffle(datos)           # ahorra memoria, no crea copia
```

### Mezclar filas de features y etiquetas de forma coordinada

```python
idx = np.arange(len(X))
np.random.shuffle(idx)
X, y = X[idx], y[idx]              # mismo orden en ambos
```

## Buenas prácticas

1. Úsala cuando **no necesites** conservar el orden original (ahorra una copia).
2. Si necesitas mantener el original, usa [[np.random.permutation]].
3. Para barajar dos arrays en paralelo, baraja un índice y aplícalo a ambos.
4. En código nuevo prefiere `rng = np.random.default_rng(); rng.shuffle(x)`.

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| `TypeError` con un entero | `shuffle` no acepta `int` | Usar `np.random.permutation(n)` |
| Esperabas un valor de retorno | Devuelve `None` (es in-place) | Leer `x` tras la llamada |
| Solo se mezclan filas en una matriz | Solo baraja el eje 0 | Barajar `ravel()` o usar `rng.permuted(x, axis=...)` |
| Perdiste el original | Mutación in-place | Copiar antes o usar `permutation` |

## Notas relacionadas

- [[np.random.permutation]]
- [[np.random.seed]]
- [[np.random.default_rng]]
- [[concepto_shape]]
- [[concepto_views_vs_copias]]
