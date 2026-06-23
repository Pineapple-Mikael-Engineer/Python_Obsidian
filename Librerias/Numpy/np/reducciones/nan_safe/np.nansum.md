---
title: np.nansum — suma ignorando NaN (NaN tratado como 0)
aliases:
  - nansum
  - np.nansum
  - suma ignorando NaN
tags:
  - numpy
  - api/funcion
  - reducciones

# --- Clasificación ---
lib: numpy
mod: np
tipo: funcion

# --- Comportamiento ---
retorna: ndarray | escalar
inplace: false

# --- Dependencias ---
requiere:
  - concepto_axis_parametro
  - concepto_dtype

draft: false
---

# np.nansum — suma ignorando NaN (NaN tratado como 0)

`np.nansum` es la versión **NaN-safe** de [[np.sum]]: hace exactamente la misma reducción —colapsa un
eje sumando sus elementos— pero **tratando cada `NaN` como el neutro de la suma, `0`**. Donde `np.sum`
**propaga** el NaN (un solo NaN en el eje convierte todo el total en `NaN`), `np.nansum` lo **omite** y
suma el resto. Toda la mecánica de `axis`, `keepdims`, `dtype` y el caso N-D es la de la gemela; aquí
solo cambia el tratamiento del NaN.

## La idea en una fórmula

Mismo **mapa de shapes** que [[np.sum]] (es un *reduce*: el eje reducido **desaparece**):

$$ (n_0,\dots,n_k)\ \xrightarrow{\ \text{nansum, axis}=p\ }\ (n_0,\dots,n_{p-1},\,n_{p+1},\dots,n_k) $$

La única diferencia con la fórmula por índices de la gemela es que el NaN se omite del sumatorio
(equivale a sustituirlo por `0`):

$$ s_j = \sum_{\substack{i \\ a_{ij}\,\neq\,\text{NaN}}} a_{ij} $$

## Parámetros

Los mismos que [[np.sum]] —`a`, `axis`, `dtype`, `out`, `keepdims`— con idéntica semántica; consúltalos
allí. `np.nansum` **no** tiene `initial` ni `where` (no los necesita: el filtrado de NaN ya es su razón
de ser). Vigila `dtype` igual que en la gemela, con el añadido de que `nansum` **solo opera sobre
floats** (el NaN solo existe en punto flotante).

## NaN: el comportamiento clave

Cada NaN se cuenta como `0` en la suma corriente. Por eso un eje con datos válidos da el total de **lo
que sí hay**:

```python
import numpy as np
np.nansum([1, 2, np.nan, 4])   # 7.0   ← suma 1+2+4, ignora el NaN
np.sum([1, 2, np.nan, 4])      # nan   ← la gemela propaga
```

> [!warning] La trampa del slice todo-NaN
> Si **todos** los elementos del eje son NaN, no quedan datos que sumar y el resultado es **`0.0`**, no
> `NaN`. Ese `0` es indistinguible de "sumé ceros reales", así que **puede ocultar la ausencia total de
> datos**. Si necesitas distinguir "suma 0" de "no había nada", cuenta los no-NaN aparte
> (`np.sum(~np.isnan(a), axis=...)`).
>
> ```python
> np.nansum([np.nan, np.nan])   # 0.0   ← no es NaN: el slice estaba vacío de datos
> ```

## Ejemplos

```python
# 2-D con NaN: reducción por columnas ignorando huecos
ventas = np.array([[100.,  np.nan],
                   [200., 300.]])
np.nansum(ventas, axis=0)   # [300., 300.]  → cada columna suma lo que tiene
np.nansum(ventas, axis=1)   # [100., 500.]
```

```python
# N-D: igual que np.sum, el eje de axis desaparece; los NaN no contaminan
T = np.array([[[1.,  2., np.nan],
               [4.,  5.,  6.]],
              [[np.nan, np.nan, np.nan],
               [1.,  1.,  1.]]])          # shape (2, 2, 3)
np.nansum(T, axis=2)        # (2, 2) → [[3., 15.], [0., 3.]]
#                                        └ el slice todo-NaN dio 0., no NaN
```

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| `0` oculta "sin datos" | eje completamente NaN → suma `0`, no NaN | contar no-NaN aparte (`(~np.isnan(a)).sum()`) |
| Resultado sigue siendo NaN | la entrada es entera o el NaN no es float NaN | asegurar `dtype` float real |
| Esperar que ignore enteros sentinela | solo ignora `np.nan`, no `0`/`-1`/etc. | enmascarar con `where`/máscara propia |

## Notas relacionadas

- [[np.sum]] — la gemela que propaga NaN; toda la mecánica de `axis`/`keepdims`/`dtype`
- [[concepto_dtype]] — `nansum` solo opera sobre floats
- [[np.nanprod]] · [[np.nanmean]] · [[np.nancumsum]]
