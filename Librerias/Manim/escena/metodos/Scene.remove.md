---
title: Scene.remove — quitar Mobjects al instante
aliases:
  - Scene.remove
  - remove
tags:
  - manim
  - api/metodo
  - escena
lib: manim
tipo: metodo
obj: Scene
order: 4
draft: false
---

# Scene.remove — quitar Mobjects al instante

`self.remove(*mobjects)` saca uno o varios [[concepto_mobject|Mobjects]] de la escena **al instante**, sin animación de salida: en el siguiente fotograma simplemente ya no están. Es la operación inversa de [[Scene.add]] (que los mete de golpe) y, como ella, es **instantánea** — no es una [[concepto_animation|Animation]] y no se pasa a [[Scene.play]]. Por eso, si lo que quieres es ver el objeto *desvanecerse* (una salida animada), `remove` NO es la herramienta: para eso está `self.play(FadeOut(mob))`. Usa `remove` cuando solo necesitas que un objeto deje de existir en la escena de inmediato (por ejemplo, limpiar un elemento auxiliar antes del siguiente paso del guion).

## Firma

```python
def remove(self, *mobjects: Mobject) -> Scene
```

- Acepta **uno o varios** Mobjects separados por comas (es variádico, `*mobjects`).
- Devuelve la propia `Scene` (`self`), lo que permite encadenar, aunque rara vez se hace.

### Parametros

| Parámetro | Tipo | Defecto | Controla |
|-----------|------|---------|----------|
| `*mobjects` | `Mobject` (variádico) | — | los objetos que se quitan de la escena; pueden ser varios separados por comas |

- Quitar un Mobject que **no estaba** en la escena no lanza error: la llamada simplemente no hace nada. Esto la hace segura para limpiezas defensivas.
- Si pasas un [[VGroup]] (o cualquier grupo), se quita el grupo completo de la lista de la escena.
- No hace falta pasar `run_time` ni nada parecido: al ser instantánea, no tiene parámetros de tiempo.

### Valor de retorno

`remove` edita la lista interna `self.mobjects` (la que también consulta `self.add`): elimina de ella los objetos indicados, de modo que a partir del siguiente fotograma renderizado ya no se dibujan. El cambio es **inmediato y sin transición**: el objeto desaparece de golpe. Devuelve `self` (la `Scene`). Importante: `remove` no *destruye* el Mobject en Python — la variable sigue existiendo y puedes volver a añadirlo más tarde con `self.add(mob)` o animarlo de nuevo con `self.play(...)`; solo deja de estar *en pantalla*.

## Ejemplos

### Quitar un objeto al instante

Un cuadrado entra animado, espera, y luego se quita de golpe con `remove` (desaparece sin transición):

```python
from manim import *

class QuitarUno(Scene):
    def construct(self):
        cuadro = Square(color=BLUE)
        self.play(Create(cuadro))
        self.wait()
        self.remove(cuadro)   # desaparece de golpe, sin animacion
        self.wait()
```

```bash
manim -pql archivo.py QuitarUno   # -p reproduce, -ql = calidad baja (rapido)
```

### Limpiar varios objetos a la vez

`remove` es variádico: puedes quitar varios Mobjects en una sola llamada separándolos por comas.

```python
from manim import *

class LimpiarVarios(Scene):
    def construct(self):
        a = Circle(color=RED).shift(LEFT * 2)
        b = Square(color=GREEN)
        c = Triangle(color=YELLOW).shift(RIGHT * 2)
        self.add(a, b, c)            # los tres aparecen de golpe
        self.wait()
        self.remove(a, b, c)         # los tres desaparecen de golpe
        self.wait()
```

```bash
manim -pql archivo.py LimpiarVarios
```

### Contraste: remove (instantáneo) vs FadeOut (animado)

La misma intención —que el objeto se vaya— resuelta de las dos maneras. El primer círculo desaparece de golpe; el segundo se desvanece suavemente porque va dentro de `self.play` con `FadeOut`:

```python
from manim import *

class RemoveVsFadeOut(Scene):
    def construct(self):
        izq = Circle(color=BLUE).shift(LEFT * 2)
        der = Circle(color=BLUE).shift(RIGHT * 2)
        self.play(Create(izq), Create(der))
        self.wait()
        self.remove(izq)             # se va de golpe (instantaneo)
        self.play(FadeOut(der))      # se desvanece (animado)
        self.wait()
```

```bash
manim -pql archivo.py RemoveVsFadeOut
```

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| El objeto "desaparece de golpe" cuando querías que se desvaneciera | usaste `self.remove(mob)` esperando animación | usa `self.play(FadeOut(mob))` para una salida animada |
| `remove` "no hace nada" | el Mobject nunca llegó a entrar (faltó `add`/`play`), o ya se había quitado | comprueba que el objeto estaba en `self.mobjects` antes de quitarlo |
| Querías quitarlo de la escena pero borrar la variable | `remove` no destruye el objeto en Python, solo lo saca del lienzo | `remove` es suficiente para que deje de verse; la variable puede reutilizarse |
| `TypeError` al pasar una lista | `remove` espera Mobjects sueltos, no una lista | desempaqueta con `self.remove(*lista)` |

## Notas relacionadas

- [[Scene.add]] — la operación inversa: añade Mobjects al instante.
- [[Scene.play]] — para una salida **animada** con `FadeOut`, `Uncreate`, etc.
- [[concepto_scene_construct]] — el modelo de los verbos instantáneos (`add`/`remove`) frente a `play`.
- [[escena/metodos/index|métodos de Scene]] — el resto de métodos que se usan dentro de `construct`.
