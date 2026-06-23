---
title: np.save — guarda UN array en formato binario .npy (conserva shape y dtype)
aliases:
  - save
  - np.save
tags:
  - numpy
  - api/funcion
  - io

# --- Clasificación ---
lib: numpy
mod: np
tipo: funcion

# --- Comportamiento ---
retorna: None
inplace: false

# --- Dependencias ---
requiere:
  - concepto_dtype

draft: false
---

# np.save — guarda UN array en formato binario .npy

`np.save` persiste **un único** `ndarray` en disco en el formato binario **`.npy`**, el formato
recomendado de NumPy para guardar arrays. A diferencia de [[ndarray.tofile]] o [[ndarray.tobytes]]
(que escriben solo los bytes crudos del buffer), `.npy` antepone una **cabecera** que guarda el
`shape`, el [[concepto_dtype|dtype]] y el `order`, de modo que el array se reconstruye **exacto** —
incluyendo su dimensionalidad N-D— con un simple [[np.load]], sin recordar metadatos a mano.

## La idea

`.npy` es un formato **autodescriptivo**: cabecera (versión, `dtype`, `fortran_order`, `shape`) +
los bytes del array. Esa cabecera es la diferencia clave con la serialización cruda:

| Aspecto | `np.save` (.npy) | [[ndarray.tofile]] / [[ndarray.tobytes]] |
|---------|------------------|------------------------------------------|
| Guarda `shape` | sí (en la cabecera) | no (solo bytes 1D crudos) |
| Guarda `dtype` | sí | no |
| Guarda `order` (C/F) | sí | no |
| Recuperación | `np.load(f)` directo | `fromfile/frombuffer` + `dtype` + `reshape` a mano |
| Portable entre versiones | sí | no (endianness/shape aparte) |

Porque conserva el `shape` completo, un array 4D o 5D vuelve con **su misma forma**, no aplanado.

## Firma

```python
np.save(
    file,                # str | Path | file-object: destino (añade .npy si falta)
    arr,                 # array_like: el array a guardar
    allow_pickle=True,   # bool: permitir pickle para dtype=object
    fix_imports=True,    # bool: compatibilidad de pickle con Python 2 (obsoleto)
) -> None
```

## Los parámetros en detalle

### `file` — destino
`str`, `Path` o un objeto archivo abierto en binario. Si es una ruta y **no** termina en `.npy`,
NumPy añade la extensión automáticamente (por eso pasar `'datos.npy'` y `'datos'` produce el mismo
archivo). No la añadas tú a mano sobre una ruta que ya la tiene, o saldrá `datos.npy.npy`.

### `arr` — el array a guardar
`array_like` de **cualquier** dimensión y `dtype`. Si no es ya un `ndarray`, se convierte con
`np.asanyarray`. Es **un solo** array; para guardar varios en un archivo, usa [[np.savez]].

### `allow_pickle` — permitir serialización pickle
`bool` (defecto `True`). Solo entra en juego con arrays de `dtype=object` (que contienen objetos
Python arbitrarios): esos **necesitan** pickle para guardarse. Con datos numéricos normales no se
usa. Ponerlo en `False` al guardar fuerza un error si el array no es serializable sin pickle, lo que
sirve para **garantizar** que el archivo resultante es seguro de cargar.

### `fix_imports` — compatibilidad Python 2
`bool` (defecto `True`). Solo afecta al pickle de objetos para que Python 2 pueda leerlo. Heredado y
sin relevancia hoy; déjalo como está.

## Round-trip

El ciclo es `np.save` ↔ [[np.load]]. La cabecera `.npy` hace que `shape` y `dtype` se recuperen
solos, así que el round-trip es **exacto** sin parámetros extra:

```python
import numpy as np

arr = np.arange(60, dtype=np.float32).reshape(3, 4, 5)
np.save('arr.npy', arr)        # escribe arr.npy (cabecera + bytes)
back = np.load('arr.npy')      # reconstruye exacto

back.shape == arr.shape        # True  → (3, 4, 5)
back.dtype == arr.dtype        # True  → float32
np.array_equal(back, arr)      # True
```

### Conservación del shape en 4D/5D

El punto crítico frente a `tofile`: la forma **N-D entera** sobrevive al ida y vuelta, sin aplanarse.

```python
# Array 5D (p. ej. lote de vídeos: lote, tiempo, alto, ancho, canal)
t5 = np.random.rand(2, 4, 8, 8, 3)
np.save('tensor5d.npy', t5)

vuelto = np.load('tensor5d.npy')
vuelto.shape                   # (2, 4, 8, 8, 3)  ← se conserva la forma 5D
vuelto.shape == t5.shape       # True
np.array_equal(vuelto, t5)     # True  → mismos datos, mismo dtype, mismo order
```

Con `tofile` el equivalente volvería como `(2048,)` (1D) y habría que recordar el shape y
`reshape` a mano; con `.npy` viene resuelto.

## Casos de uso

### Cachear un cálculo costoso

```python
import os
if not os.path.exists('cache.npy'):
    np.save('cache.npy', calcular_costoso())   # solo la primera vez
datos = np.load('cache.npy')                    # relecturas baratas
```

### Checkpoint intermedio de un tensor N-D

```python
activaciones = np.random.rand(64, 128, 256)    # (lote, tokens, features)
np.save('ckpt.npy', activaciones)              # shape y float64 conservados
```

### Garantizar un archivo seguro (sin pickle)

```python
np.save('limpio.npy', arr_numerico, allow_pickle=False)
# falla a propósito si el array exigiera pickle → el .npy resultante es seguro de cargar
```

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| Doble extensión `datos.npy.npy` | añadirla a mano sobre una ruta que ya la tiene | dejar que NumPy la ponga |
| El array vuelve aplanado | se usó `tofile`/`tobytes`, no `np.save` | usar `np.save`, que guarda el `shape` |
| `ValueError` al guardar con `allow_pickle=False` | array de `dtype=object` | dejar `allow_pickle=True`, o no usar objetos |
| Archivo grande para varios arrays separados | un `.npy` por array | agruparlos con [[np.savez]] |

## Notas relacionadas

- [[concepto_dtype]] — el metadato que la cabecera `.npy` conserva
- [[np.load]] — el inverso: reconstruye el array exacto
- [[np.savez]] — guardar **varios** arrays en un solo archivo
- [[np.savez_compressed]] · [[np.savetxt]] · [[serializacion/index|métodos de serialización del ndarray]]
