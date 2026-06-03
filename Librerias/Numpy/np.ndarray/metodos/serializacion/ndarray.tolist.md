---
title: ndarray.tolist — Convertir a listas anidadas de Python
aliases:
  - tolist
  - ndarray.tolist
tags:
  - numpy
  - api/metodo
  - io
lib: numpy
obj: ndarray
tipo: metodo
retorna: list
inplace: false
draft: false
---

# ndarray.tolist — Convertir a listas anidadas de Python

## Firma del método

```python
ndarray.tolist() -> list
```

## Valor de retorno

| Retorna | Significado |
|---------|-------------|
| `list` | Lista (anidada según `ndim`) de escalares **nativos** de Python. No modifica el array. |

Convierte cada elemento a su tipo escalar de Python (`int`, `float`, `bool`...), **perdiendo el** [[concepto_dtype|dtype]] de NumPy. Es la forma idiomática de preparar datos para `json.dumps`, que no acepta tipos NumPy.

```python
import numpy as np
arr = np.array([[1, 2], [3, 4]], dtype=np.int32)
arr.tolist()        # [[1, 2], [3, 4]]  → ints de Python
type(arr.tolist()[0][0])    # <class 'int'>  (NO np.int32)
```

## Parámetros en detalle

No recibe parámetros. La profundidad del anidamiento corresponde a `ndim`.

```python
np.array(5).tolist()        # 5        → 0D devuelve un escalar, no una lista
np.array([1, 2, 3]).tolist()# [1, 2, 3]
```

## Casos de uso

```python
import json
arr = np.array([1.5, 2.5, 3.5])
json.dumps(arr.tolist())            # '[1.5, 2.5, 3.5]'  → serializable
# json.dumps(arr)  → TypeError: Object of type ndarray is not JSON serializable
```

## Buenas prácticas

1. Úsalo en la frontera con código no-NumPy (JSON, APIs, DB).
2. Para volúmenes grandes evítalo: pierde la compacidad del buffer.
3. Si solo quieres un escalar de un array 0D/1-elem, `tolist()` o `.item()` valen.

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| Pierdo el dtype | `tolist` siempre da tipos Python | reconvertir con `np.array(lista, dtype=...)` |
| Memoria alta | listas Python pesan más que el buffer | evitar en arrays grandes |
| `np.float64` en JSON | usar el array directo, no `tolist` | aplicar `tolist()` antes de serializar |

## Notas relacionadas

- [[concepto_dtype]]
- [[ndarray.tobytes]]
