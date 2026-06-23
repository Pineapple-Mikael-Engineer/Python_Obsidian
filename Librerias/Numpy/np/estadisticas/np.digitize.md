---
title: np.digitize — a qué bin pertenece cada valor (índice, vía búsqueda binaria)
aliases:
  - digitize
  - np.digitize
tags:
  - numpy
  - api/funcion
  - estadistica

# --- Clasificación ---
lib: numpy
mod: np
tipo: funcion

# --- Comportamiento ---
retorna: ndarray
inplace: false

# --- Dependencias ---
requiere:
  - concepto_indexing

draft: false
---

# np.digitize — a qué bin pertenece cada valor (índice, vía búsqueda binaria)

`np.digitize` responde, para cada valor de `x`, **en qué intervalo cae** dado un conjunto de bordes `bins`: devuelve el **índice del bin**, no un conteo. Donde [[np.histogram]] cuenta cuántos valores hay por intervalo, `digitize` etiqueta cada valor con su intervalo. Por debajo es una **búsqueda binaria** sobre los bordes ordenados — exactamente lo que hace [[np.searchsorted]], del que es prácticamente un envoltorio. La idea en una frase: discretiza valores continuos en etiquetas de bin.

## La idea

Dados `bins` bordes **monótonos** $b_0 < b_1 < \dots < b_{m-1}$, cada valor $x_i$ recibe el índice $k$ del intervalo que lo contiene. Con `right=False` (defecto, intervalos $[b_{k-1}, b_k)$):

$$ \text{digitize}(x_i) = k \iff b_{k-1} \le x_i < b_k, \qquad k \in \{0, 1, \dots, m\} $$

Los índices `0` y `m` (`len(bins)`) son los **desbordes**: `0` si el valor cae por debajo de todos los bordes, `m` si cae en o por encima del último. La forma de la salida **copia la de `x`** (cada valor se etiqueta de forma independiente):

$$ x\ \text{de shape}\ (n_0,\dots,n_{r-1}) \ \xrightarrow{\ \text{digitize}(\cdot,\,\text{bins})\ }\ \text{índices de shape}\ (n_0,\dots,n_{r-1}) $$

## Firma

```python
np.digitize(
    x,                 # array_like: valores a clasificar (cualquier shape)
    bins,              # array_like 1D: bordes MONÓTONOS (asc o desc)
    right=False,       # bool: lado cerrado del intervalo
) -> ndarray           # mismos shape que x, dtype entero (índices de bin)
```

## Los parámetros en detalle

### `x` — los valores a clasificar
`array_like` de cualquier shape. La salida tiene **el mismo shape** que `x`: un escalar da un índice, un `(m,)` da `(m,)`, un `(p, q)` da `(p, q)`. Cada valor se procesa por separado.

### `bins` — los bordes, monótonos
`array_like` **1D** que debe estar **ordenado**, ascendente o descendente (NumPy detecta el sentido). No los verifica: si no son monótonos, los índices carecen de significado. A diferencia de `histogram`, aquí `bins` son siempre **bordes explícitos**, no un número.

```python
x = np.array([0.2, 1.5, 2.7, 5.0])
bins = np.array([0, 1, 2, 3])
np.digitize(x, bins)   # array([1, 2, 3, 4])
#   0.2 → bin 1 ([0,1))   2.7 → bin 3 ([2,3))
#   1.5 → bin 2 ([1,2))   5.0 → bin 4 (desborde superior, ≥ 3)
```

### `right` — qué extremo del intervalo es cerrado
Decide a qué lado va un valor que **coincide con un borde**:

| `right` | Intervalo | Un valor igual a `bins[k]` va a... |
|---------|-----------|------------------------------------|
| `False` (defecto) | $[b_{k-1}, b_k)$ | el bin de la **derecha** (cerrado por la izquierda) |
| `True` | $(b_{k-1}, b_k]$ | el bin de la **izquierda** (cerrado por la derecha) |

```python
bins = np.array([0, 1, 2, 3])
np.digitize([1, 2], bins, right=False)   # [2, 3]  → el borde entra en el bin de la derecha
np.digitize([1, 2], bins, right=True)    # [1, 2]  → el borde entra en el bin de la izquierda
```

(Para bordes **descendentes** la semántica de `right` se invierte de forma coherente.)

## El caso N-D

`bins` es siempre **1D** (la tabla de bordes); la dimensionalidad la aporta `x`, y la salida **reproduce su shape**. Igual que [[np.searchsorted]], la búsqueda binaria se aplica a cada elemento de `x` por separado:

```python
bins = np.array([0, 10, 20, 30])
x = np.array([[5, 15],
              [25, 35]])          # shape (2, 2)
np.digitize(x, bins)
# array([[1, 2],
#        [3, 4]])                 # shape (2, 2), el de x
```

### Relación con `searchsorted`
`np.digitize(x, bins)` equivale esencialmente a [[np.searchsorted]] sobre los mismos bordes (con el `side` correspondiente al valor de `right`). `digitize` es la cara orientada a *binning* — pensada para "índice de bin con bordes monótonos" — mientras que `searchsorted` es la primitiva general de "índice de inserción en array ordenado". Misma búsqueda binaria $O(\log m)$ por valor por debajo.

## Valor de retorno

Un `ndarray` de **enteros** con el shape de `x`. Cada entrada está en $[0, \text{len(bins)}]$:

| Índice devuelto | Significado |
|-----------------|-------------|
| `0` | el valor cae **por debajo** de `bins[0]` (desborde inferior) |
| `k` (con `1 ≤ k ≤ m-1`) | el valor cae en el intervalo `k`-ésimo |
| `len(bins)` | el valor cae en/**por encima** de `bins[-1]` (desborde superior) |

```python
np.digitize(2.7, np.array([0, 1, 2, 3]))   # 3   → escalar de entrada, índice escalar
np.digitize([-1, 5], np.array([0, 1, 2, 3])) # [0, 4]  → ambos desbordes
```

Los índices `0` y `len(bins)` señalan los desbordes — son la trampa habitual al usarlos para indexar (ver errores).

## Casos de uso

### Convertir valores continuos en categorías
```python
notas  = np.array([55, 72, 88, 95])
cortes = np.array([60, 70, 80, 90])
np.digitize(notas, cortes)   # [0, 2, 3, 4]  → F, C, B, A
```

### A qué bin de un histograma fue cada dato
```python
hist, edges = np.histogram(datos, bins=10)
bin_idx = np.digitize(datos, edges)    # el bin (1..10) de cada valor individual
```

### Discretizar para luego contar con bincount
```python
idx = np.digitize(datos, edges)        # etiqueta de bin de cada dato
np.bincount(idx)                       # cuántos por bin (reconstruye los conteos)
```

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| Índices sin sentido | `bins` no es monótono | ordenar los bordes (`np.sort`) |
| `IndexError` al indexar con el resultado | los índices van de `0` a `len(bins)` (desbordes) | acotar con `np.clip(idx, 1, len(bins)-1)` |
| Off-by-one en los bordes | semántica `[izq, der)` por defecto | ajustar `right=True/False` |
| Confundirlo con un conteo | `digitize` da **índices**, no frecuencias | para contar, [[np.histogram]] / [[np.bincount]] |

## Notas relacionadas

- [[concepto_indexing]] — los índices devueltos y su shape
- [[np.searchsorted]] — la búsqueda binaria que implementa `digitize`
- [[np.histogram]] — cuenta por bin (digitize etiqueta cada valor)
- [[np.bincount]] — contar las etiquetas que produce `digitize`
- [[Librerias/Numpy/np/estadisticas/index|estadísticas]] — el resto de la familia
