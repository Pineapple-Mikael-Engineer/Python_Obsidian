---
title: np.max — Valor máximo a lo largo de un eje
aliases:
  - max
  - np.max
  - amax
  - maximo
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

# np.max — Valor máximo a lo largo de un eje

## Firma de la función

```python
np.max(
    a,
    axis=None,
    out=None,
    keepdims=False,
    initial=<sin valor>,
    where=True
) -> ndarray | escalar
```

`np.max` es un alias de `np.amax`.

## Valor de retorno

Devuelve el valor **máximo** a lo largo del [[concepto_axis_parametro|eje]] indicado. Con `axis=None` devuelve el máximo global.

| Entrada | `axis` | Salida |
|---------|--------|--------|
| `(2, 3)` | `None` | escalar |
| `(2, 3)` | `0` | `(3,)` máximo por columna |
| `(2, 3)` | `1` | `(2,)` máximo por fila |

```python
import numpy as np
M = np.array([[1, 9, 3],
              [7, 2, 8]])
np.max(M)          # 9
np.max(M, axis=0)  # [7, 9, 8]
np.max(M, axis=1)  # [9, 8]
```

## max vs maximum vs argmax

| Función | Qué hace |
|---------|----------|
| `np.max` | el valor máximo (reduce un eje) |
| `np.maximum` | máximo **elemento a elemento** entre dos arrays |
| [[np.argmax]] | la **posición** del máximo |

```python
np.maximum([1, 5], [4, 2])   # [4, 5]  → compara par a par
```

## Parámetros en detalle

### `axis`, `keepdims`, `where`

Como en [[np.sum]]. `where` requiere indicar `initial` (valor de arranque) para no fallar con todo enmascarado.

### `initial` — valor base

Cota inferior de partida; útil con `where` o arrays vacíos.

## Casos de uso

### Normalización min-max

```python
norm = (a - np.min(a)) / (np.max(a) - np.min(a))
```

### Pico por fila

```python
picos = np.max(señales, axis=1)
```

## Buenas prácticas

1. Si necesitas **dónde** está el máximo, usa [[np.argmax]].
2. Para comparar dos arrays elemento a elemento, usa `np.maximum`.
3. Con NaN, usa [[np.nanmax]] (`np.max` propaga NaN).
4. Para el rango (max − min) directo, usa [[np.ptp]].

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| Resultado NaN | hay NaN (NaN "gana") | [[np.nanmax]] |
| Confundir con posición | se quería el índice | [[np.argmax]] |
| `zero-size array to reduction` | array vacío | pasar `initial` |

## Limitaciones

- Propaga NaN.
- Devuelve el valor, no su ubicación.

## Notas relacionadas

- [[concepto_axis_parametro]]
- [[np.min]]
- [[np.argmax]]
- [[np.ptp]]
- [[np.nanmax]]
