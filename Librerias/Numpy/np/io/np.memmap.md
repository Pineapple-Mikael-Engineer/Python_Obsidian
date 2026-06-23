---
title: np.memmap — mapea un array de disco a memoria (acceso sin cargarlo entero)
aliases:
  - memmap
  - np.memmap
  - memory map
tags:
  - numpy
  - api/funcion
  - io

# --- Clasificación ---
lib: numpy
mod: np
tipo: funcion

# --- Comportamiento ---
retorna: memmap
inplace: false

# --- Dependencias ---
requiere:
  - concepto_shape
  - concepto_dtype

draft: false
---

# np.memmap — mapea un array de disco a memoria

`np.memmap` crea un array cuyos datos viven en un **archivo en disco** en lugar de en RAM. Se
comporta como un [[concepto_ndarray|ndarray]] normal (se indexa, se sectoriza, se opera), pero el
sistema operativo trae a memoria **solo las porciones que se acceden**. Es la herramienta para
trabajar con arrays **más grandes que la RAM**: un dataset de cientos de GB se abre sin cargarse
entero, y cada lectura/escritura toca solo la página de disco implicada.

## La idea

A diferencia de [[np.save]] (`.npy`), el archivo de respaldo de un `memmap` es un **binario crudo**:
no lleva cabecera, así que **tú** debes declarar cómo interpretarlo (`dtype`, `shape`, `order`),
igual que con [[ndarray.tofile]]. El array resultante es una **ventana** sobre ese archivo:

```
disco:  [ ────────── archivo binario crudo de N bytes ────────── ]
                ▲ solo esta porción
memmap[i:j] ────┘ se pagina a RAM al accederla
```

Frente a cargar el array entero, esto cambia el modelo: el coste no es "todo en RAM de golpe" sino
"E/S de disco bajo demanda". Comparado con [[np.load]] usando `mmap_mode`, la diferencia es de dónde
salen los metadatos:

| | `np.memmap` | [[np.load]] con `mmap_mode='r'` |
|--|-------------|----------------------------------|
| Archivo de respaldo | binario **crudo** (sin cabecera) | `.npy` (con cabecera) |
| `dtype`/`shape` | **los das tú** | salen del `.npy` |
| Cuándo | interoperar con buffers crudos C/Fortran | mapear un `.npy` que tú guardaste |

## Firma

```python
np.memmap(
    filename,            # str | Path | file-object: archivo de respaldo en disco
    dtype=np.uint8,      # dtype: cómo interpretar los bytes
    mode='r+',           # {'r','r+','w+','c'}: modo de acceso (ver tabla)
    offset=0,            # int: bytes a saltar al inicio del archivo
    shape=None,          # tuple[int]: forma del array (None → todo el archivo, 1D)
    order='C',           # {'C','F'}: orden de almacenamiento en memoria
) -> memmap
```

## Los parámetros en detalle

### `filename` — archivo de respaldo
`str`, `Path` o un objeto archivo. Es el binario en disco que almacena los datos. Con `mode='w+'` se
crea/sobrescribe; con `'r'`/`'r+'` debe existir ya.

### `dtype` — cómo interpretar los bytes
El tipo con el que se leen los bytes del archivo (defecto `uint8`). **Debe coincidir** con el que se
usó al escribir el archivo; si no, saldrán datos basura (el archivo crudo no guarda esta
información, ver [[concepto_dtype]]).

### `mode` — modo de acceso
Controla lectura/escritura y si se crea el archivo:

| `mode` | Significado |
|--------|-------------|
| `'r'` | solo lectura (archivo existente) |
| `'r+'` | lectura/escritura (archivo existente) |
| `'w+'` | crear/sobrescribir, lectura/escritura |
| `'c'` | copy-on-write: se puede modificar en RAM, **no** se vuelca a disco |

### `offset` — bytes iniciales a saltar
`int` (defecto 0). Salta una cabecera u otros datos al principio del archivo antes de empezar a
mapear. Útil si el binario tiene un encabezado propio.

### `shape` — la forma N-D del array
`tuple[int]`. Junto con `dtype` define cómo se trocean los bytes en un array N-D (ver
[[concepto_shape]]). Si es `None`, el archivo entero se mapea como un array **1D**. Es lo que hace
que un `memmap` pueda ser 4D o 5D pese a que el archivo es un chorro plano de bytes.

### `order` — orden de almacenamiento
`'C'` (filas, defecto) o `'F'` (columnas). Debe coincidir con cómo se escribieron los bytes.

## Round-trip

El ciclo aquí es: escribir con `mode='w+'`, volcar con `.flush()`, reabrir con `mode='r'`. Como el
archivo es crudo, **el mismo `dtype` y `shape`** deben repetirse en ambos extremos (no se guardan).

```python
import numpy as np

arr = np.arange(24, dtype='float32').reshape(2, 3, 4)

# escribir
mm = np.memmap('m.dat', dtype='float32', mode='w+', shape=(2, 3, 4))
mm[:] = arr
mm.flush()                       # fuerza el volcado a disco

# reabrir (hay que repetir dtype y shape: el archivo crudo no los guarda)
back = np.memmap('m.dat', dtype='float32', mode='r', shape=(2, 3, 4))
back.shape == arr.shape          # True → (2, 3, 4)
np.array_equal(np.asarray(back), arr)   # True
```

### Conservación del shape en 4D/5D

El `shape` no vive en el archivo, lo aporta el parámetro: pásalo igual al reabrir y la forma N-D se
reconstruye exacta.

```python
t5 = np.random.rand(2, 4, 8, 8, 3).astype('float64')   # tensor 5D

mm = np.memmap('t5.dat', dtype='float64', mode='w+', shape=(2, 4, 8, 8, 3))
mm[:] = t5
mm.flush()

vuelto = np.memmap('t5.dat', dtype='float64', mode='r', shape=(2, 4, 8, 8, 3))
vuelto.shape                     # (2, 4, 8, 8, 3)  ← se reconstruye la forma 5D
vuelto.shape == t5.shape         # True
np.array_equal(np.asarray(vuelto), t5)   # True
```

## Casos de uso

### Procesar un dataset más grande que la RAM por bloques

```python
mm = np.memmap('datos.dat', dtype='float32', mode='r', shape=(N, D))
total = np.zeros(D)
for i in range(0, N, 1000):
    total += mm[i:i+1000].sum(axis=0)   # solo este bloque entra en RAM
```

### Escribir resultados incrementales en disco

```python
out = np.memmap('salida.dat', dtype='float32', mode='w+', shape=(N, D))
for i, fila in enumerate(generar()):
    out[i] = fila                       # se escribe directo en disco
out.flush()
```

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| Datos basura al leer | `dtype`/`shape`/`order` no coinciden con la escritura | repetir exactamente los mismos |
| Cambios que no persisten | falta `.flush()` o se usó `mode='c'` | usar `'r+'`/`'w+'` y llamar a `.flush()` |
| Se agota la RAM igualmente | se materializó todo (`np.asarray(mm)`) | acceder por **bloques**, no de golpe |
| `FileNotFoundError` con `mode='r'` | el archivo no existe | crear primero con `'w+'` |

## Notas relacionadas

- [[concepto_shape]] — define cómo se trocean los bytes crudos en N-D
- [[concepto_dtype]] — el tipo que debes declarar (no se guarda en el archivo)
- [[np.load]] — alternativa con `mmap_mode` cuando el respaldo es un `.npy` con cabecera
- [[np.save]] · [[ndarray.tofile]]
