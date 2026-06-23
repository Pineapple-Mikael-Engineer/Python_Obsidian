---
title: np.nancumprod — producto acumulado ignorando NaN (NaN tratado como 1)
aliases:
  - nancumprod
  - np.nancumprod
  - producto acumulado ignorando NaN
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
  - concepto_dtype

draft: false
---

# np.nancumprod — producto acumulado ignorando NaN (NaN tratado como 1)

`np.nancumprod` es la versión **NaN-safe** de [[np.cumprod]]: el mismo *scan* multiplicativo —en cada
posición guarda el producto de todo lo anterior— pero **tratando cada `NaN` como `1`**. La diferencia
clave es que el acumulado **no salta a NaN ni se rompe** en los huecos: la trayectoria de productos
continúa con los factores válidos. Hereda de la gemela el barrido (`axis` dirige, no colapsa), el shape
**conservado** y la **trampa aguda del overflow** (crecimiento exponencial).

## La idea en una fórmula

Mismo **mapa de shapes** que [[np.cumprod]] (es un *scan*: la forma **no cambia**; `axis=None` aplana):

$$ (n_0,\dots,n_k)\ \xrightarrow{\ \text{nancumprod, axis}=p\ }\ (n_0,\dots,n_k) \qquad \text{(shape conservado)} $$

La recurrencia es la de la gemela tratando el NaN como factor `1` (no altera el acumulado ni lo
contamina):

$$ c_k = c_{k-1} \cdot \begin{cases} a_k & a_k \neq \text{NaN} \\ 1 & a_k = \text{NaN} \end{cases} $$

## Parámetros

Los mismos que [[np.cumprod]] —`a`, `axis`, `dtype`, `out`— con idéntica semántica; consúltalos allí.
Como la gemela, **no** tiene `keepdims`, `initial` ni `where`. Lo propio: opera sobre floats (el NaN solo
existe en punto flotante) y conserva la **trampa del overflow** de [[concepto_dtype]] —fija `dtype` amplio
con varios factores.

## NaN: el comportamiento clave

En la posición del NaN, la salida repite el **producto corriente previo** (el NaN aportó factor `1`); la
serie sigue sin romperse:

```python
import numpy as np
np.nancumprod([2, np.nan, 3])   # array([2., 2., 6.])   ← el 2 se mantiene, luego ·3
np.cumprod([2, np.nan, 3])      # array([ 2., nan, nan]) ← la gemela contamina hacia adelante
```

> [!warning] La trampa del slice todo-NaN
> Si la línea es **toda NaN**, el resultado es **todo `1.`**, no NaN: cada posición arrastra un producto
> corriente de `1` (neutro multiplicativo). Ese uno es indistinguible de "multipliqué unos reales" y
> **puede ocultar que no había datos**. El `1.` en la posición de un NaN **no marca** el hueco; guarda
> `np.isnan(a)` aparte si necesitas las posiciones faltantes.

## Ejemplos

```python
# Factor compuesto con un periodo faltante
tasas = np.array([1.05, np.nan, 1.04])
np.nancumprod(tasas)   # [1.05, 1.05, 1.092]
#                               └ el hueco no rompe la capitalización
```

```python
# N-D: el shape se conserva; axis dirige el barrido, los NaN cuentan como 1
T = np.array([[2.,  np.nan, 3.],
              [np.nan, 5., np.nan]])      # shape (2, 3)
np.nancumprod(T, axis=1)   # [[2., 2., 6.],
#                             [1., 5., 5.]]   ← cada fila acumula ignorando sus NaN
```

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| Esperar que el hueco "rompa" o marque la serie | el NaN cuenta como `1`, la salida no señala dónde estaba | guardar `np.isnan(a)` aparte |
| Línea todo-NaN da `1.`, no NaN | no quedaron factores; producto corriente `1` | contar no-NaN si hace falta distinguir |
| Overflow / resultado absurdo | crecimiento multiplicativo (también en prefijos) | `dtype=np.float64` o `np.int64` |
| Esperar un escalar | `nancumprod` **conserva el shape** | para el total usar [[np.nanprod]] |

## Notas relacionadas

- [[np.cumprod]] — la gemela que propaga NaN; mecánica de barrido y overflow
- [[concepto_dtype]] — el acumulador y el overflow (agudo aquí)
- [[np.nancumsum]] · [[np.nanprod]]
