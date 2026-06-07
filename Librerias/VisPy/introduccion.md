---
title: Introduccion a VisPy
aliases: [VisPy, que es vispy]
tags: [vispy, concepto]
lib: vispy
mod: vispy
tipo: concepto
draft: false
---

# Introduccion a VisPy

VisPy es una libreria de **visualizacion cientifica de alto rendimiento** para Python. Opera directamente sobre la GPU mediante OpenGL: puede renderizar millones de puntos, lineas o volumenes a decenas de frames por segundo, donde Matplotlib se congela o se queda sin memoria. Su filosofia es delegar todo el trabajo pesado a la tarjeta grafica y no al CPU.

**Cuando usar VisPy en lugar de Matplotlib:**

- Mas de ~100 000 puntos, lineas o vertices.
- Visualizacion en tiempo real (sensores, simulaciones, streaming).
- Datos 3D interactivos (mallas, volumenes, nubes de puntos).
- Animaciones fluidas que requieren 30–60 fps o mas.

## Instalacion

```python
# pip install vispy pyqt5   # backend de ventana recomendado en desktop
# pip install vispy pyglet  # alternativa sin Qt
# pip install vispy jupyter_rfb  # para Jupyter Notebook
```

Solo se necesita `vispy` mas **un** backend de ventana. En la mayoria de los casos `pyqt5` es el mas estable.

## Las dos APIs

VisPy expone dos capas de abstraccion. No se mezclan en una misma app; elige una segun el caso:

| API | Modulo | Nivel | Cuando usarla |
|-----|--------|-------|---------------|
| **scene** | `vispy.scene` | Alto | 95 % de los casos: scatter, lineas, imagenes, volumenes, camaras |
| **gloo** | `vispy.gloo` | Bajo | Shaders GLSL propios, pipeline de renderizado personalizado |

`scene` construye sobre `gloo`; internamente todo es OpenGL, pero `scene` oculta esa complejidad con un **scene graph**: un arbol de nodos donde cada visual sabe como dibujarse a si mismo.

## Flujo minimo de uso

```python
# Instalacion: pip install vispy pyqt5

import vispy
vispy.use('pyqt5')          # 1. fijar backend ANTES de cualquier import de vispy
from vispy import scene, app
import numpy as np

# 2. crear la ventana con scene graph integrado
canvas = scene.SceneCanvas(keys='interactive', show=True)

# 3. agregar un ViewBox (viewport + camara)
view = canvas.central_widget.add_view()
view.camera = 'turntable'   # camara 3D interactiva: drag para orbitar, rueda para zoom

# 4. crear y agregar un visual
pos = np.random.randn(1000, 3).astype('float32')
scatter = scene.visuals.Markers(parent=view.scene)
scatter.set_data(pos, face_color=(1, 1, 0, 0.8), size=5)

# 5. iniciar el event loop
app.run()   # bloquea hasta cerrar la ventana
```

Estructura de un script VisPy con `scene`:

```
vispy.use(backend)              → seleccion de backend
SceneCanvas                     → ventana + scene graph
  └── central_widget.add_view() → ViewBox con camara
        └── visual(parent=view.scene) → Markers, Line, Image, Volume...
app.run()                       → event loop
```

## Conceptos clave para navegar el vault

| Concepto | Nota |
|----------|------|
| Ventana + event loop | [[Canvas]] (low-level) \| SceneCanvas (high-level) |
| Seleccion de backend | [[vispy.use]] |
| Animaciones / ticks | [[Timer]] |
| Camara interactiva 3D | TurntableCamera |
| Camara 2D | PanZoomCamera |
| Scatter / puntos | Markers |
| Lineas y curvas | Line |
| Imagenes / texturas | Image |
| Mallas 3D | Mesh |
| Volumenes | Volume |
| Shaders propios | Program (gloo) |

> [!tip] Por donde empezar
> Lee [[Canvas]] para entender el ciclo de vida de la ventana y el event loop. Luego pasa a `SceneCanvas` + `ViewBox` para el 95 % de los casos de uso reales. El [[Tree VisPy]] muestra el mapa completo del vault.

## Notas relacionadas

- [[Tree VisPy]] — estructura y roadmap del vault VisPy
- [[vispy.use]] — seleccion de backend; primer paso obligatorio
- [[Canvas]] — ciclo de vida de la ventana y el event loop de bajo nivel
- [[Timer]] — animaciones no-bloqueantes dentro del event loop
