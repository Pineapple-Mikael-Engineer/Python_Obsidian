---
title: Manim — animacion matematica orientada a objetos
aliases:
  - Manim
  - manim
  - introduccion manim
tags:
  - manim
  - indice
order: 0
draft: false
---

# Manim — animación matemática orientada a objetos

Manim (Mathematical Animation Engine) es la librería que genera las animaciones matemáticas al estilo de 3blue1brown: figuras, fórmulas y gráficos que aparecen, se transforman y se mueven fotograma a fotograma. Documentamos la **Community Edition** (`pip install manim`), la versión mantenida por la comunidad. A diferencia de NumPy o Matplotlib —donde llamas funciones sobre datos— en Manim **subclaseas una `Scene` y escribes un guion** dentro de su método `construct()`: ahí vas añadiendo objetos y reproduciendo animaciones en orden. Es, como PyQt6, una librería intensamente **orientada a objetos**: casi todo lo dibujable hereda de `Mobject` y casi toda transformación hereda de `Animation`.

## La tríada: Scene, Mobject, Animation

Todo en Manim cae en uno de tres roles. No confundirlos es la clave de la librería:

| Rol | Qué es | Pregunta que responde |
|-----|--------|------------------------|
| **Scene** | el lienzo y el guion (`construct`) donde ocurre todo | *dónde* |
| **Mobject** | un objeto matemático dibujable (un círculo, una fórmula) | *qué se ve* |
| **Animation** | una transformación en el tiempo (aparecer, morfar, moverse) | *cómo cambia* |

Un `Circle` **no es** una animación: es un Mobject. `Create(Circle())` sí lo es. Dentro de la Scene se **añaden** los mobjects (`self.add`) o se **animan** (`self.play(Create(...))`).

## En acción

```python
from manim import *

class Hola(Scene):
    def construct(self):
        c = Circle(color=BLUE)              # 1. un Mobject
        texto = Text("Hola Manim")          # 2. otro Mobject
        texto.next_to(c, DOWN)              # 3. posicionar (sistema de coordenadas)

        self.play(Create(c))                # 4. una Animation
        self.play(Write(texto))             # 5. otra Animation
        self.play(c.animate.shift(RIGHT*2)) # 6. .animate: animar un cambio
        self.wait()                         # 7. pausa
```

```bash
manim -pql hola.py Hola      # -p reproduce, -ql = calidad baja (rapido)
```

## El modelo de objetos

Las dos grandes jerarquías —lo que se dibuja y lo que lo anima— cuelgan de `Mobject` y `Animation`; la `Scene` las orquesta:

```mermaid
classDiagram
    class Scene { +construct() +play() +add() +wait() }
    class Mobject { +shift() +move_to() +set_color() +scale() }
    class VMobject { +set_fill() +set_stroke() +points }
    class Animation { +run_time +rate_func +interpolate_mobject() }
    Mobject <|-- VMobject
    VMobject <|-- Circle
    VMobject <|-- Square
    VMobject <|-- Text
    VMobject <|-- MathTex
    VMobject <|-- Axes
    VMobject <|-- VGroup
    Animation <|-- Create
    Animation <|-- Write
    Animation <|-- FadeIn
    Animation <|-- Transform
    Transform <|-- ReplacementTransform
    Animation <|-- Rotate
```

> [!tip] La clave de la herencia
> Como **todo Mobject** hereda de `Mobject`/`VMobject`, todo objeto se puede posicionar (`shift`, `next_to`), colorear (`set_color`) y escalar sin importar si es un círculo o una fórmula. Como **toda animación** hereda de `Animation`, todas aceptan `run_time` y `rate_func`. Saber qué hereda una clase es saber qué puede hacer sin abrir su documentación.

## Los tres pilares

| Pilar | Idea | Concepto |
|-------|------|----------|
| **La Scene y `construct`** | subclaseas `Scene` y escribes el guion en `construct()` | [[concepto_scene_construct]] |
| **El Mobject** | el árbol de objetos dibujables; se añaden y se transforman | [[concepto_mobject]] |
| **La Animation** | `self.play(...)` reproduce una transformación en el tiempo | [[concepto_animation]] |

## Cómo navegar el vault

| Quiero… | Ir a |
|---------|------|
| El modelo mental (Scene, Mobject, Animation, coordenadas) | [[Manim/conceptos_transversales/index\|conceptos_transversales]] |
| El lienzo y su guion (Scene, play, add, wait) | [[Manim/escena/index\|escena]] |
| Los objetos dibujables (geometría, texto, gráficos) | [[Manim/mobjects/index\|mobjects]] |
| Las animaciones (crear, transformar, mover, indicar) | [[Manim/animaciones/index\|animaciones]] |
| Colocar y componer objetos | [[Manim/posicionamiento/index\|posicionamiento]] |
| Animación continua y reactiva (updaters, ValueTracker) | [[Manim/dinamico/index\|dinamico]] |
| Color, estilo y el comando de render | [[Manim/estilo/index\|estilo]] |
| Crear objetos o animaciones propios | [[Manim/patrones/index\|patrones]] |

## Notas relacionadas

- [[concepto_scene_construct]] — la Scene y el método `construct`
- [[concepto_mobject]] — el objeto dibujable base
- [[concepto_animation]] — qué es una animación y cómo se reproduce
