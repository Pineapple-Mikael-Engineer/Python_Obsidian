---
title: KDTree — arbol k-d para vecinos mas cercanos
aliases:
  - KDTree
  - scipy.spatial.KDTree
  - cKDTree
  - arbol k-d
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

# KDTree — arbol k-d para vecinos mas cercanos

Clase que construye un **arbol k-d** (k-dimensional) sobre una nube de puntos para resolver consultas de **vecinos mas cercanos** de forma eficiente: tras un coste de construccion `O(n log n)`, cada consulta es `O(log n)` amortizado en dimensiones bajas, frente al `O(n)` de la busqueda por fuerza bruta. Se instancia con los puntos `data` y luego se consulta con metodos: `.query(x, k)` devuelve los `k` vecinos mas cercanos y sus distancias; `.query_ball_point(x, r)` devuelve todos los puntos dentro de un radio `r`; `.query_pairs(r)` lista parejas internas a distancia menor que `r`; y `.count_neighbors` cuenta vecinos entre dos arboles. Es la herramienta de referencia para vecindad en mallas, nubes de puntos y problemas de proximidad.

> `cKDTree` era la implementacion en C (rapida) frente a la antigua en Python. Desde SciPy moderno `KDTree` **es** esa implementacion rapida y `cKDTree` queda como **alias** equivalente; usa `KDTree` directamente.

## Constructor

```python
scipy.spatial.KDTree(
    data,                 # array_like (n, m): n puntos en m dimensiones
    leafsize=10,          # int: puntos por hoja; afecta velocidad, no resultado
    compact_nodes=True,   # bool: nodos compactos -> arbol mas equilibrado
    copy_data=False,      # bool: copiar data para no depender del array original
    balanced_tree=True,   # bool: usar mediana (mejor consulta, build mas caro)
    boxsize=None,         # array_like | None: dominio periodico (toroidal) por eje
)                          # -> objeto KDTree consultable
```

## Metodos y atributos principales

| Miembro | Tipo | Significado |
|---------|------|-------------|
| `tree.query(x, k=1)` | metodo | `k` vecinos mas cercanos a `x`: devuelve `(distancias, indices)` |
| `tree.query_ball_point(x, r)` | metodo | Indices de todos los puntos a distancia ≤ `r` de `x` |
| `tree.query_ball_tree(other, r)` | metodo | Parejas a ≤ `r` entre este arbol y `other` |
| `tree.query_pairs(r)` | metodo | Conjunto de parejas internas a distancia ≤ `r` |
| `tree.count_neighbors(other, r)` | metodo | Numero de parejas a ≤ `r` entre dos arboles |
| `tree.sparse_distance_matrix(other, max_distance)` | metodo | Matriz dispersa de distancias hasta `max_distance` |
| `tree.data` | `ndarray` | Los puntos almacenados |
| `tree.n`, `tree.m` | `int` | Numero de puntos y dimensiones |

## Parametros en detalle

### `data`

Array `(n, m)` de `n` puntos en `m` dimensiones. El arbol particiona recursivamente el espacio por ejes alternados. Funciona bien con `m` pequeño-moderado; en dimension muy alta la ganancia frente a fuerza bruta se degrada ("maldicion de la dimensionalidad").

### `leafsize`

Numero maximo de puntos por hoja. No cambia el **resultado**, solo el rendimiento: valores grandes aceleran la construccion pero ralentizan la consulta y viceversa. El default `10` suele ir bien.

### `boxsize`

Si se indica, el espacio es **periodico** (toroidal): la coordenada de cada eje se envuelve modulo `boxsize`. Util en simulaciones con condiciones de contorno periodicas.

### `query(x, k, p, distance_upper_bound)`

`k` es cuantos vecinos pedir; `p` el orden de la metrica Minkowski (`p=2` euclidea, `p=1` Manhattan, `p=np.inf` Chebyshev); `distance_upper_bound` descarta vecinos mas lejanos. Con `k>1` cada salida es un array por consulta; los huecos sin vecino devuelven distancia `inf` e indice `n`.

## Casos de uso

### k vecinos mas cercanos

```python
import numpy as np
from scipy.spatial import KDTree

pts = np.random.rand(1000, 2)        # nube 2D
tree = KDTree(pts)                   # construir el arbol

dist, idx = tree.query([0.5, 0.5], k=3)   # 3 vecinos del centro
idx                                  # indices de los 3 mas cercanos
dist                                 # sus distancias (orden ascendente)
```

### Todos los puntos dentro de un radio

```python
vecinos = tree.query_ball_point([0.5, 0.5], r=0.1)
len(vecinos)                         # cuantos puntos caen en el circulo r=0.1
```

### Parejas internas cercanas

```python
pares = tree.query_pairs(r=0.05)     # set de (i, j) a distancia < 0.05
n = tree.count_neighbors(tree, r=0.05)   # conteo de parejas (incluye i==j)
```

### Consulta vectorizada en bloque

```python
consulta = np.random.rand(50, 2)     # 50 puntos a la vez
dist, idx = tree.query(consulta, k=1)   # vecino mas cercano de cada uno
idx.shape                            # → (50,)
```

### Metrica distinta de la euclidea

```python
dist, idx = tree.query([0.5, 0.5], k=1, p=1)   # vecino en distancia Manhattan
```

## Buenas practicas

1. Construye el arbol **una vez** y reutilizalo para muchas consultas; ahi esta la ganancia frente a fuerza bruta.
2. Vectoriza pasando un array `(q, m)` de consultas a `.query` en lugar de un bucle Python.
3. Para emparejar dos nubes distintas usa `query_ball_tree`/`count_neighbors` entre dos arboles.
4. En dominios periodicos define `boxsize` en vez de duplicar puntos en los bordes.
5. Si la dimension `m` es muy alta, evalua fuerza bruta o metodos aproximados: el k-d deja de ganar.

## Errores comunes

| Error | Causa | Solucion |
|-------|-------|----------|
| Indice `== n` y distancia `inf` | No habia suficientes vecinos (con `distance_upper_bound`) | Subir el bound o pedir menos `k` |
| Consulta lenta pese al arbol | Dimension alta o `leafsize` mal ajustado | Reducir dimension o probar otro `leafsize` |
| Resultados fuera del dominio periodico | `boxsize` no definido | Pasar `boxsize` con el periodo por eje |
| `ValueError` por shape | `x` con dimension distinta de `data` | Igualar `m` entre consulta y puntos |
| Esperar lista ordenada en `query_ball_point` | Devuelve indices sin orden de distancia | Ordenar a mano si hace falta |

## Limitaciones

- El rendimiento se degrada en **dimension alta**; deja de superar a la fuerza bruta.
- Es una estructura **estatica**: insertar o borrar puntos exige reconstruir el arbol.
- Solo soporta metricas Minkowski (`p`); para distancias arbitrarias usa funciones de distancia directas.
- Para conjuntos enormes con consultas masivas, valora indices aproximados externos.

## Notas relacionadas

- [[scipy.spatial.distance]]
- [[Delaunay]]
- [[ConvexHull]]
