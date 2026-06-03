---
title: ndarray.max — Valor máximo del array a lo largo de un eje
aliases:
  - max
  - ndarray.max
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

# ndarray.max — Valor máximo del array a lo largo de un eje

## Firma del método

```python
ndarray.max(
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
| `[3, 1, 9, 2]` | `None` | `9` (escalar) |
| shape `(2, 3)` | `0` | máximo por columna → `(3,)` |
| shape `(2, 3)` | `1` | máximo por fila → `(2,)` |

Con `axis=None` colapsa todo y devuelve un escalar; con un eje, lo consume y devuelve un ndarray.

```python
import numpy as np
a = np.array([3, 1, 9, 2])
a.max()   # 9
```

## Equivalencia con np.max

`a.max(...)` es la forma "bound" de [[np.max]]: `np.max(a, ...)`. Misma semántica de `axis`, `keepdims`, `initial` y `where`, idéntico resultado. La forma de método encadena de forma fluida (`a.reshape(2,3).max(axis=1)`); la funcional acepta como primer argumento cualquier `array_like` (listas), no solo un `ndarray` ya construido.

## Parámetros en detalle

### `axis` — eje de reducción

`None` opera sobre `self` aplanado. Con entero (o tupla), colapsa ese eje y deja los demás. El eje indicado es el que desaparece del shape resultado.

### `keepdims` — conservar dimensiones

Con `True`, el eje reducido se mantiene con tamaño 1, lo que facilita el broadcasting posterior.

```python
M = np.array([[1, 9, 3],
              [7, 2, 8]])
M.max(axis=1)                 # [9, 8]   → shape (2,)
M.max(axis=1, keepdims=True)  # [[9],[8]] → shape (2,1)
```

### `initial` / `where` — reducción condicional

`initial` fija un valor de partida; `where` selecciona qué elementos entran en la comparación.

## Casos de uso

### Valor más alto de una serie

```python
temperaturas = np.array([12.3, 8.1, 15.0, 7.4])
temperaturas.max()   # 15.0
```

### Normalizar dividiendo por el máximo

```python
v = np.array([2.0, 4.0, 8.0])
v / v.max()   # [0.25, 0.5, 1. ]
```

## Buenas prácticas

1. Si necesitas la **posición** del máximo, usa `self.argmax()`; `.max` da el **valor**.
2. Con NaN presente, el resultado se propaga a NaN; usa [[np.nanmax]].
3. Usa `keepdims=True` cuando vayas a combinar el resultado con el array original por broadcasting.

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| Resultado NaN inesperado | NaN se propaga en la comparación | [[np.nanmax]] |
| Se esperaba la posición | `.max` da el valor | `self.argmax()` |
| `(n,)` no alinea con `self` | el eje se colapsó | `keepdims=True` |

## Notas relacionadas

- [[np.max]]
- [[concepto_axis_parametro]]
- [[ndarray.min]]
- [[ndarray.argmax]]
- [[np.nanmax]]
