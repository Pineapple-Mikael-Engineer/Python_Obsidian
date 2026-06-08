---
title: Tree VisPy
tags:
  - vispy
  - meta
draft: true
---

# 🌳 Tree VisPy

> Estructura **jerarquica** por **modulo** (`vispy.app`, `vispy.scene`, `vispy.gloo`, `vispy.color`).
> VisPy es una libreria de **visualizacion cientifica de alto rendimiento** basada en OpenGL:
> opera directamente sobre la GPU y ofrece dos APIs — `scene` (alto nivel, scene graph) y
> `gloo` (bajo nivel, shaders GLSL directos).
> `✅` = nota creada · sin marca = roadmap pendiente.

---

## 📁 Tipos de notas

| Tipo | Ubicacion | Ejemplo |
|------|-----------|---------|
| **Concepto transversal** | `conceptos_transversales/` | `concepto_scene_graph.md` |
| **Clase principal** | `vispy.<mod>/` | `Canvas.md`, `SceneCanvas.md` |
| **Visual (objeto de dibujo)** | `vispy.scene/visuals/<dim>/` | `Line.md`, `Volume.md` |
| **Camara** | `vispy.scene/cameras/` | `TurntableCamera.md` |
| **Elemento gloo** | `vispy.gloo/` | `Program.md`, `Texture2D.md` |
| **Funcion / config** | `vispy.<mod>/` | `vispy.use.md` |
| **Indice de carpeta** | `index.md` en **cada** directorio | nota madre/hub |

> Cada carpeta lleva su `index.md` (hub de navegacion rico). No se listan en el arbol
> para no saturarlo; ver `Reglas.md` §2.

---

## 📂 Estructura completa (roadmap)

```tree
VisPy/
│
├── index.md                           # que es VisPy, backends, flujo minimo
│
├── 📁 conceptos_transversales/
│   ├── concepto_canvas_app.md               # Canvas, backend, event loop, on_draw
│   ├── concepto_scene_graph.md              # scene graph: nodos, visuals, ViewBox
│   ├── concepto_cameras_transforms.md       # camara = viewport + proyeccion + interaccion
│   └── concepto_gloo_pipeline.md            # pipeline GPU: vertex/fragment shader, buffer, program
│
├── 📁 vispy.app/
│   ├── Canvas.md                            # ventana de renderizado (low-level, on_draw manual)
│   ├── Timer.md                             # tick de animacion; connect + start + stop
│   └── vispy.use.md                         # seleccionar backend: pyqt5, pyglet, glfw, jupyter…
│
├── 📁 vispy.scene/
│   ├── SceneCanvas.md                       # canvas con scene graph integrado; .scene, .central_widget
│   ├── ViewBox.md                           # viewport + camara + clipping; add_subplot pattern
│   ├── 📁 cameras/
│   │   ├── PanZoomCamera.md                 # 2D: pan con drag, zoom con rueda
│   │   ├── TurntableCamera.md               # 3D: orbitar alrededor de un centro
│   │   └── FlyCamera.md                     # 3D: movimiento libre tipo FPS (WASD)
│   └── 📁 visuals/
│       ├── 📁 2d/
│       │   ├── Line.md                      # lineas y curvas 2D/3D; pos, color, width
│       │   ├── Markers.md                   # scatter: puntos/simbolos; symbol, size, face_color
│       │   ├── Image.md                     # textura 2D desde array numpy; clim, cmap
│       │   └── Text.md                      # etiquetas y anotaciones; font_size, anchor
│       └── 📁 3d/
│           ├── Mesh.md                      # malla triangular 3D; vertices, faces, vertex_colors
│           ├── Volume.md                    # render volumetrico 3D; cmap, clim, method
│           └── Surface.md                  # superficie z=f(x,y) sobre grid regular
│
├── 📁 vispy.gloo/
│   ├── Program.md                           # shader GLSL compilado + uniforms + attributes
│   ├── VertexBuffer.md                      # datos de vertices subidos a GPU
│   └── Texture2D.md                         # textura 2D en GPU; interpolation, wrapping
│
└── 📁 vispy.color/
    ├── Color.md                             # color individual: RGBA, hex, nombre CSS
    ├── ColorArray.md                        # array de N colores; rgba, hex, iter
    └── vispy.get_colormap.md               # colormaps nombrados: fire, grays, viridis, hot…
```

---

## 📊 Estado actual de implementacion

> Rama **limpia** creada desde el commit de skills (`8e98b49`), sin notas de otras librerias.
> **Roadmap: ~26 / ~26 notas redactadas.**

| Submodulo | Plan | Estado | Prioridad |
|-----------|:----:|--------|-----------|
| `conceptos_transversales/` | 4 | ✅ completo | 🔴 primero (modelo mental) |
| `vispy.app/` | 3 | ✅ completo | 🔴 base de todo |
| `vispy.scene/` (SceneCanvas, ViewBox) | 2 | ✅ completo | 🔴 nucleo |
| `vispy.scene/cameras/` | 3 | ✅ completo | 🟠 alta |
| `vispy.scene/visuals/2d/` | 4 | ✅ completo | 🟠 alta |
| `vispy.scene/visuals/3d/` | 3 | ✅ completo | 🟡 media |
| `vispy.gloo/` | 3 | ✅ completo | 🟡 media |
| `vispy.color/` | 3 | ✅ completo | 🟡 media |
| raiz (`index.md`) | 1 | ✅ completo | 🔴 entrada |
| **Total** | **~26** | **~26 creadas** | |

### Orden sugerido de relleno

1. **`conceptos_transversales`** + `index.md` — el modelo mental: canvas, scene graph, event loop.
2. **`vispy.app`** — `Canvas`, `Timer`, `vispy.use`: el ciclo de vida de cualquier app.
3. **`vispy.scene`** — `SceneCanvas` + `ViewBox` + `cameras`: el 90 % de los casos de uso.
4. **`vispy.scene/visuals/2d`** — los visuals mas usados: `Line`, `Markers`, `Image`, `Text`.
5. **`vispy.scene/visuals/3d`** — `Mesh`, `Volume`, `Surface`.
6. **`vispy.gloo`** — para uso avanzado con shaders propios.
7. **`vispy.color`** — `Color`, `ColorArray`, colormaps.

### Notas

- VisPy requiere un **backend** de ventana (`pyqt5`, `pyglet`, `glfw`, `jupyter_rfb`…).
  Siempre mostrar `vispy.use('pyqt5')` (o el que corresponda) antes de cualquier ejemplo.
- Las dos APIs **no se mezclan** en una misma app: usa `scene` O `gloo`, no ambas.
  `scene` es preferible para el 95 % de los casos; `gloo` para shaders personalizados.
- Los visuals de `vispy.scene.visuals` son diferentes de los de `vispy.visuals` (la capa base);
  documentar siempre desde `scene.visuals` (la API publica recomendada).
- El objeto central de `scene` es el **ViewBox**: contiene la camara, el clip, y es el
  padre de todos los visuals. Casi todo se agrega con `visual.parent = view.scene`.

---

## Notas relacionadas

- [[Estandarizan Directorio Librerias]]
