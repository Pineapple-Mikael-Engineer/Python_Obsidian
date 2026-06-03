---
title: ndarray.cumsum — Suma acumulada a lo largo de un eje (método)
aliases:
  - cumsum
  - ndarray.cumsum
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

# ndarray.cumsum — Suma acumulada a lo largo de un eje (método)

## Firma del método

```python
ndarray.cumsum(axis=None, dtype=None, out=None) -> ndarray
```

## Valor de retorno

A diferencia de `sum`, **no reduce**: devuelve un array del **mismo shape** con las sumas parciales acumuladas. Con `axis=None` aplana primero y acumula sobre el array 1D (ver [[concepto_axis_parametro]]).

| Entrada | `axis` | Salida |
|---------|--------|--------|
| `(2, 3)` | `None` | `(6,)` (aplana y acumula) |
| `(2, 3)` | `0` | `(2, 3)` (acumula bajando filas) |
| `(2, 3)` | `1` | `(2, 3)` (acumula a lo largo de columnas) |

```python
import numpy as np
M = np.array([[1, 2, 3],
              [4, 5, 6]])
M.cumsum()          # [ 1  3  6 10 15 21]
M.cumsum(axis=0)    # [[1 2 3] [5 7 9]]
M.cumsum(axis=1)    # [[1 3 6] [4 9 15]]
```

## Equivalencia con np.cumsum

Versión "bound" de la función: `arr.cumsum(...) == np.cumsum(arr, ...)`. Detalle completo en [[np.cumsum]].

```python
arr.cumsum(axis=0)        # método
np.cumsum(arr, axis=0)    # función → mismo resultado
```

## Parámetros en detalle

| Parámetro | Rol |
|-----------|-----|
| `axis` | dirección de la acumulación; el shape se **conserva**. `None` aplana antes |
| `dtype` | tipo del acumulador: evita **overflow** con enteros pequeños |

```python
arr = np.array([1, 2, 3, 4])
arr.cumsum()   # [1 3 6 10]  el último valor == arr.sum()
```

## Casos de uso

```python
ventas_diarias = np.array([100, 150, 80, 200])
ventas_diarias.cumsum()   # [100 250 330 530]  acumulado a la fecha
```

## Buenas prácticas

1. El **último elemento** de `cumsum` coincide con `sum`: útil para validar.
2. Especifica siempre `axis` en 2D+; el `None` por defecto aplana y suele confundir.
3. Con enteros de pocos bits, fija `dtype` para evitar overflow.
4. Si hay NaN, usa [[np.nancumsum]] para tratarlos como 0.

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| Salida 1D inesperada en 2D | `axis=None` aplana | pasar `axis=0/1` |
| Overflow en la acumulación | acumulador de pocos bits | `dtype=np.int64` |
| `NaN` propagado en toda la cola | array con NaN | usar [[np.nancumsum]] |

## Notas relacionadas

- [[np.cumsum]]
- [[concepto_axis_parametro]]
- [[ndarray.sum]]
- [[ndarray.cumprod]]
- [[np.nancumsum]]
