---
title: colores — especificar y aplicar color en Manim
aliases:
  - colores
  - color
  - constantes de color
tags:
  - manim
  - referencia
  - estilo
lib: manim
tipo: concepto
order: 1
draft: false
---

# colores — especificar y aplicar color en Manim

En Manim un color se da casi siempre como una **constante en mayúsculas** (`RED`, `BLUE`, `GREEN`…) que la librería ya trae definida, aunque también se acepta un **string hexadecimal** (`"#FF0000"`) o un objeto **`ManimColor`** construido a mano. Ese color se **aplica** de dos maneras: al **crear** el objeto, pasándolo como `color=...` al constructor, o **después**, con el método `set_color`. La clave a no perder de vista es que `color` (y `set_color`) tiñen el objeto **entero** —tanto el relleno como el trazo a la vez—; para controlar el interior y el borde por separado, con colores u opacidades distintos, se usan `set_fill` y `set_stroke`, que se documentan en [[set_style]]. Esta nota es la referencia del color en sí: qué constantes existen, cómo se escribe un color y cómo se pinta un objeto (incluidos los gradientes de varios colores).

## Las constantes de color

Manim define decenas de colores como constantes globales **en mayúsculas**, disponibles directamente tras `from manim import *`. Estas son las más usadas:

| Constante | Color |
|-----------|-------|
| `RED` | rojo |
| `BLUE` | azul |
| `GREEN` | verde |
| `YELLOW` | amarillo |
| `ORANGE` | naranja |
| `PURPLE` | morado |
| `PINK` | rosa |
| `TEAL` | verde azulado |
| `MAROON` | granate |
| `GOLD` | dorado |
| `WHITE` | blanco |
| `BLACK` | negro |
| `GREY` / `GRAY` | gris (ambas grafías valen) |

### Las gamas con sufijo _A .. _E

Muchos colores no son un único tono sino una **gama de cinco intensidades**, con sufijo de letra: `_A` (el más claro) hasta `_E` (el más oscuro), con `_C` como tono central. Por ejemplo `BLUE_A` es un azul claro y `BLUE_E` un azul oscuro; la constante a secas (`BLUE`) coincide aproximadamente con el tono medio. Sirven para matizar sin salirte de la paleta de Manim: bordes oscuros con `BLUE_E`, rellenos suaves con `BLUE_A`.

```python
Circle(color=BLUE_E)     # azul oscuro (borde marcado)
Circle(color=BLUE_A)     # azul claro (relleno suave)
```

Existen gamas `_A.._E` para `BLUE`, `RED`, `GREEN`, `YELLOW`, `PURPLE`, `TEAL`, `MAROON`, `GOLD`, `GREY`/`GRAY`, entre otros.

## Formas de especificar un color

Donde Manim pide un color, acepta cualquiera de estas tres formas; internamente todas acaban siendo un `ManimColor`.

### La constante (lo habitual)

La forma idiomática y recomendada: una de las constantes en mayúsculas. Es legible y encaja con la paleta de la librería.

```python
Circle(color=RED)
```

### El string hexadecimal

Un string `"#RRGGBB"` para un color exacto que no esté entre las constantes (un color de marca, por ejemplo). Va entre comillas y empieza por `#`.

```python
Circle(color="#FF6600")     # un naranja concreto por su hex
```

### El objeto ManimColor

La representación interna del color. Se puede construir explícitamente (desde un hex o desde componentes RGB) cuando necesitas manipularlo —interpolar entre dos, leer sus canales—. En el día a día rara vez hace falta, pero es lo que devuelven las constantes por debajo.

```python
from manim import ManimColor
azul = ManimColor("#3498DB")
Circle(color=azul)
```

## Aplicar color

### En el constructor

Lo más directo: pasar `color=` al crear el Mobject. Tiñe a la vez el relleno y el trazo (recuerda que el relleno solo se ve si su opacidad es > 0; ver [[set_style]]).

```python
c = Circle(color=GREEN)          # borde verde (interior aun transparente)
t = Triangle(color=ORANGE)
```

### Con set_color

`mobject.set_color(color)` cambia el color **después** de crear el objeto. Devuelve `self`, así que se encadena y se puede animar con `.animate`. Como `color=`, toca **relleno y trazo a la vez**.

```python
c = Circle()
c.set_color(RED)                 # instantaneo
# animar el cambio de color:
self.play(c.animate.set_color(YELLOW))
```

Para teñir **solo** el interior o **solo** el borde —o darles colores distintos— no uses `set_color`: usa `set_fill` / `set_stroke` de [[set_style]].

## Gradientes

Un gradiente reparte **varios colores** a lo largo del objeto en vez de uno solo.

### set_color_by_gradient

`mobject.set_color_by_gradient(c1, c2, c3, ...)` distribuye la lista de colores de un extremo a otro del objeto. Devuelve `self`.

```python
barra = Rectangle(width=6, height=1)
barra.set_color_by_gradient(RED, YELLOW, GREEN)   # de rojo a verde pasando por amarillo
```

### Relleno con gradiente

`set_color_by_gradient` afecta sobre todo al trazo y, en figuras, al color base; para que el **degradado se vea en el interior** hay que tener opacidad de relleno. Una vía cómoda es pasar varios colores a `set_fill` (que también acepta una lista) o aplicar el gradiente y luego subir la opacidad.

```python
s = Square(side_length=3)
s.set_color_by_gradient(BLUE, PURPLE, PINK)
s.set_fill(opacity=1.0)          # ahora el degradado se ve macizo
```

## Ejemplos

### Una paleta de figuras de colores

Varias figuras, cada una con una constante distinta, para ver la paleta básica de un vistazo.

```python
from manim import *

class Paleta(Scene):
    def construct(self):
        colores = [RED, ORANGE, YELLOW, GREEN, TEAL, BLUE, PURPLE, PINK]
        fila = VGroup(*[
            Square(side_length=0.8, fill_opacity=1, color=col) for col in colores
        ]).arrange(RIGHT, buff=0.2)
        self.play(Create(fila))
        self.wait()
```

```bash
manim -pql archivo.py Paleta      # -p reproduce, -ql = calidad baja (rapido)
```

### Un texto con gradiente

`set_color_by_gradient` luce especialmente bien sobre un [[Text]] o un [[MathTex]], donde el degradado recorre las letras.

```python
from manim import *

class TextoGradiente(Scene):
    def construct(self):
        titulo = Text("Manim", font_size=120)
        titulo.set_color_by_gradient(BLUE, GREEN, YELLOW)
        self.play(Write(titulo))
        self.wait()
```

```bash
manim -pql archivo.py TextoGradiente
```

### Color por hexadecimal

Un color exacto que no está entre las constantes, dado por su hex.

```python
from manim import *

class PorHex(Scene):
    def construct(self):
        c = Circle(radius=1.5, color="#E91E63", fill_opacity=0.8)   # un rosa concreto
        self.play(Create(c))
        self.wait()
```

```bash
manim -pql archivo.py PorHex
```

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| `NameError: name 'red' is not defined` | escribiste el color en minúscula | las constantes van en MAYÚSCULAS: `RED`, no `red` |
| `"red"` como string no da el color esperado | un string debe ser un hex `"#RRGGBB"`, no un nombre | usa la constante `RED` o el hex `"#FF0000"` |
| El interior no se colorea aunque pusiste `color=` | `color` tiñe relleno y trazo, pero el relleno tiene `fill_opacity=0` | sube la opacidad: `fill_opacity=0.5` o `set_fill(col, opacity=0.5)` (ver [[set_style]]) |
| Quería solo el borde de color y se tiñó todo | `set_color`/`color` tocan relleno **y** trazo | usa `set_stroke(col)` para solo el borde |
| El color de un `Text` no cambia como esperaba | un texto puede tener color por partes; `set_color` lo aplica entero | usa `set_color` para todo el texto, o colorea trozos al construirlo |
| `#FF00` no funciona | un hex válido lleva 6 dígitos | escribe los seis: `"#FF0000"` |

## Notas relacionadas

- [[set_style]] — `set_fill` y `set_stroke` para colorear relleno y trazo por separado
- [[rate_functions]] — el otro plano del estilo: la curva del movimiento
- [[VMobject]] — la clase con relleno y trazo a la que se aplica el color
- [[Mobject]] — de donde `set_color` se hereda (tiñe el objeto entero)
- [[Manim/estilo/index | estilo]] — la carpeta de la apariencia
