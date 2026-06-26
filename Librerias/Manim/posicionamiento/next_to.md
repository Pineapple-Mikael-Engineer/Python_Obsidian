---
title: next_to() — colocar al lado de otro objeto
aliases:
  - next_to
  - Mobject.next_to
  - colocar al lado
tags:
  - manim
  - api/metodo
  - posicionamiento
lib: manim
tipo: metodo
obj: Mobject
order: 3
requiere:
  - concepto_sistema_coordenadas
draft: false
---

# next_to() — colocar al lado de otro objeto

`next_to` es el método para colocar un Mobject **junto a** otro (o junto a un punto), sin calcular coordenadas a mano. Le dices "ponte a la derecha de aquella figura" y él se ocupa de medir el tamaño de ambos y dejar un hueco. Es el caballo de batalla para **etiquetar** figuras, **apilar** elementos y construir disposiciones relativas: una flecha al lado de un texto, un título encima de un diagrama, una fila de cajas pegadas. A diferencia de [[shift_move_to|move_to]] (que centra un objeto **sobre** otro), `next_to` lo deja **al lado**, separado por un margen `buff`. Es un método heredado de [[Mobject]] que devuelve `self`, así que se aplica al instante y se encadena; habla el idioma de las [[constantes_direccion|constantes de dirección]] tanto para el lado (`direction`) como para el margen (`buff`).

## Firma

```python
Mobject.next_to(
    mobject_or_point: Mobject | np.ndarray,   # la referencia: otro Mobject, o un punto
    direction: np.ndarray = RIGHT,            # de que lado de la referencia colocarse
    buff: float = 0.25,                       # hueco entre ambos (MED_SMALL_BUFF)
    aligned_edge: np.ndarray = ORIGIN,        # alinear un borde comun (centra por defecto)
    submobject_to_align: Mobject | None = None,
    index_of_submobject_to_align: int | None = None,
    coor_mask: np.ndarray = np.array([1, 1, 1]),  # restringe los ejes que se mueven
) -> Self
```

### Parametros

#### `mobject_or_point` — la referencia

El primer argumento es **respecto a qué** te colocas. Casi siempre es **otro Mobject** (`etiqueta.next_to(figura, ...)`): `next_to` mide su caja envolvente y se sitúa a su lado. También acepta un **punto** de escena (`mob.next_to(ORIGIN, UP)`), útil para colocarse respecto a una coordenada fija sin un objeto de referencia. El objeto que llama (`self`) es el que se mueve; la referencia no se toca.

#### `direction` — de qué lado

La dirección, una [[constantes_direccion|constante]], indica **de qué lado** de la referencia te pones. `RIGHT` (defecto) a la derecha, `UP` encima, `DOWN` debajo, `LEFT` a la izquierda; las diagonales (`UR`, `DL`...) lo colocan en diagonal respecto a la referencia. Es lo primero que se ajusta:

```python
etiqueta.next_to(figura, UP)      # encima
etiqueta.next_to(figura, DOWN)    # debajo
etiqueta.next_to(figura, LEFT)    # a la izquierda
```

#### `buff` — el margen entre ambos

El **hueco** que se deja entre el objeto y la referencia, en unidades de escena. Por defecto `0.25` (`MED_SMALL_BUFF`), que ya separa visiblemente. Para pegar casi sin aire usa `buff=SMALL_BUFF` (0.1) o `buff=0`; para airear, `buff=LARGE_BUFF` (1.0) o un float. Es el parámetro que más se toca tras `direction`:

```python
etiqueta.next_to(figura, UP, buff=SMALL_BUFF)   # casi pegada
etiqueta.next_to(figura, UP, buff=0)            # sin hueco, tocando
```

#### `aligned_edge` — alinear un borde común

Por defecto `ORIGIN`: en el eje perpendicular a `direction`, ambos quedan **centrados**. Si pasas una dirección, alinea ese **borde** en lugar de centrar. Por ejemplo, al colocar una etiqueta a la derecha (`RIGHT`), `aligned_edge=UP` alinea los **bordes superiores** de objeto y referencia en vez de centrarlos verticalmente; `aligned_edge=DOWN` alinea las bases. Sirve para que una etiqueta lateral quede "a ras" de arriba o de abajo en vez de a media altura.

#### `submobject_to_align` / `index_of_submobject_to_align`

Para Mobjects compuestos (un `VGroup`, un `Text` con varias letras): en vez de alinear contra la caja del objeto entero, alinea respecto a **un submobject** concreto (por referencia o por índice). Son de uso avanzado y rara vez se tocan; con un Mobject simple no hacen falta.

#### `coor_mask` — restringir los ejes

Vector máscara de 3 componentes que multiplica el desplazamiento: un `0` **congela** ese eje. Permite mover el objeto al lado de la referencia solo en uno de los ejes y dejar el otro como estaba. De uso raro; el defecto `[1, 1, 1]` mueve en todos.

### Valor de retorno

Devuelve `self` —el propio Mobject ya colocado—, así que encadena (`Text("A").next_to(c, UP).set_color(YELLOW)`) y se anima dentro de `play` con `.animate`. Importante: `next_to` calcula la posición **una sola vez**, con el tamaño y la posición que la referencia tiene en ese instante; **no** es un vínculo vivo. Si luego mueves la referencia, el objeto **no** la sigue (para eso hace falta un updater; ver [[concepto_updaters]]).

## Ejemplos

### Etiquetar una figura

El uso estrella: poner un texto justo encima de una figura.

```python
from manim import *

class Etiquetar(Scene):
    def construct(self):
        figura = Circle(color=BLUE)
        etiqueta = Text("circulo").scale(0.6)
        etiqueta.next_to(figura, UP, buff=SMALL_BUFF)   # encima, casi pegada
        self.play(Create(figura), FadeIn(etiqueta))
        self.wait()
```

```bash
manim -pql archivo.py Etiquetar      # -p reproduce, -ql = calidad baja (rapido)
```

### Apilar con buff

Variando solo `direction` y `buff` se apilan elementos en columna con el aire que quieras.

```python
from manim import *

class Apilar(Scene):
    def construct(self):
        a = Square(color=RED).scale(0.5)
        b = Square(color=GREEN).scale(0.5).next_to(a, DOWN, buff=0.1)
        c = Square(color=BLUE).scale(0.5).next_to(b, DOWN, buff=0.1)
        self.add(a, b, c)
        self.wait()
```

```bash
manim -pql archivo.py Apilar
```

### aligned_edge para alinear bordes

Dos etiquetas a la derecha de una caja alta: una centrada (defecto) y otra alineada por arriba con `aligned_edge=UP`.

```python
from manim import *

class AlinearBordes(Scene):
    def construct(self):
        caja = Rectangle(color=GREY, height=3, width=1.5)
        centrada = Text("centro").scale(0.5).next_to(caja, RIGHT)
        arriba = Text("arriba").scale(0.5).next_to(caja, RIGHT, aligned_edge=UP)
        arriba.shift(DOWN * 0)   # queda a ras del borde superior de la caja
        self.add(caja, centrada, arriba)
        self.wait()
```

```bash
manim -pql archivo.py AlinearBordes
```

### Encadenar varios next_to en fila

Cada objeto se coloca a la derecha del anterior: una fila construida paso a paso.

```python
from manim import *

class EnFila(Scene):
    def construct(self):
        primero = Square(color=RED).scale(0.4)
        anterior = primero
        grupo = [primero]
        for color in [GREEN, BLUE, YELLOW, WHITE]:
            nuevo = Square(color=color).scale(0.4).next_to(anterior, RIGHT, buff=0.2)
            grupo.append(nuevo)
            anterior = nuevo
        self.add(*grupo)
        self.wait()
```

```bash
manim -pql archivo.py EnFila
```

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| La etiqueta no sigue a la figura cuando esta se mueve | `next_to` fija la posición **una vez**, no es un vínculo vivo | reagrupa en un `VGroup` y mueve el grupo, o usa un updater ([[concepto_updaters]]) |
| Objeto y referencia quedan superpuestos | usaste `move_to` (centra encima) en vez de `next_to` | usa `next_to`, que deja al lado con `buff` |
| El hueco es mayor/menor del esperado | el `buff` por defecto es `0.25`, no 0 | pásalo explícito: `buff=0` para tocar, `buff=LARGE_BUFF` para airear |
| Colocas respecto al objeto equivocado | invertiste quién llama y quién es referencia | el que **llama** se mueve: `etiqueta.next_to(figura, ...)` mueve la etiqueta |
| Las etiquetas laterales quedan a distinta altura | dejaste el centrado por defecto | usa `aligned_edge=UP`/`DOWN` para alinear el borde |
| `next_to(figura)` sin más lo deja a la derecha sin querer | `direction` por defecto es `RIGHT` | pásalo: `next_to(figura, UP)` |

## Notas relacionadas

- [[constantes_direccion]] — `direction` y `buff` salen de aquí (`UP`, `RIGHT`, `MED_SMALL_BUFF`...).
- [[shift_move_to]] — `move_to` centra **sobre** otro objeto; `next_to` lo deja **al lado**.
- [[to_edge_to_corner]] — colocar relativo al **frame** (borde/esquina) en vez de a otro objeto.
- [[align_to]] — alinear un borde con el de otro objeto sin separación.
- [[arrange]] — distribuir un grupo entero con un solo `next_to` interno automatizado.
- [[concepto_updaters]] — para que la etiqueta **siga** a la referencia si esta se mueve.
- [[posicionamiento/index|posicionamiento]] — el índice del grupo.
