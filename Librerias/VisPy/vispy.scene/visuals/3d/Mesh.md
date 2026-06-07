---
title: Mesh — malla triangular 3D
aliases:
  - Mesh
  - vispy mesh
tags:
  - vispy
  - api/clase
  - scene/visuals
lib: vispy
mod: vispy.scene.visuals
tipo: clase
retorna: Mesh
requiere:
  - SceneCanvas
  - ViewBox
  - TurntableCamera
draft: false
---

# Mesh — malla triangular 3D

`scene.visuals.Mesh` renderiza una malla triangular 3D definida por vertices y caras.
Es el visual central para objetos 3D arbitrarios: desde un tetraedro hasta una malla STL
cargada con [[Trimesh]] o `meshio`. La GPU dibuja cada triangulo de forma acelerada;
el color puede ser uniforme, por vertice o por cara.

## Importacion

```python
from vispy import scene, app
import vispy
vispy.use('pyqt5')

# acceso canonico
mesh = scene.visuals.Mesh(...)
```

## Constructor / Firma

```python
scene.visuals.Mesh(
    vertices=None,       # array (N, 3) float32 — posiciones XYZ
    faces=None,          # array (M, 3) uint32  — indices de triangulos
    vertex_colors=None,  # array (N, 4) float32 — RGBA por vertice
    face_colors=None,    # array (M, 4) float32 — RGBA por cara
    color=(0.5, 0.5, 1, 1),  # color uniforme (RGBA o nombre CSS)
    shading=None,        # 'smooth' | 'flat' | None
    mode='triangles',    # primitiva OpenGL
    parent=None,
)
```

## Parametros clave

| Parametro | Tipo | Descripcion |
|-----------|------|-------------|
| `vertices` | `(N, 3) float32` | Posiciones 3D de cada vertice |
| `faces` | `(M, 3) uint32` | Cada fila = indices de los 3 vertices del triangulo |
| `vertex_colors` | `(N, 4) float32` | RGBA por vertice; interpolado en la GPU (Gouraud) |
| `face_colors` | `(M, 4) float32` | RGBA uniforme por cara |
| `color` | RGBA / str | Color uniforme; ignorado si `vertex_colors` o `face_colors` activos |
| `shading` | str \| None | `'smooth'`: normales interpoladas; `'flat'`: normal de cara; `None`: sin iluminacion |

Solo uno de `vertex_colors`, `face_colors` o `color` esta activo a la vez (prioridad: vertex > face > color).

### shading

- `shading=None` — sin calculo de normales; el color es plano sin efecto de luz.
- `shading='flat'` — una normal por triangulo; efecto facetado (low-poly).
- `shading='smooth'` — normales interpoladas entre vertices; superficie suave (requiere normales consistentes).

## Casos de uso

### Tetraedro basico

```python
import vispy
vispy.use('pyqt5')
from vispy import scene, app
import numpy as np

canvas = scene.SceneCanvas(keys='interactive', show=True, size=(800, 600))
view = canvas.central_widget.add_view()
view.camera = 'turntable'

verts = np.array([
    [0, 0, 0], [1, 0, 0], [0.5, 1, 0], [0.5, 0.5, 1]
], dtype='float32')
faces = np.array([[0,1,2], [0,1,3], [0,2,3], [1,2,3]], dtype='uint32')

mesh = scene.visuals.Mesh(
    vertices=verts,
    faces=faces,
    color='cyan',
    shading='smooth',
    parent=view.scene,
)
app.run()
```

### Colores por vertice

```python
vcolors = np.array([
    [1, 0, 0, 1],  # rojo
    [0, 1, 0, 1],  # verde
    [0, 0, 1, 1],  # azul
    [1, 1, 0, 1],  # amarillo
], dtype='float32')

mesh = scene.visuals.Mesh(
    vertices=verts,
    faces=faces,
    vertex_colors=vcolors,
    shading=None,
    parent=view.scene,
)
```

### Cargar STL con meshio

```python
import meshio

m = meshio.read('modelo.stl')
verts = m.points.astype('float32')
faces = m.cells_dict['triangle'].astype('uint32')

mesh = scene.visuals.Mesh(
    vertices=verts,
    faces=faces,
    color='lightgray',
    shading='smooth',
    parent=view.scene,
)
```

### Actualizar datos en animacion

```python
# NO reasignar mesh = scene.visuals.Mesh(...) dentro del timer
# Usar .set_data() para actualizar sin recrear el objeto
mesh.set_data(vertices=nuevos_verts, faces=faces, color='cyan')
canvas.update()
```

## Metodos y atributos

| Nombre | Descripcion |
|--------|-------------|
| `.set_data(vertices, faces, ...)` | Actualiza geometria o color sin recrear el objeto |
| `.transform` | `MatrixTransform` — traslacion, rotacion, escala |
| `.visible` | `bool` — muestra u oculta el mesh |
| `.shading_filter` | Acceso al filtro de sombreado activo |

## Errores comunes

| Error | Causa | Solucion |
|-------|-------|----------|
| `ValueError: faces must be integer` | `faces` en `float32` en vez de `uint32` | `faces.astype('uint32')` |
| Mesh negro sin color | `shading='smooth'` sin normales validas | Probar `shading=None` primero |
| Malla invertida (caras ocultas) | Winding order incorrecto (CCW vs CW) | Invertir `faces[:, [1, 2]]` |
| `AttributeError: parent` | Visual sin `parent=view.scene` | Agregar `parent=view.scene` en el constructor |

## Notas relacionadas

- [[vispy.scene/visuals/3d/index|visuals 3D]] — contexto del submodulo
- [[TurntableCamera]] — camara orbital para explorar mallas 3D
- [[Volume]] — alternativa para datos volumetricos (CT, simulaciones)
- [[Surface]] — superficie z=f(x,y) sobre grid regular (mas sencillo que Mesh)
