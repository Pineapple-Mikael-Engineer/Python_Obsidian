---
title: Canvas — ventana de renderizado de bajo nivel
aliases: [Canvas, vispy canvas]
tags: [vispy, api/clase, app]
lib: vispy
mod: vispy.app
tipo: clase
requiere: [vispy.use]
draft: false
---

# Canvas — ventana de renderizado de bajo nivel

`Canvas` es la ventana nativa gestionada por VisPy. Es la API de **nivel bajo**: no tiene scene graph; el usuario controla manualmente todo el dibujado dentro del callback `on_draw` usando [[vispy.use]] para seleccionar el backend y `gloo` para emitir comandos OpenGL. Usala cuando necesites control total sobre el pipeline de renderizado o estes documentando gloo.

Para el 95 % de los casos conviene [[SceneCanvas]] (scene graph integrado). Usa `Canvas` solo cuando construyas tu propio pipeline con shaders.

## Importacion

```python
import vispy
vispy.use('pyqt5')          # siempre antes de importar app o scene
from vispy import app, gloo
```

## Constructor / Firma

```python
canvas = app.Canvas(
    size=(800, 600),        # (width, height) en pixeles
    title='VisPy Canvas',   # titulo de la ventana
    keys='interactive',     # 'interactive' = Esc cierra, F11 fullscreen
    show=False,             # mostrar al crear (True) o luego con .show()
    vsync=False,            # sincronizacion vertical
    resizable=True,
    decorate=True,
    fullscreen=False,
)
```

## Parametros clave

| Parametro | Tipo | Por defecto | Descripcion |
|-----------|------|-------------|-------------|
| `size` | `tuple[int, int]` | `(800, 600)` | Ancho y alto de la ventana en pixeles |
| `title` | `str` | `'VisPy canvas'` | Titulo que aparece en la barra de la ventana |
| `keys` | `str \| None` | `None` | `'interactive'` habilita Esc/F11; `None` deshabilita |
| `show` | `bool` | `False` | Si es `True`, la ventana aparece al instanciar |
| `vsync` | `bool` | `False` | Limita FPS al refresco del monitor |
| `resizable` | `bool` | `True` | Permite redimensionar la ventana |

## Casos de uso

### Canvas minimo con fondo negro

```python
import vispy
vispy.use('pyqt5')
from vispy import app, gloo

canvas = app.Canvas(size=(800, 600), keys='interactive')

@canvas.connect
def on_draw(event):
    gloo.clear(color='black')   # borra el framebuffer con negro

@canvas.connect
def on_resize(event):
    gloo.set_viewport(0, 0, *event.size)   # ajusta viewport al nuevo tamano

canvas.show()
app.run()   # bloquea hasta cerrar la ventana
```

### Conectar callbacks con `canvas.events`

Alternativa al decorador `@canvas.connect`; util cuando el callback se define en otra funcion o metodo:

```python
def my_draw(event):
    gloo.clear(color=(0.1, 0.1, 0.15, 1.0))

canvas.events.draw.connect(my_draw)
canvas.events.resize.connect(lambda e: gloo.set_viewport(0, 0, *e.size))
```

### Canvas + Timer para animacion

```python
import vispy
vispy.use('pyqt5')
from vispy import app, gloo
import numpy as np

canvas = app.Canvas(size=(800, 600), keys='interactive')
t = 0.0

@canvas.connect
def on_draw(event):
    gloo.clear(color=(t % 1.0, 0.2, 0.5, 1.0))   # color oscilante

@canvas.connect
def on_resize(event):
    gloo.set_viewport(0, 0, *event.size)

timer = app.Timer(interval=1/60, start=False)

@timer.connect
def on_timer(event):
    global t
    t += event.dt
    canvas.update()   # dispara on_draw en el proximo tick del event loop

canvas.show()
timer.start()
app.run()
```

## Callbacks de eventos

Los eventos se conectan con `@canvas.connect` (el nombre de la funcion define a que evento se asocia) o con `canvas.events.<nombre>.connect(func)`.

| Callback | Evento | Atributos del `event` |
|----------|--------|-----------------------|
| `on_draw(event)` | El canvas necesita redibujar | — |
| `on_resize(event)` | La ventana cambio de tamano | `event.size: tuple[int, int]` |
| `on_key_press(event)` | Tecla presionada | `event.key`, `event.modifiers` |
| `on_key_release(event)` | Tecla soltada | `event.key`, `event.modifiers` |
| `on_mouse_press(event)` | Boton del mouse presionado | `event.pos`, `event.button` |
| `on_mouse_move(event)` | Mouse en movimiento | `event.pos`, `event.last_event` |
| `on_mouse_wheel(event)` | Rueda del mouse | `event.delta` |
| `on_close(event)` | Ventana cerrandose | — |

> [!info] Patron de conexion
> `@canvas.connect` infiere el evento desde el **nombre** de la funcion: `on_draw` → evento `draw`, `on_resize` → evento `resize`. El nombre debe coincidir exactamente.

## Metodos y atributos

| Nombre | Tipo | Descripcion |
|--------|------|-------------|
| `.show()` | metodo | Hace visible la ventana (si `show=False` al crear) |
| `.update()` | metodo | Solicita un redibujado (dispara `on_draw` en el proximo ciclo) |
| `.close()` | metodo | Cierra y destruye la ventana |
| `.size` | `tuple[int, int]` | Tamano actual `(width, height)` en pixeles |
| `.title` | `str` | Titulo de la ventana; asignable |
| `.events` | `EventEmitter` | Acceso directo a todos los emitters de eventos |
| `.context` | `GLContext` | Contexto OpenGL asociado |

## Diferencia con SceneCanvas

| Aspecto | `Canvas` (gloo) | `SceneCanvas` (scene) |
|---------|-----------------|------------------------|
| Scene graph | No; dibujado manual | Si; nodos, visuals, ViewBox |
| Casos de uso | Shaders propios, pipeline custom | Visualizacion cientifica estandar |
| Complejidad | Alta (OpenGL directo) | Baja (API declarativa) |
| `on_draw` | Obligatorio definir | Gestionado internamente |
| `view.camera` | Manual (transformaciones GLSL) | `view.camera = 'turntable'` |

## Errores comunes

| Error | Causa | Solucion |
|-------|-------|----------|
| Pantalla negra aunque no hay error | `on_draw` no llama a `gloo.clear()` | Agregar `gloo.clear(color=...)` al inicio de `on_draw` |
| `RuntimeError: No backend available` | No se instalo ningun backend | `pip install pyqt5` o `pip install pyglet` |
| Ventana no aparece | `show=False` y no se llamo `.show()` | Llamar `canvas.show()` antes de `app.run()` |
| `on_resize` no se llama al inicio | Solo se dispara en cambios posteriores | Llamar `gloo.set_viewport(0, 0, *canvas.size)` en `on_draw` |
| `@canvas.connect` no conecta | Nombre de funcion no coincide con evento | Verificar nombre: debe ser `on_<evento>` exacto |

## Notas relacionadas

- [[Timer]] — temporizador para animaciones; se usa junto a `canvas.update()` para animar
- [[vispy.use]] — seleccionar backend antes de crear cualquier Canvas
- [[SceneCanvas]] — alternativa de alto nivel con scene graph integrado
