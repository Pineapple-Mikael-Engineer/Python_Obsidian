---
title: constantes de direccion — el vocabulario del posicionamiento
aliases:
  - constantes de direccion
  - UP DOWN LEFT RIGHT
  - direcciones de Manim
  - buff
tags:
  - manim
  - referencia
  - posicionamiento
lib: manim
tipo: concepto
order: 1
draft: false
---

# constantes de direccion — el vocabulario del posicionamiento

Antes de poder mover un Mobject hay que saber nombrar las direcciones, y eso es lo que hacen estas constantes: `UP`, `DOWN`, `LEFT`, `RIGHT`, `ORIGIN`, las diagonales y un puñado de buffers. No son magia ni enums: son **arrays de numpy** de tres componentes `(x, y, z)`, casi todos de longitud 1, que apuntan en una dirección del [[concepto_sistema_coordenadas|sistema de coordenadas de la escena]]. Son el "idioma" que hablan **todos** los métodos de esta carpeta: `shift(UP)`, `move_to(LEFT * 3)`, `next_to(otro, RIGHT)`, `to_edge(DOWN)`, `arrange(RIGHT)`. Quien domina este catálogo posiciona sin calcular vectores a mano; quien lo confunde con las coordenadas de un `Axes` comete el error más común de Manim. Esta nota es la referencia: el catálogo de constantes y cómo se combinan con aritmética para construir cualquier punto o desplazamiento.

## Importacion

Son **constantes globales** del paquete: entran con el import estrella, sin prefijo ni objeto que las contenga.

```python
from manim import *      # trae UP, DOWN, LEFT, RIGHT, ORIGIN, UL, UR, DL, DR, IN, OUT y los *_BUFF
```

Por debajo son `numpy.ndarray`; puedes imprimirlas y operarlas como cualquier vector:

```python
from manim import *
import numpy as np

print(UP)                                       # [0. 1. 0.]
print(RIGHT)                                     # [1. 0. 0.]
print(type(UP))                                  # <class 'numpy.ndarray'>
print(np.array_equal(UR, UP + RIGHT))            # True  (las diagonales son sumas)
```

## El catalogo

Las constantes de dirección son **vectores unitarios** (longitud 1 unidad de escena) que parten del centro. Todas tienen tres componentes `(x, y, z)`; en escenas 2D la `z` es 0. El `ORIGIN` es la excepción: es el punto `(0, 0, 0)`, el centro de la pantalla.

| Constante | Vector `(x, y, z)` | Apunta a |
|-----------|--------------------|----------|
| `ORIGIN` | `[0, 0, 0]` | el centro de la pantalla (no es dirección, es punto) |
| `UP` | `[0, 1, 0]` | arriba (la `y` crece hacia arriba, como en mates) |
| `DOWN` | `[0, -1, 0]` | abajo |
| `LEFT` | `[-1, 0, 0]` | izquierda |
| `RIGHT` | `[1, 0, 0]` | derecha |
| `UL` | `[-1, 1, 0]` | esquina arriba-izquierda (`UP + LEFT`) |
| `UR` | `[1, 1, 0]` | esquina arriba-derecha (`UP + RIGHT`) |
| `DL` | `[-1, -1, 0]` | esquina abajo-izquierda (`DOWN + LEFT`) |
| `DR` | `[1, -1, 0]` | esquina abajo-derecha (`DOWN + RIGHT`) |
| `IN` | `[0, 0, -1]` | hacia dentro, alejándose del espectador (solo 3D) |
| `OUT` | `[0, 0, 1]` | hacia fuera, hacia el espectador (solo 3D) |

Las cuatro diagonales son literalmente la suma de dos cardinales (`UR == UP + RIGHT`), así que puedes escribirlas como prefieras. Las constantes `IN` / `OUT` solo tienen efecto visible en una [[ThreeDScene]]; en una `Scene` 2D trabajas en el plano `z = 0` y no hacen nada. Existen además los alias `X_AXIS`, `Y_AXIS`, `Z_AXIS` (`RIGHT`, `UP`, `OUT` respectivamente) que se usan sobre todo al rotar.

## Las constantes de margen (buff)

Aparte de las direcciones hay un segundo grupo de constantes: los **buffers** o márgenes. No apuntan a ningún sitio, son **números** (floats en unidades de escena) que fijan el hueco que dejan `next_to`, `to_edge`, `to_corner` y `arrange` entre objetos o contra el borde. Tenerlos con nombre evita sembrar el código de "0.1", "0.25", "0.5" mágicos.

| Constante | Valor aproximado | Uso típico |
|-----------|------------------|------------|
| `SMALL_BUFF` | `0.1` | separación mínima, casi pegado |
| `MED_SMALL_BUFF` | `0.25` | el **defecto de `next_to`**; separación normal entre vecinos |
| `MED_LARGE_BUFF` | `0.5` | el **defecto de `to_edge` / `to_corner`**; margen contra el borde |
| `LARGE_BUFF` | `1.0` | separación amplia, aireada |

Se pasan al parámetro `buff` de los métodos de posición: `etiqueta.next_to(figura, UP, buff=SMALL_BUFF)`. También vale un número crudo (`buff=0.4`), pero las constantes mantienen la composición coherente entre notas. Ojo: el `buff` por defecto **no es el mismo** en todos los métodos (`next_to` usa `MED_SMALL_BUFF`, `to_edge` usa `MED_LARGE_BUFF`), de ahí que convenga nombrarlo cuando importe.

## Como se usan

### Mover en una direccion con shift

`shift` suma el vector a la posición actual: pasarle una constante mueve el objeto justo una unidad en esa dirección.

```python
from manim import *

class ShiftConstante(Scene):
    def construct(self):
        c = Square(color=BLUE)
        self.add(c)
        self.play(c.animate.shift(UP))      # sube exactamente 1 unidad de escena
        self.wait()
```

```bash
manim -pql archivo.py ShiftConstante      # -p reproduce, -ql = calidad baja (rapido)
```

### Escalar un vector para alargar la distancia

Multiplicar una constante por un número la **alarga**: `RIGHT * 2` son 2 unidades a la derecha. Es la forma normal de pedir distancias mayores que 1.

```python
from manim import *

class EscalarVector(Scene):
    def construct(self):
        a = Dot(color=RED).move_to(LEFT * 5)        # 5 unidades a la izquierda
        b = Dot(color=GREEN).move_to(RIGHT * 5)     # 5 a la derecha
        self.add(a, b)
        self.play(a.animate.shift(RIGHT * 10))      # cruza la pantalla: +10 en x
        self.wait()
```

```bash
manim -pql archivo.py EscalarVector
```

### Sumar direcciones para una diagonal

Sumar dos constantes **combina** sus direcciones. `UP + RIGHT` es la diagonal hacia arriba-derecha (idéntica a `UR`); con escalares construyes cualquier punto.

```python
from manim import *

class SumarDirecciones(Scene):
    def construct(self):
        p = Dot(color=YELLOW).move_to(ORIGIN)
        self.add(p)
        self.play(p.animate.shift(UP + RIGHT))      # diagonal, igual que shift(UR)
        self.play(p.animate.shift(LEFT * 2 + DOWN)) # un desplazamiento compuesto
        self.wait()
```

```bash
manim -pql archivo.py SumarDirecciones
```

### Posicionar relativo con una constante

Los métodos relativos consumen estas constantes para decir "de qué lado". Aquí `UP` le dice a `next_to` que coloque la etiqueta **encima** de la figura.

```python
from manim import *

class NextToConstante(Scene):
    def construct(self):
        figura = Circle(color=BLUE)
        etiqueta = Text("circulo").scale(0.6)
        etiqueta.next_to(figura, UP, buff=SMALL_BUFF)   # encima, casi pegada
        self.add(figura, etiqueta)
        self.wait()
```

```bash
manim -pql archivo.py NextToConstante
```

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| `move_to((3, 5))` no cae donde esperabas sobre un `Axes` | confundiste coords de **escena** con coords **matemáticas** del gráfico | traduce el punto del gráfico con `axes.c2p(3, 5)` (ver [[concepto_sistema_coordenadas]] y [[Axes]]) |
| `mob.shift(2)` da error o no mueve | pasaste un número, no un vector | usa una dirección: `mob.shift(RIGHT * 2)` |
| Olvidas que son vectores 3D y rompes operaciones | las constantes son arrays de 3 componentes, no 2 | opera siempre con otras constantes/escalares; no mezcles tuplas `(x, y)` sueltas |
| `IN` / `OUT` no hacen nada visible | estás en una `Scene` 2D (plano `z = 0`) | son para [[ThreeDScene]] |
| Multiplicas mal: `2 * RIGHT * 2` o `RIGHT * RIGHT` | `RIGHT * RIGHT` es producto elemento a elemento (da `[1,0,0]`), no lo que quieres | escala solo por **escalares**: `RIGHT * 2`, nunca vector por vector |
| El objeto se "pega" sin margen con `next_to` | el `buff` por defecto varía según el método | pásalo explícito: `buff=MED_LARGE_BUFF` o un float |

## Notas relacionadas

- [[concepto_sistema_coordenadas]] — el plano, el origen y la distinción coords de escena vs matemáticas; estas constantes son su vocabulario.
- [[shift_move_to]] — los métodos relativo (`shift`) y absoluto (`move_to`) que consumen estos vectores.
- [[next_to]] — coloca relativo a otro objeto usando `direction` y `buff`.
- [[to_edge_to_corner]] — pega al borde/esquina usando estas direcciones y `MED_LARGE_BUFF`.
- [[arrange]] — distribuye un grupo a lo largo de una de estas direcciones.
- [[Axes]] — el sistema de coordenadas **matemático** y la conversión `c2p` / `p2c`.
- [[posicionamiento/index|posicionamiento]] — el índice del grupo.
