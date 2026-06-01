---
title: np.put — Asignar valores por índices (in-place)
aliases:
  - put
  - np.put
tags:
  - numpy
  - api/funcion
  - indexado

# --- Clasificación ---
lib: numpy
mod: np
tipo: funcion

# --- Comportamiento ---
retorna: None
inplace: true

# --- Dependencias ---
requiere:
  - concepto_indexing

draft: false
---

# np.put — Asignar valores por índices (in-place)

## Firma de la función

```python
np.put(
    a,
    ind,
    v,
    mode='raise'
) -> None
```

## Valor de retorno

**No devuelve nada** (`None`): modifica `a` **in-place**. Es la operación inversa de [[np.take]]: escribe `v` en las posiciones `ind` del array aplanado.

| Antes | `ind` | `v` | Después |
|-------|-------|-----|---------|
| `[0,0,0,0]` | `[0, 2]` | `[9, 8]` | `[9,0,8,0]` |
| `[1,2,3,4]` | `[0, 1]` | `5` | `[5,5,3,4]` |

```python
import numpy as np
a = np.arange(5)
np.put(a, [0, 2], [99, 88])
a   # array([99,  1, 88,  3,  4])  → a cambió
```

## ⚠️ Trabaja sobre índices aplanados

`np.put` siempre usa índices del array **aplanado** (estilo `a.flat`), ignorando la forma 2D:

```python
M = np.zeros((2, 3))
np.put(M, [0, 4], 1)   # posiciones aplanadas 0 y 4
# [[1, 0, 0], [0, 1, 0]]
```

Para asignación 2D por (fila, columna), usa indexado directo `M[filas, cols] = v`.

## Parámetros en detalle

### `a` — array a modificar

Se modifica in-place.

### `ind` — índices (aplanados)

Entero o array de enteros sobre `a.flat`.

### `v` — valores a escribir

Escalar o array; se reciclan por broadcasting si hay menos que índices.

### `mode` — índices fuera de rango

`'raise'` (error), `'wrap'` (módulo), `'clip'` (recorta).

## Casos de uso

### Inicializar posiciones concretas

```python
buffer = np.zeros(10)
np.put(buffer, [1, 4, 7], -1)
```

## Buenas prácticas

1. Para asignación 2D por coordenadas, prefiere indexado directo `a[i, j] = v` (más claro).
2. Recuerda que **muta** `a` y devuelve `None`: nunca hagas `a = np.put(...)`.
3. Para leer por índices (lo inverso), usa [[np.take]].

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| `a` quedó en `None` | se asignó el retorno (`a = np.put(...)`) | llamar sin asignar |
| Posiciones inesperadas en 2D | usa índices **aplanados** | usar `a[filas, cols] = v` |
| `IndexError` | índice fuera de rango | `mode='clip'`/`'wrap'` |

## Limitaciones

- Solo índices aplanados; no respeta la forma multidimensional.
- Muta el array original (no apto si necesitas conservarlo).

## Notas relacionadas

- [[concepto_indexing]]
- [[np.take]]
- [[np.where]]
