---
title: np.nanmean — media ignorando NaN
aliases:
  - nanmean
  - np.nanmean
tags:
  - numpy
  - api/funcion
  - estadistica

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

draft: false
---

# np.nanmean — media ignorando NaN

`np.nanmean` es la variante **nan-safe** de [[np.mean]]: hace exactamente lo mismo —reducir un eje
a su media aritmética— pero **calcula solo sobre los valores no-NaN**, tratando cada `NaN` como si
no estuviera. La diferencia clave frente a `np.mean` está en el **divisor**: `np.mean` divide por el
número total de elementos del eje, mientras que `np.nanmean` divide por el **conteo de no-NaN**.
Toda la teoría de reducción (qué eje desaparece, `axis`, `keepdims`, retorno) está en [[np.mean]];
esta nota se centra en **el tratamiento del NaN y sus trampas**.

## La idea en una fórmula

El mapa de shapes es **idéntico** al de [[np.mean]]: el eje $p$ que se reduce desaparece del shape.

$$ (n_0,\dots,n_k)\ \xrightarrow{\ \text{nanmean, axis}=p\ }\ (n_0,\dots,n_{p-1},\,n_{p+1},\dots,n_k) $$

Lo que cambia es el cálculo por línea: si en el eje hay $N$ elementos de los cuales $M$ son no-NaN,
la media se hace **solo sobre esos $M$ y se divide por $M$** (no por $N$):

$$ \bar{x} = \frac{1}{M}\sum_{i\,:\,x_i\neq\text{NaN}} x_i \qquad M = \#\{\,i : x_i \neq \text{NaN}\,\} $$

Es decir, $N$ en la fórmula de la media **es el conteo de no-NaN**, no el total del eje. Si $M=N$
(no hay NaN), coincide con [[np.mean]].

## Parámetros

Los mismos que [[np.mean]] (`axis`, `dtype`, `out`, `keepdims`); su comportamiento no cambia —`axis`
colapsa el [[concepto_axis_parametro|eje]], `keepdims` lo conserva en tamaño 1 para broadcastear—.
La única diferencia semántica es que **el conteo del denominador excluye los NaN**. No tiene `where`
(el filtrado de NaN ya es implícito).

## NaN: el comportamiento clave

`np.nanmean` **ignora** cada `NaN`: lo descuenta tanto de la suma como del conteo. Es equivalente a
`np.mean(a, where=~np.isnan(a))`, pero más legible.

> [!warning] Trampa: el slice **todo-NaN**
> Si **todos** los valores de un eje son `NaN`, no queda ningún valor que promediar: el conteo es
> $M=0$ y el resultado de ese slice es `NaN`, con un `RuntimeWarning: Mean of empty slice`. No es un
> error: el cálculo continúa y solo ese slice sale `NaN`.

```python
np.nanmean([np.nan, np.nan])   # nan  + RuntimeWarning: Mean of empty slice
```

## Ejemplos

```python
import numpy as np

# 1-D: ignora el NaN, divide por 3 (no por 4)
np.nanmean([1, 2, np.nan, 5])      # 2.6667  → (1+2+5)/3, NO /4

# Comparación con np.mean (que propaga)
np.mean([1, 2, np.nan, 5])         # nan

# Por columna con lecturas faltantes (cada columna usa su propio conteo)
lecturas = np.array([[20.1, np.nan],
                     [21.0, 19.8 ]])
np.nanmean(lecturas, axis=0)       # [20.55, 19.8]  → col 0: (20.1+21)/2; col 1: 19.8/1
```

### N-D trabajado

```python
T = np.array([[[ 1.,  2.], [np.nan,  4.]],
              [[ 5., np.nan], [ 7.,  8.]]])   # shape (2, 2, 2)
np.nanmean(T, axis=0)
# [[3. , 2. ],      → (1+5)/2,  solo 2 (el otro NaN)
#  [7. , 6. ]]      → solo 7,   (4+8)/2
# El eje 0 desaparece; cada celda divide por su propio nº de no-NaN.
```

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| `RuntimeWarning: Mean of empty slice` + `NaN` | slice **todo-NaN** (conteo 0) | filtrar esos ejes o aceptar el `NaN` |
| Media más alta/baja de lo esperado | se esperaba dividir por el total, no por los no-NaN | el divisor es el **conteo de no-NaN**; es lo correcto |
| Sigue saliendo `NaN` con `np.mean` | `np.mean` propaga el `NaN` | usar `np.nanmean` (o `where=~np.isnan(a)`) |

## Notas relacionadas

- [[np.mean]] — la gemela; toda la teoría de reducción, `axis`, `dtype` y retorno
- [[concepto_axis_parametro]] — qué significa reducir un eje
- [[np.nansum]] · [[np.nanstd]] · [[np.nanmedian]]
