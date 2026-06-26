---
title: posicionamiento — colocar y componer mobjects en el lienzo
aliases:
  - posicionamiento
  - colocar mobjects
  - posicionar
tags:
  - manim
  - indice
lib: manim
order: 5
draft: false
---

# posicionamiento — colocar y componer mobjects en el lienzo

Posicionar es **colocar y componer** los Mobjects en el lienzo: el puente entre crearlos (geometría, texto, gráficos) y animarlos. Un objeto recién creado nace en el centro (`ORIGIN`); el posicionamiento es lo que lo lleva a su sitio y lo relaciona con los demás —a la derecha de aquel, pegado a este borde, alineado con aquel otro, repartido en una fila—. Todo en esta carpeta son **métodos heredados de [[Mobject]]**, así que cualquier Mobject (figura, texto, grupo) los tiene; **devuelven `self`**, así que se **encadenan** (`Square().shift(UP).set_color(RED)`) y se aplican al instante. Para *animar* el cambio se usan dentro de `play` con la sintaxis [[concepto_animate_syntax|.animate]]. Todos hablan el mismo idioma: las [[constantes_direccion|constantes de dirección]] sobre el [[concepto_sistema_coordenadas|sistema de coordenadas de la escena]].

## En accion

Una escena que combina varios métodos del grupo: crea figuras y un texto, los coloca con `shift`, `next_to` y `to_edge`, y reparte un `VGroup` en fila con `arrange`.

```python
from manim import *

class Posicionar(Scene):
    def construct(self):
        # absoluto / relativo al frame:
        titulo = Text("posicionamiento").scale(0.7).to_edge(UP)   # pegado al borde superior

        # relativo por un vector:
        c = Circle(color=BLUE).shift(LEFT * 3)                    # 3 a la izquierda del centro

        # relativo a otro objeto:
        etiqueta = Text("circulo").scale(0.5).next_to(c, DOWN, buff=SMALL_BUFF)

        # distribuir un grupo:
        fila = VGroup(*[Square(color=col).scale(0.4)
                        for col in [RED, GREEN, YELLOW]])
        fila.arrange(RIGHT, buff=0.3).shift(RIGHT * 2)            # en fila, y luego desplazada

        self.add(titulo, c, etiqueta, fila)
        self.wait()
```

```bash
manim -pql archivo.py Posicionar      # -p reproduce, -ql = calidad baja (rapido)
```

## El sistema

Antes de los métodos, el mapa donde actúan. El lienzo es un plano con el centro de la pantalla en `ORIGIN = (0, 0, 0)` y la `y` creciendo hacia arriba (como en mates). Las direcciones se nombran con **constantes** —`UP`, `DOWN`, `LEFT`, `RIGHT`, las diagonales `UL`/`UR`/`DL`/`DR`— que son vectores de numpy de longitud 1, y los huecos con **buffers** (`SMALL_BUFF`, `MED_SMALL_BUFF`...). El modelo completo del plano, el frame y la distinción crítica entre coords de **escena** y coords **matemáticas** de un `Axes` está en [[concepto_sistema_coordenadas]]; el catálogo de constantes y buffers, en [[constantes_direccion]]. Todos los métodos de abajo consumen ese vocabulario.

## Metodos que aporta

| Metodo | Para que | Absoluto/Relativo |
|--------|----------|-------------------|
| [[shift_move_to]] (`shift`) | mover por un **vector** desde donde esté | relativo (a la posición actual) |
| [[shift_move_to]] (`move_to`) | llevar el centro a un **punto** o al centro de otro Mobject | absoluto |
| [[next_to]] | colocar **al lado de** otro objeto con un margen | relativo (a otro objeto) |
| [[to_edge_to_corner]] | pegar al **borde** o a una **esquina** del frame | relativo (al frame) |
| [[align_to]] | **alinear** un borde con el de otro objeto | relativo (a otro objeto) |
| [[arrange]] | **distribuir** los hijos de un grupo en fila/columna | relativo (entre sí) |

## Como elegir

La pregunta es siempre "¿respecto a qué quiero colocarlo?". Esta tabla mapea la intención al método.

| Quiero… | Método | Ejemplo |
|---------|--------|---------|
| moverlo **un vector** desde donde esté | `shift` | `c.shift(UP * 2)` |
| llevarlo a una **coordenada exacta** | `move_to(punto)` | `c.move_to(RIGHT * 3)` |
| **centrarlo sobre** otro objeto | `move_to(otro)` | `etiqueta.move_to(caja)` |
| colocarlo **al lado de** otro objeto | `next_to` | `etiqueta.next_to(caja, UP)` |
| pegarlo a un **borde** del frame | `to_edge` | `titulo.to_edge(UP)` |
| pegarlo a una **esquina** | `to_corner` | `logo.to_corner(DR)` |
| **alinear un borde** con el de otro (sin superponer) | `align_to` | `a.align_to(b, LEFT)` |
| **repartir un grupo** en fila o columna | `arrange` | `grupo.arrange(RIGHT)` |

Atajo mental: vector → `shift`; punto/objeto encima → `move_to`; al lado → `next_to`; al borde → `to_edge`/`to_corner`; igualar un borde → `align_to`; un grupo entero → `arrange`.

## Patrones y recetas

### Encadenar metodos (devuelven self)

Como cada método devuelve `self`, se enlazan posición y estilo en una sola expresión legible.

```python
from manim import *

class Encadenar(Scene):
    def construct(self):
        c = Circle().shift(UP).set_color(RED)        # posiciona y estiliza en cadena
        s = Square().next_to(c, DOWN).set_fill(BLUE, opacity=0.5)
        self.add(c, s)
        self.wait()
```

```bash
manim -pql archivo.py Encadenar
```

### Etiquetar una figura con next_to

El patrón más repetido: una figura y su rótulo justo al lado, separados por un `buff` pequeño.

```python
from manim import *

class EtiquetaJunto(Scene):
    def construct(self):
        figura = Triangle(color=GREEN)
        etiqueta = Text("triangulo").scale(0.6).next_to(figura, DOWN, buff=SMALL_BUFF)
        self.play(Create(figura), FadeIn(etiqueta))
        self.wait()
```

```bash
manim -pql archivo.py EtiquetaJunto
```

### Una fila o columna con arrange

Para distribuir varios objetos sin colocarlos uno a uno, mételos en un `VGroup` y deja que `arrange` los reparta a lo largo de una dirección.

```python
from manim import *

class FilaYColumna(Scene):
    def construct(self):
        fila = VGroup(*[Square(color=BLUE).scale(0.3) for _ in range(5)])
        fila.arrange(RIGHT, buff=0.2).to_edge(UP)          # cinco en fila, arriba

        columna = VGroup(*[Dot(color=YELLOW) for _ in range(4)])
        columna.arrange(DOWN, buff=0.4).to_edge(LEFT)      # cuatro en columna, a la izquierda

        self.add(fila, columna)
        self.wait()
```

```bash
manim -pql archivo.py FilaYColumna
```

## Notas relacionadas

- [[concepto_sistema_coordenadas]] — el plano, el origen y la distinción escena vs coords matemáticas.
- [[constantes_direccion]] — el catálogo de direcciones (`UP`, `RIGHT`...) y buffers que usan todos estos métodos.
- [[shift_move_to]] — mover relativo (`shift`) vs colocar absoluto (`move_to`).
- [[next_to]] — colocar al lado de otro objeto.
- [[to_edge_to_corner]] — pegar al borde o esquina del frame.
- [[align_to]] — alinear un borde con el de otro objeto.
- [[arrange]] — distribuir los hijos de un grupo.
- [[concepto_mobject]] — la clase que aporta estos métodos por herencia.
- [[concepto_animate_syntax]] — animar un cambio de posición dentro de `play`.
- [[Manim/index|Manim]] — el índice raíz de la librería.
