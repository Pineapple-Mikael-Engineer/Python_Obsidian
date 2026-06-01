---
title: Axes3D.scatter — Nube de puntos 3D (dispersión)
aliases:
  - scatter3D
  - scatter 3d
  - dispersion 3d
  - nube de puntos 3d

tags:
  - matplotlib
  - api/metodo
  - plot/3d

# --- Clasificación ---
lib: matplotlib
obj: Axes3D
tipo: metodo

# --- Comportamiento ---
retorna: Path3DCollection
muta_estado: true

# --- Dependencias ---
requiere:
  - axes3d

draft: false
---

# Axes3D.scatter — Nube de puntos 3D (dispersión)

## Firma de la función

```python
Axes3D.scatter(
    xs, ys, zs=0,
    *,
    s=None, c=None, marker=None,
    cmap=None, norm=None,
    vmin=None, vmax=None,
    depthshade=True, alpha=None,
    **kwargs
)  # -> Path3DCollection
```

Dibuja una **nube de puntos en el espacio**: cada terna `(xs[i], ys[i], zs[i])` es un punto suelto. Es el equivalente 3D del `scatter` 2D y comparte casi toda su API. El parámetro `c` puede mapear una **4ª variable** a color (densidad, clase, magnitud), convirtiendo el gráfico en una visualización de cuatro dimensiones. Requiere un `Axes3D` (ver [[axes3d]]), que se obtiene con `ax = fig.add_subplot(projection='3d')`; muta ese Axes añadiendo la colección de puntos.

## Valor de retorno

| Entrada | Retorno | Ejemplo |
|---------|---------|---------|
| `xs, ys, zs` 1D de igual longitud | `Path3DCollection` | `pts = ax.scatter(xs, ys, zs)` |
| con `c=valores` + `cmap` | `Path3DCollection` coloreado por valor | `ax.scatter(xs, ys, zs, c=w, cmap='viridis')` |
| con `s=tamaños` | `Path3DCollection` con marcadores variables | `ax.scatter(xs, ys, zs, s=areas)` |

```python
pts = ax.scatter(xs, ys, zs, c=w, cmap='plasma')
type(pts)        # → <class 'mpl_toolkits.mplot3d.art3d.Path3DCollection'>
fig.colorbar(pts)   # el retorno alimenta la barra de color de la 4ª variable
```

## Formas básicas de llamada

| Llamada | Efecto |
|---------|--------|
| `ax.scatter(xs, ys, zs)` | nube simple, color y tamaño por defecto |
| `ax.scatter(xs, ys, zs, c='red')` | todos los puntos rojos |
| `ax.scatter(xs, ys, zs, c=w, cmap='viridis')` | color según la 4ª variable `w` |
| `ax.scatter(xs, ys, zs, s=50)` | marcadores de área 50 pt² |
| `ax.scatter(xs, ys, zs, marker='^')` | marcadores en triángulo |

## Parámetros en detalle

### `xs`, `ys`, `zs`

Las tres coordenadas de los puntos, como secuencias 1D de **igual longitud**. A diferencia de superficies y mallas, aquí no se necesitan rejillas 2D: cada índice define un punto independiente.

```python
import numpy as np
n = 200
xs = np.random.randn(n)
ys = np.random.randn(n)
zs = np.random.randn(n)
ax.scatter(xs, ys, zs)
```

### `c` (color / 4ª variable)

Acepta un color único (`'red'`) o un **array de valores** que se mapea con `cmap` a colores. Esto permite codificar una cuarta dimensión sobre los puntos del espacio 3D.

```python
w = xs**2 + ys**2 + zs**2          # magnitud como 4ª variable
ax.scatter(xs, ys, zs, c=w, cmap='coolwarm')   # color por magnitud
```

### `s` (tamaño)

Tamaño del marcador en puntos² (`area`). Escalar para todos, o array para tamaños por punto (codifica otra variable mediante el área).

```python
ax.scatter(xs, ys, zs, s=20)                 # tamaño fijo
ax.scatter(xs, ys, zs, s=100 * np.abs(zs))   # área proporcional a |z|
```

### `marker`, `depthshade`, `alpha`

`marker` cambia la forma (`'o'`, `'^'`, `'s'`, `'*'`...). `depthshade=True` atenúa los puntos lejanos para dar sensación de profundidad; ponlo en `False` para color uniforme. `alpha` controla la transparencia, útil con muchos puntos solapados.

```python
ax.scatter(xs, ys, zs, marker='^', depthshade=False, alpha=0.6)
```

## Casos de uso

```python
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D   # registra la proyección '3d'

n = 500
xs, ys, zs = np.random.randn(3, n)
w = np.sqrt(xs**2 + ys**2 + zs**2)        # 4ª variable

fig = plt.figure(figsize=(7, 5))
ax = fig.add_subplot(projection='3d')      # imprescindible: Axes3D
pts = ax.scatter(xs, ys, zs, c=w, cmap='viridis', s=15)
fig.colorbar(pts, shrink=0.6, label="radio")
ax.view_init(elev=25, azim=45)
# → nube esférica coloreada por distancia al origen
```

```python
# Clases discretas con marcadores y colores distintos
ax.scatter(xa, ya, za, c='tab:blue', marker='o', label='A')
ax.scatter(xb, yb, zb, c='tab:red',  marker='^', label='B')
ax.legend()
```

## Buenas prácticas

1. Crea el `Axes3D` con `ax = fig.add_subplot(projection='3d')` antes de dibujar.
2. Guarda el retorno (`pts = ax.scatter(...)`) cuando uses `c=array` para pasar `pts` a `fig.colorbar`.
3. Usa `c` como cuarta dimensión solo cuando la magnitud aporte información; si no, un color fijo es más limpio.
4. Baja `alpha` y/o `s` con miles de puntos para mitigar el solapamiento.
5. Ajusta la cámara con `view_init` para revelar la estructura espacial de la nube.

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| Puntos planos en z=0 | se omitió `zs` (queda en 0) | pasar las tres coordenadas `xs, ys, zs` |
| `c` no colorea con cmap | se pasó un color válido, no un array | usar un array numérico en `c` junto a `cmap` |
| Longitudes distintas | `xs, ys, zs` no coinciden en tamaño | igualar `len(xs) == len(ys) == len(zs)` |
| `'Axes' object has no attribute` 3D | el Axes no es `Axes3D` | crear con `projection='3d'` |
| Barra de color vacía | no se guardó el retorno de `scatter` | pasar `pts` a `fig.colorbar(pts)` |

## Notas relacionadas

- [[axes3d]]
- [[plot_surface]]
