---
title: ndarray.base — Array dueño de la memoria de una vista
aliases:
  - base
  - ndarray.base
tags:
  - numpy
  - api/atributo
  - memoria
lib: numpy
mod: np.ndarray
tipo: atributo
draft: false
---

# ndarray.base — Array dueño de la memoria de una vista

Referencia al array del que **esta vista toma su memoria**. Si el array es una vista, `base` apunta al objeto que posee el buffer; si tiene datos propios (es una copia o un array original), `base` es `None`. Es la forma directa de saber si un array **comparte memoria** con otro y de distinguir vista vs copia: ver [[concepto_views_vs_copias]].

## Tipo y lectura/escritura

| Aspecto | Valor |
|---------|-------|
| Tipo devuelto | `ndarray` (el array origen) o `None` |
| Lectura/escritura | **Solo lectura** |
| `base is None` | El array posee sus datos (copia / original) |
| `base is otro` | Es una vista que comparte memoria con `otro` |

## En detalle

`base` apunta al array que **posee** el buffer, que puede ser un ancestro y no el inmediato (una vista de una vista suele apuntar al dueño raíz). Para preguntar simplemente si dos arrays comparten bytes, `np.shares_memory(a, b)` es más robusto que comparar `base`.

```python
import numpy as np

arr = np.arange(10)

vista = arr[0:5]
vista.base is arr       # → True   (vista: comparte memoria)

copia = arr.copy()
copia.base is None      # → True   (copia: datos propios)

arr.base is None        # → True   (original)
```

Patrones de verificación:

| Expresión | Significado |
|-----------|-------------|
| `x.base is None` | `x` posee su memoria |
| `x.base is y` | `x` es vista de `y` |
| `x.flags.owndata` | Equivalente booleano (datos propios) |

## Casos de uso

- Detectar si una operación devolvió vista o copia: `resultado.base is original`.
- Depurar bugs de aliasing en los que escribir un array muta otro inesperadamente.
- Confirmar que un slice no copió antes de modificarlo in-place.

## Notas relacionadas

- [[concepto_views_vs_copias]]
- [[ndarray.strides]]
