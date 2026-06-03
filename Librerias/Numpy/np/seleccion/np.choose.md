---
title: np.choose — Construir un array eligiendo por índices
aliases:
  - choose
  - np.choose
tags:
  - numpy
  - api/funcion
  - indexado

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

# np.choose — Construir un array eligiendo por índices

## Firma de la función

```python
np.choose(
    a,
    choices,
    out=None,
    mode='raise'
) -> ndarray
```

## Valor de retorno

Construye un array tomando, en cada posición, el valor de `choices[a[posición]]`. El array `a` actúa como **selector de índices** entre varias opciones.

| `a` (índices) | `choices` | Resultado |
|---------------|-----------|-----------|
| `[0, 1, 0]` | `[[10,20,30], [1,2,3]]` | `[10, 2, 30]` |

```python
import numpy as np
a = np.array([0, 1, 1, 0])
choices = [np.array([10, 11, 12, 13]),   # opción 0
           np.array([20, 21, 22, 23])]   # opción 1
np.choose(a, choices)
# array([10, 21, 22, 13])  → toma de opción 0 o 1 según a
```

## Cómo funciona

Para cada posición `i`, el resultado es `choices[a[i]][i]`: `a` decide **de qué array** de `choices` se toma el elemento en esa posición.

## choose vs select

| | `np.choose` | [[np.select]] |
|--|------------|---------------|
| Selector | array de **índices enteros** | lista de **condiciones booleanas** |
| Nº de opciones | `len(choices)` | `len(condlist)` |
| Uso típico | selección por categoría conocida | reglas por umbrales |

## Parámetros en detalle

### `a` — array de índices

Enteros en `[0, len(choices)-1]`. Define qué opción se toma en cada celda.

### `choices` — secuencia de arrays

Lista/tupla de arrays broadcastables entre sí y con `a`.

### `mode` — índices fuera de rango

`'raise'` (error), `'wrap'` (módulo), `'clip'` (recorta).

## Casos de uso

### Ensamblar a partir de categorías

```python
categoria = np.array([0, 2, 1])     # selector
paletas = [np.zeros(3), np.ones(3), np.full(3, 0.5)]
np.choose(categoria, paletas)
```

## Buenas prácticas

1. Úsalo cuando ya tienes un array de **índices enteros**; para reglas por condición, [[np.select]].
2. Limitado a `choices` con pocos elementos; para tablas grandes usa [[np.take]] con fancy indexing.
3. `mode='clip'` evita errores si los índices pueden salirse.

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| `invalid entry in choice array` | índice ≥ len(choices) | `mode='clip'`/`'wrap'` o validar |
| Resultado raro por broadcasting | shapes de `choices` no alinean | igualar formas |

## Limitaciones

- Poco práctico con muchas opciones (`choices` largo): [[np.take]] o fancy indexing escalan mejor.

## Notas relacionadas

- [[concepto_indexing]]
- [[np.select]]
- [[np.take]]
- [[np.where]]
