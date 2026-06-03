---
title: np.cumprod — Producto acumulado
aliases:
  - cumprod
  - np.cumprod
  - producto acumulado
tags:
  - numpy
  - api/funcion
  - reducciones

# --- Clasificación ---
lib: numpy
mod: np
tipo: funcion

# --- Comportamiento ---
retorna: ndarray
inplace: false

# --- Dependencias ---
requiere:
  - concepto_axis_parametro
  - concepto_dtype

draft: false
---

# np.cumprod — Producto acumulado

## Firma de la función

```python
np.cumprod(
    a,
    axis=None,
    dtype=None,
    out=None
) -> ndarray
```

## Valor de retorno

Devuelve un array del mismo tamaño que `a` donde cada posición es el producto de todos los elementos anteriores (incluido él). Es la versión multiplicativa de [[np.cumsum]].

| Entrada | `axis` | Salida |
|---------|--------|--------|
| `[1, 2, 3, 4]` | `None` | `[1, 2, 6, 24]` |
| `(2, 3)` | `1` | producto acumulado por fila |

```python
import numpy as np
np.cumprod([1, 2, 3, 4])   # array([1, 2, 6, 24])
```

## Parámetros en detalle

### `axis` — eje de acumulación

`None` aplana; entero acumula a lo largo de ese [[concepto_axis_parametro|eje]].

### `dtype` — acumulador

El riesgo de **overflow** es alto (crecimiento multiplicativo); usa `dtype` amplio o flotante. Ver [[concepto_dtype]].

## Casos de uso

### Factor de capitalización compuesta

```python
tasas = np.array([1.05, 1.03, 1.04])   # +5%, +3%, +4%
crecimiento = np.cumprod(tasas)        # [1.05, 1.0815, 1.1248]
```

### Factoriales parciales

```python
np.cumprod(np.arange(1, 6))   # [1, 2, 6, 24, 120]
```

## Buenas prácticas

1. Vigila el overflow más que en `cumsum`.
2. Para ignorar NaN, usa [[np.nancumprod]].
3. Para suma acumulada, [[np.cumsum]].

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| Overflow | crecimiento multiplicativo | `dtype=np.float64` |
| Todo 0 tras un 0 | un factor es 0 anula el resto | revisar datos |

## Limitaciones

- Muy sensible al overflow; conserva el tamaño (no reduce).

## Notas relacionadas

- [[concepto_axis_parametro]]
- [[concepto_dtype]]
- [[np.cumsum]]
- [[np.prod]]
