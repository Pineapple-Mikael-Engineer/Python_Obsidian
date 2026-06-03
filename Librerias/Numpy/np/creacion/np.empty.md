---
title: np.empty — Array sin inicializar (memoria reservada)
aliases:
  - empty
  - np.empty
tags:
  - numpy
  - api/funcion
  - creacion

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
  - concepto_dtype

draft: false
---

# np.empty — Array sin inicializar (memoria reservada)

## Firma de la función

```python
np.empty(
    shape,
    dtype=float,
    order='C',
    *,
    like=None
) -> ndarray
```

## Valor de retorno

Devuelve un [[concepto_ndarray|ndarray]] del `shape` indicado **sin inicializar**: reserva la memoria pero no escribe valores, por lo que su contenido es **basura** (lo que hubiera en esa RAM). Es la más rápida de las funciones de creación.

| Llamada | Shape | Contenido |
|---------|-------|-----------|
| `np.empty(3)` | `(3,)` | valores arbitrarios |
| `np.empty((2, 2))` | `(2, 2)` | valores arbitrarios |

```python
import numpy as np
np.empty(3)   # p.ej. array([6.9e-310, 2.3e-313, 0.0])  → NO son ceros
```

## Cuándo usarla (y cuándo no)

| Situación | Función |
|-----------|---------|
| Vas a **sobrescribir cada elemento** después | `np.empty` (evita inicializar dos veces) |
| Necesitas ceros | [[np.zeros]] |
| Necesitas un valor constante | [[np.full]] |

> ⚠️ Nunca leas un `np.empty` antes de escribirlo: su contenido no está definido.

## Parámetros en detalle

### `shape`, `dtype`, `order`

Idénticos a [[np.zeros]]: `shape` define la forma, `dtype` por defecto `float`, `order` la disposición en memoria (ver [[concepto_dtype]]).

## Casos de uso

### Preasignar y llenar en un bucle

```python
n = 1000
out = np.empty(n)             # sin coste de inicializar a 0
for i in range(n):
    out[i] = calcular(i)      # se llena por completo
```

### Buffer de salida para una operación

```python
res = np.empty_like(a)        # mismo shape/dtype que a
np.multiply(a, 2, out=res)    # escribe directamente en res
```

## Buenas prácticas

1. Úsala solo si **garantizas** sobrescribir todo el array.
2. Para copiar shape/dtype de otro array, [[np.empty_like]].
3. Si dudas, usa [[np.zeros]]: la diferencia de rendimiento rara vez importa y evitas bugs.

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| Valores "aleatorios" inesperados | se leyó antes de escribir | inicializar con [[np.zeros]]/[[np.full]] |
| Asumir que son ceros | `empty` no inicializa | usar [[np.zeros]] |

## Limitaciones

- Contenido indefinido hasta que se escribe.
- El ahorro frente a `zeros` solo se nota con arrays muy grandes.

## Notas relacionadas

- [[concepto_shape]]
- [[concepto_dtype]]
- [[np.zeros]]
- [[np.full]]
- [[np.empty_like]]
