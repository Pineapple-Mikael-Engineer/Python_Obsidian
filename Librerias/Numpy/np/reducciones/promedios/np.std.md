---
title: np.std — Desviación estándar
aliases:
  - std
  - np.std
  - desviacion estandar
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
  - concepto_dtype

draft: false
---

# np.std — Desviación estándar

## Firma de la función

```python
np.std(
    a,
    axis=None,
    dtype=None,
    out=None,
    ddof=0,
    keepdims=False,
    where=True
) -> ndarray | escalar
```

## Valor de retorno

Mide la dispersión de los datos respecto a su [[np.mean|media]]: la raíz cuadrada de la [[np.var|varianza]]. Está en las **mismas unidades** que los datos.

| Entrada | Salida |
|---------|--------|
| `[2, 4, 4, 4, 5, 5, 7, 9]` | `2.0` |
| `[5, 5, 5, 5]` | `0.0` (sin dispersión) |

```python
import numpy as np
np.std([2, 4, 4, 4, 5, 5, 7, 9])   # 2.0
```

## El parámetro clave: `ddof`

`ddof` (delta degrees of freedom) decide entre desviación **poblacional** y **muestral**:

| `ddof` | Divisor | Uso |
|--------|---------|-----|
| `0` (por defecto) | `N` | desviación **poblacional** |
| `1` | `N - 1` | desviación **muestral** (corrección de Bessel) |

```python
datos = np.array([2.0, 4.0, 6.0])
np.std(datos)          # 1.633  (ddof=0, poblacional)
np.std(datos, ddof=1)  # 2.0    (ddof=1, muestral)
```

> Para estimar la dispersión de una población **a partir de una muestra**, usa `ddof=1`.

## Parámetros en detalle

### `axis`, `keepdims`, `where`

Como en [[np.mean]]: `axis` colapsa el [[concepto_axis_parametro|eje]], `keepdims` lo conserva, `where` filtra.

### `dtype` — precisión

Fija `np.float64` con datos enteros o `float16` para no perder precisión (ver [[concepto_dtype]]).

## Casos de uso

### Estandarizar datos (z-score)

```python
z = (datos - np.mean(datos, axis=0, keepdims=True)) \
    / np.std(datos, axis=0, keepdims=True)
```

### Dispersión por feature

```python
desviaciones = np.std(matriz, axis=0)
```

## Buenas prácticas

1. Elige `ddof` conscientemente: `1` para muestras, `0` para poblaciones completas.
2. Para z-scores, usa `keepdims=True` para que el broadcasting funcione.
3. Con NaN, usa [[np.nanstd]].
4. Si necesitas la varianza (unidades al cuadrado), usa [[np.var]].

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| Valor distinto al esperado | `ddof` por defecto es 0 (poblacional) | usar `ddof=1` para muestral |
| Resultado NaN | hay NaN | [[np.nanstd]] |
| División por cero al estandarizar | std = 0 (datos constantes) | manejar el caso aparte |

## Limitaciones

- Sensible a outliers (al basarse en la media).
- Propaga NaN.

## Notas relacionadas

- [[concepto_axis_parametro]]
- [[np.var]]
- [[np.mean]]
- [[np.nanstd]]
