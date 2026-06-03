---
title: np.fromfunction — Construir un array desde sus índices
aliases:
  - fromfunction
  - np.fromfunction
tags:
  - numpy
  - api/funcion
  - creacion

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
  - concepto_vectorizacion

draft: false
---

# np.fromfunction — Construir un array desde sus índices

## Firma de la función

```python
np.fromfunction(
    function,
    shape,
    *,
    dtype=float,
    **kwargs
) -> ndarray
```

## Valor de retorno

Construye un array del `shape` indicado **evaluando `function` sobre las coordenadas** de cada posición. La función recibe arrays de índices (uno por dimensión) y se aplica de forma [[concepto_vectorizacion|vectorizada]], no celda a celda.

| `function` | `shape` | Resultado |
|------------|---------|-----------|
| `lambda i, j: i + j` | `(3, 3)` | suma de índices |
| `lambda i, j: i == j` | `(3, 3)` | matriz identidad booleana |
| `lambda i: i**2` | `(5,)` | `[0, 1, 4, 9, 16]` |

```python
import numpy as np
np.fromfunction(lambda i, j: i + j, (3, 3), dtype=int)
# array([[0, 1, 2],
#        [1, 2, 3],
#        [2, 3, 4]])
```

## Cómo recibe los argumentos la función

`function` recibe **un array por dimensión**, cada uno con el [[concepto_shape|shape]] completo, conteniendo el índice de esa dimensión:

```python
# Para shape (2, 3), la función recibe:
# i = [[0,0,0],   j = [[0,1,2],
#      [1,1,1]]        [0,1,2]]
```

Por eso debe escribirse de forma **vectorizada** (operar sobre arrays), no asumir escalares.

## Parámetros en detalle

### `function` — función de los índices

Callable que toma `ndim` arrays de índices y devuelve el valor de cada celda.

### `shape` — forma del array

Tupla; determina cuántos arrays de índices recibe `function` (uno por dimensión).

### `dtype` — tipo de los índices

Tipo de los arrays de índices que se pasan a `function` (por defecto `float`). Suele convenir `int`.

## Casos de uso

### Tablero de ajedrez

```python
tablero = np.fromfunction(lambda i, j: (i + j) % 2, (8, 8), dtype=int)
```

### Matriz de distancias al origen

```python
dist = np.fromfunction(lambda i, j: np.sqrt(i**2 + j**2), (5, 5))
```

### Gradiente lineal

```python
rampa = np.fromfunction(lambda i, j: j, (4, 4), dtype=int)
```

## Buenas prácticas

1. La función debe ser **vectorizada**: usa operaciones de NumPy, no `if` sobre escalares.
2. Pasa `dtype=int` cuando los índices deban ser enteros (lo habitual).
3. Para patrones simples (constantes, secuencias) hay opciones más directas: [[np.full]], [[np.arange]], [[np.eye]].

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| `function` falla con arrays | se escribió asumiendo escalares | vectorizar (usar ops de NumPy) |
| Índices flotantes inesperados | `dtype` por defecto `float` | pasar `dtype=int` |
| Lentitud con lógica compleja | función Python no vectorizable | construir con operaciones de array directas |

## Limitaciones

- La función debe poder operar sobre arrays completos (vectorizada).
- Para reglas no vectorizables conviene construir el array por otros medios.

## Notas relacionadas

- [[concepto_shape]]
- [[concepto_vectorizacion]]
- [[np.full]]
- [[np.eye]]
- [[np.arange]]
