---
title: ndarray.tobytes — devuelve los bytes crudos del buffer (sin metadatos)
aliases:
  - tobytes
  - ndarray.tobytes
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
  - concepto_contiguidad_memoria
draft: false
---

# ndarray.tobytes — devuelve los bytes crudos del buffer (sin metadatos)

`ndarray.tobytes` exporta el array como un objeto `bytes` con el **contenido en bruto del buffer**: los
elementos uno tras otro, sin cabecera, sin `shape`, sin [[concepto_dtype|dtype]], sin endianness. Es la
representación más compacta posible (solo datos) y la base para enviar arrays por red, hashearlos o
guardarlos en una columna BLOB. La contrapartida: por sí solos, esos bytes son **ininterpretables**; hay
que conocer el dtype, el shape y el `order` por separado para reconstruir el array.

## La idea

El array → una tira plana de bytes. NumPy serializa los elementos siguiendo el orden de memoria que pidas
con `order` (ver [[concepto_contiguidad_memoria|contigüidad]]). La longitud es exacta y predecible:

$$ \texttt{len(arr.tobytes())} \;=\; \texttt{arr.size} \times \texttt{arr.itemsize} \;=\; \texttt{arr.nbytes} $$

No hay overhead: son **solo los datos**. Reemplaza al antiguo `tostring`, ya eliminado.

```python
import numpy as np
arr = np.array([1, 2, 3], dtype=np.uint8)
b = arr.tobytes()        # b'\x01\x02\x03'
len(b)                   # 3   → 3 elementos × 1 byte (uint8)
```

## Firma

```python
ndarray.tobytes(order="C") -> bytes
```

## Los parámetros en detalle

### `order` — en qué orden se aplanan los elementos
Controla el recorrido del buffer al serializar arrays de más de 1 dimensión. **No importa en 1-D**; es
crítico en 2-D+ porque cambia el orden de los bytes resultantes:

| Valor | Recorrido | Cuándo |
|-------|-----------|--------|
| `"C"` (def.) | row-major: la **última** dimensión varía más rápido (por filas) | el defecto; lo espera casi todo |
| `"F"` | column-major: la **primera** dimensión varía más rápido (por columnas) | interoperar con Fortran/MATLAB |
| `"A"` | `"F"` si el array es F-contiguo, si no `"C"` | preservar el layout físico ya existente |

```python
m = np.array([[1, 2], [3, 4]], dtype=np.uint8)
m.tobytes("C")      # b'\x01\x02\x03\x04'   → por filas: 1,2 | 3,4
m.tobytes("F")      # b'\x01\x03\x02\x04'   → por columnas: 1,3 | 2,4
```

> [!warning] Quien escribe y quien lee deben pactar el mismo `order`
> Si serializas con `order="F"` y reconstruyes asumiendo `"C"`, los elementos quedan transpuestos en
> silencio. El `order` no viaja con los bytes: es metadato que tienes que transmitir aparte.

## Valor de retorno

Un objeto `bytes` **inmutable** con una copia de los datos del buffer (el array original no se toca):

| Entrada (`shape`, `dtype`) | `len` de la salida | Contenido |
|---|---|---|
| `(3,)`, `uint8` | 3 | 1 byte por elemento |
| `(3,)`, `int32` | 12 | 4 bytes por elemento |
| `(2, 2)`, `float64` | 32 | 8 bytes por elemento, según `order` |

Los bytes siguen el **endianness nativo** de la máquina salvo que el dtype lo fije (`<i4` little, `>i4`
big). Eso, junto con la ausencia de shape/dtype, es lo que hace estos bytes **no portables** por sí solos.

## Round-trip

La inversa es `np.frombuffer`, que **reinterpreta** una secuencia de bytes como array. Hay que pasarle el
`dtype` (obligatorio) y reconstruir el `shape` a mano con `reshape`:

```python
arr = np.array([[1, 2, 3], [4, 5, 6]], dtype=np.int32)

b    = arr.tobytes()                              # 24 bytes, sin metadatos
flat = np.frombuffer(b, dtype=np.int32)           # array([1,2,3,4,5,6]) — 1-D
back = flat.reshape(arr.shape)                    # recupera (2, 3)
np.array_equal(arr, back)                         # True
```

> [!note] `np.frombuffer` devuelve un array de SOLO LECTURA
> Comparte memoria con el objeto `bytes` (que es inmutable), así que el array resultante no es escribible.
> Si necesitas mutarlo, haz `.copy()`: `np.frombuffer(b, dtype=...).reshape(...).copy()`.

Para reconstruir hacen falta **tres** datos que `tobytes` NO guarda: `dtype`, `shape` y `order`. Esa es su
trampa central.

## Casos de uso

### Enviar un array por red o guardarlo como BLOB
```python
payload = arr.tobytes()                           # solo los datos, compacto
# En el otro extremo (hay que conocer dtype y shape de antemano):
arr2 = np.frombuffer(payload, dtype=np.int32).reshape(2, 3)
```

### Hash determinista del contenido
```python
import hashlib
hashlib.sha256(arr.tobytes()).hexdigest()         # huella estable de los datos
```

### Empaquetar metadatos junto a los bytes (round-trip robusto)
```python
meta = {"dtype": str(arr.dtype), "shape": arr.shape}
blob = arr.tobytes()
# ...transmitir (meta, blob)...
rec = np.frombuffer(blob, dtype=meta["dtype"]).reshape(meta["shape"])
```

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| Datos basura al reconstruir | `dtype` en `np.frombuffer` distinto al de escritura | usar el mismo dtype (y endianness, ej. `<i4`) |
| Array sale 1-D | `tobytes` no guarda el `shape` | `reshape(shape)` tras `frombuffer` |
| Elementos transpuestos en 2-D | `order` de lectura distinto al de escritura | pactar y transmitir el `order` |
| `ValueError: buffer is read-only` al escribir | `frombuffer` da array inmutable | añadir `.copy()` |
| `AttributeError: tostring` | método antiguo eliminado | usar `tobytes` |

## Notas relacionadas

- [[concepto_dtype]] — el tipo que necesitas conocer para reinterpretar los bytes
- [[concepto_contiguidad_memoria]] — qué significa `order="C"` / `"F"` en el buffer
- [[ndarray.tofile]] — los mismos bytes crudos, pero volcados a un archivo
- [[ndarray.dump]] — alternativa que **sí** conserva dtype y shape (vía pickle)
- [[index]] — métodos de serialización del ndarray
