---
title: ndarray.put — Asignar valores por índices aplanados (in-place)
aliases:
  - put
  - ndarray.put
tags:
  - numpy
  - api/metodo
  - indexado
lib: numpy
obj: ndarray
tipo: metodo
retorna: None
inplace: true
draft: false
---

# ndarray.put — Asignar valores por índices aplanados (in-place)

## Firma del método

```python
ndarray.put(
    indices,
    values,
    mode='raise'
) -> None
```

## Valor de retorno

| Entrada (`self`) | `indices` | `values` | Efecto |
|------------------|-----------|----------|--------|
| `[0,0,0,0]` | `[0, 2]` | `[9, 9]` | `self` → `[9, 0, 9, 0]` |
| shape `(2, 2)` lleno de 0 | `[0, 3]` | `1` | `self` → `[[1,0],[0,1]]` |

Retorna `None`. **Modifica `self` in-place**. Los `indices` siempre se interpretan sobre `self` **aplanado** (orden C), sin importar su shape.

```python
import numpy as np
a = np.zeros(5)
a.put([0, 2, 4], [10, 20, 30])
a   # array([10.,  0., 20.,  0., 30.])
```

## Equivalencia con np.put

`a.put(indices, values, ...)` equivale a [[np.put]] `np.put(a, indices, values, ...)`. Ambas son la operación **inversa de take**: en vez de leer por índices, escriben por índices. A diferencia de la asignación con fancy indexing (`a[idx] = values`), `put` solo opera sobre el array aplanado (no acepta tuplas por eje) y no devuelve valor.

## Parámetros en detalle

### `indices` — posiciones aplanadas a escribir

Enteros que indexan `self.flat`. Para un 2D, el índice plano `i` corresponde a `(i // ncols, i % ncols)`.

```python
M = np.zeros((2, 3))
M.put([0, 5], [1, 1])
M   # [[1,0,0],[0,0,1]]  → posiciones (0,0) y (1,2)
```

### `values` — valores a asignar

Se difunden ([[concepto_broadcasting]]) sobre `indices`. Si hay menos valores que índices, se reciclan en ciclo:

```python
a = np.zeros(6)
a.put([0, 1, 2, 3], 7)   # un escalar se reparte → [7,7,7,7,0,0]
```

### `mode` — índices fuera de rango

| `mode` | Comportamiento |
|--------|----------------|
| `'raise'` (defecto) | lanza `IndexError` |
| `'wrap'` | da la vuelta (módulo) |
| `'clip'` | recorta al borde |

## Casos de uso

### Sembrar valores dispersos

```python
grid = np.zeros(100)
grid.put([3, 50, 99], [1.0, 1.0, 1.0])   # marca 3 posiciones
```

### Actualizar in-place sin reasignar

```python
señal = np.arange(10.0)
señal.put([0, -1], np.nan)   # extremos a NaN, mismo objeto
```

## Buenas prácticas

1. Recuerda que `indices` es **siempre sobre el array aplanado**; para indexar por eje usa `self[fila, col] = ...`.
2. Útil cuando quieres mutar el array existente sin crear copias ni reasignar la variable.
3. Para la operación de lectura inversa, usa `self.take(...)`.

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| Asignación en posición equivocada (2D) | `indices` se interpreta aplanado | calcular índice plano o usar `self[i,j]=` |
| `IndexError` | índice fuera de rango con `mode='raise'` | `mode='clip'`/`'wrap'` |
| Esperar un retorno | `put` devuelve `None` | leer `self` tras la llamada |

## Notas relacionadas

- [[np.put]]
- [[ndarray.take]]
- [[concepto_indexing]]
- [[concepto_broadcasting]]
