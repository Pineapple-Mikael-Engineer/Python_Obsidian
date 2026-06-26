---
title: config_cli — controlar la calidad y el render (CLI vs config)
aliases:
  - config_cli
  - render config
  - calidad render
tags:
  - manim
  - indice
lib: manim
order: 8
draft: false
---

# config_cli — controlar la calidad y el comportamiento del render

Una vez escrita la `Scene`, queda decidir **cómo** se renderiza: a qué resolución, a cuántos FPS, sobre qué color de fondo, con qué nombre de salida y en qué formato. Manim ofrece **dos caras de un mismo volante** para gobernar todo eso. La primera es la **línea de comandos**: pasas flags al ejecutar (`manim -pqh archivo.py Demo`), son ajustes **efímeros** que valen solo para esa ejecución y no tocan tu código —ideales para iterar—. La segunda es el objeto **`config`**: una variable global que guarda *todos* esos ajustes y que puedes escribir **desde el propio script** (`config.background_color = "#1e1e1e"`), de modo que el ajuste queda **fijo y versionado** junto a la escena. No son dos sistemas rivales sino el mismo: cada flag de la CLI no hace más que escribir un atributo de `config`. Esta carpeta documenta las dos vías en detalle —[[cli]] y [[config]]— y son la referencia ampliada del concepto [[concepto_render_cli]], que explica el flujo completo de `construct()` al vídeo.

## En accion

El mismo script, renderizado de dos maneras: **en baja** para iterar (segundos por render) y **en alta** para la entrega final (1080p60). La escena no cambia; solo cambia *cómo* la lanzas. Y cada flag de calidad tiene su equivalente exacto en `config`, así que lo que escribes en la terminal podrías fijarlo en el código.

```python
from manim import *

class Demo(Scene):
    def construct(self):
        c = Circle(color=BLUE, fill_opacity=0.4)
        t = Text("hola").next_to(c, DOWN)
        self.play(Create(c), Write(t))
        self.wait()
```

Mientras desarrollas, en baja calidad (rápido):

```bash
manim -pql archivo.py Demo      # -p reproduce, -ql = 480p15
```

Para la entrega, en alta calidad (lento pero definitivo):

```bash
manim -pqh archivo.py Demo      # -qh = 1080p60
```

Ese `-qh` es exactamente equivalente a fijar la calidad desde el script con `config`:

```python
from manim import *

config.quality = "high_quality"   # equivale al flag -qh

class Demo(Scene):
    def construct(self):
        ...
```

## Las dos vias

Las mismas decisiones de render se pueden tomar por dos caminos; eliges según si el ajuste es de "esta ejecución" o "de este proyecto".

| Via | Cuando | Nota |
|-----|--------|------|
| [[cli]] (flags del comando `manim`) | iterar, probar calidades, un render puntual | efímero: solo afecta a esa ejecución; no toca el código; lo más cómodo del día a día |
| [[config]] (el objeto global) | parámetros propios de la escena/proyecto | persistente: queda fijo en el script y se versiona; lo que escribe cada flag por dentro |

## Como elegir

La regla mental: **lo que cambia entre ejecución y ejecución va por la CLI; lo que es propio de la escena va en `config`**.

- Usa la **CLI** para el día a día y para iterar: la calidad (`-ql` mientras trabajas, `-qh` al final), el preview (`-p`), un formato puntual (`--format gif`), un frame suelto (`-s`). Son decisiones que cambias a cada rato y que no quieres clavar en el código.
- Usa **`config`** cuando un ajuste es **parte de la escena** y debe valer siempre: un color de fondo concreto, unos FPS especiales, un tamaño de lienzo a medida. Lo escribes una vez en el script y deja de depender de que recuerdes el flag cada vez.
- Cuando un mismo ajuste lo pones por las dos vías, **gana el que se evalúa más tarde**: la CLI fija `config` al arrancar, pero una asignación a `config` en tu script (que corre después, al importar) puede sobreescribirla.

## Recetas

Los cuatro lanzamientos que cubren casi todo el trabajo, todos sobre una escena llamada `Demo`.

### Render rápido de prueba (iterar)

Baja calidad y preview: el render tarda segundos y se reproduce solo al terminar. Es el comando que más teclearás.

```bash
manim -pql archivo.py Demo      # 480p15, se abre al acabar
```

### Render final en alta

Alta calidad (1080p60) para la versión de entrega. Más lento, pero es el resultado bueno.

```bash
manim -pqh archivo.py Demo      # 1080p60
```

### Exportar un GIF

Mismo render, pero la salida es un `.gif` animado en vez de `.mp4` (cómodo para incrustar en chat o web). El `--format gif` es la pieza clave.

```bash
manim -pql --format gif archivo.py Demo
```

### Guardar el último frame como imagen

Con `-s` Manim **no genera vídeo**: ejecuta el `construct()` y guarda solo el último fotograma como `.png`. Es la forma más rápida de ajustar la *composición* (posiciones, colores, tamaños) sin esperar el render completo.

```bash
manim -s archivo.py Demo        # solo el ultimo frame, en media/images/
```

## Notas relacionadas

- [[concepto_render_cli]] — el concepto base: qué pasa por dentro al ejecutar `manim`, del `construct()` al vídeo
- [[cli]] — la referencia completa de flags del comando `manim`
- [[config]] — el objeto global con todos los ajustes del render
- [[concepto_scene_construct]] — la `Scene` y el `construct()` que este render convierte en vídeo
- [[Manim/index | Manim]] — el índice raíz con el `classDiagram` global
