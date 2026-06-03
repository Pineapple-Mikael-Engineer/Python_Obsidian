---
title: scipy.spatial.distance — metricas de distancia entre puntos
aliases:
  - scipy.spatial.distance
  - pdist
  - cdist
  - squareform
tags:
  - scipy
  - api/submodulo
  - geometria-computacional
lib: scipy
tipo: submodulo
mod: scipy.spatial
requiere:
  - numpy
draft: false
---

# scipy.spatial.distance — metricas de distancia entre puntos

Submodulo que reune **funciones de distancia** entre vectores y entre conjuntos de puntos. Su nucleo son tres rutinas: `pdist(X)` calcula las distancias por pares **dentro** de un unico conjunto (devuelve un vector condensado), `cdist(XA, XB)` calcula las distancias **entre dos** conjuntos (devuelve una matriz rectangular) y `squareform` convierte el vector condensado en matriz cuadrada simetrica y viceversa. Ademas expone decenas de **metricas individuales** (`euclidean`, `cityblock`, `cosine`, `hamming`, `mahalanobis`, ...) que operan sobre dos vectores. La metrica se selecciona con el parametro `metric` (cadena o callable), lo que hace al submodulo la base de clustering, vecinos mas cercanos y matrices de similitud.

> Distincion clave: `pdist` trabaja con **un** conjunto (todas las parejas internas, sin repetir ni incluir la diagonal); `cdist` cruza **dos** conjuntos distintos. Para vecindad eficiente con muchos puntos, conviene un arbol espacial en lugar de materializar toda la matriz de distancias.

## Funciones principales

| Funcion | Entrada | Salida | Uso |
|---------|---------|--------|-----|
| `pdist(X, metric='euclidean')` | `X` `(m, n)`: m puntos en n-D | vector condensado `(m*(m-1)/2,)` | Distancias por pares internas |
| `cdist(XA, XB, metric='euclidean')` | `XA` `(mA, n)`, `XB` `(mB, n)` | matriz `(mA, mB)` | Distancias entre dos conjuntos |
| `squareform(X)` | vector condensado **o** matriz cuadrada | matriz **o** vector condensado | Convierte entre ambas formas |
| `euclidean(u, v)` | dos vectores | `float` | Distancia L2 puntual |
| `cdist(XA, XB, metric=fn)` | metrica callable `fn(u, v)` | matriz | Distancia personalizada |

## El parametro `metric`

Cadena que selecciona la distancia (igual para `pdist` y `cdist`); tambien acepta un callable `f(u, v) -> float`. Metricas comunes:

| `metric` | Formula / idea | Tipo de dato |
|----------|----------------|--------------|
| `'euclidean'` (default) | `sqrt(sum((u-v)^2))`, distancia L2 | Continuo |
| `'sqeuclidean'` | `sum((u-v)^2)`, L2 al cuadrado (mas rapida) | Continuo |
| `'cityblock'` | `sum(|u-v|)`, distancia Manhattan / L1 | Continuo |
| `'chebyshev'` | `max(|u-v|)`, distancia L-infinito | Continuo |
| `'minkowski'` | `(sum(|u-v|^p))^(1/p)`, parametro `p` | Continuo |
| `'cosine'` | `1 - (u.v)/(||u|| ||v||)`, distancia coseno | Vectores/direccion |
| `'correlation'` | `1 - corr(u, v)`, coseno centrado | Vectores |
| `'hamming'` | fraccion de componentes distintas | Categorico/binario |
| `'jaccard'` | disimilitud de conjuntos binarios | Binario |
| `'mahalanobis'` | distancia con inversa de covarianza `VI` | Continuo correlado |

Algunas metricas reciben parametros extra por keyword: `minkowski` usa `p=`, `mahalanobis` usa `VI=` (inversa de la matriz de covarianza), `seuclidean` usa `V=` (varianzas).

## Casos de uso

### Matriz de distancias dentro de un conjunto

```python
import numpy as np
from scipy.spatial.distance import pdist, squareform

X = np.array([[0, 0], [3, 0], [0, 4]])
d = pdist(X)                         # vector condensado: [3., 4., 5.]
M = squareform(d)                    # matriz simetrica 3x3 con diagonal 0
M[0, 2]                              # → 4.0  (distancia punto 0 ↔ punto 2)
```

### Distancias entre dos conjuntos (cruce)

```python
from scipy.spatial.distance import cdist

XA = np.array([[0, 0], [1, 1]])
XB = np.array([[0, 1], [2, 2], [5, 5]])
D = cdist(XA, XB)                    # matriz (2, 3)
D.shape                             # → (2, 3)
D.argmin(axis=1)                    # XB mas cercano a cada punto de XA
```

### Cambiar de metrica

```python
cdist(XA, XB, metric='cityblock')    # Manhattan en vez de euclidea
pdist(X, metric='cosine')            # disimilitud coseno entre filas
pdist(X, metric='minkowski', p=3)    # L3
```

### Metrica de Mahalanobis

```python
data = np.random.randn(100, 3)
VI = np.linalg.inv(np.cov(data, rowvar=False))   # inversa de covarianza
pdist(data, metric='mahalanobis', VI=VI)
```

### Metrica personalizada (callable)

```python
mi_dist = lambda u, v: np.abs(u - v).max()        # equivale a chebyshev
cdist(XA, XB, metric=mi_dist)
```

## Buenas practicas

1. Para alimentar clustering jerarquico, pasa el **vector condensado** de `pdist` directamente; no conviertas a matriz salvo que necesites indexar parejas concretas.
2. Usa `squareform` solo para inspeccionar o indexar; duplica memoria respecto al vector condensado.
3. Para comparar magnitudes prefiere `'sqeuclidean'` (sin raiz) cuando solo importa el **orden** de distancias: es mas rapida.
4. Estandariza o normaliza las features antes de distancias euclideas si las escalas difieren; o usa `seuclidean`/`mahalanobis`.
5. Para muchos puntos y solo vecinos cercanos, no materialices toda la matriz: usa un arbol espacial.

## Errores comunes

| Error | Causa | Solucion |
|-------|-------|----------|
| `ValueError: shapes ... not aligned` en cdist | `XA` y `XB` con distinto numero de columnas | Igualar la dimension n de ambos conjuntos |
| Tratar salida de `pdist` como matriz | `pdist` devuelve **vector condensado** | Aplicar `squareform` o indexar por formula de pareja |
| `squareform` no reconstruye | Pasar matriz no simetrica o con diagonal no nula | Garantizar matriz simetrica con ceros en la diagonal |
| `mahalanobis` lanza error | Falta `VI` (inversa de covarianza) | Pasar `VI=np.linalg.inv(cov)` |
| Resultado raro con `cosine` | Vectores nulos o sin normalizar | Filtrar filas cero; la metrica ya normaliza |

## Limitaciones

- `pdist`/`cdist` materializan **todas** las distancias: coste `O(m^2)` en memoria y tiempo, prohibitivo para millones de puntos.
- Las metricas operan sobre vectores numericos; datos mixtos exigen una metrica callable propia.
- No construyen indices espaciales; para consultas de vecindad repetidas usa un arbol k-d.

## Notas relacionadas

- [[KDTree]]
- [[ConvexHull]]
- [[Delaunay]]
