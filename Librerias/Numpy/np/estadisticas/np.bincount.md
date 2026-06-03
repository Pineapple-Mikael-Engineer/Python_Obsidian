---
title: np.bincount — Conteo de enteros no negativos
aliases:
  - bincount
  - np.bincount
tags:
  - numpy
  - api/funcion
  - estadistica

# --- Clasificación ---
lib: numpy
mod: np
tipo: funcion

# --- Comportamiento ---
retorna: ndarray
inplace: false

# --- Dependencias ---
requiere:
  - concepto_indexing

draft: false
---

# np.bincount — Conteo de enteros no negativos

## Firma de la función

```python
np.bincount(
    x,
    weights=None,
    minlength=0
) -> ndarray
```

## Valor de retorno

Cuenta las apariciones de cada entero no negativo. El resultado en la posición `i` es **cuántas veces aparece `i`** en `x`. La longitud de salida es `max(x) + 1`.

| `x` | Resultado | Lectura |
|-----|-----------|---------|
| `[0, 1, 1, 3, 3, 3]` | `[1, 2, 0, 3]` | 0→1 vez, 1→2, 2→0, 3→3 |

```python
import numpy as np
np.bincount([0, 1, 1, 3, 3, 3])   # array([1, 2, 0, 3])
```

## Parámetros en detalle

### `x` — enteros no negativos

Array 1D de enteros `≥ 0`. Valores negativos → error.

### `weights` — pesos

Si se da, suma los pesos en lugar de contar (debe tener el largo de `x`):

```python
x = np.array([0, 1, 1, 2])
w = np.array([0.5, 1.0, 1.0, 2.0])
np.bincount(x, weights=w)   # [0.5, 2.0, 2.0]
```

### `minlength` — longitud mínima

Garantiza al menos `minlength` bins (rellena con ceros).

## Casos de uso

### Frecuencia de etiquetas de clase

```python
conteos = np.bincount(etiquetas)
clase_mayoritaria = np.argmax(conteos)
```

### Suma agrupada por índice (con weights)

```python
np.bincount(grupos, weights=valores)   # suma valores por grupo
```

## Buenas prácticas

1. Solo para enteros **no negativos**; para flotantes/rangos usa [[np.histogram]].
2. Usa `minlength` si necesitas un tamaño fijo aunque falten clases altas.
3. `weights` convierte `bincount` en una suma agrupada (group-by) muy rápida.

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| `ValueError: x must be non-negative` | hay negativos | desplazar o filtrar |
| Falta una clase alta | esa clase no apareció | usar `minlength` |

## Limitaciones

- Solo enteros no negativos; la salida crece hasta `max(x)+1`.

## Notas relacionadas

- [[concepto_indexing]]
- [[np.histogram]]
- [[np.unique]]
- [[np.digitize]]
