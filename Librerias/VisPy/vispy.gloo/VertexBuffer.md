---
title: VertexBuffer — buffer de vertices en GPU
aliases:
  - VertexBuffer
  - gloo buffer
  - vertex buffer vispy
tags:
  - vispy
  - api/clase
  - gloo
lib: vispy
mod: vispy.gloo
tipo: clase
retorna: VertexBuffer
requiere:
  - concepto_gloo_pipeline
draft: false
---

# VertexBuffer — buffer de vertices en GPU

`gloo.VertexBuffer` sube un array numpy a memoria de GPU como buffer de vertices.
A diferencia de un array numpy que vive en RAM, el buffer vive en la GPU y el shader
puede leerlo directamente sin transferencia por cada frame. Usalo siempre que necesites
pasar geometria o datos por vertice a un [[Program]].

## Importacion

```python
from vispy import gloo
```

## Constructor / Firma

```python
buf = gloo.VertexBuffer(data)
```

| Parametro | Tipo | Descripcion |
|-----------|------|-------------|
| `data` | `np.ndarray` | Array numpy a subir. Puede ser structured array o array regular `float32` |

## Parametros clave

### Tipos de `data` aceptados

**Array regular** (un solo campo, e.g. posiciones):

```python
positions = np.array([[-0.5, -0.5],
                      [ 0.5, -0.5],
                      [ 0.0,  0.5]], dtype=np.float32)
buf = gloo.VertexBuffer(positions)
program['position'] = buf
```

**Structured array** (multiples campos intercalados — interleaved):

```python
dtype = [('position', np.float32, 2),
         ('color',    np.float32, 4)]
data = np.zeros(3, dtype=dtype)
data['position'] = [[-0.5, -0.5], [0.5, -0.5], [0.0, 0.5]]
data['color']    = [(1, 0, 0, 1), (0, 1, 0, 1), (0, 0, 1, 1)]

buf = gloo.VertexBuffer(data)
program.bind(buf)   # asigna 'position' y 'color' automaticamente
```

> [!tip] Structured array = un buffer, multiples attributes
> Con un structured array y `program.bind(buf)`, todos los campos del dtype
> se mapean a los attributes del shader de una sola vez. Es la forma mas eficiente
> porque los datos quedan intercalados en un solo bloque contiguo en GPU.

### `.set_data(new_data)` — actualizar sin recrear

En animaciones, re-crear el buffer cada frame es caro. Usa `.set_data()` para
subir datos nuevos al mismo buffer de GPU que ya existe:

```python
# Fuera del loop: crear el buffer una vez
buf = gloo.VertexBuffer(data)
program['position'] = buf

# Dentro del loop de animacion: solo actualizar
def update(event):
    data['position'] = calcular_nuevas_posiciones(t)
    buf.set_data(data)   # re-sube a GPU sin destruir el buffer
    canvas.update()
```

## Casos de uso

### Nube de puntos con colores

```python
import vispy; vispy.use('pyqt5')
from vispy import app, gloo
import numpy as np

VERT = """
attribute vec2 position;
attribute vec4 color;
varying vec4 v_color;
void main() {
    gl_Position = vec4(position, 0.0, 1.0);
    gl_PointSize = 8.0;
    v_color = color;
}
"""
FRAG = """
varying vec4 v_color;
void main() { gl_FragColor = v_color; }
"""

N = 500
data = np.zeros(N, dtype=[('position', np.float32, 2),
                           ('color',    np.float32, 4)])
data['position'] = np.random.uniform(-0.9, 0.9, (N, 2))
data['color']    = np.random.uniform(0.3, 1.0, (N, 4))
data['color'][:, 3] = 1.0  # alpha=1

program = gloo.Program(VERT, FRAG)
program.bind(gloo.VertexBuffer(data))

canvas = app.Canvas(size=(600, 600), keys='interactive')

@canvas.connect
def on_draw(event):
    gloo.clear('black')
    program.draw('points')

@canvas.connect
def on_resize(event):
    gloo.set_viewport(0, 0, *event.size)

canvas.show()
app.run()
```

### Animacion eficiente con `.set_data()`

```python
t = 0.0

@canvas.connect
def on_draw(event):
    global t
    t += 0.02
    data['position'][:, 0] = np.sin(np.linspace(0, 2*np.pi, N) + t) * 0.8
    buf.set_data(data)   # solo re-sube, no recrea
    gloo.clear('black')
    program.draw('points')
    canvas.update()
```

## Metodos y atributos

| Metodo / Atributo | Descripcion |
|-------------------|-------------|
| `VertexBuffer(data)` | Crea y sube el array a GPU |
| `.set_data(new_data)` | Actualiza el contenido del buffer en GPU (eficiente en animacion) |

## Errores comunes

| Error | Causa | Solucion |
|-------|-------|----------|
| Datos corruptos o artefactos | `dtype` incorrecto (e.g. `float64` en vez de `float32`) | Asegurar `dtype=np.float32` o el dtype exacto del shader |
| `AttributeError` al hacer `bind` | El structured array tiene campos que no existen en el shader | Los nombres del dtype deben coincidir exactamente con los `attribute` del vertex shader |
| Alta latencia en animacion | Se crea un `VertexBuffer` nuevo cada frame | Crear el buffer una vez y usar `.set_data()` para actualizar |

## Notas relacionadas

- [[Program]] — el Program que consume este buffer via `program['attr'] = buf` o `program.bind(buf)`
- [[concepto_gloo_pipeline]] — donde encaja el buffer en el pipeline vertex → rasterizacion → fragment
- [[Texture2D]] — alternativa para datos 2D indexados (imagen, campo escalar)
