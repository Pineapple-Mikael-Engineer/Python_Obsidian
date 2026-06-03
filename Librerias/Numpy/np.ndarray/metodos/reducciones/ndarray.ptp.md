---
title: ndarray.ptp — Rango (máximo menos mínimo) a lo largo de un eje
aliases:
  - ptp
  - ndarray.ptp
tags:
  - numpy
  - api/metodo
  - reducciones
lib: numpy
obj: ndarray
tipo: metodo
retorna: escalar o ndarray
inplace: false
draft: false
---

# ndarray.ptp — Rango (máximo menos mínimo) a lo largo de un eje

## Firma del método

```python
ndarray.ptp(
    axis=None,
    out=None,
    keepdims=False
) -> escalar | ndarray
```

## Valor de retorno

| Entrada (`self`) | `axis` | Retorno |
|------------------|--------|---------|
| `[3, 1, 9, 2]` | `None` | `8` (`9 - 1`) |
| shape `(2, 3)` | `0` | rango por columna → `(3,)` |
| shape `(2, 3)` | `1` | rango por fila → `(2,)` |

`ptp` significa **"peak to peak"**: equivale a `self.max(...) - self.min(...)` a lo largo del eje. Con `axis=None` devuelve un escalar.

```python
import numpy as np
a = np.array([3, 1, 9, 2])
a.ptp()   # 8
```

## Equivalencia con np.ptp

`a.ptp(...)` es la forma "bound" de [[np.ptp]]: `np.ptp(a, ...)`. Misma semántica de `axis` y `keepdims`, idéntico resultado. La forma de método encadena de forma fluida; la funcional acepta como primer argumento cualquier `array_like` (listas), no solo un `ndarray` ya construido.

## Parámetros en detalle

### `axis` — eje de reducción

`None` opera sobre `self` aplanado. Con entero (o tupla), colapsa ese eje y deja los demás.

```python
M = np.array([[1, 9, 3],
              [7, 2, 8]])
M.ptp(axis=1)   # [8, 6]   → (9-1, 8-2)
```

### `keepdims` — conservar dimensiones

Con `True`, el eje reducido se mantiene con tamaño 1 para facilitar el broadcasting posterior.

### Cuidado con enteros sin signo

Como internamente resta, con dtype entero sin signo (`uint8`...) un resultado negativo puede desbordar y dar un valor enorme. Convierte a un tipo con signo antes de usar `ptp`.

## Casos de uso

### Amplitud de una señal

```python
señal = np.array([0.2, -0.5, 0.9, 0.1])
señal.ptp()   # 1.4   → amplitud pico a pico
```

### Rango de cada característica (feature scaling)

```python
X = np.random.rand(100, 4)
rangos = X.ptp(axis=0)   # rango por columna → shape (4,)
X / rangos               # normalización por rango (broadcasting)
```

## Buenas prácticas

1. Para dispersión robusta a outliers, prefiere desviación estándar o IQR; `ptp` solo ve los extremos.
2. Convierte a dtype con signo o a float si hay riesgo de desbordamiento con enteros sin signo.
3. Usa `keepdims=True` cuando vayas a dividir el array original por el rango.

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| Valor enorme inesperado | desbordamiento con `uint` al restar | castear a `int`/`float` |
| Sensible a un único outlier | mide solo los extremos | usar std o IQR |
| `(n,)` no alinea con `self` | el eje se colapsó | `keepdims=True` |

## Notas relacionadas

- [[np.ptp]]
- [[concepto_axis_parametro]]
- [[ndarray.max]]
- [[ndarray.min]]
