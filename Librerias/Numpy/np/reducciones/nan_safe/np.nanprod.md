---
title: np.nanprod — Producto ignorando NaN
aliases:
  - nanprod
  - np.nanprod
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

# np.nanprod — Producto ignorando NaN

## Firma de la función

```python
np.nanprod(
    a,
    axis=None,
    dtype=None,
    out=None,
    keepdims=False
) -> ndarray | escalar
```

## Valor de retorno

Versión de [[np.prod]] que **trata los `NaN` como 1** (elemento neutro del producto), en lugar de propagarlos.

| Entrada | `np.prod` | `np.nanprod` |
|---------|-----------|--------------|
| `[1, 2, nan, 4]` | `nan` | `8.0` |
| `[nan, nan]` | `nan` | `1.0` |

```python
import numpy as np
np.nanprod([1, 2, np.nan, 4])   # 8.0
```

## Parámetros en detalle

Idénticos a [[np.prod]]: `axis` colapsa el [[concepto_axis_parametro|eje]], `dtype` controla el acumulador (vigilar overflow), `keepdims` conserva el eje.

## Casos de uso

### Producto de factores con huecos

```python
factores = np.array([1.05, np.nan, 1.03])
np.nanprod(factores)   # 1.0815  (ignora el NaN)
```

## Buenas prácticas

1. Un eje todo-NaN devuelve `1`, no NaN: puede ocultar ausencia de datos.
2. Vigila el **overflow** igual que en [[np.prod]].

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| `1` oculta "sin datos" | eje todo NaN → producto 1 | verificar conteo de no-NaN |
| Overflow | crecimiento multiplicativo | `dtype` amplio |

## Limitaciones

- Trata NaN como 1, lo que puede sesgar si todo es NaN.

## Notas relacionadas

- [[concepto_axis_parametro]]
- [[np.prod]]
- [[np.nansum]]
