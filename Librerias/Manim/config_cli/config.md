---
title: config — el objeto global de ajustes del render
aliases:
  - config
  - manim config
  - tempconfig
tags:
  - manim
  - api/config
  - config_cli
lib: manim
tipo: config
order: 1
draft: false
---

# config — el objeto global de ajustes

`config` es el objeto global que guarda **todos** los ajustes del render: resolución, FPS, color de fondo, nombre de salida, directorios de `media/`, formato, calidad... Es la otra cara de la [[cli]]: lo que pasas por flags al ejecutar `manim` no hace más que **escribir en este objeto**. Su ventaja es que puedes tocarlo **desde el propio script**, antes de que arranque el render, para fijar un ajuste de forma permanente sin tener que recordar pasar el flag cada vez. El concepto general de las dos vías está en [[concepto_render_cli]].

## Importacion

`config` es una única instancia compartida. Llega de dos maneras equivalentes:

```python
from manim import config        # importarlo explicitamente
```

```python
from manim import *             # config ya queda disponible (esta en el namespace)
```

Con el `import *` habitual de Manim no hace falta importarlo aparte: `config` ya está en el espacio de nombres. En ambos casos es **el mismo objeto**; modificarlo afecta a todo el render.

## Atributos clave

Los ajustes que más se tocan desde el script. Cada uno tiene su flag equivalente en la [[cli]].

| Atributo | Controla | Ejemplo |
|----------|----------|---------|
| `background_color` | color de fondo del lienzo | `config.background_color = "#1e1e1e"` |
| `frame_rate` | los FPS de salida | `config.frame_rate = 30` |
| `pixel_height` / `pixel_width` | resolución en **píxeles** | `config.pixel_width = 1920` |
| `quality` | calidad por nombre | `config.quality = "high_quality"` |
| `frame_width` / `frame_height` | tamaño del lienzo en **unidades de escena** | `config.frame_width = 16` |
| `disable_caching` | desactivar la caché de animaciones | `config.disable_caching = True` |
| `output_file` | nombre del archivo de salida | `config.output_file = "intro_final"` |

> [!warning] `frame_*` (unidades) NO es `pixel_*` (píxeles)
> `frame_width`/`frame_height` miden el lienzo en **unidades de escena** (las mismas en que se posicionan los Mobjects: por defecto el alto es 8 unidades). `pixel_width`/`pixel_height` miden la **resolución en píxeles** del vídeo. Cambiar `frame_width` hace que quepa *más o menos escena* (zoom); cambiar `pixel_width` cambia la *nitidez/resolución*. Son cosas distintas.

## Formas de fijar config

Hay tres maneras de escribir en `config`, según si el ajuste es para todo el script, para un bloque, o ya viene dado por la CLI.

### Desde el script

La forma directa: asignas el atributo **antes** de que arranque el render (típicamente arriba del archivo, tras los imports). Vale para todas las escenas del archivo.

```python
from manim import *

config.background_color = "#1e1e1e"   # fondo gris oscuro para todo el archivo
config.frame_rate = 30
```

### Con un context manager

`tempconfig` aplica unos ajustes **solo dentro del bloque `with`** y los revierte al salir. Útil para renderizar una escena con una config distinta sin tocar el resto.

```python
from manim import tempconfig

with tempconfig({"background_color": "#1e1e1e", "frame_rate": 30}):
    ...   # aqui dentro la config esta modificada; fuera vuelve a lo normal
```

### Equivalencia con la CLI

Cada flag de la [[cli]] no es más que un atajo que escribe un atributo de `config` al arrancar. Por eso las dos vías son intercambiables:

| Flag CLI | Atributo que fija |
|----------|-------------------|
| `-qh` | `config.quality = "high_quality"` |
| `-r 1920,1080` | `config.pixel_width = 1920`, `config.pixel_height = 1080` |
| `--fps 30` | `config.frame_rate = 30` |
| `-o intro` | `config.output_file = "intro"` |
| `--disable_caching` | `config.disable_caching = True` |

## Ejemplo

Una escena precedida de unas asignaciones a `config` que cambian el **fondo** y los **FPS**: al renderizar, el fondo ya sale gris oscuro y el vídeo va a 30 FPS sin pasar ningún flag de fondo por la terminal.

```python
from manim import *

config.background_color = "#1e1e1e"   # fondo gris oscuro
config.frame_rate = 30                # 30 FPS de salida

class Demo(Scene):
    def construct(self):
        c = Circle(color=BLUE, fill_opacity=0.4)
        t = Text("config global").next_to(c, DOWN)
        self.play(Create(c), Write(t))
        self.wait()
```

```bash
manim -pql archivo.py Demo      # el fondo y los FPS ya vienen de config
```

## Errores comunes

Los dos tropiezos típicos con `config`.

| Error | Causa | Solución |
|-------|-------|----------|
| El ajuste "no se aplica" | tocaste `config` **después** de que el render arrancó (dentro de `construct`, demasiado tarde) | asigna `config.*` **antes** de la clase / del render, o usa `tempconfig` |
| El zoom o la nitidez salen mal | confundiste `frame_width` (unidades de escena) con `pixel_width` (píxeles) | para resolución usa `pixel_*`; para cuánta escena cabe, `frame_*` |

## Notas relacionadas

- [[concepto_render_cli]] — el concepto: cómo CLI y `config` son dos caras del mismo render
- [[cli]] — los flags del comando `manim`, cada uno escribe un atributo de aquí
- [[config_cli/index | config_cli]] — la carpeta padre: las dos vías para controlar el render
- [[concepto_sistema_coordenadas]] — las unidades de escena en que miden `frame_width`/`frame_height`
