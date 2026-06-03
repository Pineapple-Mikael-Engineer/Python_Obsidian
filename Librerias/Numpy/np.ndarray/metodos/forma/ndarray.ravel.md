---
title: ndarray.ravel — Aplanar a 1D (vista si es posible)
aliases:
  - ravel
  - ndarray.ravel
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

# ndarray.ravel — Aplanar a 1D (vista si es posible)

## Firma del método

```python
ndarray.ravel(order='C') -> ndarray
```

## Valor de retorno

Devuelve un `ndarray` **1D** con todos los elementos. Es una [[concepto_views_vs_copias|vista]] siempre que la memoria lo permita; solo copia cuando el aplanado no puede expresarse con los `strides` actuales (p. ej. tras ciertos transpose en `order='C'`).

| Entrada | Llamada | Salida |
|---------|---------|--------|
| `(2, 3)` C-contiguo | `arr.ravel()` | `(6,)` vista |
| `(2, 3)` transpuesto | `arr.ravel()` | `(6,)` copia |
| cualquier shape | `arr.ravel('F')` | `(n,)` orden columnas |

## Equivalencia con np.ravel

Versión "bound" de la función: `arr.ravel(...) == np.ravel(arr, ...)`. Detalle de `order` en [[np.ravel]].

```python
arr.ravel()        # método
np.ravel(arr)      # función → mismo resultado
```

## Parámetros en detalle

`order` controla el recorrido al aplanar:

| Valor | Significado |
|-------|-------------|
| `'C'` (defecto) | por filas (última dimensión primero) |
| `'F'` | por columnas (estilo Fortran) |
| `'A'` | `'F'` si es Fortran-contiguo, si no `'C'` |
| `'K'` | en el orden en que están en memoria |

## Casos de uso

```python
M = np.arange(6).reshape(2, 3)
M.ravel()           # array([0, 1, 2, 3, 4, 5]) — vista
M.ravel()[0] = 99   # ¡modifica M si es vista!

img = np.random.rand(28, 28)
img.ravel().shape   # (784,)
```

## Buenas prácticas

1. Usa `ravel` cuando aplanar barato (vista) es aceptable y no necesitas independencia.
2. Si **siempre** quieres una copia independiente, usa [[ndarray.flatten]].
3. No asumas vista o copia: si vas a escribir en el resultado y no quieres tocar el original, fuerza `.copy()`.

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| El original cambió al escribir en el aplanado | `ravel` devolvió vista | usar `flatten` o `.copy()` |
| Orden de elementos inesperado | `order` por defecto `'C'` | revisar `order='F'` |

## Notas relacionadas

- [[np.ravel]]
- [[ndarray.flatten]]
- [[concepto_views_vs_copias]]
- [[concepto_shape]]
