---
title: np.savetxt — guarda un array 1D o 2D como texto delimitado
aliases:
  - savetxt
  - np.savetxt
tags:
  - numpy
  - api/funcion
  - io

# --- Clasificación ---
lib: numpy
mod: np
tipo: funcion

# --- Comportamiento ---
retorna: None
inplace: false

# --- Dependencias ---
requiere:
  - concepto_shape
  - concepto_dtype

draft: false
---

# np.savetxt — guarda un array 1D o 2D como texto delimitado

`np.savetxt` vuelca un array a un archivo de **texto legible** (CSV, TSV, columnas por espacios):
cada fila del array es una línea, cada elemento un campo formateado según `fmt`. Es la pareja de
escritura de [[np.loadtxt]] y la salida ideal cuando el destino tiene que ser **portable y humano**
—abrible en cualquier editor, hoja de cálculo u otro lenguaje—. La restricción dura es la
dimensión: **solo acepta arrays 1D o 2D**, porque una rejilla de texto no tiene forma natural de
representar tres o más ejes. Para N-D o para precisión exacta, el formato binario [[np.save]].

## La idea

Guardar es el inverso de cargar: el array 2D se serializa como una rejilla de texto, formateando
cada número con `fmt` y uniendo los campos con `delimiter`.

$$ \text{ndarray } (R, C)\ \xrightarrow{\ \text{savetxt, fmt}\ }\ \text{texto } (R \text{ líneas} \times C \text{ campos}) $$

Un array **1D** `(n,)` se escribe como **una columna** (n líneas de un campo). Un array de **3+
dimensiones** no tiene mapeo a rejilla y lanza `ValueError`. La función **no devuelve nada**
(`None`): su efecto es el archivo en disco.

## Firma

```python
np.savetxt(
    fname,                 # str | Path | file: destino
    X,                     # array_like 1D o 2D: los datos a escribir
    fmt='%.18e',           # str | seq[str]: formato de cada número
    delimiter=' ',         # str: separador entre campos de una fila
    newline='\n',          # str: terminador de línea
    header='',             # str: bloque de texto antes de los datos
    footer='',             # str: bloque de texto tras los datos
    comments='# ',         # str: prefijo de header/footer
    encoding=None,         # str | None: codificación del archivo
) -> None
```

## Los parámetros en detalle

### `fname` — el destino
`str`/`Path`, o un objeto archivo abierto. Si el nombre termina en `.gz`, escribe **comprimido**
con gzip automáticamente.

### `X` — los datos (1D o 2D, no más)
`array_like`. Debe tener **una o dos dimensiones** (ver [[concepto_shape]]); un array `(2, 3, 4)`
lanza `Expected 1D or 2D array, got 3D array`. Si necesitas guardar N-D en texto, primero
`reshape`/`ravel` a 2D y anota tú la forma original (o usa binario).

### `fmt` — cómo se formatea cada número
El parámetro que define la apariencia y la **precisión** del archivo. Usa formato estilo `printf`:

- `'%d'` — enteros.
- `'%.4f'` — punto fijo con 4 decimales (legible, compacto).
- `'%.18e'` — notación científica con 18 dígitos (**defecto**; ida y vuelta sin pérdida en `float64`).
- `'%.3g'` — significativos, elige fijo o científico según convenga.

Puede ser una **lista de formatos**, uno por columna, para mezclar estilos (`['%d', '%.2f']`).

```python
np.savetxt('enteros.csv', X, delimiter=',', fmt='%d')        # sin decimales
np.savetxt('precio.csv',  X, delimiter=',', fmt='%.2f')      # 2 decimales
np.savetxt('mix.csv',     X, delimiter=',', fmt=['%d', '%.3e'])  # por columna
```

### `delimiter` — separador entre campos
Lo que va **entre columnas** de una misma fila. Defecto `' '` (un espacio); `','` para CSV, `'\t'`
para TSV. Debe coincidir con el `delimiter` que use [[np.loadtxt]] al releer.

### `newline` — terminador de línea
Lo que va **al final de cada fila**. Defecto `'\n'`. Cámbialo a `'\r\n'` si el archivo tiene que
consumirse en Windows con herramientas quisquillosas.

### `header` — bloque antes de los datos
Texto que se escribe **antes** de la primera fila. Se prefija con `comments`. Su uso típico es la
fila de nombres de columna.

```python
np.savetxt('d.csv', X, delimiter=',', header='col1,col2')   # → "# col1,col2"
```

### `footer` — bloque tras los datos
Igual que `header` pero al **final** del archivo (también prefijado con `comments`). Útil para notas
o sumarios.

### `comments` — prefijo de header/footer
Cadena que antecede a cada línea de `header`/`footer`; defecto `'# '`. Es la clave del CSV "limpio":
con `comments=''` la cabecera **no** lleva `#` delante y se vuelve un encabezado CSV de verdad.

```python
np.savetxt('limpio.csv', X, delimiter=',',
           header='x,y', comments='')   # primera línea: "x,y" sin '#'
```

### `encoding` — codificación
`None` usa la del sistema. Fíjala (`'utf-8'`) si `header`/`footer` llevan acentos.

## Round-trip

`savetxt` y [[np.loadtxt]] forman un par lectura/escritura: lo escrito se recupera si el
`delimiter` y el tratamiento de la cabecera coinciden.

```python
import numpy as np

A = np.array([[1.0, 2.0, 3.0],
              [4.0, 5.0, 6.0]])

# escribir con cabecera comentada (defecto comments='# ')
np.savetxt('m.csv', A, delimiter=',', header='a,b,c')
B = np.loadtxt('m.csv', delimiter=',')   # la cabecera '# a,b,c' se salta sola

np.allclose(A, B)   # True
```

> [!tip] Dos cabeceras, dos formas de releer
> - Con `comments='# '` (defecto) la cabecera sale como `# a,b,c`; [[np.loadtxt]] la salta sola
>   porque su `comments` también es `'#'`.
> - Con `comments=''` la cabecera es `a,b,c` (CSV estándar); al releer hay que descartarla con
>   `skiprows=1`, porque ya no parece un comentario.

> [!warning] El texto pierde precisión: cuida `fmt`
> `fmt='%.2f'` redondea a 2 decimales en disco; al releer ya no recuperas el `float64` original. Para
> ida y vuelta exacta deja el defecto `'%.18e'`, o usa el binario [[np.save]] (bit a bit, además N-D).

## Casos de uso

### Exportar resultados a un CSV limpio
```python
np.savetxt('resultados.csv', np.column_stack([x, y]),
           delimiter=',', header='x,y', comments='', fmt='%.3f')
```

### Guardar una tabla de enteros
```python
conteos = np.array([[10, 3], [7, 12]])
np.savetxt('conteos.tsv', conteos, delimiter='\t', fmt='%d')
```

### Mezclar formatos por columna
```python
# col 0 entero (id), col 1 científico (medida)
np.savetxt('mix.csv', tabla, delimiter=',', fmt=['%d', '%.4e'])
```

### Guardar comprimido
```python
np.savetxt('grande.csv.gz', X, delimiter=',')   # gzip automático por la extensión
```

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| `Expected 1D or 2D array, got 3D` | `X` tiene 3+ dimensiones | `reshape` a 2D, o usar [[np.save]] |
| `#` delante de la cabecera del CSV | `comments` por defecto (`'# '`) | `comments=''` |
| Archivo enorme / ilegible | `fmt='%.18e'` por defecto (científico, 18 dígitos) | `fmt='%.4f'` u otro punto fijo |
| Pérdida de precisión al releer | `fmt` con pocos decimales | `fmt='%.18e'` o binario [[np.save]] |
| `delimiter` no coincide al releer | guardado con `' '`, leído con `','` | usar el mismo separador en ambos lados |

## Notas relacionadas

- [[np.loadtxt]] — la pareja de lectura (round-trip de texto)
- [[np.genfromtxt]] — lectura robusta cuando el texto trae huecos
- [[np.save]] — binario `.npy`: N-D, exacto y más rápido
- [[concepto_shape]] · [[Librerias/Numpy/np/io/index|índice de io]]
