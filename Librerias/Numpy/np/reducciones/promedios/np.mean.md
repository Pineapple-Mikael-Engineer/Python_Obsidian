---
title: np.mean — Media aritmética
aliases:
  - mean
  - np.mean
  - media
  - promedio
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

# np.mean — Media aritmética

## Firma de la función

```python
np.mean(
    a,
    axis=None,
    dtype=None,
    out=None,
    keepdims=False,
    where=True
) -> ndarray | escalar
```

## Valor de retorno

Calcula la media aritmética (suma / cantidad) a lo largo del [[concepto_axis_parametro|eje]] indicado. Con `axis=None` promedia todo. El resultado siempre es flotante.

| Entrada | `axis` | Salida |
|---------|--------|--------|
| `(2, 3)` | `None` | escalar |
| `(2, 3)` | `0` | `(3,)` media por columna |
| `(2, 3)` | `1` | `(2,)` media por fila |

```python
import numpy as np
M = np.array([[1, 2, 3],
              [4, 5, 6]])
np.mean(M)          # 3.5
np.mean(M, axis=0)  # [2.5, 3.5, 4.5]
```

## Parámetros en detalle

### `axis`, `keepdims`, `where`

Como en [[np.sum]]: `axis` colapsa, `keepdims` mantiene el eje en tamaño 1, `where` promedia solo donde es `True`.

```python
arr = np.array([1, 2, np.nan, 4])
np.mean(arr, where=~np.isnan(arr))   # 2.333  → ignora el NaN
```

### `dtype` — precisión del cálculo

Con enteros o `float16`, fija `dtype=np.float64` para mayor precisión del acumulador (ver [[concepto_dtype]]).

## Casos de uso

### Promedio de columnas (features)

```python
datos = np.random.rand(100, 4)
medias = np.mean(datos, axis=0)   # media de cada columna
```

### Centrar datos (restar la media)

```python
centrado = datos - np.mean(datos, axis=0, keepdims=True)
```

## Buenas prácticas

1. Para datos con NaN, usa [[np.nanmean]] (o `where`).
2. Para una media **ponderada**, usa [[np.average]] con `weights`.
3. Usa `keepdims=True` al centrar/normalizar para que el broadcasting funcione.
4. La media es sensible a outliers; considera [[np.median]] si hay valores extremos.

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| Resultado NaN | hay NaN en la entrada | [[np.nanmean]] o `where` |
| Broadcasting falla al centrar | se perdió el eje | `keepdims=True` |
| Media engañosa | outliers | usar [[np.median]] |

## Limitaciones

- Sensible a valores extremos.
- Propaga NaN (usar variante `nan`).

## Notas relacionadas

- [[concepto_axis_parametro]]
- [[concepto_dtype]]
- [[np.average]]
- [[np.median]]
- [[np.std]]
- [[np.nanmean]]
