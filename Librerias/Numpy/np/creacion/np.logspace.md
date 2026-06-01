---
title: np.logspace — Puntos espaciados logarítmicamente
aliases:
  - logspace
  - np.logspace
tags:
  - numpy
  - api/funcion
  - creacion

# --- Clasificación ---
lib: numpy
mod: np
tipo: funcion

# --- Comportamiento ---
retorna: ndarray
inplace: false

# --- Dependencias ---
requiere:
  - concepto_shape
  - concepto_dtype

draft: false
---

# np.logspace — Puntos espaciados logarítmicamente

## Firma de la función

```python
np.logspace(
    start,
    stop,
    num=50,
    endpoint=True,
    base=10.0,
    dtype=None,
    axis=0
) -> ndarray
```

## Valor de retorno

Devuelve un [[concepto_ndarray|ndarray]] 1D de `num` valores espaciados uniformemente en **escala logarítmica**. Equivale a `base ** np.linspace(start, stop, num)`: los **exponentes** son lineales, los valores crecen geométricamente.

| Llamada | Resultado |
|---------|-----------|
| `np.logspace(0, 3, 4)` | `[1., 10., 100., 1000.]` |
| `np.logspace(0, 2, 3)` | `[1., 10., 100.]` |
| `np.logspace(0, 9, 10, base=2)` | potencias de 2: `[1, 2, 4, ..., 512]` |

```python
import numpy as np
np.logspace(0, 3, 4)   # array([   1.,   10.,  100., 1000.])
```

## Relación con linspace

> `start` y `stop` son **exponentes**, no valores. `logspace(a, b)` == `base ** linspace(a, b)`.

```python
np.logspace(0, 3, 4)              # [1, 10, 100, 1000]
10 ** np.linspace(0, 3, 4)        # idéntico
```

## Parámetros en detalle

### `start`, `stop` — exponentes

El rango va de `base**start` a `base**stop`. Para empezar en 1 usa `start=0`.

### `num` — cantidad de puntos

Entero ≥ 0. Define el [[concepto_shape|shape]] `(num,)`.

### `base` — base del logaritmo

Por defecto `10.0`. Usa `2` para escalas binarias, `np.e` para naturales.

### `endpoint` — incluir el extremo

Como en [[np.linspace]]: `True` incluye `base**stop`.

## Casos de uso

### Eje X logarítmico para gráficas

```python
frecuencias = np.logspace(1, 5, 100)   # 10 Hz a 100 kHz
```

### Barrido de hiperparámetros (learning rate)

```python
lrs = np.logspace(-5, -1, 5)   # [1e-5, 1e-4, 1e-3, 1e-2, 1e-1]
```

## Buenas prácticas

1. Recuerda que los argumentos son **exponentes**, no los valores finales.
2. Para magnitudes que abarcan varios órdenes (frecuencias, concentraciones), es más natural que [[np.linspace]].
3. Si ya tienes los valores extremos (no los exponentes), usa `np.geomspace(inicio, fin, num)`.

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| Valores enormes/diminutos inesperados | se pasaron valores en vez de exponentes | usar `np.geomspace` o `log10` de los extremos |
| Base equivocada | `base=10` por defecto | indicar `base` |

## Limitaciones

- Espaciado solo logarítmico; para lineal usa [[np.linspace]].
- Trabaja con exponentes, lo que confunde si esperas los valores directos.

## Notas relacionadas

- [[concepto_shape]]
- [[np.linspace]]
- [[np.arange]]
