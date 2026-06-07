---
title: np.ndarray — metodos de forma
tags:
  - numpy
  - indice
draft: false
---

# np.ndarray — metodos de forma

Los 6 metodos de forma modifican la estructura dimensional del array desde el propio objeto. Ninguno cambia los datos; todos reorganizan como se navegan.

## Tabla de metodos

| Metodo | Firma resumida | Descripcion |
|--------|---------------|-------------|
| [[ndarray.reshape]] | `arr.reshape(*shape)` | Nueva forma; casi siempre vista |
| [[ndarray.ravel]] | `arr.ravel(order='C')` | Aplana a 1D; vista si posible |
| [[ndarray.flatten]] | `arr.flatten(order='C')` | Aplana a 1D; siempre copia |
| [[ndarray.transpose]] | `arr.transpose(*axes)` | Permuta todos los ejes |
| [[ndarray.swapaxes]] | `arr.swapaxes(ax1, ax2)` | Intercambia dos ejes |
| [[ndarray.squeeze]] | `arr.squeeze(axis=None)` | Elimina ejes de tamaño 1 |

## Diferencia con las funciones `np.X`

Cada metodo tiene una funcion NumPy equivalente. La semantica es identica; solo cambia la sintaxis:

| Metodo (objeto) | Funcion (modulo) |
|-----------------|-----------------|
| `arr.reshape(3, 4)` | `np.reshape(arr, (3, 4))` |
| `arr.ravel()` | `np.ravel(arr)` |
| `arr.flatten()` | *(sin equivalente directo; usar `np.ravel` + `.copy()`)* |
| `arr.transpose()` | `np.transpose(arr)` |
| `arr.swapaxes(0, 1)` | `np.swapaxes(arr, 0, 1)` |
| `arr.squeeze()` | `np.squeeze(arr)` |

## `flatten` vs `ravel`

Ambos producen un array 1D con los mismos datos, pero difieren en si copian:

| | `ravel` | `flatten` |
|-|---------|-----------|
| Devuelve | Vista si el array es contiguo; copia si no | **Siempre copia** |
| Modifica el original | Si se modifica la vista, si | Nunca |
| Uso tipico | Calculo temporal, encadenamiento | Cuando se necesita independencia garantizada |

```python
a = np.array([[1, 2], [3, 4]])
r = a.ravel()    # vista — r[0] = 99 modifica a
f = a.flatten()  # copia — f[0] = 99 no afecta a
```
