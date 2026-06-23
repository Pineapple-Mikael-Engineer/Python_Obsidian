---
title: ndarray.byteswap — invierte el orden de bytes (endianness) de cada elemento
aliases:
  - byteswap
  - ndarray.byteswap
tags:
  - numpy
  - api/metodo
  - dtype
lib: numpy
mod: np.ndarray
obj: ndarray
tipo: metodo
retorna: ndarray
inplace: false
requiere:
  - concepto_dtype
draft: false
---

# ndarray.byteswap — invierte el orden de bytes (endianness) de cada elemento

`byteswap` **invierte el orden de los bytes** dentro de cada elemento del array (little-endian ↔ big-endian). No cambia la etiqueta de byte order del [[concepto_dtype|dtype]], solo los bytes del buffer, así que el **valor numérico cambia**. Su uso real es leer datos binarios producidos en una arquitectura con endianness distinta. Por defecto devuelve una copia; con `inplace=True` muta `self`.

## La idea

Cada elemento de un dtype multibyte (un `int16` ocupa 2 bytes, un `float64` ocupa 8) tiene un **orden de bytes** definido por la arquitectura. `byteswap` **voltea ese orden** byte a byte, dentro de cada elemento, sin tocar shape ni dtype.

$$ \text{elemento de } k \text{ bytes: } [\,b_0,\,b_1,\dots,b_{k-1}\,] \ \xrightarrow{\ \texttt{byteswap}\ }\ [\,b_{k-1},\dots,b_1,\,b_0\,] $$

Para un `uint16`, el valor `1` (bytes `0x00 0x01` en big-endian) pasa a leerse como `256` (`0x01 0x00`). El [[concepto_dtype|dtype]] guarda el byte order en su prefijo: `<` little-endian, `>` big-endian, `=` nativo. `byteswap` mueve los bytes pero **deja ese prefijo igual**, por lo que el número reportado cambia.

## Firma

```python
ndarray.byteswap(inplace=False) -> ndarray
```

## Los parámetros en detalle

### `inplace` — modificar el propio array o devolver una copia

| `inplace` | Comportamiento | Retorno |
|-----------|----------------|---------|
| `False` (defecto) | crea una copia con los bytes invertidos | array nuevo |
| `True` | invierte los bytes de `self` | el propio `self` (ya mutado) |

```python
a = np.array([1, 256], dtype=np.int16)
a.byteswap(inplace=True)   # muta 'a'
a                          # array([256,   1], dtype=int16)
```

Con `inplace=True` se evita duplicar el buffer — clave al normalizar archivos grandes leídos de disco.

## ¿Vista o copia?

Depende de `inplace`. Con el defecto `inplace=False` devuelve una **copia** (buffer propio, el original intacto). Con `inplace=True` opera **in-place** sobre `self` y lo retorna (no es una vista nueva: es el mismo objeto mutado).

```python
import numpy as np
a = np.array([1, 256, 8755], dtype=np.uint16)
b = a.byteswap()           # copia con bytes volteados
np.shares_memory(a, b)     # False  → a queda intacto
b                          # array([  256,     1, 13090], dtype=uint16)
```

## byteswap frente a cambiar la etiqueta de endianness

Hay dos operaciones independientes y a menudo se necesitan **ambas**:

- **`byteswap`** → mueve los bytes, **deja** la etiqueta del dtype. El valor cambia.
- **cambiar la etiqueta** (con `arr.view(dtype_con_otro_endian)`) → **deja** los bytes, cambia la etiqueta. El valor cambia.
- Aplicar **las dos** → bytes y etiqueta cambian de forma coherente: misma representación lógica, layout nativo. Es lo correcto para "interpretar datos de otra máquina".

```python
a = np.array([1, 256], dtype='>i2')   # int16 big-endian
nativo = a.byteswap().view('<i2')     # bytes volteados + etiqueta little-endian
```

> [!note] No-op en dtypes de 1 byte
> `int8`, `uint8` y `bool` ocupan un solo byte: no tienen orden de bytes y `byteswap` no hace nada útil sobre ellos.

## Valor de retorno

Un `ndarray` con el **mismo shape y dtype** (incluida la etiqueta de endianness) pero con los bytes de cada elemento invertidos. Es copia con `inplace=False`, o el propio `self` con `inplace=True`.

| Entrada (`uint16`) | Llamada | Salida |
|--------------------|---------|--------|
| `[1, 256, 8755]` | `arr.byteswap()` | `[256, 1, 13090]` (copia) |
| `[1]` | `arr.byteswap(inplace=True)` | `self` → `[256]` |
| `[5]` int8 | `arr.byteswap()` | `[5]` (no-op, 1 byte) |

## Casos de uso

### Leer un buffer binario con endianness distinto

```python
# bytes escritos en big-endian, máquina little-endian
raw = np.frombuffer(b'\x00\x01\x00\x02', dtype=np.uint16)   # lee [256, 512]
raw.byteswap()    # array([1, 2], dtype=uint16)  → corrige el orden
```

### Normalizar un archivo a endianness nativo sin copia extra

```python
datos = np.fromfile('sensor.bin', dtype='>f4')   # float32 big-endian
datos.byteswap(inplace=True)   # ahora en orden de la CPU, mismo buffer
```

### Ejemplo realista: cargar un volumen científico portado entre arquitecturas

```python
vol = np.fromfile('scan.raw', dtype='>i2').reshape(256, 256, 64)
vol = vol.byteswap().view('<i2')   # bytes + etiqueta → int16 nativo coherente
vol.max()                          # ahora los valores son correctos
```

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| El valor sigue "mal" tras `byteswap` | falta ajustar la etiqueta de endianness | combinar con `view('<...')` / `view('>...')` |
| Esperar un valor de retorno con `inplace=True` | retorna `self`, ya mutado | usar el propio array tras la llamada |
| `byteswap` no cambia nada | dtype de 1 byte (`int8`/`uint8`/`bool`) | esos tipos no tienen endianness; omitir |
| Doble swap sin querer | aplicar `byteswap` dos veces | recordar que dos swaps vuelven al original |

## Notas relacionadas

- [[concepto_dtype]] — el byte order (`<` / `>` / `=`) como parte del dtype
- [[ndarray.view]] — cambiar la etiqueta de endianness sin mover bytes
- [[concepto_views_vs_copias]] — qué devuelve según `inplace`
