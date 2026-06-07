---
title: np.ndarray — metodos de serializacion
tags:
  - numpy
  - indice
draft: false
---

# np.ndarray — metodos de serializacion

5 metodos para exportar el ndarray fuera del ecosistema NumPy: a disco, a estructuras Python nativas o a bytes en memoria. Ningun metodo modifica el array original. La eleccion depende del destino y de si se necesita preservar el dtype y la shape exactos para poder reconstruir el array despues.

## Tabla de metodos segun destino

| Destino | Metodo | Preserva metadatos | Descripcion |
|---------|--------|--------------------|-------------|
| Disco binario raw | [[ndarray.tofile]] | No | Escribe los bytes crudos del array a un fichero; maximo rendimiento |
| Disco con pickle | [[ndarray.dump]] | Si (pickle) | Serializa con `pickle` a un fichero; preserva dtype y shape |
| Lista Python | [[ndarray.tolist]] | No (tipos Python) | Convierte a lista anidada de escalares nativos (int, float) |
| Bytes en memoria (raw) | [[ndarray.tobytes]] | No | Devuelve el buffer crudo del array como objeto `bytes` |
| Bytes con pickle | [[ndarray.dumps]] | Si (pickle) | Serializa con `pickle` y devuelve `bytes` en vez de escribir a archivo |

## `tofile` — binario raw

Escribe los bytes del array directamente al archivo sin ningun encabezado. Maximo rendimiento, minima portabilidad: para releer los datos hay que conocer el dtype, shape y endianness exactos:

```python
arr = np.arange(6).reshape(2, 3)
arr.tofile("datos.bin")

# Relectura — requiere conocer dtype y shape de antemano
arr2 = np.fromfile("datos.bin", dtype=np.int64).reshape(2, 3)
```

## `dump` y `dumps` — pickle

Preservan dtype, shape y todos los metadatos del array. `dump` escribe a un archivo; `dumps` devuelve los bytes para transmision o almacenamiento en memoria:

```python
arr = np.arange(6).reshape(2, 3)

arr.dump("array.pkl")
arr2 = np.load("array.pkl", allow_pickle=True)

b = arr.dumps()
import pickle
arr3 = pickle.loads(b)
```

Para arrays numericos simples, `np.save` / `np.load` (formato `.npy`) son preferibles a `dump/dumps` por ser mas robustos entre versiones de Python y NumPy.

## `tolist` — lista Python

Convierte el array a una lista Python anidada de escalares nativos (int, float, bool). Los elementos dejan de ser tipos NumPy y pasan a ser tipos Python estandar, lo que los hace serializables a JSON:

```python
arr = np.array([[1, 2], [3, 4]])
arr.tolist()  # → [[1, 2], [3, 4]]

import json
json.dumps(arr.tolist())  # funciona; json.dumps(arr) fallaria
```

## `tobytes` — buffer crudo en memoria

Equivalente a `tofile` pero en memoria: devuelve los bytes del array como objeto `bytes` Python. Util para transmision por red, hashing o interfaz con otros sistemas que esperan bytes crudos. Para reconstruir se necesita conocer el dtype:

```python
arr = np.array([1, 2, 3], dtype=np.int32)
b = arr.tobytes()                          # 12 bytes (3 elementos x 4 bytes)
arr2 = np.frombuffer(b, dtype=np.int32)   # reconstruye el array
```

## Cuadro comparativo `tofile` vs `dump`

| | `tofile` | `dump` |
|-|----------|--------|
| Formato | Binario raw (sin metadatos) | Pickle (incluye dtype, shape) |
| Para releer | `np.fromfile(f, dtype=...)` | `pickle.load(f)` o `np.load(f, allow_pickle=True)` |
| Portabilidad | Depende de dtype y endianness del sistema | Portable entre sistemas Python |
| Tamaño en disco | Minimo (solo datos) | Ligeramente mayor (overhead de pickle) |
