---
title: np.prod — Producto de elementos a lo largo de un eje
aliases:
  - prod
  - np.prod
  - producto
tags:
  - numpy
  - api/funcion
  - reducciones

# --- Clasificación ---
lib: numpy
mod: np
tipo: funcion

# --- Comportamiento ---
retorna: ndarray o escalar
inplace: false

# --- Dependencias ---
requiere:
  - concepto_axis_parametro
  - concepto_dtype

draft: false
---

# np.prod — Producto de elementos a lo largo de un eje

## Firma de la función

```python
np.prod(
    a,
    axis=None,
    dtype=None,
    keepdims=False,
    initial=1,
    where=True
) -> ndarray | escalar
```

## Valor de retorno

Multiplica los elementos de `a` a lo largo del [[concepto_axis_parametro|eje]] indicado. Análoga a [[np.sum]] pero con multiplicación. Con `axis=None` devuelve el producto total.

| Entrada | `axis` | Salida |
|---------|--------|--------|
| `[1, 2, 3, 4]` | `None` | `24` |
| `(2, 3)` | `0` | `(3,)` producto por columna |
| `(2, 3)` | `1` | `(2,)` producto por fila |

```python
import numpy as np
np.prod([1, 2, 3, 4])   # 24
M = np.array([[1, 2], [3, 4]])
np.prod(M, axis=0)      # [3, 8]
```

## Parámetros en detalle

### `axis`, `keepdims`, `where`

Idénticos a [[np.sum]]: `axis` colapsa el eje, `keepdims` lo conserva con tamaño 1, `where` filtra.

### `dtype` — acumulador

Los productos **crecen muy rápido**; el riesgo de overflow es mayor que en la suma. Fija `dtype` con enteros:

```python
arr = np.arange(1, 21)            # factorial de 20
np.prod(arr)                     # puede desbordar int64
np.prod(arr, dtype=np.float64)   # seguro (aunque pierde exactitud)
```

## Casos de uso

### Tamaño total a partir de un shape

```python
shape = (3, 4, 5)
np.prod(shape)   # 60  → número de elementos
```

### Probabilidad conjunta de eventos independientes

```python
p = np.array([0.9, 0.8, 0.95])
np.prod(p)   # 0.684
```

## Buenas prácticas

1. Vigila el **overflow**: los productos escalan exponencialmente; usa `dtype` amplio o flotante.
2. Para productos acumulados parciales, usa [[np.cumprod]].
3. Si hay NaN, usa [[np.nanprod]].

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| Overflow / resultado negativo absurdo | enteros desbordados | `dtype=np.float64` o `np.int64` |
| `0` inesperado | algún elemento es 0 | revisar los datos |
| NaN propagado | hay NaN en la entrada | [[np.nanprod]] |

## Limitaciones

- Muy sensible al overflow con enteros.
- Propaga NaN.

## Notas relacionadas

- [[concepto_axis_parametro]]
- [[concepto_dtype]]
- [[np.sum]]
- [[np.cumprod]]
