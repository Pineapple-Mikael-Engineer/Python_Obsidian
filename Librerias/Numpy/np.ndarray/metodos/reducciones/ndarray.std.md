---
title: ndarray.std — Desviación estándar a lo largo de un eje (método)
aliases:
  - std
  - ndarray.std
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

# ndarray.std — Desviación estándar a lo largo de un eje (método)

## Firma del método

```python
ndarray.std(axis=None, dtype=None, out=None, ddof=0, keepdims=False, where=True) -> ndarray | escalar
```

## Valor de retorno

Calcula la desviación estándar (raíz cuadrada de la varianza). El eje indicado se **colapsa**; con `axis=None` usa todo el array. Resultado **siempre float** (ver [[concepto_axis_parametro]]).

| Entrada | `axis` | Salida |
|---------|--------|--------|
| `(2, 3)` | `None` | escalar (desviación total) |
| `(2, 3)` | `0` | `(3,)` (desviación por columna) |
| `(2, 3)` | `1` | `(2,)` (desviación por fila) |

```python
import numpy as np
M = np.array([[1, 2, 3],
              [4, 5, 6]])
M.std()          # 1.7078...
M.std(axis=0)    # [1.5 1.5 1.5]
M.std(axis=1)    # [0.8165 0.8165]
```

## Equivalencia con np.std

Versión "bound" de la función: `arr.std(...) == np.std(arr, ...)`. Detalle completo en [[np.std]].

```python
arr.std(axis=0)        # método
np.std(arr, axis=0)    # función → mismo resultado
```

## Parámetros en detalle

| Parámetro | Rol |
|-----------|-----|
| `axis` | eje a colapsar (`int`, tupla o `None`) |
| `ddof` | grados de libertad: divisor de la varianza interna es `N - ddof` |
| `keepdims` | conserva el eje reducido con tamaño 1 (clave para estandarizar) |

`ddof` selecciona desviación **poblacional** o **muestral**:

```python
x = np.array([2, 4, 6, 8])
x.std()          # ddof=0 → poblacional (divide entre N)
x.std(ddof=1)    # muestral (divide entre N-1)
```

## Casos de uso

```python
# Estandarización (z-score) por columna
X = np.array([[1.0, 10.0], [2.0, 20.0], [3.0, 30.0]])
(X - X.mean(axis=0, keepdims=True)) / X.std(axis=0, keepdims=True)
```

## Buenas prácticas

1. Para estandarizar, combina con `mean` y `keepdims=True` para alinear ejes.
2. Para **estadística muestral** usa `ddof=1`; NumPy usa `ddof=0` por defecto.
3. `std` está en las **mismas unidades** que los datos (a diferencia de `var`).
4. Si hay NaN, usa [[np.nanstd]] para ignorarlos.

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| Discrepancia con pandas/otros | `ddof` por defecto distinto | igualar `ddof` |
| Resultado `NaN` | el array contiene NaN | usar [[np.nanstd]] |
| División por cero al estandarizar | columna constante (`std=0`) | añadir `eps` o tratar el caso |

## Notas relacionadas

- [[np.std]]
- [[concepto_axis_parametro]]
- [[ndarray.var]]
- [[ndarray.mean]]
- [[np.nanstd]]
