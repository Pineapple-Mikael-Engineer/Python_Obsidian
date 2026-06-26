---
title: Scene.wait() — pausar manteniendo el fotograma
aliases:
  - Scene.wait
  - wait
  - self.wait
tags:
  - manim
  - api/metodo
  - escena
lib: manim
tipo: metodo
obj: Scene
order: 3
draft: false
---

# Scene.wait() — pausar manteniendo el fotograma

`self.wait(...)` introduce una **pausa** en el guion de la [[concepto_scene_construct|Scene]]: durante `duration` segundos no cambia nada, se mantiene congelado el último fotograma. Es el verbo que da **respiración** al vídeo — deja leer un texto, separa dos pasos para que se distingan, o espera a que un [[concepto_updaters|updater]] o una condición terminen. Aunque parece trivial, es esencial: una escena que solo usa `self.add` (instantáneo) sin ningún `wait` ni `play` produce un vídeo de 0 segundos. Casi todo `construct` termina con un `self.wait()` para que el último estado se vea antes de cortar.

## Firma

```python
def wait(
    self,
    duration: float = 1.0,                       # segundos de pausa
    stop_condition: Callable[[], bool] | None = None,  # corta la espera antes si devuelve True
    frozen_frame: bool | None = None,            # fuerza/evita congelar el frame (auto si None)
) -> None:
    ...
```

`wait` no devuelve nada (`None`); su efecto es añadir un tramo de vídeo en el que el estado no cambia (salvo updaters activos).

### Parametros

#### `duration` — cuántos segundos pausa

Float en segundos, `1.0` por defecto. Es lo único que se pasa el 95 % de las veces: `self.wait()` pausa 1 s, `self.wait(0.5)` medio segundo, `self.wait(3)` tres segundos. Durante ese tiempo el último fotograma se mantiene fijo, lo que da al espectador margen para leer o asimilar lo que acaba de pasar.

#### `stop_condition` — cortar la espera antes de tiempo

Un **callable sin argumentos** que devuelve `bool`. Si lo das, Manim evalúa la condición en cada fotograma de la espera y **corta** en cuanto devuelve `True`, aunque no se hayan cumplido los `duration` segundos (que actúan como tope máximo). Es la forma de esperar a que **algo dinámico ocurra** —por ejemplo, que un objeto movido por un updater alcance cierta posición— sin saber de antemano cuánto tardará.

#### `frozen_frame` — congelar o no el fotograma

Bool opcional. Si es `None` (defecto), Manim decide solo: congela el frame cuando no hay nada que actualizar (espera estática, más eficiente) y lo deja "vivo" cuando hay updaters o una `stop_condition` que evaluar. Pásalo explícito solo en casos raros: `frozen_frame=False` fuerza el render fotograma a fotograma durante la espera (necesario si quieres que se sigan ejecutando updaters), `True` lo congela.

### Valor de retorno

`wait` graba un tramo de vídeo de hasta `duration` segundos en el que la cámara sigue capturando pero **no se reproduce ninguna animación nueva**. Si hay updaters activos en los mobjects, **sí siguen ejecutándose** (el fotograma no se congela), de modo que `wait` es también la forma de "dejar correr" el tiempo para que los updaters animen. Si hay `stop_condition`, la espera termina antes en cuanto se cumple. Devuelve `None`.

## Ejemplos

### Pausa simple al final

El cierre típico: tras la última animación, un `wait()` deja ver el resultado un segundo antes de cortar.

```python
from manim import *

class PausaSimple(Scene):
    def construct(self):
        t = Text("Hola, Manim")
        self.play(Write(t))
        self.wait()                 # 1 s para leer antes de que termine el video
```

```bash
manim -pql archivo.py PausaSimple      # -p reproduce, -ql = calidad baja (rapido)
```

### Separar pasos con pausas

Las pausas entre `play` marcan el ritmo: cada paso se distingue del siguiente.

```python
from manim import *

class SepararPasos(Scene):
    def construct(self):
        formula = MathTex("a^2 + b^2 = c^2")
        self.play(Write(formula))
        self.wait(1)                                   # deja leer la formula
        self.play(formula.animate.set_color(YELLOW))   # la resalta
        self.wait(0.5)                                 # pausa corta
        self.play(formula.animate.scale(1.5))          # la agranda
        self.wait(2)                                   # pausa larga final
```

```bash
manim -pql archivo.py SepararPasos
```

### Esperar a una condición con stop_condition

Un punto se mueve por un updater; `wait` corta automáticamente cuando cruza el centro, sin saber cuántos segundos tarda (con tope de 10 s).

```python
from manim import *

class EsperarCondicion(Scene):
    def construct(self):
        d = Dot(color=RED).shift(LEFT * 5)
        self.add(d)
        d.add_updater(lambda m, dt: m.shift(RIGHT * 2 * dt))   # se mueve solo

        # espera hasta que el punto pase x=0, como mucho 10 segundos:
        self.wait(10, stop_condition=lambda: d.get_x() >= 0)

        d.clear_updaters()
        self.play(d.animate.set_color(GREEN))   # marca que llego
        self.wait()
```

```bash
manim -pql archivo.py EsperarCondicion
```

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| El vídeo dura 0 segundos | solo usaste `add` (instantáneo) y ningún `wait`/`play` | añade al menos un `self.wait()` |
| El último estado "no se ve" antes de cortar | faltó un `wait` final | cierra el `construct` con `self.wait()` |
| `stop_condition` no corta nunca | la condición jamás devuelve `True` (o el `duration` es muy corto) | revisa la lógica y deja un `duration` tope razonable |
| Los updaters no avanzan durante la espera | el frame se congeló | normalmente Manim lo detecta; si no, `frozen_frame=False` |
| `wait` "no hace nada" | pusiste `self.wait` sin paréntesis | llámalo: `self.wait()` |

## Notas relacionadas

- [[concepto_scene_construct]] — `wait` es uno de los cuatro verbos del guion; la pausa.
- [[Scene.play]] — el verbo que sí anima; `wait` separa los `play`.
- [[Scene.add]] — instantáneo; necesita un `wait` para que el vídeo dure.
- [[concepto_updaters]] — durante un `wait` los updaters siguen corriendo.
- [[concepto_render_cli]] — cómo el `construct` (con sus pausas) se convierte en vídeo.
