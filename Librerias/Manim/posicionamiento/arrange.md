---
title: arrange() — distribuir los submobjects en fila o columna
aliases:
  - arrange
  - arrange_in_grid
tags:
  - manim
  - api/metodo
  - posicionamiento
lib: manim
tipo: metodo
obj: VGroup
order: 6
requiere:
  - concepto_sistema_coordenadas
draft: false
---

# arrange() — distribuir los submobjects en fila o columna

`arrange` ordena los **hijos de un [[VGroup]]** (sus submobjects) en una fila o columna, separados por un margen uniforme, sin que tengas que colocar cada uno a mano con `shift` o `move_to`. Es el método estrella para los **layouts**: en vez de calcular la posición de cinco figuras una por una, las metes en un grupo y llamas `grupo.arrange(RIGHT)`. Con `direction=RIGHT` quedan en **fila**; con `direction=DOWN`, en **columna**. Opera sobre el orden en que los submobjects entraron al grupo y los recoloca relativos unos a otros; luego, el grupo entero se ancla en la escena con `move_to`, `to_edge` o `to_corner`. Su pariente `arrange_in_grid` hace lo mismo en **rejilla**.

## Firma

```python
def arrange(
    self,
    direction: np.ndarray = RIGHT,   # RIGHT = fila, DOWN = columna
    buff: float = DEFAULT_MOBJECT_TO_MOBJECT_BUFFER,   # separación entre vecinos (0.25)
    center: bool = True,             # recentrar el grupo en su posición tras ordenar
    **kwargs,                        # de alineación, p. ej. aligned_edge
) -> Mobject:
    ...
```

### Parametros

#### `direction` — el eje de distribución

Una constante de dirección ([[concepto_sistema_coordenadas]]) que marca **hacia dónde crece** la disposición. Las dos habituales: `RIGHT` (los hijos se ponen en **fila**, de izquierda a derecha, en el orden en que entraron al grupo) y `DOWN` (en **columna**, de arriba abajo). También valen `LEFT` y `UP` (invierten el sentido). Por defecto `RIGHT`.

| Quiero… | Llamada |
|---------|---------|
| una fila (izquierda → derecha) | `grupo.arrange(RIGHT)` |
| una columna (arriba → abajo) | `grupo.arrange(DOWN)` |
| una fila en sentido inverso | `grupo.arrange(LEFT)` |

#### `buff` — la separación entre vecinos

Float en unidades de escena: cuánto **espacio** queda entre cada par de hijos consecutivos. Por defecto vale `DEFAULT_MOBJECT_TO_MOBJECT_BUFFER` (`0.25`). Igual que en otros métodos de posición, puedes usar las constantes `SMALL_BUFF`, `MED_LARGE_BUFF`, `LARGE_BUFF` en vez de números mágicos. `buff=0` los deja pegados.

#### `center` — recentrar tras ordenar

Bool, por defecto `True`. Cuando es `True`, tras distribuir a los hijos el método **recentra el grupo entero** sobre su posición original (el centro del grupo no se desplaza). Con `center=False`, el primer hijo se queda donde estaba y los demás crecen a partir de él, así que el grupo se desplaza hacia un lado.

#### `aligned_edge` (kwarg) — alinear el eje perpendicular

Pasado entre los `**kwargs`. Por defecto `arrange` **centra** los hijos en el eje perpendicular al de `direction` (en una columna, todos quedan centrados horizontalmente). Con `aligned_edge` igualas en cambio un **borde**: en una columna, `aligned_edge=LEFT` hace que todos los hijos compartan su borde izquierdo (como un `align_to` interno), útil para listas de texto que deben arrancar en la misma vertical.

### Valor de retorno

Devuelve `self` (el propio grupo), encadenable: `VGroup(a, b, c).arrange(RIGHT).to_edge(UP)`. El reordenamiento es inmediato; para animarlo, `self.play(grupo.animate.arrange(DOWN))`.

## Ejemplos

### Una fila de figuras con arrange(RIGHT)

El layout más simple: tres figuras alineadas horizontalmente con una sola llamada.

```python
from manim import *

class FilaSimple(Scene):
    def construct(self):
        grupo = VGroup(Circle(), Square(), Triangle())
        grupo.arrange(RIGHT, buff=0.5)     # en fila, separadas 0.5
        self.play(Create(grupo))
        self.wait()
```

```bash
manim -pql archivo.py FilaSimple      # -p reproduce, -ql = calidad baja (rapido)
```

### Una columna con arrange(DOWN)

Cambiando solo la dirección, los mismos objetos se apilan en vertical.

```python
from manim import *

class ColumnaSimple(Scene):
    def construct(self):
        grupo = VGroup(
            Text("primero"),
            Text("segundo"),
            Text("tercero"),
        )
        grupo.arrange(DOWN, buff=0.4)      # en columna, de arriba abajo
        self.play(Write(grupo))
        self.wait()
```

```bash
manim -pql archivo.py ColumnaSimple
```

### buff y aligned_edge en una lista de texto

Una columna de textos de distinto largo, alineados todos por su borde izquierdo en vez de centrados.

```python
from manim import *

class ListaAlineada(Scene):
    def construct(self):
        items = VGroup(
            Text("uno", font_size=36),
            Text("treinta y tres", font_size=36),
            Text("dos", font_size=36),
        )
        items.arrange(DOWN, buff=0.5, aligned_edge=LEFT)   # mismo borde izquierdo
        items.to_edge(LEFT)                                # ancla el grupo a la izquierda
        self.add(items)
        self.wait()
```

```bash
manim -pql archivo.py ListaAlineada
```

### En rejilla con arrange_in_grid

Cuando quieres una matriz de objetos en vez de una sola fila o columna, el pariente `arrange_in_grid(rows, cols, buff)` los distribuye en una rejilla.

```python
from manim import *

class Rejilla(Scene):
    def construct(self):
        cuadros = VGroup(*[Square(side_length=0.8) for _ in range(6)])
        cuadros.arrange_in_grid(rows=2, cols=3, buff=0.3)   # 2 filas x 3 columnas
        self.play(Create(cuadros))
        self.wait()
```

```bash
manim -pql archivo.py Rejilla
```

## arrange y VGroup

`arrange` no posiciona objetos sueltos: actúa sobre los **submobjects** de quien lo llama, así que esos objetos tienen que ser **hijos de un grupo** primero. Por eso casi siempre se usa sobre un [[VGroup]] (o `Group`): el grupo es lo que **tiene** submobjects que ordenar. El patrón canónico es de dos pasos:

1. **Agrupar** — `grupo = VGroup(a, b, c)` mete los objetos como submobjects.
2. **Distribuir** — `grupo.arrange(RIGHT)` los recoloca unos respecto a otros.

Recién creado, un `VGroup` **no ordena** a sus miembros (aparecen donde cada uno estuviera); `arrange` es justamente lo que les da una disposición. Y como `arrange` solo coloca a los hijos **relativos entre sí**, después decides dónde va el conjunto: `grupo.to_edge(UP)` o `grupo.move_to(ORIGIN)` ancla el bloque ya formado en la escena.

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| `arrange` no ordena nada / objetos sueltos no se mueven | los llamaste sobre objetos que **no son submobjects de un grupo** | mételos primero en un [[VGroup]] y llama `arrange` sobre el grupo |
| El grupo aparece descentrado tras `arrange` | usaste `center=False` (crece desde el primer hijo) | deja `center=True`, o ancla luego con `move_to`/`to_edge` |
| Los textos de la columna salen centrados, no a ras | por defecto `arrange` **centra** el eje perpendicular | pasa `aligned_edge=LEFT` (o el borde que quieras) |
| Esperabas una rejilla y salió una sola fila | `arrange` solo hace fila o columna | usa `arrange_in_grid(rows, cols, buff)` |
| `VGroup(lista).arrange(...)` falla | pasaste una **lista** al constructor en vez de argumentos sueltos | desempaqueta: `VGroup(*lista)` |
| El grupo entero quedó fuera de cuadro | `arrange` no controla **dónde** va el grupo, solo la disposición interna | ánclalo después con `move_to`/`to_edge`/`to_corner` |

## Notas relacionadas

- [[VGroup]] — el contenedor cuyos submobjects ordena `arrange`; sin grupo no hay nada que distribuir.
- [[concepto_sistema_coordenadas]] — las direcciones `RIGHT`/`DOWN` que marcan el eje de la fila o columna.
- [[to_edge_to_corner]] — anclar el grupo ya distribuido contra los bordes del frame.
- [[shift_move_to]] — mover el grupo entero a una posición tras ordenarlo por dentro.
- [[align_to]] — alinear bordes de objetos sueltos (lo que `aligned_edge` hace dentro del grupo).
- [[Manim/posicionamiento/index | posicionamiento]] — el panorama de los métodos de colocación.
