---
title: np.random.uniform — Uniforme en un rango arbitrario [low, high)
aliases:
  - uniform
  - random.uniform
  - np.random.uniform
tags:
  - numpy
  - api/funcion
  - aleatorio
lib: numpy
mod: np.random
tipo: funcion
retorna: ndarray o float
inplace: false
draft: false
---

# np.random.uniform — Uniforme en un rango arbitrario [low, high)

## Firma de la función

```python
np.random.uniform(low=0.0, high=1.0, size=None) -> ndarray
# low  = límite inferior (incluido)
# high = límite superior (excluido)
# size = entero o TUPLA (shape del resultado)
```

Genera valores con distribución **uniforme continua en `[low, high)`**. A diferencia de [[np.random.random]] y [[np.random.rand]] (que solo cubren `[0, 1)`), `uniform` permite un **rango arbitrario** sin reescalar a mano. El `size` es una tupla, como en `random`.

## Valor de retorno

| Entrada | Retorno | Ejemplo |
|---------|---------|---------|
| `uniform()` | `float` en `[0, 1)` | `0.547...` |
| `uniform(10, 20)` | `float` en `[10, 20)` | `13.82...` |
| `uniform(-1, 1, 3)` | ndarray `(3,)` en `[-1, 1)` | `[-0.4, 0.9, 0.1]` |
| `uniform(0, 5, (2, 3))` | ndarray `(2, 3)` en `[0, 5)` | matriz 2×3 |

```python
import numpy as np
np.random.uniform(-1, 1, (2, 3))
# array([[ 0.41, -0.72,  0.09],
#        [-0.30,  0.86, -0.55]])
```

## Parámetros en detalle

### `low` — límite inferior (incluido)

Valor mínimo posible. Por defecto `0.0`. Puede ser un array para hacer [[concepto_broadcasting|broadcasting]] con `high`.

```python
np.random.uniform(low=5)        # [5, 1)?  → ojo: high por defecto es 1.0
np.random.uniform(low=5, high=10)
```

### `high` — límite superior (excluido)

Valor máximo (no alcanzable). Por defecto `1.0`. Si `high < low`, NumPy no lanza error: simplemente invierte el rango efectivo.

```python
np.random.uniform(0, 100, 4)    # 4 valores en [0, 100)
```

### `size` — el shape como tupla

Entero (1D) o **tupla** para el [[concepto_shape|shape]] nD. Toma una tupla (como `random`), no dimensiones sueltas (como `rand`).

```python
np.random.uniform(0, 1, 5)        # (5,)
np.random.uniform(0, 1, (3, 4))   # (3, 4)
```

## Casos de uso

### Inicializar pesos en un rango simétrico

```python
W = np.random.uniform(-0.5, 0.5, (4, 4))   # pesos centrados en 0
```

### Coordenadas aleatorias dentro de un dominio

```python
x = np.random.uniform(0, 100, 1000)   # x en [0, 100)
y = np.random.uniform(0, 50, 1000)    # y en [0, 50)
```

### Broadcasting de límites por columna

```python
lows  = np.array([0, 10, 100])
highs = np.array([1, 20, 200])
np.random.uniform(lows, highs)   # un valor por cada par (low, high)
```

## Buenas prácticas

1. Usa `uniform` siempre que necesites un rango distinto de `[0, 1)`; evita el patrón `low + (high-low)*rand(...)`.
2. Recuerda que `high` queda **excluido** (intervalo semiabierto).
3. El `size` es **tupla** (como `random`), no dimensiones sueltas (como `rand`).
4. Para enteros uniformes usa `np.random.randint`, no `uniform`.
5. Fija semilla (`np.random.seed`) o usa un `Generator` moderno para reproducibilidad.

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| Rango inesperado con `uniform(5)` | `high` sigue siendo `1.0` por defecto | pasar `high` explícito |
| `TypeError` con `size` suelto | `uniform(0, 1, 2, 3)` se lee mal | usar tupla: `uniform(0, 1, (2, 3))` |
| Querías enteros | `uniform` siempre da floats | usar `np.random.randint` |
| `high` nunca aparece | intervalo semiabierto `[low, high)` | es el comportamiento esperado |

## Notas relacionadas

- [[np.random.random]]
- [[np.random.rand]]
- [[concepto_shape]]
