---
title: Delaunay — triangulacion de Delaunay de una nube de puntos
aliases:
  - Delaunay
  - scipy.spatial.Delaunay
  - triangulacion de Delaunay
tags:
  - scipy
  - api/clase
  - geometria-computacional
lib: scipy
tipo: clase
mod: scipy.spatial
requiere:
  - numpy
draft: false
---

# Delaunay — triangulacion de Delaunay de una nube de puntos

Clase que calcula la **triangulacion de Delaunay** de un conjunto de puntos (via **Qhull**): la particion del dominio en triangulos (o simplices en N-D) que **maximiza el angulo minimo** de cada triangulo, evitando triangulos finos y degenerados. Tras construirla con `points`, expone `.simplices` (indices de los vertices de cada triangulo/simplex), el metodo `.find_simplex(p)` (en que triangulo cae un punto `p`, clave para interpolacion) y `.neighbors` (triangulos adyacentes a cada uno). Es la base del mallado de datos dispersos y de la interpolacion lineal sobre puntos irregulares; de hecho, sustenta a la funcion `griddata`. Las facetas exteriores de la triangulacion coinciden con la envolvente convexa de la nube.

> La triangulacion de Delaunay y el casco convexo estan ligados: las caras **externas** de la triangulacion forman exactamente la envolvente convexa; ver [[ConvexHull]]. `Delaunay` rellena el interior con simplices, mientras que el casco solo describe el borde.

## Constructor

```python
scipy.spatial.Delaunay(
    points,               # array_like (n, ndim): n puntos en ndim dimensiones
    furthest_site=False,  # bool: triangulacion del sitio mas lejano (raro)
    incremental=False,    # bool: permitir add_points posteriores
    qhull_options=None,   # str | None: opciones crudas de Qhull (p.ej. 'QJ')
)                          # -> objeto Delaunay con simplices/find_simplex/neighbors
```

## Atributos y metodos principales

| Miembro | Tipo | Significado |
|---------|------|-------------|
| `tri.simplices` | `ndarray (nsimplex, ndim+1)` | Indices de los vertices de cada simplex (triangulo en 2D) |
| `tri.find_simplex(p)` | metodo | Indice del simplex que contiene `p` (`-1` si esta fuera) |
| `tri.neighbors` | `ndarray` | Simplices vecinos de cada simplex (`-1` si es borde) |
| `tri.points` | `ndarray` | Los puntos de entrada |
| `tri.transform` | `ndarray` | Matrices afines para coordenadas baricentricas |
| `tri.convex_hull` | `ndarray` | Facetas que forman la envolvente convexa |
| `tri.vertex_neighbor_vertices` | tupla | Adyacencia vertice-a-vertice (formato CSR) |
| `tri.add_points(pts)` | metodo | Anade puntos (requiere `incremental=True`) |

## Parametros en detalle

### `points`

Array `(n, ndim)`. En 2D produce triangulos; en 3D, tetraedros; en general, simplices de `ndim+1` vertices. Puntos casi colineales/coplanares pueden hacer fallar a Qhull; `qhull_options='QJ'` aplica una perturbacion minima que lo evita.

### `find_simplex(p)`

Localiza el simplex que contiene cada punto de `p` (acepta un array `(m, ndim)`). Devuelve el indice del simplex o `-1` si el punto cae **fuera** del casco convexo. Es la operacion central de la **interpolacion** sobre datos dispersos: una vez localizado el triangulo, se interpola con coordenadas baricentricas.

### `incremental`

Con `True` se pueden anadir puntos con `add_points` sin reconstruir; a cambio se inhabilitan algunos atributos cacheados.

## Casos de uso

### Triangular una nube y leer los triangulos

```python
import numpy as np
from scipy.spatial import Delaunay

pts = np.random.rand(20, 2)
tri = Delaunay(pts)                  # construir la triangulacion

tri.simplices                        # (ntri, 3): indices de cada triangulo
tri.simplices.shape[0]               # numero de triangulos
# plt.triplot(pts[:, 0], pts[:, 1], tri.simplices)
```

### Localizar en que triangulo cae un punto

```python
p = np.array([[0.5, 0.5], [2.0, 2.0]])
s = tri.find_simplex(p)              # indice de simplex por punto
s                                    # → p.ej. [12, -1]  (el 2o cae fuera)
dentro = s >= 0                      # mascara de puntos dentro del casco
```

### Interpolacion baricentrica manual

```python
i = tri.find_simplex([0.5, 0.5])         # triangulo contenedor
T = tri.transform[i, :2]                 # parte afin de la transformacion
r = tri.transform[i, 2]
b = T @ (np.array([0.5, 0.5]) - r)       # 2 coords baricentricas
bary = np.append(b, 1 - b.sum())         # tercera coord
verts = tri.simplices[i]                 # vertices del triangulo
# valor = (bary * z[verts]).sum()        # interpolar un campo z
```

### Vecinos de un triangulo

```python
tri.neighbors[0]                     # simplices adyacentes al triangulo 0
tri.convex_hull                      # facetas externas = casco convexo
```

## Buenas practicas

1. Usa `find_simplex` para clasificar puntos dentro/fuera del dominio: `-1` significa fuera del casco convexo.
2. Para interpolar sobre datos dispersos casi siempre conviene `griddata` (que usa Delaunay por dentro) en lugar de gestionar baricentricas a mano.
3. Ante puntos colineales/coplanares que rompen Qhull, anade `qhull_options='QJ'`.
4. Aprovecha `tri.convex_hull` para obtener el borde sin construir un `ConvexHull` aparte.
5. Si vas a localizar muchos puntos, llama a `find_simplex` con un array de golpe: esta vectorizado.

## Errores comunes

| Error | Causa | Solucion |
|-------|-------|----------|
| `QhullError: ... is flat` | Puntos colineales (2D) o coplanares (3D) | Anadir `qhull_options='QJ'` o dispersar |
| `find_simplex` devuelve `-1` inesperado | El punto cae fuera del casco convexo | Verificar el dominio; extrapolar requiere otra tecnica |
| Triangulos cruzados al graficar | Pasar mal el array de `simplices` | Usar `tri.simplices` tal cual con `triplot` |
| `add_points` falla | No se creo con `incremental=True` | Construir con `incremental=True` |
| Interpolacion incorrecta | Baricentricas mal calculadas | Preferir `griddata` o revisar `transform` |

## Limitaciones

- No **extrapola**: fuera del casco convexo `find_simplex` da `-1` y no hay simplex contenedor.
- Sensible a degeneraciones numericas; puede requerir joggle (`QJ`).
- El coste crece rapido con la dimension; en alta dimension la triangulacion es enorme.
- Para interpolacion lista para usar, casi siempre es mejor `griddata` que operar sobre los simplices manualmente.

## Notas relacionadas

- [[ConvexHull]]
- [[KDTree]]
- [[scipy.spatial.distance]]
