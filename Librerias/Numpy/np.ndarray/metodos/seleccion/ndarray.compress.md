---
title: ndarray.compress — Seleccionar elementos donde una máscara booleana es True
aliases:
  - compress
  - ndarray.compress
tags:
  - numpy
  - api/metodo
  - indexado
lib: numpy
obj: ndarray
tipo: metodo
retorna: ndarray
inplace: false
draft: false
---

# ndarray.compress — Seleccionar elementos donde una máscara booleana es True

## Firma del método

```python
ndarray.compress(
    condition,
    axis=None,
    out=None
) -> ndarray
```

## Valor de retorno

| Entrada (`self`) | `condition` | `axis` | Retorno |
|------------------|-------------|--------|---------|
| `[10,20,30,40]` | `[True,False,True,False]` | `None` | `array([10, 30])` |
| shape `(3, 4)` | `[True,False,True]` | `0` | filas 0 y 2 → `(2, 4)` |
| shape `(3, 4)` | `[False,True,True,False]` | `1` | columnas 1 y 2 → `(3, 2)` |

Devuelve una **copia** con los elementos cuya condición es `True`. La máscara puede ser **más corta** que el eje: los índices no cubiertos se descartan (se tratan como `False`).

```python
import numpy as np
a = np.array([10, 20, 30, 40])
a.compress([True, False, True])   # array([10, 30])  ← el 4º se ignora
```

## Equivalencia con np.compress

`a.compress(condition, ...)` es la forma "bound" de [[np.compress]]: `np.compress(condition, a, ...)`. Nota el **orden invertido** de argumentos en la versión funcional. Frente a la indexación booleana clásica del [[concepto_indexing|fancy/boolean indexing]] (`a[mask]`), `compress` añade el parámetro `axis` para filtrar filas o columnas enteras, y tolera máscaras más cortas que el eje.

## Parámetros en detalle

### `condition` — máscara 1-D de bool

Array (o array_like) de booleanos. Su longitud se compara contra el eje indicado; si es menor, los elementos sobrantes del eje quedan fuera.

### `axis` — eje sobre el que filtrar

`None` (defecto) trabaja sobre `self` aplanado. Con entero, selecciona slices completos a lo largo de ese eje:

```python
M = np.arange(12).reshape(3, 4)
M.compress([True, False, True], axis=0)   # filas 0 y 2 → (2, 4)
```

### `out` — array destino opcional

Buffer preasignado donde escribir el resultado.

## Casos de uso

### Filtrar filas por una condición derivada

```python
datos = np.random.rand(5, 3)
mask = datos[:, 0] > 0.5
datos.compress(mask, axis=0)   # solo filas con primera col > 0.5
```

### Submuestreo de columnas

```python
M = np.arange(12).reshape(3, 4)
M.compress([True, False, False, True], axis=1)   # columnas 0 y 3
```

## Buenas prácticas

1. Para 1D, `self[mask]` es más idiomático; usa `.compress` cuando filtres a lo largo de un `axis`.
2. Asegúrate de que `condition` sea booleana 1-D y de longitud coherente con el eje.
3. `compress` siempre devuelve copia; no modifica `self`.

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| Menos elementos de los esperados | máscara más corta que el eje (resto = `False`) | igualar longitud de `condition` al eje |
| `ValueError` de dimensiones | `condition` no es 1-D | aplanar la máscara a 1-D |
| Esperar filtrado 2-D simultáneo | `compress` filtra un solo eje | combinar dos llamadas o usar `self[mask_filas][:, mask_cols]` |

## Notas relacionadas

- [[np.compress]]
- [[concepto_indexing]]
- [[ndarray.take]]
- [[concepto_axis_parametro]]
