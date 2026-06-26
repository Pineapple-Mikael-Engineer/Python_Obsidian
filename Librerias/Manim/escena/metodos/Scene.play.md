---
title: Scene.play() — reproducir animaciones
aliases:
  - Scene.play
  - play
  - self.play
tags:
  - manim
  - api/metodo
  - escena
lib: manim
tipo: metodo
obj: Scene
order: 1
draft: false
---

# Scene.play() — reproducir animaciones

`self.play(...)` es el método central de toda [[concepto_scene_construct|Scene]]: es **lo único que dura y que se ve animarse**. Recibe una o varias [[concepto_animation|animaciones]] y las renderiza a fotogramas dentro del `construct`. Mientras que `self.add` pone objetos en pantalla al instante, cada `self.play` consume tiempo de vídeo (`run_time` segundos) y produce el movimiento. La regla mental: si quieres que algo *se vea cambiar*, va dentro de un `play`; si solo quieres que *esté ahí*, va en un `add`. Un mismo `play` puede recibir **varias animaciones separadas por comas** y las reproduce **simultáneamente**, compartiendo el mismo `run_time`.

## Firma

```python
def play(
    self,
    *animations: Animation,          # una o varias Animation, separadas por comas
    run_time: float | None = None,   # segundos; sobreescribe el run_time de cada animacion
    rate_func: Callable[[float], float] = smooth,  # curva de velocidad global del bloque
    lag_ratio: float = 0,            # desfase entre las animaciones (0 = a la vez, >0 = cascada)
    subcaption: str | None = None,   # subtitulo opcional para el tramo
    subcaption_duration: float | None = None,
    subcaption_offset: float = 0,
    **kwargs,
) -> None:
    ...
```

`play` siempre se llama sobre `self` dentro de `construct`. No devuelve nada útil (`None`): su efecto es grabar un tramo de vídeo.

### Parametros

#### `*animations` — las animaciones a reproducir

Una o varias `Animation`, pasadas como argumentos posicionales separados por comas. **Todas las que pongas en un mismo `play` se reproducen a la vez** (en paralelo), compartiendo el `run_time` del bloque. Cada argumento debe ser una `Animation` de verdad, no un Mobject: `self.play(Create(c))` (correcto) y no `self.play(c)` (error). También acepta la sintaxis `.animate`, que fabrica una animación a partir de un método del mobject: `self.play(c.animate.shift(RIGHT))` (ver [[concepto_animate_syntax]]).

| Quiero… | Cómo se escribe |
|---------|-----------------|
| una sola animación | `self.play(Create(c))` |
| dos **a la vez** | `self.play(Create(a), Create(b))` |
| una **tras** otra | dos `self.play` seguidos |
| animar un método (mover, escalar…) | `self.play(c.animate.shift(RIGHT))` |

#### `run_time` — la duración del bloque

Float en segundos. Si lo das, **sobreescribe** el `run_time` propio de las animaciones: todo el bloque dura exactamente esos segundos. Si lo dejas en `None`, manda el `run_time` de las animaciones (por defecto `1.0` cada una). Es el parámetro que más se toca para acelerar o frenar un paso completo.

#### `rate_func` — la curva de velocidad

Una **función** que mapea el tiempo lineal (0→1) al `alpha` de interpolación; cambia *cómo se siente* el movimiento sin tocar ni el objeto ni la duración. Por defecto `smooth` (arranca y frena suave). Otras útiles: `linear` (ritmo mecánico constante), `there_and_back` (va al estado final y vuelve), `rush_into` / `rush_from`. Se pasa **sin paréntesis** (la función, no su llamada): `rate_func=linear`, nunca `rate_func=smooth()`. Ver el catálogo en [[rate_functions]].

#### `lag_ratio` — el desfase entre animaciones

Float que **escalona el arranque** de cada animación del bloque. Con `lag_ratio=0` (defecto) todas empiezan a la vez; con `lag_ratio>0` cada una arranca cuando la anterior lleva esa fracción recorrida, produciendo una **cascada**. `lag_ratio=1` las encadena casi sin solape. Es la forma rápida de obtener el efecto cascada sin envolver en [[LaggedStart]].

#### `subcaption` — subtítulo del tramo

String opcional con un subtítulo que se asocia al tramo de vídeo (útil al exportar con subtítulos). `subcaption_duration` y `subcaption_offset` ajustan cuánto dura y con qué desfase aparece. Rara vez se usan en animaciones normales.

### Valor de retorno

`play` toma las animaciones, las prepara (lee el estado inicial de cada mobject), y las **renderiza fotograma a fotograma** según `run_time`, `rate_func` y los FPS de la calidad elegida. Cada fotograma evalúa `interpolate_mobject(alpha)` de cada animación y compone la imagen. Al terminar, los mobjects quedan en su estado final dentro de la escena. Devuelve `None`: no encadenes nada sobre su resultado. El efecto observable es un tramo de vídeo de `run_time` segundos.

## Ejemplos

### Una sola animación

Lo más básico: dibujar un círculo con `Create`.

```python
from manim import *

class PlayUna(Scene):
    def construct(self):
        c = Circle(color=BLUE)
        self.play(Create(c))     # se traza el borde progresivamente, en 1 s por defecto
        self.wait()
```

```bash
manim -pql archivo.py PlayUna      # -p reproduce, -ql = calidad baja (rapido)
```

### Varias animaciones a la vez

Separadas por comas, las tres creaciones ocurren **simultáneamente** en el mismo bloque.

```python
from manim import *

class PlayVarias(Scene):
    def construct(self):
        a = Circle(color=RED).shift(LEFT * 3)
        b = Square(color=GREEN)
        c = Triangle(color=YELLOW).shift(RIGHT * 3)

        # las tres se dibujan a la vez:
        self.play(Create(a), Create(b), Create(c))
        self.wait()
```

```bash
manim -pql archivo.py PlayVarias
```

### Controlar la duración con run_time

El mismo movimiento, pero el bloque entero dura 3 segundos en vez de 1.

```python
from manim import *

class PlayRunTime(Scene):
    def construct(self):
        d = Dot(color=BLUE).shift(LEFT * 5)
        self.add(d)
        self.play(d.animate.shift(RIGHT * 10), run_time=3)   # cruza la pantalla en 3 s
        self.wait()
```

```bash
manim -pql archivo.py PlayRunTime
```

### En cascada con lag_ratio

Con `lag_ratio>0`, cada animación del bloque arranca un poco después que la anterior: efecto de cascada sin compositores.

```python
from manim import *

class PlayCascada(Scene):
    def construct(self):
        puntos = [Dot().shift(RIGHT * i + UP) for i in range(-3, 4)]
        # cada FadeIn empieza cuando el anterior lleva 0.5 recorrido:
        self.play(*[FadeIn(p) for p in puntos], lag_ratio=0.5)
        self.wait()
```

```bash
manim -pql archivo.py PlayCascada
```

### La sintaxis .animate

`play` también anima el resultado de un método encadenado al mobject vía `.animate`: se anima el cambio en vez de aplicarlo de golpe.

```python
from manim import *

class PlayAnimate(Scene):
    def construct(self):
        c = Square(color=BLUE)
        self.add(c)
        # anima a la vez el desplazamiento, el giro, la escala y el color:
        self.play(c.animate.shift(RIGHT * 2).rotate(PI / 4).scale(1.5).set_color(RED),
                  run_time=2, rate_func=there_and_back)
        self.wait()
```

```bash
manim -pql archivo.py PlayAnimate
```

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| `self.play(Circle())` falla o no anima | pasaste un **Mobject** donde se espera una **Animation** | envuélvelo: `self.play(Create(Circle()))` |
| El objeto se mueve de golpe pese al `play` | usaste `c.shift(...)` directo en vez de `.animate` | `self.play(c.animate.shift(...))` |
| `rate_func=smooth()` da error | pasaste la **llamada**, no la función | sin paréntesis: `rate_func=smooth` |
| Quería cascada y salieron a la vez | las comas son **simultáneas** | sube `lag_ratio` o usa [[LaggedStart]] |
| El bloque dura "demasiado poco/mucho" | no ajustaste `run_time` | pásalo: `self.play(anim, run_time=2)` |
| `AttributeError` al encadenar sobre `self.play(...)` | `play` devuelve `None` | guarda el mobject aparte; no encadenes sobre el `play` |

## Notas relacionadas

- [[concepto_scene_construct]] — `play` es uno de los cuatro verbos del guion de la Scene.
- [[concepto_animation]] — lo que `play` reproduce; de ahí salen `run_time`, `rate_func`, `lag_ratio`.
- [[concepto_animate_syntax]] — la sintaxis `.animate` para animar un método dentro de `play`.
- [[Scene.add]] — el contraste instantáneo: poner objetos sin animarlos.
- [[Scene.wait]] — pausar entre llamadas a `play`.
- [[rate_functions]] — el catálogo de curvas de velocidad.
- [[LaggedStart]] — cascada con control fino del desfase.
- [[AnimationGroup]] — componer varias animaciones en una sola.
