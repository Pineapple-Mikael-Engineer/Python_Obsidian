---
title: to_edge() y to_corner() — pegar al borde o a la esquina del frame
aliases:
  - to_edge
  - to_corner
  - to_edge to_corner
tags:
  - manim
  - api/metodo
  - posicionamiento
lib: manim
tipo: metodo
obj: Mobject
order: 4
requiere:
  - concepto_sistema_coordenadas
draft: false
---

# to_edge() y to_corner() — pegar al borde o a la esquina del frame

`to_edge` y `to_corner` colocan un Mobject **respecto a los límites de la pantalla**, no respecto a otro objeto. Mientras que [[next_to]] coloca "al lado de aquel círculo" y `move_to` lleva a una coordenada exacta, estos dos dicen "pégate arriba del todo" o "vete a la esquina inferior derecha" sin que tengas que calcular el medio-ancho del frame (`~7.11`) ni el medio-alto (`4.0`) a mano. Son los métodos para los elementos que viven en el marco: un **título** arriba, una **marca de agua** en una esquina, una **leyenda** abajo. `to_edge` pega a uno de los cuatro bordes (`UP`, `DOWN`, `LEFT`, `RIGHT`); `to_corner` pega a una de las cuatro esquinas (`UL`, `UR`, `DL`, `DR`). Ambos dejan un **margen** configurable (`buff`) entre el objeto y el límite, y ambos devuelven `self` para encadenar.

## to_edge

Mueve el objeto hasta que su borde correspondiente toca el borde del frame indicado, dejando `buff` unidades de margen. No cambia su posición en el eje perpendicular: `to_edge(UP)` lo sube hasta arriba pero **conserva su `x` actual** (no lo centra horizontalmente).

```python
def to_edge(
    self,
    edge: np.ndarray = LEFT,   # borde de destino: UP / DOWN / LEFT / RIGHT
    buff: float = MED_LARGE_BUFF,   # margen entre el objeto y el borde (0.5 por defecto)
) -> Mobject:
    ...
```

### Parametros

#### `edge` — a qué borde pegar

Una de las **cuatro constantes cardinales** de dirección ([[concepto_sistema_coordenadas]]): `UP` (borde superior), `DOWN` (inferior), `LEFT` (izquierdo), `RIGHT` (derecho). El valor por defecto es `LEFT`, así que **casi siempre lo pasas explícito**. Solo afecta al eje de esa dirección: con `edge=UP` el objeto sube al tope pero su coordenada `x` no se toca; con `edge=LEFT` se pega a la izquierda pero su `y` se conserva.

| Quiero el objeto… | Llamada |
|-------------------|---------|
| arriba del todo (un título) | `mob.to_edge(UP)` |
| abajo del todo (una leyenda) | `mob.to_edge(DOWN)` |
| pegado a la izquierda | `mob.to_edge(LEFT)` |
| pegado a la derecha | `mob.to_edge(RIGHT)` |

#### `buff` — el margen hasta el borde

Float en unidades de escena: cuánto **separa** el objeto del límite del frame. Por defecto vale `MED_LARGE_BUFF` (`0.5`). Manim define un escalón de constantes de buffer que conviene usar en vez de números mágicos: `SMALL_BUFF` (`0.1`), `MED_SMALL_BUFF` (`0.25`), `MED_LARGE_BUFF` (`0.5`), `LARGE_BUFF` (`1.0`). Con `buff=0` el objeto queda **literalmente tocando** el borde (a menudo se ve recortado); súbelo para despegarlo.

### Valor de retorno

Devuelve `self` (el mismo Mobject), de modo que puedes **encadenar**: `Text("Hola").to_edge(UP).set_color(YELLOW)`. El efecto es inmediato (sin animación); para animar el movimiento usa la sintaxis `.animate`: `self.play(mob.animate.to_edge(UP))`.

## to_corner

Mueve el objeto hasta una de las **cuatro esquinas** del frame, pegándolo simultáneamente a los **dos** bordes que forman esa esquina, con `buff` de margen en ambos. Es, en esencia, `to_edge` aplicado a la vez en horizontal y en vertical.

```python
def to_corner(
    self,
    corner: np.ndarray = DL,   # esquina de destino: UL / UR / DL / DR
    buff: float = MED_LARGE_BUFF,   # margen a cada uno de los dos bordes (0.5 por defecto)
) -> Mobject:
    ...
```

### Parametros

#### `corner` — a qué esquina pegar

Una de las **cuatro constantes diagonales**: `UL` (arriba-izquierda), `UR` (arriba-derecha), `DL` (abajo-izquierda), `DR` (abajo-derecha). Recuerda que las diagonales son la suma de dos cardinales (`UR == UP + RIGHT`), así que `to_corner(UR)` equivale a pegar arriba **y** a la derecha. El defecto es `DL`, normalmente lo pasas explícito.

| Quiero el objeto en la esquina… | Llamada |
|---------------------------------|---------|
| superior izquierda | `mob.to_corner(UL)` |
| superior derecha | `mob.to_corner(UR)` |
| inferior izquierda | `mob.to_corner(DL)` |
| inferior derecha (marca de agua) | `mob.to_corner(DR)` |

#### `buff` — el margen hasta los bordes

Igual que en `to_edge`: float en unidades de escena, por defecto `MED_LARGE_BUFF` (`0.5`). Aquí el margen se aplica **a los dos bordes** que tocan la esquina, así que el objeto queda separado tanto en horizontal como en vertical.

### Valor de retorno

Devuelve `self`, encadenable igual que `to_edge`. Sin animación por defecto; envuélvelo en `.animate` para animarlo.

## to_edge vs to_corner

| | `to_edge` | `to_corner` |
|--|-----------|-------------|
| Pega a… | **un** borde | **dos** bordes (una esquina) |
| Constante que recibe | cardinal: `UP` `DOWN` `LEFT` `RIGHT` | diagonal: `UL` `UR` `DL` `DR` |
| Eje perpendicular | **se conserva** (no centra el otro eje) | ambos ejes quedan fijados a la esquina |
| Uso típico | título arriba, leyenda abajo, barra lateral | marca de agua, logo, contador en una esquina |
| Equivalencia | — | `to_corner(UR)` ≈ `to_edge(UP)` **y** `to_edge(RIGHT)` a la vez |

La regla mental: si te basta con "arriba" (sin importar el centrado horizontal), `to_edge`; si quieres clavar el objeto en una **esquina**, `to_corner`.

## Ejemplos

### Un título pegado arriba con to_edge(UP)

El caso más común: un texto que hace de título y se queda en el tope del frame.

```python
from manim import *

class TituloArriba(Scene):
    def construct(self):
        titulo = Text("Mi animación", font_size=48)
        titulo.to_edge(UP)           # sube al borde superior, conserva su x (centrado)
        self.play(Write(titulo))
        self.wait()
```

```bash
manim -pql archivo.py TituloArriba      # -p reproduce, -ql = calidad baja (rapido)
```

### Una marca de agua en una esquina con to_corner(DR)

Un texto pequeño clavado en la esquina inferior derecha, como una firma.

```python
from manim import *

class MarcaDeAgua(Scene):
    def construct(self):
        contenido = Circle(color=BLUE).scale(2)
        firma = Text("@miCanal", font_size=24, color=GRAY)
        firma.to_corner(DR)          # esquina inferior derecha
        self.add(contenido, firma)
        self.wait()
```

```bash
manim -pql archivo.py MarcaDeAgua
```

### Margen personalizado con buff

El mismo título, pero más despegado del borde usando una constante de buffer mayor.

```python
from manim import *

class BuffPersonalizado(Scene):
    def construct(self):
        ceñido = Text("buff=0", font_size=36).to_edge(UP, buff=0)
        holgado = Text("buff=LARGE_BUFF", font_size=36).to_edge(DOWN, buff=LARGE_BUFF)
        self.add(ceñido, holgado)
        self.wait()
```

```bash
manim -pql archivo.py BuffPersonalizado
```

### Varios objetos en distintos bordes y esquinas

Combinando los dos métodos para poblar el marco de la escena.

```python
from manim import *

class MarcoCompleto(Scene):
    def construct(self):
        self.add(
            Text("arriba", font_size=28).to_edge(UP),
            Text("abajo", font_size=28).to_edge(DOWN),
            Text("izq", font_size=28).to_edge(LEFT),
            Text("der", font_size=28).to_edge(RIGHT),
            Dot(color=RED).to_corner(UL),
            Dot(color=GREEN).to_corner(UR),
            Dot(color=BLUE).to_corner(DL),
            Dot(color=YELLOW).to_corner(DR),
        )
        self.wait()
```

```bash
manim -pql archivo.py MarcoCompleto
```

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| El objeto se sale por arriba/abajo del frame | el Mobject es **más alto que el frame**; pegarlo a un borde no lo encoge | redúcelo con `scale(...)` antes de posicionar, o baja el `font_size` |
| Pasaste una diagonal a `to_edge` | `to_edge(UR)` mezcla dos ejes y da un resultado raro | usa una **cardinal** (`UP`/`DOWN`/`LEFT`/`RIGHT`) en `to_edge`; para esquina usa `to_corner` |
| Pasaste una cardinal a `to_corner` | `to_corner(UP)` no llega a una esquina | usa una **diagonal** (`UL`/`UR`/`DL`/`DR`) en `to_corner` |
| Esperabas que `to_edge(UP)` centrara el objeto en horizontal | `to_edge` **no toca** el eje perpendicular | combina con `set_x(0)` o usa `to_corner` si quieres fijar ambos ejes |
| El objeto queda tocando el borde y se ve recortado | `buff` demasiado pequeño (o `0`) | sube `buff` a `MED_LARGE_BUFF` o `LARGE_BUFF` |
| El movimiento ocurre de golpe pese a querer animarlo | llamaste `mob.to_edge(...)` directo | anímalo: `self.play(mob.animate.to_edge(UP))` |

## Notas relacionadas

- [[concepto_sistema_coordenadas]] — de dónde salen `UP`/`DOWN`/`UL`/`DR` y el tamaño del frame que estos métodos usan como referencia.
- [[next_to]] — el contraste: colocar respecto a **otro objeto**, no respecto al frame.
- [[shift_move_to]] — desplazar relativo (`shift`) o colocar en una coordenada absoluta (`move_to`).
- [[align_to]] — alinear el borde de un objeto con el de otro sin pegarlo al frame.
- [[arrange]] — distribuir los hijos de un grupo; luego el grupo entero se ancla con `to_edge`/`to_corner`.
- [[Manim/posicionamiento/index | posicionamiento]] — el panorama de los métodos de colocación.
