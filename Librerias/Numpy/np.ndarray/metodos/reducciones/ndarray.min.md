---
title: ndarray.min — Valor mínimo del array a lo largo de un eje
aliases:
  - min
  - ndarray.min
tags:
  - numpy
  - api/metodo
  - reducciones
lib: numpy
obj: ndarray
tipo: metodo
retorna: escalar o ndarray
inplace: false
draft: false
---

# ndarray.min — Valor mínimo del array a lo largo de un eje

## Firma del método

```python
ndarray.min(
    axis=None,
    out=None,
    keepdims=False,
    initial=<no value>,
    where=<no value>
) -> escalar | ndarray
```

## Valor de retorno

| Entrada (`self`) | `axis` | Retorno |
|------------------|--------|---------|
| `[3, 1, 9, 2]` | `None` | `1` (escalar) |
| shape `(2, 3)` | `0` | mínimo por columna → `(3,)` |
| shape `(2, 3)` | `1` | mínimo por fila → `(2,)` |

Con `axis=None` colapsa todo y devuelve un escalar; con un eje, lo consume y devuelve un ndarray.

```python
import numpy as np
a = np.array([3, 1, 9, 2])
a.min()   # 1
```

## Equivalencia con np.min

`a.min(...)` es la forma "bound" de [[np.min]]: `np.min(a, ...)`. Misma semántica de `axis`, `keepdims`, `initial` y `where`, idéntico resultado. La forma de método encadena de forma fluida (`a.reshape(2,3).min(axis=1)`); la funcional acepta como primer argumento cualquier `array_like` (listas), no solo un `ndarray` ya construido.

## Parámetros en detalle

### `axis` — eje de reducción

`None` opera sobre `self` aplanado. Con entero (o tupla), colapsa ese eje y deja los demás. El eje indicado es el que desaparece del shape resultado.

### `keepdims` — conservar dimensiones

Con `True`, el eje reducido se mantiene con tamaño 1, lo que facilita el broadcasting posterior.

```python
M = np.array([[1, 9, 3],
              [7, 2, 8]])
M.min(axis=1)                 # [1, 2]   → shape (2,)
M.min(axis=1, keepdims=True)  # [[1],[2]] → shape (2,1)
```

### `initial` / `where` — reducción condicional

`initial` fija un valor de partida; `where` selecciona qué elementos entran en la comparación.

## Casos de uso

### Valor más bajo de una serie

```python
temperaturas = np.array([12.3, 8.1, 15.0, 7.4])
temperaturas.min()   # 7.4
```

### Mínimo por fila encadenando

```python
np.random.rand(100, 5).reshape(100, 5).min(axis=1)   # 100 mínimos
```

## Buenas prácticas

1. Si necesitas la **posición** del mínimo, usa `self.argmin()`; `.min` da el **valor**.
2. Con NaN presente, el resultado se propaga a NaN; usa [[np.nanmin]].
3. Usa `keepdims=True` cuando vayas a combinar el resultado con el array original por broadcasting.

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| Resultado NaN inesperado | NaN se propaga en la comparación | [[np.nanmin]] |
| Se esperaba la posición | `.min` da el valor | `self.argmin()` |
| `(n,)` no alinea con `self` | el eje se colapsó | `keepdims=True` |

## Notas relacionadas

- [[np.min]]
- [[concepto_axis_parametro]]
- [[ndarray.max]]
- [[ndarray.argmin]]
- [[np.nanmin]]
