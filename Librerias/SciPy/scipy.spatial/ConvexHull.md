---
title: ConvexHull — envolvente convexa de una nube de puntos
aliases:
  - ConvexHull
  - scipy.spatial.ConvexHull
  - envolvente convexa
  - casco convexo
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

# ConvexHull — envolvente convexa de una nube de puntos

Clase que calcula la **envolvente convexa** (convex hull) de un conjunto de puntos en N dimensiones usando la libreria **Qhull**: el menor poligono (2D) o poliedro (3D+) convexo que contiene todos los puntos. Tras construirla con `points`, expone el resultado como atributos: `.vertices` son los indices de los puntos que forman el casco (en 2D, en orden antihorario), `.simplices` son las facetas (aristas en 2D, triangulos en 3D), `.area` mide el perimetro en 2D o la superficie en 3D, y `.volume` mide el area en 2D o el volumen en 3D. Sirve para hallar el **contorno externo** de una nube y el area o volumen que ocupa.

> Cuidado con la nomenclatura dimensional: en 2D `.volume` es el **area** encerrada y `.area` es el **perimetro**. En 3D `.volume` es el volumen y `.area` la superficie. SciPy nombra siempre el atributo por su rol N-dimensional, no por el del plano.

## Constructor

```python
scipy.spatial.ConvexHull(
    points,               # array_like (n, ndim): n puntos en ndim dimensiones
    incremental=False,    # bool: permitir add_points despues (build incremental)
    qhull_options=None,   # str | None: opciones crudas para Qhull (p.ej. 'QJ')
)                          # -> objeto ConvexHull con vertices/simplices/area/volume
```

## Atributos y metodos principales

| Miembro | Tipo | Significado |
|---------|------|-------------|
| `hull.vertices` | `ndarray` | Indices de los puntos del casco (2D: antihorario) |
| `hull.simplices` | `ndarray (nfacet, ndim)` | Indices de los puntos de cada faceta |
| `hull.area` | `float` | Perimetro en 2D / superficie en 3D |
| `hull.volume` | `float` | Area en 2D / volumen en 3D |
| `hull.points` | `ndarray` | Los puntos de entrada |
| `hull.neighbors` | `ndarray` | Facetas vecinas de cada faceta |
| `hull.equations` | `ndarray` | Ecuaciones `[normal, offset]` de cada hiperplano-faceta |
| `hull.add_points(pts)` | metodo | Anade puntos (requiere `incremental=True`) |

## Parametros en detalle

### `points`

Array `(n, ndim)`. Qhull soporta 2D, 3D y dimensiones mayores. Los puntos interiores se ignoran en el casco pero cuentan para `points`. Si los puntos son casi coplanares/colineales, Qhull puede fallar por precision; ahi ayuda `qhull_options='QJ'` (joggle, perturbacion minima).

### `incremental`

Con `True` se puede llamar a `add_points` despues para ampliar el casco sin reconstruir desde cero; a cambio, algunos atributos derivados se recalculan.

### `qhull_options`

Cadena con opciones nativas de Qhull. Las mas usadas: `'QJ'` (joggle ante degeneracion) y `'Qt'` (triangular la salida). Solo necesarias en casos degenerados.

## Casos de uso

### Contorno y area de una nube 2D

```python
import numpy as np
from scipy.spatial import ConvexHull

pts = np.random.rand(30, 2)
hull = ConvexHull(pts)               # construir el casco

hull.vertices                        # indices del contorno (antihorario)
hull.volume                          # AREA encerrada (en 2D)
hull.area                            # PERIMETRO (en 2D)
```

### Cerrar el poligono para dibujarlo

```python
contorno = pts[hull.vertices]                 # puntos del borde en orden
cerrado = np.vstack([contorno, contorno[0]])  # repetir el primero para cerrar
# plt.plot(cerrado[:, 0], cerrado[:, 1])
```

### Volumen ocupado en 3D

```python
p3 = np.random.rand(50, 3)
h3 = ConvexHull(p3)
h3.volume                            # volumen del poliedro
h3.area                              # superficie exterior
h3.simplices.shape                   # (nfacetas, 3): triangulos del casco
```

### Construccion incremental

```python
h = ConvexHull(pts[:20], incremental=True)
h.add_points(pts[20:])               # ampliar con mas puntos
h.close()                            # liberar el estado incremental
```

## Buenas practicas

1. Recuerda la convencion dimensional: en 2D usa `.volume` para el **area** y `.area` para el **perimetro**.
2. Para dibujar el contorno 2D, repite el primer vertice al final para cerrar el poligono.
3. Ante puntos colineales/coplanares o duplicados que rompen Qhull, prueba `qhull_options='QJ'`.
4. Usa `incremental=True` solo si realmente anadiras puntos despues; tiene sobrecoste.
5. Para saber si un punto esta dentro del casco, evalua el signo de `equations @ [punto, 1]` o usa una triangulacion de Delaunay.

## Errores comunes

| Error | Causa | Solucion |
|-------|-------|----------|
| `QhullError: ... is flat` | Puntos colineales (2D) o coplanares (3D) | Anadir `qhull_options='QJ'` o aportar mas dispersion |
| Confundir `area` y `volume` en 2D | Convencion N-dimensional de los atributos | `volume`=area, `area`=perimetro en 2D |
| Poligono "abierto" al graficar | No se cerro el contorno | Repetir `contorno[0]` al final |
| `add_points` lanza error | Casco no creado con `incremental=True` | Construir con `incremental=True` |
| `vertices` no luce ordenado en 3D | El orden antihorario solo aplica en 2D | En 3D usar `simplices` para las caras |

## Limitaciones

- Solo calcula la envolvente **convexa**; para contornos concavos (alpha shapes) hace falta otra tecnica.
- Sensible a degeneraciones numericas (colinealidad/coplanaridad); puede requerir joggle.
- El orden antihorario de `vertices` esta garantizado solo en **2D**.
- No clasifica directamente puntos dentro/fuera; eso se deriva de `equations` o de Delaunay.

## Notas relacionadas

- [[Delaunay]]
- [[KDTree]]
- [[scipy.spatial.distance]]
