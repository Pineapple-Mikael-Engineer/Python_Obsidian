---
title: np.squeeze — Eliminar ejes de tamaño 1
aliases:
  - squeeze
  - np.squeeze
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

draft: false
---

# np.squeeze — Eliminar ejes de tamaño 1

## Firma de la función

```python
np.squeeze(
    a,
    axis=None
) -> ndarray
```

## Valor de retorno

Devuelve un [[concepto_ndarray|ndarray]] que es una [[concepto_views_vs_copias|vista]] de `a` con las dimensiones de tamaño 1 eliminadas. Los datos no cambian; solo se simplifica el [[concepto_shape|shape]].

| Shape entrada | `axis` | Shape salida |
|---------------|--------|--------------|
| `(1, 3, 1)` | `None` | `(3,)` |
| `(1, 3, 1)` | `0` | `(3, 1)` |
| `(1, 3, 1)` | `2` | `(1, 3)` |
| `(2, 3)` | `None` | `(2, 3)` (sin ejes de 1) |

```python
import numpy as np
a = np.array([[[1], [2], [3]]])   # shape (1, 3, 1)
np.squeeze(a).shape                # (3,)
```

## Parámetros en detalle

### `a` — array de entrada

Array de cualquier forma.

### `axis` — eje(s) a eliminar

- `None` (por defecto): elimina **todos** los ejes de tamaño 1.
- Entero o tupla: elimina solo esos ejes, que **deben** tener tamaño 1.

```python
a = np.zeros((1, 3, 1))
np.squeeze(a, axis=0).shape    # (3, 1)
np.squeeze(a, axis=(0, 2)).shape  # (3,)
```

## Casos de uso

### Quitar la dimensión de batch tras una predicción

```python
pred = modelo(x)        # shape (1, 10)
pred = np.squeeze(pred) # shape (10,)  → vector de logits
```

### Colapsar el resultado de una reducción con keepdims

```python
M = np.ones((4, 5))
s = M.sum(axis=1, keepdims=True)   # (4, 1)
s = np.squeeze(s, axis=1)          # (4,)
```

### Limpiar ejes sobrantes de un slice

```python
cubo = np.random.rand(10, 1, 10)
plano = np.squeeze(cubo)   # (10, 10)
```

## Buenas prácticas

1. Indica `axis` explícito cuando solo quieras quitar un eje concreto: evita sorpresas si otro eje vale 1.
2. Es la operación **inversa** de [[np.expand_dims]].
3. Útil tras reducciones con `keepdims=True` (ver [[concepto_axis_parametro]]).
4. Recuerda que devuelve vista; no copia los datos.

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| `cannot select an axis to squeeze out which has size not equal to one` | el `axis` indicado no vale 1 | comprobar el shape antes |
| Se eliminó un eje que querías conservar | `axis=None` quita todos los de tamaño 1 | pasar `axis` explícito |
| Escalar 0D inesperado | todos los ejes valían 1, ej. `(1,1,1)` | reconstruir con `reshape` si necesitas forma |

## Limitaciones

- Solo elimina ejes de **tamaño 1**; no fusiona ejes mayores (para eso, `reshape`).
- Si el array no tiene ejes unitarios, devuelve el mismo shape sin cambios.

## Notas relacionadas

- [[concepto_shape]]
- [[concepto_axis_parametro]]
- [[np.expand_dims]]
- [[np.reshape]]
- [[np.ravel]]
