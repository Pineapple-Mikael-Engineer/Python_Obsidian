---
title: always_redraw() — recrear un mobject cada fotograma
aliases:
  - always_redraw
  - redraw
tags:
  - manim
  - api/funcion
  - dinamico
lib: manim
tipo: funcion
order: 3
requiere:
  - concepto_updaters
draft: false
---

# always_redraw() — recrear un mobject cada fotograma

`always_redraw(func)` crea un mobject que se **redibuja por completo en cada fotograma**: en vez de modificar un objeto existente, llama a una función que **lo reconstruye desde cero** y reemplaza el anterior por el nuevo. Es el atajo para cuando resulta más fácil **recrear** el objeto que ajustarlo en su sitio: una recta entre dos puntos que se mueven, una etiqueta cuyo texto se recalcula, un área bajo una curva que cambia de forma. Internamente devuelve un mobject con un [[concepto_updaters|updater]] que en cada frame hace `become(func(...))` —descarta su geometría y adopta la de lo que `func` produce—, así que basta con describir *cómo es el objeto ahora* y Manim lo mantiene al día. Contrasta con [[add_updater]]: `add_updater` **modifica** el mismo objeto fotograma a fotograma (cambia un atributo); `always_redraw` lo **recrea** entero. Como todo updater, solo se ve actuar mientras pase tiempo de vídeo (`self.wait` / `self.play`).

## Firma

```python
def always_redraw(
    func: Callable[..., Mobject],    # funcion que CONSTRUYE y devuelve un mobject nuevo
    *args,                           # argumentos posicionales que se pasan a func cada frame
    **kwargs,                        # argumentos por nombre que se pasan a func cada frame
) -> Mobject:                        # el mobject que se autorredibuja (es el que se añade)
    ...
```

Lo habitual es llamarla con una `lambda` sin argumentos que captura los mobjects de los que depende: `always_redraw(lambda: Line(a.get_center(), b.get_center()))`. Los `*args`/`**kwargs` solo se usan si prefieres una función con parámetros explícitos en vez de capturar por clausura.

### Parametros

#### `func` — la función que reconstruye el objeto

El argumento central: una **función que devuelve un mobject nuevo** cada vez que se llama. Manim la invoca en cada fotograma y usa su resultado como el aspecto actual del objeto. La clave es que `func` debe construir el mobject leyendo el **estado actual** de aquello de lo que depende —`a.get_center()`, `tracker.get_value()`, etc.— para que el resultado refleje el fotograma presente. Suele ser una `lambda` sin parámetros que captura por clausura los objetos relevantes:

```python
# la recta se reconstruye con las posiciones ACTUALES de a y b en cada frame
linea = always_redraw(lambda: Line(a.get_center(), b.get_center(), color=YELLOW))
```

> [!warning] No captures valores que se reasignan
> `func` debe leer el **estado vivo** de los mobjects (`a.get_center()`), no un valor calculado una vez. Si dentro escribes algo como `centro = a.get_center()` antes y luego usas `centro`, congelas el valor del primer frame. Lee siempre dentro de la función.

#### `*args`, `**kwargs` — argumentos reenviados a func

Si `func` acepta parámetros, lo que pongas en `*args`/`**kwargs` se le **reenvía en cada llamada** (cada fotograma). Permite parametrizar la reconstrucción sin clausuras. En la práctica casi siempre se usa la forma `always_redraw(lambda: ...)` sin argumentos, capturando lo necesario por clausura, así que estos parámetros se ven poco.

### Valor de retorno

Devuelve **el mobject que se autorredibuja**: el objeto que produce la **primera** llamada a `func`, ya equipado con un updater que en cada fotograma ejecuta `func` de nuevo y hace `become(...)` con el resultado. Ese objeto devuelto es **el que debes añadir a la escena** (`self.add(...)`) y guardar en una variable; es a través de él que el redibujado vive. No añadas además el mobject "base" del que depende como si fuera el dibujo: el resultado de `always_redraw` ya es el dibujo.

## Ejemplos

### Una recta entre dos puntos móviles

El caso canónico: la geometría completa (los dos extremos) cambia cada fotograma, así que **recrear** la `Line` es más limpio que recalcular ángulos y longitudes a mano.

```python
from manim import *

class RectaViva(Scene):
    def construct(self):
        a = Dot(LEFT * 3, color=RED)
        b = Dot(RIGHT * 3, color=GREEN)
        # se RECREA la linea cada fotograma con las posiciones actuales de a y b
        linea = always_redraw(lambda: Line(a.get_center(), b.get_center(), color=YELLOW))

        self.add(a, b, linea)
        self.play(a.animate.shift(UP * 2), b.animate.shift(DOWN * 2))   # la linea se reajusta sola
        self.play(a.animate.shift(RIGHT * 5))
        self.wait()
```

```bash
manim -pql archivo.py RectaViva      # -p reproduce, -ql = calidad baja (rapido)
```

La función describe *cómo es la recta ahora*; Manim la redibuja sin que haya que calcular nada.

### Una etiqueta decimal que se recalcula con un ValueTracker

Cuando lo que cambia es el **texto** (no solo la posición), recrear es la vía natural: un [[ValueTracker]] lleva el valor y la etiqueta se reconstruye con su lectura actual.

```python
from manim import *

class EtiquetaViva(Scene):
    def construct(self):
        t = ValueTracker(0)
        # la etiqueta se REGENERA cada frame con el valor actual del tracker
        etiqueta = always_redraw(
            lambda: MathTex(f"x = {t.get_value():.2f}").scale(1.5)
        )

        self.add(etiqueta)
        self.play(t.animate.set_value(10), run_time=3)   # se anima el VALOR; el texto le sigue
        self.wait()
```

```bash
manim -pql archivo.py EtiquetaViva
```

No se anima la etiqueta: se anima `t`, y en cada fotograma `always_redraw` construye un `MathTex` nuevo con el valor del momento. (Para un número puro, [[DecimalNumber]] con [[add_updater]] evita recompilar LaTeX cada frame; `always_redraw` brilla cuando cambia la estructura del texto, no solo la cifra.)

### Una recta tangente que sigue a un punto sobre una curva

El patrón reactivo completo: un `ValueTracker` es la coordenada $x$ de un punto sobre una parábola; el punto y la **recta tangente** se reconstruyen a partir de él. La tangente cambia de posición y de pendiente cada frame, así que recrearla es lo más cómodo.

```python
from manim import *

class TangenteViva(Scene):
    def construct(self):
        ejes = Axes(x_range=[-3, 3], y_range=[0, 9])
        curva = ejes.plot(lambda x: x**2, color=BLUE)
        t = ValueTracker(-2)

        punto = always_redraw(
            lambda: Dot(ejes.c2p(t.get_value(), t.get_value()**2), color=YELLOW)
        )
        # la recta tangente se reconstruye con la pendiente 2x del punto actual
        tangente = always_redraw(
            lambda: ejes.get_secant_slope_group(
                x=t.get_value(), graph=curva, dx=0.01,
                secant_line_color=RED, secant_line_length=4,
            )
        )

        self.add(ejes, curva, punto, tangente)
        self.play(t.animate.set_value(2), run_time=4)   # mueves UN valor; todo le sigue
        self.wait()
```

```bash
manim -pql archivo.py TangenteViva
```

Solo se anima `t`. El punto se reposiciona y la tangente cambia de inclinación, todo derivado de un único `get_value()` recreando los objetos cada fotograma.

## add_updater vs. always_redraw

| | [[add_updater]] | `always_redraw` |
|--|------------------|-----------------|
| Qué hace cada frame | **modifica** el mismo objeto (ajusta un atributo) | **recrea** el objeto entero (`become(func())`) |
| Cuándo conviene | cambia posición, color, ángulo, valor | cambia la **geometría/estructura** completa |
| La función | recibe el mobject: `func(m)` o `func(m, dt)` | **no recibe nada** y **devuelve** un mobject nuevo |
| Coste | barato (solo toca atributos) | mayor: construye un objeto nuevo por frame |
| Qué se añade a la escena | el mobject original | **el resultado** de `always_redraw` |

Usa `always_redraw` cuando recalcular a mano sería engorroso (cambia la forma completa); usa `add_updater` cuando solo ajustas un atributo del mismo objeto.

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| El objeto no se actualiza, queda congelado | `func` capturó un valor calculado una vez (`c = a.get_center()`) en vez de leer el estado vivo | lee dentro de la función cada frame: `lambda: Line(a.get_center(), ...)` |
| Aparecen el objeto viejo y el nuevo a la vez | añadiste **también** el mobject base con `self.add(obj_viejo)` además del de `always_redraw` | añade solo el resultado de `always_redraw`, no el objeto base |
| No se ve cambiar nada | tras añadirlo no hubo `self.wait()` ni `self.play(...)`: no se renderizó ningún fotograma | añade un `wait` o una animación que haga avanzar el tiempo |
| La escena va lenta o tartamudea | recrear un mobject caro (mucho LaTeX/puntos) cada frame es costoso | si solo cambia un atributo, usa [[add_updater]] en su lugar |
| `always_redraw(Line(...))` da error o no se actualiza | pasaste un **mobject ya construido**, no una **función** | pasa una función: `always_redraw(lambda: Line(...))` |
| `become` falla / el texto LaTeX parpadea | la función devuelve tipos de mobject incompatibles entre frames | que `func` devuelva siempre el mismo tipo de mobject |

## Notas relacionadas

- [[concepto_updaters]] — el concepto base; `always_redraw` es azúcar para un updater que hace `become(func())` cada frame.
- [[add_updater]] — el contraste: **modificar** el mismo objeto en vez de recrearlo; cuándo elegir cada uno.
- [[ValueTracker]] — el número animable que la función de `always_redraw` lee con `get_value()` para reconstruir el objeto.
- [[DecimalNumber]] — para un número puro que cambia, suele ser mejor `DecimalNumber` + `add_updater` que recompilar LaTeX cada frame.
- [[Scene.play]] — lo que anima el `ValueTracker` del que el redibujado depende.
