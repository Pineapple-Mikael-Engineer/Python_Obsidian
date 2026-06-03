---
title: ndarray.transpose — Permutar los ejes (método)
aliases:
  - transpose
  - ndarray.transpose
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

# ndarray.transpose — Permutar los ejes (método)

## Firma del método

```python
ndarray.transpose(*axes) -> ndarray
```

## Valor de retorno

Devuelve una [[concepto_views_vs_copias|vista]] con los ejes permutados. **No copia datos**: solo reordena los `strides`, coste casi nulo.

| Shape entrada | Llamada | Shape salida |
|---------------|---------|--------------|
| `(2, 3)` | `arr.transpose()` | `(3, 2)` (invierte) |
| `(2, 3, 4)` | `arr.transpose()` | `(4, 3, 2)` |
| `(2, 3, 4)` | `arr.transpose(0, 2, 1)` | `(2, 4, 3)` |
| `(2, 3, 4)` | `arr.transpose((1, 0, 2))` | `(3, 2, 4)` |

## Equivalencia con np.transpose

Versión "bound" de la función: `arr.transpose(...) == np.transpose(arr, ...)`. Detalle de `axes` en [[np.transpose]].

```python
arr.transpose(1, 0, 2)        # método
np.transpose(arr, (1, 0, 2))  # función → mismo resultado
```

## El atajo `.T`

Para invertir **todos** los ejes, el atributo `.T` equivale a `transpose()` sin argumentos y es más breve:

```python
M.T                # == M.transpose()
M.T.shape          # ejes invertidos
```

> En un array 1D, tanto `.T` como `transpose()` no hacen nada: `(3,)` sigue siendo `(3,)`.

## Parámetros en detalle

A diferencia de `np.transpose` (que recibe `axes` como tupla), el **método admite los ejes como enteros sueltos**:

```python
T = np.ones((2, 3, 4))
T.transpose(1, 0, 2).shape     # (3, 2, 4) — enteros sueltos
T.transpose((1, 0, 2)).shape   # (3, 2, 4) — tupla también vale
```

`axes` debe ser una **permutación** de `range(ndim)`: cada eje exactamente una vez.

## Casos de uso

```python
A = np.random.rand(3, 5)
A.T @ A              # (5, 3) @ (3, 5) → (5, 5)

img = np.random.rand(224, 224, 3)   # HWC
img.transpose(2, 0, 1).shape        # CHW → (3, 224, 224)
```

## Buenas prácticas

1. Para invertir todo, usa `.T`; para permutaciones concretas, `transpose(...)`.
2. Si solo intercambias **dos** ejes, [[ndarray.swapaxes]] es más legible.
3. Es una vista: escribir en el resultado modifica el original.
4. Tras transponer el array deja de ser C-contiguo; usa `np.ascontiguousarray` si una librería lo exige.

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| `.T` no hace nada | el array es 1D | usar `reshape(-1, 1)` |
| `ValueError: axes don't match array` | `axes` no es permutación de `range(ndim)` | incluir cada eje una vez |
| Resultado no contiguo rompe otra función | vista con strides reordenados | `np.ascontiguousarray(resultado)` |

## Notas relacionadas

- [[np.transpose]]
- [[ndarray.swapaxes]]
- [[concepto_views_vs_copias]]
- [[concepto_shape]]
