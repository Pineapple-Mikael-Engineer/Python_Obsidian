---
title: Program — shader GLSL compilado en GPU
aliases:
  - Program
  - gloo program
  - shader vispy
tags:
  - vispy
  - api/clase
  - gloo
lib: vispy
mod: vispy.gloo
tipo: clase
retorna: Program
requiere:
  - concepto_gloo_pipeline
draft: false
---

# Program — shader GLSL compilado en GPU

`gloo.Program` es el nucleo de toda la API gloo: compila un par de shaders GLSL (vertex + fragment)
en la GPU y expone una interfaz Python para pasar datos (attributes y uniforms) antes de renderizar.
Usalo cuando necesites control total del pipeline OpenGL con shaders propios.

## Importacion

```python
from vispy import gloo
```

## Constructor / Firma

```python
program = gloo.Program(vert, frag, count=None)
```

| Parametro | Tipo | Descripcion |
|-----------|------|-------------|
| `vert` | `str` | Codigo fuente del vertex shader (GLSL) |
| `frag` | `str` | Codigo fuente del fragment shader (GLSL) |
| `count` | `int \| None` | Numero de vertices (opcional; se infiere del buffer si es `None`) |

## Parametros clave

### Asignacion de attributes y uniforms

La indizacion `program['nombre'] = valor` detecta automaticamente si `nombre`
corresponde a un `attribute` o a un `uniform` en el shader:

```python
# Attribute — toma un VertexBuffer (datos en GPU)
buf = gloo.VertexBuffer(data)
program['position'] = buf

# Uniform — toma un valor Python o numpy directamente
program['color'] = (1.0, 0.0, 0.0, 1.0)
program['scale'] = 2.0
```

> [!info] Diferencia attribute vs uniform
> Un **attribute** varia por vertice (posicion, color por vertice, normal…) y
> requiere un [[VertexBuffer]]. Un **uniform** es constante para toda la draw call
> (transformacion, color global, tiempo…) y se pasa directo como escalar o array numpy.

### `.bind(buffer)`

Atajo para asignar todos los campos de un structured numpy array de una sola vez:

```python
data = np.zeros(3, dtype=[('position', np.float32, 2),
                           ('color',    np.float32, 4)])
program.bind(gloo.VertexBuffer(data))
# equivale a:
# program['position'] = VertexBuffer(data['position'])
# program['color']    = VertexBuffer(data['color'])
```

## Casos de uso

### Minimo — triangulo solido

```python
import vispy; vispy.use('pyqt5')
from vispy import app, gloo
import numpy as np

VERT = """
attribute vec2 position;
void main() {
    gl_Position = vec4(position, 0.0, 1.0);
}
"""
FRAG = """
uniform vec4 color;
void main() {
    gl_FragColor = color;
}
"""

data = np.array([[-0.5, -0.5], [0.5, -0.5], [0.0, 0.5]], dtype=np.float32)
program = gloo.Program(VERT, FRAG)
program['position'] = gloo.VertexBuffer(data)
program['color'] = (0.2, 0.6, 1.0, 1.0)

canvas = app.Canvas(size=(600, 600), keys='interactive')

@canvas.connect
def on_draw(event):
    gloo.clear('black')
    program.draw('triangles')   # renderiza 3 vertices -> 1 triangulo

@canvas.connect
def on_resize(event):
    gloo.set_viewport(0, 0, *event.size)

canvas.show()
app.run()
```

### Con color por vertice (structured array)

```python
data = np.zeros(3, dtype=[('position', np.float32, 2),
                           ('color',    np.float32, 4)])
data['position'] = [[-0.5, -0.5], [0.5, -0.5], [0.0, 0.5]]
data['color']    = [(1, 0, 0, 1), (0, 1, 0, 1), (0, 0, 1, 1)]

program = gloo.Program(VERT, FRAG)
program.bind(gloo.VertexBuffer(data))   # asigna 'position' y 'color' de golpe
```

## Metodos y atributos

| Metodo / Atributo | Descripcion |
|-------------------|-------------|
| `program['nombre'] = val` | Asigna attribute (VertexBuffer) o uniform (valor Python/numpy) |
| `program.bind(VertexBuffer)` | Asigna todos los campos de un structured buffer |
| `program.draw(mode)` | Renderiza. `mode`: `'triangles'`, `'points'`, `'lines'`, `'line_strip'`, `'triangle_strip'` |
| `program['nombre']` | Lee el valor asignado (util para depuracion) |

## Errores comunes

| Error | Causa | Solucion |
|-------|-------|----------|
| `KeyError: 'nombre'` | El nombre no existe en ningun shader | Verificar ortografia exacta en el GLSL |
| Pantalla en negro (sin excepcion) | Shader compila pero datos invalidos o `draw()` no se llama en `on_draw` | Revisar que `gloo.clear()` precede a `draw()` y que el buffer tiene vertices |
| `ValueError` al asignar uniform | Tipo incompatible (e.g. entero donde espera `float`) | Usar `float` o `np.float32` explicitamente |
| No aparece la ventana | Backend no seleccionado | Agregar `vispy.use('pyqt5')` al inicio |

## Notas relacionadas

- [[VertexBuffer]] — buffer de vertices que se asigna a attributes
- [[Texture2D]] — textura que se asigna a uniforms sampler2D
- [[concepto_gloo_pipeline]] — modelo mental del pipeline vertex → fragment → framebuffer
- [[Canvas]] — la ventana donde se ejecuta `on_draw` y se llama `program.draw()`
