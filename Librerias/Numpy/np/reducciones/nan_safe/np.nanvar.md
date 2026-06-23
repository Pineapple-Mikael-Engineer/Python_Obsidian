---
title: np.nanvar — varianza ignorando NaN
aliases:
  - nanvar
  - np.nanvar
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

# np.nanvar — varianza ignorando NaN

`np.nanvar` es la variante **nan-safe** de [[np.var]]: el promedio de las desviaciones al cuadrado
respecto a la media, pero **calculado solo sobre los valores no-NaN** del eje. La diferencia clave
frente a `np.var` es el **conteo $N$**: tanto la media interna como el divisor $N-\text{ddof}$ usan
el **número de no-NaN**, no el total del eje. Es el cuadrado de [[np.nanstd]]. La teoría completa
(varianza, `ddof`, reducción, retorno) está en [[np.var]]; aquí solo el NaN y sus trampas.

## La idea en una fórmula

El mapa de shapes es **idéntico** al de [[np.var]]: el eje $p$ que se reduce desaparece del shape.

$$ (n_0,\dots,n_k)\ \xrightarrow{\ \text{nanvar, axis}=p\ }\ (n_0,\dots,n_{p-1},\,n_{p+1},\dots,n_k) $$

Si en el eje hay $N$ valores no-NaN con media $\bar{x}$ (también solo sobre los no-NaN), la varianza
es el promedio de las desviaciones al cuadrado de **esos** valores, con divisor $N-\text{ddof}$:

$$ \sigma^2 = \frac{1}{N-\text{ddof}}\sum_{i\,:\,x_i\neq\text{NaN}}(x_i-\bar{x})^2 \qquad N = \#\{\,i : x_i \neq \text{NaN}\,\} $$

Aquí **$N$ es el conteo de no-NaN**, no el número total de elementos del eje.

## Parámetros

Los mismos que [[np.var]] (`axis`, `dtype`, `out`, `ddof`, `keepdims`). **`ddof` es igual de
importante**: `ddof=0` (defecto) es poblacional (divisor $N$); `ddof=1` es muestral insesgado
(divisor $N-1$). La diferencia es que aquí ese $N$ es el conteo de **no-NaN** del eje, no su tamaño.
Remite a [[np.var]] para el detalle de `ddof` y a [[concepto_axis_parametro]] para `axis`.

## NaN: el comportamiento clave

`np.nanvar` descuenta cada `NaN` del cálculo (de la media, de las desviaciones y del conteo $N$).
Hay **dos** trampas, no una:

> [!warning] Trampa 1: slice **todo-NaN**
> Si todos los valores del eje son `NaN`, el conteo es $N=0$: el slice sale `NaN` con un
> `RuntimeWarning: Degrees of freedom <= 0 for slice`.

> [!warning] Trampa 2: pocos no-NaN frente a `ddof`
> El divisor real es `(nº de no-NaN) - ddof`. Si tras quitar NaN un slice queda con **$N \le$ `ddof`**
> valores válidos (p. ej. 1 solo no-NaN con `ddof=1`), el divisor es $\le 0$ → ese slice sale `NaN`
> con `RuntimeWarning: Degrees of freedom <= 0`. Con `ddof=1` basta **un único** no-NaN para romperlo.

```python
np.nanvar([np.nan, np.nan])              # nan  + RuntimeWarning (todo-NaN)
np.nanvar([5.0, np.nan, np.nan], ddof=1) # nan  + RuntimeWarning (1 no-NaN, divisor 1-1=0)
```

## Ejemplos

```python
import numpy as np

# 1-D: varianza de 2,4,6 (ignora el NaN), divisor 3
np.nanvar([2, 4, np.nan, 6])        # 2.667
np.var([2, 4, np.nan, 6])           # nan  → la gemela propaga

# Muestral (ddof=1) sobre los no-NaN
np.nanvar([2, 4, np.nan, 6], ddof=1)  # 4.0  → divide por (3-1)=2

# Filtrar features sin variación tolerando huecos
v = np.nanvar(datos, axis=0)
constantes = v == 0
```

### N-D trabajado

```python
T = np.array([[[ 0.,  2.], [np.nan,  6.]],
              [[ 4., np.nan], [10.,  6.]]])   # shape (2, 2, 2)
np.nanvar(T, axis=0)
# [[4. , 0. ],     → var(0,4)=4;   solo 2 → var=0 (un único valor)
#  [0. , 0. ]]     → solo 10 → 0;  var(6,6)=0
# El eje 0 desaparece; cada celda usa su propio conteo de no-NaN.
```

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| `RuntimeWarning: Degrees of freedom <= 0` + `NaN` | slice todo-NaN, o no-NaN $\le$ `ddof` | filtrar esos ejes, o bajar `ddof` |
| Valor distinto al de otra librería | `ddof` por defecto es 0 (poblacional) | usar `ddof=1` para muestral |
| Magnitud "rara", al cuadrado | la varianza está en unidades$^2$ | usar [[np.nanstd]] |
| Sigue saliendo `NaN` con `np.var` | `np.var` propaga el `NaN` | usar `np.nanvar` |

## Notas relacionadas

- [[np.var]] — la gemela; teoría de varianza, `ddof`, reducción y retorno
- [[concepto_axis_parametro]] — qué significa reducir un eje
- [[np.nanstd]] · [[np.nanmean]]
