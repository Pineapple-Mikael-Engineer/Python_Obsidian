---
title: np.min — Valor mínimo a lo largo de un eje
aliases:
  - min
  - np.min
  - amin
  - minimo
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

# np.min — Valor mínimo a lo largo de un eje

## Firma de la función

```python
np.min(
    a,
    axis=None,
    out=None,
    keepdims=False,
    initial=<sin valor>,
    where=True
) -> ndarray | escalar
```

`np.min` es un alias de `np.amin`. Es la contraparte de [[np.max]].

## Valor de retorno

Devuelve el valor **mínimo** a lo largo del [[concepto_axis_parametro|eje]] indicado. Con `axis=None`, el mínimo global.

| Entrada | `axis` | Salida |
|---------|--------|--------|
| `(2, 3)` | `None` | escalar |
| `(2, 3)` | `0` | `(3,)` mínimo por columna |
| `(2, 3)` | `1` | `(2,)` mínimo por fila |

```python
import numpy as np
M = np.array([[1, 9, 3],
              [7, 2, 8]])
np.min(M)          # 1
np.min(M, axis=1)  # [1, 2]
```

## min vs minimum vs argmin

| Función | Qué hace |
|---------|----------|
| `np.min` | el valor mínimo (reduce un eje) |
| `np.minimum` | mínimo **elemento a elemento** entre dos arrays |
| [[np.argmin]] | la **posición** del mínimo |

## Parámetros en detalle

### `axis`, `keepdims`, `where`, `initial`

Idénticos a [[np.max]].

## Casos de uso

### Rango de los datos

```python
rango = np.max(a) - np.min(a)   # o np.ptp(a)
```

### Suelo por columna

```python
minimos = np.min(matriz, axis=0)
```

## Buenas prácticas

1. Para la **posición** del mínimo, usa [[np.argmin]].
2. Con NaN, usa [[np.nanmin]].
3. Para comparar dos arrays par a par, usa `np.minimum`.

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| Resultado NaN | hay NaN | [[np.nanmin]] |
| Confundir con índice | se quería la posición | [[np.argmin]] |
| array vacío | sin elementos | pasar `initial` |

## Limitaciones

- Propaga NaN; devuelve valor, no ubicación.

## Notas relacionadas

- [[concepto_axis_parametro]]
- [[np.max]]
- [[np.argmin]]
- [[np.ptp]]
- [[np.nanmin]]
