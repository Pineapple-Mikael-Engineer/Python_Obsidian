---
title: scipy.interpolate.griddata — interpolacion de datos dispersos en N dimensiones
aliases:
  - griddata
  - scipy.interpolate.griddata
  - interpolacion datos dispersos
tags:
  - scipy
  - api/funcion
  - interpolacion
lib: scipy
tipo: funcion
mod: scipy.interpolate
retorna: ndarray
requiere:
  - numpy
  - numpy.meshgrid
draft: false
---

# scipy.interpolate.griddata — interpolacion de datos dispersos en N dimensiones

Interpola valores conocidos en **puntos dispersos / no estructurados** (sin malla regular) para estimarlos en posiciones nuevas `xi`, en cualquier numero de dimensiones. Es la herramienta tipica para **reconstruir un campo** (temperatura, presion, elevacion) sobre una grilla a partir de mediciones esparcidas. Recibe las coordenadas conocidas `points` de forma `(N, ndim)`, sus valores `values`, y los puntos destino `xi` (a menudo una malla creada con `np.meshgrid`). Devuelve un `ndarray` con la forma de `xi`.

> Distincion clave: `griddata` no exige que los datos esten en una rejilla; trabaja con puntos arbitrarios triangulando el espacio. Si los datos YA estan en una malla rectangular ordenada, usa `RegularGridInterpolator` (mucho mas rapido y sin triangulacion). Ver [[concepto_relacion_numpy]] sobre como NumPy aporta los arrays que aqui entran y salen.

## Firma

```python
scipy.interpolate.griddata(
    points,             # ndarray (N, ndim) o tuple de arrays 1D: coords conocidas
    values,             # ndarray (N,): valor en cada punto conocido
    xi,                 # ndarray (M, ndim) o tuple de mallas: donde interpolar
    method='linear',    # str: 'nearest' | 'linear' | 'cubic'
    fill_value=np.nan,  # float: valor fuera del casco convexo (no aplica a 'nearest')
    rescale=False,      # bool: reescala puntos a cubo unidad antes de interpolar
) -> ndarray
```

## Valor de retorno

| Tipo | Forma | Significado |
|------|-------|-------------|
| `ndarray` | igual que `xi` (sin el eje de dimension) | Valores interpolados en cada punto destino |

Los puntos de `xi` que caen **fuera del casco convexo** (convex hull) de `points` reciben `NaN`, salvo que se fije `fill_value` o se use `method='nearest'` (que siempre tiene valor).

## Formas basicas de llamada

| Objetivo | Llamada |
|----------|---------|
| Interpolar lineal sobre una malla | `griddata(pts, vals, (XX, YY))` |
| Vecino mas cercano (sin NaN) | `griddata(pts, vals, xi, method='nearest')` |
| Interpolacion suave 2D | `griddata(pts, vals, xi, method='cubic')` |
| Relleno fuera del casco | `griddata(pts, vals, xi, fill_value=0.0)` |
| Datos con escalas dispares por eje | `griddata(pts, vals, xi, rescale=True)` |

## Parametros en detalle

### `points` (obligatorio)

Coordenadas de los puntos conocidos. Array `(N, ndim)` (cada fila un punto) o, en 2D, una tupla `(x, y)` de dos arrays 1D de longitud `N`. Definen la nube de datos que se triangula internamente (Delaunay) para `linear` y `cubic`.

```python
import numpy as np
from scipy.interpolate import griddata

# 200 mediciones dispersas en un dominio 2D
rng = np.random.default_rng(0)
pts = rng.random((200, 2))          # (N, 2): coords (x, y) conocidas
vals = np.sin(pts[:, 0] * 6) * np.cos(pts[:, 1] * 6)
```

### `values` (obligatorio)

Array 1D `(N,)` con el valor escalar asociado a cada fila de `points`. Su longitud debe coincidir con `N`.

### `xi` (obligatorio)

Puntos destino. Suele construirse con `np.meshgrid` y pasarse como tupla de mallas `(XX, YY)`; tambien admite un array `(M, ndim)`. La salida adopta la forma de las mallas pasadas.

```python
# malla regular de salida 100x100 sobre [0,1]^2
gx, gy = np.linspace(0, 1, 100), np.linspace(0, 1, 100)
XX, YY = np.meshgrid(gx, gy)        # mallas 2D
campo = griddata(pts, vals, (XX, YY), method='linear')
campo.shape    # → (100, 100)
```

### `method`

| Valor | Que hace | Dimensiones | Salida fuera del casco |
|-------|----------|-------------|------------------------|
| `'nearest'` | Valor del punto conocido mas cercano | N-D | siempre definida (sin NaN) |
| `'linear'` | Interpolacion baricentrica sobre la triangulacion | N-D | `NaN` / `fill_value` |
| `'cubic'` | Spline suave (Clough-Tocher en 2D) | solo 1D y 2D | `NaN` / `fill_value` |

`cubic` da el campo mas suave pero **solo existe para 1D y 2D**; en mas dimensiones se debe usar `linear` o `nearest`.

### `fill_value`

Valor asignado a puntos fuera del casco convexo. Por defecto `np.nan`. **No tiene efecto con `method='nearest'`**, que siempre encuentra un vecino.

```python
campo = griddata(pts, vals, (XX, YY), method='linear', fill_value=0.0)
# las esquinas sin datos quedan en 0.0 en vez de NaN
```

### `rescale`

Con `rescale=True` los puntos se reescalan al cubo unidad antes de triangular. Util cuando los ejes tienen **unidades/magnitudes muy distintas** (p. ej. x en metros y z en milimetros), evitando triangulaciones degeneradas.

## Casos de uso

### Reconstruir un campo de temperatura sobre una grilla

```python
import numpy as np
from scipy.interpolate import griddata

# Sensores dispersos: (x, y) en m y temperatura medida en C
xy = np.array([[0.1, 0.2], [0.8, 0.1], [0.5, 0.9],
               [0.3, 0.6], [0.9, 0.7], [0.2, 0.85]])
T  = np.array([21.0, 24.5, 19.8, 22.1, 25.0, 20.3])

gx, gy = np.linspace(0, 1, 50), np.linspace(0, 1, 50)
XX, YY = np.meshgrid(gx, gy)
T_grid = griddata(xy, T, (XX, YY), method='cubic')
T_grid.shape    # → (50, 50)   campo continuo listo para contourf/imshow
```

### Evitar NaN en los bordes con nearest

```python
# 'linear' deja NaN fuera del casco; 'nearest' rellena todo el dominio
T_lin  = griddata(xy, T, (XX, YY), method='linear')
T_near = griddata(xy, T, (XX, YY), method='nearest')
np.isnan(T_lin).any()    # → True   (esquinas sin datos)
np.isnan(T_near).any()   # → False  (siempre hay vecino)
```

### Interpolar en puntos sueltos (no una malla)

```python
# xi como lista de puntos concretos, no una grilla
destino = np.array([[0.4, 0.4], [0.7, 0.5]])
vals_d  = griddata(xy, T, destino, method='linear')
vals_d.shape    # → (2,)
```

### 3D: campo escalar en un volumen

```python
# En 3D solo 'linear' o 'nearest' ('cubic' no esta disponible)
pts3 = np.random.default_rng(1).random((300, 3))
v3   = pts3.sum(axis=1)
gx = gy = gz = np.linspace(0, 1, 20)
GX, GY, GZ = np.meshgrid(gx, gy, gz)
vol = griddata(pts3, v3, (GX, GY, GZ), method='linear')
vol.shape    # → (20, 20, 20)
```

## Buenas practicas

1. Construye `xi` con `np.meshgrid` y pasalo como tupla `(XX, YY)`; la salida hereda esa forma y se grafica directo con `contourf`/`imshow`.
2. Usa `method='cubic'` para campos suaves de visualizacion (solo 1D/2D); `linear` para algo robusto y general; `nearest` cuando no quieras introducir valores inventados.
3. Si necesitas el dominio completo sin huecos, usa `fill_value` o combina con `nearest`.
4. Aplica `rescale=True` cuando las coordenadas tengan escalas dispares por eje.
5. Si vas a interpolar **muchas veces** sobre los mismos puntos conocidos, prefiere construir un interpolador reutilizable (`LinearNDInterpolator`, `CloughTocher2DInterpolator`): `griddata` re-triangula en cada llamada.
6. Si tus datos ya forman una malla regular, NO uses `griddata`: usa `RegularGridInterpolator`, mucho mas rapido.

## Errores comunes

| Error | Causa | Solucion |
|-------|-------|----------|
| Salida llena de `NaN` | `xi` cae fuera del casco convexo de `points` | Usar `fill_value`, `method='nearest'` o ampliar los datos |
| `ValueError: different number of values and points` | `len(values) != N` | Alinear `values` con las filas de `points` |
| `cubic` lanza error en 3D | `cubic` solo existe en 1D y 2D | Usar `linear` o `nearest` |
| `QhullError` / triangulacion degenerada | Puntos colineales/coplanares o escalas dispares | Activar `rescale=True` o perturbar/limpiar puntos |
| Resultado lento con muchas llamadas | `griddata` triangula en cada invocacion | Crear `LinearNDInterpolator` una vez y reutilizar |
| Forma de salida inesperada | `xi` pasado como array plano, no como mallas | Pasar la tupla de `meshgrid` `(XX, YY)` |

## Limitaciones

- Re-triangula en cada llamada: ineficiente para interpolacion repetida sobre los mismos `points`.
- `cubic` limitado a 1D y 2D; en mas dimensiones solo `linear`/`nearest`.
- No extrapola: fuera del casco convexo entrega `NaN`/`fill_value` (salvo `nearest`).
- Para datos sobre malla regular es la herramienta equivocada: `RegularGridInterpolator` es el camino correcto.
- No suaviza ruido: interpola los valores tal cual; para ajuste suavizado usar splines (`splrep` con `s>0`).

## Notas relacionadas

- [[RegularGridInterpolator]]
- [[LinearNDInterpolator]]
- [[scipy.interpolate.splrep_splev]]
- [[concepto_relacion_numpy]]
