---
title: np.histogramdd — histograma en D dimensiones (sample (N, D) → conteos D-dimensionales)
aliases:
  - histogramdd
  - np.histogramdd
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

# np.histogramdd — histograma en D dimensiones (sample (N, D) → conteos D-dimensionales)

`np.histogramdd` es **el** histograma general: cuenta cuántos puntos de un espacio de $D$ dimensiones caen en cada celda de una rejilla $D$-dimensional. [[np.histogram]] (1D) y [[np.histogram2d]] (2D) son casos particulares cómodos de esta función. La entrada es una sola matriz `(N, D)` — `N` puntos, cada uno con `D` coordenadas — y la salida es un array de conteos con **`D` ejes**, uno por dimensión del espacio. La idea en una frase: divide un espacio $D$-dimensional en una rejilla de cajas y cuenta puntos por caja.

## La idea

La entrada `sample` es `(N, D)`: la fila `i` es un punto $\mathbf{p}_i = (p_{i,0}, p_{i,1}, \dots, p_{i,D-1})$ y la **columna `d` es la dimensión `d`**. Para cada dimensión se eligen $n_d$ bins (con $n_d+1$ bordes). Un punto cae en la celda multi-índice $(k_0, k_1, \dots, k_{D-1})$ si, en cada dimensión, su coordenada está entre los bordes correspondientes:

$$ H_{k_0,\dots,k_{D-1}} \;=\; \#\Big\{\, i \;:\; \bigwedge_{d=0}^{D-1}\ e^{(d)}_{k_d} \le p_{i,d} < e^{(d)}_{k_d+1} \,\Big\} $$

El mapa de shapes es la generalización directa del 2D: una matriz `(N, D)` produce un tensor de conteos con un eje por dimensión, más una **lista** de `D` vectores de bordes:

$$ \text{sample}\ (N, D) \ \xrightarrow{\ \text{histogramdd},\ \text{bins}=(n_0,\dots,n_{D-1})\ }\ \big(\ H\ (n_0, n_1, \dots, n_{D-1}),\ \ [\,e^{(0)},\dots,e^{(D-1)}\,]\ \big) $$

con cada `edges[d]` de longitud $n_d + 1$. El eje `d` del tensor `H` **es** la dimensión `d` del espacio de datos: `H.sum(axis=d)` colapsa esa variable.

## Firma

```python
np.histogramdd(
    sample,            # array_like (N, D): N puntos, D coordenadas por punto
    bins=10,           # int | sequence: nº de bins (global o por dimensión) o bordes por dim
    range=None,        # sequence de (min, max) por dimensión | None
    density=False,     # bool: densidad de probabilidad D-dimensional en vez de conteos
    weights=None,      # array_like (N,) | None: peso de cada punto
) -> tuple[ndarray, list[ndarray]]   # (H, edges)
```

## Los parámetros en detalle

### `sample` — los puntos, como `(N, D)`
`array_like` con forma `(N, D)`: **filas = puntos, columnas = dimensiones**. Es la confusión número uno: si tienes los datos como `D` arrays de longitud `N` (una variable por array), hay que apilarlos en columnas con `np.column_stack` antes de pasarlos. NumPy lee `D` del número de columnas, así que un `sample` transpuesto produce un histograma en el número de dimensiones equivocado.

```python
xs, ys, zs = ...                 # tres variables, cada una (N,)
sample = np.column_stack([xs, ys, zs])   # (N, 3)  ← correcto
```

### `bins` — la rejilla, por dimensión
Tantos modos como dimensiones:

| Valor | Significado |
|-------|-------------|
| `int` | mismo número de bins en **todas** las dimensiones |
| `[n_0, n_1, ..., n_{D-1}]` | nº de bins por dimensión |
| `[bordes_0, ..., bordes_{D-1}]` | bordes explícitos por dimensión (anchuras desiguales) |

### `range` — recorte por dimensión
Secuencia de `D` pares `(min, max)`, uno por dimensión; los puntos fuera de la caja se **ignoran**. Se puede poner `None` en una dimensión concreta para que use su min/max automático.

### `density` — densidad D-dimensional
Si `True`, cada celda vale $H / (N\cdot V_{\text{celda}})$, normalizado para que el **hipervolumen** integre 1. Imprescindible para comparar entre muestras de distinto tamaño o contra una densidad teórica.

### `weights` — puntos ponderados
`array_like (N,)`. Cada punto suma su peso a su celda en lugar de 1.

## El caso N-D

Este **es** el caso N-D natural — no hay una versión "más alta". Las otras dos histogramas son atajos para los `D` pequeños:

| Dimensiones | Función | Entrada | Salida (conteos) | edges |
|---|---|---|---|---|
| 1D | [[np.histogram]] | `(N,)` | `(bins,)` | un array |
| 2D | [[np.histogram2d]] | dos `(N,)` | `(nx, ny)` | dos arrays |
| **N-D** | `np.histogramdd` | `(N, D)` | `(n_0, \dots, n_{D-1})` | **lista** de `D` arrays |

### Ejemplo trabajado en D = 4

Cuatro mediciones por observación — digamos un sensor que registra `(temperatura, presión, humedad, vibración)` de `N` muestras. El `sample` es `(N, 4)` y el histograma resultante es un **tensor de 4 ejes**, una caja por combinación de bins:

```python
import numpy as np
rng = np.random.default_rng(0)

# 10 000 observaciones, cada una con 4 features → sample (N, 4)
sample = rng.normal(size=(10_000, 4))    # columnas: temp, presión, humedad, vibración

# bins por dimensión: 3 en temp, 4 en presión, 5 en humedad, 2 en vibración
H, edges = np.histogramdd(sample, bins=(3, 4, 5, 2))

H.shape                 # (3, 4, 5, 2)   ← un eje por dimensión del espacio
H.ndim                  # 4
len(edges)              # 4              ← una lista con un array de bordes por dimensión
[e.shape for e in edges]   # [(4,), (5,), (6,), (3,)]  ← cada uno = n_d + 1
H.sum()                 # 10000.0        ← cada observación cayó en una caja
```

Interpretación de los ejes de `H` (multi-índice `(k0, k1, k2, k3)`):

```text
eje 0 (tamaño 3) → bin de TEMPERATURA   (columna 0 de sample)
eje 1 (tamaño 4) → bin de PRESIÓN       (columna 1)
eje 2 (tamaño 5) → bin de HUMEDAD       (columna 2)
eje 3 (tamaño 2) → bin de VIBRACIÓN     (columna 3)
```

`H[0, 0, 0, 0]` = nº de observaciones con temperatura baja **y** presión baja **y** humedad baja **y** vibración baja. Como cada eje es una dimensión, se puede **marginalizar** una variable reduciendo su eje con [[np.sum]]:

```python
H.sum(axis=3).shape     # (3, 4, 5)  → marginaliza la vibración (histograma 3D de las otras 3)
H.sum(axis=(2, 3)).shape   # (3, 4)   → histograma 2D conjunto de temp × presión
H.sum(axis=(0, 1, 2)).shape # (2,)    → histograma 1D solo de la vibración
```

Esta es la potencia real de `histogramdd`: un solo conteo $D$-dimensional del que se obtienen **todos** los histogramas marginales sumando ejes. (El mismo esquema con `bins=(2,3,4,5,6)` daría un tensor `(2,3,4,5,6)` para `D=5`.)

> [!warning] La maldición de la dimensionalidad
> El número de celdas es $\prod_d n_d$, que crece **exponencialmente** con `D`. En el ejemplo D=4 son $3\cdot4\cdot5\cdot2 = 120$ cajas; con 10 bins en 5 dimensiones serían $10^5 = 100\,000$ celdas, casi todas vacías si `N` no es enorme. Por encima de 3-4 dimensiones, baja el número de bins o reduce `D`.

## Valor de retorno

Devuelve una **tupla** `(H, edges)`. Ojo a la asimetría con las otras dos: aquí `edges` es **una sola lista de `D` arrays**, no `D` valores sueltos en la tupla.

| Salida | Tipo / shape | Contenido | dtype |
|--------|--------------|-----------|-------|
| `H` | `ndarray` `(n_0, \dots, n_{D-1})` | conteo (o peso) por celda; eje `d` = dimensión `d` | `float64` |
| `edges` | `list` de `D` arrays | `edges[d]` tiene shape `(n_d + 1,)`: bordes de la dimensión `d` | cada uno `float64` |

```python
H, edges = np.histogramdd(np.random.rand(1000, 3), bins=(5, 5, 5))
H.shape                  # (5, 5, 5)
type(edges)              # list
len(edges)               # 3  → desempaquetar: ex, ey, ez = edges
```

## Casos de uso

### Densidad en un espacio de features
```python
X = ...                                   # (N, D) matriz de features
H, edges = np.histogramdd(X, bins=8, density=True)
# H es la densidad conjunta de las D features
```

### Obtener todos los marginales de un solo conteo
```python
H, edges = np.histogramdd(sample, bins=(3, 4, 5, 2))   # D=4, ver arriba
marg_temp     = H.sum(axis=(1, 2, 3))   # (3,)   histograma 1D de la temperatura
marg_temp_pre = H.sum(axis=(2, 3))      # (3, 4) conjunto temp × presión
```

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| `D` equivocado / shape raro | `sample` está transpuesto (`(D, N)`) | pasar `(N, D)`: `np.column_stack([...])` |
| `edges` "no se desempaqueta" | `edges` es **una lista** de `D` arrays | `edges[d]` o `e0, e1, ... = edges` |
| Memoria/tiempo desbordados | $\prod n_d$ explota con `D` | bajar `bins` o reducir dimensiones |
| Variables sueltas no se apilan | `histogramdd` quiere **una** matriz | `np.column_stack([x, y, z])` |

## Notas relacionadas

- [[concepto_shape]] — el tensor `(n_0,…,n_{D-1})` y por qué `edges[d]` mide `n_d+1`
- [[np.histogram]] — el caso D=1
- [[np.histogram2d]] — el caso D=2 (atajo de esta función)
- [[np.sum]] — marginalizar una dimensión reduciendo su eje en `H`
- [[Librerias/Numpy/np/estadisticas/index|estadísticas]] — el resto de la familia
