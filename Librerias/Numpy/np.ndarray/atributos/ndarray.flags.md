---
title: ndarray.flags — banderas del layout en memoria
aliases:
  - flags
  - ndarray.flags
tags:
  - numpy
  - api/atributo
  - memoria
lib: numpy
mod: np.ndarray
tipo: atributo
draft: false
---

# ndarray.flags — banderas del layout en memoria

Objeto `numpy.flagsobj` que expone banderas booleanas sobre cómo está dispuesto el array en memoria: contigüidad, propiedad del buffer y si es escribible. Es la herramienta clave para diagnosticar [[concepto_contiguidad_memoria|contigüidad]] y distinguir vistas de copias antes de operar o de pasar el array a código C/Fortran.

## Tipo y lectura/escritura

| Tipo de dato | ¿Asignable? |
|--------------|-------------|
| `numpy.flagsobj` | El objeto es **solo lectura**; algunas banderas sueltas (`WRITEABLE`) sí se asignan, pero las de contigüidad y `OWNDATA` las gestiona NumPy |

Se accede por clave en mayúsculas (`arr.flags['C_CONTIGUOUS']`) o por atributo en minúsculas (`arr.flags.c_contiguous`); son equivalentes.

## En detalle

Las cinco banderas que se consultan a diario:

| Bandera | Significado |
|---------|-------------|
| `C_CONTIGUOUS` | Datos contiguos en orden C (*row-major*, último eje contiguo) |
| `F_CONTIGUOUS` | Datos contiguos en orden Fortran (*column-major*, primer eje contiguo) |
| `OWNDATA` | El array es dueño de su buffer (no es una vista de otro) |
| `WRITEABLE` | Se pueden modificar los elementos |
| `ALIGNED` | Los datos están alineados según el hardware |

```python
import numpy as np

arr = np.array([[1, 2], [3, 4]])    # C-order por defecto
arr.flags.c_contiguous   # True
arr.flags.f_contiguous   # False
arr.flags.owndata        # True

vista = arr.T            # transponer NO copia
vista.flags.owndata      # False   → es una vista
vista.flags.c_contiguous # False
vista.flags.f_contiguous # True    → la T de un C-contiguo es F-contigua
```

## Casos de uso

```python
# Materializar C-contiguo solo si hace falta, antes de una extensión C
if not arr.flags['C_CONTIGUOUS']:
    arr = np.ascontiguousarray(arr)

# Detectar una vista (comparte buffer) sin comparar memorias
es_vista = not arr.flags.owndata

# Proteger un array contra escrituras accidentales
arr.flags.writeable = False
arr[0] = 1   # ValueError: assignment destination is read-only
```

> [!note] `OWNDATA == False` sugiere vista, no lo garantiza
> Es una señal típica de que el array comparte buffer con otro, pero la comprobación robusta de solapamiento es `np.may_share_memory(a, b)`; ver [[concepto_views_vs_copias]].

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| Asumir que un slice/`.T` es C-contiguo | Slicing y transpuesta rompen la contigüidad C | Comprobar `flags['C_CONTIGUOUS']` o usar `np.ascontiguousarray` |
| Escribir en un array con `WRITEABLE == False` | Vistas de buffers de solo lectura | Copiar con `.copy()` antes de modificar |

## Notas relacionadas

- [[concepto_contiguidad_memoria]]
- [[concepto_views_vs_copias]]
- [[ndarray.strides]]
- [[ndarray.T]]
