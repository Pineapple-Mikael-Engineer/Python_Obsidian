---
title: np/io — lectura y escritura de arrays en disco
tags:
  - numpy
  - indice
draft: false
---

# np/io — lectura y escritura de arrays en disco

`io/` agrupa las funciones de NumPy para leer y guardar arrays en el sistema de archivos. Hay dos familias principales segun el formato: **texto** (CSV, TSV y similares) y **binario NumPy** (`.npy`, `.npz`). Ademas, [[np.memmap]] permite trabajar con arrays que no caben en RAM mapeandolos directamente desde disco.

## Tabla de decision por caso de uso

| Situacion | Funcion |
|-----------|---------|
| Leer un CSV o archivo de texto regular | [[np.loadtxt]] |
| Guardar un array como texto legible | [[np.savetxt]] |
| Leer un CSV con valores faltantes o cabeceras complejas | [[np.genfromtxt]] |
| Guardar un array en formato binario NumPy | [[np.save]] |
| Cargar un `.npy` o `.npz` desde disco | [[np.load]] |
| Guardar multiples arrays en un solo archivo | [[np.savez]] |
| Guardar multiples arrays con compresion | [[np.savez_compressed]] |
| Array muy grande que no cabe en RAM | [[np.memmap]] |

## Dos formatos, dos casos de uso

### Texto (CSV / TSV)

Interoperable con Excel, pandas, otros lenguajes. Mas lento y ocupa mas espacio.

```python
import numpy as np

# Guardar
arr = np.array([[1.0, 2.0], [3.0, 4.0]])
np.savetxt("datos.csv", arr, delimiter=",", header="x,y")

# Leer
arr2 = np.loadtxt("datos.csv", delimiter=",", skiprows=1)
```

### Binario NumPy (.npy / .npz)

Preserva dtype, shape y orden de memoria exactos. Mucho mas rapido y compacto.

```python
# Un solo array
np.save("arr.npy", arr)
arr3 = np.load("arr.npy")

# Multiples arrays
np.savez("multi.npz", a=arr, b=arr2)
data = np.load("multi.npz")
data["a"]   # recupera el array "a"
```

## Notas de la carpeta

- [[np.loadtxt]] — leer archivos de texto con formato regular
- [[np.savetxt]] — guardar array como texto (CSV, TSV, etc.)
- [[np.genfromtxt]] — leer texto con valores faltantes o estructura irregular
- [[np.load]] — cargar archivos `.npy` o `.npz`
- [[np.save]] — guardar un array en formato binario `.npy`
- [[np.savez]] — guardar multiples arrays en un `.npz` sin compresion
- [[np.savez_compressed]] — guardar multiples arrays en un `.npz` comprimido
- [[np.memmap]] — array mapeado a memoria desde un archivo binario en disco
