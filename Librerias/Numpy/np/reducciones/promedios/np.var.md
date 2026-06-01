---
title: np.var — Varianza
aliases:
  - var
  - np.var
  - varianza
tags:
  - numpy
  - api/funcion
  - estadistica

# --- Clasificación ---
lib: numpy
mod: np
tipo: funcion

# --- Comportamiento ---
retorna: ndarray o escalar
inplace: false

# --- Dependencias ---
requiere:
  - concepto_axis_parametro

draft: false
---

# np.var — Varianza

## Firma de la función

```python
np.var(
    a,
    axis=None,
    dtype=None,
    out=None,
    ddof=0,
    keepdims=False,
    where=True
) -> ndarray | escalar
```

## Valor de retorno

Mide la dispersión como el promedio de las desviaciones al cuadrado respecto a la [[np.mean|media]]. Es el **cuadrado** de la [[np.std|desviación estándar]], por lo que está en unidades al cuadrado.

| Entrada | Salida |
|---------|--------|
| `[2, 4, 6]` | `2.667` (ddof=0) |
| `[5, 5, 5]` | `0.0` |

```python
import numpy as np
np.var([2, 4, 6])           # 2.667
np.std([2, 4, 6]) ** 2      # 2.667  → var == std²
```

## El parámetro `ddof`

Idéntico a [[np.std]]:

| `ddof` | Divisor | Uso |
|--------|---------|-----|
| `0` (por defecto) | `N` | varianza **poblacional** |
| `1` | `N - 1` | varianza **muestral** |

```python
np.var([2.0, 4.0, 6.0], ddof=1)   # 4.0  (muestral)
```

## Parámetros en detalle

### `axis`, `keepdims`, `where`, `dtype`

Igual que en [[np.std]] y [[np.mean]]; `axis` colapsa el [[concepto_axis_parametro|eje]].

## Casos de uso

### Comparar variabilidad entre features

```python
varianzas = np.var(matriz, axis=0)
mas_variable = np.argmax(varianzas)
```

### Detectar columnas constantes (varianza 0)

```python
constantes = np.var(datos, axis=0) == 0
```

## Buenas prácticas

1. Si quieres una medida en las **mismas unidades** que los datos, usa [[np.std]].
2. Elige `ddof=1` para varianza muestral insesgada.
3. Con NaN, usa [[np.nanvar]].

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| Magnitud "rara" | está al cuadrado | usar [[np.std]] para unidades originales |
| Valor distinto al de otra librería | `ddof` por defecto 0 | usar `ddof=1` |
| NaN | hay NaN | [[np.nanvar]] |

## Limitaciones

- Unidades al cuadrado (menos interpretable que la desviación).
- Propaga NaN; sensible a outliers.

## Notas relacionadas

- [[concepto_axis_parametro]]
- [[np.std]]
- [[np.mean]]
- [[np.nanvar]]
