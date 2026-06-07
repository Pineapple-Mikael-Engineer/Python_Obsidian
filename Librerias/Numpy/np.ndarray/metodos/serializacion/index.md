---
title: np.ndarray — metodos de serializacion
tags:
  - numpy
  - indice
draft: false
---

# np.ndarray — metodos de serializacion

Los 5 metodos de serializacion exportan el array fuera de NumPy: a disco, a estructuras Python nativas o a bytes en memoria. Ningun metodo modifica el array original.

## Tabla de metodos segun destino

| Destino | Metodo | Descripcion |
|---------|--------|-------------|
| Disco binario raw | [[ndarray.tofile]] | Escribe los bytes del array directamente a un fichero |
| Disco con pickle | [[ndarray.dump]] | Serializa con `pickle.dump` a un fichero |
| Lista Python | [[ndarray.tolist]] | Convierte a lista anidada de escalares Python |
| Bytes en memoria | [[ndarray.tobytes]] | Devuelve un objeto `bytes` con el buffer crudo |
| Bytes con pickle | [[ndarray.dumps]] | Serializa con `pickle.dumps` y devuelve `bytes` |

## Diferencias clave

### `tofile` vs `dump`

| | `tofile` | `dump` |
|-|----------|--------|
| Formato | Binario raw (sin metadatos) | Pickle (incluye dtype, shape) |
| Para leer despues | `np.fromfile(f, dtype=...)` | `pickle.load(f)` o `np.load(f, allow_pickle=True)` |
| Portabilidad | Depende de dtype y endianness del sistema | Portable entre sistemas Python |

### `tobytes` vs `dumps`

- `tobytes()` — el buffer crudo del array como objeto `bytes`. Equivalente a `tofile` pero en memoria. Para reconstruir: `np.frombuffer(b, dtype=...)`.
- `dumps()` — serializa con pickle y devuelve `bytes`. Para reconstruir: `pickle.loads(b)`. Incluye todos los metadatos.

### Cuando usar `pickle` (`dump` / `dumps`)

Para almacenar arrays con tipos no estandar (objetos, dtypes estructurados) o cuando se necesita reconstruir el array sin conocer su dtype de antemano. Para arrays numericos simples, `np.save` / `np.load` son preferibles a `dump/dumps` por ser mas robustos entre versiones.

```python
import pickle

arr = np.arange(6).reshape(2, 3)

# Serializar
b = arr.dumps()

# Reconstruir
arr2 = pickle.loads(b)
```
