---
title: np.multiply — Producto elemento a elemento (ufunc)
aliases:
  - multiply
  - np.multiply
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
  - concepto_broadcasting

draft: false
---

# np.multiply — Producto elemento a elemento (ufunc)

## Firma de la función

```python
np.multiply(x1, x2, /, out=None, *, where=True, dtype=None) -> ndarray
```

## Valor de retorno

Devuelve `x1 * x2` elemento a elemento, con [[concepto_broadcasting|broadcasting]]. Es la [[concepto_ufuncs|ufunc]] del operador `*`.

| `x1` | `x2` | Resultado |
|------|------|-----------|
| `[1, 2, 3]` | `[4, 5, 6]` | `[4, 10, 18]` |
| `[1, 2, 3]` | `10` | `[10, 20, 30]` |

```python
import numpy as np
np.multiply([1, 2, 3], [4, 5, 6])   # array([ 4, 10, 18])
```

## ⚠️ No es producto matricial

`np.multiply` (y `*`) es **elemento a elemento**. Para producto matricial usa `@` o `np.matmul`/`np.dot`:

```python
A * B          # Hadamard (elemento a elemento)
A @ B          # producto matricial
```

## Parámetros en detalle

Idénticos a [[np.add]]: `out`, `where`, `dtype`.

## Casos de uso

### Escalar un array / aplicar pesos

```python
ponderado = np.multiply(valores, pesos)
```

## Buenas prácticas

1. Usa `*` salvo que necesites `out`/`where`.
2. No lo confundas con producto matricial (`@`).
3. Vigila el overflow con enteros.

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| Esperar producto matricial | `*` es elemento a elemento | usar `@` o `np.matmul` |
| `could not be broadcast` | shapes incompatibles | revisar dimensiones |

## Limitaciones

- Elemento a elemento; para producto-reducción usa [[np.prod]].

## Notas relacionadas

- [[concepto_ufuncs]]
- [[np.add]]
- [[np.divide]]
- [[np.prod]]
