---
title: ndarray.byteswap — Invertir el orden de bytes (endianness)
aliases:
  - byteswap
  - ndarray.byteswap
tags:
  - numpy
  - api/metodo
  - memoria
lib: numpy
obj: ndarray
tipo: metodo
retorna: ndarray
inplace: false
draft: false
---

# ndarray.byteswap — Invertir el orden de bytes (endianness)

## Firma del método

```python
ndarray.byteswap(inplace=False) -> ndarray
```

## Valor de retorno

Devuelve un `ndarray` con los **bytes de cada elemento invertidos** (little-endian ↔ big-endian). El dtype reportado no cambia su tamaño, pero los valores cambian si se reinterpretan. Por defecto devuelve una **copia**; con `inplace=True` modifica `self` y lo retorna.

| Entrada (`uint16`) | Llamada | Salida |
|--------------------|---------|--------|
| `[1, 256, 8755]` | `arr.byteswap()` | `[256, 1, 13090]` |
| `[1]` | `arr.byteswap(inplace=True)` | `self` → `[256]` |

```python
import numpy as np
a = np.array([1, 256, 8755], dtype=np.uint16)
a.byteswap()
# array([  256,     1, 13090], dtype=uint16)  → cada par de bytes volteado
```

## Parámetros en detalle

### `inplace` — modificar el propio array

| `inplace` | Comportamiento | Retorno |
|-----------|----------------|---------|
| `False` (defecto) | crea copia con bytes invertidos | array nuevo |
| `True` | invierte los bytes de `self` | el propio `self` |

```python
a = np.array([1, 256], dtype=np.int16)
a.byteswap(inplace=True)   # muta a
a                          # array([256,   1], dtype=int16)
```

## byteswap vs cambiar el dtype endianness

`byteswap` reordena los bytes **dejando igual** la etiqueta de endianness del dtype, por lo que el valor numérico cambia. Para reinterpretar sin tocar bytes (cambiar solo la etiqueta) se usa `view` con un dtype de distinto endianness. La combinación habitual para "leer datos de otra máquina" es: ajustar la etiqueta y luego `byteswap`.

```python
a = np.array([1, 256], dtype='>i2')   # big-endian
a.newbyteorder()        # cambia etiqueta, no bytes
a.byteswap()            # cambia bytes, no etiqueta
```

## Casos de uso

### Leer datos binarios con endianness distinto

```python
# buffer escrito en big-endian, máquina little-endian
raw = np.frombuffer(b'\x00\x01\x00\x02', dtype=np.uint16)
raw.byteswap()   # corrige el orden a [1, 2]
```

### Normalizar a endianness nativo in-place

```python
datos = np.fromfile('sensor.bin', dtype='>f4')
datos.byteswap(inplace=True)   # ahora en orden de la CPU, sin copia extra
```

## Buenas prácticas

1. Distingue **bytes** (los mueve `byteswap`) de la **etiqueta** de endianness del dtype (la cambia `newbyteorder`); para un valor correcto normalmente hay que ajustar ambas.
2. Usa `inplace=True` para evitar duplicar buffers grandes leídos de disco.
3. No lo apliques a dtypes de 1 byte (`int8`, `uint8`, `bool`): no tienen orden de bytes y es un no-op.

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| Valor sigue "mal" tras byteswap | falta ajustar la etiqueta de endianness | combinar con `newbyteorder` o `view` |
| Esperar que devuelva valor con `inplace=True` | retorna `self`, ya mutado | usar el propio array |
| No-op en arrays de 1 byte | esos dtypes no tienen endianness | innecesario, omitir |

## Notas relacionadas

- [[concepto_dtype]]
- [[ndarray.view]]
- [[concepto_views_vs_copias]]
