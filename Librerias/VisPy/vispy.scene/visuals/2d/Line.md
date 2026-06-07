---
title: Line — visual de lineas y curvas
aliases: [Line, vispy line]
tags: [vispy, api/clase, scene/visuals]
lib: vispy
mod: vispy.scene.visuals
tipo: clase
requiere: [SceneCanvas, ViewBox]
draft: false
---

# Line — visual de lineas y curvas

Visual de alto nivel para dibujar lineas continuas o segmentos independientes sobre un
[[ViewBox]]. Es la pieza central para graficar funciones, trayectorias y datos de series
de tiempo en tiempo real.

## Importacion

```python
import vispy; vispy.use('pyqt5')
from vispy import scene, app
import numpy as np
```

Acceso recomendado: `scene.visuals.Line(...)` (API publica de scene).

## Constructor / Firma

```python
scene.visuals.Line(
    pos=None,          # array (N, 2) o (N, 3) float32 — obligatorio
    color='white',     # string CSS, tuple RGBA, o array (N, 4)
    width=1.0,         # grosor en pixeles (float)
    connect='strip',   # 'strip' | 'segments' | array bool (N-1,)
    method='gl',       # 'gl' | 'agg'
    antialias=False,   # bool — solo tiene efecto con method='agg'
    parent=None,       # nodo padre (view.scene para visuals normales)
)
```

## Parametros clave

### `pos`

| Forma | Shape | Uso |
|-------|-------|-----|
| 2D | `(N, 2)` float32 | coordenadas x, y |
| 3D | `(N, 3)` float32 | coordenadas x, y, z |

Siempre usar `dtype='float32'`; VisPy rechaza float64 en la mayoria de backends.

```python
t = np.linspace(0, 2 * np.pi, 500)
pos = np.column_stack([t, np.sin(t)]).astype('float32')
```

### `color`

| Tipo de valor | Ejemplo | Resultado |
|---------------|---------|-----------|
| String CSS | `'cyan'`, `'red'` | color uniforme |
| Tuple RGBA | `(1, 0.5, 0, 1)` | color uniforme |
| Array `(N, 4)` | `colores_por_punto` | color variable por vertice |

El array por punto permite gradientes o codificacion de magnitud.

### `connect`

| Valor | Comportamiento |
|-------|---------------|
| `'strip'` | linea continua; cada punto se conecta con el siguiente |
| `'segments'` | pares de puntos: (0,1), (2,3), (4,5)… — `N` debe ser par |
| array bool `(N-1,)` | control fino: `True` conecta, `False` rompe |

### `method`

| Valor | Velocidad | Calidad |
|-------|-----------|---------|
| `'gl'` | muy rapido (GPU nativo) | sin anti-aliasing |
| `'agg'` | mas lento (CPU-side) | anti-aliasing suavizado |

Para datos en tiempo real usa siempre `method='gl'`.

## Casos de uso

### Grafica de funcion

```python
canvas = scene.SceneCanvas(keys='interactive', show=True, size=(800, 600))
view = canvas.central_widget.add_view()
view.camera = 'panzoom'
view.camera.set_range(x=(0, 10), y=(-2, 2))

t = np.linspace(0, 10, 1000)
pos = np.column_stack([t, np.sin(t)]).astype('float32')
line = scene.visuals.Line(pos=pos, color='cyan', width=2, parent=view.scene)

app.run()
```

### Segmentos independientes

```python
# Dibuja 3 segmentos separados: (0,0)-(1,1), (2,0)-(3,1), (4,0)-(5,1)
pts = np.array([
    [0, 0], [1, 1],
    [2, 0], [3, 1],
    [4, 0], [5, 1],
], dtype='float32')
segs = scene.visuals.Line(pos=pts, color='orange', connect='segments', parent=view.scene)
```

### Actualizar en animacion

```python
def on_timer(event):
    phase = event.elapsed
    new_pos = np.column_stack([t, np.sin(t + phase)]).astype('float32')
    line.set_data(pos=new_pos)
    canvas.update()

timer = app.Timer(interval=1/60, connect=on_timer, start=True)
```

## Metodos y atributos

| Miembro | Tipo | Descripcion |
|---------|------|-------------|
| `.set_data(pos, color, width, connect)` | metodo | actualiza datos sin recrear el visual |
| `.pos` | atributo | array de posiciones actual |
| `.color` | atributo | color actual |
| `.width` | atributo | grosor actual |
| `.parent` | atributo | nodo padre en el scene graph |
| `.visible` | atributo | bool — ocultar/mostrar sin destruir |

## Errores comunes

| Error | Causa | Solucion |
|-------|-------|---------|
| Visual no aparece | `parent` no apunta a `view.scene` | verificar `parent=view.scene` |
| ValueError en pos | dtype float64 | convertir: `pos.astype('float32')` |
| Linea borrosa con `method='gl'` | comportamiento esperado | usar `method='agg'` o aceptarlo |
| N impar con `connect='segments'` | segmentos requieren pares | asegurar `len(pos) % 2 == 0` |

## Notas relacionadas

- [[Markers]]
- [[ViewBox]]
- [[SceneCanvas]]
- [[vispy.scene/visuals/2d/index\|Visuals 2D]]
