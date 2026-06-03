---
title: np.random.random_integers — Enteros en [low, high] (DEPRECADA)
aliases:
  - random_integers
  - random.random_integers
  - np.random.random_integers
tags:
  - numpy
  - api/funcion
  - aleatorio
lib: numpy
mod: np.random
tipo: funcion
retorna: ndarray o int
inplace: false
draft: false
---

# np.random.random_integers — Enteros en [low, high] (DEPRECADA)

> ⚠️ **DEPRECADA.** Usa [[np.random.randint]] en su lugar.

Genera enteros aleatorios uniformes en el intervalo **cerrado** `[low, high]`, donde el límite superior **SÍ se incluye** (a diferencia de `randint`, que lo excluye). Está deprecada desde NumPy 1.11 y se mantiene solo por compatibilidad; el código nuevo no debería usarla.

## Firma de la función

```python
np.random.random_integers(
    low,
    high=None,
    size=None
) -> ndarray | int
```

## Valor de retorno

Devuelve un entero o un [[concepto_ndarray|ndarray]] con el [[concepto_shape|shape]] de `size`. La diferencia clave con `randint` es la **inclusión del tope**.

| Llamada | Rango efectivo | Retorno |
|---------|----------------|---------|
| `np.random.random_integers(6)` | `[1, 6]` | un `int` en 1..6 |
| `np.random.random_integers(1, 6)` | `[1, 6]` | un `int` en 1..6 |
| `np.random.random_integers(1, 6, size=4)` | `[1, 6]` | `ndarray` de 4 enteros |

```python
import numpy as np
np.random.random_integers(1, 6, size=5)
# DeprecationWarning: This function is deprecated. Please call randint(1, 6 + 1) instead
# array([6, 1, 6, 3, 4])   # el 6 SÍ puede salir
```

## Parámetros en detalle

### `low` — límite inferior (o superior si `high` es None)

Con un solo argumento el rango es `[1, low]` (¡empieza en 1, no en 0!). Con dos, `low` es el inicio inclusivo.

```python
np.random.random_integers(4)      # [1, 4]  → 1,2,3,4
np.random.random_integers(2, 4)   # [2, 4]  → 2,3,4
```

### `high` — límite superior INCLUIDO

Al contrario que en [[np.random.randint]], aquí `high` es alcanzable. Esta es precisamente la fuente de confusión que motivó su deprecación.

### `size` — forma de la salida

Entero o tupla; define el [[concepto_shape|shape]]. `None` devuelve escalar.

## Casos de uso

> En código nuevo **no la uses**. Migra así:

```python
# Antiguo (deprecado):
np.random.random_integers(1, 6, size=10)

# Equivalente recomendado (high + 1 para reincluir el tope):
np.random.randint(1, 6 + 1, size=10)
```

## Buenas prácticas

1. **No emplear en código nuevo.** Sustituir por [[np.random.randint]] con `high + 1`.
2. Si aparece un `DeprecationWarning`, es esta función: migra la llamada.
3. Recuerda que con un único argumento el rango empieza en **1**, no en 0.

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| `DeprecationWarning` | la función está deprecada | migrar a `randint(low, high+1)` |
| Rango empieza en 1 | con 1 arg el inicio es 1 | pasar `low` explícito |
| Resultados con un valor de más | `high` está incluido aquí | al migrar a `randint` recordar el `+1` |

## Notas relacionadas

- [[concepto_shape]]
- [[np.random.randint]]
- [[np.random.choice]]
- [[np.random.binomial]]
