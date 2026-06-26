---
title: Mobject — el objeto matemático dibujable
aliases:
  - Mobject
  - VMobject
  - mobject
tags:
  - manim
  - concepto
order: 2
lib: manim
tipo: concepto
requiere:
  - concepto_sistema_coordenadas
draft: false
---

# Mobject — el objeto matemático dibujable

`Mobject` (de *Mathematical Object*) es la **clase base de todo lo que se dibuja** en Manim: un círculo, una fórmula, un eje, un texto y hasta un grupo de cosas son, en el fondo, Mobjects. Si la [[concepto_scene_construct|Scene]] es el lienzo y el guion, el Mobject es el **actor**: la pieza concreta que aparece en pantalla y que se posiciona, se colorea, se escala y se transforma. La idea central es que **todo objeto dibujable hereda de `Mobject`**, así que todos comparten el mismo repertorio de métodos: aprender a mover y colorear un `Circle` es, literalmente, aprender a mover y colorear *cualquier* cosa de Manim. Por dentro, un Mobject no es más que dos cosas: sus `points` (la geometría que ocupa el espacio) y sus `submobjects` (sus hijos), y de esa segunda pieza nace que los Mobjects formen un **árbol** de objetos anidados.

## Por qué existe

Una animación necesita "cosas" que animar, y esas cosas deben tener un comportamiento común: todas ocupan una posición en el espacio, todas tienen un color, todas pueden crecer o girar. En vez de que cada figura reimplemente "moverse" o "colorearse" a su manera, Manim concentra ese comportamiento en una única clase base, `Mobject`, y deja que cada figura concreta solo aporte **su geometría**. El resultado es una regla mental potentísima: si sabes que algo es un Mobject, ya sabes que puedes hacerle `shift`, `scale`, `set_color` o `move_to` sin abrir su documentación. La librería entera se vuelve consultable porque comparte un tronco común.

```python
# Un Mobject NO se dibuja con una funcion suelta:
# es un objeto que se crea, se posiciona y luego se anima o se agrega.
from manim import *

class QueEsUnMobject(Scene):
    def construct(self):
        c = Circle()          # un Mobject (en concreto, un VMobject)
        c.set_color(BLUE)     # metodo heredado de Mobject
        c.shift(UP)           # otro metodo heredado de Mobject
        self.add(c)           # entra en la Scene
        self.wait()
```

```bash
manim -pql archivo.py QueEsUnMobject      # -p reproduce, -ql = calidad baja (rapido)
```

El `Circle` no sabe "moverse" por sí mismo: hereda `shift` de `Mobject`. Esa herencia es la que hace que el mismo código funcione igual sobre un círculo, sobre un texto o sobre una fórmula.

## El modelo: Mobject, VMobject y el árbol de hijos

### Mobject (base) vs VMobject (vectorizado)

Hay una distinción que conviene fijar desde el principio: `Mobject` es la base abstracta, pero **casi todo lo que usarás en la práctica es un `VMobject`** (*Vectorized Mobject*), una subclase que dibuja su geometría con **curvas de Bézier** y que por eso entiende de relleno y de trazo. `Circle`, `Square`, `Text`, `MathTex`, `Axes` y `VGroup` son todos VMobjects. La diferencia importa porque algunos métodos de estilo (`set_fill`, `set_stroke`) solo tienen sentido en algo vectorizado.

| Clase | Qué es | Aporta | Ejemplos |
|-------|--------|--------|----------|
| `Mobject` | la base abstracta de todo lo dibujable | posición, escala, giro, color, árbol de hijos | (rara vez se instancia directo) |
| `VMobject` | Mobject dibujado con curvas de Bézier | `fill`, `stroke`, `points` como Bézier | `Circle`, `Square`, `Text`, `MathTex`, `Axes`, `VGroup` |

La regla mental: **cuando pienses "una figura con borde y relleno", piensa `VMobject`**; `Mobject` es solo el ancestro del que todos heredan lo común. Otros tipos especiales (como `ImageMobject` para imágenes ráster) heredan de `Mobject` pero **no** de `VMobject`, y por eso no aceptan `set_stroke`.

### Las dos piezas internas: points y submobjects

Todo Mobject guarda su estado en dos atributos clave: `points` es **su propia geometría** (los puntos de las curvas de Bézier que lo forman) y `submobjects` es **la lista de sus hijos**, otros Mobjects que cuelgan de él. Esa segunda pieza es la que convierte la escena en un árbol.

| Atributo interno | Qué contiene | Para qué |
|------------------|--------------|----------|
| `points` | los puntos (Bézier) de **su** geometría | define la forma propia del objeto |
| `submobjects` | la lista de **hijos** (otros Mobjects) | anida objetos: un grupo, las letras de un texto, los ejes de un `Axes` |

Esto explica un detalle que sorprende: un `Text("Hola")` no es una mancha única, sino un Mobject **padre** cuyos `submobjects` son las letras; un `Axes` es un padre cuyos hijos son los dos ejes. Manipular el padre afecta a todos sus descendientes a la vez.

### El árbol y la familia

Como cada Mobject puede tener hijos, y cada hijo puede tener los suyos, los objetos de una escena forman un **árbol**. La consecuencia práctica gobierna casi todo el posicionamiento: **al transformar al padre, se transforman todos sus hijos**. Si mueves un grupo, sus miembros se mueven con él manteniendo sus posiciones relativas; si lo escalas, todo crece junto.

| Operación sobre el árbol | Qué hace |
|--------------------------|----------|
| `padre.add(hijo)` | añade `hijo` a los `submobjects` de `padre` |
| `padre.remove(hijo)` | lo saca del árbol del padre |
| `VGroup(a, b, c)` | crea un padre cuyos hijos son `a`, `b`, `c` |
| `mob.get_family()` | devuelve el mobject y **toda** su descendencia |
| transformar el padre (`shift`, `scale`, `rotate`) | arrastra a **toda** la familia |

`VGroup` es la forma más habitual de construir el árbol a mano: agrupa varios VMobjects en un único objeto que se mueve y se anima como una sola pieza (ver [[VGroup]]).

## Los métodos universales (heredados de Mobject)

Estos métodos los tiene **cualquier** Mobject, porque están definidos en la clase base. Son el vocabulario que no cambia entre un círculo y una fórmula. Aquí casi siempre se usa la versión **instantánea** (aplica el cambio de golpe); para **animar** ese mismo cambio se envuelve en `self.play(mob.animate.<metodo>(...))` (ver [[concepto_animate_syntax]]).

### Posicionar

Colocan el objeto en el espacio usando las constantes de dirección (`UP`, `DOWN`, `LEFT`, `RIGHT`, `ORIGIN`...) del [[concepto_sistema_coordenadas|sistema de coordenadas]].

| Método | Qué hace |
|--------|----------|
| `shift(vector)` | desplaza una cantidad **relativa** (`shift(RIGHT*2)`) |
| `move_to(punto_o_mob)` | lleva el **centro** a una posición **absoluta** |
| `next_to(mob, dir)` | lo coloca **al lado** de otro mobject en la dirección `dir` |
| `to_edge(dir)` / `to_corner(dir)` | lo pega a un borde o esquina del marco |
| `align_to(mob, dir)` | alinea un lado con el de otro mobject |

### Redimensionar y girar

| Método | Qué hace |
|--------|----------|
| `scale(factor)` | multiplica el **tamaño** por `factor` (2 = doble) |
| `rotate(angulo)` | **gira** el objeto (radianes: `PI/2`, `90*DEGREES`) |
| `stretch(factor, dim)` | estira solo en una dimensión (0 = x, 1 = y) |
| `flip(eje)` | refleja respecto a un eje |

### Colorear y estilizar

`set_color` está en `Mobject`; `set_fill` y `set_stroke` viven en `VMobject` (necesitan geometría vectorizada).

| Método | Qué hace | Definido en |
|--------|----------|-------------|
| `set_color(COLOR)` | tiñe relleno y trazo a la vez | `Mobject` |
| `set_fill(COLOR, opacity)` | controla el **relleno** y su opacidad | `VMobject` |
| `set_stroke(COLOR, width)` | controla el **borde** (color y grosor) | `VMobject` |
| `set_opacity(valor)` | transparencia global (0 a 1) | `Mobject` |

### Consultar (getters)

Devuelven información geométrica; son la base para colocar unos objetos respecto a otros.

| Método | Devuelve |
|--------|----------|
| `get_center()` | el punto central (vector `[x, y, z]`) |
| `get_width()` / `get_height()` | el ancho / alto que ocupa |
| `get_top()` / `get_bottom()` | el punto más alto / bajo |
| `get_left()` / `get_right()` | el punto más a la izquierda / derecha |
| `get_color()` | el color actual |

### Duplicar

| Método | Qué hace |
|--------|----------|
| `copy()` | devuelve una **copia independiente** (no comparte estado con el original) |

`copy()` es imprescindible cuando quieres conservar el estado original de un objeto antes de transformarlo (por ejemplo, para un `Transform` que parta de una réplica intacta).

## Ejemplos progresivos

### Nivel 1: los métodos universales sobre cualquier figura

Un mismo conjunto de métodos (`set_color`, `shift`, `scale`, `rotate`) aplicado a figuras distintas: todas responden igual porque todas son Mobjects.

```python
from manim import *

class MetodosUniversales(Scene):
    def construct(self):
        c = Circle().set_color(RED).shift(LEFT * 3)        # posicionar + colorear
        s = Square().set_color(GREEN).scale(0.5)           # escalar
        t = Triangle().set_color(BLUE).shift(RIGHT * 3).rotate(PI / 4)  # girar
        self.add(c, s, t)
        self.wait()
```

```bash
manim -pql archivo.py MetodosUniversales
```

### Nivel 2: el mismo método sobre un círculo y sobre una fórmula

La demostración de que la herencia funciona: `set_color` y `move_to` se comportan idéntico en un `Circle` (geometría) y en un `MathTex` (texto LaTeX), porque ambos heredan de `Mobject`. Requiere LaTeX instalado para `MathTex`.

```python
from manim import *

class HerenciaEnAccion(Scene):
    def construct(self):
        circulo = Circle()
        formula = MathTex("e^{i\\pi} + 1 = 0")

        # EXACTAMENTE los mismos metodos sobre objetos muy distintos:
        circulo.set_color(YELLOW).to_edge(LEFT)
        formula.set_color(YELLOW).to_edge(RIGHT)

        self.add(circulo, formula)
        self.wait()
```

```bash
manim -pql archivo.py HerenciaEnAccion
```

### Nivel 3: el árbol de submobjects con VGroup

Agrupamos tres figuras en un `VGroup` y transformamos el **grupo entero**: al escalar y girar el padre, los tres hijos lo siguen manteniendo su disposición relativa. Esa es la esencia del árbol de Mobjects.

```python
from manim import *

class ArbolDeMobjects(Scene):
    def construct(self):
        a = Circle(color=RED)
        b = Square(color=GREEN)
        c = Triangle(color=BLUE)

        grupo = VGroup(a, b, c).arrange(RIGHT, buff=0.5)  # hijos en fila
        self.play(Create(grupo))

        # mover/escalar/girar el PADRE arrastra a los tres hijos a la vez:
        self.play(grupo.animate.scale(1.5))
        self.play(grupo.animate.rotate(PI / 4))
        self.play(grupo.animate.shift(UP))
        self.wait()
```

```bash
manim -pql archivo.py ArbolDeMobjects
```

### Nivel 4: add() para anidar y get_center() para consultar

Construimos el árbol "a mano" con `mob.add(otro)` y usamos un getter (`get_center`) para colocar un objeto respecto a otro. Al mover el padre, el hijo que le añadimos viaja con él.

```python
from manim import *

class AnidarYConsultar(Scene):
    def construct(self):
        caja = Square(side_length=2, color=WHITE)
        punto = Dot(color=YELLOW).move_to(caja.get_center())  # getter: el centro de la caja

        caja.add(punto)              # punto pasa a ser HIJO de caja (entra en su arbol)
        self.add(caja)
        self.wait(0.5)

        # como punto es hijo de caja, se mueve y rota con ella:
        self.play(caja.animate.shift(RIGHT * 2).rotate(PI / 6))
        self.wait()
```

```bash
manim -pql archivo.py AnidarYConsultar
```

## Casos que fallan

| Error | Causa | Solución |
|-------|-------|----------|
| `set_stroke` / `set_fill` no hace nada o falla | el objeto es un `Mobject` no vectorizado (p. ej. `ImageMobject`) | usa un `VMobject`, o `set_opacity` para transparencia general |
| El objeto "salta" en vez de animarse | llamaste `mob.shift(...)` **fuera** de `self.play` (es instantáneo) | envuélvelo: `self.play(mob.animate.shift(...))` (ver [[concepto_animate_syntax]]) |
| Mover un hijo no mueve al padre | la herencia del árbol va **del padre a los hijos**, no al revés | mueve el padre (el `VGroup`), o saca el hijo del grupo |
| Transformar un original arruina una copia esperada | reutilizaste el mismo objeto en vez de `copy()` | guarda `original = mob.copy()` antes de transformar |
| El `VGroup` aparece amontonado en el centro | no lo ordenaste | usa `.arrange(...)` o posiciona cada hijo antes de agrupar |
| `set_color` colorea de más (relleno y borde) | `set_color` toca ambos; querías solo uno | usa `set_fill(...)` o `set_stroke(...)` por separado |

## Relación con otros conceptos

- [[concepto_scene_construct]] — los Mobjects se añaden (`self.add`) y se animan (`self.play`) dentro de la Scene.
- [[concepto_animation]] — toda animación opera **sobre** uno o varios Mobjects.
- [[concepto_animate_syntax]] — la sintaxis `.animate` convierte un método de Mobject en una animación.
- [[concepto_sistema_coordenadas]] — el espacio (`ORIGIN`, `UP`, `RIGHT`…) donde se posicionan los Mobjects.
- [[concepto_herencia_mobjects]] — la jerarquía completa de clases que cuelga de `Mobject`/`VMobject`.
- [[VGroup]] — el contenedor más usado para construir el árbol de submobjects.
