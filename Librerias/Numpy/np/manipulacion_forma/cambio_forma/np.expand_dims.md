---
title: np.expand_dims — Insertar un eje de tamaño 1
aliases:
  - expand_dims
  - np.expand_dims
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
  - concepto_broadcasting

draft: false
---

# np.expand_dims — Insertar un eje de tamaño 1

## Firma de la función

```python
np.expand_dims(
    a,
    axis
) -> ndarray
```

## Valor de retorno

Devuelve una [[concepto_views_vs_copias|vista]] de `a` con un nuevo eje de tamaño 1 insertado en la posición `axis`. Aumenta `ndim` en 1; los datos no cambian. Es clave para habilitar [[concepto_broadcasting|broadcasting]].

| Shape entrada | `axis` | Shape salida |
|---------------|--------|--------------|
| `(3,)` | `0` | `(1, 3)` |
| `(3,)` | `1` | `(3, 1)` |
| `(2, 3)` | `0` | `(1, 2, 3)` |
| `(2, 3)` | `-1` | `(2, 3, 1)` |

```python
import numpy as np
v = np.array([1, 2, 3])        # shape (3,)
np.expand_dims(v, axis=0).shape  # (1, 3)  fila
np.expand_dims(v, axis=1).shape  # (3, 1)  columna
```

## Relación con newaxis y reshape

Tres formas equivalentes de añadir un eje:

```python
v = np.arange(3)
np.expand_dims(v, 1)   # (3, 1)
v[:, np.newaxis]       # (3, 1)  → np.newaxis es None
v.reshape(-1, 1)       # (3, 1)
```

`expand_dims` es la más explícita y legible cuando el eje se calcula en código.

## Parámetros en detalle

### `a` — array de entrada

Array de cualquier forma.

### `axis` — posición del nuevo eje

Entero o tupla de enteros (NumPy ≥ 1.18). Admite valores negativos (desde el final).

```python
a = np.ones((2, 3))
np.expand_dims(a, axis=(0, 3)).shape   # (1, 2, 3, 1)
```

## Casos de uso

### Preparar broadcasting entre vector y matriz

```python
M = np.ones((4, 3))
v = np.array([10, 20, 30, 40])      # (4,)  → no alinea con (4, 3)
M + np.expand_dims(v, axis=1)       # (4,1) sí alinea → suma por fila
```

### Añadir dimensión de batch o canal

```python
img = np.random.rand(28, 28)        # (28, 28)
batch = np.expand_dims(img, 0)      # (1, 28, 28)  → un solo ejemplo
canal = np.expand_dims(img, -1)     # (28, 28, 1)  → un canal
```

## Buenas prácticas

1. Es la operación **inversa** de [[np.squeeze]].
2. Úsalo para resolver errores de broadcasting por dimensiones que no alinean (ver [[concepto_axis_parametro]]).
3. Prefiérelo sobre `reshape` cuando solo quieras *insertar* un eje: comunica mejor la intención.
4. Acepta `axis` negativo para insertar al final sin conocer `ndim`.

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| `AxisError: axis N is out of bounds` | `axis` mayor que `ndim` del resultado | el rango válido es `[-(ndim+1), ndim]` |
| Broadcasting sigue fallando | se insertó el eje en la posición equivocada | revisar si querías `axis=0` vs `axis=1` |
| Forma duplicada inesperada | se llamó dos veces | un solo `expand_dims` por eje deseado |

## Limitaciones

- Solo inserta ejes de **tamaño 1**; no replica datos (eso es [[np.repeat]] o [[np.tile]]).
- Aumenta `ndim` de uno en uno por posición indicada.

## Notas relacionadas

- [[concepto_shape]]
- [[concepto_broadcasting]]
- [[concepto_axis_parametro]]
- [[np.squeeze]]
- [[np.reshape]]
- [[np.newaxis]]
