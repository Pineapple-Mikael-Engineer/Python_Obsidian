---
title: updaters — animación continua y reactiva
aliases:
  - updaters
  - add_updater
  - updater
tags:
  - manim
  - concepto
order: 6
lib: manim
tipo: concepto
requiere:
  - concepto_mobject
draft: false
---

# updaters — animación continua y reactiva

Un **updater** es una función que Manim llama **en cada fotograma** mientras un mobject la tenga puesta. Sirve para todo lo que no encaja en el molde de `self.play(...)` —que tiene un principio y un fin claros—, sino que debe ocurrir de forma **continua** o **reactiva**: un punto que sigue al cursor de otro objeto, una etiqueta que muestra un valor que va cambiando, una recta que se mantiene siempre tangente a una curva, un reloj que avanza. Mientras `self.play` dibuja *un trozo de vídeo con duración fija*, el updater corre **fotograma a fotograma durante todo el tiempo que el mobject lo lleve encima** (a lo largo de los `wait` y los `play` que vengan después de instalarlo). Es el mecanismo con el que Manim pasa de animaciones "guionizadas" a animaciones "vivas".

## Por qué existe

Con solo `self.play(...)` puedes describir cambios con principio y fin (mueve esto de A a B en 2 segundos), pero hay una familia entera de efectos que no se pueden expresar así: **mantener una relación entre objetos que cambia con el tiempo**. Si una etiqueta debe decir siempre la coordenada $x$ de un punto, no basta con animarla una vez: hay que **recalcularla en cada fotograma** mientras el punto se mueva. El updater resuelve exactamente eso —da un gancho que se ejecuta por fotograma— y, combinado con un número animable ([[ValueTracker]]), permite construir escenas donde mueves *una sola cosa* y *todo lo que depende de ella se actualiza solo*. Es la diferencia entre dibujar fotogramas a mano y declarar una dependencia que el motor mantiene viva.

```python
# self.play describe un cambio con FIN; el updater describe una RELACION continua.
from manim import *

class PorQue(Scene):
    def construct(self):
        punto = Dot()
        etiqueta = Text("sigueme")
        # "la etiqueta esta SIEMPRE encima del punto": eso es una relacion, no un cambio puntual
        etiqueta.add_updater(lambda m: m.next_to(punto, UP))
        self.add(punto, etiqueta)
        self.play(punto.animate.shift(RIGHT * 3))  # la etiqueta lo sigue sola
        self.wait()
```

```bash
manim -pql archivo.py PorQue      # -p reproduce, q=quality (l=low / h=high)
```

## El modelo: una función por fotograma

La regla mental es simple: **registras una función en el mobject, y Manim la llama una vez por cada fotograma que se renderice mientras esté registrada.** Esa función recibe el propio mobject y, opcionalmente, el tiempo transcurrido desde el fotograma anterior.

### Las dos firmas de un updater

Manim mira **cuántos parámetros** acepta tu función para decidir cómo llamarla:

| Firma | Manim la llama así | Cuándo usarla |
|-------|--------------------|----------------|
| `func(m)` | le pasa el mobject | la posición/forma depende de **otros objetos** o de un `ValueTracker` |
| `func(m, dt)` | le pasa el mobject y el delta de tiempo | la animación depende del **tiempo** (girar, avanzar un reloj) |

`dt` es el **tiempo en segundos transcurrido desde el fotograma anterior** (a 60 FPS, $dt \approx 0{,}0167$). Multiplicar por `dt` hace que el movimiento sea independiente de los FPS: `m.rotate(2 * dt)` gira a 2 radianes por segundo, salga el vídeo a la calidad que salga.

### La API de updaters

| Método | Qué hace |
|--------|----------|
| `mob.add_updater(func)` | instala `func`; se llamará cada fotograma |
| `mob.remove_updater(func)` | quita **esa** función concreta |
| `mob.clear_updaters()` | quita **todos** los updaters del mobject |
| `mob.update()` | fuerza una ejecución manual de los updaters (raro) |
| `mob.suspend_updating()` / `mob.resume_updating()` | pausa / reanuda sin desinstalar |

### always_redraw: recrear en vez de modificar

A veces no quieres *modificar* un mobject cada fotograma, sino **volver a crearlo entero** a partir de otros que cambian (una recta entre dos puntos móviles, una etiqueta cuyo texto cambia). Para eso está `always_redraw(func)`: recibe una **función sin argumentos que devuelve un mobject nuevo**, y en cada fotograma descarta el anterior y dibuja el que la función produce.

```python
linea = always_redraw(lambda: Line(p1.get_center(), p2.get_center()))
```

`always_redraw(f)` es, en esencia, azúcar para crear el mobject y ponerle un updater que lo regenera. Úsalo cuando recalcular *a mano* sería engorroso (cambia la geometría completa, no solo la posición); usa `add_updater` cuando solo ajustas un atributo (posición, color) del mismo objeto.

### ValueTracker: el número animable que mueve todo

Un updater por sí solo reacciona a *otros mobjects*. Para tener un **valor abstracto** (un ángulo, un parámetro $t$, un contador) que puedas **animar** y que los updaters **lean**, se usa [[ValueTracker]]: un mobject invisible que guarda un número.

| Operación | Código |
|-----------|--------|
| Crear con valor inicial | `t = ValueTracker(0)` |
| Leer el valor (en un updater) | `t.get_value()` |
| Fijar al instante | `t.set_value(5)` |
| **Animar** el valor | `self.play(t.animate.set_value(10))` |

El patrón estrella es: animas **un solo** `ValueTracker`, y varios updaters que leen su `get_value()` actualizan todo lo que depende de él. Mueves un número, y un punto, una etiqueta y una recta se mueven en consecuencia.

## Ejemplos progresivos

### Nivel 1: un objeto que sigue a otro (`add_updater`, firma `func(m)`)

El updater más común: mantener una etiqueta pegada a un punto que se mueve.

```python
from manim import *

class Seguir(Scene):
    def construct(self):
        punto = Dot(color=YELLOW)
        etiqueta = Text("aqui").scale(0.6)
        etiqueta.add_updater(lambda m: m.next_to(punto, UP, buff=0.2))

        self.add(punto, etiqueta)
        self.play(punto.animate.shift(RIGHT * 3 + UP))  # la etiqueta lo persigue
        self.play(punto.animate.shift(LEFT * 4))
        self.wait()
```

```bash
manim -pql archivo.py Seguir
```

La etiqueta nunca se anima directamente: solo declara *"colócate siempre encima del punto"*, y el movimiento del punto arrastra a la etiqueta.

### Nivel 2: girar con el tiempo (firma `func(m, dt)`)

Cuando el efecto depende del reloj y no de otro objeto, se usa la segunda firma con `dt`.

```python
from manim import *

class Girar(Scene):
    def construct(self):
        cuadro = Square(color=BLUE)
        cuadro.add_updater(lambda m, dt: m.rotate(0.8 * dt))  # 0.8 rad/seg, constante

        self.add(cuadro)
        self.wait(4)                 # SIN este wait no pasarian fotogramas: no se veria girar
        cuadro.clear_updaters()      # dejar de girar
        self.wait()
```

```bash
manim -pql archivo.py Girar
```

Fíjate en que el giro ocurre durante un `self.wait(4)`: el updater no necesita un `play`, solo que **el reloj avance**. Sin el `wait`, `construct` terminaría sin renderizar fotogramas y el cuadro nunca giraría.

### Nivel 3: un contador con DecimalNumber + ValueTracker

Mostrar un número que sube de 0 a 10 de forma animada: el `ValueTracker` lleva el valor, el `DecimalNumber` lo refleja cada fotograma.

```python
from manim import *

class Contador(Scene):
    def construct(self):
        tracker = ValueTracker(0)
        numero = DecimalNumber(0, num_decimal_places=2).scale(2)
        # cada fotograma, el numero copia el valor actual del tracker
        numero.add_updater(lambda m: m.set_value(tracker.get_value()))

        self.add(numero)
        self.play(tracker.animate.set_value(10), run_time=3)  # animar el VALOR
        self.wait()
```

```bash
manim -pql archivo.py Contador
```

No animamos el `DecimalNumber`: animamos el **tracker**, y el updater hace que el texto siga el valor. Cambiar `run_time` o meter un `rate_func` cambia *cómo* sube el contador sin tocar el updater.

### Nivel 4: always_redraw — una recta entre dos puntos móviles

Aquí la geometría completa cambia cada fotograma (los dos extremos se mueven), así que **recrear** es más limpio que modificar.

```python
from manim import *

class RectaViva(Scene):
    def construct(self):
        a = Dot(LEFT * 3, color=RED)
        b = Dot(RIGHT * 3, color=GREEN)
        # se RECREA la linea cada fotograma con las posiciones actuales de a y b
        linea = always_redraw(lambda: Line(a.get_center(), b.get_center(), color=YELLOW))

        self.add(a, b, linea)
        self.play(a.animate.shift(UP * 2), b.animate.shift(DOWN * 2))  # la linea se reajusta sola
        self.play(a.animate.shift(RIGHT * 5))
        self.wait()
```

```bash
manim -pql archivo.py RectaViva
```

Como `always_redraw` regenera la `Line` en cada fotograma, no hay que calcular ángulos ni longitudes: la función describe *cómo es la recta ahora* y Manim la redibuja sin parar.

### Nivel 5: todo junto — mover un punto y que todo reaccione

El patrón reactivo completo: un `ValueTracker` es la coordenada $x$ de un punto sobre una parábola; el punto, la etiqueta y una recta tangente se actualizan a la vez.

```python
from manim import *

class Reactivo(Scene):
    def construct(self):
        ejes = Axes(x_range=[-3, 3], y_range=[0, 9])
        curva = ejes.plot(lambda x: x**2, color=BLUE)
        t = ValueTracker(-2)

        punto = always_redraw(
            lambda: Dot(ejes.c2p(t.get_value(), t.get_value()**2), color=YELLOW)
        )
        etiqueta = always_redraw(
            lambda: MathTex(f"x={t.get_value():.1f}").scale(0.7).next_to(punto, UR)
        )

        self.add(ejes, curva, punto, etiqueta)
        self.play(t.animate.set_value(2), run_time=4)  # mueves UN valor; todo lo demas le sigue
        self.wait()
```

```bash
manim -pql archivo.py Reactivo
```

Solo se anima `t`. El punto se reposiciona, la etiqueta cambia su texto y su posición, y todo deriva de un único `get_value()`. Esa es la esencia de la animación reactiva en Manim.

## Casos que fallan

| Síntoma | Causa | Solución |
|---------|-------|----------|
| El updater no hace nada visible | tras `add_updater` no hubo `self.wait()` ni `self.play(...)`: no se renderizó ningún fotograma | añade un `self.wait()` o una animación después de instalarlo |
| El objeto sigue moviéndose cuando no debería | nunca quitaste el updater | `mob.remove_updater(func)` o `mob.clear_updaters()` al terminar |
| `lambda m, dt:` da error o ignora `dt` | mezclaste las firmas: pasaste `dt` donde la función solo acepta `m` (o viceversa) | usa `func(m)` si dependes de otros objetos; `func(m, dt)` si dependes del tiempo |
| El movimiento va más rápido/lento según la calidad | usaste un paso fijo (`m.shift(RIGHT*0.1)`) en vez de escalar por `dt` | multiplica por `dt`: `m.shift(RIGHT * velocidad * dt)` |
| `always_redraw` "duplica" o deja rastros del objeto | añadiste **además** el mobject original con `self.add(obj_viejo)` | añade solo el resultado de `always_redraw`, no el objeto base |
| No puedo quitar el updater con `remove_updater` | pasaste una `lambda` distinta de la que registraste (cada lambda es un objeto nuevo) | guarda la función en una variable y pásala, o usa `clear_updaters()` |
| El updater "congela" durante un `Transform` del mismo objeto | una animación que reemplaza el mobject puede chocar con su updater | quita el updater antes de transformarlo y vuelve a ponerlo después |

## Relación con otros conceptos

- [[concepto_mobject]] — el updater se instala **sobre** un mobject; es un método que todos heredan.
- [[concepto_animation]] — `self.play(...)` anima cambios con principio y fin; el updater cubre lo **continuo/reactivo**. A menudo se combinan: animas un `ValueTracker` con `play` y un updater traduce ese valor.
- [[ValueTracker]] — el número animable que es el motor de las animaciones reactivas.
- [[always_redraw]] — recrear un mobject entero por fotograma cuando su geometría depende de otros que cambian.
