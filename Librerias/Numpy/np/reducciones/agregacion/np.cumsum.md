---
title: np.cumsum — Suma acumulada
aliases:
  - cumsum
  - np.cumsum
  - suma acumulada
tags:
  - numpy
  - api/funcion
  - reducciones

# --- Clasificación ---
lib: numpy
mod: np
tipo: funcion

# --- Comportamiento ---
retorna: ndarray
inplace: false

# --- Dependencias ---
requiere:
  - concepto_axis_parametro

draft: false
---

# np.cumsum — Suma acumulada

## Firma de la función

```python
np.cumsum(
    a,
    axis=None,
    dtype=None,
    out=None
) -> ndarray
```

## Valor de retorno

Devuelve un array del **mismo tamaño** que `a` donde cada posición contiene la suma de todos los elementos anteriores (incluido él). A diferencia de [[np.sum]], **no colapsa** el eje.

| Entrada | `axis` | Salida |
|---------|--------|--------|
| `[1, 2, 3, 4]` | `None` | `[1, 3, 6, 10]` |
| `(2, 3)` | `0` | acumula por columnas |
| `(2, 3)` | `1` | acumula por filas |

```python
import numpy as np
np.cumsum([1, 2, 3, 4])   # array([1, 3, 6, 10])
```

## Parámetros en detalle

### `a` — array de entrada

Array o secuencia.

### `axis` — eje de acumulación

Si es `None`, aplana primero y acumula en 1D. Con entero, acumula a lo largo de ese [[concepto_axis_parametro|eje]] conservando el shape.

```python
M = np.array([[1, 2, 3],
              [4, 5, 6]])
np.cumsum(M, axis=1)   # [[1, 3, 6], [4, 9, 15]]
```

### `dtype` — acumulador

Como en `sum`, fija el tipo para evitar overflow con enteros pequeños.

## Casos de uso

### Saldo acumulado en el tiempo

```python
movimientos = np.array([100, -30, 50, -20])
saldo = np.cumsum(movimientos)   # [100, 70, 120, 100]
```

### Función de distribución acumulada (CDF) empírica

```python
frecuencias = np.array([2, 3, 5, 1])
cdf = np.cumsum(frecuencias) / np.sum(frecuencias)
```

## Buenas prácticas

1. Útil para series temporales, saldos y CDFs.
2. Para el **producto** acumulado, usa [[np.cumprod]]; para diferencias, [[np.diff]] (operación inversa aproximada).
3. Si hay NaN y quieres ignorarlos, usa [[np.nancumsum]].

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| Resultado aplanado | `axis=None` por defecto en 2D | pasar `axis` |
| Overflow en enteros | acumulador pequeño | `dtype` mayor |
| NaN contamina el resto de la serie | NaN se propaga acumulativamente | [[np.nancumsum]] |

## Limitaciones

- Conserva el tamaño (no reduce); para el total usa [[np.sum]].

## Notas relacionadas

- [[concepto_axis_parametro]]
- [[np.sum]]
- [[np.cumprod]]
- [[np.diff]]
- [[np.nancumsum]]
