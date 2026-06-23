---
title: ndarray.tofile — escribe los datos crudos a un archivo (binario o texto)
aliases:
  - tofile
  - ndarray.tofile
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
  - concepto_contiguidad_memoria
draft: false
---

# ndarray.tofile — escribe los datos crudos a un archivo (binario o texto)

`ndarray.tofile` vuelca el contenido del array a un archivo en **binario crudo** (por defecto) o en
**texto** (si pasas `sep`). Es la versión en disco de [[ndarray.tobytes]]: escribe los bytes del buffer
sin cabecera, sin `shape`, sin [[concepto_dtype|dtype]] y sin endianness. Es **rápido y compacto**, pero
**no portable**: para releerlo hay que conocer el dtype y reformar a mano. Para guardar arrays "de verdad"
con sus metadatos, la recomendación es `np.save` / `np.savez` (formato `.npy`).

## La idea

El array → un archivo plano de bytes (o de números en texto). En modo binario, el archivo contiene
exactamente `arr.nbytes` bytes, en el orden de memoria del array (ver
[[concepto_contiguidad_memoria|contigüidad]]); el `shape` se aplana y **se pierde**.

$$ \texttt{arr}\ \xrightarrow{\ \text{tofile, sep=""}\ }\ \underbrace{[\,b_0\,b_1\,\dots\,b_{N-1}\,]}_{N\,=\,\texttt{arr.nbytes}}\ \text{(sin cabecera)} $$

Con `sep` no vacío escribe los números como **texto** separados por ese carácter (formato humano, pero
pierde precisión binaria exacta y ocupa más).

```python
import numpy as np
arr = np.arange(6, dtype=np.int32).reshape(2, 3)
arr.tofile("datos.bin")                       # 24 bytes binarios (6 × 4)
np.fromfile("datos.bin", dtype=np.int32)      # array([0,1,2,3,4,5]) → shape (2,3) PERDIDA
```

## Firma

```python
ndarray.tofile(
    fid,            # str | Path | objeto archivo abierto: destino
    sep="",         # str: "" → binario crudo; cualquier otro → texto con ese separador
    format="%s",    # str: formato C de cada elemento en modo texto
) -> None
```

## Los parámetros en detalle

### `fid` — el destino
Una ruta (`str` / `Path`) o un objeto archivo ya abierto (en modo binario `"wb"` para el modo binario).
Si pasas una ruta, NumPy abre, escribe y cierra el archivo.

```python
arr.tofile("salida.bin")                      # por ruta
with open("salida.bin", "wb") as f:
    arr.tofile(f)                             # por handle abierto
```

### `sep` — binario o texto
El interruptor principal del método:
- `""` (defecto) → **binario crudo**: los bytes del buffer, máximo rendimiento, mínima portabilidad.
- cualquier otro string → **texto**: escribe los números como texto separados por `sep`. Pierde la
  exactitud binaria y ocupa bastante más, pero es legible e independiente del endianness.

```python
arr.tofile("datos.txt", sep=",")              # "0,1,2,3,4,5"  → texto plano
arr.tofile("datos.txt", sep="\n")             # un número por línea
```

### `format` — el formato en modo texto
Solo aplica cuando `sep` no está vacío. Es un especificador de formato C que decide cómo se imprime cada
elemento (decimales, notación, etc.). Ignorado en modo binario.

```python
np.array([1.23456, 2.7]).tofile("f.txt", sep=" ", format="%.2f")   # "1.23 2.70"
```

## Valor de retorno

`None`: el efecto es el **archivo escrito**. No modifica el array (solo lo exporta). El tamaño del archivo
en modo binario es exactamente `arr.nbytes`; en modo texto depende de `format` y `sep`.

## Round-trip

La inversa es `np.fromfile`. Igual que con `tobytes`/`frombuffer`, hay que **conocer el dtype** (y el
`sep` si fue texto) y **reformar el shape** a mano, porque el archivo no los guarda:

```python
arr = np.arange(6, dtype=np.int32).reshape(2, 3)

# Binario:
arr.tofile("datos.bin")
back = np.fromfile("datos.bin", dtype=np.int32).reshape(2, 3)
np.array_equal(arr, back)                     # True

# Texto (mismo sep al leer):
arr.tofile("datos.txt", sep=",")
back = np.fromfile("datos.txt", dtype=np.int32, sep=",").reshape(2, 3)
```

> [!warning] No portable: dtype, shape y endianness viajan por separado
> Un archivo de `tofile` leído con el dtype equivocado da basura; leído en una máquina de endianness
> distinta, también. Para persistencia portable usa `np.save` (`.npy`), que guarda dtype, shape y
> endianness en la cabecera y se relee con un simple `np.load("x.npy")` sin tener que recordar nada.

## Casos de uso

### Volcado binario compacto para interoperar con C/Fortran
Fija el dtype con [[ndarray.astype]] antes de exportar para que el otro lado sepa qué leer:

```python
arr.astype("<f8").tofile("buffer.dat")        # float64 little-endian explícito
back = np.fromfile("buffer.dat", dtype="<f8").reshape(arr.shape)
```

### Exportar a texto legible (CSV simple 1-D)
```python
np.array([1.5, 2.5, 3.5]).tofile("col.csv", sep=",", format="%.3f")
```

### Por qué preferir `np.save` para guardar arrays propios
```python
np.save("arr.npy", arr)                       # guarda dtype + shape en la cabecera
back = np.load("arr.npy")                      # round-trip exacto, sin recordar metadatos
np.array_equal(arr, back)                      # True, shape (2,3) incluido
```

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| Datos basura al leer | `dtype` en `np.fromfile` distinto al de escritura | usar el mismo dtype (mejor explícito, ej. `<f8`) |
| Array sale 1-D | `tofile` no guarda el `shape` | `reshape(...)` tras `np.fromfile` |
| No portable entre máquinas | endianness/dtype dependientes del sistema | fijar dtype con endianness (`<f8`) o usar `np.save` |
| Texto cuando se quería binario (o al revés) | `sep` no coincide entre escritura y lectura | mismo `sep` en ambos lados (`""` para binario) |
| Pérdida de precisión en texto | `format` recorta decimales | ampliar `format` o, mejor, usar binario / `.npy` |

## Notas relacionadas

- [[concepto_dtype]] — el tipo que debes recordar para releer el archivo
- [[concepto_contiguidad_memoria]] — el orden en que se vuelcan los bytes
- [[ndarray.tobytes]] — la misma serialización cruda, pero a un objeto `bytes` en memoria
- [[np.fromfile]] — la operación inversa
- [[np.save]] — alternativa portable con metadatos (formato `.npy`)
- [[index]] — métodos de serialización del ndarray
