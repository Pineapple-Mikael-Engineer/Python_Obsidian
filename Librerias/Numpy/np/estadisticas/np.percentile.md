---
title: np.percentile — Percentil de los datos
aliases:
  - percentile
  - np.percentile
  - percentil
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

# np.percentile — Percentil de los datos

## Firma de la función

```python
np.percentile(
    a,
    q,
    axis=None,
    out=None,
    method='linear',
    keepdims=False
) -> ndarray | escalar
```

## Valor de retorno

Devuelve el valor por debajo del cual cae el `q`% de los datos. El percentil 50 es la [[np.median|mediana]]. `q` puede ser un valor o una lista (devuelve un array).

| `q` | Significado |
|-----|-------------|
| `0` | mínimo |
| `25` | primer cuartil (Q1) |
| `50` | mediana |
| `75` | tercer cuartil (Q3) |
| `100` | máximo |

```python
import numpy as np
datos = np.arange(1, 101)        # 1..100
np.percentile(datos, 50)         # 50.5
np.percentile(datos, [25, 75])   # [25.75, 75.25]
```

## Parámetros en detalle

### `a` — datos

Array de entrada.

### `q` — percentil(es)

Escalar o secuencia en `[0, 100]`.

### `axis` — eje

Como en las reducciones (ver [[concepto_axis_parametro]]); `None` aplana.

### `method` — interpolación entre puntos

Cuando el percentil cae entre dos datos, define cómo interpolar (`'linear'` por defecto, `'lower'`, `'higher'`, `'nearest'`, `'midpoint'`).

## Casos de uso

### Rango intercuartílico (IQR)

```python
q1, q3 = np.percentile(datos, [25, 75])
iqr = q3 - q1
```

### Recortar outliers por percentiles

```python
lo, hi = np.percentile(datos, [1, 99])
np.clip(datos, lo, hi)
```

## Buenas prácticas

1. Pasa una **lista** de `q` para obtener varios percentiles en una llamada.
2. Para cuantiles en `[0, 1]` en vez de `[0, 100]`, usa `np.quantile`.
3. Con NaN, usa `np.nanpercentile`.

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| `q` fuera de rango | se pasó `[0,1]` en vez de `[0,100]` | usar `np.quantile` o escalar a 0-100 |
| Resultado NaN | hay NaN | `np.nanpercentile` |

## Limitaciones

- `q` en escala 0-100 (no 0-1); propaga NaN.

## Notas relacionadas

- [[concepto_axis_parametro]]
- [[np.median]]
- [[np.histogram]]
- [[np.digitize]]
