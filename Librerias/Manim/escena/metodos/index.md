---
title: métodos de Scene — los verbos de construct()
aliases:
  - métodos de Scene
  - metodos de escena
tags:
  - manim
  - indice
lib: manim
order: 1
draft: false
---

# métodos de Scene — los verbos de construct()

Esta carpeta reúne los **métodos de [[Scene]]** que se usan *dentro* de `construct`, siempre a través de `self` (la propia escena). No son funciones sueltas: son el vocabulario con el que escribes el guion de una animación. Cada línea de `construct` es, casi siempre, una llamada a uno de estos métodos —reproducir una animación, mostrar u ocultar un objeto, pausar, o reordenar capas—, y el **orden** en que los llamas es el orden temporal del vídeo (ver [[concepto_scene_construct]]). Conviene tener clara una distinción que gobierna todos: `play` es lo único que **dura y se anima**; `add`, `remove` y los de orden son **instantáneos**.

## En accion

Una escena corta que usa los cuatro verbos de reproducción y uno de orden: añade un objeto, reproduce una animación, espera, reordena capas y quita un objeto.

```python
from manim import *

class Verbos(Scene):
    def construct(self):
        fondo = Square(color=GREY, fill_opacity=1).scale(2)
        punto = Dot(color=YELLOW)

        self.add(fondo)                  # mostrar al instante
        self.play(Create(punto))         # reproducir (animado)
        self.wait()                      # pausar
        self.bring_to_front(punto)       # orden: el punto, encima del fondo
        self.wait()
        self.remove(fondo)              # quitar al instante
        self.wait()
```

```bash
manim -pql archivo.py Verbos   # -p reproduce, -ql = calidad baja (rapido)
```

## Los metodos

| Método | Firma | Qué hace |
|--------|-------|----------|
| [[Scene.play]] | `self.play(*anims, run_time=..., **kwargs)` | reproduce una o varias **Animations**; es lo único que dura y se anima |
| [[Scene.add]] | `self.add(*mobjects)` | muestra uno o varios Mobjects **al instante**, sin animación |
| [[Scene.wait]] | `self.wait(duration=1.0)` | pausa `duration` segundos manteniendo el último fotograma |
| [[Scene.remove]] | `self.remove(*mobjects)` | quita Mobjects de la escena **al instante** (lo inverso de `add`) |
| [[Scene.bring_to_front]] | `self.bring_to_front(*mobjects)` | pone los Mobjects **encima de todo** (cambia el z-order) |

Junto a `bring_to_front` está su pareja `self.bring_to_back(*mobjects)`, que manda los objetos **detrás de todo** (documentada en la misma nota). Y para vaciar la escena de golpe existe `self.clear()`, que quita *todos* los Mobjects de una vez.

## Dos grupos

Los métodos de `Scene` se entienden mejor en dos familias según para qué sirven:

### Reproducir / mostrar

Los verbos que construyen el guion temporal: meter objetos, animarlos, pausar y sacarlos.

| Método | Instantáneo o animado |
|--------|-----------------------|
| [[Scene.play]] | **animado** (dura `run_time` segundos) |
| [[Scene.add]] | instantáneo |
| [[Scene.wait]] | pausa (mantiene el fotograma) |
| [[Scene.remove]] | instantáneo |

### Orden de dibujado (z-order)

No cambian *qué* hay ni *cuándo*, sino *qué se ve delante* cuando dos Mobjects se solapan.

| Método | Efecto |
|--------|--------|
| [[Scene.bring_to_front]] | lleva los objetos al frente (encima de todo) |
| `bring_to_back` | manda los objetos al fondo (detrás de todo) |

## Notas relacionadas

- [[Scene]] — la clase que aporta todos estos métodos vía `self`.
- [[concepto_scene_construct]] — el modelo mental: `add`/`remove` instantáneos frente a `play`.
- [[concepto_animation]] — lo que `self.play` reproduce.
- [[Manim/index|Manim]] — el índice raíz de la librería.
