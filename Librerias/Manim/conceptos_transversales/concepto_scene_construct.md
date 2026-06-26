---
title: la Scene y construct() — el lienzo y el guion
aliases:
  - Scene
  - construct
  - scene construct
tags:
  - manim
  - concepto
order: 1
lib: manim
tipo: concepto
requiere:
  - concepto_mobject
draft: false
---

# la Scene y construct() — el lienzo y el guion

En Manim no se "dibuja" llamando funciones sueltas: se **subclasea `Scene`** y se escribe un **guion**
dentro de su metodo `construct()`. Ese metodo es el corazon de toda animacion — Manim lo ejecuta de
arriba a abajo, y cada `self.play(...)` o `self.add(...)` que encuentra se convierte en un trozo del
video final. La `Scene` es a la vez el **lienzo** (el espacio donde viven los objetos) y el **director**
(quien decide que ocurre y en que orden).

## Por que existe

Una animacion es una secuencia ordenada de cambios en el tiempo. Necesitas un sitio donde declarar
*que objetos hay* y *que les pasa, y cuando*. En vez de un API imperativo disperso, Manim te da una
clase que sobreescribes: el orden de las lineas de `construct()` **es** el orden temporal del video.
Leer el `construct` es leer el guion.

```python
# No existe una funcion suelta "anima_esto()".
# Defines una Scene y describes el guion en construct():
from manim import *

class MiPrimera(Scene):
    def construct(self):
        ...   # aqui va todo: crear objetos, reproducir animaciones, pausar
```

## El modelo: cuatro verbos dentro de construct

Casi todo `construct` se escribe con cuatro metodos de `self` (la Scene):

| Metodo | Que hace | Anima? |
|--------|----------|--------|
| `self.add(mobj)` | pone un Mobject en pantalla **al instante** | no |
| `self.play(anim)` | reproduce una **Animation** (dura `run_time` seg) | si |
| `self.wait(t)` | pausa `t` segundos (1 por defecto) | — |
| `self.remove(mobj)` | quita un Mobject al instante | no |

La regla mental: **`add` y `remove` son instantaneos; `play` es lo que dura y se ve animarse.**

## Ejemplos progresivos

### Nivel 1: la Scene minima

```python
from manim import *

class Minima(Scene):
    def construct(self):
        self.play(Create(Circle()))   # crea un circulo animadamente
        self.wait()
```

```bash
manim -pql archivo.py Minima
```

### Nivel 2: add (instantaneo) vs play (animado)

```python
from manim import *

class AddVsPlay(Scene):
    def construct(self):
        cuadro = Square(color=BLUE)
        self.add(cuadro)               # aparece de golpe, sin animacion
        self.wait()
        self.play(cuadro.animate.shift(RIGHT * 2))  # ahora SI se ve moverse
        self.wait()
```

El `Square` esta en pantalla desde el primer frame (lo anadimos con `add`). El desplazamiento, en
cambio, se anima porque va dentro de `play` con `.animate` (ver [[concepto_animate_syntax]]).

### Nivel 3: un guion con varios pasos

```python
from manim import *

class Guion(Scene):
    def construct(self):
        titulo = Text("Teorema").to_edge(UP)
        formula = MathTex("a^2 + b^2 = c^2")

        self.play(Write(titulo))           # 1. escribe el titulo
        self.play(FadeIn(formula))         # 2. aparece la formula
        self.wait(0.5)
        self.play(formula.animate.scale(1.5).set_color(YELLOW))  # 3. la agranda y colorea
        self.wait()
        self.play(FadeOut(titulo, formula))  # 4. todo desaparece
```

El orden de los `self.play` es el orden del video: titulo, formula, enfasis, salida.

## Variantes de Scene

`Scene` es la base 2D. Para casos especiales se subclasea una variante (que a su vez hereda de
`Scene`), y cambia lo que `self` puede hacer:

| Clase | Para que | Aporta |
|-------|----------|--------|
| `Scene` | animacion 2D normal | lo basico |
| `MovingCameraScene` | mover/zoomear la camara | `self.camera.frame` animable |
| `ThreeDScene` | escenas 3D | `self.set_camera_orientation(...)` |
| `ZoomedScene` | recuadro con zoom | una mini-camara |

## Casos que fallan

| Error | Causa | Solucion |
|-------|-------|----------|
| No se ve nada / video vacio | olvidaste `self.add` o `self.play`; el objeto nunca entro a la Scene | anade o reproduce el mobject |
| `construct() takes 1 positional argument` | escribiste `def construct():` sin `self` | siempre `def construct(self):` |
| Todo aparece de golpe | usaste `self.add` esperando animacion | usa `self.play(Create(...))` / `.animate` |
| El objeto se mueve sin animarse | hiciste `mobj.shift(...)` fuera de `play` | mete el cambio en `self.play(mobj.animate.shift(...))` |
| `NameError: Circle` | falto el import | `from manim import *` al inicio |

## Relacion con otros conceptos

- [[concepto_mobject]] — los objetos que se anaden a la Scene
- [[concepto_animation]] — lo que `self.play` reproduce
- [[concepto_animate_syntax]] — `.animate` para animar un cambio dentro de `play`
- [[concepto_render_cli]] — como se convierte el `construct` en un video (`manim -pql`)
