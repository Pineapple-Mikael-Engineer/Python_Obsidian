---
title: ndarray.cumprod — Producto acumulado a lo largo de un eje (método)
aliases:
  - cumprod
  - ndarray.cumprod
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

# ndarray.cumprod — Producto acumulado a lo largo de un eje (método)

## Firma del método

```python
ndarray.cumprod(axis=None, dtype=None, out=None) -> ndarray
```

## Valor de retorno

Análogo a `cumsum` pero multiplicando: **no reduce**, devuelve un array del **mismo shape** con los productos parciales. Con `axis=None` aplana primero (ver [[concepto_axis_parametro]]).

| Entrada | `axis` | Salida |
|---------|--------|--------|
| `(2, 3)` | `None` | `(6,)` (aplana y acumula) |
| `(2, 3)` | `0` | `(2, 3)` (acumula bajando filas) |
| `(2, 3)` | `1` | `(2, 3)` (acumula a lo largo de columnas) |

```python
import numpy as np
M = np.array([[1, 2, 3],
              [4, 5, 6]])
M.cumprod()          # [  1   2   6  24 120 720]
M.cumprod(axis=1)    # [[1 2 6] [4 20 120]]
```

## Equivalencia con np.cumprod

Versión "bound" de la función: `arr.cumprod(...) == np.cumprod(arr, ...)`. Detalle completo en [[np.cumprod]].

```python
arr.cumprod(axis=0)        # método
np.cumprod(arr, axis=0)    # función → mismo resultado
```

## Parámetros en detalle

| Parámetro | Rol |
|-----------|-----|
| `axis` | dirección de la acumulación; el shape se **conserva**. `None` aplana antes |
| `dtype` | tipo del acumulador: **muy propenso a overflow** por crecimiento exponencial |

```python
arr = np.array([1, 2, 3, 4])
arr.cumprod()   # [ 1  2  6 24]  el último valor == arr.prod()
```

## Casos de uso

```python
factores = np.array([1.0, 1.05, 1.10, 0.95])
factores.cumprod()   # crecimiento compuesto acumulado
```

## Buenas prácticas

1. El **último elemento** de `cumprod` coincide con `prod`: útil para validar.
2. Ideal para **crecimiento compuesto** (interés, retornos encadenados).
3. Usa `dtype=np.float64` salvo que controles bien los rangos enteros.
4. Si hay NaN, usa [[np.nancumprod]] para tratarlos como 1.

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| Overflow en la cola del array | crecimiento exponencial | `dtype=np.float64` |
| Toda la cola a 0 | apareció un `0` intermedio | revisar datos de entrada |
| `NaN` propagado | array con NaN | usar [[np.nancumprod]] |

## Notas relacionadas

- [[np.cumprod]]
- [[concepto_axis_parametro]]
- [[ndarray.prod]]
- [[ndarray.cumsum]]
- [[np.nancumprod]]
