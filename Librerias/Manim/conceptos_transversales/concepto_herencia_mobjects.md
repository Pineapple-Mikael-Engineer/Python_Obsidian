---
title: herencia — subclasear para crear lo propio
aliases:
  - herencia
  - subclasear
  - mobject propio
  - animation propia
tags:
  - manim
  - concepto
order: 7
lib: manim
tipo: concepto
requiere:
  - concepto_mobject
draft: false
---

# herencia — subclasear para crear lo propio

En Manim, la forma natural de crear **algo propio** —un objeto reutilizable o una animación a medida— no es escribir funciones sueltas, sino **subclasear**, exactamente igual que ya subclaseas `Scene` para escribir una escena. Si quieres un objeto nuevo, heredas de `VMobject`; si quieres una animación nueva, heredas de `Animation`. Esta es la misma idea que gobierna toda la librería: Manim es intensamente orientada a objetos, y **encajar lo tuyo en sus jerarquías te regala todo lo que esas jerarquías ya saben hacer**. Un objeto que hereda de `VMobject` puede, sin que escribas una línea más, posicionarse, colorearse, escalarse y animarse con `Create(...)`; una animación que hereda de `Animation` obtiene gratis `run_time` y `rate_func`. Subclasear es, en Manim, la puerta de entrada a lo personalizado.

## Por qué existe

Manim ya sabe cómo **posicionar** cualquier `Mobject` (`shift`, `next_to`, `to_edge`), cómo **colorearlo** (`set_color`, `set_fill`), cómo **escalarlo y rotarlo**, y cómo **animarlo** (`Create`, `Transform`, `.animate`). Toda esa maquinaria vive en las clases base. Si crearas tu objeto como una función que devuelve formas sueltas, tendrías que reimplementar o cablear a mano cada uno de esos comportamientos. Al **heredar** de `VMobject`, en cambio, tu objeto *es* un mobject de pleno derecho: entra en la tríada Scene/Mobject/Animation por la puerta grande y todo el resto de la librería lo trata como a cualquier `Circle`. La herencia no es aquí un adorno de diseño: es **el mecanismo de extensión** previsto por Manim.

```python
# Un objeto propio NO es una funcion que devuelve formas;
# es una CLASE que hereda de VMobject y, por tanto, sabe moverse, colorearse y animarse sola.
from manim import *

class Diana(VMobject):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)               # PRIMERO: inicializa la maquinaria heredada
        for r, col in [(1.2, RED), (0.8, WHITE), (0.4, RED)]:
            self.add(Circle(radius=r, color=col, fill_opacity=1))
```

```bash
manim -pql archivo.py UsarDiana      # (ver el ejemplo de mas abajo)
```

## El modelo: dos jerarquías, dos formas de subclasear

Recuerda la tríada: `Scene` (el lienzo), `Mobject` (lo que se ve) y `Animation` (cómo cambia). Crear algo propio es **insertar una clase tuya** en una de esas dos últimas jerarquías.

| Quieres crear… | Heredas de | Lo esencial que defines |
|----------------|------------|--------------------------|
| Un **objeto** dibujable propio | `VMobject` | su geometría en `__init__` (tras `super().__init__()`) |
| Una **animación** propia | `Animation` | `interpolate_mobject(self, alpha)` |

### Regla de oro del Mobject propio: `super().__init__()` primero

Cuando subclaseas `VMobject`, lo **primero** dentro de `__init__` debe ser `super().__init__(**kwargs)`. Esa llamada inicializa toda la estructura interna del mobject (su lista de puntos, sus submobjects, su estilo). Si construyes tu geometría **antes** de llamarla, Manim borrará o no registrará lo que hayas añadido, y obtendrás objetos vacíos o errores difíciles de leer. El `**kwargs` que recibes y reenvías es lo que permite que quien use tu clase pueda pasarle `color=...`, `stroke_width=...` y demás estilo estándar.

Hay dos maneras de definir la geometría dentro de `__init__`:

| Técnica | Cómo | Cuándo |
|---------|------|--------|
| **Componer** otros mobjects | `self.add(Circle(), Line(), ...)` | tu objeto es un *conjunto* de piezas (lo más común) |
| **Fijar puntos** a mano | `self.set_points_as_corners([...])` / `self.start_new_path(...)` | tu objeto es una *forma nueva* trazada punto a punto |

### Regla de oro de la Animation propia: `interpolate_mobject(alpha)`

Una animación en Manim es, en el fondo, una función del **progreso** `alpha`, que va de `0` (inicio) a `1` (final). Al subclasear `Animation`, defines `interpolate_mobject(self, alpha)`: el método que dice **cómo se ve el mobject en el instante `alpha`**. Manim te llama a este método muchas veces por segundo, con `alpha` creciendo de 0 a 1 según el `run_time` y el `rate_func`, y compone los fotogramas con lo que tú dibujes. El mobject que animas está en `self.mobject`.

## Ejemplos progresivos

### Nivel 1: un VMobject compuesto reutilizable

El caso más frecuente: agrupar varias piezas en una clase con nombre propio. Aquí, una "diana" de círculos concéntricos.

```python
from manim import *

class Diana(VMobject):
    def __init__(self, radio=1.2, **kwargs):
        super().__init__(**kwargs)
        anillos = [(radio, RED), (radio * 0.66, WHITE), (radio * 0.33, RED)]
        for r, col in anillos:
            self.add(Circle(radius=r, color=col, fill_opacity=1, stroke_width=2))

class UsarDiana(Scene):
    def construct(self):
        d = Diana()
        self.play(Create(d))   # Create funciona GRATIS: Diana es un VMobject
        self.wait()
```

```bash
manim -pql archivo.py UsarDiana
```

No hemos escrito nada sobre cómo "crear" o "animar" la diana: por heredar de `VMobject`, `Create(d)` ya sabe trazarla.

### Nivel 2: usarlo como cualquier otro mobject

Lo prometido por la herencia: la clase propia se posiciona, colorea, escala y anima igual que un `Circle`.

```python
from manim import *

class Diana(VMobject):
    def __init__(self, radio=1.2, **kwargs):
        super().__init__(**kwargs)
        for r, col in [(radio, RED), (radio * 0.66, WHITE), (radio * 0.33, RED)]:
            self.add(Circle(radius=r, color=col, fill_opacity=1, stroke_width=2))

class DianaEnAccion(Scene):
    def construct(self):
        d = Diana().to_edge(LEFT)            # to_edge: heredado de Mobject
        self.play(Create(d))
        self.play(d.animate.shift(RIGHT * 4))  # .animate: heredado
        self.play(d.animate.scale(0.5).rotate(PI / 6))  # scale/rotate: heredados
        self.wait()
```

```bash
manim -pql archivo.py DianaEnAccion
```

### Nivel 3: un objeto que agrupa una figura y su etiqueta

Una composición útil: una clase que junta una forma con un rótulo, de modo que mover el conjunto mueve ambos a la vez.

```python
from manim import *

class FiguraRotulada(VMobject):
    def __init__(self, figura, texto, **kwargs):
        super().__init__(**kwargs)
        rotulo = Text(texto).scale(0.5).next_to(figura, DOWN, buff=0.2)
        self.add(figura, rotulo)             # ambos quedan dentro del mismo mobject

class Rotulada(Scene):
    def construct(self):
        item = FiguraRotulada(Square(color=BLUE, fill_opacity=0.5), "cuadro")
        self.play(FadeIn(item))
        self.play(item.animate.shift(UP * 2))  # se mueven figura Y etiqueta juntas
        self.wait()
```

```bash
manim -pql archivo.py Rotulada
```

Como ambos hijos viven dentro del mismo `VMobject`, cualquier transformación del conjunto (`shift`, `scale`) afecta a los dos sin esfuerzo extra. Para composiciones sueltas (sin clase propia) suele bastar un [[VGroup]]; crear una subclase compensa cuando quieres **darle un nombre, un constructor con parámetros y reutilizarlo**.

### Nivel 4 (avanzado): una Animation propia con `interpolate_mobject`

Cuando ninguna animación de fábrica hace lo que quieres, heredas de `Animation` y describes el fotograma en función de `alpha`. Aquí, un mobject que aparece girando y creciendo a la vez.

```python
from manim import *

class GirarYCrecer(Animation):
    def __init__(self, mobject, vueltas=1, **kwargs):
        self.vueltas = vueltas
        self.copia_base = mobject.copy()     # el estado de partida, para no acumular
        super().__init__(mobject, **kwargs)

    def interpolate_mobject(self, alpha):
        # alpha va de 0 a 1: definimos como se ve el mobject en cada instante
        self.mobject.become(self.copia_base)
        self.mobject.scale(alpha if alpha > 0 else 0.001)
        self.mobject.rotate(self.vueltas * TAU * alpha)

class AnimPropia(Scene):
    def construct(self):
        estrella = Star(color=YELLOW, fill_opacity=1)
        self.play(GirarYCrecer(estrella, vueltas=2), run_time=2)  # run_time: heredado de Animation
        self.wait()
```

```bash
manim -pql archivo.py AnimPropia
```

No tocamos el reloj ni los FPS: solo decimos *cómo se ve en el progreso `alpha`*, y Manim reparte ese progreso de 0 a 1 según `run_time` y `rate_func`, ambos heredados de `Animation`.

## Casos que fallan

| Síntoma | Causa | Solución |
|---------|-------|----------|
| El objeto sale vacío o no aparece | construiste la geometría **antes** de `super().__init__()`, que la borró | llama `super().__init__(**kwargs)` como **primera** línea de `__init__` |
| `TypeError: __init__() got an unexpected keyword argument 'color'` | no recibes ni reenvías `**kwargs`, y el estilo estándar no llega a la base | firma `def __init__(self, ..., **kwargs)` y `super().__init__(**kwargs)` |
| La animación propia "acumula" rotaciones/escala cada fotograma | en `interpolate_mobject` modificas el mobject ya modificado del fotograma anterior | parte siempre de una copia base (`self.mobject.become(self.copia_base)`) |
| `Create(MiObjeto())` no anima nada | heredaste de `Mobject` (sin puntos/trazo) en vez de `VMobject` | hereda de `VMobject` para objetos con contorno/relleno |
| La animación propia da error al construirla | olvidaste pasar el mobject a `super().__init__(mobject, ...)` | una `Animation` siempre se inicializa con el mobject que anima |
| `scale(0)` lanza error o deja el objeto invisible para siempre | escalar exactamente a 0 es degenerado | arranca desde un valor mínimo (`alpha if alpha > 0 else 0.001`) |

## Relación con otros conceptos

- [[concepto_mobject]] — la clase base de todo lo dibujable; tu objeto propio hereda de `VMobject`, una de sus ramas.
- [[concepto_animation]] — la jerarquía de la que cuelga una animación propia; al heredar obtienes `run_time` y `rate_func`.
- [[mobject_personalizado]] — la receta práctica (patrón) para construir un `VMobject` propio paso a paso.
- [[animacion_personalizada]] — la receta práctica para escribir una `Animation` con `interpolate_mobject`.
