---
title: VisPy — visualizacion cientifica acelerada por GPU
aliases: [VisPy, que es vispy, indice vispy]
tags: [vispy, indice]
lib: vispy
mod: vispy
draft: false
---

# VisPy — visualizacion cientifica acelerada por GPU

VisPy es una libreria de **visualizacion de alto rendimiento** para Python. Opera directamente sobre la GPU mediante OpenGL: renderiza millones de puntos, lineas o volumenes a decenas de frames por segundo, donde Matplotlib se congela o se queda sin memoria. Delega el trabajo pesado a la tarjeta grafica, no al CPU.

A diferencia de NumPy o SciPy —donde casi todo son **funciones** sobre `ndarray`— VisPy es **orientada a objetos**: aportas y conectas **clases** (un `Canvas`, una `Camera`, varios `Visual`). El modelo dominante es la **composicion** (un arbol de nodos: el *scene graph*), con **herencia** puntual cuando subclaseas `Canvas` o creas un `Visual` propio. Por eso este vault documenta, ademas de cada clase, **de quien hereda** (abajo) — saber la herencia es saber que metodos comparten.

## Cuando usar VisPy en lugar de Matplotlib

- Mas de ~100 000 puntos, lineas o vertices.
- Tiempo real (sensores, simulaciones, streaming).
- Datos 3D interactivos (mallas, volumenes, nubes de puntos).
- Animaciones fluidas de 30–60 fps o mas.

## Instalacion

```python
# pip install vispy pyqt5         # backend de ventana recomendado en desktop
# pip install vispy pyglet        # alternativa sin Qt
# pip install vispy jupyter_rfb   # para Jupyter Notebook
```

Solo se necesita `vispy` mas **un** backend de ventana. `pyqt5` es el mas estable.

## Las dos APIs

VisPy expone dos capas. No se mezclan en una misma app; elige una segun el caso:

| API | Modulo | Nivel | Cuando usarla |
|-----|--------|-------|---------------|
| **scene** | `vispy.scene` | Alto | 95 % de los casos: scatter, lineas, imagenes, volumenes, camaras |
| **gloo** | `vispy.gloo` | Bajo | Shaders GLSL propios, pipeline de renderizado personalizado |

`scene` construye sobre `gloo`: internamente todo es OpenGL, pero `scene` lo oculta con un **scene graph**, un arbol de nodos donde cada visual sabe dibujarse a si mismo.

## Flujo minimo (API scene)

```python
import vispy
vispy.use('pyqt5')          # 1. fijar backend ANTES de importar scene/app
from vispy import scene, app
import numpy as np

canvas = scene.SceneCanvas(keys='interactive', show=True)  # 2. ventana + scene graph
view = canvas.central_widget.add_view()                    # 3. ViewBox (viewport + camara)
view.camera = 'turntable'                                  #    camara 3D interactiva

pos = np.random.randn(1000, 3).astype('float32')           # 4. crear y agregar un visual
scatter = scene.visuals.Markers(parent=view.scene)
scatter.set_data(pos, face_color=(1, 1, 0, 0.8), size=5)

app.run()                                                  # 5. event loop (bloquea)
```

## Clases que aporta VisPy

Lo que importas y conectas. Agrupadas por modulo; la columna **Hereda de** indica el origen de sus metodos compartidos.

| Clase | Modulo | Hereda de | Rol |
|-------|--------|-----------|-----|
| `Canvas` | `vispy.app` | — (raiz) | Ventana OpenGL + event loop (estilo bajo nivel / gloo) |
| `SceneCanvas` | `vispy.scene` | **`app.Canvas`** | Ventana **con scene graph**; añade `.scene` y `.central_widget` |
| `Timer` | `vispy.app` | — | Ticks no-bloqueantes para animacion |
| `Node` | `vispy.scene` | — (raiz del grafo) | Nodo del scene graph: padre/hijos + transform |
| `Widget` \| `ViewBox` \| `Grid` | `vispy.scene` | **`Node`** | Viewport (`ViewBox`), layout de subplots (`Grid`) |
| `BaseCamera` | `vispy.scene.cameras` | **`Node`** | Base de todas las camaras |
| `PanZoomCamera` | `vispy.scene.cameras` | **`BaseCamera`** | Navegacion 2D |
| `TurntableCamera` \| `FlyCamera` \| `ArcballCamera` | `vispy.scene.cameras` | **`PerspectiveCamera` ← `BaseCamera`** | Navegacion 3D |
| `Visual` | `vispy.visuals` | `BaseVisual` | Sabe **dibujarse** en GPU (shaders internos) |
| `scene.visuals.*` (`Line`, `Markers`, `Image`, `Text`, `Mesh`, `Volume`, `Surface`) | `vispy.scene.visuals` | **`Node` + `Visual`** (VisualNode) | Visuals que viven en el arbol |
| `Program` | `vispy.gloo` | `GLObject` | Shader GLSL compilado + uniforms/attributes |
| `VertexBuffer` \| `IndexBuffer` | `vispy.gloo` | `DataBuffer` ← `GLObject` | Datos de vertices/indices en GPU |
| `Texture2D` \| `Texture3D` | `vispy.gloo` | `BaseTexture` ← `GLObject` | Texturas en GPU |
| `Color` | `vispy.color` | **`ColorArray`** | Un color = `ColorArray` de longitud 1 |
| `Colormap` | `vispy.color` | — | Mapea valores 0–1 a colores |

## Mapa de herencia (que metodos comparten)

```
app.Canvas ─────────────► .show() .update() .close() .size
│                          eventos: on_draw on_resize on_mouse_* on_key_*
│                          .events  .connect()
└── scene.SceneCanvas ──► hereda TODO lo anterior + .scene (Node raiz) + .central_widget

Node ───────────────────► .parent .children .transform .transforms .visible
│                          (todo lo que vive en el scene graph es un Node)
├── Widget
│   ├── ViewBox ────────► .camera  .add(visual)  un viewport con clipping
│   └── Grid ───────────► .add_view(row, col)    subplots
├── BaseCamera ─────────► .set_range() .reset() .link()  .interactive
│   ├── PanZoomCamera                 (2D)
│   └── PerspectiveCamera
│        ├── TurntableCamera          (3D, orbita)
│        ├── FlyCamera                (3D, libre WASD)
│        └── ArcballCamera            (3D, arcball)
└── VisualNode = Node + Visual  →  scene.visuals.*
     ├── Line   Markers   Image   Text          (2D)
     └── Mesh   Volume    SurfacePlot           (3D)

Visual ─────────────────► .set_data(...) .transform .attach() .draw() .update()
                           (los scene.visuals.* heredan esto del lado Visual)

gloo.GLObject ──────────► objeto en memoria GPU
├── Program ────────────► program['uniform'] = ... ;  program.draw('triangles')
├── DataBuffer → VertexBuffer | IndexBuffer
└── BaseTexture → Texture2D | Texture3D
```

> [!tip] La idea clave de la herencia
> `SceneCanvas` **es un** `Canvas` (por eso comparte `on_draw`, `.update()`, `.size`…).
> Cada `scene.visuals.X` **es un** `Node` (vive en el arbol, tiene `.parent`/`.transform`) **y un** `Visual` (sabe dibujarse, tiene `.set_data()`). Esa doble herencia es el corazon de la API `scene`.

## Como navegar el vault

| Quiero… | Ir a |
|---------|------|
| El modelo mental (canvas, scene graph, camaras, GPU) | [[VisPy/conceptos_transversales/index\|conceptos_transversales]] |
| Ventana, backend y animacion | [[VisPy/vispy.app/index\|vispy.app]] |
| Scene graph: SceneCanvas, ViewBox, Node | [[VisPy/vispy.scene/index\|vispy.scene]] |
| Camaras 2D/3D | [[VisPy/vispy.scene/cameras/index\|cameras]] |
| Visuals (lineas, puntos, mallas, volumenes) | [[VisPy/vispy.scene/visuals/index\|visuals]] |
| Bajo nivel: shaders, buffers, texturas | [[VisPy/vispy.gloo/index\|vispy.gloo]] |
| Colores y colormaps | [[VisPy/vispy.color/index\|vispy.color]] |

> [!tip] Por donde empezar
> Lee [[concepto_canvas_app]] y [[concepto_scene_graph]] para el modelo mental, luego `SceneCanvas` + `ViewBox` cubren el 95 % de los casos.

## Notas relacionadas

- [[concepto_scene_graph]] — el arbol de nodos que organiza la escena
- [[vispy.use]] — seleccion de backend; primer paso obligatorio
- [[Canvas]] — ciclo de vida de la ventana y el event loop
