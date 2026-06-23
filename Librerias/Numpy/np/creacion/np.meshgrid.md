---
title: np.meshgrid — rejillas de coordenadas a partir de vectores 1D
aliases:
  - meshgrid
  - np.meshgrid
  - rejilla
  - malla
tags:
  - numpy
  - api/funcion
  - creacion

# --- Clasificación ---
lib: numpy
mod: np
tipo: funcion

# --- Comportamiento ---
retorna: list[ndarray]
inplace: false

# --- Dependencias ---
requiere:
  - concepto_shape
  - concepto_broadcasting

draft: false
---

# np.meshgrid — rejillas de coordenadas a partir de vectores 1D

`np.meshgrid` toma varios vectores de coordenadas 1D (uno por eje) y construye las **rejillas de
coordenadas** que los combinan: para cada punto de la malla, devuelve sus coordenadas en arrays del
mismo shape. Con dos vectores `x` `(n,)` e `y` `(m,)` produce dos matrices `X, Y` que, leídas
elemento a elemento, recorren **todas las combinaciones** $(x_i, y_j)$. Es la herramienta estándar
para **evaluar una función $f(x, y)$ sobre una rejilla** y para preparar datos de gráficos 3D y mapas
de contorno.

## La idea

A partir de `x` de shape $(n,)$ e `y` de shape $(m,)$, `meshgrid` genera dos arrays 2D donde:

- `X[j, i] = x[i]` — la coordenada x repetida a lo largo de las filas,
- `Y[j, i] = y[j]` — la coordenada y repetida a lo largo de las columnas.

Con el `indexing='xy'` por defecto (convención cartesiana), **ambas salidas tienen shape $(m, n)$**:

$$ x:(n,),\ \ y:(m,) \;\xrightarrow{\ \text{meshgrid, indexing='xy'}\ }\; X:(m,n),\ \ Y:(m,n) $$

Con `indexing='ij'` (convención matricial) las salidas son $(n, m)$ y los papeles de filas/columnas
se intercambian. La gracia es que evaluar `f(X, Y)` aprovecha el [[concepto_broadcasting|broadcasting]]
y la vectorización: una sola expresión calcula `f` en los `m·n` puntos sin bucles. De hecho, con
`sparse=True`, `meshgrid` ni siquiera materializa las matrices completas, sino vectores de shape
`(1, n)` y `(m, 1)` que broadcastean a `(m, n)` cuando se operan.

## Firma

```python
np.meshgrid(
    *xi,                # array_like: 1, 2 o más vectores de coordenadas 1D
    copy=True,          # bool: si False, devuelve vistas (ojo al escribir)
    sparse=False,       # bool: salidas "ralas" (1,n)/(m,1) para ahorrar memoria
    indexing='xy',      # 'xy' (cartesiano) | 'ij' (matricial)
) -> list[ndarray]
```

## Los parámetros en detalle

### `*xi` — los vectores de coordenadas
Uno o más arrays 1D, uno por eje de la rejilla. Con `k` vectores, `meshgrid` devuelve una **lista de
`k` arrays**, cada uno de la forma completa de la rejilla. El orden de salida sigue al de entrada.

```python
x = np.array([1, 2, 3])      # (3,)
y = np.array([10, 20])       # (2,)
X, Y = np.meshgrid(x, y)     # X, Y de shape (2, 3)  (indexing='xy')
X
# [[1, 2, 3],
#  [1, 2, 3]]
Y
# [[10, 10, 10],
#  [20, 20, 20]]
```

### `indexing` — convención de ejes (`'xy'` vs `'ij'`)
Decide qué eje es fila y cuál columna. Es la fuente número uno de confusión con `meshgrid`:

| `indexing` | shape de salida (de `x:(n,)`, `y:(m,)`) | convención | uso típico |
|---|---|---|---|
| `'xy'` (defecto) | `(m, n)` | cartesiana: `x`→columnas, `y`→filas | gráficos, `contour`, mapas |
| `'ij'` | `(n, m)` | matricial: `x`→filas, `y`→columnas | indexar matrices, álgebra |

```python
X, Y = np.meshgrid(x, y, indexing='ij')   # ahora shape (3, 2)
```

### `sparse` — rejilla rala (ahorro de memoria)
Si `True`, en vez de matrices completas devuelve arrays con un solo eje "real" y el resto en tamaño
1, que **broadcastean** a la rejilla densa al operarlos. Para `x:(n,)`, `y:(m,)` con `'xy'`:

$$ X:(1,n),\quad Y:(m,1)\ \xrightarrow{\ \text{broadcast}\ }\ (m,n) $$

Memoria $O(n+m)$ en vez de $O(n\cdot m)$, sin cambiar el resultado de `f(X, Y)`:

```python
X, Y = np.meshgrid(x, y, sparse=True)
X.shape, Y.shape    # (1, 3), (2, 1)
(X + Y).shape       # (2, 3)  → broadcasting reconstruye la rejilla densa
```

### `copy` — vistas en vez de copias
Si `False`, las salidas pueden ser **vistas** con strides 0 (no copian datos); ahorra memoria pero
escribir en ellas es peligroso (un valor toca varias celdas). Por defecto `True` (copias seguras).

## El caso N-D

`meshgrid` generaliza a cualquier número de vectores: con `k` vectores de tamaños $n_0, n_1, \dots,
n_{k-1}$ devuelve `k` arrays, **cada uno de shape $k$-dimensional**. Con `indexing='ij'` el mapa es
directo (sin el swap de los dos primeros ejes que introduce `'xy'`):

$$ x_0:(n_0,),\dots,x_{k-1}:(n_{k-1},) \;\xrightarrow{\ \text{meshgrid, 'ij'}\ }\; k \text{ arrays de shape } (n_0, n_1, \dots, n_{k-1}) $$

Ejemplo con **3 vectores** → 3 rejillas 3D, el caso típico para evaluar un campo $f(x, y, z)$ en un
volumen:

```python
x = np.linspace(0, 1, 4)     # (4,)
y = np.linspace(0, 1, 5)     # (5,)
z = np.linspace(0, 1, 6)     # (6,)

X, Y, Z = np.meshgrid(x, y, z, indexing='ij')
X.shape, Y.shape, Z.shape    # (4, 5, 6) cada uno

# Evaluar un campo escalar en todo el volumen, sin bucles:
campo = np.sqrt(X**2 + Y**2 + Z**2)   # distancia al origen, shape (4, 5, 6)
campo.shape                            # (4, 5, 6)
```

Cada uno de los $4\cdot5\cdot6 = 120$ puntos del volumen recibe sus tres coordenadas vía las rejillas
`X, Y, Z`, y la expresión vectorizada calcula `campo` de golpe. Con `sparse=True` las mismas tres
salidas serían `(4,1,1)`, `(1,5,1)` y `(1,1,6)`, que broadcastean a `(4, 5, 6)` (ver
[[concepto_broadcasting]]) ocupando $4+5+6$ valores en vez de $120\cdot3$.

## Casos de uso

### Evaluar f(x, y) sobre una rejilla
```python
x = np.linspace(-2, 2, 100)
y = np.linspace(-2, 2, 100)
X, Y = np.meshgrid(x, y)
Z = np.exp(-(X**2 + Y**2))    # gaussiana 2D, shape (100, 100)
```

### Superficie / contorno para graficar
```python
X, Y = np.meshgrid(x, y)
# plt.contourf(X, Y, Z)  o  ax.plot_surface(X, Y, Z)
```

### Rejilla rala para ahorrar memoria
```python
X, Y = np.meshgrid(x, y, sparse=True)   # (1,100) y (100,1)
Z = np.exp(-(X**2 + Y**2))              # broadcasting → (100, 100)
```

### Campo 3D (volumen)
```python
X, Y, Z = np.meshgrid(x, y, z, indexing='ij')
potencial = 1.0 / np.sqrt(X**2 + Y**2 + Z**2 + 1e-9)   # (nx, ny, nz)
```

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| Shape de salida "traspuesto" | `'xy'` da `(m, n)`, no `(n, m)` | usar `indexing='ij'` si quieres `(n, m)` |
| `X` e `Y` intercambiados al graficar | mezclar convención `'xy'`/`'ij'` con la del graficador | fijar `indexing` y verificar `X.shape` |
| Resultado corrupto al escribir en la salida | se usó `copy=False` (vistas con stride 0) | dejar `copy=True` (defecto) |
| Memoria desbordada con rejilla grande | matrices densas $O(n\cdot m)$ | usar `sparse=True` y dejar broadcastear |
| `f(X, Y)` falla por shapes | mezclar salidas densas y ralas | no mezclar; o reconstruir con el mismo `sparse` |

## Notas relacionadas

- [[concepto_shape]] — los `k` arrays de salida comparten la forma de la rejilla
- [[concepto_broadcasting]] — base de `sparse=True` y de evaluar `f` sin bucles
- [[np.linspace]] — el origen habitual de los vectores de coordenadas
- [[np.arange]] · [[np.mgrid]] · [[np.indices]]
