---
title: Scene.bring_to_front / bring_to_back — orden de dibujado (z-order)
aliases:
  - Scene.bring_to_front
  - Scene.bring_to_back
  - bring_to_front
  - bring_to_back
tags:
  - manim
  - api/metodo
  - escena
lib: manim
tipo: metodo
obj: Scene
order: 5
draft: false
---

# Scene.bring_to_front / bring_to_back — orden de dibujado (z-order)

`self.bring_to_front(*mobjects)` y su pareja `self.bring_to_back(*mobjects)` controlan el **orden de dibujado** (z-order) de los [[concepto_mobject|Mobjects]] dentro de la escena: cuál se pinta encima de cuál cuando dos objetos se **solapan**. Manim dibuja los Mobjects en el orden en que aparecen en `self.mobjects`; el último de la lista queda *arriba del todo*. `bring_to_front` mueve los objetos indicados al final de esa lista (los pone **encima de todo**); `bring_to_back`, al principio (los manda **detrás de todo**). Ambos son **instantáneos** —no animan— y solo reordenan; el objeto no cambia de posición ni de tamaño, solo de capa. Son la herramienta cuando dos figuras se pisan y necesitas decidir cuál queda visible por delante.

## Firma

```python
def bring_to_front(self, *mobjects: Mobject) -> Scene
def bring_to_back(self, *mobjects: Mobject) -> Scene
```

- Ambos son **variádicos** (`*mobjects`): aceptan uno o varios Mobjects separados por comas.
- Ambos devuelven la propia `Scene` (`self`).
- Solo reordenan objetos que **ya están** en la escena; no añaden nada (para eso está [[Scene.add]]).

## Los parametros en detalle

| Parámetro | Tipo | Defecto | Controla |
|-----------|------|---------|----------|
| `*mobjects` | `Mobject` (variádico) | — | los objetos cuyo orden de capa se cambia; con varios, conservan su orden relativo entre sí |

- `bring_to_front(a, b)` deja a `a` y `b` por delante de todos los demás, y entre ellos `b` queda sobre `a` (se respeta el orden de los argumentos).
- Si el Mobject **no estaba** en la escena, estos métodos lo añaden implícitamente al reordenar; en la práctica conviene haberlo añadido antes con `add`/`play`.
- El **z-order** aquí es por orden en la lista de la escena. Para un control numérico más fino existe además `mobject.set_z_index(n)`, pero `bring_to_front`/`bring_to_back` cubren el caso habitual "ponlo delante / detrás".

## Que hace / devuelve

Ambos métodos editan la lista interna `self.mobjects`, que define el orden de pintado. `bring_to_front(x)` saca `x` de su posición actual y lo **reinserta al final** de la lista, de modo que se dibuja el último y, por tanto, queda **por encima** de cualquier objeto que se solape con él. `bring_to_back(x)` lo reinserta **al principio**, así se dibuja primero y el resto queda por encima (lo manda **al fondo**). El efecto es **inmediato y sin animación**, y solo afecta a *qué se ve delante*: las coordenadas, el color y el tamaño del Mobject no cambian. Ambos devuelven `self`.

## Ejemplos

### Dos figuras solapadas: cambiar cuál queda encima

Dos cuadrados que se pisan. Al principio el azul (añadido después) queda encima; con `bring_to_front` pasamos el rojo al frente, y con `bring_to_back` lo devolvemos al fondo:

```python
from manim import *

class QuienVaDelante(Scene):
    def construct(self):
        rojo = Square(color=RED, fill_opacity=1).shift(LEFT * 0.5)
        azul = Square(color=BLUE, fill_opacity=1).shift(RIGHT * 0.5)

        self.add(rojo, azul)            # azul se anade despues -> queda encima
        self.wait()

        self.bring_to_front(rojo)       # ahora el rojo pasa al frente
        self.wait()

        self.bring_to_back(rojo)        # y lo mandamos otra vez al fondo
        self.wait()
```

```bash
manim -pql archivo.py QuienVaDelante   # -p reproduce, -ql = calidad baja (rapido)
```

### Un fondo que debe quedar siempre detrás

Caso típico: añades un rectángulo de fondo *después* de tener contenido y, sin querer, tapa todo. `bring_to_back` lo coloca tras todo de un golpe:

```python
from manim import *

class FondoAlFondo(Scene):
    def construct(self):
        titulo = Text("Hola").scale(1.5)
        self.play(Write(titulo))

        fondo = Rectangle(width=8, height=2, color=GREY, fill_opacity=1)
        self.add(fondo)                 # tapa el titulo (se anadio el ultimo)
        self.wait()

        self.bring_to_back(fondo)       # el fondo pasa detras; el titulo vuelve a verse
        self.wait()
```

```bash
manim -pql archivo.py FondoAlFondo
```

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| El objeto sigue tapado pese a llamar `bring_to_front` | lo llamaste *antes* de añadir el otro Mobject, que volvió a quedar encima | reordena **después** de tener todos los objetos en escena |
| Esperabas una transición y el cambio fue de golpe | `bring_to_front`/`bring_to_back` son instantáneos, no animan | el reordenado de capas no se anima; cambia el orden y sigue con tu `play` |
| El objeto "se movió" al traerlo al frente | confusión: estos métodos NO cambian posición, solo capa | si necesitas moverlo, usa `shift`/`move_to`; el z-order es independiente |
| El fondo tapa todo y no se arregla | el rectángulo de fondo se añadió el último | `self.bring_to_back(fondo)` o añádelo el primero |

## Notas relacionadas

- [[Scene.add]] — añadir Mobjects; el último añadido queda encima por defecto.
- [[Scene.remove]] — quitar Mobjects de la escena al instante.
- [[concepto_scene_construct]] — los verbos instantáneos de `self` dentro de `construct`.
- [[escena/metodos/index|métodos de Scene]] — el grupo de orden frente al de reproducir/mostrar.
