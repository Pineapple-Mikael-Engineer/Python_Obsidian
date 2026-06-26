---
title: la Scene y construct() — el lienzo y el guion
aliases:
  - Scene
  - construct
  - scene construct
tags:
  - manim
  - concepto
order: 1
lib: manim
tipo: concepto
requiere:
  - concepto_mobject
draft: false
---

# la Scene y construct() — el lienzo y el guion

En Manim no se "dibuja" llamando funciones sueltas: se **subclasea `Scene`** y se escribe un **guion** dentro de su método `construct()`. Ese método es el corazón de toda animación — Manim lo ejecuta de arriba abajo, y cada `self.play(...)` o `self.add(...)` que encuentra se convierte en un trozo del vídeo final. La `Scene` es a la vez el **lienzo** (el espacio donde viven los objetos) y el **director** (quien decide qué ocurre y en qué orden). Toda animación que escribas en Manim empieza por esta misma estructura, así que entenderla bien es entender el 80 % de la librería.

## Por qué existe

Una animación es una secuencia ordenada de cambios en el tiempo. Necesitas un sitio donde declarar *qué objetos hay* y *qué les pasa, y cuándo*. En lugar de un API imperativo disperso (donde cada llamada dibuja algo sin un contexto común), Manim te da una clase que sobreescribes: el **orden de las líneas** de `construct()` **es** el orden temporal del vídeo. Leer el `construct` de una escena es leer su guion de principio a fin.

```python
# No existe una funcion suelta "anima_esto()".
# Defines una Scene y describes el guion en construct():
from manim import *

class MiPrimera(Scene):
    def construct(self):
        ...   # aqui va todo: crear objetos, reproducir animaciones, pausar
```

La clase `Scene` aporta, vía `self`, todo lo necesario para montar el vídeo: el reloj, el lienzo, la cámara y los métodos para añadir y animar. Tú solo rellenas el guion.

## El modelo: cuatro verbos dentro de construct

Casi todo `construct` se escribe combinando cuatro métodos de `self` (la propia Scene). Son el vocabulario mínimo:

| Método | Qué hace | ¿Anima? |
|--------|----------|---------|
| `self.add(mobj)` | pone uno o varios Mobjects en pantalla **al instante** | no |
| `self.play(anim, ...)` | reproduce una o varias **Animations** (dura `run_time` segundos) | sí |
| `self.wait(t)` | pausa `t` segundos (1 por defecto); mantiene el último fotograma | — |
| `self.remove(mobj)` | quita un Mobject al instante (sin animación de salida) | no |

La regla mental que no falla: **`add` y `remove` son instantáneos; `play` es lo único que dura y que se ve animarse.** Si algo "aparece de golpe" cuando esperabas una animación, casi seguro lo metiste con `add` en vez de con `play`.

### El ciclo de vida de una Scene

Cuando ejecutas `manim archivo.py MiEscena`, por dentro ocurre esto:

1. Manim **instancia** tu clase (`MiEscena()`).
2. Llama a **`construct(self)`** una sola vez; ahí se graba toda la lista de animaciones.
3. Cada `self.play(...)` se **renderiza** a fotogramas (según el `run_time` y los FPS).
4. Al terminar `construct`, el vídeo se ensambla y se guarda (y con `-p` se reproduce).

Por eso `construct` no devuelve nada ni se llama a mano: es el gancho que Manim invoca por ti, igual que `paintEvent` en una GUI. Tu trabajo es **describir** el guion; el motor lo convierte en fotogramas.

## Ejemplos progresivos

### Nivel 1: la Scene mínima

La animación más corta que se puede escribir: crear un círculo y esperar.

```python
from manim import *

class Minima(Scene):
    def construct(self):
        self.play(Create(Circle()))   # crea un circulo animadamente
        self.wait()
```

```bash
manim -pql archivo.py Minima      # -p reproduce, -ql = calidad baja (rapido)
```

### Nivel 2: add (instantáneo) vs play (animado)

La distinción más importante para no llevarse sorpresas:

```python
from manim import *

class AddVsPlay(Scene):
    def construct(self):
        cuadro = Square(color=BLUE)
        self.add(cuadro)                            # aparece de golpe, sin animacion
        self.wait()
        self.play(cuadro.animate.shift(RIGHT * 2))  # ahora SI se ve moverse
        self.wait()
```

El `Square` está en pantalla desde el primer fotograma porque lo añadimos con `add`. El desplazamiento, en cambio, se anima porque va dentro de `play` con la sintaxis `.animate` (ver [[concepto_animate_syntax]]).

### Nivel 3: un guion con varios pasos

El orden de los `self.play` es, literalmente, el orden del vídeo:

```python
from manim import *

class Guion(Scene):
    def construct(self):
        titulo = Text("Teorema").to_edge(UP)
        formula = MathTex("a^2 + b^2 = c^2")

        self.play(Write(titulo))           # 1. escribe el titulo
        self.play(FadeIn(formula))         # 2. aparece la formula
        self.wait(0.5)
        self.play(formula.animate.scale(1.5).set_color(YELLOW))  # 3. la agranda y colorea
        self.wait()
        self.play(FadeOut(titulo, formula))  # 4. todo desaparece
```

### Nivel 4: varias animaciones a la vez y control del tiempo

Un solo `self.play` puede reproducir **varias animaciones simultáneas** (basta separarlas por comas), y `run_time` controla cuánto dura cada bloque:

```python
from manim import *

class Simultaneo(Scene):
    def construct(self):
        a = Circle(color=RED).shift(LEFT * 2)
        b = Square(color=GREEN).shift(RIGHT * 2)

        # las dos creaciones ocurren a la vez, en 2 segundos
        self.play(Create(a), Create(b), run_time=2)
        # las dos se mueven al centro a la vez
        self.play(a.animate.move_to(ORIGIN), b.animate.move_to(ORIGIN))
        self.wait()
```

Para encadenar (una tras otra) o escalonar (en cascada) se usan composiciones como [[AnimationGroup]] y [[LaggedStart]]; para lo simultáneo simple basta con las comas.

## Variantes de Scene

`Scene` es la base 2D. Para casos especiales se subclasea una variante (que a su vez hereda de `Scene`), y eso cambia lo que `self` puede hacer:

| Clase | Para qué | Aporta |
|-------|----------|--------|
| `Scene` | animación 2D normal | lo básico (`play`, `add`, `wait`) |
| `MovingCameraScene` | mover o hacer zoom con la cámara | `self.camera.frame` animable |
| `ThreeDScene` | escenas 3D | `self.set_camera_orientation(phi, theta)` |
| `ZoomedScene` | mostrar un recuadro ampliado | una mini-cámara de zoom |

La elección de la clase base es lo primero que decides al crear una escena: si vas a mover la cámara, arrancas ya con `MovingCameraScene`.

## Atributos útiles de self

Dentro de `construct`, `self` no solo tiene los cuatro verbos; también expone el estado de la escena:

| Atributo / método | Para qué |
|-------------------|----------|
| `self.mobjects` | la lista de todos los Mobjects actualmente en pantalla |
| `self.camera` | la cámara (su `background_color`, y en variantes su `frame`) |
| `self.renderer` | el motor de render (rara vez se toca a mano) |
| `self.next_section()` | divide el vídeo en secciones (útil para exportar por trozos) |

## Casos que fallan

| Error | Causa | Solución |
|-------|-------|----------|
| No se ve nada / vídeo vacío | olvidaste `self.add` o `self.play`; el objeto nunca entró a la Scene | añade o reproduce el mobject |
| `construct() takes 1 positional argument but 2 were given` | escribiste `def construct():` sin `self` | siempre `def construct(self):` |
| Todo aparece de golpe | usaste `self.add` esperando que se animara | usa `self.play(Create(...))` o `.animate` |
| El objeto "salta" en vez de animarse | hiciste `mobj.shift(...)` fuera de `play` | mete el cambio en `self.play(mobj.animate.shift(...))` |
| `NameError: name 'Circle' is not defined` | faltó el import | `from manim import *` al inicio |
| El vídeo dura 0 segundos | solo usaste `add`/`remove` (instantáneos) y ningún `play`/`wait` | añade al menos un `self.wait()` o una animación |

## Relación con otros conceptos

- [[concepto_mobject]] — los objetos que se añaden a la Scene y se transforman.
- [[concepto_animation]] — lo que `self.play` reproduce.
- [[concepto_animate_syntax]] — la sintaxis `.animate` para animar un cambio dentro de `play`.
- [[concepto_sistema_coordenadas]] — el espacio (`ORIGIN`, `UP`, `RIGHT`…) donde se colocan los mobjects.
- [[concepto_render_cli]] — cómo el `construct` se convierte en un vídeo con `manim -pql`.
