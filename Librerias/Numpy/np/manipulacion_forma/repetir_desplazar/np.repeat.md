---
title: np.repeat — Repetir cada elemento N veces
aliases:
  - repeat
  - np.repeat
tags:
  - numpy
  - api/funcion
  - manipulacion

# --- Clasificación ---
lib: numpy
mod: np
tipo: funcion

# --- Comportamiento ---
retorna: ndarray
inplace: false

# --- Dependencias ---
requiere:
  - concepto_shape
  - concepto_axis_parametro

draft: false
---

# np.repeat — Repetir cada elemento N veces

## Firma de la función

```python
np.repeat(
    a,
    repeats,
    axis=None
) -> ndarray
```

## Valor de retorno

Devuelve un array donde **cada elemento** se repite `repeats` veces de forma consecutiva. Con `axis=None` (por defecto) aplana primero.

| Entrada | `repeats` | `axis` | Salida |
|---------|-----------|--------|--------|
| `[1, 2, 3]` | `2` | `None` | `[1, 1, 2, 2, 3, 3]` |
| `[1, 2, 3]` | `[1, 2, 3]` | `None` | `[1, 2, 2, 3, 3, 3]` |
| `[[1, 2], [3, 4]]` | `2` | `0` | `[[1,2],[1,2],[3,4],[3,4]]` |

```python
import numpy as np
np.repeat([1, 2, 3], 2)   # array([1, 1, 2, 2, 3, 3])
```

## repeat vs tile

> `repeat` repite **elemento a elemento** (`1,1,2,2`); [[np.tile]] repite el **bloque completo** (`1,2,1,2`).

```python
np.repeat([1, 2], 3)   # [1, 1, 1, 2, 2, 2]
np.tile([1, 2], 3)     # [1, 2, 1, 2, 1, 2]
```

## Parámetros en detalle

### `a` — array de entrada

Array o secuencia.

### `repeats` — número de repeticiones

Entero (igual para todos) o array (uno por elemento del eje).

### `axis` — eje sobre el que repetir

`None` aplana; un entero repite a lo largo de ese [[concepto_axis_parametro|eje]] conservando el resto.

```python
M = np.array([[1, 2], [3, 4]])
np.repeat(M, 2, axis=1)   # [[1,1,2,2],[3,3,4,4]]
```

## Casos de uso

### Expandir etiquetas por grupo

```python
clases = np.array([0, 1, 2])
conteos = np.array([3, 2, 4])
etiquetas = np.repeat(clases, conteos)   # [0,0,0,1,1,2,2,2,2]
```

### Escalar (upsample) una imagen por píxel

```python
img = np.array([[1, 2], [3, 4]])
grande = np.repeat(np.repeat(img, 2, axis=0), 2, axis=1)   # (4, 4)
```

## Buenas prácticas

1. Usa `repeat` para duplicar valores in situ; `tile` para repetir patrones.
2. `repeats` como array permite repeticiones desiguales por elemento.
3. Indica `axis` para no aplanar matrices sin querer.

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| Matriz aplanada inesperadamente | `axis=None` por defecto | pasar `axis` |
| `operands could not be broadcast` | `repeats` array de largo distinto al eje | igualar la longitud |
| Confundir patrón con elemento | se quería `tile` | usar [[np.tile]] |

## Limitaciones

- Repite elementos contiguos; no replica el array completo (eso es `tile`).

## Notas relacionadas

- [[concepto_shape]]
- [[concepto_axis_parametro]]
- [[np.tile]]
- [[np.roll]]
