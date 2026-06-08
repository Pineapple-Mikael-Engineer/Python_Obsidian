---
title: np.ndarray — metodos de forma
tags:
  - numpy
  - indice
draft: false
---

# np.ndarray — metodos de forma

6 metodos para reorganizar la estructura dimensional del array desde el propio objeto. Ninguno cambia los datos numericos; todos reorganizan como se navegan esos datos en memoria. La distincion mas importante entre ellos es si devuelven una **vista** (comparten el mismo buffer de bytes con el original) o una **copia** (buffer independiente): modificar una vista modifica el original; modificar una copia no.

## Tabla de metodos

| Metodo | Firma resumida | Vista / Copia | Descripcion |
|--------|---------------|---------------|-------------|
| [[ndarray.reshape]] | `arr.reshape(*shape)` | Vista si contiguo; copia si no | Asigna nueva forma compatible con el mismo numero de elementos |
| [[ndarray.ravel]] | `arr.ravel(order='C')` | Vista si posible | Aplana a 1D; devuelve vista cuando el array es contiguo |
| [[ndarray.flatten]] | `arr.flatten(order='C')` | Siempre copia | Aplana a 1D con independencia garantizada del original |
| [[ndarray.transpose]] | `arr.transpose(*axes)` | Siempre vista | Permuta todos los ejes; sin argumentos equivale a `.T` |
| [[ndarray.swapaxes]] | `arr.swapaxes(ax1, ax2)` | Siempre vista | Intercambia exactamente dos ejes |
| [[ndarray.squeeze]] | `arr.squeeze(axis=None)` | Siempre vista | Elimina dimensiones de tamaño 1 |

## `flatten` vs `ravel`

Ambos producen un array 1D con los mismos datos, pero difieren en si copian. La eleccion es de intencion:

| | `ravel` | `flatten` |
|-|---------|-----------|
| Devuelve | Vista si el array es contiguo; copia si no | Siempre copia |
| Modifica el original | Si se modifica la vista, si | Nunca |
| Uso tipico | Calculo temporal, encadenamiento | Cuando se necesita que la version aplanada sea independiente |

```python
a = np.array([[1, 2], [3, 4]])
r = a.ravel()    # vista — r[0] = 99 cambia a[0, 0]
f = a.flatten()  # copia — f[0] = 99 no afecta a
```

## `reshape` con `-1`

Cuando uno de los valores de la nueva forma es `-1`, NumPy lo infiere automaticamente a partir de los demas:

```python
a = np.arange(12)
a.reshape(3, -1)   # → shape (3, 4); NumPy calcula que 12/3 = 4
a.reshape(-1)      # → shape (12,); equivalente a ravel
```

## `transpose` vs `swapaxes`

`swapaxes` es un caso especial de `transpose` limitado a exactamente dos ejes:

```python
a = np.zeros((2, 3, 4))
a.transpose(2, 0, 1).shape  # → (4, 2, 3)
a.swapaxes(0, 2).shape      # → (4, 3, 2)
```

## `squeeze` — cuando usarlo

Util para limpiar el output de funciones que devuelven shapes con dimensiones unitarias residuales, como `(1, n, 1)` o `(n, 1)`:

```python
a = np.zeros((1, 3, 1))
a.squeeze().shape         # → (3,)
a.squeeze(axis=0).shape   # → (3, 1)  — solo elimina el eje 0
```

## Diferencia con las funciones `np.X`

Cada metodo tiene una funcion NumPy equivalente en el modulo de manipulacion de forma. La semantica es identica; solo cambia la sintaxis:

| Metodo (objeto) | Funcion (modulo) |
|-----------------|-----------------|
| `arr.reshape(3, 4)` | `np.reshape(arr, (3, 4))` |
| `arr.ravel()` | `np.ravel(arr)` |
| `arr.flatten()` | *(sin equivalente directo; usar `np.ravel(arr).copy()`)* |
| `arr.transpose()` | `np.transpose(arr)` |
| `arr.swapaxes(0, 1)` | `np.swapaxes(arr, 0, 1)` |
| `arr.squeeze()` | `np.squeeze(arr)` |
