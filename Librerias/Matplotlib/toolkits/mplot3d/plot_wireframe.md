---
title: Axes3D.plot_wireframe — Superficie 3D como malla de alambre
aliases:
  - plot_wireframe
  - wireframe
  - malla de alambre
  - rejilla 3d

tags:
  - matplotlib
  - api/metodo
  - plot/3d

# --- Clasificación ---
lib: matplotlib
obj: Axes3D
tipo: metodo

# --- Comportamiento ---
retorna: Line3DCollection
muta_estado: true

# --- Dependencias ---
requiere:
  - axes3d
  - numpy.meshgrid

draft: false
---

# Axes3D.plot_wireframe — Superficie 3D como malla de alambre

## Firma de la función

```python
Axes3D.plot_wireframe(
    X, Y, Z,
    *,
    rcount=50, ccount=50,
    rstride=1, cstride=1,
    **kwargs
)  # -> Line3DCollection
```

Dibuja una superficie como **malla de alambre**: solo las líneas de la rejilla que conectan los puntos `(X, Y, Z)`, sin relleno de las celdas. A diferencia de [[plot_surface]] (que rellena cada celda con un parche poligonal opaco), aquí se ve a través de la superficie, lo que resulta más ligero y útil para inspeccionar la estructura. Requiere un `Axes3D` (ver [[axes3d]]), que se crea con `ax = fig.add_subplot(projection='3d')`; muta ese Axes añadiendo la colección de líneas.

## Valor de retorno

| Entrada | Retorno | Ejemplo |
|---------|---------|---------|
| mallas X, Y, Z 2D coherentes | `Line3DCollection` | `wire = ax.plot_wireframe(X, Y, Z)` |
| con `rstride=2, cstride=2` | `Line3DCollection` más espaciada | `ax.plot_wireframe(X, Y, Z, rstride=2, cstride=2)` |
| con `color='k'` | `Line3DCollection` de color uniforme | `ax.plot_wireframe(X, Y, Z, color='k')` |

```python
wire = ax.plot_wireframe(X, Y, Z, color='steelblue')
type(wire)        # → <class 'mpl_toolkits.mplot3d.art3d.Line3DCollection'>
wire.set_alpha(0.5)   # el retorno permite ajustar la colección a posteriori
```

## Formas básicas de llamada

| Llamada | Efecto |
|---------|--------|
| `ax.plot_wireframe(X, Y, Z)` | malla completa, una línea por fila y columna |
| `ax.plot_wireframe(X, Y, Z, rstride=2, cstride=2)` | una de cada 2 filas/columnas (más ligera) |
| `ax.plot_wireframe(X, Y, Z, rstride=0)` | solo líneas en una dirección (columnas) |
| `ax.plot_wireframe(X, Y, Z, cstride=0)` | solo líneas en la otra dirección (filas) |
| `ax.plot_wireframe(X, Y, Z, color='k', linewidth=0.5)` | rejilla negra fina |

## Parámetros en detalle

### `X`, `Y`, `Z`

Las tres mallas 2D que definen la superficie. `X` e `Y` suelen venir de `np.meshgrid` y `Z` es la altura en cada punto. Las tres deben ser **arrays 2D de la misma forma**.

```python
import numpy as np
x = np.linspace(-3, 3, 40)
y = np.linspace(-3, 3, 40)
X, Y = np.meshgrid(x, y)        # X, Y: (40, 40)
Z = np.exp(-(X**2 + Y**2))      # Z:    (40, 40)
ax.plot_wireframe(X, Y, Z)
```

### `rstride`, `cstride` (o `rcount`, `ccount`)

Controlan el **espaciado de los hilos**: cada cuántas filas/columnas se traza una línea. Valores altos dibujan menos líneas (rejilla más abierta, más rápida). Un valor de `0` en uno de ellos suprime las líneas en esa dirección, dejando solo "peines" en la otra.

| Parámetro | Significado | Efecto |
|-----------|-------------|--------|
| `rstride=1, cstride=1` | todas las filas/columnas | rejilla densa, máximo detalle |
| `rstride=3, cstride=3` | una de cada 3 | rejilla más abierta y rápida |
| `rstride=0` | sin líneas de filas | solo hilos verticales (columnas) |
| `cstride=0` | sin líneas de columnas | solo hilos horizontales (filas) |

### `color`, `linewidth`, `alpha`

Estilo de los hilos: `color` da el color uniforme de toda la malla, `linewidth` el grosor y `alpha` la transparencia. No admite `cmap` para colorear por altura como hace `plot_surface`.

```python
ax.plot_wireframe(X, Y, Z, color='darkred', linewidth=0.4, alpha=0.8)
```

## Casos de uso

```python
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D   # registra la proyección '3d'

x = np.linspace(-5, 5, 60)
y = np.linspace(-5, 5, 60)
X, Y = np.meshgrid(x, y)
Z = np.sin(np.sqrt(X**2 + Y**2))

fig = plt.figure(figsize=(7, 5))
ax = fig.add_subplot(projection='3d')      # imprescindible: Axes3D
ax.plot_wireframe(X, Y, Z, rstride=3, cstride=3, color='teal')
ax.set_zlabel("z")
ax.view_init(elev=40, azim=-60)
# → rejilla del "sombrero mexicano", se ve a través de ella
```

```python
# Comparar estructura sin ocultar el fondo: wireframe abierto
ax.plot_wireframe(X, Y, Z, rstride=5, cstride=5, linewidth=0.6)
# → malla ligera, ideal para superponer sobre otra superficie
```

## Buenas prácticas

1. Crea siempre el `Axes3D` con `ax = fig.add_subplot(projection='3d')` antes de llamar al método.
2. Genera `X`, `Y` con `np.meshgrid` y calcula `Z` vectorizado sobre esas mallas.
3. Sube `rstride`/`cstride` (o baja `rcount`/`ccount`) en mallas densas para no saturar de líneas.
4. Usa wireframe cuando necesites ver a través de la superficie o superponerla a otra capa.
5. Combina con `view_init` para presentar la malla desde el ángulo más legible.

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| `'Axes' object has no attribute 'plot_wireframe'` | el Axes no es 3D | crear con `projection='3d'` |
| `Argument Z must be 2-dimensional` | `Z` es 1D | construir `Z` sobre mallas de `np.meshgrid` |
| Formas incompatibles X/Y/Z | no tienen la misma forma 2D | verificar `X.shape == Y.shape == Z.shape` |
| `cmap` no colorea la malla | wireframe no soporta mapa por altura | usar `plot_surface` si se quiere color por Z |
| Maraña de líneas ilegible | malla demasiado densa | subir `rstride`/`cstride` |

## Notas relacionadas

- [[axes3d]]
- [[plot_surface]]
