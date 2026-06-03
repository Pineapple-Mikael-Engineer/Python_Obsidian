---
title: ndarray.var — Varianza a lo largo de un eje (método)
aliases:
  - var
  - ndarray.var
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

# ndarray.var — Varianza a lo largo de un eje (método)

## Firma del método

```python
ndarray.var(axis=None, dtype=None, out=None, ddof=0, keepdims=False, where=True) -> ndarray | escalar
```

## Valor de retorno

Calcula la varianza (media de las desviaciones al cuadrado respecto a la media). El eje indicado se **colapsa**; con `axis=None` usa todo el array. Resultado **siempre float** (ver [[concepto_axis_parametro]]).

| Entrada | `axis` | Salida |
|---------|--------|--------|
| `(2, 3)` | `None` | escalar (varianza total) |
| `(2, 3)` | `0` | `(3,)` (varianza por columna) |
| `(2, 3)` | `1` | `(2,)` (varianza por fila) |

```python
import numpy as np
M = np.array([[1, 2, 3],
              [4, 5, 6]])
M.var()          # 2.9166...
M.var(axis=0)    # [2.25 2.25 2.25]
M.var(axis=1)    # [0.666... 0.666...]
```

## Equivalencia con np.var

Versión "bound" de la función: `arr.var(...) == np.var(arr, ...)`. Detalle completo en [[np.var]].

```python
arr.var(axis=0)        # método
np.var(arr, axis=0)    # función → mismo resultado
```

## Parámetros en detalle

| Parámetro | Rol |
|-----------|-----|
| `axis` | eje a colapsar (`int`, tupla o `None`) |
| `ddof` | grados de libertad: divisor es `N - ddof` |
| `keepdims` | conserva el eje reducido con tamaño 1 |

`ddof` (delta degrees of freedom) selecciona varianza **poblacional** o **muestral**:

```python
x = np.array([2, 4, 6, 8])
x.var()          # ddof=0 → poblacional (divide entre N)
x.var(ddof=1)    # muestral (divide entre N-1, estimador insesgado)
```

## Casos de uso

```python
medidas = np.array([[10, 12, 11], [20, 19, 21]])
medidas.var(axis=1, ddof=1)   # dispersión muestral por sensor
```

## Buenas prácticas

1. Para **estadística inferencial** (estimar a partir de muestra) usa `ddof=1`.
2. Por defecto NumPy usa `ddof=0` (poblacional), distinto de pandas (`ddof=1`).
3. `var` es el cuadrado de `std`: `arr.var() == arr.std()**2`.
4. Si hay NaN, usa [[np.nanvar]] para ignorarlos.

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| Discrepancia con pandas | defaults de `ddof` distintos | igualar `ddof` |
| Resultado `NaN` | el array contiene NaN | usar [[np.nanvar]] |
| `var` 0 inesperado con 1 dato y ddof=1 | divisor `N-ddof = 0` | revisar tamaño de muestra |

## Notas relacionadas

- [[np.var]]
- [[concepto_axis_parametro]]
- [[ndarray.std]]
- [[ndarray.mean]]
- [[np.nanvar]]
