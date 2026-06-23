---
title: ndarray.strides — bytes a saltar por eje
aliases:
  - strides
  - ndarray.strides
tags:
  - numpy
  - api/atributo
  - memoria
lib: numpy
mod: np.ndarray
tipo: atributo
draft: false
---

# ndarray.strides — bytes a saltar por eje

Tupla $(s_0, \dots, s_{k-1})$ donde $s_d$ son los **bytes** que hay que avanzar en el buffer para incrementar en 1 el índice del eje $d$. Es el metadato que conecta un índice N-D con una posición lineal de memoria, y la pieza que explica por qué tantas operaciones de NumPy no copian datos. El modelo completo (buffer + 3 metadatos) vive en [[concepto_ndarray]] y su cara física en [[concepto_contiguidad_memoria]].

## Tipo y lectura/escritura

| Tipo de dato | ¿Asignable? |
|--------------|-------------|
| `tuple` de `int` (longitud `= ndim`), en **bytes** | **Sí, pero peligroso.** Asignar strides a mano puede hacer que el array lea fuera de su buffer (corrupción/segfault). Reservado a trucos como `np.lib.stride_tricks.as_strided` |

## En detalle

Con los strides, localizar cualquier elemento es una sola cuenta aritmética en vez de una búsqueda anidada. El offset en bytes del elemento $A[i_0,\dots,i_{k-1}]$ es:

$$ \text{offset}(i_0,\dots,i_{k-1}) \;=\; \sum_{d=0}^{k-1} i_d \cdot s_d $$

Para un array C-contiguo, el stride de un eje es el `itemsize` por el producto de los tamaños de los ejes a su derecha; el último eje tiene el stride mínimo ($= \text{itemsize}$):

```python
import numpy as np

arr = np.array([[1, 2, 3],
                [4, 5, 6]], dtype=np.int64)   # itemsize = 8, shape (2, 3)
arr.strides     # (24, 8)
#   eje 0 (fila):    3 elem × 8 = 24 bytes
#   eje 1 (columna): 1 elem × 8 =  8 bytes
```

**Por qué `.T` solo cambia los strides:** transponer no mueve ni un byte, solo **invierte** la tupla de strides (y la de shape). Por eso es $O(1)$ y la traspuesta de un C-contiguo queda F-contigua. Slicing hace lo mismo: ajusta strides sin copiar.

```python
arr.T.strides       # (8, 24)   strides invertidos → vista, F-contigua
arr[::2].strides    # (48, 8)   el paso 2 duplica el stride del eje 0
```

## Casos de uso

```python
# Diagnosticar si el último eje es el contiguo (stride mínimo = itemsize)
arr.strides[-1] == arr.itemsize

# Saber si una vista comparte buffer (suele tener strides no naturales)
arr.flags['C_CONTIGUOUS']   # la forma robusta de comprobar contigüidad

# Ventanas deslizantes sin copia (avanzado, usar la API segura)
from numpy.lib.stride_tricks import sliding_window_view
sliding_window_view(np.arange(10), 3)   # (8, 3) sobre el mismo buffer
```

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| Asumir que strides están en elementos | Están en **bytes** | Dividir entre `itemsize` para pasar a elementos |
| `as_strided` con strides mal calculados | Lee fuera del buffer | Preferir `sliding_window_view` (segura) |
| Asignar `arr.strides = ...` a la ligera | Puede corromper memoria | No tocar manualmente salvo certeza total |

## Notas relacionadas

- [[concepto_ndarray]]
- [[concepto_contiguidad_memoria]]
- [[concepto_views_vs_copias]]
- [[ndarray.flags]]
