---
title: el sistema de coordenadas de la escena
aliases:
  - sistema de coordenadas
  - coordenadas de escena
  - ORIGIN UP DOWN LEFT RIGHT
tags:
  - manim
  - concepto
order: 5
lib: manim
tipo: concepto
requiere:
  - concepto_mobject
draft: false
---

# el sistema de coordenadas de la escena

Para colocar un objeto en Manim no das píxeles ni porcentajes: das un **punto** o una **dirección** en el sistema de coordenadas de la escena. Ese sistema es un plano (en realidad un espacio 3D) con el **centro de la pantalla en `(0, 0, 0)`**, y trae un puñado de **constantes de dirección** —`UP`, `DOWN`, `LEFT`, `RIGHT`, `ORIGIN`...— que son simplemente vectores de numpy. Entender este sistema es entender el "mapa" donde viven todos los Mobjects: cada `shift`, `move_to`, `next_to` o `to_edge` habla este lenguaje. Y hay una distinción que evita el error más común de los principiantes: las coordenadas de la **escena** no son las coordenadas **matemáticas** de un `Axes`.

## Por qué existe

Manim necesita un sistema de referencia **independiente de la resolución**: la misma escena se renderiza a 480p o a 4K, así que medir en píxeles sería un desastre. La solución es un sistema de **unidades de escena** fijas, con el origen en el centro y ejes orientados como en matemáticas (la `y` **crece hacia arriba**, al revés que en casi todas las APIs gráficas, donde crece hacia abajo). Encima de ese sistema, en lugar de obligarte a escribir vectores a mano, Manim define **constantes con nombre** para las direcciones que más se usan. Así `mob.shift(UP)` se lee como "súbelo una unidad" en vez de `mob.shift(np.array([0, 1, 0]))`.

```python
from manim import *
import numpy as np

# UP, RIGHT, etc. NO son magia: son vectores numpy. Esto es literalmente cierto:
print(UP)              # [0. 1. 0.]
print(RIGHT)           # [1. 0. 0.]
print(np.array_equal(UP, np.array([0., 1., 0.])))   # True
```

## El modelo: el plano, el origen y las constantes de dirección

El centro de la pantalla es `ORIGIN = (0, 0, 0)`. Desde ahí, las direcciones son **vectores unitarios** (de longitud 1 unidad de escena). Todas son arrays de numpy de 3 componentes `(x, y, z)`; en escenas 2D la `z` es 0.

| Constante | Valor `(x, y, z)` | Dirección |
|-----------|-------------------|-----------|
| `ORIGIN` | `[0, 0, 0]` | el centro de la pantalla |
| `UP` | `[0, 1, 0]` | arriba |
| `DOWN` | `[0, -1, 0]` | abajo |
| `LEFT` | `[-1, 0, 0]` | izquierda |
| `RIGHT` | `[1, 0, 0]` | derecha |
| `UL` | `[-1, 1, 0]` | esquina arriba-izquierda |
| `UR` | `[1, 1, 0]` | esquina arriba-derecha |
| `DL` | `[-1, -1, 0]` | esquina abajo-izquierda |
| `DR` | `[1, -1, 0]` | esquina abajo-derecha |
| `IN` | `[0, 0, -1]` | hacia dentro (alejándose, 3D) |
| `OUT` | `[0, 0, 1]` | hacia fuera (hacia ti, 3D) |

Las diagonales (`UL`, `UR`, `DL`, `DR`) son simplemente la suma de dos cardinales: `UR == UP + RIGHT`. Las constantes `IN`/`OUT` solo importan en escenas 3D ([[ThreeDScene]]); en 2D trabajas en el plano `z = 0`.

### El tamaño del frame: lo que se sale no se ve

El sistema es infinito, pero la **cámara** solo muestra un rectángulo. Por defecto el frame mide **~14.22 unidades de ancho por 8 de alto** (relación 16:9), centrado en el `ORIGIN`. Estos valores están en `config`:

| Atributo | Valor por defecto | Qué es |
|----------|-------------------|--------|
| `config.frame_height` | `8.0` | alto visible (de `y = -4` a `y = +4`) |
| `config.frame_width` | `~14.22` | ancho visible (`frame_height * 16/9`) |
| `config.frame_x_radius` | `~7.11` | medio ancho (borde derecho/izquierdo) |
| `config.frame_y_radius` | `4.0` | medio alto (borde superior/inferior) |

Consecuencia práctica: un objeto en `RIGHT * 10` queda **fuera de cuadro** (el borde derecho está en `x ≈ 7.11`). Si "algo no aparece", a menudo es que está colocado fuera del frame. Para pegar un objeto al borde sin calcular estos números a mano se usa `to_edge` / `to_corner`.

### Aritmética de direcciones

Como las constantes son vectores numpy, se **operan con aritmética normal** para construir cualquier punto o desplazamiento. Esto es lo que se usa al posicionar:

```python
RIGHT * 2          # [2, 0, 0]  -> 2 unidades a la derecha
UP * 3             # [0, 3, 0]  -> 3 hacia arriba
UP + RIGHT         # [1, 1, 0]  -> diagonal (igual que UR)
LEFT * 2 + UP      # [-2, 1, 0] -> un punto cualquiera
ORIGIN             # [0, 0, 0]  -> el centro
-RIGHT             # [-1, 0, 0] -> igual que LEFT
```

La regla mental: **multiplicar una dirección por un número la alarga; sumar dos direcciones las combina.** Con eso construyes cualquier vector que necesites pasar a un método de posición.

### Posicionar con estas constantes

Cuatro métodos del Mobject consumen estos vectores. La distinción **relativo vs absoluto** es la que más confunde:

| Método | Qué hace | Relativo / absoluto |
|--------|----------|---------------------|
| `mob.shift(UP * 2)` | **suma** ese vector a la posición actual | relativo (desde donde esté) |
| `mob.move_to(LEFT * 3)` | **lleva el centro** a ese punto exacto | absoluto (a esa coordenada) |
| `mob.to_edge(UP)` | lo pega al **borde** indicado | relativo al frame |
| `mob.next_to(otro, RIGHT)` | lo coloca **al lado** de otro Mobject | relativo a otro objeto |

`shift` **desplaza** (no le importa dónde acabe, solo cuánto se mueve); `move_to` **coloca** (no le importa de dónde venga, solo dónde acaba). El detalle completo de estos y otros métodos (`align_to`, `to_corner`, buffers de `next_to`...) está en [[posicionamiento]].

## La distinción clave: coordenadas de escena vs coordenadas matemáticas

Este es el malentendido que hay que erradicar. Hay **dos** sistemas de coordenadas distintos conviviendo:

- **Coordenadas de la escena** — las de este documento. `RIGHT * 3` está 3 unidades **de pantalla** a la derecha del centro. Son las que usan `shift`, `move_to`, `to_edge`, etc.
- **Coordenadas matemáticas** — las de un `Axes` o un `NumberPlane`. Ahí, el punto `(3, 5)` es un punto **del gráfico** (según la escala de los ejes), **no** un punto de la pantalla. Un `Axes` puede tener su origen descentrado y sus ejes comprimidos: el `(0, 0)` matemático rara vez coincide con el `ORIGIN` de la escena.

El puente entre ambos mundos es `axes.c2p(x, y)` ("coords to point"): convierte un punto **matemático** en su punto de **escena** correspondiente. Su inverso es `axes.p2c(punto)` ("point to coords").

```python
from manim import *

class DosSistemas(Scene):
    def construct(self):
        ejes = Axes(x_range=[0, 5], y_range=[0, 25, 5])

        # MAL: punto.move_to((3, 9, 0)) usaria coords de ESCENA -> casi fuera de cuadro
        # BIEN: traducir el punto matematico (3, 9) a coordenadas de escena con c2p:
        punto = Dot(ejes.c2p(3, 9), color=YELLOW)

        self.add(ejes, punto)
        self.wait()
```

```bash
manim -pql archivo.py DosSistemas      # -p reproduce, -ql = calidad baja (rapido)
```

Regla mental: **si trabajas con un `Axes`/`NumberPlane`, todo dato del gráfico pasa por `c2p` antes de colocarse.** Las constantes `UP`/`RIGHT`/`ORIGIN` son siempre de la escena.

## Ejemplos progresivos

### Nivel 1: un objeto en cada esquina

Las cuatro diagonales (`UL`, `UR`, `DL`, `DR`) con `to_corner` colocan algo en cada esquina del frame:

```python
from manim import *

class Esquinas(Scene):
    def construct(self):
        self.add(
            Dot(color=RED).to_corner(UL),
            Dot(color=GREEN).to_corner(UR),
            Dot(color=BLUE).to_corner(DL),
            Dot(color=YELLOW).to_corner(DR),
            Dot(color=WHITE).move_to(ORIGIN),   # uno en el centro de referencia
        )
        self.wait()
```

```bash
manim -pql archivo.py Esquinas
```

### Nivel 2: aritmética de direcciones

Construimos puntos combinando constantes; cada cuadrado se coloca en una coordenada calculada a mano:

```python
from manim import *

class Aritmetica(Scene):
    def construct(self):
        a = Square(color=RED).move_to(RIGHT * 2)         # 2 a la derecha
        b = Square(color=GREEN).move_to(UP + RIGHT)      # diagonal (igual que UR)
        c = Square(color=BLUE).move_to(LEFT * 3 + DOWN)  # punto compuesto
        d = Square(color=YELLOW).move_to(ORIGIN)         # el centro

        self.add(a, b, c, d)
        self.wait()
```

```bash
manim -pql archivo.py Aritmetica
```

### Nivel 3: el contraste shift (relativo) vs move_to (absoluto)

Dos puntos que parten del mismo sitio: a uno le **sumamos** un vector con `shift`, al otro le **fijamos** el destino con `move_to`. Se ve la diferencia entre desplazar y colocar:

```python
from manim import *

class ShiftVsMoveTo(Scene):
    def construct(self):
        # Ambos arrancan en LEFT*4 (mismo punto de partida):
        rojo = Dot(color=RED).move_to(LEFT * 4)
        azul = Dot(color=BLUE).move_to(LEFT * 4)
        self.add(rojo, azul)
        self.wait()

        # shift: SUMA RIGHT*2 a su posicion -> acaba en LEFT*4 + RIGHT*2 = LEFT*2
        # move_to: IGNORA de donde viene, lo lleva exactamente a RIGHT*2
        self.play(
            rojo.animate.shift(RIGHT * 2),
            azul.animate.move_to(RIGHT * 2),
        )
        self.wait()
```

```bash
manim -pql archivo.py ShiftVsMoveTo
```

El punto rojo (con `shift`) acaba en `LEFT*2`; el azul (con `move_to`) acaba en `RIGHT*2`, aunque partieran del mismo lugar. La animación usa la sintaxis [[concepto_animate_syntax]] para que el desplazamiento se vea ocurrir.

## Casos que fallan

| Síntoma | Causa | Solución |
|---------|-------|----------|
| El objeto no aparece | está colocado fuera del frame (p. ej. `RIGHT * 10`) | mantén `\|x\| < ~7.11` y `\|y\| < 4`, o usa `to_edge` |
| `move_to((3, 5))` no cae donde esperaba en un `Axes` | usaste coords de escena en vez de matemáticas | traduce con `axes.c2p(3, 5)` |
| `shift` no lleva al objeto a donde quería | `shift` es **relativo**, suma a la posición actual | usa `move_to` para un destino absoluto |
| `mob.shift(2)` da error o no hace nada | pasaste un número, no un vector | usa una dirección: `mob.shift(RIGHT * 2)` |
| La `y` va al revés de lo que crees | en Manim la `y` **crece hacia arriba** (como en mates) | `UP` es `+y`, `DOWN` es `-y` |
| `IN`/`OUT` no hacen nada visible | estás en una `Scene` 2D (plano `z = 0`) | son para [[ThreeDScene]] |

## Relación con otros conceptos

- [[concepto_mobject]] — los objetos que se colocan en estas coordenadas con `shift`, `move_to`...
- [[concepto_scene_construct]] — el frame de la `Scene` define qué porción del plano se ve.
- [[concepto_animate_syntax]] — animar un cambio de posición (`c.animate.shift(...)`).
- [[posicionamiento]] — el detalle de `shift`, `move_to`, `to_edge`, `next_to`, `align_to`.
- [[Axes]] — el sistema de coordenadas **matemático** y la conversión `c2p` / `p2c`.
