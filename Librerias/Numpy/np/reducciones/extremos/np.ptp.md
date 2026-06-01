---
title: np.ptp — Rango (peak to peak, max − min)
aliases:
  - ptp
  - np.ptp
  - rango
  - peak to peak
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

# np.ptp — Rango (peak to peak, max − min)

## Firma de la función

```python
np.ptp(
    a,
    axis=None,
    out=None,
    keepdims=False
) -> ndarray | escalar
```

## Valor de retorno

Devuelve el **rango**: la diferencia entre el máximo y el mínimo (`max - min`) a lo largo del [[concepto_axis_parametro|eje]]. El nombre viene de "peak to peak".

| Entrada | `axis` | Salida |
|---------|--------|--------|
| `[1, 5, 2, 8]` | `None` | `7` (8 − 1) |
| `(2, 3)` | `0` | rango por columna |

```python
import numpy as np
np.ptp([1, 5, 2, 8])   # 7
M = np.array([[1, 9], [7, 2]])
np.ptp(M, axis=1)      # [8, 5]
```

## Parámetros en detalle

### `axis`, `keepdims`

Como en [[np.max]] / [[np.min]].

## Casos de uso

### Amplitud de una señal

```python
amplitud = np.ptp(onda)
```

### Detectar columnas con poca variación

```python
rangos = np.ptp(datos, axis=0)
casi_constantes = rangos < 1e-6
```

## Buenas prácticas

1. Equivale a `np.max(a, axis) - np.min(a, axis)` pero más conciso.
2. Cuidado con enteros sin signo: `max - min` puede desbordar (`uint8`).
3. No tiene variante `nan`: enmascara los NaN antes si los hay.

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| Resultado absurdo con `uint` | overflow en la resta | convertir a `int`/`float` antes |
| NaN | propaga NaN | filtrar NaN previamente |

## Limitaciones

- Sin variante `nan`.
- Sensible a outliers (depende de los extremos).

## Notas relacionadas

- [[concepto_axis_parametro]]
- [[np.max]]
- [[np.min]]
