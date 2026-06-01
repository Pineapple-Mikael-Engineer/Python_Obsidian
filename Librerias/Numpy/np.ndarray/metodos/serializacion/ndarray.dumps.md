---
title: ndarray.dumps — Serializar el array a bytes con pickle
aliases:
  - dumps
  - ndarray.dumps
tags:
  - numpy
  - api/metodo
  - io
lib: numpy
obj: ndarray
tipo: metodo
retorna: bytes
inplace: false
draft: false
---

# ndarray.dumps — Serializar el array a bytes con pickle

## Firma del método

```python
ndarray.dumps() -> bytes
```

## Valor de retorno

| Retorna | Significado |
|---------|-------------|
| `bytes` | Cadena de bytes con el array serializado por **pickle**. No modifica el array (solo lo exporta a memoria). |

Es la variante en memoria de [[ndarray.dump]]: en lugar de escribir un archivo, devuelve los bytes pickled. Como pickle serializa el objeto completo, conserva `shape` y [[concepto_dtype|dtype]]. Se recupera con `pickle.loads`.

```python
import numpy as np, pickle
arr = np.arange(4).reshape(2, 2)
blob = arr.dumps()              # bytes pickled (b'\x80\x04...')
back = pickle.loads(blob)       # array([[0, 1], [2, 3]])
```

## Parámetros en detalle

No recibe parámetros. Equivale a `pickle.dumps(arr)`.

```python
import pickle
blob = pickle.dumps(arr)        # resultado equivalente a arr.dumps()
```

## Casos de uso

```python
# Guardar el array en una caché en memoria (Redis, columna BLOB)
cache.set('clave', arr.dumps())
arr2 = pickle.loads(cache.get('clave'))     # dtype y shape intactos
```

## Buenas prácticas

1. Útil cuando necesitas bytes (red, caché, DB) sin pasar por disco.
2. Para persistir en archivo, usa [[ndarray.dump]] o, mejor, `np.save`.
3. **Nunca** hagas `pickle.loads` de datos de origen no confiable.

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| Bytes ilegibles como texto | pickle es binario | tratarlos como `bytes`, no `str` |
| Incompatibilidad entre versiones | formato pickle dependiente | preferir `.npy` para almacenamiento largo |
| Ejecución de código al cargar | `pickle.loads` no es seguro | no deserializar fuentes ajenas |

## Notas relacionadas

- [[concepto_dtype]]
- [[ndarray.dump]]
