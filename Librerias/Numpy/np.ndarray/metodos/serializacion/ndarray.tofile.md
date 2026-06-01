---
title: ndarray.tofile — Escribir los datos crudos a un archivo
aliases:
  - tofile
  - ndarray.tofile
tags:
  - numpy
  - api/metodo
  - io
lib: numpy
obj: ndarray
tipo: metodo
retorna: None
inplace: false
draft: false
---

# ndarray.tofile — Escribir los datos crudos a un archivo

## Firma del método

```python
ndarray.tofile(
    fid,
    sep="",
    format="%s"
) -> None
```

## Valor de retorno

| Retorna | Significado |
|---------|-------------|
| `None` | Vuelca el contenido del buffer al archivo; **no** modifica el array (solo lo exporta). |

Escribe **solo los datos crudos**, sin metadatos de `shape` ni [[concepto_dtype|dtype]]. Por eso al recuperar con `np.fromfile` debes indicar tú el dtype y reconstruir la forma. Contrasta con [[np.save]], que sí guarda esos metadatos en formato `.npy`.

```python
import numpy as np
arr = np.arange(6, dtype=np.int32).reshape(2, 3)
arr.tofile('datos.bin')                 # binario crudo, 24 bytes
np.fromfile('datos.bin', dtype=np.int32)
# array([0, 1, 2, 3, 4, 5])  → forma (2,3) PERDIDA, se aplana
```

## Parámetros en detalle

| Parámetro | Tipo | Descripción |
|-----------|------|-------------|
| `fid` | str / file | Ruta u objeto archivo abierto. |
| `sep` | str | Separador. `""` (def.) → binario crudo. Cualquier otro → texto. |
| `format` | str | Formato de cada elemento en modo texto (ej. `"%.4f"`). |

```python
arr.tofile('datos.txt', sep=',')        # texto: "0,1,2,3,4,5"
arr.tofile('datos.txt', sep=',', format='%.2f')
```

## Casos de uso

```python
# Volcado binario compacto para interoperar con C/Fortran
arr.astype(np.float64).tofile('buffer.dat')

# Recuperación (debes conocer dtype y reformar a mano)
back = np.fromfile('buffer.dat', dtype=np.float64).reshape(2, 3)
```

## Buenas prácticas

1. Anota aparte `dtype` y `shape`: el archivo no los conserva.
2. Fija el dtype con `astype` antes de exportar para que sea portable.
3. Si necesitas preservar la forma, prefiere [[np.save]] en vez de `tofile`.

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| Datos basura al leer | dtype erróneo en `np.fromfile` | usar el mismo dtype que se escribió |
| Array 1D inesperado | `tofile` no guarda shape | reformar con `.reshape(...)` tras leer |
| No portable entre máquinas | endianness/dtype dependiente | fijar dtype explícito (ej. `<f8`) |

## Notas relacionadas

- [[concepto_dtype]]
- [[np.fromfile]]
- [[np.save]]
