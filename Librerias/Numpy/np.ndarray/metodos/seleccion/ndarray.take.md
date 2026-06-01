---
title: ndarray.take — Seleccionar elementos del array por índices a lo largo de un eje
aliases:
  - take
  - ndarray.take
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

# ndarray.take — Seleccionar elementos del array por índices a lo largo de un eje

## Firma del método

```python
ndarray.take(
    indices,
    axis=None,
    out=None,
    mode='raise'
) -> ndarray
```

## Valor de retorno

| Entrada (`self`) | `indices` | `axis` | Retorno |
|------------------|-----------|--------|---------|
| `[10,20,30,40]` | `[0, 2]` | `None` | `array([10, 30])` |
| shape `(3, 4)` | `[0, 2]` | `1` | columnas 0 y 2 → `(3, 2)` |
| `[10,20,30]` | `2` (escalar) | `None` | `30` (escalar) |

Devuelve una **copia** con los elementos tomados; nunca modifica `self`.

```python
import numpy as np
a = np.array([10, 20, 30, 40])
a.take([0, 2, 3])   # array([10, 30, 40])
```

## Equivalencia con np.take

`a.take(indices, ...)` es la forma "bound" de [[np.take]]: `np.take(a, indices, ...)`. Misma semántica de `axis` y `mode`, idéntico resultado. La forma de método encadena de forma fluida (`a.reshape(3,4).take([0,2], axis=1)`); la funcional acepta como primer argumento cualquier `array_like` (listas), no solo un `ndarray` ya construido.

## Parámetros en detalle

### `indices` — posiciones a tomar

Entero o array de enteros. El shape de `indices` determina el shape de la salida.

### `axis` — eje de selección

`None` (por defecto) opera sobre `self` aplanado. Con entero, selecciona a lo largo de ese eje:

```python
M = np.arange(12).reshape(3, 4)
M.take([0, 2], axis=1)   # columnas 0 y 2 → shape (3, 2)
```

### `mode` — índices fuera de rango

| `mode` | Comportamiento |
|--------|----------------|
| `'raise'` (defecto) | lanza `IndexError` |
| `'wrap'` | da la vuelta (módulo) |
| `'clip'` | recorta al borde |

## Casos de uso

### Muestrear filas encadenando

```python
datos = np.random.rand(100, 5)
datos.take([3, 7, 50], axis=0)   # 3 filas seleccionadas
```

### Lookup table

```python
tabla = np.array([0.0, 0.5, 1.0])
tabla.take([2, 0, 1, 2])   # array([1. , 0. , 0.5, 1. ])
```

## Buenas prácticas

1. Para indexado simple, `self[indices]` es más idiomático; usa `.take` cuando necesites `axis` o `mode` explícitos o encadenar.
2. `mode='clip'`/`'wrap'` evita `IndexError` con índices que puedan salirse de rango.
3. Para escribir por índices (lo inverso e in-place), usa `self.put(...)`.

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| `IndexError` | índice fuera de rango con `mode='raise'` | `mode='clip'`/`'wrap'` o validar |
| Resultado aplanado inesperado | `axis=None` por defecto | pasar `axis` |
| Esperar modificación de `self` | `.take` retorna copia | usar `.put` para in-place |

## Notas relacionadas

- [[np.take]]
- [[concepto_indexing]]
- [[ndarray.put]]
- [[concepto_axis_parametro]]
