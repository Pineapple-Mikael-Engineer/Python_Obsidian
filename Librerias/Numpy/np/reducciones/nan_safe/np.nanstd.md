---
title: np.nanstd — desviación típica ignorando NaN
aliases:
  - nanstd
  - np.nanstd
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

# np.nanstd — desviación típica ignorando NaN

`np.nanstd` es la variante **nan-safe** de [[np.std]]: la raíz de la varianza —dispersión en las
unidades originales— pero **calculada solo sobre los valores no-NaN** del eje. Es exactamente
$\sqrt{\text{nanvar}}$ (`np.nanstd(a, ddof=k) == np.sqrt(np.nanvar(a, ddof=k))`). La diferencia
clave frente a `np.std` es el **conteo $N$**: la media interna y el divisor $N-\text{ddof}$ usan el
**número de no-NaN**, no el total del eje. Toda la teoría (dispersión, `ddof`, reducción, retorno)
está en [[np.std]]; aquí solo el NaN y sus trampas.

## La idea en una fórmula

El mapa de shapes es **idéntico** al de [[np.std]]: el eje $p$ que se reduce desaparece del shape.

$$ (n_0,\dots,n_k)\ \xrightarrow{\ \text{nanstd, axis}=p\ }\ (n_0,\dots,n_{p-1},\,n_{p+1},\dots,n_k) $$

Sobre los $N$ valores no-NaN del eje, con su media $\bar{x}$ (también de los no-NaN):

$$ \sigma = \sqrt{\frac{1}{N-\text{ddof}}\sum_{i\,:\,x_i\neq\text{NaN}}(x_i-\bar{x})^2} \qquad N = \#\{\,i : x_i \neq \text{NaN}\,\} $$

Aquí **$N$ es el conteo de no-NaN**, no el número total de elementos del eje.

## Parámetros

Los mismos que [[np.std]] (`axis`, `dtype`, `out`, `ddof`, `keepdims`). **`ddof` es igual de
importante**: `ddof=0` (defecto) es poblacional (divisor $N$); `ddof=1` es muestral insesgado
(divisor $N-1$). Aquí ese $N$ es el conteo de **no-NaN** del eje. Remite a [[np.std]] para el
detalle de `ddof` y a [[concepto_axis_parametro]] para `axis`.

## NaN: el comportamiento clave

`np.nanstd` descuenta cada `NaN` del cálculo (media, desviaciones y conteo $N$). Igual que
[[np.nanvar]], tiene **dos** trampas:

> [!warning] Trampa 1: slice **todo-NaN**
> Si todos los valores del eje son `NaN`, el conteo es $N=0$: el slice sale `NaN` con un
> `RuntimeWarning: Degrees of freedom <= 0 for slice`.

> [!warning] Trampa 2: pocos no-NaN frente a `ddof`
> El divisor real es `(nº de no-NaN) - ddof`. Si tras quitar NaN un slice queda con **$N \le$ `ddof`**
> valores válidos (p. ej. 1 solo no-NaN con `ddof=1`), el divisor es $\le 0$ → ese slice sale `NaN`
> con `RuntimeWarning: Degrees of freedom <= 0`. Con `ddof=1` basta **un único** no-NaN para romperlo.

```python
np.nanstd([np.nan, np.nan])              # nan  + RuntimeWarning (todo-NaN)
np.nanstd([5.0, np.nan, np.nan], ddof=1) # nan  + RuntimeWarning (1 no-NaN, divisor 1-1=0)
```

## Ejemplos

```python
import numpy as np

# 1-D: desviación de 2,4,6 (ignora el NaN)
np.nanstd([2, 4, np.nan, 6])        # 1.633
np.std([2, 4, np.nan, 6])           # nan  → la gemela propaga

# Muestral (ddof=1) sobre los no-NaN
np.nanstd([2, 4, np.nan, 6], ddof=1)  # 2.0  → sqrt de la varianza muestral

# Dispersión por feature con datos faltantes
desv = np.nanstd(matriz, axis=0, ddof=1)
```

### N-D trabajado

```python
T = np.array([[[ 0.,  2.], [np.nan,  6.]],
              [[ 4., np.nan], [10.,  6.]]])   # shape (2, 2, 2)
np.nanstd(T, axis=0)
# [[2. , 0. ],     → std(0,4)=2;   solo 2 → 0 (un único valor)
#  [0. , 0. ]]     → solo 10 → 0;  std(6,6)=0
# El eje 0 desaparece; cada celda usa su propio conteo de no-NaN.
```

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| `RuntimeWarning: Degrees of freedom <= 0` + `NaN` | slice todo-NaN, o no-NaN $\le$ `ddof` | filtrar esos ejes, o bajar `ddof` |
| Valor distinto al de otra librería (R, pandas) | `ddof` por defecto es 0 (poblacional) | usar `ddof=1` para muestral |
| División por cero al estandarizar | la desviación de un eje es 0 (un solo no-NaN o constante) | manejar ese eje aparte |
| Sigue saliendo `NaN` con `np.std` | `np.std` propaga el `NaN` | usar `np.nanstd` |

## Notas relacionadas

- [[np.std]] — la gemela; teoría de dispersión, `ddof`, reducción y retorno
- [[concepto_axis_parametro]] — qué significa reducir un eje
- [[np.nanvar]] · [[np.nanmean]]
