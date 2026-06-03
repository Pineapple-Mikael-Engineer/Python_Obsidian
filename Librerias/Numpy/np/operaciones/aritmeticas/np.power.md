---
title: np.power — Potencia elemento a elemento (ufunc)
aliases:
  - power
  - np.power
tags:
  - numpy
  - api/funcion
  - transformaciones

# --- Clasificación ---
lib: numpy
mod: np
tipo: funcion

# --- Comportamiento ---
retorna: ndarray
inplace: false

# --- Dependencias ---
requiere:
  - concepto_ufuncs
  - concepto_dtype

draft: false
---

# np.power — Potencia elemento a elemento (ufunc)

## Firma de la función

```python
np.power(x1, x2, /, out=None, *, where=True, dtype=None) -> ndarray
```

## Valor de retorno

Devuelve `x1 ** x2` elemento a elemento (base `x1`, exponente `x2`), con broadcasting. Es la [[concepto_ufuncs|ufunc]] del operador `**`.

| `x1` | `x2` | Resultado |
|------|------|-----------|
| `[1, 2, 3]` | `2` | `[1, 4, 9]` |
| `2` | `[1, 2, 3]` | `[2, 4, 8]` |
| `[1, 2, 3]` | `[3, 2, 1]` | `[1, 4, 3]` |

```python
import numpy as np
np.power([1, 2, 3], 2)   # array([1, 4, 9])
```

## Parámetros en detalle

Idénticos a [[np.add]]: `out`, `where`, `dtype`.

## ⚠️ Exponentes negativos con enteros

`np.power` con base **entera** y exponente **negativo** lanza error (no puede devolver fracciones en int):

```python
np.power(2, -1)              # ValueError (enteros)
np.power(2.0, -1)            # 0.5 (flotante OK)
```

## Casos de uso

### Elevar al cuadrado / raíces

```python
np.power(x, 2)      # cuadrado (o np.square, más rápido)
np.power(x, 0.5)    # raíz (o np.sqrt)
```

### Decaimiento exponencial discreto

```python
np.power(0.9, np.arange(10))   # [1, 0.9, 0.81, ...]
```

## Buenas prácticas

1. Para el cuadrado usa [[np.square]]; para raíz, [[np.sqrt]] (más directas y rápidas).
2. Usa base flotante si el exponente puede ser negativo o fraccionario.
3. Vigila el **overflow**: las potencias crecen muy rápido.

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| `Integers to negative integer powers are not allowed` | base int, exp negativo | usar base `float` |
| Overflow | potencias grandes | `dtype=float64` |

## Limitaciones

- Restricción de exponentes negativos con enteros.

## Notas relacionadas

- [[concepto_ufuncs]]
- [[np.square]]
- [[np.sqrt]]
- [[np.exp]]
