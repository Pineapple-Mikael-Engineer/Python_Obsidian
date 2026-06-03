---
title: np.average — Media (opcionalmente ponderada)
aliases:
  - average
  - np.average
  - media ponderada
tags:
  - numpy
  - api/funcion
  - estadistica

# --- Clasificación ---
lib: numpy
mod: np
tipo: funcion

# --- Comportamiento ---
retorna: ndarray o escalar
inplace: false

# --- Dependencias ---
requiere:
  - concepto_axis_parametro

draft: false
---

# np.average — Media (opcionalmente ponderada)

## Firma de la función

```python
np.average(
    a,
    axis=None,
    weights=None,
    returned=False,
    keepdims=False
) -> ndarray | escalar
```

## Valor de retorno

Calcula la media. Sin `weights` equivale a [[np.mean]]; con `weights` calcula la **media ponderada** `sum(a*w) / sum(w)`.

| Llamada | Resultado |
|---------|-----------|
| `np.average([1, 2, 3])` | `2.0` |
| `np.average([1, 2, 3], weights=[1, 1, 4])` | `2.5` |

```python
import numpy as np
notas = np.array([4.0, 6.0, 8.0])
pesos = np.array([1, 1, 2])         # el último vale doble
np.average(notas, weights=pesos)    # 6.5
```

## mean vs average

| | [[np.mean]] | `np.average` |
|--|------------|--------------|
| Ponderación | no | sí (`weights`) |
| `where` condicional | sí | no |
| Devuelve suma de pesos | no | sí (`returned=True`) |

## Parámetros en detalle

### `weights` — pesos

Array de la misma forma que `a` (o compatible con el eje). Mayor peso = más influencia.

### `returned` — devolver la suma de pesos

Si `True`, retorna `(media, suma_de_pesos)`.

```python
media, total_pesos = np.average(notas, weights=pesos, returned=True)
```

## Casos de uso

### Promedio ponderado por importancia

```python
precios = np.array([10.0, 20.0, 30.0])
cantidades = np.array([100, 50, 10])      # ponderar por volumen
precio_medio = np.average(precios, weights=cantidades)
```

## Buenas prácticas

1. Si no necesitas pesos, [[np.mean]] es más directo (y admite `where`).
2. Los `weights` no necesitan sumar 1: se normalizan internamente.
3. Para datos con NaN, enmascara antes (no tiene parámetro `nan`).

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| `Length of weights not compatible` | shape de `weights` no alinea | igualar al eje promediado |
| `Weights sum to zero` | pesos suman 0 | usar pesos válidos |

## Limitaciones

- No tiene variante `nan` ni parámetro `where`.

## Notas relacionadas

- [[concepto_axis_parametro]]
- [[np.mean]]
- [[np.median]]
