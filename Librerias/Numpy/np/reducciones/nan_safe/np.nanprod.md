---
title: np.nanprod — producto ignorando NaN (NaN tratado como 1)
aliases:
  - nanprod
  - np.nanprod
  - producto ignorando NaN
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

# np.nanprod — producto ignorando NaN (NaN tratado como 1)

`np.nanprod` es la versión **NaN-safe** de [[np.prod]]: misma reducción multiplicativa —colapsa un eje
multiplicando sus elementos— pero **tratando cada `NaN` como el neutro del producto, `1`**. Donde
`np.prod` **propaga** el NaN (un solo NaN deja todo el producto en `NaN`), `np.nanprod` lo **omite** y
multiplica el resto. Hereda de la gemela toda la mecánica de `axis`/`keepdims`/`dtype` y N-D, **incluida
la trampa aguda del overflow** (los productos crecen exponencialmente).

## La idea en una fórmula

Mismo **mapa de shapes** que [[np.prod]] (es un *reduce*: el eje reducido **desaparece**):

$$ (n_0,\dots,n_k)\ \xrightarrow{\ \text{nanprod, axis}=p\ }\ (n_0,\dots,n_{p-1},\,n_{p+1},\dots,n_k) $$

La fórmula por índices es la de la gemela omitiendo los NaN (equivale a sustituirlos por `1`):

$$ p_j = \prod_{\substack{i \\ a_{ij}\,\neq\,\text{NaN}}} a_{ij} $$

## Parámetros

Los mismos que [[np.prod]] —`a`, `axis`, `dtype`, `out`, `keepdims`— con idéntica semántica; consúltalos
allí. `np.nanprod` **no** tiene `initial` ni `where`. Lo propio: solo opera sobre **floats** (el NaN solo
existe en punto flotante) y conserva la **trampa del overflow** de [[concepto_dtype]] —fija `dtype` amplio
en cuanto multipliques varios factores.

## NaN: el comportamiento clave

Cada NaN se cuenta como `1`, así que no altera el producto de los datos válidos:

```python
import numpy as np
np.nanprod([1, 2, np.nan, 4])   # 8.0   ← multiplica 1·2·4, ignora el NaN
np.prod([1, 2, np.nan, 4])      # nan   ← la gemela propaga
```

> [!warning] La trampa del slice todo-NaN
> Si **todos** los elementos del eje son NaN, no queda nada que multiplicar y el resultado es **`1.0`**,
> no `NaN`. Ese `1` (producto vacío = neutro multiplicativo) es indistinguible de "multiplicé unos
> reales", de modo que **puede ocultar la ausencia total de datos**. Para distinguirlo, cuenta los
> no-NaN aparte (`np.sum(~np.isnan(a), axis=...)`).
>
> ```python
> np.nanprod([np.nan, np.nan])   # 1.0   ← no es NaN: el slice estaba vacío de datos
> ```

## Ejemplos

```python
# Factores con un hueco: el NaN no estropea el producto
factores = np.array([1.05, np.nan, 1.03])
np.nanprod(factores)   # 1.0815   → 1.05 · 1.03, ignora el NaN
```

```python
# N-D: el eje de axis desaparece; un slice todo-NaN cae a 1.
T = np.array([[[1., 2., np.nan],
               [4., 5.,  6.]],
              [[np.nan, np.nan, np.nan],
               [2., 2., 2.]]])          # shape (2, 2, 3)
np.nanprod(T, axis=2)   # (2, 2) → [[2., 120.], [1., 8.]]
#                                            └ slice todo-NaN → 1., no NaN
```

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| `1` oculta "sin datos" | eje todo-NaN → producto `1`, no NaN | contar no-NaN aparte (`(~np.isnan(a)).sum()`) |
| Resultado negativo/absurdo | overflow del acumulador (crece exponencial) | `dtype=np.float64` (o `int64` si cabe) |
| Resultado sigue siendo NaN | la entrada no es float real | asegurar `dtype` float |

## Notas relacionadas

- [[np.prod]] — la gemela que propaga NaN; mecánica de `axis`/`keepdims`/`dtype` y overflow
- [[concepto_dtype]] — la promoción del acumulador y el overflow (agudo aquí)
- [[np.nansum]] · [[np.nancumprod]]
