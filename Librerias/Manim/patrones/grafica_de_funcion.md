---
title: grafica de funcion — graficar una funcion con Axes y c2p
aliases:
  - grafica de funcion
  - graficar funcion
  - plot Axes
tags:
  - manim
  - patron
  - patrones
lib: manim
tipo: patron
order: 4
requiere:
  - Axes
  - concepto_sistema_coordenadas
draft: false
---

# gráfica de función — graficar una función con Axes y c2p

Esta receta resuelve la tarea estrella de Manim para matemáticas: dibujar unos ejes, graficar `y = f(x)` encima y colocar puntos, áreas o rectas **alineados con la curva**. La clave que lo gobierna todo es [[Axes]] junto con su método `c2p` (coords-to-point): los ejes viven escalados dentro de la escena, así que el punto matemático `(2, 4)` **no** está en la coordenada de escena `(2, 4)`; para pasar del mundo del gráfico al de la escena se usa `ax.c2p(x, y)` **siempre**. Úsala para cualquier visualización de cálculo o análisis: una curva con su punto, el área bajo ella, una recta tangente, rectángulos de Riemann o un punto que la recorre animado.

## El problema

Quieres graficar una función y poner cosas sobre la gráfica —un punto en su máximo, una etiqueta, el área bajo la curva— y que todo encaje exactamente con los ejes. El obstáculo es que los ejes están **escalados y posicionados** dentro del frame: si colocas un `Dot` en las coordenadas matemáticas a pelo (`Dot([2, 4, 0])`), cae en el sitio equivocado, casi siempre fuera de cuadro. Necesitas un puente entre las coordenadas del gráfico y las de la escena. Ese puente es `c2p`, y la receta consiste en crear los ejes, graficar con `plot` (que ya aplica `c2p` por dentro) y traducir con `c2p` todo lo que coloques a mano.

## La receta

Unos ejes, la curva `y = sin(x)`, sus etiquetas y un punto anclado **sobre** la curva en su máximo. El punto es lo único que colocamos a mano: por eso pasa por `ax.c2p(...)`; `plot` no lo necesita porque aplica la conversión internamente.

```python
from manim import *
import numpy as np

class GraficaSeno(Scene):
    def construct(self):
        # 1. los ejes: x_range e y_range son [min, max, step] en coords MATEMATICAS
        ax = Axes(
            x_range=[0, 2 * np.pi, np.pi / 2],
            y_range=[-1.5, 1.5, 0.5],
        )

        # 2. las etiquetas de los ejes (acepta texto o LaTeX)
        etiquetas = ax.get_axis_labels(x_label="x", y_label="y")

        # 3. la curva: plot recibe una funcion de Python y respeta la escala (c2p interno)
        curva = ax.plot(lambda x: np.sin(x), color=BLUE)

        # 4. un punto ANCLADO sobre la curva, en el maximo (PI/2, 1)
        #    OBLIGATORIO c2p: a pelo, (PI/2, 1) caeria fuera de los ejes
        maximo = Dot(ax.c2p(np.pi / 2, 1), color=YELLOW)

        self.play(Create(ax), Write(etiquetas))
        self.play(Create(curva))
        self.play(FadeIn(maximo))
        self.wait()
```

```bash
manim -pql archivo.py GraficaSeno      # -p reproduce, -ql = calidad baja (rapido)
```

## Como funciona

Tres piezas hacen el trabajo: `c2p` (el puente), `plot` (que lo usa por ti) y el `x_range` (la trampa de los tres números).

### c2p — por qué no se usan coordenadas crudas

`c2p` (alias de `coords_to_point`) traduce **coordenadas del gráfico → punto de la escena**. Existe porque los ejes están escalados: `Axes` ajusta su tamaño para caber en el frame, de modo que una unidad matemática del eje **no** mide una unidad de escena. Por eso `(PI/2, 1)` matemático cae en algún punto de escena que depende de cómo se hayan dibujado los ejes, y solo `ax.c2p(np.pi/2, 1)` te lo da correcto. La regla sin excepción: **un `Dot`, una etiqueta, una recta o cualquier cosa que deba alinearse con los ejes se posiciona con `ax.c2p(x, y)`**. Su inverso, `p2c`, va de un punto de escena a las coordenadas matemáticas que representa.

### plot y el rango de la curva

`ax.plot(funcion)` dibuja `y = f(x)` recibiendo una función de Python (típicamente un `lambda x: ...`). No tienes que llamar a `c2p` a mano para la curva: `plot` lo aplica internamente para cada punto que muestrea, por eso la curva sale ya encajada en los ejes. Por defecto recorre el `x_range` de los ejes; puedes acotarlo con `plot(funcion, x_range=[a, b])` para dibujar solo un tramo. Lo que devuelve es un Mobject (una `ParametricFunction`) que se anima como cualquier otro.

### El rango de los ejes: [min, max, step]

`x_range` e `y_range` son `[min, max, step]`, **no** `[min, max]`: el tercer número es el paso entre marcas. Es el error más común al empezar. Además, el `y_range` tiene que abarcar lo que la función alcanza: si `f(x)` crece más allá del `y_range`, `plot` recorta la curva por arriba. Dimensiona los ejes a lo que vas a graficar.

## Variaciones

Cuatro extensiones de la receta, cada una sobre los mismos ejes y curva. Todas dependen de `c2p` (directa o indirectamente).

### Área bajo la curva con get_area

`ax.get_area(graph, x_range=...)` sombrea el área bajo la curva en un tramo. El `x_range` del área debe caer dentro del de la curva.

```python
from manim import *

class AreaBajoCurva(Scene):
    def construct(self):
        ax = Axes(x_range=[0, 4, 1], y_range=[0, 16, 4])
        curva = ax.plot(lambda x: x**2, x_range=[0, 4], color=BLUE)
        area = ax.get_area(curva, x_range=[1, 3], color=GREEN, opacity=0.5)  # area entre x=1 y x=3
        self.play(Create(ax), Create(curva))
        self.play(FadeIn(area))
        self.wait()
```

```bash
manim -pql archivo.py AreaBajoCurva
```

### Recta secante (y tangente) con get_secant_slope_group

`ax.get_secant_slope_group(x, graph, dx=...)` construye la recta secante a la curva en `x` separada `dx`; al hacer `dx` pequeño, se aproxima a la tangente.

```python
from manim import *

class Secante(Scene):
    def construct(self):
        ax = Axes(x_range=[-3, 3, 1], y_range=[0, 9, 1])
        curva = ax.plot(lambda x: x**2, color=BLUE)
        secante = ax.get_secant_slope_group(
            x=1, graph=curva, dx=0.01,                 # dx pequeño ≈ recta tangente en x=1
            secant_line_color=YELLOW, secant_line_length=4,
        )
        self.play(Create(ax), Create(curva))
        self.play(Create(secante))
        self.wait()
```

```bash
manim -pql archivo.py Secante
```

### Un punto que recorre la curva con ValueTracker y always_redraw

Un [[ValueTracker]] guarda el valor de `x`; `always_redraw` redibuja el punto en cada fotograma leyendo ese `x` y anclándolo a la curva con `c2p`. Animar el tracker hace que el punto recorra la curva.

```python
from manim import *

class PuntoRecorre(Scene):
    def construct(self):
        ax = Axes(x_range=[-3, 3, 1], y_range=[0, 9, 1])
        curva = ax.plot(lambda x: x**2, color=BLUE)

        x = ValueTracker(-3)                          # guarda la abscisa actual
        punto = always_redraw(                        # se redibuja siguiendo a x
            lambda: Dot(ax.c2p(x.get_value(), x.get_value() ** 2), color=YELLOW)
        )

        self.play(Create(ax), Create(curva))
        self.add(punto)
        self.play(x.animate.set_value(3), run_time=4)  # el punto recorre la parabola
        self.wait()
```

```bash
manim -pql archivo.py PuntoRecorre
```

### Rectángulos de Riemann con get_riemann_rectangles

`ax.get_riemann_rectangles(graph, x_range=..., dx=...)` aproxima el área con rectángulos; bajar `dx` los hace más finos y la aproximación mejor.

```python
from manim import *

class Riemann(Scene):
    def construct(self):
        ax = Axes(x_range=[0, 4, 1], y_range=[0, 16, 4])
        curva = ax.plot(lambda x: x**2, x_range=[0, 4], color=BLUE)
        rects = ax.get_riemann_rectangles(
            curva, x_range=[0, 4], dx=0.5, color=[BLUE, GREEN], fill_opacity=0.6
        )
        self.play(Create(ax), Create(curva))
        self.play(Create(rects))
        self.wait()
```

```bash
manim -pql archivo.py Riemann
```

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| El `Dot`/etiqueta cae fuera de los ejes o en mal sitio | lo colocaste con coordenadas matemáticas crudas, sin traducir | posiciónalo con `ax.c2p(x, y)`: todo punto del gráfico pasa por `c2p` |
| Los ejes salen con marcas espaciadas raro | confundiste `x_range=[min, max]` con `[min, max, step]` | el tercer número es el paso: `x_range=[0, 10, 2]` |
| `plot` corta la curva por arriba | la función supera el `y_range` definido | amplía `y_range`, o acota `x_range` en `plot(..., x_range=[a, b])` |
| El área/Riemann no encaja con la curva | pasaste un `x_range` distinto al de la curva | usa el mismo tramo en `get_area`/`get_riemann_rectangles` que en `plot` |
| `AttributeError: get_graph` / `plot` no existe | usas un nombre antiguo o ManimGL | en ManimCE es `plot` (antes `get_graph`); asegúrate de usar Community Edition |
| El punto con `always_redraw` no se mueve | falta animar el `ValueTracker` o lo metiste con `add` ya en su valor final | anima `x.animate.set_value(...)` dentro de `self.play` |

## Notas relacionadas

- [[Axes]] — la clase central: el constructor, `c2p`, `plot`, `get_area`, `get_riemann_rectangles` y `get_secant_slope_group` en detalle
- [[concepto_sistema_coordenadas]] — coordenadas de escena (`UP`, `RIGHT`, `ORIGIN`) frente a coordenadas matemáticas, y el porqué de `c2p`
- [[ValueTracker]] — el valor animable que, con `always_redraw`, hace que un punto recorra la curva
- [[NumberPlane]] — un `Axes` con rejilla de fondo; hereda `c2p` y `plot`
- [[Manim/patrones/index | patrones]] — el índice de las recetas
