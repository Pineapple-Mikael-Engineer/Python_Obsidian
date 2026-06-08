---
title: conceptos_transversales — Los 4 modelos mentales de VisPy
tags:
  - vispy
  - indice
draft: false
---

# conceptos_transversales — Los 4 modelos mentales de VisPy

Antes de escribir una sola linea de VisPy hay cuatro conceptos que hay que entender: el
event loop, el scene graph, las camaras y el pipeline GPU. Sin ellos, el codigo parece
magico y los errores son imposibles de diagnosticar. Con ellos, el 95 % de los problemas
tienen una causa obvia.

Esta carpeta contiene las cuatro notas que forman ese modelo mental. No son notas de API
(eso esta en `vispy.app/`, `vispy.scene/`, `vispy.gloo/`) — son los **conceptos estructurales**
que conectan todas las notas de API entre si.

## El modelo de objetos de VisPy

Aqui esta el cambio de chip respecto a NumPy/SciPy: alli todo era **funciones sobre `ndarray`**;
en VisPy todo es **orientado a objetos** — clases que se instancian y se conectan entre si. El
patron dominante no es llamar funciones sueltas sino **composicion**: el scene graph es un arbol
de nodos donde agregas cada visual indicando su sitio con `parent=view.scene`, y el render recorre
ese arbol. La **herencia** aparece de forma puntual cuando subclaseas `Canvas` para tu propia
ventana o creas un `Visual` propio. Para el mapa completo de clases y su jerarquia de herencia,
ve [[VisPy/index | VisPy]].

## Como se relacionan los 4 conceptos

```
┌─────────────────────────────────────────────────────────────┐
│                      app.run()                              │
│           (event loop — bloquea, procesa eventos)           │
│                           │                                 │
│          ┌────────────────┴──────────────────┐              │
│          │                                   │              │
│    app.Canvas                         scene.SceneCanvas     │
│    (bajo nivel)                       (alto nivel)          │
│          │                                   │              │
│    on_draw() manual                   scene graph           │
│          │                     ┌─────────────┴──────────┐   │
│    vispy.gloo                  │                        │   │
│    (shaders GLSL)           ViewBox                  ViewBox │
│          │                     │                        │   │
│    Program                  Camera                  Camera  │
│    VertexBuffer             (PanZoom /              (Turntable│
│    Texture2D                Turntable /              / Fly)  │
│                             Fly)                            │
│                                │                            │
│                          visuals hijos                      │
│                     (Line, Markers, Image…)                  │
└─────────────────────────────────────────────────────────────┘
```

**Flujo de ejecucion minimo** (los dos caminos posibles):

```
# Camino A: scene (alto nivel)
SceneCanvas → central_widget.add_view() → view.camera = ... → visual(parent=view.scene) → app.run()

# Camino B: gloo (bajo nivel)
Canvas → Program(vert, frag) → bind(VertexBuffer) → on_draw: program.draw() → app.run()
```

El event loop (`app.run()`) es comun a ambos caminos. Sin el, la ventana no responde.

## Tabla de decision — cuando leer cada concepto

| Pregunta / situacion | Leer primero |
|----------------------|-------------|
| La ventana no se abre o no responde | [[concepto_canvas_app]] |
| No entiendo como se elige el backend (pyqt5, pyglet…) | [[concepto_canvas_app]] |
| No se donde agregar un visual o por que no aparece | [[concepto_scene_graph]] |
| Quiero varios subplots o viewports | [[concepto_scene_graph]] |
| El zoom/pan no funciona como espero | [[concepto_cameras_transforms]] |
| Necesito una camara 3D con orbita | [[concepto_cameras_transforms]] |
| Quiero rotar o escalar un visual individualmente | [[concepto_cameras_transforms]] |
| Necesito un shader personalizado en GLSL | [[concepto_gloo_pipeline]] |
| Quiero entender como funciona `scene` por dentro | [[concepto_gloo_pipeline]] |
| Tengo un error de OpenGL sin mensaje claro | [[concepto_gloo_pipeline]] |

## Notas

- [[concepto_canvas_app]] — `Canvas`, backends, event loop, `on_draw`, `app.run()`
- [[concepto_scene_graph]] — grafo de nodos, `ViewBox`, visuals, cascada de transformaciones
- [[concepto_cameras_transforms]] — `PanZoomCamera`, `TurntableCamera`, `FlyCamera`, `STTransform`
- [[concepto_gloo_pipeline]] — `Program`, `VertexBuffer`, shaders GLSL, modos de dibujo

## Notas relacionadas

- [[Tree VisPy]] — roadmap y estructura completa del vault de VisPy
