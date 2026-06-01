---
title: np.full — Array relleno con un valor constante
aliases:
  - full
  - np.full
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
  - concepto_dtype

draft: false
---

# np.full — Array relleno con un valor constante

## Firma de la función

```python
np.full(
    shape,
    fill_value,
    dtype=None,
    order='C',
    *,
    like=None
) -> ndarray
```

## Valor de retorno

Devuelve un [[concepto_ndarray|ndarray]] del `shape` indicado con **todos los elementos iguales** a `fill_value`. Generaliza [[np.zeros]] (valor 0) y [[np.ones]] (valor 1).

| Llamada | Resultado |
|---------|-----------|
| `np.full(3, 7)` | `[7, 7, 7]` |
| `np.full((2, 2), 9.5)` | matriz 2×2 de `9.5` |
| `np.full(3, np.nan)` | `[nan, nan, nan]` |

```python
import numpy as np
np.full((2, 3), -1)
# array([[-1, -1, -1],
#        [-1, -1, -1]])
```

## Parámetros en detalle

### `shape` — forma

Entero o tupla (ver [[concepto_shape]]).

### `fill_value` — valor de relleno

Escalar (o array compatible por broadcasting). El `dtype` se **infiere de `fill_value`** si no se especifica:

```python
np.full(3, 7).dtype      # int64   (entero)
np.full(3, 7.0).dtype    # float64 (flotante)
np.full(3, np.nan)       # fuerza float (nan no es entero)
```

### `dtype` — tipo explícito

Sobrescribe el inferido. Útil para fijar precisión (ver [[concepto_dtype]]).

## Casos de uso

### Inicializar con un centinela (sentinel)

```python
distancias = np.full(n, np.inf)   # "infinito" como valor de partida
ids = np.full(n, -1, dtype=int)   # -1 = "sin asignar"
```

### Matriz de un valor por defecto

```python
config = np.full((10, 10), 0.5)
```

## Buenas prácticas

1. Prefiérela sobre `np.ones(shape) * k` o `np.zeros(shape) + k`: más clara y directa.
2. Para clonar shape/dtype de otro array, usa [[np.full_like]].
3. Fija `dtype` si `fill_value` podría inferir un tipo no deseado.

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| dtype entero inesperado | `fill_value` es int | pasar `7.0` o `dtype=float` |
| `nan` da error en int | `nan` solo existe en float | usar `dtype=float` |

## Limitaciones

- Un único valor de relleno (para patrones usa [[np.tile]] o [[np.fromfunction]]).

## Notas relacionadas

- [[concepto_shape]]
- [[concepto_dtype]]
- [[np.zeros]]
- [[np.ones]]
- [[np.full_like]]
