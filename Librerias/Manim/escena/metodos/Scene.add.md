---
title: Scene.add() — poner objetos en pantalla al instante
aliases:
  - Scene.add
  - add
  - self.add
tags:
  - manim
  - api/metodo
  - escena
lib: manim
tipo: metodo
obj: Scene
order: 2
draft: false
---

# Scene.add() — poner objetos en pantalla al instante

`self.add(...)` pone uno o varios [[concepto_mobject|Mobjects]] en la [[concepto_scene_construct|Scene]] **al instante, sin animación**: aparecen desde el primer fotograma siguiente. Es el contraste directo de `self.play(Create(...))`, que los dibuja progresivamente. Se usa para todo lo que debe estar ahí "ya": el fondo, los ejes, un objeto que luego vas a animar, o cualquier elemento estático que no necesita una entrada animada. Los mobjects se añaden **en orden**, y ese orden fija el **z-order** (lo añadido después se pinta encima). Si un mobject ya estaba en la escena, volver a añadirlo lo **trae al frente** en vez de duplicarlo.

## Firma

```python
def add(self, *mobjects: Mobject) -> Scene:
    ...
```

Sin parámetros de tiempo (no anima): solo recibe los mobjects. **Devuelve la propia `Scene`** (`self`), lo que permite encadenar, aunque en la práctica casi nunca se aprovecha.

### Parametros

#### `*mobjects` — los objetos a mostrar

Uno o varios `Mobject`, pasados como argumentos posicionales separados por comas. Cada uno entra en la lista `self.mobjects` y pasa a renderizarse en cada fotograma a partir de ese punto. Reglas que conviene tener claras:

| Situación | Comportamiento |
|-----------|----------------|
| añadir un mobject nuevo | aparece al instante, encima de lo anterior |
| añadir varios de golpe | `self.add(a, b, c)` — entran en ese orden (c queda más al frente) |
| añadir un mobject que **ya** estaba | no se duplica: se mueve al **frente** del z-order |
| añadir un [[VGroup]] | añade el grupo entero como una unidad |

El **orden de dibujado** importa cuando los objetos se solapan: el último añadido tapa a los anteriores. Para reordenar después se usan `bring_to_front` / `bring_to_back`, o se vuelve a añadir el que quieres delante.

### Valor de retorno

`add` inserta los mobjects en `self.mobjects` (la lista de lo que está en pantalla) y los marca para renderizarse desde el siguiente fotograma; no genera ningún tramo de vídeo por sí mismo (es instantáneo). Devuelve la propia `Scene`. Como no consume tiempo, si una escena **solo** usa `add` sin ningún `play` ni `wait`, el vídeo resultante dura 0 segundos: añade un `self.wait()` para verlo.

## Ejemplos

### Un fondo estático con add

Lo añadido con `add` está en pantalla desde el inicio, sin animarse; solo el círculo se anima con `play`.

```python
from manim import *

class FondoEstatico(Scene):
    def construct(self):
        fondo = Rectangle(width=14, height=8, color=GREY, fill_opacity=0.2)
        ejes = NumberPlane()
        self.add(fondo, ejes)          # ambos aparecen YA, sin animacion

        c = Circle(color=YELLOW)
        self.play(Create(c))           # esto si se ve dibujarse, sobre el fondo
        self.wait()
```

```bash
manim -pql archivo.py FondoEstatico      # -p reproduce, -ql = calidad baja (rapido)
```

### Contraste add vs play(Create)

El cuadro entra de golpe (`add`); el círculo se dibuja progresivamente (`play(Create)`). Es la distinción clave para no llevarse sorpresas.

```python
from manim import *

class AddVsCreate(Scene):
    def construct(self):
        cuadro = Square(color=BLUE).shift(LEFT * 2)
        circulo = Circle(color=GREEN).shift(RIGHT * 2)

        self.add(cuadro)               # aparece instantaneo
        self.wait(0.5)
        self.play(Create(circulo))     # se traza el borde poco a poco
        self.wait()
```

```bash
manim -pql archivo.py AddVsCreate
```

### El orden de dibujado (z-order)

El último mobject añadido se pinta encima. Aquí el círculo rojo tapa al cuadrado azul porque se añadió después.

```python
from manim import *

class OrdenDibujado(Scene):
    def construct(self):
        s = Square(color=BLUE, fill_opacity=1).shift(LEFT * 0.5)
        c = Circle(color=RED, fill_opacity=1).shift(RIGHT * 0.5)

        self.add(s, c)                 # c se anade despues -> queda al frente
        self.wait()

        # volver a anadir 's' lo trae al frente (no lo duplica):
        self.add(s)
        self.wait()
```

```bash
manim -pql archivo.py OrdenDibujado
```

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| Todo aparece de golpe cuando esperabas una animación | usaste `add` en lugar de `play(Create(...))` | usa `self.play(Create(mobj))` o `.animate` |
| El vídeo dura 0 segundos | solo usaste `add` (instantáneo) y ningún `play`/`wait` | añade al menos un `self.wait()` |
| Un objeto queda tapado por otro | el z-order lo da el orden de `add` | añade el de delante el último, o usa `bring_to_front` |
| El mobject "no aparece" pese al `add` | está fuera del encuadre o con `fill_opacity=0` y sin trazo | revisa posición, color y opacidad |
| Se duplica un objeto | en realidad no se duplica: re-añadir solo lo trae al frente | si lo ves doble, creaste dos instancias distintas |

## Notas relacionadas

- [[concepto_scene_construct]] — `add` es uno de los cuatro verbos del guion; el instantáneo.
- [[concepto_mobject]] — los objetos que `add` pone en pantalla.
- [[Scene.play]] — la versión animada: dibujar/transformar en el tiempo.
- [[Scene.wait]] — necesario para que un vídeo de solo `add` dure algo.
- [[concepto_animate_syntax]] — animar un cambio con `.animate` dentro de `play`.
