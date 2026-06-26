---
title: set_fill / set_stroke — relleno y trazo de un VMobject
aliases:
  - set_style
  - set_fill
  - set_stroke
tags:
  - manim
  - api/metodo
  - estilo
lib: manim
tipo: metodo
obj: VMobject
order: 2
draft: false
---

# set_fill / set_stroke — relleno y trazo de un VMobject

Todo [[VMobject]] tiene **dos capas de apariencia independientes**: el **relleno** (`fill`, el interior de la figura) y el **trazo** (`stroke`, el borde). `set_fill` controla el primero —color y opacidad del interior— y `set_stroke` el segundo —color, grosor y opacidad del borde—. Esto es lo que los distingue de `set_color` (de [[colores]]), que toca **ambas capas a la vez** con el mismo color: en cuanto quieras un interior translúcido con un borde de otro color, o un borde grueso sin tocar el relleno, necesitas estos dos métodos. Existe además `set_style`, que fija relleno y trazo en una sola llamada, y `set_opacity`, que ajusta la transparencia global. Los cuatro modifican el objeto **al instante** y devuelven `self`, así que se encadenan y se animan con `.animate`.

## set_fill

Fija el **relleno** (interior) de la figura: su color y, sobre todo, su **opacidad**.

```python
VMobject.set_fill(color=None, opacity=None, family=True)
```

### Parametros

| Parametro | Tipo | Defecto | Que controla |
|-----------|------|---------|--------------|
| `color` | color \| None | `None` | color del interior; si es `None`, conserva el color de relleno actual |
| `opacity` | float \| None | `None` | **la clave**: opacidad del relleno, de `0.0` (transparente, figura hueca) a `1.0` (sólido) |
| `family` | bool | `True` | si propaga el cambio a todos los **descendientes** (`submobjects`); con `False`, solo el propio mobject |

#### `opacity` — por qué casi siempre hay que darlo

Por defecto las figuras de Manim nacen con `fill_opacity = 0`: están **huecas** aunque tengan `fill_color`. Por eso `set_fill(RED)` sin opacidad a menudo "no hace nada visible": el color está, pero la transparencia lo oculta. Para ver el interior hay que subir la opacidad explícitamente.

```python
Circle().set_fill(RED)               # sigue hueco: opacity por defecto es 0
Circle().set_fill(RED, opacity=0.7)  # interior rojo translucido, ya se ve
```

### Valor de retorno

Devuelve `self` (el propio mobject), de modo que se encadena con otras llamadas de estilo o posición: `c.set_fill(RED, opacity=0.6).set_stroke(WHITE, width=8)`. El cambio es **instantáneo**; para animarlo, va dentro de `self.play(c.animate.set_fill(...))`.

## set_stroke

Fija el **trazo** (borde) de la figura: su color, su **grosor** y su opacidad.

```python
VMobject.set_stroke(color=None, width=None, opacity=None, background=False, family=True)
```

### Parametros

| Parametro | Tipo | Defecto | Que controla |
|-----------|------|---------|--------------|
| `color` | color \| None | `None` | color del borde; si es `None`, conserva el color de trazo actual |
| `width` | float \| None | `None` | **el grosor** del borde en píxeles (el defecto del objeto suele ser `4.0`); súbelo para un borde marcado, bájalo a `0` para quitarlo |
| `opacity` | float \| None | `None` | opacidad del borde, de `0.0` a `1.0` |
| `background` | bool | `False` | si dibuja el trazo **por detrás** del relleno (útil para que el borde no tape el interior) |
| `family` | bool | `True` | si propaga el cambio a los `submobjects` |

#### `width` — el grosor que da carácter al borde

A diferencia del relleno, el trazo **sí se ve por defecto** (las figuras nacen con borde). `width` lo engrosa o adelgaza: un `width=10` da un contorno grueso y vistoso; `width=0` lo elimina del todo (figura sin borde, solo relleno).

```python
Square().set_stroke(YELLOW, width=12)   # borde amarillo grueso
Square().set_stroke(width=0)            # sin borde
```

### Valor de retorno

Devuelve `self`, encadenable como `set_fill`. Instantáneo; se anima envolviéndolo en `self.play(s.animate.set_stroke(...))`.

## Los atributos: fill_opacity y stroke_width

Detrás de estos métodos hay dos **atributos** del VMobject que también se pueden fijar **al construir** el objeto (como kwargs del constructor). Tocar el atributo en el constructor y llamar al método después son dos vías al mismo estado.

| Atributo | Kwarg del constructor | Método equivalente | Por defecto |
|----------|----------------------|--------------------|-------------|
| `fill_opacity` | `Circle(fill_opacity=0.5)` | `set_fill(opacity=0.5)` | `0.0` (hueco) |
| `fill_color` | `Circle(fill_color=RED)` | `set_fill(RED)` | hereda de `color` |
| `stroke_width` | `Circle(stroke_width=8)` | `set_stroke(width=8)` | `4.0` |
| `stroke_color` | `Circle(stroke_color=YELLOW)` | `set_stroke(YELLOW)` | hereda de `color` |

```python
# en el constructor (de una vez, al crear):
Circle(fill_color=BLUE, fill_opacity=0.5, stroke_color=WHITE, stroke_width=8)
# o despues, con los metodos (mismo resultado):
Circle().set_fill(BLUE, opacity=0.5).set_stroke(WHITE, width=8)
```

`set_style(fill_color=..., fill_opacity=..., stroke_color=..., stroke_width=...)` hace lo mismo que ambos métodos juntos en **una sola llamada**, y `set_opacity(x)` ajusta a la vez la opacidad de relleno y trazo.

## set_fill vs set_stroke vs set_color

Los tres tocan el color, pero sobre capas distintas. La regla: `set_color` es la brocha gorda (todo); `set_fill`/`set_stroke` son el control fino (cada capa por separado).

| Método | Capa que toca | Parámetros propios | Cuándo usarlo |
|--------|---------------|--------------------|---------------|
| `set_color` | relleno **y** trazo a la vez | solo color | un color uniforme para toda la figura, sin distinguir interior y borde |
| `set_fill` | solo el **relleno** | `color`, `opacity` | dar interior (¡recuerda la opacidad!) o cambiar solo el interior |
| `set_stroke` | solo el **trazo** | `color`, `width`, `opacity` | engrosar/colorear el borde sin tocar el relleno |
| `set_style` | relleno y trazo, por separado | los cuatro a la vez | fijar todo el estilo en una llamada |

## Ejemplos

### Una figura maciza

Relleno sólido con `opacity=1`: la figura deja de estar hueca.

```python
from manim import *

class Maciza(Scene):
    def construct(self):
        c = Circle(radius=1.5)
        c.set_fill(BLUE, opacity=1.0)     # interior azul opaco
        self.play(Create(c))
        self.wait()
```

```bash
manim -pql archivo.py Maciza      # -p reproduce, -ql = calidad baja (rapido)
```

### Un borde grueso de otro color

`set_stroke` solo, sin tocar el relleno: la figura queda hueca pero con un contorno marcado.

```python
from manim import *

class BordeGrueso(Scene):
    def construct(self):
        s = Square(side_length=3)
        s.set_stroke(YELLOW, width=14)    # borde amarillo grueso, interior intacto (hueco)
        self.play(Create(s))
        self.wait()
```

```bash
manim -pql archivo.py BordeGrueso
```

### Relleno y borde de colores distintos

El estilo "pulido" clásico: interior de un color, borde de otro. Se encadenan porque ambos devuelven `self`.

```python
from manim import *

class RellenoYBorde(Scene):
    def construct(self):
        t = Triangle().scale(2)
        t.set_fill(PURPLE, opacity=0.6).set_stroke(GOLD, width=10)
        self.play(Create(t))
        self.wait()
```

```bash
manim -pql archivo.py RellenoYBorde
```

### Animar el estilo encadenado

Como devuelven `self`, dentro de `.animate` se encadenan varios cambios de estilo en un solo `play`.

```python
from manim import *

class AnimarEstilo(Scene):
    def construct(self):
        c = Circle(radius=1.5, fill_opacity=0.2)
        self.add(c)
        # anima a la vez subir la opacidad del relleno y engrosar/recolorear el borde:
        self.play(c.animate.set_fill(GREEN, opacity=0.9).set_stroke(WHITE, width=12), run_time=2)
        self.wait()
```

```bash
manim -pql archivo.py AnimarEstilo
```

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| La figura sigue hueca tras `set_fill(RED)` | no diste `opacity`; sigue en `0.0` | `set_fill(RED, opacity=0.7)` |
| `set_fill(RED, width=8)` no engrosa el borde | `width` es de **`set_stroke`**, no de `set_fill` | el grosor va en `set_stroke(width=8)` |
| Quería solo el borde y se tiñó el interior | usaste `set_color` (toca ambas capas) | usa `set_stroke` para solo el borde |
| El estilo cambió también en los hijos sin querer | `family=True` propaga a los `submobjects` | pasa `family=False` para afectar solo al propio mobject |
| El objeto "salta" en vez de animar el estilo | llamaste `set_fill`/`set_stroke` fuera de `self.play` (es instantáneo) | envuélvelo: `self.play(mob.animate.set_fill(...))` |
| `set_stroke(width=0)` y la figura desaparece | quitaste el borde y el relleno estaba hueco | sube `fill_opacity` o no pongas `width=0` |

## Notas relacionadas

- [[VMobject]] — la clase que define `set_fill`, `set_stroke`, `fill_opacity` y `stroke_width`
- [[colores]] — qué colores pasar (constantes, hex) y `set_color` para teñir el objeto entero
- [[rate_functions]] — el plano temporal del estilo: la curva del movimiento
- [[Mobject]] — de donde viene `set_color`, que toca relleno y trazo a la vez
- [[Manim/estilo/index | estilo]] — la carpeta de la apariencia
