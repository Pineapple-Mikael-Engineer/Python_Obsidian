---
title: np.take — Seleccionar elementos por índices a lo largo de un eje
aliases:
  - take
  - np.take
tags:
  - numpy
  - api/funcion
  - indexado

# --- Clasificación ---
lib: numpy
mod: np
tipo: funcion

# --- Comportamiento ---
retorna: ndarray
inplace: false

# --- Dependencias ---
requiere:
  - concepto_indexing
  - concepto_axis_parametro

draft: false
---

# np.take — Seleccionar elementos por índices a lo largo de un eje

## Firma de la función

```python
np.take(
    a,
    indices,
    axis=None,
    out=None,
    mode='raise'
) -> ndarray
```

## Valor de retorno

Devuelve los elementos de `a` en las posiciones `indices`, a lo largo del [[concepto_axis_parametro|eje]] indicado. Es la versión funcional del [[concepto_indexing|fancy indexing]] `a[indices]`, con control de `axis` y `mode`.

| Entrada | `indices` | `axis` | Salida |
|---------|-----------|--------|--------|
| `[10,20,30,40]` | `[0, 2]` | `None` | `[10, 30]` |
| `(3, 4)` | `[0, 2]` | `1` | columnas 0 y 2 |

```python
import numpy as np
a = np.array([10, 20, 30, 40])
np.take(a, [0, 2, 3])   # array([10, 30, 40])
```

## Parámetros en detalle

### `a` — array de entrada

Array fuente.

### `indices` — posiciones a tomar

Entero o array de enteros. Su shape determina el shape de la salida.

### `axis` — eje de selección

`None` opera sobre `a` aplanado. Con entero, selecciona a lo largo de ese eje:

```python
M = np.arange(12).reshape(3, 4)
np.take(M, [0, 2], axis=1)   # columnas 0 y 2 → (3, 2)
```

### `mode` — qué hacer con índices fuera de rango

| `mode` | Comportamiento |
|--------|----------------|
| `'raise'` (por defecto) | lanza error |
| `'wrap'` | da la vuelta (módulo) |
| `'clip'` | recorta al borde |

## Casos de uso

### Reordenar / muestrear filas

```python
datos = np.random.rand(100, 5)
muestra = np.take(datos, [3, 7, 50], axis=0)
```

### Lookup table (tabla de búsqueda)

```python
tabla = np.array([0.0, 0.5, 1.0])
np.take(tabla, [2, 0, 1, 2])   # [1.0, 0.0, 0.5, 1.0]
```

## Buenas prácticas

1. Para indexado simple, `a[indices]` es más idiomático; usa `take` cuando necesites `axis` o `mode` explícitos.
2. `mode='clip'`/`'wrap'` evita errores con índices que puedan salirse de rango.
3. Para escribir por índices (lo inverso), usa [[np.put]].

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| `IndexError` | índice fuera de rango con `mode='raise'` | usar `mode='clip'`/`'wrap'` o validar |
| Resultado aplanado | `axis=None` por defecto | pasar `axis` |

## Limitaciones

- No modifica `a`; para asignación in-place está [[np.put]].

## Notas relacionadas

- [[concepto_indexing]]
- [[concepto_axis_parametro]]
- [[np.put]]
- [[np.where]]
