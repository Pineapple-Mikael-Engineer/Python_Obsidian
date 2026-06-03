---
title: np.concatenate — Unir arrays a lo largo de un eje existente
aliases:
  - concatenate
  - np.concatenate
  - concatenar
tags:
  - numpy
  - api/funcion
  - manipulacion

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
  - concepto_axis_parametro

draft: false
---

# np.concatenate — Unir arrays a lo largo de un eje existente

## Firma de la función

```python
np.concatenate(
    (a1, a2, ...),
    axis=0,
    out=None,
    dtype=None
) -> ndarray
```

## Valor de retorno

Devuelve un **nuevo** [[concepto_ndarray|ndarray]] (copia) que une la secuencia de arrays a lo largo del [[concepto_axis_parametro|eje]] indicado. El eje de unión crece; los demás deben coincidir.

| Arrays | `axis` | Shapes entrada | Shape salida |
|--------|--------|----------------|--------------|
| `a, b` | `0` | `(2,3)` y `(4,3)` | `(6, 3)` |
| `a, b` | `1` | `(2,3)` y `(2,5)` | `(2, 8)` |
| `a, b` (1D) | `0` | `(3,)` y `(2,)` | `(5,)` |

```python
import numpy as np
a = np.array([[1, 2], [3, 4]])
b = np.array([[5, 6]])
np.concatenate((a, b), axis=0)
# array([[1, 2],
#        [3, 4],
#        [5, 6]])              # (3, 2)
```

## Regla fundamental

> Todos los arrays deben tener el **mismo shape excepto en el eje de concatenación**.

```python
a = np.ones((2, 3))
b = np.ones((2, 5))
np.concatenate((a, b), axis=1)   # OK → (2, 8): coinciden en eje 0
np.concatenate((a, b), axis=0)   # Error → difieren en eje 1 (3 vs 5)
```

## Parámetros en detalle

### `(a1, a2, ...)` — secuencia de arrays

Tupla o lista de arrays. **Todos deben tener el mismo `ndim`**. `concatenate` no crea ejes nuevos (para eso, [[np.stack]]).

### `axis` — eje de unión

Entero. Es el eje que crece. Con `axis=None`, aplana todos los arrays y concatena en 1D.

```python
a = np.array([[1, 2], [3, 4]])
b = np.array([[5, 6], [7, 8]])
np.concatenate((a, b), axis=None)   # [1, 2, 3, 4, 5, 6, 7, 8]
```

### `dtype` — tipo del resultado (NumPy ≥ 1.20)

Fuerza el [[concepto_dtype|dtype]] de salida, evitando una conversión posterior.

## concatenate vs stack vs los atajos

| Función | Qué hace | Ejes |
|---------|----------|------|
| `np.concatenate` | une en un eje **existente** | mantiene `ndim` |
| [[np.stack]] | une creando un eje **nuevo** | `ndim + 1` |
| [[np.vstack]] | concatena en `axis=0` (vertical) | atajo |
| [[np.hstack]] | concatena en `axis=1` (horizontal) | atajo |

## Casos de uso

### Acumular bloques de datos por filas

```python
bloques = [np.random.rand(10, 4) for _ in range(5)]
todo = np.concatenate(bloques, axis=0)   # (50, 4)
```

### Añadir columnas a una matriz

```python
X = np.ones((100, 3))
nueva = np.zeros((100, 1))
X = np.concatenate((X, nueva), axis=1)   # (100, 4)
```

### Unir señales 1D

```python
señal = np.concatenate((tramo1, tramo2, tramo3))
```

## Buenas prácticas

1. Concatenar dentro de un bucle es costoso (copia en cada paso): acumula en una lista y concatena **una sola vez** al final.
2. Verifica que los shapes coinciden en todos los ejes salvo el de unión antes de llamar.
3. Para unir creando un eje nuevo (ej. apilar imágenes en un batch), usa [[np.stack]].
4. Para 2D, [[np.vstack]] / [[np.hstack]] se leen mejor que `axis=0/1`.

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| `all the input array dimensions except for the concatenation axis must match exactly` | shapes incompatibles fuera del eje | revisar/ajustar dimensiones |
| `zero-dimensional arrays cannot be concatenated` | se pasaron escalares | convertir con `np.atleast_1d` |
| Rendimiento pésimo | concatenar en bucle | acumular en lista y concatenar al final |
| `ndim` no coincide | mezclar 1D con 2D | igualar dimensiones (ej. `expand_dims`) o usar `stack` |

## Limitaciones

- No crea ejes nuevos: para apilar a una dimensión superior está [[np.stack]].
- Siempre copia: no existe una versión vista.
- Requiere igual `ndim` en todas las entradas.

## Notas relacionadas

- [[concepto_shape]]
- [[concepto_axis_parametro]]
- [[np.stack]]
- [[np.vstack]]
- [[np.hstack]]
- [[np.split]]
