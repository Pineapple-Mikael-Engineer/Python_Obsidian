---
title: np.histogram — cuenta cuántos valores caen en cada bin (1D)
aliases:
  - histogram
  - np.histogram
  - histograma
tags:
  - numpy
  - api/funcion
  - estadistica

# --- Clasificación ---
lib: numpy
mod: np
tipo: funcion

# --- Comportamiento ---
retorna: tuple
inplace: false

# --- Dependencias ---
requiere:
  - concepto_shape

draft: false
---

# np.histogram — cuenta cuántos valores caen en cada bin (1D)

`np.histogram` reparte los valores de un array 1D en **intervalos contiguos** (los *bins*) y cuenta cuántos caen en cada uno. Es la base del análisis de **distribución de frecuencias**: convierte una nube de números en un perfil de "cuántos hay aquí, cuántos allí". No dibuja nada — solo calcula los conteos y los bordes; para visualizar se pasan a Matplotlib (o se usa `plt.hist`, que llama a esto por debajo). La idea en una frase: discretiza un eje continuo y cuenta por celda.

## La idea

Dado un array `a` y un conjunto de `bins` bins, NumPy define `bins + 1` bordes $e_0 < e_1 < \dots < e_{\text{bins}}$ y cuenta cuántos valores de `a` caen en cada intervalo $[e_{k}, e_{k+1})$ (el último bin es cerrado por ambos lados, $[e_{\text{bins}-1}, e_{\text{bins}}]$):

$$ \text{hist}_k \;=\; \#\{\, i : e_k \le a_i < e_{k+1} \,\}, \qquad k = 0,\dots,\text{bins}-1 $$

El detalle que organiza toda la nota: **`hist` tiene `bins` elementos pero `bin_edges` tiene `bins + 1`**, porque $n$ intervalos necesitan $n+1$ fronteras. Esa asimetría es la fuente de casi todos los errores. Como mapa de shapes, la entrada 1D de cualquier tamaño colapsa a dos vectores de longitud fija:

$$ a\ \text{de shape}\ (N,) \ \xrightarrow{\ \text{histogram, bins}=b\ }\ \big(\ \text{hist}\ (b,),\ \ \text{bin\_edges}\ (b+1,)\ \big) $$

## Firma

```python
np.histogram(
    a,                 # array_like: datos de entrada (se aplana a 1D)
    bins=10,           # int | secuencia | str: nº de bins, bordes, o regla automática
    range=None,        # (float, float) | None: límites (min, max) a considerar
    density=False,     # bool: devolver densidad de probabilidad en vez de conteos
    weights=None,      # array_like | None: peso de cada valor
) -> tuple[ndarray, ndarray]   # (hist, bin_edges)
```

## Los parámetros en detalle

### `a` — los datos de entrada
`array_like`. Si no es 1D, **se aplana** internamente (`a.ravel()`) antes de contar: un `(3, 4)` se trata como 12 valores sueltos. Para histogramas que respeten la estructura multidimensional, usa [[np.histogram2d]] o [[np.histogramdd]].

### `bins` — cuántos intervalos, o dónde están sus bordes
El parámetro central, con tres modos:

| Valor | Significado |
|-------|-------------|
| `int` (defecto `10`) | ese número de bins de **igual anchura** sobre el rango |
| secuencia, p. ej. `[0, 1, 5, 10]` | **bordes explícitos** (pueden ser desiguales); define `len-1` bins |
| `str`: `'auto'`, `'sturges'`, `'fd'`, `'scott'`... | regla que **elige el número** de bins según los datos |

```python
datos = np.array([1, 2, 1, 3, 5, 2, 1])
np.histogram(datos, bins=4)[0]            # [3, 2, 1, 1]
np.histogram(datos, bins=[0, 2, 4, 6])[0] # [3, 3, 1]  → bordes desiguales propios
```

Con bordes explícitos, **tú controlas `bin_edges`**; con un `int`, NumPy los reparte uniformemente entre el mínimo y el máximo (o entre `range`).

### `range` — recortar a un intervalo
Tupla `(min, max)`. Solo se cuentan los valores dentro; los de fuera se **ignoran** (no se truncan al borde). Solo aplica cuando `bins` es un entero; con bordes explícitos no tiene efecto. Útil para fijar el mismo eje en varios histogramas comparables.

```python
np.histogram([1, 2, 3, 100], bins=3, range=(0, 3))[0]   # [1, 1, 1]  → el 100 se descarta
```

### `density` — conteos vs densidad de probabilidad
Si `True`, en vez de conteos devuelve la **densidad** $\text{hist}_k / (N \cdot \Delta_k)$, normalizada para que el **área** integre 1 (no la suma): $\sum_k \text{hist}_k \cdot \Delta_k = 1$, donde $\Delta_k$ es la anchura del bin. Es lo que hay que usar para comparar con una PDF teórica o entre muestras de distinto tamaño.

```python
h, e = np.histogram(muestras, bins=20, density=True)
np.sum(h * np.diff(e))   # ≈ 1.0  → integra a 1, no suma 1
```

### `weights` — cada valor pesa lo suyo
`array_like` de la misma longitud que `a`. En lugar de sumar 1 por valor, cada bin acumula la suma de los pesos de los valores que caen en él. Convierte el histograma en un **agregado ponderado** por intervalo (energía total por banda, masa por celda...).

```python
a = np.array([0.5, 0.5, 2.5])
w = np.array([10, 20, 5])
np.histogram(a, bins=[0, 1, 2, 3], weights=w)[0]   # [30., 0., 5.]
```

## El caso N-D

`np.histogram` es **estrictamente 1D**: aplana cualquier entrada antes de contar, así que no hay un eje que preservar. La generalización a más dimensiones es un cambio de función, no un parámetro:

| Dimensiones | Función | Entrada | Salida (conteos) |
|---|---|---|---|
| 1D | `np.histogram` | `(N,)` | `(bins,)` |
| 2D | [[np.histogram2d]] | dos `(N,)` (`x`, `y`) | `(nx, ny)` |
| N-D | [[np.histogramdd]] | `(N, D)` | `(n_0, \dots, n_{D-1})` |

## Valor de retorno

Devuelve una **tupla de dos arrays**, no un solo array — desempaquetar siempre. La asimetría de longitudes es la clave:

| Salida | Longitud / shape | Contenido | dtype |
|--------|------------------|-----------|-------|
| `hist` | `(bins,)` | nº de valores (o suma de pesos) por bin | `int64` (conteos) · `float64` (con `weights`/`density`) |
| `bin_edges` | `(bins + 1,)` | los bordes de los bins, en orden | `float64` |

```python
hist, edges = np.histogram(np.array([1, 2, 1, 3, 5, 2, 1]), bins=4)
hist             # array([3, 2, 1, 1])        ← 4 conteos
edges            # array([1., 2., 3., 4., 5.]) ← 5 bordes
len(edges) - len(hist)   # 1  ← SIEMPRE uno más
```

Para graficar o etiquetar, se usan los **centros** de los bins, derivados de los bordes:

```python
centros = (edges[:-1] + edges[1:]) / 2     # (bins,) → uno por barra
```

## Casos de uso

### Distribución de una muestra
```python
hist, edges = np.histogram(muestras, bins='auto')
centros = (edges[:-1] + edges[1:]) / 2
# plt.bar(centros, hist, width=np.diff(edges))
```

### Densidad comparable entre muestras de distinto tamaño
```python
h1, e1 = np.histogram(grupo_a, bins=30, range=(0, 100), density=True)
h2, e2 = np.histogram(grupo_b, bins=30, range=(0, 100), density=True)
# mismo eje (range) + density → directamente comparables
```

### Saber a qué bin fue cada dato
Si además de contar necesitas el índice del bin de cada valor, combínalo con [[np.digitize]] sobre los mismos bordes:

```python
hist, edges = np.histogram(datos, bins=10)
idx = np.digitize(datos, edges)   # bin de cada dato individual
```

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| Desfase al graficar | `edges` tiene `bins+1` elementos, no `bins` | usar centros `(edges[:-1]+edges[1:])/2` |
| `ValueError` al desempaquetar | devuelve **tupla** `(hist, edges)` | `hist, edges = np.histogram(...)` |
| La suma con `density=True` no da 1 | `density` normaliza el **área**, no la suma | comprobar `np.sum(h*np.diff(e)) ≈ 1` |
| Valores "desaparecen" | quedaron fuera de `range` | ampliar `range` o quitarlo |
| Estructura 2D ignorada | `histogram` aplana la entrada | usar [[np.histogram2d]] / [[np.histogramdd]] |

## Notas relacionadas

- [[concepto_shape]] — por qué `hist` y `bin_edges` tienen longitudes distintas
- [[np.histogram2d]] — la versión de dos variables
- [[np.histogramdd]] — la generalización a D dimensiones
- [[np.digitize]] — el bin de cada valor (no el conteo)
- [[np.bincount]] — conteo directo para enteros no negativos
- [[Librerias/Numpy/np/estadisticas/index|estadísticas]] — el resto de la familia
