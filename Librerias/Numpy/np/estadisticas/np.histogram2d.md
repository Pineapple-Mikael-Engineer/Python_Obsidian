---
title: np.histogram2d — histograma 2D de dos variables (x, y) en una rejilla
aliases:
  - histogram2d
  - np.histogram2d
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

# np.histogram2d — histograma 2D de dos variables (x, y) en una rejilla

`np.histogram2d` cuenta cuántos **pares** $(x_i, y_i)$ caen en cada celda de una rejilla 2D. Es la versión bidimensional de [[np.histogram]]: en vez de repartir valores en intervalos de una recta, reparte puntos en las casillas de un plano cuadriculado. El resultado es una **matriz de conteos** que se visualiza como mapa de calor / densidad conjunta. La idea en una frase: discretiza el plano $x\times y$ en una rejilla y cuenta puntos por casilla.

## La idea

Se reciben dos arrays 1D `x` e `y` **de la misma longitud** — emparejados elemento a elemento, $(x_i, y_i)$ es un punto. Se definen `nx` bins en el eje X (con `nx+1` bordes) y `ny` bins en el eje Y (con `ny+1` bordes); cada punto cae en una celda $(r, c)$ y se cuenta:

$$ H_{r,c} \;=\; \#\{\, i : xe_r \le x_i < xe_{r+1}\ \wedge\ ye_c \le y_i < ye_{c+1} \,\} $$

El mapa de shapes: dos vectores `(N,)` producen una **matriz** `(nx, ny)` de conteos más los bordes de cada eje:

$$ x,\,y\ \text{de shape}\ (N,) \ \xrightarrow{\ \text{histogram2d}\ }\ \big(\ H\ (n_x, n_y),\ \ xe\ (n_x{+}1,),\ \ ye\ (n_y{+}1,)\ \big) $$

La fila de `H` indexa el bin de **X**, la columna indexa el bin de **Y**. Esa convención (fila = X) es justo la que obliga a transponer al graficar con `imshow`.

## Firma

```python
np.histogram2d(
    x,                 # array_like (N,): coordenada X de cada punto
    y,                 # array_like (N,): coordenada Y de cada punto
    bins=10,           # int | [nx, ny] | array | [array_x, array_y]: bins por eje
    range=None,        # [[xmin, xmax], [ymin, ymax]] | None: límites por eje
    density=False,     # bool: densidad de probabilidad 2D en vez de conteos
    weights=None,      # array_like (N,) | None: peso de cada punto
) -> tuple[ndarray, ndarray, ndarray]   # (H, xedges, yedges)
```

## Los parámetros en detalle

### `x`, `y` — las dos coordenadas
Dos `array_like` **1D de igual longitud** `N`: `x[i]` e `y[i]` son las coordenadas del mismo punto. Si difieren en longitud, los puntos no se pueden emparejar y NumPy lanza error.

### `bins` — la rejilla, por eje
Más flexible que en 1D porque hay dos ejes:

| Valor | Significado |
|-------|-------------|
| `int` | mismo número de bins en **ambos** ejes |
| `[nx, ny]` | bins distintos por eje |
| array de bordes | mismos bordes explícitos en ambos ejes |
| `[bordes_x, bordes_y]` | bordes explícitos independientes por eje |

```python
np.histogram2d(x, y, bins=20)             # rejilla 20×20
np.histogram2d(x, y, bins=[30, 10])       # 30 en X, 10 en Y
np.histogram2d(x, y, bins=[xe, ye])       # bordes propios por eje
```

### `range` — recorte por eje
`[[xmin, xmax], [ymin, ymax]]`. Los puntos fuera de ese rectángulo se **ignoran**. Sirve para fijar la misma ventana en varios histogramas comparables. Solo aplica cuando `bins` da números, no bordes.

### `density` — densidad conjunta
Si `True`, devuelve la densidad de probabilidad 2D: cada celda vale $H_{r,c}/(N\cdot A_{r,c})$ con $A_{r,c}$ el área de la celda, de modo que **el volumen total integra 1** ($\sum H_{r,c}\,A_{r,c}=1$).

### `weights` — puntos ponderados
`array_like (N,)`. Cada punto suma su peso a la celda en lugar de 1; convierte la rejilla en un agregado ponderado (masa, energía...) por casilla.

## El caso N-D

`np.histogram2d` es exactamente 2D — es un caso particular cómodo de [[np.histogramdd]]. De hecho `histogram2d(x, y)` equivale a `histogramdd(np.column_stack([x, y]))`. Para tres o más variables hay que dar el salto a `histogramdd`, que toma una sola matriz `(N, D)`:

| Dimensiones | Función | Entrada | Salida (conteos) |
|---|---|---|---|
| 1D | [[np.histogram]] | `(N,)` | `(bins,)` |
| 2D | `np.histogram2d` | dos `(N,)` | `(nx, ny)` |
| N-D | [[np.histogramdd]] | `(N, D)` | `(n_0, \dots, n_{D-1})` |

## Valor de retorno

Devuelve una **tupla de tres arrays** — `H` y un vector de bordes por eje:

| Salida | Shape | Contenido | dtype |
|--------|-------|-----------|-------|
| `H` | `(nx, ny)` | conteo (o peso) por celda; **fila = X, columna = Y** | `float64` |
| `xedges` | `(nx + 1,)` | bordes del eje X | `float64` |
| `yedges` | `(ny + 1,)` | bordes del eje Y | `float64` |

```python
x = np.random.rand(1000)
y = np.random.rand(1000)
H, xe, ye = np.histogram2d(x, y, bins=20)
H.shape          # (20, 20)
xe.shape, ye.shape   # ((21,), (21,))  ← cada uno, un borde más que su eje
H.sum()          # 1000.0  ← todos los puntos contados (sin density)
```

## Casos de uso

### Mapa de densidad de puntos (heatmap)
```python
H, xe, ye = np.histogram2d(lon, lat, bins=50)
# imshow espera fila = eje vertical → transponer y origin='lower'
# plt.imshow(H.T, origin='lower', extent=[xe[0], xe[-1], ye[0], ye[-1]])
```

### Densidad conjunta comparable
```python
H, xe, ye = np.histogram2d(x, y, bins=40, range=[[0, 1], [0, 1]], density=True)
np.sum(H * np.outer(np.diff(xe), np.diff(ye)))   # ≈ 1.0  → integra a 1
```

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| Imagen "girada"/transpuesta | `H` usa fila=X, `imshow` espera fila=Y | graficar `H.T` con `origin='lower'` |
| `x` e `y` de distinto largo | deben emparejarse punto a punto | igualar longitudes |
| Devuelve **tres** valores | la tupla es `(H, xedges, yedges)` | `H, xe, ye = np.histogram2d(...)` |
| Puntos "perdidos" | quedaron fuera de `range` | ampliar/quitar `range` |

## Notas relacionadas

- [[concepto_shape]] — la matriz `(nx, ny)` y los bordes `nx+1`/`ny+1`
- [[np.histogram]] — la versión 1D
- [[np.histogramdd]] — la generalización a D variables (`histogram2d` es su caso D=2)
- [[Librerias/Numpy/np/estadisticas/index|estadísticas]] — el resto de la familia
