---
title: Texture2D — textura 2D en GPU
aliases:
  - Texture2D
  - gloo textura
  - textura vispy
tags:
  - vispy
  - api/clase
  - gloo
lib: vispy
mod: vispy.gloo
tipo: clase
retorna: Texture2D
requiere:
  - concepto_gloo_pipeline
draft: false
---

# Texture2D — textura 2D en GPU

`gloo.Texture2D` sube un array 2D numpy a GPU como textura OpenGL. El shader accede
a ella mediante un `uniform sampler2D` y la muestrea con coordenadas UV normalizadas
(`[0,1] x [0,1]`). Usala para mostrar imagenes, visualizar campos escalares 2D coloreados,
o implementar render-to-texture en efectos avanzados.

## Importacion

```python
from vispy import gloo
```

## Constructor / Firma

```python
tex = gloo.Texture2D(data, interpolation='nearest', wrapping='clamp_to_edge')
```

| Parametro | Tipo | Valores | Descripcion |
|-----------|------|---------|-------------|
| `data` | `np.ndarray` | shape `(H,W)`, `(H,W,3)`, `(H,W,4)` | Datos de la textura. `uint8` para imagenes, `float32` para datos cientificos |
| `interpolation` | `str` | `'nearest'`, `'linear'` | `'nearest'` = pixelado exacto; `'linear'` = suavizado bilineal |
| `wrapping` | `str` | `'clamp_to_edge'`, `'repeat'`, `'mirrored_repeat'` | Que ocurre al muestrear fuera de `[0,1]` |

## Parametros clave

### Formatos de `data`

```python
# Escala de grises — (H, W), dtype uint8 o float32
gray = np.random.randint(0, 256, (256, 256), dtype=np.uint8)
tex = gloo.Texture2D(gray)

# RGB — (H, W, 3), dtype uint8
img_rgb = np.random.randint(0, 256, (256, 256, 3), dtype=np.uint8)
tex = gloo.Texture2D(img_rgb)

# RGBA — (H, W, 4), dtype uint8
img_rgba = np.random.randint(0, 256, (256, 256, 4), dtype=np.uint8)
tex = gloo.Texture2D(img_rgba, interpolation='linear', wrapping='repeat')

# Datos float (campo escalar cientifico)
field = np.random.uniform(0, 1, (128, 128)).astype(np.float32)
tex = gloo.Texture2D(field, interpolation='linear')
```

### Asignacion al shader

En el vertex shader se generan o se reciben coordenadas UV; el fragment shader
las usa para muestrear la textura:

```glsl
// vertex shader
attribute vec2 position;
attribute vec2 texcoord;
varying vec2 v_texcoord;
void main() {
    gl_Position = vec4(position, 0.0, 1.0);
    v_texcoord = texcoord;
}

// fragment shader
uniform sampler2D tex;
varying vec2 v_texcoord;
void main() {
    gl_FragColor = texture2D(tex, v_texcoord);
}
```

```python
program['tex'] = tex   # asigna la Texture2D al uniform sampler2D
```

### `.set_data(new_data)` — actualizar frames

Para video o animacion de datos, re-subir sin recrear la textura:

```python
tex = gloo.Texture2D(frame0, interpolation='linear')
program['tex'] = tex

def on_timer(event):
    tex.set_data(siguiente_frame())   # re-sube a GPU
    canvas.update()
```

## Casos de uso

### Mostrar una imagen

```python
import vispy; vispy.use('pyqt5')
from vispy import app, gloo
import numpy as np

VERT = """
attribute vec2 position;
attribute vec2 texcoord;
varying vec2 v_tc;
void main() {
    gl_Position = vec4(position, 0.0, 1.0);
    v_tc = texcoord;
}
"""
FRAG = """
uniform sampler2D tex;
varying vec2 v_tc;
void main() {
    gl_FragColor = texture2D(tex, v_tc);
}
"""

# Quad que ocupa toda la ventana
data = np.zeros(4, dtype=[('position', np.float32, 2),
                           ('texcoord', np.float32, 2)])
data['position'] = [(-1,-1), (1,-1), (-1,1), (1,1)]
data['texcoord']  = [(0,1),  (1,1),  (0,0), (1,0)]   # Y invertida: OpenGL vs imagen

# Imagen sintetica 256x256 RGB
img = np.zeros((256, 256, 3), dtype=np.uint8)
img[:128, :128] = [255, 80, 0]    # naranja
img[128:, 128:] = [0, 120, 255]   # azul
img[:128, 128:] = [80, 200, 80]   # verde
img[128:, :128] = [200, 50, 200]  # magenta

program = gloo.Program(VERT, FRAG)
program.bind(gloo.VertexBuffer(data))
program['tex'] = gloo.Texture2D(img, interpolation='linear')

canvas = app.Canvas(size=(512, 512), keys='interactive')

@canvas.connect
def on_draw(event):
    gloo.clear('black')
    program.draw('triangle_strip')   # 4 vertices = 2 triangulos = 1 quad

@canvas.connect
def on_resize(event):
    gloo.set_viewport(0, 0, *event.size)

canvas.show()
app.run()
```

### Campo escalar coloreado (datos cientificos)

```python
# Mapa de calor con colormap manual en el shader
field = np.sin(np.linspace(0, 4*np.pi, 256))[:, None] * \
        np.cos(np.linspace(0, 4*np.pi, 256))[None, :]
field = ((field + 1) / 2 * 255).astype(np.uint8)   # normalizar a [0,255]
tex = gloo.Texture2D(field, interpolation='linear')  # escala de grises
```

## Metodos y atributos

| Metodo / Atributo | Descripcion |
|-------------------|-------------|
| `Texture2D(data, ...)` | Crea y sube la textura a GPU |
| `.set_data(new_data)` | Actualiza el contenido sin recrear la textura (eficiente para video/animacion) |
| `program['nombre'] = tex` | Asigna la textura a un `uniform sampler2D` del shader |

## Errores comunes

| Error | Causa | Solucion |
|-------|-------|----------|
| Imagen volteada verticalmente | OpenGL tiene Y=0 abajo; las imagenes tienen Y=0 arriba | Invertir `texcoord` en Y (`v_tc.y = 1.0 - texcoord.y`) o hacer `np.flipud(img)` antes de subir |
| Textura negra o no aparece | El uniform `sampler2D` no esta asignado | Verificar `program['nombre'] = tex` antes de la primera draw call |
| Artefactos en bordes | `wrapping='repeat'` cuando se esperaba clamp | Cambiar a `wrapping='clamp_to_edge'` |
| `ValueError` al subir float64 | La GPU no acepta float64 nativo | Convertir con `.astype(np.float32)` |

## Notas relacionadas

- [[Program]] — el Program al que se asigna la textura como uniform
- [[VertexBuffer]] — buffer paralelo que suministra las coordenadas UV (`texcoord`)
- [[concepto_gloo_pipeline]] — como encajan texturas y samplers en el pipeline OpenGL
