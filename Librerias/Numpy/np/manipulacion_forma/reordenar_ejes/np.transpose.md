---
title: np.transpose — Reordenar (permutar) los ejes
aliases:
  - transpose
  - np.transpose
  - transponer
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
  - concepto_views_vs_copias

draft: false
---

# np.transpose — Reordenar (permutar) los ejes

## Firma de la función

```python
np.transpose(
    a,
    axes=None
) -> ndarray
```

## Valor de retorno

Devuelve una [[concepto_views_vs_copias|vista]] de `a` con los ejes permutados. **No copia datos**: solo reordena los `strides`, por lo que es una operación de coste casi nulo.

| Shape entrada | `axes` | Shape salida |
|---------------|--------|--------------|
| `(2, 3)` | `None` | `(3, 2)` (invierte) |
| `(2, 3, 4)` | `None` | `(4, 3, 2)` (invierte todo) |
| `(2, 3, 4)` | `(0, 2, 1)` | `(2, 4, 3)` |
| `(2, 3, 4)` | `(1, 0, 2)` | `(3, 2, 4)` |

```python
import numpy as np
M = np.array([[1, 2, 3],
              [4, 5, 6]])      # (2, 3)
np.transpose(M)
# array([[1, 4],
#        [2, 5],
#        [3, 6]])              # (3, 2)
```

## El atajo `.T`

Para invertir todos los ejes, el atributo `.T` es equivalente y más breve:

```python
M.T            # igual que np.transpose(M)
M.T.shape      # (3, 2)
```

> Ojo: en un array **1D**, `.T` no hace nada (`(3,)` sigue siendo `(3,)`). Para una columna usa [[np.expand_dims]] o `reshape(-1, 1)`.

## Parámetros en detalle

### `a` — array de entrada

Array de cualquier dimensión.

### `axes` — nueva ordenación de ejes

Tupla que es una **permutación** de `range(ndim)`. La posición `i` del resultado toma el eje `axes[i]` del original. Si es `None`, invierte el orden completo.

```python
T = np.ones((2, 3, 4))
np.transpose(T, (1, 0, 2)).shape   # (3, 2, 4)  → intercambia ejes 0 y 1
np.transpose(T, (2, 1, 0)).shape   # (4, 3, 2)  → equivale a None
```

## Casos de uso

### Transponer una matriz para multiplicación

```python
A = np.random.rand(3, 5)
B = np.random.rand(3, 5)
C = A.T @ B          # (5, 3) @ (3, 5) → (5, 5)
```

### Cambiar convención de imagen (HWC ↔ CHW)

```python
img = np.random.rand(224, 224, 3)     # alto, ancho, canal
chw = np.transpose(img, (2, 0, 1))    # canal, alto, ancho → (3, 224, 224)
```

### Intercambiar solo dos ejes

```python
T = np.ones((2, 3, 4))
np.transpose(T, (0, 2, 1)).shape   # (2, 4, 3)
# equivalente más legible: np.swapaxes(T, 1, 2)
```

## Buenas prácticas

1. Para invertir todos los ejes, usa `.T`; para permutaciones concretas, `transpose(a, axes)`.
2. Si solo intercambias **dos** ejes, [[np.swapaxes]] o [[np.moveaxis]] son más claros.
3. Recuerda que es una vista: escribir en el resultado modifica el original.
4. Tras transponer, el array deja de ser C-contiguo; usa `np.ascontiguousarray` si una librería lo exige (ver [[concepto_contiguidad_memoria]]).

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| `.T` no hace nada | el array es 1D | usar `reshape(-1, 1)` o [[np.expand_dims]] |
| `ValueError: axes don't match array` | `axes` no es permutación de `range(ndim)` | incluir cada eje exactamente una vez |
| Resultado no contiguo rompe otra función | transpose devuelve vista con strides reordenados | `np.ascontiguousarray(resultado)` |

## Limitaciones

- No copia datos: si necesitas un layout físico distinto, fuerza la copia.
- Para mover **un** eje a otra posición conservando el orden relativo del resto, [[np.moveaxis]] es preferible.

## Notas relacionadas

- [[concepto_shape]]
- [[concepto_views_vs_copias]]
- [[concepto_contiguidad_memoria]]
- [[np.swapaxes]]
- [[np.moveaxis]]
- [[np.reshape]]
