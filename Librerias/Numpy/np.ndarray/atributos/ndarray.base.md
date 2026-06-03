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
obj: ndarray
tipo: atributo
draft: false
---

# ndarray.base — Array dueño de la memoria de una vista

## Qué representa

Referencia al array del que **esta vista toma su memoria**. Si el array es una vista, `base` apunta al objeto que posee el buffer; si el array posee sus propios datos (es una copia o un array original), `base` es `None`. Es la forma directa de distinguir vista vs copia: ver [[concepto_views_vs_copias]].

## Tipo y acceso

| Aspecto | Valor |
|---------|-------|
| Tipo devuelto | `ndarray` (la vista origen) o `None` |
| Acceso | **SOLO LECTURA** |
| `base is None` | El array posee sus datos (copia / original) |
| `base is otro` | Es una vista que comparte memoria con `otro` |

## Ejemplos

```python
import numpy as np

arr = np.arange(10)

vista = arr[0:5]
vista.base is arr       # → True   (vista: comparte memoria)

copia = arr.copy()
copia.base is None      # → True   (copia: datos propios)

arr.base is None        # → True   (original)
```

## Patrón de verificación

| Expresión | Significado |
|-----------|-------------|
| `x.base is None` | `x` posee su memoria |
| `x.base is y` | `x` es vista directa de `y` |
| `x.flags.owndata` | Equivalente booleano (datos propios) |

## Notas relacionadas

- [[concepto_views_vs_copias]]
- [[ndarray.strides]]
