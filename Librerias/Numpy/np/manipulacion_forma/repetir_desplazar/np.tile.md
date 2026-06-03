---
title: np.tile — Repetir el array completo como un mosaico
aliases:
  - tile
  - np.tile
  - mosaico
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

draft: false
---

# np.tile — Repetir el array completo como un mosaico

## Firma de la función

```python
np.tile(
    A,
    reps
) -> ndarray
```

## Valor de retorno

Devuelve un array que repite el **bloque completo** `A` el número de veces indicado en `reps`, en cada eje (como baldosas de un mosaico).

| Entrada | `reps` | Salida |
|---------|--------|--------|
| `[1, 2]` | `3` | `[1, 2, 1, 2, 1, 2]` |
| `[1, 2]` | `(2, 2)` | `[[1,2,1,2],[1,2,1,2]]` |
| `[[1, 2]]` | `(2, 1)` | `[[1,2],[1,2]]` |

```python
import numpy as np
np.tile([1, 2], 3)        # array([1, 2, 1, 2, 1, 2])
np.tile([1, 2], (2, 2))   # array([[1, 2, 1, 2],
                          #        [1, 2, 1, 2]])
```

## tile vs repeat

> `tile` repite el **patrón completo** (`1,2,1,2`); [[np.repeat]] repite **cada elemento** (`1,1,2,2`).

## Parámetros en detalle

### `A` — array a repetir

Array o secuencia.

### `reps` — repeticiones por eje

Entero o tupla. Si `reps` tiene más dimensiones que `A`, se promociona `A` añadiendo ejes por la izquierda.

```python
np.tile(np.array([1, 2, 3]), (2, 1)).shape   # (2, 3)
```

## Casos de uso

### Construir una rejilla repitiendo un patrón

```python
patron = np.array([[0, 1], [1, 0]])
tablero = np.tile(patron, (4, 4))    # (8, 8) tipo damero
```

### Replicar un vector como filas

```python
fila = np.array([1, 2, 3])
M = np.tile(fila, (5, 1))            # (5, 3): la fila repetida 5 veces
```

## Buenas prácticas

1. Para replicar un patrón completo; para duplicar elementos in situ, [[np.repeat]].
2. En muchos casos el [[concepto_broadcasting|broadcasting]] evita tener que materializar el mosaico (más eficiente en memoria).
3. `reps` como tupla controla la repetición por eje.

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| Resultado tipo `1,1,2,2` esperado | se quería repetir elementos | usar [[np.repeat]] |
| Memoria alta por materializar copias | `tile` crea el array completo | considerar broadcasting |

## Limitaciones

- Materializa una copia completa: si solo necesitas alinear shapes para operar, el broadcasting es preferible.

## Notas relacionadas

- [[concepto_shape]]
- [[concepto_broadcasting]]
- [[np.repeat]]
- [[np.roll]]
