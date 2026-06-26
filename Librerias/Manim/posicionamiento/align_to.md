---
title: align_to() — alinear un borde con el de otro objeto
aliases:
  - align_to
  - alinear bordes
tags:
  - manim
  - api/metodo
  - posicionamiento
lib: manim
tipo: metodo
obj: Mobject
order: 5
requiere:
  - concepto_sistema_coordenadas
draft: false
---

# align_to() — alinear un borde con el de otro objeto

`align_to` mueve un Mobject hasta que **uno de sus bordes queda a ras del borde del mismo lado** de otro objeto (o de un punto), sin tocar su posición en el eje perpendicular. La diferencia clave con [[next_to]] es que `align_to` **no separa** los objetos: no los pone "uno al lado del otro", sino que **iguala un borde** de ambos. Con `direction=UP` iguala los topes superiores (las dos partes de arriba quedan a la misma altura); con `direction=DOWN`, las bases; con `direction=LEFT`, los lados izquierdos. Es el método para "que todos estos textos empiecen en la misma vertical" o "que estas figuras de distinto tamaño se apoyen en el mismo suelo", manteniendo libre el otro eje.

## Firma

```python
def align_to(
    self,
    mobject_or_point: Mobject | np.ndarray,   # objeto (o punto) de referencia
    direction: np.ndarray = UP,               # qué borde alinear: UP/DOWN/LEFT/RIGHT
) -> Mobject:
    ...
```

### Parametros

#### `mobject_or_point` — la referencia

Contra qué se alinea. Normalmente **otro Mobject**: `a.align_to(b, UP)` mueve `a` hasta que su borde superior coincide con el de `b`. También acepta un **punto** (un array de numpy): `a.align_to(ORIGIN, LEFT)` lleva el borde izquierdo de `a` a `x = 0`. La referencia **no se mueve**; solo se mueve el objeto sobre el que llamas el método.

#### `direction` — qué borde se alinea

La clave del método: indica **qué lado** de ambos objetos se pone al mismo nivel. Solo afecta a ese eje; el perpendicular se conserva.

| `direction` | Qué iguala | Resultado |
|-------------|------------|-----------|
| `UP` | los bordes **superiores** | los dos topes a la misma altura |
| `DOWN` | los bordes **inferiores** | las dos bases a la misma altura (apoyadas en el mismo suelo) |
| `LEFT` | los bordes **izquierdos** | los dos lados izquierdos en la misma vertical |
| `RIGHT` | los bordes **derechos** | los dos lados derechos en la misma vertical |

Mini-ejemplo: si `grande` y `chico` son cuadrados de distinto tamaño y haces `chico.align_to(grande, DOWN)`, el cuadrado pequeño desciende hasta apoyar su base en la **misma altura** que la base del grande (quedan "sobre el mismo suelo"), pero su `x` no cambia. Para alinear por arriba, `direction=UP`; el tope del pequeño sube hasta el tope del grande.

### Valor de retorno

Devuelve `self`, así que es encadenable: `chico.align_to(grande, DOWN).set_color(RED)`. El movimiento es inmediato; para animarlo usa `.animate`: `self.play(chico.animate.align_to(grande, DOWN))`.

## align_to vs next_to

| | `align_to` | `next_to` |
|--|------------|-----------|
| Qué hace | pone un **borde** al mismo nivel que el de otro | coloca el objeto **al lado** de otro, separado |
| ¿Los separa? | **No**: pueden solaparse; solo iguala un borde | **Sí**: deja un `buff` entre ambos |
| El eje perpendicular | se **conserva** (no lo toca) | el objeto se **centra** en el eje perpendicular |
| Uso típico | alinear una columna por la izquierda, igualar bases | poner una etiqueta junto a una figura |
| Resultado de `(a, UP)` | tope de `a` a la altura del tope de la referencia | `a` queda **encima** de la referencia, separado |

La regla mental: `align_to` **nivela** un borde (mismo nivel, posible solape); `next_to` **adosa** dejando espacio (lados distintos, sin solape).

## Ejemplos

### Alinear figuras de distinto tamaño por su base

Tres figuras de alturas diferentes que, tras `align_to(..., DOWN)`, quedan apoyadas en el mismo "suelo".

```python
from manim import *

class MismaBase(Scene):
    def construct(self):
        chico = Square(side_length=1, color=RED).shift(LEFT * 4 + UP)
        medio = Square(side_length=2, color=GREEN)
        grande = Square(side_length=3, color=BLUE).shift(RIGHT * 4 + DOWN)

        self.add(chico, medio, grande)
        self.wait()

        # nivelar las bases con la del cuadrado mediano (no cambia su x):
        chico.align_to(medio, DOWN)
        grande.align_to(medio, DOWN)
        self.wait()
```

```bash
manim -pql archivo.py MismaBase      # -p reproduce, -ql = calidad baja (rapido)
```

### Alinear por la izquierda una columna de textos

Varios textos de distinto largo que arrancan todos en la misma vertical izquierda.

```python
from manim import *

class ColumnaIzquierda(Scene):
    def construct(self):
        lineas = VGroup(
            Text("uno", font_size=36),
            Text("treinta y tres", font_size=36),
            Text("dos", font_size=36),
        ).arrange(DOWN, buff=0.5)

        self.add(lineas)
        self.wait()

        # cada línea queda con su borde izquierdo a ras del de la primera:
        for linea in lineas:
            linea.align_to(lineas[0], LEFT)
        self.wait()
```

```bash
manim -pql archivo.py ColumnaIzquierda
```

### Alinear a un punto

En vez de a otro objeto, alineamos un borde a una coordenada fija (aquí el borde izquierdo al centro `x = 0`).

```python
from manim import *

class AlinearAPunto(Scene):
    def construct(self):
        eje = Line(UP * 3, DOWN * 3, color=GRAY)   # referencia visual en x = 0
        caja = Square(color=YELLOW).shift(LEFT * 2)
        self.add(eje, caja)
        self.wait()

        # el borde IZQUIERDO de la caja se pega a x = 0 (al ORIGIN como punto):
        caja.align_to(ORIGIN, LEFT)
        self.wait()
```

```bash
manim -pql archivo.py AlinearAPunto
```

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| Esperabas separación y los objetos se solapan | `align_to` **no separa**, solo nivela un borde | usa [[next_to]] si quieres dejar espacio entre ellos |
| El objeto se movió también en el otro eje | confundiste el borde a alinear | `align_to` solo toca el eje de `direction`; revisa que pasaste el borde correcto |
| `direction=UP` bajó el objeto en vez de subirlo | con `UP` se igualan los **topes**; si el objeto era más alto, su tope baja al de la referencia | piensa en términos de "qué borde" se iguala, no de "hacia dónde se mueve" |
| Quería todo centrado, no a ras de un borde | `align_to` alinea **bordes**, no centros | para centrar en un eje usa `set_x`/`set_y` o `move_to` |
| La referencia también se movió | no se mueve la referencia; quizá llamaste el método al revés | el objeto que se mueve es sobre el que llamas `.align_to`; la referencia es el argumento |

## Notas relacionadas

- [[next_to]] — el contraste directo: adosar con separación en vez de nivelar un borde.
- [[concepto_sistema_coordenadas]] — las direcciones `UP`/`DOWN`/`LEFT`/`RIGHT` que `align_to` interpreta como bordes.
- [[shift_move_to]] — desplazar o colocar por coordenada, sin referencia a un borde.
- [[to_edge_to_corner]] — alinear, pero contra los **límites del frame** en vez de contra otro objeto.
- [[arrange]] — distribuir los hijos de un grupo (acepta un `aligned_edge` que alinea internamente como `align_to`).
- [[Manim/posicionamiento/index | posicionamiento]] — el panorama de los métodos de colocación.
