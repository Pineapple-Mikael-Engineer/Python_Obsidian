---
title: rate_functions — las curvas de velocidad del movimiento
aliases:
  - rate_functions
  - rate_func
  - curvas de velocidad
tags:
  - manim
  - referencia
  - estilo
lib: manim
tipo: concepto
order: 3
draft: false
---

# rate_functions — las curvas de velocidad del movimiento

Una `rate_func` (función de velocidad o *easing*) **remapea el avance temporal** de una animación: recibe un `alpha` que va linealmente de `0` a `1` (el tiempo crudo) y devuelve otro valor entre `0` y `1` (el avance real de la animación en ese instante). Eso es lo que controla la **sensación** del movimiento —si arranca y frena suave, si va a velocidad constante, si va y vuelve, si rebota— **sin tocar ni el objeto ni la duración**: el `run_time` decide cuánto dura; la `rate_func` decide cómo se reparte ese tiempo. Es un parámetro de **toda [[Animation]]** (lo hereda de la clase base), así que se pasa de dos formas: al constructor de la animación (`Create(c, rate_func=...)`) o directamente al bloque (`self.play(..., rate_func=...)`). La de por defecto es `smooth` (arranque y frenado suaves), que ya queda natural casi siempre; cambiarla es lo que da carácter a un movimiento.

## El catalogo

Las funciones más usadas, agrupadas por la sensación que producen. Todas se pasan **sin paréntesis** (la referencia a la función, no su llamada).

| Funcion | Efecto |
|---------|--------|
| `smooth` | **el defecto**: arranca lento, acelera, frena al final (suave por ambos lados) |
| `linear` | velocidad **constante**, sin aceleración; movimiento mecánico (barridos, rotaciones uniformes, relojes) |
| `rush_into` | arranca **rápido** y frena al final (entra con fuerza y se asienta) |
| `rush_from` | arranca **lento** y acelera hacia el final (sale despacio y coge velocidad) |
| `there_and_back` | va al estado final **y vuelve** al inicial dentro del mismo bloque (rebote, latido, destello de posición) |
| `there_and_back_with_pause` | como `there_and_back` pero con una **pausa** en el punto más lejano antes de volver |
| `slow_into` | entra muy despacio al principio (énfasis en el arranque) |
| `running_start` | retrocede un poco antes de lanzarse hacia delante (toma carrerilla) |
| `wiggle` | oscila de un lado a otro (temblor, vibración) |
| `ease_in_sine` / `ease_out_sine` / `ease_in_out_sine` | familia *easing* basada en seno: `in` suaviza el arranque, `out` el final, `in_out` ambos |

Existen familias `ease_*` análogas con otras curvas (`ease_in_quad`, `ease_out_cubic`, `ease_in_out_expo`, `ease_in_bounce`, `ease_in_elastic`…), del más suave (`sine`/`quad`) al más exagerado (`expo`/`bounce`/`elastic`); el patrón `ease_in_*` / `ease_out_*` / `ease_in_out_*` se repite en todas.

## Como se usan

### En una Animation

Se pasa como `rate_func=` al constructor de la animación o, más cómodo, al `self.play` (donde gobierna **todo el bloque**). Siempre **sin paréntesis**.

```python
self.play(Create(c), rate_func=linear)          # en el play (afecta a todo el bloque)
self.play(Rotate(c, PI, rate_func=there_and_back))   # en el constructor de la animacion
```

### Importarlas

Con `from manim import *` ya tienes disponibles las más comunes (`smooth`, `linear`, `there_and_back`…). Si importas por nombre, vienen del propio paquete o del submódulo `rate_functions`.

```python
from manim import there_and_back, linear      # por nombre
from manim import rate_functions
self.play(c.animate.shift(UP), rate_func=rate_functions.smooth)   # via submodulo
```

## Ejemplos

### Comparar smooth, linear y there_and_back

El **mismo** desplazamiento aplicado a tres puntos, cada uno con una `rate_func` distinta, en secuencia: se ve cómo cambia la sensación sin cambiar la distancia ni la duración.

```python
from manim import *

class CompararRates(Scene):
    def construct(self):
        a = Dot(color=BLUE).shift(LEFT * 5 + UP)
        b = Dot(color=GREEN).shift(LEFT * 5)
        c = Dot(color=RED).shift(LEFT * 5 + DOWN)
        self.add(a, b, c)

        self.play(a.animate.shift(RIGHT * 10), rate_func=smooth, run_time=2)          # suave
        self.play(b.animate.shift(RIGHT * 10), rate_func=linear, run_time=2)          # constante
        self.play(c.animate.shift(RIGHT * 10), rate_func=there_and_back, run_time=2)  # va y vuelve
        self.wait()
```

```bash
manim -pql archivo.py CompararRates      # -p reproduce, -ql = calidad baja (rapido)
```

### Los tres a la vez, lado a lado

Pasando las tres animaciones en un mismo `play` se reproducen en paralelo y la diferencia entre las curvas se aprecia de un vistazo (el de `linear` llega antes a la mitad, el de `smooth` arranca despacio).

```python
from manim import *

class LadoALado(Scene):
    def construct(self):
        izq = VGroup(*[Dot().shift(LEFT * 5 + UP * i) for i in (1, 0, -1)])
        self.add(izq)
        a, b, c = izq

        self.play(
            a.animate.shift(RIGHT * 10),
            b.animate.shift(RIGHT * 10),
            c.animate.shift(RIGHT * 10),
            rate_func=smooth,    # cambia este por linear / rush_into para comparar
            run_time=3,
        )
        self.wait()
```

```bash
manim -pql archivo.py LadoALado
```

### Un rebote con there_and_back

`there_and_back` lleva el objeto al estado final y lo devuelve solo, sin un segundo `play`: ideal para un rebote o un latido.

```python
from manim import *

class ReboteRate(Scene):
    def construct(self):
        pelota = Circle(radius=0.5, color=YELLOW, fill_opacity=1).shift(DOWN * 2)
        self.add(pelota)
        # sube y baja tres veces:
        for _ in range(3):
            self.play(pelota.animate.shift(UP * 3), rate_func=there_and_back, run_time=1)
        self.wait()
```

```bash
manim -pql archivo.py ReboteRate
```

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| `TypeError` o nada se anima con `rate_func=smooth()` | pasaste la **llamada** (con paréntesis), no la función | sin paréntesis: `rate_func=smooth` |
| El movimiento dura más/menos de lo previsto | confundiste `rate_func` con `run_time` | la duración es `run_time`; la `rate_func` solo reparte ese tiempo |
| `NameError: name 'there_and_back' is not defined` | no la importaste y no usaste `from manim import *` | `from manim import there_and_back` o `rate_functions.there_and_back` |
| El objeto vuelve al inicio sin querer | usaste `there_and_back`, que **va y vuelve** | usa `smooth` o `linear` si quieres que se quede en el destino |
| El "rebote" no se nota | la `rate_func` no cambia la distancia, solo el ritmo | combínala con un `run_time` adecuado; para un rebote físico real, prueba `ease_out_bounce` |

## Notas relacionadas

- [[Animation]] — la clase base cuyo parámetro `rate_func` heredan todas las animaciones
- [[Rotate]] — un caso típico donde `linear` o `there_and_back` cambian mucho la sensación
- [[concepto_animation]] — el modelo mental de la animación y su `alpha` de 0 a 1
- [[Scene.play]] — donde se pasa la `rate_func` que gobierna todo un bloque
- [[colores]] — el plano espacial del estilo (color, relleno, trazo)
- [[Manim/estilo/index | estilo]] — la carpeta de la apariencia
