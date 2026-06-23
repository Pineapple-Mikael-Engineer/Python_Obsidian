---
title: np.genfromtxt — lee texto con valores faltantes y tipos mixtos
aliases:
  - genfromtxt
  - np.genfromtxt
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
  - concepto_shape

draft: false
---

# np.genfromtxt — lee texto con valores faltantes y tipos mixtos

`np.genfromtxt` es la versión **robusta** de [[np.loadtxt]]: lee el mismo tipo de archivos de texto
delimitado, pero tolera lo que `loadtxt` no soporta —**celdas vacías**, valores no numéricos,
**columnas de tipos distintos** y cabeceras con nombres—. El precio es la **velocidad**: hace dos
pasadas y mucha lógica de inferencia, así que es claramente más lenta. La regla de oro: usa
`loadtxt` para datos limpios y rápidos; cambia a `genfromtxt` cuando los datos están **"sucios"** o
necesitas un **array estructurado** con columnas nombradas.

## La idea

Como `loadtxt`, mapea una rejilla de texto a un array; la diferencia está en cómo trata las celdas
problemáticas. En vez de fallar ante un campo vacío, lo **detecta** (`missing_values`) y lo
**rellena** (`filling_values`):

$$ \text{texto con huecos } (R, C)\ \xrightarrow{\ \text{genfromtxt}\ }\ \text{ndarray } (R', C) $$

Con `names=True`, el resultado deja de ser una rejilla homogénea y pasa a ser un **array
estructurado**: 1D de longitud $R'$ donde cada elemento es un registro con campos nombrados, y cada
columna puede tener su propio `dtype` (ver [[concepto_dtype]]). Ese es el modo más potente —y el
que más lo diferencia de `loadtxt`—.

## Firma

```python
np.genfromtxt(
    fname,                  # str | Path | file | generador de líneas
    dtype=float,            # dtype | None: tipo; None infiere por columna
    comments='#',           # str: marca de comentario
    delimiter=None,         # str | int | seq[int] | None: separador
    skip_header=0,          # int: líneas iniciales a saltar
    skip_footer=0,          # int: líneas finales a saltar
    converters=None,        # dict: conversores por columna
    missing_values=None,    # str | seq | dict: qué cuenta como faltante
    filling_values=None,    # valor | seq | dict: con qué rellenar el hueco
    usecols=None,           # int | seq[int] | None: columnas a leer
    names=None,             # bool | str | seq: nombres de columna
    unpack=False,           # bool: transponer (columnas → variables)
    encoding=None,          # str | None: codificación
) -> ndarray
```

## Los parámetros en detalle

### `fname` — la fuente
Igual que en [[np.loadtxt]]: archivo, `Path`, objeto abierto o generador de líneas; soporta
`.gz`/`.bz2`.

### `dtype` — tipo, o inferencia automática
Defecto `float`. Lo distintivo: con `dtype=None`, `genfromtxt` **infiere el tipo de cada columna por
separado** (una columna queda `int`, otra `float`, otra `str`). Es lo que permite los **tipos
mixtos** que `loadtxt` no maneja.

```python
# cada columna toma su propio tipo
np.genfromtxt('mixto.csv', delimiter=',', dtype=None, encoding='utf-8')
```

### `delimiter` — separador de campos
`None` parte por espacios en blanco; `','`/`'\t'` para CSV/TSV. También acepta un **entero o
secuencia de enteros** para campos de **ancho fijo** (sin separador explícito), algo que `loadtxt`
hace peor.

### `comments` — líneas a ignorar
Marca de comentario, defecto `'#'`. Todo lo que la siga se descarta.

### `skip_header` / `skip_footer` — recortar extremos
`skip_header` salta líneas al **principio** (equivale al `skiprows` de `loadtxt`); `skip_footer`
salta líneas al **final** —útil para descartar totales o notas al pie que no son datos—.

### `missing_values` — qué cuenta como faltante
Define las cadenas que se interpretan como **hueco**: `''` (vacío), `'NA'`, `'NaN'`, `'-'`... Puede
ser un valor único, una lista, o un `dict` por columna. Si no se pone, una celda vacía ya se
considera faltante.

### `filling_values` — con qué rellenar el hueco
El valor que sustituye cada faltante detectado. Defecto: `nan` para floats, `-1` para enteros,
`'???'` para strings. Acepta un escalar (para todo), o un `dict` `{columna: valor}` para rellenar
distinto en cada columna.

```python
# columna 0 → rellena con 0; columna 2 → rellena con -1
np.genfromtxt('sucio.csv', delimiter=',',
              filling_values={0: 0, 2: -1})
```

### `converters` — conversión por columna
`dict` `{columna: función}` que recibe el campo como string. Igual que en [[np.loadtxt]], pero aquí
es habitual combinarlo con la lógica de faltantes (p. ej. mapear `'sí'/'no'` a `1/0`).

### `usecols` — qué columnas leer
`int` o secuencia de índices; con `names`, también acepta los **nombres** de columna. Descarta el
resto.

### `names` — columnas con nombre (array estructurado)
El otro gran diferenciador. `names=True` lee la **primera fila** como nombres y devuelve un **array
estructurado** accesible por nombre. También puedes pasar la lista de nombres tú mismo
(`names=['t', 'v']`) o una cadena separada por comas.

```python
d = np.genfromtxt('clima.csv', delimiter=',', names=True, dtype=None, encoding='utf-8')
d['temperatura']     # accede a la columna por nombre
d.dtype.names        # ('fecha', 'temperatura', ...)
```

### `unpack` — columnas como variables
Si `True`, transpone para asignar cada columna a una variable, igual que en `loadtxt`. Con `names`,
desempaqueta los campos del array estructurado.

### `encoding` — codificación
Fíjala (`'utf-8'`) sobre todo al usar `dtype=None`/columnas de texto con acentos.

## Round-trip

`genfromtxt` **lee**; no tiene una pareja de escritura propia. El par escritura/lectura de NumPy
sigue siendo [[np.savetxt]] ↔ [[np.loadtxt]]. `genfromtxt` entra cuando el texto que escribió otro
(o un export con huecos) **no es lo bastante limpio** para `loadtxt`:

```python
import numpy as np

# savetxt produce texto regular y sin huecos → loadtxt basta para releerlo
A = np.array([[1.0, 2.0], [3.0, 4.0]])
np.savetxt('limpio.csv', A, delimiter=',')
np.loadtxt('limpio.csv', delimiter=',')        # round-trip estándar

# genfromtxt es para el archivo que llega de fuera con celdas vacías:
# "1,2\n3,\n,4"  →  rellena los huecos en vez de fallar
np.genfromtxt('externo.csv', delimiter=',', filling_values=0)
```

> [!note] Si vas a guardar tú, guarda limpio
> Lo que escribes con [[np.savetxt]] no tiene huecos, así que se relee con [[np.loadtxt]] (más
> rápido). `genfromtxt` está pensado para datos **ajenos** o irregulares, no para tu propio
> round-trip.

## Casos de uso

### Leer un CSV con celdas vacías
```python
# rellena cada hueco con NaN (defecto en floats) o con el valor que elijas
np.genfromtxt('datos.csv', delimiter=',', filling_values=np.nan)
```

### Array estructurado con columnas nombradas
```python
tabla = np.genfromtxt('ventas.csv', delimiter=',', names=True,
                      dtype=None, encoding='utf-8')
tabla['region']          # columna por nombre
tabla['importe'].mean()  # operar sobre un campo
```

### Tipos mixtos inferidos por columna
```python
# id (int), nombre (str), precio (float) en el mismo archivo
np.genfromtxt('catalogo.csv', delimiter=',', dtype=None, encoding='utf-8')
```

### Descartar cabecera y pie
```python
np.genfromtxt('reporte.csv', delimiter=',',
              skip_header=2, skip_footer=1)   # 2 líneas de título, 1 de total
```

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| `nan` inesperados en columnas | huecos rellenados con el defecto | ajustar `filling_values` (o validar la fuente) |
| Strings como `b'texto'` | codificación por defecto en bytes | `encoding='utf-8'` |
| Tipos mal inferidos | `dtype` fijo en `float` ante texto | `dtype=None` para inferir por columna |
| No se puede indexar por nombre | falta `names=True` | `names=True` para array estructurado |
| Rendimiento lento en archivos grandes | genfromtxt hace doble pasada | si los datos están limpios, [[np.loadtxt]]; si son enormes, binario [[np.load]] o pandas |

## Notas relacionadas

- [[np.loadtxt]] — la versión rápida para datos limpios (sin huecos ni tipos mixtos)
- [[np.savetxt]] — la escritura de texto (su pareja de lectura es `loadtxt`)
- [[concepto_dtype]] — `dtype=None` y la inferencia por columna del array estructurado
- [[np.load]] · [[Librerias/Numpy/np/io/index|índice de io]]
