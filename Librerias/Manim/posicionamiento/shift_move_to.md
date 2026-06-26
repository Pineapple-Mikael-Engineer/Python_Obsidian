---
title: shift y move_to — mover relativo vs colocar absoluto
aliases:
  - shift
  - move_to
  - Mobject.shift
  - Mobject.move_to
tags:
  - manim
  - api/metodo
  - posicionamiento
lib: manim
tipo: metodo
obj: Mobject
order: 2
requiere:
  - concepto_sistema_coordenadas
draft: false
---

# shift y move_to — mover relativo vs colocar absoluto

Son el par fundamental del posicionamiento, y la diferencia entre ambos es la primera distinción que hay que tener clara en Manim. `shift` mueve **relativo**: suma un vector a la posición actual, sin importarle dónde estaba ni dónde acaba, solo *cuánto* se desplaza. `move_to` coloca **absoluto**: lleva el centro del Mobject a un punto exacto (o al centro de otro Mobject), sin importarle de dónde venía, solo *dónde* acaba. Ambos son métodos heredados de [[Mobject]] que devuelven `self`, así que se aplican al instante y se **encadenan**; para *animar* el movimiento se usan dentro de `play` con la sintaxis [[concepto_animate_syntax|.animate]]. Hablan el idioma de las [[constantes_direccion|constantes de dirección]]: el vector que les pasas casi siempre se construye con `UP`, `RIGHT`, `ORIGIN` y aritmética.

## shift

`shift` aplica un **desplazamiento relativo**: toma uno o varios vectores, los suma, y mueve el Mobject esa cantidad desde donde esté ahora. Es acumulativo (cada `shift` parte de la posición resultante del anterior) y es el método natural cuando piensas en términos de "muévelo un poco más a la derecha" en vez de "ponlo en tal coordenada".

```python
Mobject.shift(*vectors: np.ndarray) -> Self
```

### Parametros

| Parametro | Tipo | Defecto | Que controla |
|-----------|------|---------|--------------|
| `*vectors` | `np.ndarray` (uno o varios) | — | el/los vector(es) de desplazamiento; si pasas varios, se **suman** antes de aplicarse |

El argumento es posicional y variádico: lo normal es pasar un único vector construido con constantes (`mob.shift(RIGHT * 2)`), pero `mob.shift(UP, RIGHT)` es válido y equivale a `mob.shift(UP + RIGHT)`. Debe ser un vector (array de 3 componentes), no un número suelto: `mob.shift(2)` falla.

### Valor de retorno

Devuelve `self` —el propio Mobject ya desplazado—, lo que permite **encadenar**: `Square().shift(UP).shift(RIGHT)` o, más idiomático, `Square().shift(UP).set_color(RED)`. Como modifica el objeto in situ y al instante, fuera de `play` el cambio no se anima; para verlo ocurrir, `self.play(mob.animate.shift(...))`.

## move_to

`move_to` hace un **posicionamiento absoluto**: lleva el centro del Mobject a un punto dado, o al centro de **otro** Mobject si le pasas un Mobject en vez de un punto. Es el método para "ponlo exactamente aquí", independientemente de su posición previa. Con `aligned_edge` puedes alinear por un borde en vez de por el centro, y con `coor_mask` restringir el movimiento a ciertos ejes.

```python
Mobject.move_to(
    point_or_mobject: np.ndarray | Mobject,   # destino: un punto, o un Mobject (usa su centro)
    aligned_edge: np.ndarray = ORIGIN,        # que parte del objeto se alinea al destino
    coor_mask: np.ndarray = np.array([1, 1, 1]),  # que ejes se mueven (1 = si, 0 = se ignora)
) -> Self
```

### Parametros

#### `point_or_mobject` — el destino

El primer argumento es el destino y acepta **dos formas**. Si le das un **punto** (un vector de escena), lleva el centro del Mobject a esa coordenada: `mob.move_to(LEFT * 3)`. Si le das **otro Mobject**, lleva el centro del Mobject al centro de ese otro: `etiqueta.move_to(figura)` superpone la etiqueta sobre la figura. Es la sobrecarga que hace `move_to` tan cómodo para "centrar A sobre B".

#### `aligned_edge` — alinear por un borde en vez del centro

Por defecto `ORIGIN`, que significa "alinea el **centro** del objeto con el destino". Si pasas una dirección (`UP`, `LEFT`, `UR`...), alinea ese **borde o esquina** del objeto con el destino en lugar del centro. Por ejemplo `mob.move_to(ORIGIN, aligned_edge=DOWN)` deja el **borde inferior** del objeto en el origen (el objeto queda por encima del centro), útil para apoyar algo "sobre" un punto.

#### `coor_mask` — restringir los ejes que se mueven

Un vector de 3 componentes que actúa de **máscara**: multiplica componente a componente el movimiento, así que un `0` **congela** ese eje. `mob.move_to(otro, coor_mask=np.array([1, 0, 0]))` iguala solo la `x` (lo alinea horizontalmente con `otro`) y deja la `y` intacta. Es la forma de "muévelo al destino, pero solo en horizontal".

### Valor de retorno

Devuelve `self`, igual que `shift`, así que también encadena (`Dot().move_to(UP).set_color(RED)`) y se anima con `.animate`. La diferencia clave no está en el retorno sino en la **semántica**: `move_to` ignora la posición previa.

## shift vs move_to

La elección entre uno y otro depende de si piensas en términos de *cuánto mover* o de *dónde acabar*.

| | `shift(v)` | `move_to(p)` |
|--|-----------|--------------|
| Tipo | **relativo**: suma `v` a la posición actual | **absoluto**: lleva el centro a `p` |
| Le importa | cuánto se desplaza | dónde acaba |
| Punto de partida | sí influye (acumulativo) | se ignora |
| Acepta otro Mobject | no (solo vectores) | sí (usa su centro) |
| Pensamiento típico | "súbelo 2 unidades más" | "ponlo en el origen" / "céntralo sobre X" |
| Mismo punto de llegada da igual de dónde venga | no | sí |

Regla mental: si dos objetos parten de sitios distintos y quieres que acaben **en el mismo lugar**, usa `move_to` (a ambos les das el mismo destino). Si quieres moverlos **lo mismo** conservando su separación, usa `shift` (a ambos el mismo vector).

## Ejemplos

### shift acumulativo

Cada `shift` parte de donde dejó el anterior: tres pasos relativos encadenados.

```python
from manim import *

class ShiftAcumulativo(Scene):
    def construct(self):
        c = Square(color=BLUE).move_to(LEFT * 5)
        self.add(c)
        self.play(c.animate.shift(RIGHT * 3))   # de LEFT*5 a LEFT*2
        self.play(c.animate.shift(RIGHT * 3))   # de LEFT*2 a RIGHT*1
        self.play(c.animate.shift(UP * 2))      # y luego sube
        self.wait()
```

```bash
manim -pql archivo.py ShiftAcumulativo      # -p reproduce, -ql = calidad baja (rapido)
```

### move_to a un punto absoluto

Da igual desde dónde: el objeto acaba justo en el punto indicado.

```python
from manim import *

class MoveToPunto(Scene):
    def construct(self):
        c = Circle(color=GREEN).move_to(DL * 3)   # arranca abajo-izquierda
        self.add(c)
        self.play(c.animate.move_to(ORIGIN))      # al centro exacto
        self.play(c.animate.move_to(RIGHT * 4 + UP * 2))  # a una coordenada concreta
        self.wait()
```

```bash
manim -pql archivo.py MoveToPunto
```

### move_to al centro de otro objeto

Pasando un Mobject en vez de un punto, el centro de uno va al centro del otro: aquí la etiqueta se centra sobre el cuadrado.

```python
from manim import *

class MoveToObjeto(Scene):
    def construct(self):
        caja = Square(color=BLUE, fill_opacity=0.3).scale(1.5).shift(RIGHT * 2)
        etiqueta = Text("A").scale(0.8)
        self.add(caja, etiqueta)
        self.wait()
        self.play(etiqueta.animate.move_to(caja))   # la etiqueta salta al centro de la caja
        self.wait()
```

```bash
manim -pql archivo.py MoveToObjeto
```

### aligned_edge: apoyar por un borde

Con `aligned_edge` el objeto se alinea al destino por el borde indicado en vez de por el centro: aquí ambos cuadrados van al origen, pero el segundo se apoya por su base.

```python
from manim import *

class AlignedEdge(Scene):
    def construct(self):
        marca = Dot(ORIGIN, color=YELLOW)             # el destino, marcado
        por_centro = Square(color=BLUE).scale(0.8)
        por_centro.move_to(ORIGIN)                     # centro en el origen
        por_base = Square(color=RED).scale(0.8)
        por_base.move_to(ORIGIN, aligned_edge=DOWN)    # base en el origen -> queda arriba
        self.add(marca, por_centro, por_base)
        self.wait()
```

```bash
manim -pql archivo.py AlignedEdge
```

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| `shift` no lleva el objeto a la coordenada que querías | `shift` es **relativo**: suma a la posición actual | usa `move_to(punto)` para un destino absoluto |
| `move_to` "pierde" el desplazamiento previo | `move_to` ignora de dónde venía | si querías acumular, usa `shift` |
| `mob.shift(2)` o `mob.move_to(3)` falla | pasaste un número, no un vector | usa direcciones: `shift(RIGHT * 2)`, `move_to(RIGHT * 3)` |
| El objeto se mueve de golpe pese a estar en `play` | usaste `c.shift(...)` directo en vez de `.animate` | `self.play(c.animate.shift(...))` |
| `move_to((3, 5))` no cae donde esperabas en un `Axes` | usaste coords de **escena**, no las matemáticas | traduce con `axes.c2p(3, 5)` (ver [[concepto_sistema_coordenadas]]) |
| `aligned_edge` no hace nada | dejaste el defecto `ORIGIN` (alinea por el centro) | pásale una dirección: `aligned_edge=UP` |
| `AttributeError` al encadenar sobre `self.play(...)` | `play` devuelve `None`; `shift`/`move_to` sí devuelven `self` | encadena sobre el **Mobject**, no sobre el `play` |

## Notas relacionadas

- [[constantes_direccion]] — los vectores (`UP`, `RIGHT`, `ORIGIN`...) que se pasan a ambos métodos.
- [[concepto_sistema_coordenadas]] — el plano donde caen los puntos y la distinción escena vs coords matemáticas.
- [[next_to]] — el otro relativo: colocar **al lado de** otro objeto con margen.
- [[to_edge_to_corner]] — relativo al **frame**: pegar al borde o esquina.
- [[align_to]] — alinear un borde con el de otro objeto sin superponer centros.
- [[concepto_animate_syntax]] — animar `shift` / `move_to` dentro de `play`.
- [[posicionamiento/index|posicionamiento]] — el índice del grupo.
