---
title: la sintaxis .animate — animar un cambio
aliases:
  - animate
  - .animate
  - animate syntax
tags:
  - manim
  - concepto
order: 4
lib: manim
tipo: concepto
requiere:
  - concepto_animation
draft: false
---

# la sintaxis .animate — animar un cambio

Todo Mobject sabe transformarse a sí mismo: `c.shift(RIGHT)` lo desplaza, `c.scale(2)` lo agranda, `c.set_color(RED)` lo recolorea. El problema es que esos métodos cambian el objeto **al instante**, sin animación. La sintaxis `.animate` es el puente que convierte **cualquiera** de esos métodos en una **animación reproducible** con `self.play(...)`: `self.play(c.animate.shift(RIGHT))` no salta el círculo a la derecha, lo **desliza** suavemente hasta allí. Es, junto a las clases `Animation` (`Create`, `Transform`...), la segunda gran forma de animar en Manim — y la más cómoda para "animar el cambio que ya sabes hacer a mano".

## Por qué existe

Sin `.animate` tendrías un problema incómodo: para cada cosa que un Mobject sabe hacer (`shift`, `scale`, `rotate`, `set_color`, `to_edge`, `next_to`...) necesitarías una clase de animación dedicada que la reprodujera en el tiempo. Serían decenas de clases casi idénticas. En vez de eso, Manim ofrece **un único mecanismo** que toma el método que ya existe en el Mobject y lo envuelve en una animación. La idea es: *"sé mover el objeto; ahora quiero ver ese movimiento ocurrir"*. El cambio que escribirías para aplicarlo de golpe es exactamente el que escribes para animarlo — solo intercalas `.animate` antes del método.

```python
# Las dos lineas hacen el MISMO cambio final (el circulo acaba 2 a la derecha).
# La diferencia es solo CUANDO y COMO se ve:
c.shift(RIGHT * 2)                      # se aplica YA, en un fotograma (salta)
self.play(c.animate.shift(RIGHT * 2))   # se ANIMA en el tiempo (se desliza)
```

Esa simetría es el motivo de su existencia: aprendes el método una vez (para posicionar, estilizar, transformar) y lo reutilizas tal cual para animarlo, sin memorizar una clase nueva por cada acción.

## El modelo: .animate es un proxy que graba el estado final

`mobject.animate` **no** es un método; es un **proxy** (un objeto intermediario). Cuando escribes `c.animate.shift(RIGHT)`, ocurre esto por dentro:

1. `c.animate` devuelve un proxy ligado a `c`.
2. Llamar `.shift(RIGHT)` sobre el proxy **no mueve `c` todavía**: aplica el cambio sobre una **copia** y **graba** cuál sería el estado resultante.
3. El proxy se entrega a `self.play(...)`, que ya tiene dos fotos: el **estado inicial** de `c` (como está ahora) y el **estado final** (el que grabó el proxy).
4. Manim **interpola** entre ambos estados a lo largo del `run_time`, fotograma a fotograma. Al terminar, `c` queda en el estado final de verdad.

La regla mental: **`.animate` graba "el antes" y "el después", y Manim rellena el camino entre ambos**. Por eso `.animate` siempre vive dentro de `self.play(...)`: fuera de él no tiene sentido, porque nadie reproduce la interpolación.

| Forma | Qué es | Cuándo ocurre el cambio |
|-------|--------|--------------------------|
| `c.shift(RIGHT)` | llamada normal al método | al instante (un fotograma) |
| `c.animate.shift(RIGHT)` | proxy que se da a `play` | interpolado durante `run_time` |
| `self.play(c.animate.shift(RIGHT))` | la animación reproduciéndose | se ve el deslizamiento |

### Encadenar métodos: varios cambios a la vez

Como cada método de transformación devuelve el propio Mobject (o, aquí, el proxy), se pueden **encadenar** en una sola expresión. El proxy acumula **todos** los cambios y graba el estado final tras aplicarlos todos; `self.play` los anima **simultáneamente**:

```python
# Los TRES cambios (mover, agrandar, colorear) se animan a la vez, en un solo play:
self.play(c.animate.shift(RIGHT).scale(2).set_color(RED))
```

Esto es distinto de aplicarlos en `self.play` separados (que los reproduciría **uno tras otro**). Encadenar sobre un mismo `.animate` = todo junto, en paralelo, en el mismo bloque de tiempo.

## Ejemplos progresivos

### Nivel 1: un .animate simple

El caso base — animar un único método. Comparamos el salto instantáneo con el deslizamiento animado:

```python
from manim import *

class AnimateSimple(Scene):
    def construct(self):
        c = Circle(color=BLUE)
        self.add(c)                            # aparece de golpe en el centro
        self.wait()
        self.play(c.animate.shift(RIGHT * 3))  # se DESLIZA 3 a la derecha
        self.wait()
```

```bash
manim -pql archivo.py AnimateSimple      # -p reproduce, -ql = calidad baja (rapido)
```

### Nivel 2: encadenar varios cambios

Tres transformaciones en una sola animación, todas a la vez. Fíjate en que es **un** `self.play` con **un** `.animate` encadenado:

```python
from manim import *

class AnimateEncadenado(Scene):
    def construct(self):
        c = Square(color=BLUE, fill_opacity=0.5)
        self.add(c)
        self.wait()
        # mover + agrandar + recolorear, simultaneamente, en 2 segundos:
        self.play(c.animate.shift(UP * 2).scale(1.5).set_color(YELLOW), run_time=2)
        self.wait()
```

```bash
manim -pql archivo.py AnimateEncadenado
```

Si en cambio quisieras que ocurrieran **en cascada** (primero mover, luego agrandar, luego colorear), usarías tres `self.play` seguidos, cada uno con su propio `.animate`.

### Nivel 3: la trampa de la rotación — .animate.rotate vs Rotate

Este es el ejemplo que conviene entender de memoria. `.animate` interpola **los puntos** del Mobject del estado inicial al final **en línea recta**. Para mover, escalar o colorear eso es justo lo que quieres. Pero para **rotar** no: un giro no es un movimiento recto de cada punto, es un movimiento **circular**. Si interpolas en recta los puntos de un objeto que gira media vuelta (`PI`), a mitad de camino los puntos pasan **por el centro** y el objeto se ve **encogerse** (o aplastarse) antes de volver a salir. La animación dedicada `Rotate` sí gira de verdad, alrededor del centro, sin deformar.

```python
from manim import *

class RotacionTrampa(Scene):
    def construct(self):
        # Dos cuadrados identicos, uno a cada lado, para comparar:
        izq = Square(color=RED).shift(LEFT * 3)
        der = Square(color=GREEN).shift(RIGHT * 3)
        etq_i = Text(".animate.rotate", font_size=24).next_to(izq, DOWN)
        etq_d = Text("Rotate", font_size=24).next_to(der, DOWN)
        self.add(izq, der, etq_i, etq_d)
        self.wait()

        # IZQUIERDA: interpola los puntos en recta -> se DEFORMA a mitad de giro
        # DERECHA: gira de verdad alrededor del centro -> giro limpio
        self.play(
            izq.animate.rotate(PI),
            Rotate(der, PI),
            run_time=3,
        )
        self.wait()
```

```bash
manim -pql archivo.py RotacionTrampa
```

Al reproducirlo se ve que el cuadrado rojo (`.animate.rotate`) se aplasta hacia el centro a media animación, mientras que el verde (`Rotate`) describe un giro limpio. La conclusión práctica está en la tabla siguiente.

## Cuándo usar .animate y cuándo la Animation dedicada

`.animate` es cómodo, pero no siempre es lo correcto. La pregunta clave es: *¿la interpolación recta de los puntos da el resultado que quiero?*

| Cambio | `.animate` funciona bien | Usa mejor la `Animation` dedicada |
|--------|--------------------------|-----------------------------------|
| Mover (`shift`, `move_to`) | sí, recto es lo natural | — |
| Escalar (`scale`) | sí | — |
| Recolorear (`set_color`, `set_fill`) | sí, interpola el color | — |
| Rotar (`rotate`) | no, deforma el objeto | `Rotate(mob, angulo)` |
| Aparecer desde nada | no tiene "estado inicial" útil | `Create(mob)`, `FadeIn(mob)`, `Write(mob)` |
| Convertirse en **otro** Mobject | `.animate` no cambia de identidad | `Transform(a, b)`, `ReplacementTransform(a, b)` |
| Desaparecer | no | `FadeOut(mob)`, `Uncreate(mob)` |

La regla resumida: **`.animate.metodo()` para cambiar un objeto que ya está en pantalla en algo de sí mismo (posición, tamaño, color); una `Animation` dedicada para nacer, morir, morfar a otro objeto o girar.**

## Casos que fallan

| Síntoma | Causa | Solución |
|---------|-------|----------|
| El objeto "salta" sin animarse | usaste `c.shift(...)` (sin `.animate`) fuera o dentro de `play` | escribe `self.play(c.animate.shift(...))` |
| `AttributeError` / no anima nada | pusiste `.animate` fuera de `self.play` | el proxy solo sirve dentro de `self.play(...)` |
| El objeto se encoge a mitad de giro | rotaste con `.animate.rotate(...)` (interpola en recta) | usa la animación `Rotate(mob, angulo)` |
| No se ve nada cambiar | el método no modifica el estado (p. ej. `shift(ORIGIN)`) | comprueba que el cambio realmente altera el objeto |
| Quería pasos en cascada y salen a la vez | encadenaste todo en un solo `.animate` | usa varios `self.play(...)` separados |
| `.animate` sobre un grupo no hace lo esperado | algunos métodos de [[VGroup]] no se animan elemento a elemento | anima cada submobject o usa [[LaggedStart]] |

## Relación con otros conceptos

- [[concepto_animation]] — qué es una `Animation`; `.animate` produce una internamente (`_AnimationBuilder`).
- [[concepto_scene_construct]] — `.animate` solo tiene sentido dentro de un `self.play(...)` del `construct`.
- [[concepto_mobject]] — los métodos que `.animate` envuelve (`shift`, `scale`, `set_color`...) son métodos del Mobject.
- [[concepto_sistema_coordenadas]] — las direcciones (`RIGHT`, `UP`...) que se pasan a `.animate.shift(...)`.
- [[posicionamiento]] — el detalle de `shift`, `move_to`, `next_to`, `to_edge` que se animan con `.animate`.
