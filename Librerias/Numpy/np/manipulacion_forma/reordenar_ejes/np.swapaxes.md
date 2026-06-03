---
title: np.swapaxes — Intercambiar dos ejes
aliases:
  - swapaxes
  - np.swapaxes
tags:
  - numpy
  - api/funcion
  - shape

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
  - concepto_views_vs_copias

draft: false
---

# np.swapaxes — Intercambiar dos ejes

## Firma de la función

```python
np.swapaxes(
    a,
    axis1,
    axis2
) -> ndarray
```

## Valor de retorno

Devuelve una [[concepto_views_vs_copias|vista]] de `a` con los ejes `axis1` y `axis2` intercambiados. No copia datos: solo reordena los `strides`. Es el caso particular de [[np.transpose]] cuando solo permutas **dos** ejes.

| Shape entrada | `axis1, axis2` | Shape salida |
|---------------|----------------|--------------|
| `(2, 3)` | `0, 1` | `(3, 2)` |
| `(2, 3, 4)` | `0, 2` | `(4, 3, 2)` |
| `(2, 3, 4)` | `1, 2` | `(2, 4, 3)` |

```python
import numpy as np
T = np.ones((2, 3, 4))
np.swapaxes(T, 1, 2).shape   # (2, 4, 3)
```

## Parámetros en detalle

### `a` — array de entrada

Array de cualquier dimensión.

### `axis1`, `axis2` — ejes a intercambiar

Enteros (admiten negativos). El orden entre ellos es irrelevante: `swapaxes(a, 1, 2)` == `swapaxes(a, 2, 1)`.

## Relación con transpose

```python
T = np.ones((2, 3, 4))
np.swapaxes(T, 0, 2)            # más legible para 2 ejes
np.transpose(T, (2, 1, 0))     # equivalente con permutación completa
```

> Usa `swapaxes` cuando solo intercambias **dos** ejes; usa [[np.transpose]] para permutaciones generales y [[np.moveaxis]] para reubicar un eje conservando el resto.

## Casos de uso

### Pasar de (batch, features, tiempo) a (batch, tiempo, features)

```python
datos = np.random.rand(32, 10, 100)     # (batch, feat, tiempo)
datos = np.swapaxes(datos, 1, 2)        # (32, 100, 10)
```

### Transponer la matriz interna de un lote de matrices

```python
lote = np.random.rand(8, 3, 5)
lote_T = np.swapaxes(lote, 1, 2)        # cada matriz 3x5 → 5x3
```

## Buenas prácticas

1. Para intercambiar exactamente dos ejes es más claro que `transpose`.
2. Recuerda que devuelve vista: el resultado comparte memoria con `a`.
3. Tras intercambiar, el array deja de ser C-contiguo (ver [[concepto_contiguidad_memoria]]).

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| `AxisError: axis N is out of bounds` | `axis1`/`axis2` fuera de rango | usar ejes válidos (`0..ndim-1` o negativos) |
| El original cambió | es una vista | `.copy()` si necesitas independencia |

## Limitaciones

- Solo intercambia **dos** ejes; para mover uno conservando el resto, [[np.moveaxis]].
- No copia: si una librería exige memoria contigua, fuerza la copia.

## Notas relacionadas

- [[concepto_shape]]
- [[concepto_views_vs_copias]]
- [[np.transpose]]
- [[np.moveaxis]]
