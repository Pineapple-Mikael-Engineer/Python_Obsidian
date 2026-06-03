---
title: np.ones — Array inicializado a unos
aliases:
  - ones
  - np.ones
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

# np.ones — Array inicializado a unos

## Firma de la función

```python
np.ones(
    shape,
    dtype=None,
    order='C',
    *,
    like=None
) -> ndarray
```

## Valor de retorno

Devuelve un [[concepto_ndarray|ndarray]] del `shape` indicado con todos sus elementos a `1`. El `dtype` por defecto es `float64`.

| Llamada | Shape | dtype | Contenido |
|---------|-------|-------|-----------|
| `np.ones(3)` | `(3,)` | `float64` | `[1., 1., 1.]` |
| `np.ones((2, 2))` | `(2, 2)` | `float64` | matriz de unos |
| `np.ones(3, dtype=int)` | `(3,)` | `int64` | `[1, 1, 1]` |

```python
import numpy as np
np.ones((2, 3))
# array([[1., 1., 1.],
#        [1., 1., 1.]])
```

## Parámetros en detalle

### `shape` — forma del array

Entero (1D) o tupla (nD). Define el [[concepto_shape|shape]]. Único parámetro obligatorio.

```python
np.ones(4)        # (4,)
np.ones((3, 3))   # (3, 3)
```

### `dtype` — tipo de los unos

Por defecto `float64`. Especifícalo según necesidad (ver [[concepto_dtype]]).

```python
np.ones(3, dtype=np.int32)   # [1, 1, 1]
np.ones(2, dtype=bool)       # [True, True]
```

### `order` — disposición en memoria

`'C'` (por defecto) o `'F'`. Ver [[concepto_contiguidad_memoria]].

## Casos de uso

### Vector de sesgo / bias

```python
bias = np.ones(10)            # término independiente en regresión
```

### Inicializar pesos o factores a 1

```python
escala = np.ones((3, 3))      # matriz neutra para multiplicación elemento a elemento
```

### Construir un valor constante por multiplicación

```python
cincos = np.ones(5) * 5       # [5., 5., 5., 5., 5.]
# (más directo: np.full(5, 5))
```

### Columna de unos para diseño de matriz (mínimos cuadrados)

```python
x = np.array([1.0, 2.0, 3.0])
A = np.column_stack([np.ones_like(x), x])   # [[1, x0], [1, x1], ...]
```

## Buenas prácticas

1. Idéntico a [[np.zeros]] salvo el valor de relleno; aplican las mismas reglas.
2. Para clonar shape/dtype de otro array, usa [[np.ones_like]].
3. Para un valor constante distinto de 1, prefiere [[np.full]] antes que `np.ones(...) * k`.
4. Recuerda el defecto `float`: añade `dtype=int` si trabajas con enteros.

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| Floats donde esperabas ints | dtype por defecto `float` | `np.ones(n, dtype=int)` |
| `np.ones(2, 3)` falla | `3` se interpreta como dtype | usar tupla `np.ones((2, 3))` |
| `np.ones(n) * k` poco claro | rodeo para un valor constante | usar `np.full(n, k)` |

## Limitaciones

- Solo rellena con `1`; para otros valores constantes está [[np.full]].
- No genera secuencias: ver [[np.arange]] y [[np.linspace]].

## Notas relacionadas

- [[concepto_shape]]
- [[concepto_dtype]]
- [[np.zeros]]
- [[np.full]]
- [[np.ones_like]]
- [[np.empty]]
- [[np.array]]
