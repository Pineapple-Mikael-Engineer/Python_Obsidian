---
title: np.load — Cargar arrays desde .npy / .npz
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
retorna: ndarray o NpzFile
inplace: false

# --- Dependencias ---
requiere:
  - concepto_dtype

draft: false
---

# np.load — Cargar arrays desde .npy / .npz

## Firma de la función

```python
np.load(
    file,
    mmap_mode=None,
    allow_pickle=False,
    encoding='ASCII'
) -> ndarray | NpzFile
```

## Valor de retorno

Carga datos guardados con [[np.save]] (`.npy`) o [[np.savez]] (`.npz`), restaurando `shape` y [[concepto_dtype|dtype]] exactos.

| Archivo | Retorno |
|---------|---------|
| `.npy` | un `ndarray` |
| `.npz` | objeto `NpzFile` (dict-like; acceso por nombre) |

```python
import numpy as np
arr = np.load('datos.npy')          # un array

archivo = np.load('varios.npz')     # contenedor
x = archivo['x']                    # acceso por nombre
```

## Parámetros en detalle

### `file` — archivo a cargar

Ruta a `.npy`/`.npz` u objeto archivo.

### `mmap_mode` — mapeo en memoria

`'r'`, `'r+'`...: carga el array como [[np.memmap|memory-map]] sin leerlo entero en RAM (ideal para archivos enormes).

```python
grande = np.load('enorme.npy', mmap_mode='r')   # no carga todo en RAM
```

### `allow_pickle` — seguridad

Por defecto `False` (más seguro). Necesario `True` solo para arrays de objetos; **no** lo actives con archivos de origen no confiable.

## Casos de uso

### Recuperar un checkpoint

```python
pesos = np.load('modelo.npy')
```

### Iterar el contenido de un .npz

```python
with np.load('datos.npz') as d:
    for nombre in d.files:
        print(nombre, d[nombre].shape)
```

## Buenas prácticas

1. Para `.npz`, cierra el archivo (usa `with`) o accede por nombre.
2. Usa `mmap_mode='r'` con archivos que no caben en memoria.
3. Mantén `allow_pickle=False` salvo necesidad real (seguridad).

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| `Cannot load file containing pickled data` | array de objetos | `allow_pickle=True` (si confías) |
| Esperar array y recibir `NpzFile` | era un `.npz` | indexar por nombre (`d['x']`) |

## Limitaciones

- `allow_pickle=True` puede ejecutar código malicioso de archivos no confiables.

## Notas relacionadas

- [[concepto_dtype]]
- [[np.save]]
- [[np.savez]]
- [[np.memmap]]
