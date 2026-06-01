---
title: ndarray.astype — Convertir a otro dtype (siempre copia)
aliases:
  - astype
  - ndarray.astype
tags:
  - numpy
  - api/metodo
  - dtype
lib: numpy
obj: ndarray
tipo: metodo
retorna: ndarray
inplace: false
draft: false
---

# ndarray.astype — Convertir a otro dtype (siempre copia)

## Firma del método

```python
ndarray.astype(
    dtype,
    order='K',
    casting='unsafe',
    subok=True,
    copy=True
) -> ndarray
```

## Valor de retorno

Devuelve un `ndarray` nuevo con el **mismo shape** y los datos reinterpretados al nuevo dtype. **Por defecto siempre devuelve una copia independiente** (buffer propio), incluso si el dtype destino coincide con el origen.

| Entrada | Llamada | Salida |
|---------|---------|--------|
| `[1.7, 2.9]` float64 | `arr.astype(np.int32)` | `[1, 2]` int32 (trunca) |
| `[0, 1, 2]` int | `arr.astype(bool)` | `[False, True, True]` |
| `[1, 0]` int | `arr.astype(np.float64)` | `[1., 0.]` float64 |

```python
import numpy as np
arr = np.array([1.7, 2.9, 3.1])
out = arr.astype(np.int32)
out         # array([1, 2, 3], dtype=int32)  → trunca, NO redondea
out.base is arr   # False → copia independiente
```

## Equivalencia

No existe `np.astype` clásico (existe `np.astype()` desde NumPy 2.0, pero la vía idiomática es el método). Para el modelo de tipos completo ver [[concepto_dtype]].

## Parámetros en detalle

### `dtype` — tipo destino

Cualquier especificador de dtype: clase (`np.int32`), string (`'float32'`, `'<i4'`) o `np.dtype`.

```python
arr.astype('float32')   # equivalente a np.float32
arr.astype('U10')       # texto Unicode de hasta 10 chars
```

### `casting` — política de conversión

| `casting` | Permite |
|-----------|---------|
| `'no'` | ninguna conversión |
| `'equiv'` | solo cambios de byte-order |
| `'safe'` | solo conversiones sin pérdida |
| `'same_kind'` | dentro del mismo kind (float64→float32) |
| `'unsafe'` (defecto) | cualquiera, aunque pierda datos |

```python
a = np.array([1.5, 2.5])
a.astype(np.int32, casting='safe')   # TypeError → float→int no es safe
a.astype(np.int32)                   # OK con 'unsafe' por defecto
```

### `copy` — evitar copia si ya coincide

Con `copy=False`, si el array ya tiene el dtype/order pedidos, devuelve el **mismo** objeto (no copia). En cualquier otro caso copia igual.

```python
arr = np.array([1, 2], dtype=np.int32)
arr.astype(np.int32, copy=False) is arr   # True → sin copia
arr.astype(np.int64, copy=False) is arr   # False → debe copiar
```

### `order`, `subok`

`order` (`'C'`, `'F'`, `'A'`, `'K'`) fija la disposición en memoria del resultado. `subok=True` conserva subclases del array.

## Casos de uso

### Reducir memoria

```python
img = np.zeros((1000, 1000))          # float64 → 8 MB
img8 = img.astype(np.uint8)           # uint8   → 1 MB
```

### Redondear antes de truncar

```python
arr = np.array([3.99, 1.01])
arr.astype(np.int32)            # [3, 1]  → trunca
np.round(arr).astype(np.int32) # [4, 1]  → redondea primero
```

### Preparar datos para una operación tipada

```python
ids = np.array(['10', '20', '30'])
ids.astype(np.int64)           # [10, 20, 30]  → parsea texto a int
```

## Buenas prácticas

1. Recuerda que de float a int **trunca hacia cero**, no redondea: usa `np.round` antes si lo necesitas.
2. Cuida el overflow al bajar de tamaño (`int64`→`int8`): los valores fuera de rango dan wrap-around silencioso.
3. Como siempre copia, evita llamarlo en bucles calientes; conviértelo una sola vez.

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| Esperar redondeo float→int | `astype` trunca | `np.round(arr).astype(int)` |
| `TypeError` de casting | conversión no permitida por `casting` | usar `casting='unsafe'` (por defecto) |
| Overflow silencioso | dtype destino demasiado pequeño | elegir un dtype con rango suficiente |
| Asumir vista | `astype` copia siempre | leer el array devuelto, no el original |

## Notas relacionadas

- [[concepto_dtype]]
- [[concepto_views_vs_copias]]
- [[ndarray.dtype]]
- [[ndarray.copy]]
