---
title: escena basica — el esqueleto minimo de una Scene
aliases:
  - escena basica
  - esqueleto Scene
  - plantilla Scene
tags:
  - manim
  - patron
  - patrones
lib: manim
tipo: patron
order: 1
requiere:
  - concepto_scene_construct
draft: false
---

# escena básica — el esqueleto mínimo de una Scene

Esta receta resuelve la primera pregunta de todo el que abre Manim: ¿cuál es el código mínimo que tengo que escribir para que algo aparezca en pantalla? La respuesta es siempre el mismo esqueleto —subclasear `Scene`, sobreescribir `construct`, crear un Mobject, animarlo y esperar— seguido de un comando de render. Toda animación de Manim, por compleja que sea, empieza calcando esta plantilla; por eso es el patrón fundacional del que cuelgan los demás. Úsala cada vez que arranques un archivo nuevo: es el "hola mundo" que copias antes de empezar a pensar en lo que quieres mostrar.

## El problema

Quieres que Manim dibuje algo y lo guarde como vídeo, pero no hay una función suelta que llamar (`dibuja(circulo)` no existe). Manim no funciona con llamadas imperativas dispersas: necesita una **clase** que él pueda instanciar y un **método** que pueda ejecutar para grabar el guion. Sin ese andamiaje —la clase que hereda de [[Scene]] y el método `construct`— no hay dónde colgar las instrucciones, y el render no produce nada. La receta es ese andamiaje mínimo, listo para rellenar.

## La receta

Una Scene completa y ejecutable: crea un círculo, lo dibuja animadamente, lo desplaza y espera. Es el esqueleto que copiarás al empezar cualquier archivo.

```python
from manim import *                       # 1. trae todo: Scene, Circle, Create, las constantes...

class MiEscena(Scene):                    # 2. subclaseas Scene: tu escena ES una Scene
    def construct(self):                  # 3. sobreescribes construct(self): aqui va el guion
        circulo = Circle(color=BLUE)      # 4. creas un Mobject (todavia NO esta en pantalla)
        self.play(Create(circulo))        # 5. lo dibujas con una animacion (esto dura y se ve)
        self.play(circulo.animate.shift(RIGHT * 2))  # 6. lo mueves, tambien animado
        self.wait()                       # 7. pausas 1 s manteniendo el ultimo fotograma
```

```bash
manim -pql archivo.py MiEscena      # -p reproduce al terminar, -ql = calidad baja (rapido)
```

El comando nombra el archivo (`archivo.py`) y la clase a renderizar (`MiEscena`): Manim instancia esa clase, ejecuta su `construct` una vez y ensambla los fotogramas en un `.mp4`.

## Como funciona

Cada pieza del esqueleto tiene un papel fijo; entender el reparto es entender el ciclo de una escena.

### Subclasear Scene y sobreescribir construct

No instancias `Scene` ni llamas a `construct` tú mismo: defines una **subclase** y Manim hace ambas cosas por ti. Al ejecutar `manim archivo.py MiEscena`, el motor instancia `MiEscena()` y llama a su `construct(self)` exactamente una vez. Por eso `construct` **debe** llevar `self` (es un método) y por eso nunca lo invocas a mano: es un gancho que Manim dispara, igual que un framework de GUI llama a tu manejador de eventos. Tu único trabajo es **describir** el guion dentro de él.

### El orden de las instrucciones ES el orden del vídeo

Manim lee `construct` de arriba abajo, y ese orden de líneas se convierte literalmente en el orden temporal del vídeo: primero se dibuja el círculo, luego se mueve, luego viene la pausa. No hay un planificador que reordene nada; leer el `construct` es leer el guion de principio a fin. Mover la línea del `shift` antes del `Create` cambiaría el vídeo.

### self.play vs self.add vs self.wait

Son los tres verbos del esqueleto, y la diferencia entre ellos es la causa número uno de sorpresas al empezar.

| Verbo | Qué hace | ¿Dura / se anima? |
|-------|----------|-------------------|
| `self.play(anim)` | reproduce una Animation (`Create`, `Transform`, `.animate`...) | sí: ocupa `run_time` segundos y se ve cambiar |
| `self.add(mobj)` | mete el Mobject en pantalla al instante, sin animación | no: aparece de golpe en un fotograma |
| `self.wait(t)` | pausa `t` segundos (1 por defecto) congelando el último fotograma | mantiene, no anima |

La regla que no falla: **`add` es instantáneo, `play` es lo único que se ve animarse**. Si algo "aparece de golpe" cuando esperabas una animación, casi seguro lo metiste con `add` en vez de con `self.play(Create(...))`. Crear el Mobject (`circulo = Circle(...)`) tampoco lo muestra: solo lo construye en memoria; hasta que no pasa por `add` o `play` no entra en la escena.

## Variaciones

Tres ajustes que harás constantemente sobre el esqueleto base.

### Varias escenas en un mismo archivo

Un archivo puede contener todas las escenas que quieras: cada `class X(Scene)` es independiente, y eliges cuál renderizar nombrándola en el comando.

```python
from manim import *

class Intro(Scene):
    def construct(self):
        self.play(Write(Text("Hola")))
        self.wait()

class Final(Scene):
    def construct(self):
        self.play(Create(Square(color=GREEN)))
        self.wait()
```

```bash
manim -pql archivo.py Intro     # renderiza solo Intro
manim -pql archivo.py Final     # renderiza solo Final
manim -pql -a archivo.py        # -a (all): renderiza TODAS las escenas del archivo
```

### Dividir la escena en secciones con next_section

`self.next_section("nombre")` marca un corte lógico dentro de `construct`: con `--save_sections` Manim exporta cada tramo como un clip aparte, útil para reusar trozos o montar por partes.

```python
from manim import *

class PorSecciones(Scene):
    def construct(self):
        self.next_section("Aparece el titulo")
        titulo = Text("Teorema").to_edge(UP)
        self.play(Write(titulo))

        self.next_section("Aparece la formula")
        self.play(FadeIn(MathTex("a^2 + b^2 = c^2")))
        self.wait()
```

```bash
manim -pql --save_sections archivo.py PorSecciones    # un clip por seccion
```

### Subir a calidad alta para el render final

El esqueleto no cambia: solo cambias la bandera de calidad del comando. `-ql` (low) es rápido para iterar; `-qh` (high) es el render de entrega.

```bash
manim -pql archivo.py MiEscena      # baja (480p15): borrador rapido mientras trabajas
manim -pqh archivo.py MiEscena      # alta (1080p60): el render final
manim -pqk archivo.py MiEscena      # 4K (2160p60): maxima resolucion
```

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| `construct() takes 1 positional argument but 2 were given` | escribiste `def construct():` sin `self` | siempre `def construct(self):` |
| No se ve nada / vídeo vacío | creaste el Mobject pero no lo añadiste ni animaste | mételo con `self.add(m)` o `self.play(Create(m))` |
| Todo aparece de golpe | usaste `self.add` esperando que se animara | usa `self.play(Create(...))` o `.animate` |
| El vídeo dura 0 segundos | solo usaste `add`/`remove` (instantáneos), sin `play` ni `wait` | añade al menos un `self.wait()` o una animación |
| `NameError: name 'Circle' is not defined` | faltó el import | `from manim import *` como primera línea |
| `manim: error ... Scene ... not found` | el nombre de clase del comando no coincide con el del archivo | nombra en el comando la clase exacta: `manim ... archivo.py MiEscena` |

## Notas relacionadas

- [[concepto_scene_construct]] — el modelo mental completo: la Scene como lienzo y guion, y el ciclo de vida de `construct`
- [[Scene]] — la clase base que subclaseas, con sus variantes (`MovingCameraScene`, `ThreeDScene`) y atributos de `self`
- [[concepto_render_cli]] — el comando `manim` en detalle: banderas de calidad, `-p`, `-a`, formatos de salida
- [[concepto_animate_syntax]] — la sintaxis `.animate` que usa el paso 6 para animar un cambio
- [[Manim/patrones/index | patrones]] — el índice de las recetas, con cuál elegir para qué
