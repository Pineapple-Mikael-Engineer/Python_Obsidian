---
title: np.nanmedian — mediana ignorando NaN
aliases:
  - nanmedian
  - np.nanmedian
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

# np.nanmedian — mediana ignorando NaN

`np.nanmedian` es la variante **nan-safe** de [[np.median]]: el valor central del eje ordenado, pero
**calculado solo sobre los valores no-NaN**. Combina las dos virtudes de robustez —no la arrastran
los outliers (como [[np.median]]) **ni** los huecos `NaN`—. La diferencia clave frente a `np.median`
es que el "número de elementos" del que se toma el centro es el **conteo de no-NaN** del eje, no su
tamaño total. Toda la teoría (orden, caso par/impar, reducción, retorno) está en [[np.median]];
aquí solo el NaN y sus trampas.

## La idea en una fórmula

El mapa de shapes es **idéntico** al de [[np.median]]: el eje $p$ que se reduce desaparece del shape.

$$ (n_0,\dots,n_k)\ \xrightarrow{\ \text{nanmedian, axis}=p\ }\ (n_0,\dots,n_{p-1},\,n_{p+1},\dots,n_k) $$

Se descartan los `NaN` y se ordenan los $N$ valores no-NaN restantes $x_{(1)}\le\dots\le x_{(N)}$; la
mediana es el central según la paridad de **$N$ = nº de no-NaN** (no del tamaño del eje):

$$
\operatorname{med}(x)=
\begin{cases}
x_{\left(\frac{N+1}{2}\right)} & N \text{ impar} \\[4pt]
\dfrac{x_{\left(\frac{N}{2}\right)}+x_{\left(\frac{N}{2}+1\right)}}{2} & N \text{ par}
\end{cases}
\qquad N = \#\{\,i : x_i \neq \text{NaN}\,\}
$$

La paridad que decide entre "central único" y "promedio de los dos centrales" la fija el conteo de
no-NaN, no el número total de elementos del eje (ver [[concepto_axis_parametro]]).

## Parámetros

Los mismos que [[np.median]] (`axis`, `out`, `overwrite_input`, `keepdims`); su comportamiento no
cambia. `overwrite_input=True` permite reordenar `a` in-place para ahorrar memoria (lo **destruye**).
No tiene `dtype` ni `ddof`. Remite a [[np.median]].

## NaN: el comportamiento clave

`np.nanmedian` **excluye** los `NaN` antes de ordenar y tomar el centro, así que un `NaN` nunca
desplaza la mediana (a diferencia de [[np.median]], donde un solo `NaN` la contamina por completo).

> [!warning] Trampa: el slice **todo-NaN**
> Si **todos** los valores de un eje son `NaN`, no queda ningún valor del que tomar el centro: ese
> slice sale `NaN` con un `RuntimeWarning: All-NaN slice encountered`. No es un error; el resto de
> slices se calcula con normalidad.

```python
np.nanmedian([np.nan, np.nan])   # nan  + RuntimeWarning: All-NaN slice encountered
```

## Ejemplos

```python
import numpy as np

# 1-D: ignora el NaN, mediana de [1, 3, 100]
np.nanmedian([1, np.nan, 3, 100])   # 3.0
np.median([1, np.nan, 3, 100])      # nan  → la gemela se contamina

# Resumen robusto de datos sucios (outlier + NaN)
datos = np.array([30, np.nan, 32, 500, 31])
np.nanmedian(datos)   # 31.0  → robusto al 500 y al NaN
```

### N-D trabajado

```python
T = np.array([[[ 1.,  2.], [np.nan,  4.]],
              [[ 5., np.nan], [ 7.,  8.]],
              [[ 9., 10.  ], [11.,  6.]]])   # shape (3, 2, 2)
np.nanmedian(T, axis=0)
# [[5. ,  6.],     → med(1,5,9)=5;   med(2,10)=6 (un NaN fuera → par de 2)
#  [9. ,  6.]]     → med(7,11)=9;    med(4,8,6)=6
# El eje 0 desaparece; cada celda ordena solo sus no-NaN y toma el centro.
```

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| `RuntimeWarning: All-NaN slice encountered` + `NaN` | slice **todo-NaN** | filtrar esos ejes o aceptar el `NaN` |
| Sigue saliendo `NaN` con `np.median` | un solo `NaN` contamina `np.median` | usar `np.nanmedian` |
| `a` quedó modificado | `overwrite_input=True` reordenó `a` | dejarlo en `False` si necesitas `a` |
| Más lento que `nanmean` | la mediana requiere ordenar | esperado; usa `nanmean` si no hay outliers |

## Notas relacionadas

- [[np.median]] — la gemela; teoría de orden, caso par/impar, reducción y retorno
- [[concepto_axis_parametro]] — qué significa reducir un eje
- [[np.nanmean]] · [[np.nanstd]]
