---
title: ndarray.squeeze — Eliminar ejes de tamaño 1 (método)
aliases:
  - squeeze
  - ndarray.squeeze
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

# ndarray.squeeze — Eliminar ejes de tamaño 1 (método)

## Firma del método

```python
ndarray.squeeze(axis=None) -> ndarray
```

## Valor de retorno

Devuelve una [[concepto_views_vs_copias|vista]] sin los ejes de longitud 1. Con `axis=None` elimina **todos** los ejes unitarios; con un eje (o tupla) concreto, solo esos. **No copia datos**.

| Shape entrada | Llamada | Shape salida |
|---------------|---------|--------------|
| `(1, 3, 1)` | `arr.squeeze()` | `(3,)` |
| `(1, 3, 1)` | `arr.squeeze(0)` | `(3, 1)` |
| `(1, 3, 1)` | `arr.squeeze(2)` | `(1, 3)` |
| `(1, 3, 1)` | `arr.squeeze((0, 2))` | `(3,)` |

## Equivalencia con np.squeeze

Versión "bound" de la función: `arr.squeeze(...) == np.squeeze(arr, ...)`. Ver [[np.squeeze]].

```python
arr.squeeze()           # método
np.squeeze(arr)         # función → mismo resultado
```

## Parámetros en detalle

`axis` selecciona qué eje(s) unitario(s) eliminar:

| Valor | Comportamiento |
|-------|----------------|
| `None` (defecto) | quita todos los ejes de tamaño 1 |
| entero | quita ese eje (debe medir 1) |
| tupla de enteros | quita esos ejes (todos deben medir 1) |

```python
a = np.zeros((1, 3, 1))
a.squeeze().shape        # (3,)
a.squeeze(0).shape       # (3, 1)
a.squeeze(1)             # ValueError: el eje 1 mide 3, no 1
```

## Casos de uso

```python
# Quitar la dimensión de batch tras una predicción de un solo elemento:
pred = np.random.rand(1, 10)
pred.squeeze().shape         # (10,)

# Limpiar ejes sobrantes tras indexar con slices:
M = np.arange(12).reshape(3, 4)
col = M[:, 1:2]              # (3, 1)
col.squeeze().shape         # (3,)
```

## Buenas prácticas

1. Para quitar un eje **concreto** y evitar sorpresas, pasa `axis` explícito en lugar de `None`.
2. Operación inversa: añadir un eje de tamaño 1 con [[np.expand_dims]] o `reshape`.
3. Es una vista: escribir en el resultado modifica el original.

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| `ValueError: cannot select an axis to squeeze out which has size not equal to one` | el `axis` indicado no mide 1 | revisar la shape antes de squeeze |
| Resultado con menos ejes de los esperados | `squeeze()` quitó todos los unitarios | pasar `axis` específico |

## Notas relacionadas

- [[np.squeeze]]
- [[np.expand_dims]]
- [[concepto_views_vs_copias]]
- [[concepto_shape]]
