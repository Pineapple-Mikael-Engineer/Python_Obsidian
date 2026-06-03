---
title: np.loadtxt — Cargar datos numéricos desde texto
aliases:
  - loadtxt
  - np.loadtxt
tags:
  - numpy
  - api/funcion
  - io

# --- Clasificación ---
lib: numpy
mod: np
tipo: funcion

# --- Comportamiento ---
retorna: ndarray
inplace: false

# --- Dependencias ---
requiere:
  - concepto_dtype

draft: false
---

# np.loadtxt — Cargar datos numéricos desde texto

## Firma de la función

```python
np.loadtxt(
    fname,
    dtype=float,
    comments='#',
    delimiter=None,
    skiprows=0,
    usecols=None,
    unpack=False,
    max_rows=None,
    encoding='bytes'
) -> ndarray
```

## Valor de retorno

Devuelve un [[concepto_ndarray|ndarray]] con los datos de un archivo de texto (CSV, TSV...). Rápida, pero **exige datos limpios y regulares** (sin huecos). Para datos con valores faltantes, usa [[np.genfromtxt]].

```python
import numpy as np
datos = np.loadtxt('datos.csv', delimiter=',')
```

## Parámetros en detalle

### `fname` — archivo

Ruta, objeto archivo o generador de líneas.

### `delimiter` — separador

`None` (espacios) por defecto; usa `','` para CSV, `'\t'` para TSV.

### `skiprows` — saltar cabeceras

Número de líneas iniciales a ignorar.

### `usecols` — columnas a leer

Tupla de índices: `usecols=(0, 2)` lee solo esas columnas.

### `unpack` — desempaquetar en columnas

Si `True`, transpone para asignar columnas a variables:

```python
x, y = np.loadtxt('xy.csv', delimiter=',', unpack=True)
```

### `dtype` — tipo de salida

Por defecto `float` (ver [[concepto_dtype]]).

## Casos de uso

### Leer columnas a variables

```python
t, v = np.loadtxt('medidas.txt', skiprows=1, unpack=True)
```

## Buenas prácticas

1. Para datos con **huecos o tipos mixtos**, usa [[np.genfromtxt]] (loadtxt falla).
2. `unpack=True` es cómodo para asignar columnas a variables.
3. Para datasets grandes/complejos, pandas `read_csv` suele ser mejor.

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| `could not convert string to float` | valores faltantes/no numéricos | usar [[np.genfromtxt]] |
| Columnas mal separadas | `delimiter` incorrecto | indicar el separador real |
| Cabecera parseada como datos | no se saltó | `skiprows=1` |

## Limitaciones

- No tolera valores faltantes ni columnas de texto mezcladas.

## Notas relacionadas

- [[concepto_dtype]]
- [[np.savetxt]]
- [[np.genfromtxt]]
- [[np.load]]
