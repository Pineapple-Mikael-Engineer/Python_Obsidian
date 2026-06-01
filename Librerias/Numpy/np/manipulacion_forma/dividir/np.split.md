---
title: np.split — Dividir un array en sub-arrays
aliases:
  - split
  - np.split
  - dividir
tags:
  - numpy
  - api/funcion
  - manipulacion

# --- Clasificación ---
lib: numpy
mod: np
tipo: funcion

# --- Comportamiento ---
retorna: list
inplace: false

# --- Dependencias ---
requiere:
  - concepto_shape
  - concepto_axis_parametro

draft: false
---

# np.split — Dividir un array en sub-arrays

## Firma de la función

```python
np.split(
    ary,
    indices_or_sections,
    axis=0
) -> list[ndarray]
```

## Valor de retorno

Devuelve una **lista** de sub-arrays (vistas) resultado de cortar `ary` a lo largo del [[concepto_axis_parametro|eje]] indicado. Es la operación inversa de [[np.concatenate]].

| Entrada | `indices_or_sections` | Salida |
|---------|------------------------|--------|
| `(6,)` | `3` | 3 arrays de `(2,)` |
| `(6,)` | `[2, 4]` | `(2,)`, `(2,)`, `(2,)` (cortes en 2 y 4) |
| `(4, 4)`, `axis=1` | `2` | 2 arrays de `(4, 2)` |

```python
import numpy as np
arr = np.arange(6)
np.split(arr, 3)   # [array([0, 1]), array([2, 3]), array([4, 5])]
```

## Dos modos de uso

### Modo 1: número de partes iguales (entero)

Divide en `N` partes iguales. **Exige** que el tamaño del eje sea divisible por `N`.

```python
np.split(np.arange(9), 3)   # 3 partes de 3
np.split(np.arange(10), 3)  # ValueError: no divisible (usar array_split)
```

### Modo 2: puntos de corte (lista de índices)

Corta en las posiciones indicadas; no requiere divisibilidad.

```python
np.split(np.arange(8), [3, 5])
# [array([0,1,2]), array([3,4]), array([5,6,7])]
```

## Parámetros en detalle

### `ary` — array a dividir

Array de cualquier dimensión.

### `indices_or_sections` — cómo cortar

Entero (N partes iguales) o lista de índices de corte.

### `axis` — eje sobre el que cortar

Por defecto `0` (filas). Usa `axis=1` para columnas, etc.

## Casos de uso

### Separar features y target

```python
datos = np.random.rand(100, 5)
X, y = np.split(datos, [4], axis=1)   # X:(100,4)  y:(100,1)
```

### Partir en lotes

```python
lotes = np.split(np.arange(12), 4)    # 4 lotes de 3
```

## Buenas prácticas

1. Si el tamaño **no** es divisible, usa `np.array_split` (reparte el resto sin error).
2. Para 2D, [[np.vsplit]] (filas) y [[np.hsplit]] (columnas) se leen mejor.
3. El resultado es una lista de **vistas**: modificar un trozo afecta al original.

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| `array split does not result in an equal division` | tamaño no divisible por N | usar `np.array_split` |
| Esperar array y recibir lista | `split` devuelve `list` | desempaquetar o indexar la lista |
| Cortes en el eje equivocado | `axis` por defecto 0 | pasar `axis` explícito |

## Limitaciones

- El modo entero exige divisibilidad exacta (a diferencia de `array_split`).
- Devuelve vistas, no copias independientes.

## Notas relacionadas

- [[concepto_shape]]
- [[concepto_axis_parametro]]
- [[np.concatenate]]
- [[np.vsplit]]
- [[np.hsplit]]
