---
title: ndarray.mean — Media aritmética a lo largo de un eje (método)
aliases:
  - mean
  - ndarray.mean
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

# ndarray.mean — Media aritmética a lo largo de un eje (método)

## Firma del método

```python
ndarray.mean(axis=None, dtype=None, out=None, keepdims=False, where=True) -> ndarray | escalar
```

## Valor de retorno

Promedia los elementos del array. El eje indicado se **colapsa**; con `axis=None` promedia todo y devuelve un escalar. El resultado es **siempre float**, aunque la entrada sea entera (ver [[concepto_axis_parametro]]).

| Entrada | `axis` | Salida |
|---------|--------|--------|
| `(2, 3)` | `None` | escalar (media total) |
| `(2, 3)` | `0` | `(3,)` (media por columna) |
| `(2, 3)` | `1` | `(2,)` (media por fila) |

```python
import numpy as np
M = np.array([[1, 2, 3],
              [4, 5, 6]])
M.mean()          # 3.5
M.mean(axis=0)    # [2.5 3.5 4.5]
M.mean(axis=1)    # [2. 5.]
```

## Equivalencia con np.mean

Versión "bound" de la función: `arr.mean(...) == np.mean(arr, ...)`. Detalle completo en [[np.mean]].

```python
arr.mean(axis=0)        # método
np.mean(arr, axis=0)    # función → mismo resultado
```

## Parámetros en detalle

| Parámetro | Rol |
|-----------|-----|
| `axis` | eje a colapsar (`int`, tupla o `None`) |
| `dtype` | tipo del acumulador; con `float16` conviene subir a `float64` por precisión |
| `keepdims` | conserva el eje reducido con tamaño 1 (clave para centrar/normalizar) |

```python
M = np.array([[1, 2], [3, 4]])
M - M.mean(axis=1, keepdims=True)   # centra cada fila por su media
```

## Casos de uso

```python
notas = np.array([[7, 8, 9], [5, 6, 4]])
notas.mean(axis=1)   # [8. 5.]  media por alumno
```

## Buenas prácticas

1. Usa `keepdims=True` para **centrar** o normalizar restando la media.
2. Con `float16`/`float32` y muchos elementos, fija `dtype=np.float64` para precisión.
3. Si hay NaN, usa [[np.nanmean]]: la media normal **propaga NaN** y arruina el resultado.
4. Para media ponderada usa `np.average(arr, weights=...)`, no `mean`.

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| Resultado `NaN` | el array contiene NaN | usar [[np.nanmean]] |
| Pérdida de precisión | acumulador `float16/32` | `dtype=np.float64` |
| Broadcasting falla al centrar | se perdió el eje | `keepdims=True` |
| `RuntimeWarning: Mean of empty slice` | eje/sub-slice vacío | filtrar antes de promediar |

## Notas relacionadas

- [[np.mean]]
- [[concepto_axis_parametro]]
- [[ndarray.std]]
- [[ndarray.var]]
- [[np.nanmean]]
