---
title: np.nancumsum — suma acumulada ignorando NaN (NaN tratado como 0)
aliases:
  - nancumsum
  - np.nancumsum
  - suma acumulada ignorando NaN
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

# np.nancumsum — suma acumulada ignorando NaN (NaN tratado como 0)

`np.nancumsum` es la versión **NaN-safe** de [[np.cumsum]]: el mismo *scan* de prefijos —en cada posición
guarda la suma de todo lo anterior— pero **tratando cada `NaN` como `0`**. La diferencia clave es que el
acumulado **no salta a NaN ni se "rompe"** al encontrar un hueco: la serie sigue creciendo con lo que sí
hay. Hereda de la gemela toda la mecánica de barrido (`axis` dirige, no colapsa) y **conserva el shape**.

## La idea en una fórmula

Mismo **mapa de shapes** que [[np.cumsum]] (es un *scan*: la forma **no cambia**; `axis=None` aplana):

$$ (n_0,\dots,n_k)\ \xrightarrow{\ \text{nancumsum, axis}=p\ }\ (n_0,\dots,n_k) \qquad \text{(shape conservado)} $$

La recurrencia de prefijos es la de la gemela tratando el NaN como `0` (no aporta, pero **tampoco
contamina** el acumulado):

$$ c_k = c_{k-1} + \begin{cases} a_k & a_k \neq \text{NaN} \\ 0 & a_k = \text{NaN} \end{cases} $$

## Parámetros

Los mismos que [[np.cumsum]] —`a`, `axis`, `dtype`, `out`— con idéntica semántica; consúltalos allí.
Como la gemela, **no** tiene `keepdims`, `initial` ni `where`. Vigila `dtype` igual (overflow de enteros
pequeños, también en los prefijos intermedios, ver [[concepto_dtype]]); opera sobre floats porque el NaN
solo existe en punto flotante.

## NaN: el comportamiento clave

En la posición del NaN, la salida muestra la **suma corriente previa** (el NaN aportó `0`); la serie
continúa sin perder lo acumulado:

```python
import numpy as np
np.nancumsum([1, np.nan, 3])   # array([1., 1., 4.])   ← el 1 se mantiene, luego +3
np.cumsum([1, np.nan, 3])      # array([ 1., nan, nan]) ← la gemela contamina hacia adelante
```

> [!warning] La trampa del slice todo-NaN
> Si la línea es **toda NaN**, el resultado es **todo `0.`**, no NaN: cada posición arrastra una suma
> corriente de `0`. Ese cero es indistinguible de "sumé ceros reales" y **puede ocultar que no había
> datos**. Además, el `0.` en la posición de un NaN **no marca** dónde estaba el hueco: si necesitas
> recuperar las posiciones faltantes, guárdalas con `np.isnan(a)` antes.

## Ejemplos

```python
# Saldo acumulado tolerando un hueco
movs = np.array([100., np.nan, -30., 50.])
np.nancumsum(movs)   # [100., 100.,  70., 120.]
#                              └ el hueco no rompe la serie
```

```python
# N-D: el shape se conserva; axis dirige el barrido, los NaN cuentan como 0
T = np.array([[1.,  np.nan, 3.],
              [np.nan, 2., np.nan]])      # shape (2, 3)
np.nancumsum(T, axis=1)   # [[1., 1., 4.],
#                            [0., 2., 2.]]   ← cada fila acumula ignorando sus NaN
```

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| Esperar que el hueco "congele" o marque la serie | el NaN cuenta como `0`, la salida no señala dónde estaba | guardar `np.isnan(a)` aparte |
| Línea todo-NaN da `0.`, no NaN | no quedaron datos; suma corriente `0` | contar no-NaN si hace falta distinguir |
| Overflow en enteros | acumulador pequeño (también en prefijos) | `dtype=np.int64` |
| Esperar un escalar | `nancumsum` **conserva el shape** | para el total usar [[np.nansum]] |

## Notas relacionadas

- [[np.cumsum]] — la gemela que propaga NaN; mecánica de barrido y `axis`
- [[concepto_dtype]] — el acumulador y el overflow
- [[np.nansum]] · [[np.nancumprod]]
