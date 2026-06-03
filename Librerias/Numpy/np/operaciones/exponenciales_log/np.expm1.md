---
title: np.expm1 — e^x − 1 con precisión cerca de 0 (ufunc)
aliases:
  - expm1
  - np.expm1
tags:
  - numpy
  - api/funcion
  - transformaciones

# --- Clasificación ---
lib: numpy
mod: np
tipo: funcion

# --- Comportamiento ---
retorna: ndarray
inplace: false

# --- Dependencias ---
requiere:
  - concepto_ufuncs

draft: false
---

# np.expm1 — e^x − 1 con precisión cerca de 0 (ufunc)

## Firma de la función

```python
np.expm1(x, /, out=None, *, where=True, dtype=None) -> ndarray
```

## Valor de retorno

Calcula `e^x − 1` elemento a elemento, pero con **precisión numérica** para `x` cercano a 0, donde `np.exp(x) - 1` perdería dígitos significativos (cancelación catastrófica).

| `x` | `np.exp(x)-1` | `np.expm1(x)` |
|-----|---------------|---------------|
| `1e-10` | `~0` (impreciso) | `1.0000e-10` (correcto) |

```python
import numpy as np
np.expm1(1e-10)        # 1.00000000005e-10
np.exp(1e-10) - 1      # 1.000000082e-10  → menos preciso
```

## Parámetros en detalle

`x` cualquier real; `out`, `where`, `dtype` como toda ufunc (ver [[np.add]]).

## Casos de uso

### Interés compuesto / tasas pequeñas

```python
crecimiento = np.expm1(tasa)   # preciso para tasas diminutas
```

## Buenas prácticas

1. Úsala siempre que necesites `exp(x) - 1` con `x` pequeño.
2. Su pareja es [[np.log1p]] (`log(1+x)`), para el camino inverso.

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| Pérdida de precisión | usar `np.exp(x) - 1` con `x→0` | usar `np.expm1` |

## Limitaciones

- Mismo overflow que [[np.exp]] para `x` grande.

## Notas relacionadas

- [[concepto_ufuncs]]
- [[np.exp]]
- [[np.log]]
