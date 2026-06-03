---
title: ndarray.reshape — Cambiar la forma del array (método)
aliases:
  - reshape
  - ndarray.reshape
tags:
  - numpy
  - api/metodo
  - shape
lib: numpy
obj: ndarray
tipo: metodo
retorna: ndarray
inplace: false
draft: false
---

# ndarray.reshape — Cambiar la forma del array (método)

## Firma del método

```python
ndarray.reshape(*shape, order='C') -> ndarray
```

## Valor de retorno

Devuelve un `ndarray` con la nueva forma y los mismos datos. Casi siempre es una [[concepto_views_vs_copias|vista]] (comparte memoria); solo copia si el array no es contiguo en el `order` pedido.

| Llamada | Salida |
|---------|--------|
| `arange(12).reshape(3, 4)` | matriz 3×4 (vista) |
| `arange(12).reshape((3, 4))` | matriz 3×4 (tupla también válida) |
| `arange(12).reshape(3, -1)` | `(3, 4)` (dim inferida) |
| `arange(12).reshape(-1)` | `(12,)` (aplanado) |

## Equivalencia con np.reshape

Es la versión "bound" de la función: `arr.reshape(...) == np.reshape(arr, ...)`. Para el detalle completo de parámetros, `-1` inferido y `order`, ver [[np.reshape]].

```python
arr.reshape(3, 4)        # método
np.reshape(arr, (3, 4))  # función → mismo resultado
```

## Parámetros en detalle

A diferencia de la función `np.reshape` (que exige `newshape` como tupla), el **método admite enteros sueltos** como argumentos posicionales, sintaxis más cómoda en la práctica:

```python
arr = np.arange(12)
arr.reshape(3, 4)      # enteros sueltos (solo el método)
arr.reshape((3, 4))    # tupla (también funciona)
```

`order` (`'C'`, `'F'`, `'A'`) controla el recorrido; idéntico a la función.

## Casos de uso

```python
datos = np.arange(1, 13)       # (12,)
datos.reshape(3, 4)            # tabla 3 filas × 4 columnas

v = np.arange(3)
v.reshape(-1, 1)               # (3, 1) columna
v.reshape(1, -1)               # (1, 3) fila
```

## Buenas prácticas

1. Como método, encadena natural: `img.reshape(-1).mean()`.
2. Usa `-1` para inferir una dimensión y evitar cálculos manuales.
3. Recuerda que devuelve una **vista**: añade `.copy()` si necesitas independencia.
4. Para aplanar con intención explícita, [[ndarray.ravel]] comunica mejor.

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| `cannot reshape array of size N into shape (...)` | `producto(shape) != size` | ajustar dimensiones o usar `-1` |
| `can only specify one unknown dimension` | dos `-1` en la llamada | dejar solo uno |
| El original cambió inesperadamente | era una vista | usar `.copy()` |

## Notas relacionadas

- [[np.reshape]]
- [[ndarray.ravel]]
- [[concepto_shape]]
- [[concepto_views_vs_copias]]
