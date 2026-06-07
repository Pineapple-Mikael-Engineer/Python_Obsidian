---
title: vispy.scene/visuals/3d — visuals 3D de alto nivel
tags:
  - vispy
  - indice
draft: false
---

# vispy.scene/visuals/3d — visuals 3D

Los visuals 3D de VisPy permiten renderizar geometria, volumenes y superficies directamente
en la GPU mediante OpenGL. Los tres visuals de esta carpeta cubren los casos de uso centrales:
geometria triangulada arbitraria ([[Mesh]]), datos volumetricos con ray-casting ([[Volume]])
y funciones z=f(x,y) sobre grids regulares ([[Surface]]). Todos requieren un `ViewBox` con
camara 3D (tipicamente [[TurntableCamera]]) como contenedor.

## Ejemplo unificador

El patron minimo para cualquier visual 3D es identico: canvas → view → camera → visual.

```python
import vispy
vispy.use('pyqt5')
from vispy import scene, app
import numpy as np

canvas = scene.SceneCanvas(keys='interactive', show=True, size=(800, 600))
view = canvas.central_widget.add_view()
view.camera = 'turntable'   # orbita con drag del mouse

# --- Mesh: tetraedro simple ---
verts = np.array([[0,0,0],[1,0,0],[0.5,1,0],[0.5,0.5,1]], dtype='float32')
faces = np.array([[0,1,2],[0,1,3],[0,2,3],[1,2,3]], dtype='uint32')
mesh = scene.visuals.Mesh(vertices=verts, faces=faces,
                           color='cyan', shading='smooth',
                           parent=view.scene)

# --- Volume: cubo de ruido con MIP ---
vol_data = np.random.rand(64, 64, 64).astype('float32')
vol = scene.visuals.Volume(vol_data, clim=(0, 1), cmap='fire',
                            method='mip', parent=view.scene)

# --- Surface: onda sinusoidal ---
xs = np.linspace(-5, 5, 100)
ys = np.linspace(-5, 5, 100)
X, Y = np.meshgrid(xs, ys)
Z = np.sin(np.sqrt(X**2 + Y**2)).astype('float32')
surf = scene.visuals.SurfacePlot(z=Z, x=xs, y=ys,
                                  shading='smooth', parent=view.scene)

app.run()
```

> [!info] Backend obligatorio
> Siempre declarar el backend antes del primer import de scene:
> `import vispy; vispy.use('pyqt5')`.
> Sin esto el ejemplo puede fallar si el backend por defecto no esta instalado.

## Como se relacionan

Los tres visuals representan formas distintas de dato 3D. La eleccion depende del tipo
de dato de origen, no de la apariencia final deseada.

| Visual | Clase API | Dato de entrada | Caso tipico |
|--------|-----------|-----------------|-------------|
| [[Mesh]] | `scene.visuals.Mesh` | `(N,3) vertices` + `(M,3) faces` | Objetos STL/OBJ, geometria arbitraria |
| [[Volume]] | `scene.visuals.Volume` | `(D, H, W) float32` 3D array | CT/MRI, simulaciones CFD, atmosfera |
| [[Surface]] | `scene.visuals.SurfacePlot` | `(rows, cols) float32` Z + X/Y opcionales | z=f(x,y), mapas de elevacion, ondas |

### Tabla de decision rapida

| Situacion | Visual |
|-----------|--------|
| Tengo un archivo .stl o .obj | [[Mesh]] con `meshio`/`trimesh` |
| Tengo un escaneo CT o MRI | [[Volume]] con `method='mip'` o `'iso'` |
| Tengo datos en un grid regular z=f(x,y) | [[Surface]] |
| Quiero mostrar isosuperficies de un campo escalar | [[Volume]] con `method='iso'` |
| Necesito colorear la superficie segun z | [[Surface]] con `vertex_colors` |
| La geometria no es un grid ni un volumen | [[Mesh]] con vertices y faces manuales |

### Diferencias criticas

- **Mesh**: el usuario define la triangulacion completa (`vertices` + `faces`). Maxima
  flexibilidad; necesario para geometrias no estructuradas.
- **Volume**: opera sobre voxeles; el ray-casting se hace en el shader GLSL. No produce
  una malla superficial sino una proyeccion volumetrica. Requiere arrays 3D contiguos en
  memoria (`float32`, C-order).
- **Surface**: genera la triangulacion automaticamente a partir del grid 2D. Conveniente
  y rapido; no admite huecos ni topologia no regular.

## Notas

- [[Mesh]] — `scene.visuals.Mesh`: malla triangular 3D arbitraria
- [[Volume]] — `scene.visuals.Volume`: renderizado volumetrico con ray-casting
- [[Surface]] — `scene.visuals.SurfacePlot`: superficie z=f(x,y) en grid regular

## Notas relacionadas

- [[vispy.scene/visuals/2d/index|visuals 2D]] — visuals planos: Line, Markers, Image, Text
- [[TurntableCamera]] — camara orbital; la mas usada con visuals 3D
- [[ViewBox]] — contenedor de visuals y camaras
- [[Tree VisPy]] — roadmap completo del vault VisPy
