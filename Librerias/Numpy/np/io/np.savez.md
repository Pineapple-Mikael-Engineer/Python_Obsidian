---
title: np.savez — guarda VARIOS arrays con nombre en un .npz (zip sin comprimir)
aliases:
  - savez
  - np.savez
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

# np.savez — guarda VARIOS arrays con nombre en un .npz

`np.savez` agrupa **varios** arrays en un único archivo **`.npz`**: por dentro es un **zip sin
comprimir** que contiene un `.npy` por array (cada uno con su cabecera de `shape` y
[[concepto_dtype|dtype]]). Donde [[np.save]] guarda un solo array, `savez` guarda un conjunto
**nombrado** (`savez(f, a=..., b=...)`) que luego se recupera por nombre con [[np.load]]. Cada array
conserva su forma N-D exacta, porque cada miembro del zip es un `.npy` completo.

## La idea

Un `.npz` = un contenedor zip donde cada entrada es `<nombre>.npy`. El nombre lo decides al guardar:

| Forma de pasar el array | Nombre dentro del `.npz` |
|-------------------------|--------------------------|
| `np.savez(f, a, b)` (posicional) | `arr_0`, `arr_1` (auto) |
| `np.savez(f, x=a, y=b)` (kwargs) | `'x'`, `'y'` (recomendado) |

Al cargar, [[np.load]] devuelve un objeto **`NpzFile`** (tipo dict, perezoso): los arrays no se leen
hasta que se indexan por nombre (`d['x']`). Frente a guardar N archivos `.npy` sueltos, `savez`
mantiene el dataset entero en **un solo archivo** autodescriptivo.

## Firma

```python
np.savez(
    file,        # str | Path | file-object: destino (añade .npz si falta)
    *args,       # arrays posicionales → nombres automáticos arr_0, arr_1, ...
    **kwds,      # arrays por palabra clave → nombre = la clave (recomendado)
) -> None
```

## Los parámetros en detalle

### `file` — destino
`str`, `Path` o un objeto archivo abierto en binario. Si es una ruta sin `.npz`, NumPy añade la
extensión. (Con un objeto archivo no se añade nada.)

### `*args` — arrays posicionales
Cada array posicional recibe un nombre **automático** `arr_0`, `arr_1`, … según el orden. Cómodo
pero opaco: al cargar tendrás que recordar qué era `arr_0`. Útil solo para guardados rápidos.

### `**kwds` — arrays con nombre (recomendado)
Cada par `clave=array` guarda el array bajo esa clave, que será su nombre al recargar
(`d['clave']`). Es la forma legible y la que deberías usar casi siempre: el archivo queda
autodocumentado (`X_train`, `y_train`, …).

> [!note] Mezclar posicionales y kwargs
> Se pueden combinar: `np.savez(f, matriz, etiquetas=y)` guarda `arr_0` y `etiquetas`. No repitas
> una clave que colisione con un `arr_N` automático.

## Round-trip

El ciclo es `np.savez` ↔ [[np.load]], recuperando **por nombre**. Cada array vuelve con su `shape` y
`dtype` intactos, porque cada uno es un `.npy` dentro del zip.

```python
import numpy as np

x = np.arange(10)
y = np.ones((3, 3))
np.savez('datos.npz', x=x, matriz=y)     # nombres por kwargs

with np.load('datos.npz') as d:          # NpzFile (lazy); cerrar con with
    d.files                              # ['x', 'matriz']
    xr = d['x']                          # se materializa al indexar
    mr = d['matriz']
    xr.shape, mr.shape                   # (10,) (3, 3)
```

### Conservación del shape en 4D/5D

Cada miembro del `.npz` conserva su forma N-D completa, independientemente de los demás.

```python
cubo  = np.arange(2*2*2*2*2).reshape(2, 2, 2, 2, 2)   # 5D
plano = np.random.rand(4, 3, 8, 8)                    # 4D
np.savez('mixto.npz', cubo=cubo, plano=plano)

with np.load('mixto.npz') as d:
    d['cubo'].shape == cubo.shape        # True → (2, 2, 2, 2, 2) se conserva
    d['plano'].shape == plano.shape      # True → (4, 3, 8, 8) se conserva
    np.array_equal(d['cubo'], cubo)      # True
```

## Casos de uso

### Guardar un dataset completo de entrenamiento

```python
np.savez('dataset.npz', X_train=X_train, y_train=y_train, X_test=X_test, y_test=y_test)
# un solo archivo con todo el split, recuperable por nombre
```

### Empaquetar resultados heterogéneos de un experimento

```python
np.savez('run.npz', perdida=hist_perdida, pesos=W, config=np.array(cfg))
```

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| Nombres `arr_0`, `arr_1` confusos al cargar | se pasaron posicionales | guardar con kwargs nombrados |
| Esperabas un array y recibes `NpzFile` | `.npz` contiene varios | indexar por nombre `d['x']` |
| `KeyError` al cargar | nombre equivocado | revisar `d.files` |
| El contenedor no se libera | `np.load` sin cerrar | usar `with np.load(...) as d:` |
| Archivo más grande de lo esperado | `savez` no comprime | usar [[np.savez_compressed]] si hay redundancia |

## Notas relacionadas

- [[concepto_dtype]] — conservado por cada `.npy` interno
- [[np.savez_compressed]] — igual pero comprimido (zip deflate)
- [[np.save]] — para **un** solo array
- [[np.load]] — el inverso: devuelve el `NpzFile`
