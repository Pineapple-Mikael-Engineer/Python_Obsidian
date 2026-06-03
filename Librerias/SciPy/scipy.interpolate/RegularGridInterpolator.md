---
title: RegularGridInterpolator — interpolacion N-D en malla regular (callable)
aliases:
  - RegularGridInterpolator
  - scipy.interpolate.RegularGridInterpolator
  - interpolacion en grilla
tags:
  - scipy
  - api/clase
  - interpolacion
lib: scipy
tipo: clase
mod: scipy.interpolate
requiere:
  - numpy
draft: false
---

# RegularGridInterpolator — interpolacion N-D en malla regular (callable)

Clase que interpola valores definidos sobre una **malla regular (rectilinea)** en N dimensiones. "Regular" significa que los puntos forman una rejilla producto de ejes 1D (no necesariamente con espaciado uniforme), no que esten igualmente espaciados. Se construye con los ejes y el array de valores, y luego se evalua `rgi(puntos)` sobre coordenadas arbitrarias. Es la herramienta correcta para **datos tabulados en grilla** (tablas termodinamicas, campos 2D/3D, lookup multivariable).

## Constructor

```python
scipy.interpolate.RegularGridInterpolator(
    points,                 # tupla de arrays 1D: (eje0, eje1, ...), uno por dimension
    values,                 # ndarray N-D: forma (len(eje0), len(eje1), ...)
    method='linear',       # str: 'linear','nearest','cubic','quintic','pchip',...
    bounds_error=True,     # bool: error si un punto cae fuera de la malla
    fill_value=nan,        # valor fuera de rango (None = extrapolar; solo algunos metodos)
)                            # -> callable rgi(xi, method=None) -> ndarray
```

## Parametros en detalle

### `points` y `values`

- `points`: **tupla** de arrays 1D **estrictamente crecientes**, uno por eje. Sus longitudes definen la forma de la malla.
- `values`: array N-D cuya forma debe ser exactamente `(len(points[0]), len(points[1]), ...)`. `values[i, j, ...]` es el valor en el nodo `(points[0][i], points[1][j], ...)`.

### `method`

| `method` | Esquema | Coste / continuidad |
|----------|---------|---------------------|
| `'linear'` (default) | Multilineal (bilineal/trilineal) | Rapido, C0 |
| `'nearest'` | Valor del nodo mas cercano | Muy rapido, escalonado |
| `'slinear'` | Spline grado 1 por ejes | C0 |
| `'cubic'` | Spline grado 3 por ejes | Suave C2, mas caro |
| `'quintic'` | Spline grado 5 por ejes | Muy suave, caro |
| `'pchip'` | Hermite monotono por ejes | Sin overshoot |

El metodo puede sobrescribirse en cada llamada: `rgi(xi, method='nearest')`.

### `bounds_error` y `fill_value`

Igual filosofia que en otros interpoladores: con `bounds_error=True` (default) un punto fuera de la malla lanza `ValueError`. Con `bounds_error=False` se rellena con `fill_value`; si `fill_value=None`, se **extrapola** (solo para metodos que lo soportan, p.ej. linear/nearest).

## Casos de uso

### Interpolar un campo 2D (tabla de propiedades)

```python
import numpy as np
from scipy.interpolate import RegularGridInterpolator

T = np.array([300., 350., 400., 450.])      # eje 0: temperatura
P = np.array([1e5, 2e5, 5e5])               # eje 1: presion
H = np.random.rand(4, 3)                      # values[i,j] = entalpia(T[i], P[j])

rgi = RegularGridInterpolator((T, P), H)      # se construye el interpolador

# se EVALUA en puntos (m, ndim): cada fila es (T, P)
pts = np.array([[325., 1.5e5],
                [410., 3.0e5]])
rgi(pts)                                       # → ndarray (2,) entalpias interpoladas
```

### Fuera de rango sin error

```python
rgi2 = RegularGridInterpolator((T, P), H,
                               bounds_error=False, fill_value=-1.0)
rgi2([[500., 1e5]])                            # → array([-1.]) (fuera de la malla)
```

### Campo 3D y metodo suave

```python
x = np.linspace(0, 1, 5); y = np.linspace(0, 1, 6); z = np.linspace(0, 1, 7)
V = np.random.rand(5, 6, 7)                    # values en la rejilla 3D
rgi3 = RegularGridInterpolator((x, y, z), V, method='cubic')
rgi3([[0.2, 0.4, 0.6]])                        # interpola con spline cubico
```

## Buenas practicas

1. Pasa `points` como **tupla de ejes 1D crecientes**; no construyas la malla densa con `meshgrid` para esto.
2. Asegura que `values.shape` casa con las longitudes de los ejes, en el **mismo orden**.
3. Da los puntos de consulta como array `(m, ndim)`; una sola consulta es `[[c0, c1, ...]]`.
4. Empieza con `'linear'`; sube a `'cubic'/'pchip'` solo si necesitas suavidad o monotonia, asumiendo mas coste.
5. Decide el comportamiento fuera de rango de forma explicita (`bounds_error` o `fill_value`) en vez de confiar en el default.

## Errores comunes

| Error | Causa | Solucion |
|-------|-------|----------|
| `ValueError: One of the requested xi is out of bounds` | Punto fuera de la malla con `bounds_error=True` | Fijar `fill_value`/`None` o filtrar consultas |
| `ValueError: There are N points and M values...` | `values.shape` no casa con los ejes | Alinear forma y orden de `points`/`values` |
| `ValueError: The points in dimension k must be strictly ascending` | Eje no ordenado | Ordenar cada eje de `points` |
| Forma de salida inesperada | `xi` no es `(m, ndim)` | Usar `np.array(pts)` con ndim columnas |
| Resultado escalonado | `method='nearest'` sin querer | Cambiar a `'linear'`/`'cubic'` |

## Limitaciones

- Solo sirve para datos en **malla regular**; para puntos **dispersos no estructurados** usa `griddata` (o `LinearNDInterpolator`). El contraste clave: `griddata` triangula nubes de puntos arbitrarias, esta clase exige rejilla producto.
- Interpola exactamente: **no suaviza** ruido.
- Los metodos de alto orden (`cubic`, `quintic`) son **caros** en memoria/tiempo y pueden oscilar.
- La extrapolacion (`fill_value=None`) solo esta disponible para algunos metodos.

## Notas relacionadas

- [[interp1d]]
- [[CubicSpline]]
- [[scipy.interpolate.griddata]]
- [[numpy.meshgrid]]
