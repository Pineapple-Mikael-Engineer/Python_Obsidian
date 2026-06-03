---
title: np.abs — Valor absoluto (ufunc)
aliases:
  - abs
  - np.abs
  - absolute
  - valor absoluto
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

draft: false
---

# np.abs — Valor absoluto (ufunc)

## Firma de la función

```python
np.abs(x, /, out=None, *, where=True, dtype=None) -> ndarray
```

`np.abs` es un alias de `np.absolute`.

## Valor de retorno

Devuelve el **valor absoluto** elemento a elemento. Para números complejos devuelve el **módulo** `√(re²+im²)`.

| `x` | Resultado |
|-----|-----------|
| `[-1, 2, -3]` | `[1, 2, 3]` |
| `3 + 4j` | `5.0` (módulo) |

```python
import numpy as np
np.abs([-1, -2, 3])    # array([1, 2, 3])
np.abs(3 + 4j)         # 5.0
```

## abs vs fabs

| Función | Complejos | dtype salida |
|---------|-----------|--------------|
| `np.abs` | sí (módulo) | conserva (int→int) |
| [[np.fabs]] | no (error) | siempre float |

## Parámetros en detalle

`x` cualquiera (real o complejo); `out`, `where`, `dtype` como toda ufunc (ver [[np.add]]).

## Casos de uso

### Error absoluto

```python
mae = np.mean(np.abs(prediccion - objetivo))
```

### Magnitud de números complejos

```python
magnitud = np.abs(senal_compleja)
```

## Buenas prácticas

1. Funciona con enteros, flotantes y complejos (módulo).
2. Si necesitas siempre flotante y solo reales, [[np.fabs]].
3. Cuidado: `abs(int_min)` puede desbordar (ej. `int8` -128).

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| Overflow en el mínimo entero | `-128` en int8 no tiene opuesto | usar tipo mayor o float |

## Limitaciones

- Posible overflow en el valor entero más negativo.

## Notas relacionadas

- [[concepto_ufuncs]]
- [[np.fabs]]
- [[np.sign]]
