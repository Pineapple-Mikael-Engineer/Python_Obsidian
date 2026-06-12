---
title: concepto_canvas_app — Canvas, event loop y backends en VisPy
aliases: [canvas vispy, event loop vispy, on_draw]
tags: [vispy, api/concepto, fundamentos]
lib: vispy
mod: vispy.app
tipo: concepto
draft: false
---

# Canvas, event loop y backends en VisPy

`Canvas` es la ventana OpenGL donde VisPy dibuja. Todo en VisPy parte de un canvas: sin el,
no hay contexto GPU, no hay callbacks, no hay visualizacion. `app.run()` es el event loop
que mantiene la ventana viva y procesa mouse, teclado y redraws. Sin `app.run()`, la ventana
aparece y se cierra de inmediato o directamente no responde.

## La idea central

El modelo mental es: **crear canvas → conectar callbacks → `canvas.show()` → `app.run()`**.

`on_draw` es el unico callback obligatorio si se usa `gloo` (bajo nivel): cada vez que el
sistema necesita redibujar (primer frame, resize, `canvas.update()`), se llama a `on_draw`.
`app.run()` bloquea la ejecucion hasta que se cierra la ventana.

```python
import vispy
vispy.use('pyqt5')                  # backend antes de cualquier import de Canvas
from vispy import app, gloo

canvas = app.Canvas(size=(800, 600), title='Demo', keys='interactive')

@canvas.connect
def on_draw(event):
    gloo.clear('black')             # limpiar con color de fondo

canvas.show()
app.run()                           # bloquea hasta cerrar la ventana
```

## Como funciona

### Backends disponibles

VisPy no gestiona la ventana directamente: delega esa tarea a una libreria de GUI o de
ventanas nativas. Hay que elegir el backend **antes** de importar `Canvas` o `SceneCanvas`.

| Backend | Comando | Cuando usarlo |
|---------|---------|---------------|
| PyQt5 | `vispy.use('pyqt5')` | Desktop general; el mas estable |
| pyglet | `vispy.use('pyglet')` | Sin Qt; facil de instalar |
| glfw | `vispy.use('glfw')` | Minimo, rapido, sin dependencias pesadas |
| jupyter_rfb | `vispy.use('jupyter_rfb')` | Jupyter Notebook / JupyterLab |

Si no se llama a `vispy.use()`, VisPy elige automaticamente el primer backend instalado,
lo que puede producir comportamientos distintos en diferentes entornos.

### Ciclo de vida completo

```python
import vispy
vispy.use('pyqt5')
from vispy import app, gloo
import numpy as np

canvas = app.Canvas(size=(800, 600), title='Ciclo completo', keys='interactive')

@canvas.connect
def on_draw(event):
    gloo.clear((0.1, 0.1, 0.1, 1.0))   # RGBA: gris oscuro
    # aqui iria program.draw(...)

@canvas.connect
def on_resize(event):
    # ajustar el viewport al nuevo tamano de ventana
    gloo.set_viewport(0, 0, *event.size)

@canvas.connect
def on_key_press(event):
    if event.key == 'Escape':
        canvas.close()
    elif event.key == 'Space':
        canvas.update()             # forzar redibujado manual

canvas.show()
app.run()
```

### Diferencia entre `Canvas` y `SceneCanvas`

`app.Canvas` es la clase base de bajo nivel: el usuario gestiona `on_draw` a mano, llama a
`gloo` directamente y controla cada pixel del shader. `scene.SceneCanvas` hereda de `Canvas`
pero agrega el scene graph completo — no hay que escribir `on_draw` porque el engine de
`scene` lo hace internamente.

```python
# SceneCanvas: on_draw lo gestiona el scene graph, no el usuario
from vispy import scene, app
import vispy
vispy.use('pyqt5')

canvas = scene.SceneCanvas(keys='interactive', show=True, size=(800, 600))
view = canvas.central_widget.add_view()
view.camera = 'turntable'
# agregar visuals con parent=view.scene y listo
app.run()
```

## Casos de uso

### Caso 1: ventana minima con fondo de color

```python
import vispy
vispy.use('pyqt5')
from vispy import app, gloo

canvas = app.Canvas(size=(640, 480), title='Fondo azul', keys='interactive')

@canvas.connect
def on_draw(event):
    gloo.clear((0.0, 0.2, 0.5, 1.0))   # azul oscuro

canvas.show()
app.run()
```

### Caso 2: animacion con Timer

```python
import vispy
vispy.use('pyqt5')
from vispy import app, gloo

canvas = app.Canvas(size=(800, 600), keys='interactive')
t = [0.0]

@canvas.connect
def on_draw(event):
    r = 0.5 + 0.5 * __import__('math').sin(t[0])
    gloo.clear((r, 0.2, 0.4, 1.0))     # rojo oscilante

timer = app.Timer(interval=1/60, connect=lambda e: (t.__setitem__(0, t[0] + 0.05),
                                                     canvas.update()), start=True)
canvas.show()
app.run()
```

### Caso 3: seleccion de backend en Jupyter

```python
import vispy
vispy.use('jupyter_rfb')               # backend para notebooks
from vispy import scene, app

canvas = scene.SceneCanvas(keys='interactive', show=True)
view = canvas.central_widget.add_view()
view.camera = 'panzoom'
canvas                                 # mostrar inline en el notebook
```

## Errores comunes

| Error | Causa | Solucion |
|-------|-------|----------|
| `ImportError: No backend found` | Ningun backend instalado | `pip install pyqt5` o `pip install pyglet` |
| La ventana no responde a eventos | Falta `app.run()` | Agregar `app.run()` al final del script |
| `vispy.use()` no tiene efecto | Se llamo despues de importar `Canvas` | Llamar `vispy.use()` antes de `from vispy import app` |
| Pantalla negra sin dibujo | `on_draw` no llama a `gloo.clear()` ni `program.draw()` | Agregar `gloo.clear(color)` dentro de `on_draw` |
| La ventana parpadea en resize | Falta `on_resize` con `gloo.set_viewport` | Conectar `on_resize` y ajustar el viewport |

## Notas relacionadas

- [[concepto_scene_graph]] — el scene graph que `SceneCanvas` gestiona internamente
- [[concepto_gloo_pipeline]] — como usar `gloo` dentro de `on_draw`
- [[concepto_cameras_transforms]] — camaras que se conectan al canvas via `ViewBox`
