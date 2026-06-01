---
title: Axes3D — La región de ploteo 3D de Matplotlib
aliases:
  - Axes3D
  - axes3d
  - ejes 3d
  - region de ploteo 3d

tags:
  - matplotlib
  - api/clase
  - plot/3d

# --- Clasificación ---
lib: matplotlib
obj: Axes3D
tipo: clase

# --- Comportamiento ---
retorna: Axes3D
muta_estado: true

# --- Dependencias ---
requiere:
  - concepto_figure_axes
  - Axes

draft: false
---

# Axes3D — La región de ploteo 3D de Matplotlib

## Qué es

Un `Axes3D` es **la versión tridimensional de un Axes**: un sistema de coordenadas con tres ejes (X, Y, Z) donde se dibujan superficies, mallas, nubes de puntos y curvas en el espacio. Hereda casi toda la API de [[Axes]] (títulos, etiquetas, leyenda, límites) y añade un eje Z y métodos gráficos propios del 3D.

Pertenece al toolkit `mpl_toolkits.mplot3d`, una extensión incluida en Matplotlib pero no cargada por defecto. Mentalmente: si `Axes` es una hoja con coordenadas X/Y, `Axes3D` es esa misma hoja proyectando un volumen X/Y/Z que se observa desde un punto de cámara configurable.

## Cómo se obtiene

La vía idiomática es pasar `projection='3d'` al crear el subgrafo desde un `Figure`. El import de `mpl_toolkits.mplot3d` registra la proyección 3D; en versiones modernas de Matplotlib basta `projection='3d'` sin import explícito, pero conviene documentarlo por compatibilidad.

```python
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D   # registra la proyección '3d'

fig = plt.figure()
ax = fig.add_subplot(projection='3d')     # ax es un Axes3D
type(ax)        # → <class 'mpl_toolkits.mplot3d.axes3d.Axes3D'>
```

| Forma | Resultado | Acceso |
|-------|-----------|--------|
| `fig.add_subplot(projection='3d')` | un `Axes3D` suelto | `ax.plot_surface(...)` |
| `fig.add_subplot(2, 2, 1, projection='3d')` | `Axes3D` en rejilla 2x2, celda 1 | `ax.scatter(...)` |
| `plt.subplots(subplot_kw={'projection':'3d'})` | `Figure` + un `Axes3D` | `ax.plot3D(...)` |
| `fig.add_axes(rect, projection='3d')` | `Axes3D` en posición manual | `ax.plot_wireframe(...)` |

Casi nunca se instancia `Axes3D(...)` directamente: siempre se obtiene desde un `Figure` con la proyección 3D.

## Métodos clave

### Métodos gráficos (crean Artists 3D)

| Método | Dibuja | Retorna |
|--------|--------|---------|
| [[plot_surface]] | superficie continua sobre malla X,Y,Z | `Poly3DCollection` |
| `plot_wireframe` | malla de alambre (sin relleno) | `Line3DCollection` |
| `scatter` | nube de puntos 3D | `Path3DCollection` |
| `plot3D` / `plot` | curva/línea en el espacio | lista de `Line3D` |
| `contour3D` / `contour` | contornos proyectados en 3D | `QuadContourSet` |
| `contourf3D` | contornos rellenos en 3D | `QuadContourSet` |
| `bar3d` | barras volumétricas | `Poly3DCollection` |
| `quiver` | campo de vectores 3D | `Line3DCollection` |

### Métodos de formato (configuran el Axes3D)

| Método | Controla | Ejemplo |
|--------|----------|---------|
| `ax.set_xlabel` / `ax.set_ylabel` | etiquetas X, Y | `ax.set_xlabel("x")` |
| `ax.set_zlabel` | etiqueta del eje Z (propio del 3D) | `ax.set_zlabel("altura")` |
| `ax.set_xlim` / `ax.set_ylim` | límites X, Y | `ax.set_xlim(-5, 5)` |
| `ax.set_zlim` | límites del eje Z (propio del 3D) | `ax.set_zlim(0, 10)` |
| `ax.view_init` | ángulo de cámara (elevación, azimut) | `ax.view_init(elev=30, azim=45)` |
| `ax.set_title` | título del subgrafo | `ax.set_title("Superficie")` |
| `ax.set_box_aspect` | proporción de la caja 3D | `ax.set_box_aspect((1,1,1))` |

El control de cámara con `view_init(elev, azim)` es exclusivo del 3D: `elev` es el ángulo de elevación sobre el plano X-Y y `azim` la rotación azimutal alrededor del eje Z. Todo lo demás (leyenda, grid, guardado vía `fig.savefig`) sigue el mismo reparto de responsabilidades que en [[concepto_figure_axes]].

## Atributos

| Atributo | Contiene | Tipo |
|----------|----------|------|
| `ax.zaxis` | el eje Z individual | `Axis` |
| `ax.xaxis` / `ax.yaxis` | los ejes X e Y | `Axis` |
| `ax.collections` | superficies, mallas, scatters 3D | lista de `Collection` |
| `ax.lines` | curvas dibujadas con `plot3D` | lista de `Line3D` |
| `ax.figure` | el `Figure` contenedor | `Figure` |
| `ax.elev` / `ax.azim` | ángulos actuales de cámara | `float` |

```python
ax = fig.add_subplot(projection='3d')
ax.plot3D([0, 1], [0, 1], [0, 1])
len(ax.lines)        # → 1
ax.elev               # → 30.0  (elevación por defecto)
```

## Ejemplo de ciclo de vida

```python
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D   # registra '3d'

x = np.linspace(-5, 5, 60)
y = np.linspace(-5, 5, 60)
X, Y = np.meshgrid(x, y)                  # mallas 2D
Z = np.sin(np.sqrt(X**2 + Y**2))          # alturas

fig = plt.figure(figsize=(7, 5))
ax = fig.add_subplot(projection='3d')     # crear Axes3D
ax.plot_surface(X, Y, Z, cmap='viridis')  # dibujar (muta el Axes3D)
ax.set_xlabel("x")
ax.set_ylabel("y")
ax.set_zlabel("z")                        # etiqueta propia del 3D
ax.set_title("Sombrero mexicano")
ax.view_init(elev=35, azim=120)           # mover la cámara

fig.savefig("superficie3d.png")           # guardar (responsabilidad del Figure)
```

## Buenas prácticas

1. Importa `mpl_toolkits.mplot3d` aunque parezca opcional: garantiza que `projection='3d'` esté registrado en cualquier versión.
2. Crea siempre el `Axes3D` desde un `Figure` con `projection='3d'`; no instancies la clase a mano.
3. Genera las mallas X, Y con `np.meshgrid` antes de pasar a métodos de superficie/malla.
4. Ajusta la cámara con `view_init(elev, azim)` para mostrar la cara más informativa de la superficie.
5. Fija `set_zlim` y `set_box_aspect` cuando la escala de Z distorsione la lectura del volumen.

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| `Unknown projection '3d'` | no se importó `mpl_toolkits.mplot3d` (versión antigua) | añadir `from mpl_toolkits.mplot3d import Axes3D` |
| `ax.set_zlabel` no existe | `ax` es un `Axes` 2D, no `Axes3D` | crear con `projection='3d'` |
| Superficie plana o vacía | `X`, `Y`, `Z` no son mallas 2D coherentes | generar con `np.meshgrid` y mismas dimensiones |
| Vista poco clara | cámara en ángulo por defecto | usar `view_init(elev, azim)` |
| `plot_surface` con 1D | espera arrays 2D | reformar a malla antes de llamar |

## Notas relacionadas

- [[concepto_figure_axes]]
- [[Axes]]
- [[plot_surface]]
