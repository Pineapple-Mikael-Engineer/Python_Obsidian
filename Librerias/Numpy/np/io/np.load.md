---
title: np.load — carga arrays desde .npy / .npz (reconstruye shape y dtype)
aliases:
  - load
  - np.load
tags:
  - numpy
  - api/funcion
  - io

# --- Clasificación ---
lib: numpy
mod: np
tipo: funcion

# --- Comportamiento ---
retorna: ndarray | NpzFile
inplace: false

# --- Dependencias ---
requiere:
  - concepto_dtype

draft: false
---

# np.load — carga arrays desde .npy / .npz

`np.load` es el **inverso** de [[np.save]] / [[np.savez]]: lee un archivo `.npy` o `.npz` y
reconstruye el array (o arrays) con su `shape` y [[concepto_dtype|dtype]] **exactos**, leyéndolos de
la cabecera del propio archivo. No hay que recordar metadatos: a diferencia de `np.fromfile` (que
exige pasar el `dtype` y hacer `reshape` a mano), aquí toda la información de forma viaja dentro del
archivo, así que un array N-D vuelve con su misma dimensionalidad.

## La idea

Lo que devuelve **depende del archivo**, y conviene desambiguarlo de entrada:

| Archivo | Qué contiene | `np.load` devuelve |
|---------|--------------|--------------------|
| `.npy` | un solo array | un `ndarray` |
| `.npz` | varios arrays con nombre | un objeto **`NpzFile`** (tipo dict, **lazy**) |

El caso `.npz` es la trampa: **no** devuelve un array, sino un contenedor perezoso. Los arrays no se
descomprimen hasta que se indexan por nombre (`d['x']`), lo que permite abrir un `.npz` enorme y
sacar solo el array que interesa. Por eso conviene cerrarlo (`with` o `.close()`).

## Firma

```python
np.load(
    file,                 # str | Path | file-object: .npy o .npz a leer
    mmap_mode=None,       # None | {'r','r+','w+','c'}: mapear a memoria en vez de cargar
    allow_pickle=False,   # bool: permitir des-pickle (riesgo de seguridad)
    fix_imports=True,     # bool: compatibilidad pickle Python 2 (obsoleto)
    encoding='ASCII',     # str: codificación al des-picklar arrays de objetos
) -> ndarray | NpzFile
```

## Los parámetros en detalle

### `file` — archivo a leer
`str`, `Path` o un objeto archivo abierto en binario. La extensión (`.npy` vs `.npz`) y la cabecera
deciden el modo; no hay que indicarlo.

### `mmap_mode` — mapear a memoria en lugar de cargar
`None` (defecto) carga el array entero en RAM. Si se da `'r'`, `'r+'`, `'w+'` o `'c'`, devuelve un
[[np.memmap|array mapeado a memoria]] respaldado por el `.npy`: el sistema operativo trae a RAM solo
las porciones que se acceden. Ideal para arrays más grandes que la memoria. Solo aplica a `.npy`.

```python
grande = np.load('enorme.npy', mmap_mode='r')   # no carga todo en RAM
fila = grande[0]                                 # solo esta porción entra en RAM
```

### `allow_pickle` — permitir des-pickle (aviso de seguridad)
`bool`, defecto **`False`** (seguro). Solo se necesita `True` para cargar arrays de `dtype=object`,
que se guardaron con pickle.

> [!warning] Riesgo de seguridad
> `allow_pickle=True` **ejecuta código** al deserializar. **Nunca** lo actives con archivos de
> origen no confiable: un `.npy` malicioso puede correr código arbitrario al cargarse. Manténlo en
> `False` salvo que tú mismo generaras el archivo y necesites objetos Python.

### `fix_imports`, `encoding` — solo para pickle
`fix_imports` (defecto `True`) y `encoding` (defecto `'ASCII'`) solo intervienen al des-picklar
arrays de objetos guardados con Python 2. Sin relevancia para datos numéricos modernos.

## Round-trip

`np.load` cierra el ciclo de [[np.save]] (`.npy`) y de [[np.savez]] (`.npz`). El `shape` y el
`dtype` salen de la cabecera, así que la recuperación es exacta y sin parámetros.

```python
import numpy as np

# .npy → un array
arr = np.arange(12).reshape(3, 4)
np.save('m.npy', arr)
back = np.load('m.npy')
back.shape == arr.shape and back.dtype == arr.dtype   # True

# .npz → NpzFile (acceso por nombre, lazy)
np.savez('v.npz', x=arr, y=np.ones(5))
with np.load('v.npz') as d:        # cerrar el contenedor
    d.files                        # ['x', 'y']
    xr = d['x']                    # ahora sí se materializa el array x
    xr.shape                       # (3, 4)
```

### Conservación del shape en 4D/5D

La forma N-D entera se restaura desde la cabecera; nada se aplana.

```python
t5 = np.random.rand(2, 3, 4, 5, 6)     # tensor 5D
np.save('t5.npy', t5)

vuelto = np.load('t5.npy')
vuelto.shape                   # (2, 3, 4, 5, 6)  ← se conserva la forma 5D
vuelto.shape == t5.shape       # True
np.array_equal(vuelto, t5)     # True
```

## Casos de uso

### Recuperar un checkpoint

```python
pesos = np.load('modelo.npy')
```

### Iterar el contenido de un `.npz`

```python
with np.load('datos.npz') as d:
    for nombre in d.files:
        print(nombre, d[nombre].shape)   # se materializa array a array
```

### Leer un array enorme por porciones (sin cargarlo entero)

```python
grande = np.load('dataset.npy', mmap_mode='r')
for i in range(0, len(grande), 1000):
    bloque = np.asarray(grande[i:i+1000])   # solo este bloque en RAM
```

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| `Cannot load file containing pickled data` | array de objetos y `allow_pickle=False` | `allow_pickle=True` **solo si confías** en el archivo |
| Esperabas un array y recibes `NpzFile` | el archivo era `.npz` | indexar por nombre: `d['x']` |
| `KeyError` al indexar el `NpzFile` | nombre inexistente | revisar `d.files` |
| Archivo `.npz` que no se libera | `np.load` sin cerrar | usar `with np.load(...) as d:` |
| Pierdes la ventaja de `mmap_mode` | materializas todo el array | acceder por porciones, no `np.asarray(todo)` |

## Notas relacionadas

- [[concepto_dtype]] — el metadato que la cabecera restaura
- [[np.save]] — guardar un array (inverso de `.npy`)
- [[np.savez]] · [[np.savez_compressed]] — guardar varios (inverso de `.npz`)
- [[np.memmap]] — el array mapeado que devuelve `mmap_mode`
