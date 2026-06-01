---
title: ndarray.flags — información sobre el layout en memoria
aliases:
  - flags
  - ndarray.flags
tags:
  - numpy
  - api/atributo
  - memoria
lib: numpy
obj: ndarray
tipo: atributo
draft: false
---

# ndarray.flags — información sobre el layout en memoria

## Qué representa

Objeto `numpy.flagsobj` que expone banderas booleanas describiendo cómo está dispuesto el array en memoria: contigüidad, propiedad del buffer y si es escribible. Es la herramienta clave para diagnosticar [[concepto_contiguidad_memoria|contigüidad]] y distinguir vistas de copias.

## Tipo y acceso

| Tipo de dato | ¿Solo lectura o asignable? |
|--------------|----------------------------|
| `numpy.flagsobj` | El objeto es **solo lectura**; algunas banderas individuales (`WRITEABLE`) son asignables, pero la mayoría (contigüidad, `OWNDATA`) las gestiona NumPy y no se pueden cambiar a mano |

Acceso por mayúsculas (`arr.flags['C_CONTIGUOUS']`) o por atributo en minúsculas (`arr.flags.c_contiguous`).

## Banderas principales

| Bandera | Significado |
|---------|-------------|
| `C_CONTIGUOUS` | Datos contiguos en orden C (row-major, última dimensión contigua) |
| `F_CONTIGUOUS` | Datos contiguos en orden Fortran (column-major) |
| `OWNDATA` | El array es dueño de su buffer (no es una vista de otro) |
| `WRITEABLE` | Se pueden modificar los elementos (asignable) |
| `ALIGNED` | Los datos están alineados respecto al hardware |

## Ejemplos

```python
import numpy as np
arr = np.array([[1, 2], [3, 4]])     # C-order por defecto
arr.flags.c_contiguous   # → True
arr.flags.f_contiguous   # → False
arr.flags.owndata        # → True
```

```python
arr_f = np.array([[1, 2], [3, 4]], order='F')
arr_f.flags.f_contiguous # → True

vista = arr.T            # transponer NO copia
vista.flags.owndata      # → False   es una vista
vista.flags.f_contiguous # → True    T de un C-contiguo es F-contiguo
```

## Detectar vistas vs copias

`OWNDATA == False` es una señal típica de que el array es una vista que comparte buffer con otro; ver [[concepto_views_vs_copias]].

## Notas relacionadas

- [[concepto_contiguidad_memoria]]
- [[concepto_views_vs_copias]]
- [[ndarray.T]]
- [[ndarray.nbytes]]
