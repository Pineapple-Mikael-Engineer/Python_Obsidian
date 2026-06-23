---
title: ndarray.shape — tupla con el tamaño de cada eje
aliases:
  - shape
  - ndarray.shape
tags:
  - numpy
  - api/atributo
  - shape
lib: numpy
mod: np.ndarray
tipo: atributo
draft: false
---

# ndarray.shape — tupla con el tamaño de cada eje

Tupla $(n_0, n_1, \dots, n_{k-1})$ de enteros no negativos donde cada $n_d$ es el número de elementos en el eje $d$. Es el metadato que convierte el buffer lineal del array en un tensor navegable: dice cómo *interpretar* los bytes, no los almacena. La teoría profunda (mapa de shapes, `(3,)` vs `(3,1)`, broadcasting) vive en [[concepto_shape]]; aquí lo práctico del atributo.

## Tipo y lectura/escritura

| Tipo de dato | ¿Asignable? |
|--------------|-------------|
| `tuple` de `int` (longitud `= ndim`) | **Sí.** Reasignar `arr.shape = (...)` hace un reshape *in-place* si el `size` total se conserva |

Es uno de los pocos atributos **asignables**. A diferencia de [[np.reshape]], la asignación a `shape` **falla** (en vez de copiar) si la nueva forma exigiese reordenar memoria; equivale a un reshape que solo admite el caso vista.

## En detalle

`shape` da el tamaño de cada eje y, de él, se derivan `ndim = len(shape)` y `size = ∏ nᵢ`.

```python
import numpy as np

np.array(5).shape          # ()      escalar 0D → tupla vacía
np.arange(4).shape         # (4,)    1D, la coma no es opcional
np.zeros((2, 3)).shape     # (2, 3)  matriz 2×3
np.zeros((2, 3, 4)).shape  # (2, 3, 4)
```

Asignar a `shape` reinterpreta el mismo buffer sin copiar, siempre que el producto se mantenga:

```python
arr = np.arange(12)
arr.shape = (3, 4)   # OK → 3*4 = 12, reshape in-place (no copia)
arr.shape = (5, 2)   # ValueError: total size must be unchanged (5*2=10 ≠ 12)
```

## Casos de uso

```python
# Validar la forma antes de operar
assert arr.shape == (2, 3)

# Desempaquetar ejes con nombres legibles
lote, alto, ancho, canales = imgs.shape

# Tomar un eje concreto sin recalcular
n_filas = arr.shape[0]

# Reformar in-place cuando se sabe que el array es contiguo
arr.shape = (-1, 4)   # un -1 deja que NumPy infiera ese eje
```

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| Confundir `(3,)` con `(3, 1)` | Mismos valores, distinto `ndim` | `(3,)` es 1D; para columna usar `arr.reshape(-1, 1)` |
| `arr.shape = (...)` lanza `AttributeError: incompatible shape` | El array no es contiguo y la nueva forma exigiría copia | Usar `arr = arr.reshape(...)`, que sí puede copiar |
| Olvidar la coma en `(4,)` | `(4)` es el entero `4`, no una tupla | Escribir siempre la coma para tuplas de un elemento |

## Notas relacionadas

- [[concepto_shape]]
- [[concepto_ndarray]]
- [[ndarray.ndim]]
- [[ndarray.size]]
- [[np.reshape]]
