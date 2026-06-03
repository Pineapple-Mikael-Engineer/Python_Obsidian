---
title: np.add — Suma elemento a elemento (ufunc)
aliases:
  - add
  - np.add
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
  - concepto_broadcasting

draft: false
---

# np.add — Suma elemento a elemento (ufunc)

## Firma de la función

```python
np.add(
    x1,
    x2,
    /,
    out=None,
    *,
    where=True,
    dtype=None,
    casting='same_kind',
    order='K'
) -> ndarray
```

## Valor de retorno

Devuelve `x1 + x2` **elemento a elemento**, alineando shapes por [[concepto_broadcasting|broadcasting]]. Es la [[concepto_ufuncs|ufunc]] que respalda el operador `+`.

| `x1` | `x2` | Resultado |
|------|------|-----------|
| `[1, 2, 3]` | `10` | `[11, 12, 13]` |
| `[1, 2, 3]` | `[4, 5, 6]` | `[5, 7, 9]` |
| `(2, 3)` | `(3,)` | broadcasting → `(2, 3)` |

```python
import numpy as np
np.add([1, 2, 3], [4, 5, 6])   # array([5, 7, 9])
np.add(arr, 10)                # equivale a arr + 10
```

## Relación con el operador `+`

`arr1 + arr2` llama internamente a `np.add(arr1, arr2)`. La forma función añade los parámetros `out`, `where`, `dtype`.

## Parámetros en detalle

### `x1`, `x2` — operandos

Arrays o escalares, broadcastables entre sí.

### `out` — array de salida

Escribe el resultado en un array preexistente (evita asignar memoria nueva):

```python
np.add(a, b, out=a)   # suma in-place sobre a
```

### `where` — máscara condicional

Solo calcula donde `where` es True; el resto conserva el valor de `out`.

```python
np.add(a, b, where=a > 0, out=np.zeros_like(a))
```

### `dtype` — tipo del resultado

Fuerza el [[concepto_dtype|dtype]] de salida.

## Casos de uso

### Acumular en un buffer sin copias

```python
total = np.zeros(3)
for fila in matriz:
    np.add(total, fila, out=total)
```

### Suma con broadcasting

```python
M = np.ones((3, 4))
v = np.array([1, 2, 3, 4])
np.add(M, v)   # suma v a cada fila
```

## Buenas prácticas

1. Para código normal usa el operador `+`; usa `np.add` cuando necesites `out`/`where`.
2. `out=` reduce asignaciones de memoria en bucles intensivos.
3. Las demás operaciones tienen su ufunc: [[np.subtract]], [[np.multiply]], [[np.divide]].

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| `operands could not be broadcast together` | shapes incompatibles | revisar dimensiones (ver [[concepto_broadcasting]]) |
| Overflow silencioso | enteros pequeños | fijar `dtype` mayor |
| `out` con dtype incompatible | casting estricto | ajustar `dtype`/`casting` |

## Limitaciones

- Suma elemento a elemento; para suma-reducción de un array usa [[np.sum]].

## Notas relacionadas

- [[concepto_ufuncs]]
- [[concepto_broadcasting]]
- [[np.subtract]]
- [[np.multiply]]
- [[np.divide]]
- [[np.sum]]
