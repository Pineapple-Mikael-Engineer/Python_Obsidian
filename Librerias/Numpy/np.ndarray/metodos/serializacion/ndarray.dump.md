---
title: ndarray.dump — serializa el array a un archivo con pickle (conserva dtype y shape)
aliases:
  - dump
  - ndarray.dump
tags:
  - numpy
  - api/metodo
  - serializacion
lib: numpy
mod: np.ndarray
obj: ndarray
tipo: metodo
retorna: None
inplace: false
requiere:
  - concepto_dtype
draft: false
---

# ndarray.dump — serializa el array a un archivo con pickle (conserva dtype y shape)

`ndarray.dump` guarda el array en un archivo usando **pickle**, el protocolo de serialización de Python.
A diferencia de [[ndarray.tofile]] y [[ndarray.tobytes]] (que escriben solo bytes crudos), `dump`
serializa el **objeto completo**: conserva el [[concepto_dtype|dtype]], el `shape`, el `order` y todo lo
necesario para reconstruir el array idéntico, sin que tengas que recordar nada. El precio es el de
pickle: **menos portable** entre versiones y con un **riesgo de seguridad** al cargar.

## La idea

El array → un archivo pickle autodescriptivo. Toda la información del objeto viaja dentro del archivo, así
que el round-trip es **exacto y sin metadatos externos**:

$$ \texttt{arr (dtype, shape)}\ \xrightarrow{\ \text{dump → pickle}\ }\ \texttt{archivo}\ \xrightarrow{\ \text{np.load(allow\_pickle=True)}\ }\ \texttt{arr (dtype, shape)} $$

`arr.dump(file)` equivale a `pickle.dump(arr, open(file, "wb"))`.

```python
import numpy as np
arr = np.arange(6, dtype=np.int16).reshape(2, 3)
arr.dump("estado.pkl")                                 # crea estado.pkl
back = np.load("estado.pkl", allow_pickle=True)        # array([[0,1,2],[3,4,5]], int16)
back.dtype, back.shape                                 # (dtype('int16'), (2, 3)) → exacto
```

## Firma

```python
ndarray.dump(file) -> None
```

## Los parámetros en detalle

### `file` — el destino
Una ruta (`str` / `Path`) o un objeto archivo abierto en modo binario (`"wb"`). Si pasas una ruta, NumPy
abre, escribe y cierra el archivo por ti.

```python
arr.dump("estado.pkl")                                 # por ruta
from pathlib import Path
arr.dump(Path("checkpoints") / "estado.pkl")           # con Path
with open("estado.pkl", "wb") as f:
    arr.dump(f)                                         # por handle abierto
```

No hay más parámetros: el protocolo de pickle y el contenido los gestiona NumPy.

## Valor de retorno

`None`: el efecto es el **archivo escrito**. No modifica el array (solo lo exporta). El archivo es un
pickle binario; pesa un poco más que el volcado crudo de `tofile` por el overhead de pickle, a cambio de
llevar todos los metadatos dentro.

## Round-trip

La inversa es `np.load(file, allow_pickle=True)`, o `pickle.load` estándar. Como el pickle es
autodescriptivo, **no hay que pasar dtype ni shape**:

```python
import numpy as np, pickle

arr = np.arange(6, dtype=np.int16).reshape(2, 3)
arr.dump("estado.pkl")

# Opción A — NumPy (requiere allow_pickle):
back = np.load("estado.pkl", allow_pickle=True)
np.array_equal(arr, back) and back.dtype == arr.dtype   # True

# Opción B — pickle estándar:
with open("estado.pkl", "rb") as f:
    back = pickle.load(f)
```

> [!danger] Pickle ejecuta código al cargar
> Deserializar un pickle puede ejecutar código arbitrario: **nunca** cargues archivos `.pkl` de origen no
> confiable. `np.load` exige `allow_pickle=True` precisamente como freno de seguridad. Para datos que
> vienen de fuera, usa formatos sin código embebido (`.npy` vía `np.save`).

## Casos de uso

### Snapshot rápido de un array con dtype y shape exactos
```python
modelo = np.random.rand(100, 100)
modelo.dump("checkpoint.pkl")                          # se recupera idéntico, sin recordar nada
back = np.load("checkpoint.pkl", allow_pickle=True)
```

### Por qué `np.save` suele ser mejor para persistir
`.npy` también conserva dtype y shape, pero es **estable entre versiones** y **seguro** (sin código):

```python
np.save("modelo.npy", modelo)                          # portable y seguro
back = np.load("modelo.npy")                            # sin allow_pickle, round-trip exacto
```

Regla práctica: usa `dump`/pickle solo dentro de tu propio proceso o caché de confianza; para guardar
arrays de verdad, `np.save`.

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| `ValueError: allow_pickle=False` al cargar | `np.load` bloquea pickle por defecto | pasar `allow_pickle=True` (solo si confías en el archivo) |
| No carga en otra versión de NumPy/Python | el formato pickle depende de versiones | usar `.npy` con `np.save` para almacenamiento largo |
| Riesgo de ejecución de código | pickle deserializa código al cargar | no abrir `.pkl` de fuentes ajenas |
| Quería los bytes, no un archivo | `dump` escribe a disco | usar [[ndarray.dumps]] (devuelve `bytes`) |

## Notas relacionadas

- [[concepto_dtype]] — el tipo que `dump` conserva (a diferencia de `tofile`/`tobytes`)
- [[ndarray.dumps]] — misma serialización pickle, pero a `bytes` en memoria
- [[ndarray.tofile]] — alternativa cruda, más rápida pero sin metadatos
- [[np.save]] — persistencia portable y segura en `.npy`
- [[index]] — métodos de serialización del ndarray
