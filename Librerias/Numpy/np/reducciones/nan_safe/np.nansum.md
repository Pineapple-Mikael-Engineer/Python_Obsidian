---
title: np.nansum — Suma ignorando NaN
aliases:
  - nansum
  - np.nansum
tags:
  - numpy
  - api/funcion
  - reducciones

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

# np.nansum — Suma ignorando NaN

## Firma de la función

```python
np.nansum(
    a,
    axis=None,
    dtype=None,
    out=None,
    keepdims=False
) -> ndarray | escalar
```

## Valor de retorno

Idéntica a [[np.sum]] pero **tratando los `NaN` como 0**. Mientras `np.sum` propaga NaN (cualquier NaN hace que el total sea NaN), `nansum` los ignora.

| Entrada | `np.sum` | `np.nansum` |
|---------|----------|-------------|
| `[1, 2, nan, 4]` | `nan` | `7.0` |
| `[nan, nan]` | `nan` | `0.0` |

```python
import numpy as np
np.nansum([1, 2, np.nan, 4])   # 7.0
```

## Parámetros en detalle

### `axis`, `keepdims`, `dtype`

Igual que [[np.sum]]: `axis` colapsa el [[concepto_axis_parametro|eje]], `keepdims` lo conserva.

## Casos de uso

### Totales con datos faltantes

```python
ventas = np.array([[100, np.nan], [200, 300]])
np.nansum(ventas, axis=0)   # [300., 300.]
```

## Buenas prácticas

1. Útil cuando los NaN representan "dato faltante" y quieres sumar el resto.
2. Cuidado: un eje **todo NaN** devuelve `0`, no NaN (puede ocultar ausencia total de datos).
3. Para la media ignorando NaN, usa [[np.nanmean]].

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| `0` oculta "sin datos" | eje completamente NaN → suma 0 | comprobar el conteo de no-NaN aparte |

## Limitaciones

- Trata NaN como 0, lo que puede sesgar interpretaciones si todo es NaN.

## Notas relacionadas

- [[concepto_axis_parametro]]
- [[np.sum]]
- [[np.nanmean]]
- [[np.nanprod]]
