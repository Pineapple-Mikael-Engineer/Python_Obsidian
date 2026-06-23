---
title: np.loadtxt — lee un archivo de texto delimitado a un array
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
  - concepto_shape

draft: false
---

# np.loadtxt — lee un archivo de texto delimitado a un array

`np.loadtxt` parsea un archivo de **texto** legible (CSV, TSV, columnas separadas por espacios) y lo
convierte en un `ndarray`. Es la vía **rápida** de entrada cuando los datos están **limpios y son
regulares**: misma cantidad de columnas en cada fila, todo numérico, sin huecos. Su contrato es
estricto a propósito —si una celda no se puede convertir, **falla**—, y esa rigidez es justo lo que
la hace veloz. En cuanto los datos están "sucios" (faltantes, tipos mixtos) hay que delegar en
[[np.genfromtxt]].

## La idea

Un archivo de texto es una rejilla de caracteres; `loadtxt` la lee fila a fila, parte cada línea por
el `delimiter` y convierte cada campo al `dtype` pedido. El resultado es una rejilla numérica:

$$ \text{texto } (R \text{ líneas} \times C \text{ campos}) \ \xrightarrow{\ \text{loadtxt}\ }\ \text{ndarray } (R', C) $$

donde $R' = R - \texttt{skiprows}$ (descontando comentarios y cabeceras saltadas). Típicamente el
resultado es **2D** `(filas, columnas)`; si solo hay una columna o una fila, colapsa a **1D** `(n,)`.
Con `unpack=True` el array se **transpone** para que cada columna sea una variable.

## Firma

```python
np.loadtxt(
    fname,                 # str | Path | file | generador de líneas
    dtype=float,           # dtype: tipo de TODAS las celdas del array
    comments='#',          # str | seq[str] | None: marca de comentario
    delimiter=None,        # str | None: separador de campos (None = espacios)
    converters=None,       # dict | callable: conversores por columna
    skiprows=0,            # int: líneas iniciales a ignorar
    usecols=None,          # int | seq[int] | None: columnas a leer
    unpack=False,          # bool: transponer (columnas → variables)
    ndmin=0,               # int {0,1,2}: dimensión mínima del resultado
    encoding=None,         # str | None: codificación del archivo
    max_rows=None,         # int | None: máximo de filas de datos a leer
) -> ndarray
```

## Los parámetros en detalle

### `fname` — la fuente
`str`/`Path` a un archivo, un objeto archivo ya abierto, o cualquier **generador de líneas**.
Acepta `.gz`/`.bz2` y los descomprime al vuelo. Es el único parámetro obligatorio.

### `dtype` — tipo de TODAS las celdas
Por defecto `float`. `loadtxt` aplica **un solo `dtype` a todo el array** (ver [[concepto_dtype]]):
si pones `dtype=int` y una celda trae `3.5`, falla. Para columnas de tipos distintos necesitas un
`dtype` estructurado (engorroso aquí) o directamente [[np.genfromtxt]].

```python
np.loadtxt('enteros.txt', dtype=int)        # toda la rejilla como int
np.loadtxt('texto.txt', dtype=str)          # strings (p. ej. etiquetas)
```

### `delimiter` — separador de campos
`None` (defecto) parte por **cualquier racha de espacios en blanco** (espacios o tabs). Para CSV usa
`','`; para TSV `'\t'`; para un ancho fijo, una secuencia de enteros. Es el error #1 cuando "las
columnas salen mal".

```python
np.loadtxt('datos.csv', delimiter=',')      # CSV
np.loadtxt('datos.tsv', delimiter='\t')     # TSV
```

### `comments` — líneas a ignorar por contenido
Marca(s) de comentario; todo lo que siga (incluso a media línea) se descarta. Defecto `'#'`. Puede
ser una lista (`['#', '//']`) o `None` para no tratar nada como comentario (más rápido).

### `converters` — conversión por columna
`dict` `{índice_columna: función}` o un único callable. Permite parsear formatos que no convierten
solos: comas decimales, fechas, porcentajes. Cada función recibe el **campo como string** y devuelve
el valor.

```python
# columna 0 con coma decimal europea: "3,14" → 3.14
np.loadtxt('eu.csv', delimiter=';',
           converters={0: lambda s: float(s.replace(',', '.'))})
```

### `skiprows` — saltar cabeceras
Número de líneas **iniciales** a ignorar antes de empezar a parsear. El uso típico es `skiprows=1`
para descartar una fila de títulos de columna que no es numérica.

### `usecols` — qué columnas leer
`int` o secuencia de índices (base 0); `usecols=(0, 2)` lee solo esas dos. Reduce el ancho del
array y evita parsear columnas que no interesan (o que son texto y romperían el `dtype`). Acepta
índices negativos.

### `unpack` — columnas como variables
Si `True`, **transpone** el resultado: en vez de `(filas, columnas)` devuelve `(columnas, filas)`,
de modo que cada columna se asigna a una variable distinta. Es el modismo para separar `x, y` de un
archivo de dos columnas.

```python
x, y = np.loadtxt('xy.csv', delimiter=',', unpack=True)
```

### `ndmin` — forzar dimensión mínima
`0` (defecto), `1` o `2`. Garantiza que el resultado tenga al menos esa dimensión: con `ndmin=2`,
un archivo de una sola fila o columna sigue saliendo como `(1, n)` / `(n, 1)` en vez de colapsar a
`(n,)`. Útil para que el shape sea **predecible** aguas abajo.

### `encoding` — codificación del texto
`None` usa la del sistema. Fíjalo (`'utf-8'`, `'latin-1'`) si el archivo trae acentos o símbolos y
ves errores de decodificación.

### `max_rows` — limitar filas leídas
Lee como mucho ese número de **filas de datos** (tras `skiprows`). Sirve para inspeccionar un trozo
de un archivo grande sin cargarlo entero.

## Round-trip

`loadtxt` es la mitad de lectura de la pareja con [[np.savetxt]]: lo que uno escribe, el otro lo
recupera —siempre que el `delimiter` coincida y la cabecera se trate igual—.

```python
import numpy as np

A = np.array([[1.0, 2.0, 3.0],
              [4.0, 5.0, 6.0]])

np.savetxt('m.csv', A, delimiter=',', fmt='%.6f')   # escribe texto
B = np.loadtxt('m.csv', delimiter=',')              # lo lee de vuelta

np.allclose(A, B)   # True  (igualdad hasta la precisión de fmt)
```

> [!warning] El round-trip exacto no está garantizado en floats
> El texto guarda **dígitos decimales**, no el valor binario. Con `fmt='%.6f'` pierdes precisión
> frente al `float64` original; usa `fmt='%.18e'` (el defecto) para ida y vuelta sin pérdida, o el
> formato binario [[np.save]]/[[np.load]] si quieres bit a bit.

Si `savetxt` escribió una cabecera con `header=`, esta queda prefijada por `comments` (`'# '`), así
que `loadtxt` la salta sola por el defecto `comments='#'`. Si guardaste con `comments=''` (cabecera
"limpia"), tendrás que descartarla con `skiprows=1` al leer.

## Casos de uso

### Leer columnas a variables (unpack)
```python
t, v = np.loadtxt('medidas.txt', skiprows=1, unpack=True)
# t = primera columna, v = segunda columna
```

### Seleccionar columnas de un CSV ancho
```python
# archivo con 5 columnas; solo quiero la 0 (tiempo) y la 3 (señal)
tiempo, senal = np.loadtxt('log.csv', delimiter=',',
                           usecols=(0, 3), unpack=True)
```

### Saltar metadatos y comentarios
```python
# las 3 primeras líneas son metadatos; el archivo usa ';' y comenta con '//'
np.loadtxt('exp.txt', delimiter=';', comments='//', skiprows=3)
```

### Forzar 2D para un archivo de una fila
```python
np.loadtxt('una_fila.csv', delimiter=',', ndmin=2).shape   # (1, n), no (n,)
```

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| `could not convert string to float` | celda vacía, texto, o coma decimal | usar [[np.genfromtxt]] o `converters=` |
| Columnas mal separadas / array 1D inesperado | `delimiter` por defecto (espacios) en un CSV | indicar `delimiter=','` |
| Cabecera parseada como datos | no se saltó la fila de títulos | `skiprows=1` |
| `ValueError: Wrong number of columns` | filas con distinto número de campos | datos irregulares → [[np.genfromtxt]] |
| Resultado `(n,)` cuando se esperaba `(n,1)` | una sola columna colapsa a 1D | `ndmin=2` |
| `UnicodeDecodeError` | acentos con codificación errónea | `encoding='utf-8'` |

## Notas relacionadas

- [[np.savetxt]] — la pareja de escritura (round-trip de texto)
- [[np.genfromtxt]] — la versión robusta para datos con huecos o tipos mixtos
- [[concepto_dtype]] — por qué `loadtxt` exige un único tipo para todo el array
- [[np.load]] · [[Librerias/Numpy/np/io/index|índice de io]]
