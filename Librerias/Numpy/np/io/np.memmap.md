---
title: np.memmap — Array mapeado a un archivo en disco
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

# np.memmap — Array mapeado a un archivo en disco

## Firma de la función

```python
np.memmap(
    filename,
    dtype=uint8,
    mode='r+',
    offset=0,
    shape=None,
    order='C'
) -> memmap
```

## Valor de retorno

Devuelve un array **mapeado a memoria**: se comporta como un [[concepto_ndarray|ndarray]] pero los datos viven en **disco**, no en RAM. El sistema operativo carga solo las porciones que se acceden. Permite trabajar con arrays **más grandes que la memoria**.

```python
import numpy as np
# Array de 1 GB sin cargarlo entero en RAM
mm = np.memmap('grande.dat', dtype='float32', mode='w+', shape=(250_000, 1000))
mm[0] = np.arange(1000)     # se escribe en disco
mm.flush()                  # fuerza el volcado
```

## El parámetro `mode`

| `mode` | Significado |
|--------|-------------|
| `'r'` | solo lectura |
| `'r+'` | lectura/escritura (archivo existente) |
| `'w+'` | crear/sobrescribir (lectura/escritura) |
| `'c'` | copy-on-write (cambios no se guardan) |

## Parámetros en detalle

### `filename` — archivo de respaldo

Archivo binario en disco que almacena los datos.

### `dtype`, `shape` — interpretación

Como un buffer crudo: **debes especificar** `dtype` y `shape` para interpretarlo (no se guardan en el archivo, a diferencia de `.npy`).

### `offset` — desplazamiento

Bytes a saltar al inicio (útil si el archivo tiene cabecera).

## memmap vs load(mmap_mode)

[[np.load]] con `mmap_mode='r'` da un memmap **a partir de un .npy** (que sí guarda shape/dtype). `np.memmap` trabaja con un binario crudo donde tú defines la interpretación.

## Casos de uso

### Procesar un dataset enorme por partes

```python
mm = np.memmap('datos.dat', dtype='float32', mode='r', shape=(N, D))
for i in range(0, N, 1000):
    bloque = mm[i:i+1000]    # solo este bloque entra en RAM
```

## Buenas prácticas

1. Llama a `.flush()` para asegurar que los cambios llegan a disco.
2. Para `.npy` con metadatos, prefiere [[np.load]] con `mmap_mode`.
3. Accede por **bloques** para no traer todo a RAM (anula la ventaja).

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| Datos basura al leer | `dtype`/`shape` incorrectos | deben coincidir con cómo se escribió |
| Cambios no persisten | falta `flush` o `mode='c'` | usar `'r+'`/`'w+'` y `.flush()` |

## Limitaciones

- El archivo crudo no guarda `dtype`/`shape`: debes conocerlos.
- El rendimiento depende del acceso a disco.

## Notas relacionadas

- [[concepto_shape]]
- [[concepto_dtype]]
- [[np.load]]
- [[np.save]]
