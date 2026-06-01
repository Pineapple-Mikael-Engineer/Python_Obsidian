---
title: ndarray.sum — Suma de elementos a lo largo de un eje (método)
aliases:
  - sum
  - ndarray.sum
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

# ndarray.sum — Suma de elementos a lo largo de un eje (método)

## Firma del método

```python
ndarray.sum(axis=None, dtype=None, out=None, keepdims=False, initial=0, where=True) -> ndarray | escalar
```

## Valor de retorno

Suma los elementos del array. El eje indicado se **colapsa**; con `axis=None` suma todo y devuelve un escalar (ver [[concepto_axis_parametro]]).

| Entrada | `axis` | Salida |
|---------|--------|--------|
| `(2, 3)` | `None` | escalar (suma total) |
| `(2, 3)` | `0` | `(3,)` (suma por columna) |
| `(2, 3)` | `1` | `(2,)` (suma por fila) |

```python
import numpy as np
M = np.array([[1, 2, 3],
              [4, 5, 6]])
M.sum()          # 21
M.sum(axis=0)    # [5, 7, 9]
M.sum(axis=1)    # [6, 15]
```

## Equivalencia con np.sum

Versión "bound" de la función: `arr.sum(...) == np.sum(arr, ...)`. Para el detalle completo de parámetros (`initial`, `where`), ver [[np.sum]].

```python
arr.sum(axis=0)        # método
np.sum(arr, axis=0)    # función → mismo resultado
```

## Parámetros en detalle

| Parámetro | Rol |
|-----------|-----|
| `axis` | eje a colapsar (`int`, tupla o `None`) |
| `dtype` | tipo del acumulador: evita **overflow** con enteros pequeños |
| `keepdims` | conserva el eje reducido con tamaño 1 (útil para broadcasting) |

```python
arr = np.ones(1000, dtype=np.int8)
arr.sum()                  # puede desbordar el acumulador
arr.sum(dtype=np.int64)    # acumulador seguro
```

## Casos de uso

```python
ventas = np.array([[100, 200], [150, 250]])
ventas.sum()            # 700  total
ventas.sum(axis=0)      # [250, 450]  por producto

datos = np.array([1, 5, 2, 8, 3])
(datos > 3).sum()       # 2  → True cuenta como 1
```

## Buenas prácticas

1. Con enteros de pocos bits, fija `dtype` para evitar overflow silencioso.
2. Usa `keepdims=True` cuando vayas a dividir/restar el resultado del array original.
3. `(mascara).sum()` es el idioma para **contar** condiciones (True=1).
4. Si hay NaN, usa [[np.nansum]] para ignorarlos en lugar de propagar NaN.

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| Resultado erróneo por overflow | acumulador de pocos bits | `dtype=np.int64` |
| `NaN` en el resultado | el array contiene NaN | usar [[np.nansum]] |
| Broadcasting falla tras sumar | se perdió el eje | `keepdims=True` |
| Sentido de `axis` invertido | confundir filas/columnas | recordar: el eje indicado se colapsa |

## Notas relacionadas

- [[np.sum]]
- [[concepto_axis_parametro]]
- [[ndarray.cumsum]]
- [[ndarray.prod]]
- [[ndarray.mean]]
- [[np.nansum]]
