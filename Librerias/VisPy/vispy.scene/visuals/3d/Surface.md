---
title: Surface — superficie z=f(x,y) en grid regular
aliases:
  - Surface
  - SurfacePlot
  - vispy surface
tags:
  - vispy
  - api/clase
  - scene/visuals
lib: vispy
mod: vispy.scene.visuals
tipo: clase
retorna: SurfacePlot
requiere:
  - SceneCanvas
  - ViewBox
  - TurntableCamera
draft: false
---

# Surface — superficie z=f(x,y) en grid regular

`scene.visuals.SurfacePlot` renderiza una superficie 3D definida como una funcion de dos
variables sobre un grid regular: `z = f(x, y)`. Es la alternativa mas rapida y directa a
[[Mesh]] cuando los datos provienen de una matriz 2D: funciones matematicas, mapas de elevacion
(DEM), resultados de simulacion en grid cartesiano o espectros de frecuencia.

## Importacion

```python
from vispy import scene, app
import vispy
vispy.use('pyqt5')

surf = scene.visuals.SurfacePlot(...)
```

## Constructor / Firma

```python
scene.visuals.SurfacePlot(
    z=None,          # array 2D (rows, cols) float32 — valores de altura
    x=None,          # array 1D (cols,) o 2D (rows, cols) — coordenadas X
    y=None,          # array 1D (rows,) o 2D (rows, cols) — coordenadas Y
    shading='smooth',  # 'smooth' | 'flat' | None
    color=(0.5, 0.5, 1, 1),  # color uniforme RGBA
    vertex_colors=None,  # array (rows*cols, 4) float32 — color por vertice
    parent=None,
)
```

## Parametros clave

| Parametro | Tipo | Descripcion |
|-----------|------|-------------|
| `z` | `(rows, cols) float32` | Altura de la superficie; dimensiones = numero de puntos del grid |
| `x` | `(cols,)` o `(rows, cols)` | Coordenadas X del grid; opcional (por defecto 0..cols-1) |
| `y` | `(rows,)` o `(rows, cols)` | Coordenadas Y del grid; opcional (por defecto 0..rows-1) |
| `shading` | str \| None | Modo de iluminacion: `'smooth'`, `'flat'` o `None` |
| `color` | RGBA / str | Color uniforme de la superficie |
| `vertex_colors` | `(rows*cols, 4) float32` | Color por vertice; debe ser flat (aplanado del grid) |

La triangulacion del grid se genera automaticamente internamente: no es necesario definir `faces`.

## Casos de uso

### Funcion matematica basica

```python
import vispy
vispy.use('pyqt5')
from vispy import scene, app
import numpy as np

canvas = scene.SceneCanvas(keys='interactive', show=True, size=(800, 600))
view = canvas.central_widget.add_view()
view.camera = 'turntable'

xs = np.linspace(-5, 5, 100)
ys = np.linspace(-5, 5, 100)
X, Y = np.meshgrid(xs, ys)
Z = np.sin(np.sqrt(X**2 + Y**2)).astype('float32')

surf = scene.visuals.SurfacePlot(
    z=Z,
    x=xs,
    y=ys,
    shading='smooth',
    color=(0.3, 0.6, 0.9, 1.0),
    parent=view.scene,
)
app.run()
```

### Mapa de elevacion (DEM)

```python
import numpy as np

# Simular un terreno con ruido
rng = np.random.default_rng(42)
elevacion = rng.random((256, 256)).astype('float32') * 500  # metros

lon = np.linspace(-70.0, -68.0, 256)  # grados
lat = np.linspace(-33.0, -31.0, 256)

surf = scene.visuals.SurfacePlot(
    z=elevacion,
    x=lon,
    y=lat,
    shading='flat',
    color='lightgray',
    parent=view.scene,
)
```

### Colorear la superficie segun z

```python
from vispy.color import get_colormap

Z = np.sin(np.sqrt(X**2 + Y**2)).astype('float32')

# Normalizar z al rango [0, 1] para el colormap
z_norm = (Z - Z.min()) / (Z.max() - Z.min())
cmap = get_colormap('viridis')
colors = cmap.map(z_norm.ravel()).astype('float32')  # (rows*cols, 4)

surf = scene.visuals.SurfacePlot(
    z=Z,
    vertex_colors=colors,
    shading='smooth',
    parent=view.scene,
)
```

### Actualizar en animacion

```python
t = 0.0

def on_timer(event):
    global t
    t += 0.05
    Z_nuevo = np.sin(np.sqrt(X**2 + Y**2) - t).astype('float32')
    surf.set_data(z=Z_nuevo)
    canvas.update()

timer = app.Timer(interval=1/60, connect=on_timer, start=True)
```

## Metodos y atributos

| Nombre | Descripcion |
|--------|-------------|
| `.set_data(z, x, y, vertex_colors, ...)` | Actualiza la superficie sin recrear el objeto |
| `.transform` | `MatrixTransform` para trasladar, rotar o escalar la superficie |
| `.visible` | `bool` — muestra u oculta |
| `.shading` | Propiedad lectura/escritura del modo de iluminacion |

## SurfacePlot vs Mesh

[[Mesh]] es mas flexible pero exige definir `vertices` y `faces` manualmente. `SurfacePlot`
es mas conveniente para grids regulares porque la triangulacion es automatica.

| Situacion | Visual recomendado |
|-----------|-------------------|
| Funcion z=f(x,y) en grid cartesiano | `SurfacePlot` |
| Geometria arbitraria (STL, OBJ, esferas) | `Mesh` |
| Grid con huecos o mascaras | `Mesh` (mas control) |
| Animacion de ondas / mapas de calor 3D | `SurfacePlot` |

## Errores comunes

| Error | Causa | Solucion |
|-------|-------|----------|
| Superficie plana / invisible | `z` en `float64` con valores muy pequenos | `z.astype('float32')`, verificar escala |
| `IndexError` en `vertex_colors` | Tamano no coincide con `rows*cols` | `colors = cmap.map(z_norm.ravel())` — ravel antes de mapear |
| Superficie sin volumen aparente | Camera demasiado lejana o sin `view.camera.set_range()` | Llamar `view.camera.set_range()` tras crear el visual |
| `shading` no visible | `color=(r,g,b,a)` demasiado oscuro o sin luz | Cambiar color o probar `shading=None` |

## Notas relacionadas

- [[vispy.scene/visuals/3d/index|visuals 3D]] — contexto del submodulo
- [[Mesh]] — malla triangular arbitraria; usar cuando el grid no es regular
- [[Volume]] — para datos volumetricos 3D (CT, MRI, simulaciones CFD)
- [[TurntableCamera]] — camara orbital para inspeccionar la superficie
