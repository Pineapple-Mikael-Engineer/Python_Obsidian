---
title: estilo — la apariencia (color, relleno, trazo y la curva del movimiento)
aliases:
  - estilo
  - apariencia
tags:
  - manim
  - indice
lib: manim
order: 7
draft: false
---

# estilo — la apariencia (color, relleno, trazo y la curva del movimiento)

Esta carpeta reúne lo que decide **cómo se ve** una escena: el **color** de las figuras, el **relleno** de su interior, el **grosor y color del trazo** de su borde, y la **curva de velocidad** con que se mueven. Es la diferencia entre una animación sosa —figuras grises de borde fino que se desplazan a velocidad mecánica— y una pulida —colores vivos, interiores translúcidos, bordes marcados y movimientos que arrancan y frenan con naturalidad—. Conviene separar dos planos desde el principio: el **color, el relleno y el trazo** son la apariencia *espacial* (cómo luce el objeto quieto, en cualquier fotograma), mientras que la **`rate_func`** es la apariencia *temporal* (cómo se reparte el movimiento en el tiempo, sin tocar el objeto). Casi todo lo del primer plano son **métodos heredados de [[VMobject]] que devuelven `self`** (`set_color`, `set_fill`, `set_stroke`), así que se encadenan y se animan con `.animate`; lo del segundo plano es un **parámetro de toda [[Animation]]** (`rate_func`), que se pasa a `self.play`. Aprender a estilizar un [[Circle]] es aprender a estilizar cualquier cosa, porque el repertorio es común a todo VMobject.

## En accion

Una escena que estiliza varias figuras —color por separado para relleno y borde, opacidad de relleno, grosor de trazo y un gradiente— y luego reproduce un desplazamiento con una `rate_func` distinta de la de por defecto, para que se vea de golpe que el estilo tiene un plano espacial (el aspecto) y un plano temporal (el movimiento).

```python
from manim import *

class EstiloEnAccion(Scene):
    def construct(self):
        # apariencia espacial: relleno e interior con opacidad, borde grueso de otro color
        c = Circle(radius=1.2)
        c.set_fill(BLUE, opacity=0.6)        # interior azul translucido
        c.set_stroke(WHITE, width=8)         # borde blanco grueso

        # un gradiente de relleno sobre un cuadrado
        s = Square(side_length=2).next_to(c, RIGHT, buff=1)
        s.set_color_by_gradient(YELLOW, RED, PURPLE)
        s.set_fill(opacity=0.8)

        self.play(Create(c), Create(s))
        # apariencia temporal: el mismo shift, pero va y vuelve en vez de ir y quedarse
        self.play(VGroup(c, s).animate.shift(UP * 1.5), rate_func=there_and_back, run_time=2)
        self.wait()
```

```bash
manim -pql archivo.py EstiloEnAccion      # -p reproduce, -ql = calidad baja (rapido)
```

## Que aporta

Las tres notas de la carpeta cubren los dos planos del estilo. Las dos primeras son apariencia espacial (color y forma del relleno/trazo); la tercera es apariencia temporal (la curva del movimiento).

| Tema | Para que |
|------|----------|
| [[colores]] | qué constantes de color hay (`RED`, `BLUE`…), cómo especificar un color (constante, hex, `ManimColor`) y cómo aplicarlo con `set_color`; incluye los gradientes |
| [[set_style]] | controlar **relleno** y **trazo** por separado con `set_fill` y `set_stroke` (color, opacidad, grosor); es lo que distingue interior de borde |
| [[rate_functions]] | el catálogo de curvas de velocidad (`smooth`, `linear`, `there_and_back`…) que cambian la **sensación** del movimiento sin tocar el objeto ni su duración |

## Como elegir

La primera decisión es siempre **espacial o temporal**: si cambias cómo *luce* el objeto, vas a color/relleno/trazo; si cambias cómo se *mueve*, vas a la `rate_func`.

### set_color vs set_fill / set_stroke

`set_color` (heredado de [[Mobject]]) es el atajo de brocha gorda: tiñe **relleno y trazo a la vez** con el mismo color. Sirve cuando no te importa distinguirlos —un borde rojo con interior rojo—. En cuanto quieras que el interior y el borde tengan **colores u opacidades distintos**, `set_color` se queda corto: ahí entran `set_fill` (solo el interior) y `set_stroke` (solo el borde), que viven en [[set_style]].

| Quiero… | Uso |
|---------|-----|
| Teñir todo el objeto de un color | `mob.set_color(RED)` |
| Solo el interior (color + opacidad) | `mob.set_fill(RED, opacity=0.7)` |
| Solo el borde (color + grosor) | `mob.set_stroke(YELLOW, width=8)` |
| Interior y borde de colores distintos | `set_fill(...)` **y** `set_stroke(...)` |
| Un degradado de varios colores | `mob.set_color_by_gradient(RED, YELLOW)` |

### Cuándo cambiar la rate_func

La `rate_func` por defecto es `smooth` (arranca y frena suave), que ya queda bien la mayoría de las veces. Cámbiala cuando el movimiento por defecto no transmita lo que quieres: `linear` para un ritmo constante y mecánico (un reloj, un barrido), `there_and_back` para un ida y vuelta (un rebote, un latido, un destello de posición), `rush_into`/`rush_from` para entradas o salidas con energía. Recuerda que la `rate_func` **no cambia la duración** (eso es `run_time`) ni el objeto: solo reparte el avance en el tiempo.

## Patrones y recetas

Tres recetas que se repiten al estilizar: distinguir relleno y borde, pintar un degradado, y dar carácter a un movimiento.

### Relleno y borde de colores distintos

El estilo "pulido" más típico: un interior translúcido de un color y un borde marcado de otro. Se consigue con `set_fill` y `set_stroke` por separado (encadenados, porque ambos devuelven `self`).

```python
from manim import *

class RellenoYBorde(Scene):
    def construct(self):
        s = Square(side_length=3)
        s.set_fill(BLUE, opacity=0.5).set_stroke(YELLOW, width=10)   # interior azul, borde amarillo grueso
        self.play(Create(s))
        self.wait()
```

```bash
manim -pql archivo.py RellenoYBorde
```

### Un gradiente de color

`set_color_by_gradient` reparte una lista de colores a lo largo del objeto. Combinado con `set_fill(opacity=...)`, el degradado se ve en el interior.

```python
from manim import *

class Gradiente(Scene):
    def construct(self):
        barra = Rectangle(width=6, height=1)
        barra.set_color_by_gradient(BLUE, GREEN, YELLOW, RED)   # de azul a rojo
        barra.set_fill(opacity=1.0)
        self.play(Create(barra))
        self.wait()
```

```bash
manim -pql archivo.py Gradiente
```

### Un movimiento con there_and_back

Para un rebote o un destello de posición sin escribir dos `play`, basta una `rate_func` que vaya y vuelva: el objeto sube y regresa solo dentro del mismo bloque.

```python
from manim import *

class Rebote(Scene):
    def construct(self):
        d = Dot(color=RED).shift(DOWN * 2)
        self.add(d)
        self.play(d.animate.shift(UP * 4), rate_func=there_and_back, run_time=1.5)   # sube y vuelve
        self.wait()
```

```bash
manim -pql archivo.py Rebote
```

## Notas relacionadas

- [[colores]] — las constantes de color, las formas de especificarlo y los gradientes
- [[set_style]] — `set_fill` y `set_stroke`: relleno y trazo por separado
- [[rate_functions]] — el catálogo de curvas de velocidad para el plano temporal
- [[VMobject]] — la clase donde viven `set_fill`, `set_stroke`, `fill_opacity` y `stroke_width`
- [[Animation]] — la clase cuyo parámetro `rate_func` controla la curva del movimiento
- [[Scene.play]] — donde se pasa la `rate_func` de un bloque entero
- [[Manim/index | Manim]] — el índice raíz con el `classDiagram` global
