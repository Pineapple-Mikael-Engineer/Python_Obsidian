---
title: ndarray.prod — Producto de elementos a lo largo de un eje (método)
aliases:
  - prod
  - ndarray.prod
tags:
  - numpy
  - api/metodo
  - reducciones
lib: numpy
obj: ndarray
tipo: metodo
retorna: ndarray o escalar
inplace: false
draft: false
---

# ndarray.prod — Producto de elementos a lo largo de un eje (método)

## Firma del método

```python
ndarray.prod(axis=None, dtype=None, out=None, keepdims=False, initial=1, where=True) -> ndarray | escalar
```

## Valor de retorno

Multiplica los elementos del array. El eje indicado se **colapsa**; con `axis=None` multiplica todo y devuelve un escalar (ver [[concepto_axis_parametro]]).

| Entrada | `axis` | Salida |
|---------|--------|--------|
| `(2, 3)` | `None` | escalar (producto total) |
| `(2, 3)` | `0` | `(3,)` (producto por columna) |
| `(2, 3)` | `1` | `(2,)` (producto por fila) |

```python
import numpy as np
M = np.array([[1, 2, 3],
              [4, 5, 6]])
M.prod()          # 720
M.prod(axis=0)    # [ 4 10 18]
M.prod(axis=1)    # [  6 120]
```

## Equivalencia con np.prod

Versión "bound" de la función: `arr.prod(...) == np.prod(arr, ...)`. Detalle completo de `initial` y `where` en [[np.prod]].

```python
arr.prod(axis=0)        # método
np.prod(arr, axis=0)    # función → mismo resultado
```

## Parámetros en detalle

| Parámetro | Rol |
|-----------|-----|
| `axis` | eje a colapsar (`int`, tupla o `None`) |
| `dtype` | tipo del acumulador: el producto crece rápido, **propenso a overflow** |
| `keepdims` | conserva el eje reducido con tamaño 1 |

```python
arr = np.arange(1, 21)          # factorial de 20
arr.prod()                      # desborda int64 (resultado erróneo)
arr.prod(dtype=np.float64)      # acumulador de mayor rango
```

## Casos de uso

```python
shape = np.array([3, 4, 5])
shape.prod()        # 60  → número total de elementos
```

## Buenas prácticas

1. El producto **crece exponencialmente**: vigila el overflow más que con `sum`.
2. Usa `dtype=np.float64` para rangos grandes (factoriales, probabilidades).
3. Un solo `0` en el array anula todo el producto: conviene verificar antes.
4. Si hay NaN, usa [[np.nanprod]] para ignorarlos.

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| Resultado negativo/erróneo | overflow del acumulador entero | `dtype=np.float64` |
| Producto siempre 0 | hay un `0` en el array | filtrar ceros si procede |
| `NaN` en el resultado | el array contiene NaN | usar [[np.nanprod]] |

## Notas relacionadas

- [[np.prod]]
- [[concepto_axis_parametro]]
- [[ndarray.sum]]
- [[ndarray.cumprod]]
- [[np.nanprod]]
