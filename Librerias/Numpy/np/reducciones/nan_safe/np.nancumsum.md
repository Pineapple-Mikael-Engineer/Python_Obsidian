---
title: np.nancumsum — Suma acumulada ignorando NaN
aliases:
  - nancumsum
  - np.nancumsum
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

draft: false
---

# np.nancumsum — Suma acumulada ignorando NaN

## Firma de la función

```python
np.nancumsum(
    a,
    axis=None,
    dtype=None,
    out=None
) -> ndarray
```

## Valor de retorno

Versión de [[np.cumsum]] que **trata los `NaN` como 0**: la acumulación no se "rompe" al encontrar un NaN, simplemente no aporta en esa posición.

| Entrada | `np.cumsum` | `np.nancumsum` |
|---------|-------------|----------------|
| `[1, nan, 3]` | `[1, nan, nan]` | `[1, 1, 4]` |

```python
import numpy as np
np.nancumsum([1, np.nan, 3])   # array([1., 1., 4.])
```

## Parámetros en detalle

Igual que [[np.cumsum]]: `axis` define el eje de acumulación (ver [[concepto_axis_parametro]]); `None` aplana.

## Casos de uso

### Saldo acumulado tolerando huecos

```python
movs = np.array([100, np.nan, -30, 50])
np.nancumsum(movs)   # [100, 100, 70, 120]
```

## Buenas prácticas

1. Mantiene la longitud (como `cumsum`); el NaN se trata como 0 en la suma corriente.
2. Para el total directo, [[np.nansum]].

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| Esperar que el hueco "congele" la serie | NaN cuenta como 0 | revisar si querías otra semántica |

## Limitaciones

- En la posición del NaN, el valor mostrado es la suma corriente previa (NaN tratado como 0).

## Notas relacionadas

- [[concepto_axis_parametro]]
- [[np.cumsum]]
- [[np.nansum]]
- [[np.nancumprod]]
