---
title: ndarray.dumps — serializa el array a un objeto bytes con pickle (en memoria)
aliases:
  - dumps
  - ndarray.dumps
tags:
  - numpy
  - api/metodo
  - serializacion
lib: numpy
mod: np.ndarray
obj: ndarray
tipo: metodo
retorna: bytes
inplace: false
requiere:
  - concepto_dtype
draft: false
---

# ndarray.dumps — serializa el array a un objeto bytes con pickle (en memoria)

`ndarray.dumps` es la variante **en memoria** de [[ndarray.dump]]: en lugar de escribir un archivo,
devuelve un objeto `bytes` con el array serializado por **pickle**. Como pickle serializa el objeto
completo, conserva el [[concepto_dtype|dtype]], el `shape` y todos los metadatos, así que el round-trip es
exacto sin información externa. Es lo que quieres cuando el destino es una **caché, una red o una columna
BLOB** y no un disco.

## La idea

El array → un objeto `bytes` autodescriptivo (a diferencia de [[ndarray.tobytes]], cuyos bytes son crudos
y necesitan dtype/shape aparte). Todo viaja dentro del blob:

$$ \texttt{arr (dtype, shape)}\ \xrightarrow{\ \text{dumps → pickle}\ }\ \texttt{bytes}\ \xrightarrow{\ \text{pickle.loads}\ }\ \texttt{arr (dtype, shape)} $$

`arr.dumps()` equivale a `pickle.dumps(arr)`.

```python
import numpy as np, pickle
arr  = np.arange(4, dtype=np.int8).reshape(2, 2)
blob = arr.dumps()                       # b'\x80\x04...'  → bytes pickled
back = pickle.loads(blob)                # array([[0, 1], [2, 3]], dtype=int8)
back.dtype, back.shape                   # (dtype('int8'), (2, 2)) → exacto
```

## Firma

```python
ndarray.dumps() -> bytes
```

No recibe parámetros.

## Los parámetros en detalle

`dumps()` no acepta argumentos: equivale exactamente a `pickle.dumps(arr)`. El protocolo de pickle y el
contenido los gestiona NumPy.

```python
import pickle
blob_a = arr.dumps()
blob_b = pickle.dumps(arr)               # resultado equivalente
```

## Valor de retorno

Un objeto `bytes` con el array pickled (incluidos dtype y shape). No modifica el array (solo lo exporta a
memoria). A diferencia de `tobytes`, estos bytes **no** son el buffer crudo: llevan la cabecera de pickle
y la descripción del objeto, así que pesan algo más pero son autosuficientes.

| | `dumps()` | `tobytes()` |
|---|---|---|
| Contenido | objeto pickled (dtype + shape + datos) | solo los datos del buffer |
| Conserva metadatos | Sí | No |
| Inversa | `pickle.loads` | `np.frombuffer` (+ dtype + reshape) |
| Seguridad al cargar | riesgo (ejecuta código) | sin riesgo |

## Round-trip

La inversa es `pickle.loads`. Como el blob es autodescriptivo, **no hay que pasar dtype ni shape**:

```python
import pickle
blob = arr.dumps()
back = pickle.loads(blob)
back.dtype == arr.dtype and np.array_equal(arr, back)   # True
```

> [!danger] `pickle.loads` ejecuta código al deserializar
> **Nunca** hagas `pickle.loads` de bytes de origen no confiable: un pickle malicioso puede ejecutar
> código arbitrario. Úsalo solo con datos que tú mismo generaste o de una fuente de confianza. Para
> intercambio con terceros, prefiere formatos sin código embebido.

## Casos de uso

### Guardar el array en una caché en memoria (Redis, Memcached)
```python
cache.set("clave", arr.dumps())                         # bytes listos para la caché
arr2 = pickle.loads(cache.get("clave"))                 # dtype y shape intactos
```

### Almacenar en una columna BLOB de base de datos
```python
cursor.execute("INSERT INTO t (datos) VALUES (?)", (arr.dumps(),))
fila = cursor.execute("SELECT datos FROM t").fetchone()
arr2 = pickle.loads(fila[0])
```

### Enviar por red sin pasar por disco
```python
sock.sendall(arr.dumps())                               # un solo blob autodescriptivo
# En el receptor: arr2 = pickle.loads(datos_recibidos)
```

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| Tratar el blob como texto | el pickle es binario | manejarlo como `bytes`, nunca `str` |
| `pickle.loads` falla en otra versión | formato pickle dependiente de versiones | usar `np.save`/`.npy` para almacenamiento largo |
| Ejecución de código al cargar | `pickle.loads` no valida el origen | no deserializar bytes de fuentes ajenas |
| Quería un archivo, no bytes | `dumps` devuelve `bytes` en memoria | usar [[ndarray.dump]] (escribe a archivo) |

## Notas relacionadas

- [[concepto_dtype]] — el tipo que `dumps` conserva dentro del blob
- [[ndarray.dump]] — misma serialización pickle, pero a un archivo
- [[ndarray.tobytes]] — bytes **crudos** (sin metadatos), más compactos y seguros
- [[np.save]] — persistencia portable y segura en `.npy`
- [[index]] — métodos de serialización del ndarray
