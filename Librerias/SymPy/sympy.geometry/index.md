---
title: sympy.geometry — geometria analitica simbolica
tags:
  - sympy
  - indice
draft: false
---

# sympy.geometry — geometria analitica simbolica

Este submodulo cubre la **geometria analitica exacta**: las clases representan objetos geometricos (puntos, rectas, circulos, poligonos) cuyos atributos son **expresiones simbolicas** —radicales, multiples de `pi`, fracciones exactas— nunca flotantes. La diferencia frente a calcular con NumPy o Python puro es que no hay error de redondeo: `Circle(Point(0,0), 5).area` devuelve `25*pi`, no `78.539...`; `Point(0,0).distance(Point(3,4))` devuelve `5`, no `5.000000000000001`. El puente al mundo numerico es `.evalf()` sobre cualquier resultado.

El ejemplo unificador: construir un triangulo con vertices simbolicos y extraer todas sus propiedades geometricas exactas.

```python
from sympy.geometry import Triangle, Circle, Point
from sympy import symbols, sqrt, pi

a = symbols("a", positive=True)

# Triangulo rectangulo isosceles con cateto simbolico
T = Triangle(Point(0, 0), Point(a, 0), Point(0, a))

T.area                   # a**2/2
T.perimeter              # a*(2 + sqrt(2))
T.is_right               # True

T.circumcircle           # Circle(Point2D(a/2, a/2), a*sqrt(2)/2)
T.incircle               # Circle(Point2D(a*(1 - sqrt(2)/2), a*(1 - sqrt(2)/2)), ...)

# Con a = 3 (numerico):
T.area.subs(a, 3)        # 9/2    -> exacto
T.area.subs(a, 3).evalf()  # 4.50000000000000  -> float si se necesita
```

## Como se relacionan las clases

La clase central es [[Point]]: todos los demas objetos se construyen a partir de puntos. `Line` es la mas util para intersecciones y distancias; `Circle` y `Polygon`/`Triangle` son los objetos de area.

| Clase | Construida con | Atributos clave | Cuando usarla |
|-------|---------------|-----------------|---------------|
| [[Point]] | coordenadas `(x, y)` | `.x`, `.y`, `.distance()`, `.midpoint()` | Base de todo; representar posiciones exactas |
| [[Line]] | dos `Point` (o punto + pendiente) | `.slope`, `.equation()`, `.intersection()`, `.distance(point)` | Rectas infinitas; pendiente, corte, distancia punto-recta |
| [[Circle]] | `Point` centro + radio | `.area`, `.circumference`, `.equation()`, `.intersection()` | Areas/longitudes exactas con `pi`; cortes con rectas |
| [[Polygon]] | N `Point` (N >= 3) | `.area`, `.perimeter`, `.vertices`, `.sides` | Poligonos generales; cuadrilateros, pentagonos... |
| `Triangle` | exactamente 3 `Point` | todo lo de `Polygon` + `.circumcircle`, `.incircle`, `.altitudes` | Triangulos con propiedades avanzadas (inscrita, circunscrita, alturas) |

Arbol de decision:

- ¿Solo necesitas representar una posicion o calcular distancia/punto medio? -> [[Point]].
- ¿Trabajas con rectas (pendiente, ecuacion, cortes, paralelismo)? -> [[Line]].
- ¿Necesitas el area o la longitud de una curva cerrada, o cortes exactos con `pi`? -> [[Circle]].
- ¿Poligono con 3 vertices y quieres la circunscrita, inscrita o alturas? -> `Triangle` (subclase de [[Polygon]]).
- ¿Poligono con 4 o mas vertices, o poligono regular? -> [[Polygon]] o `RegularPolygon`.

> [!info] Relacion con sympy.solvers y sympy.core
> Los resultados de `sympy.geometry` son expresiones `Expr` normales de SymPy: se pueden pasar a `solve`, `simplify`, `integrate` o `lambdify` sin conversion. `T.area` es una `Expr` que puedes derivar respecto a `a` con `diff(T.area, a)`.

## Notas

- [[Point]] — punto en el plano; base de todos los objetos de esta carpeta.
- [[Line]] — recta infinita; pendiente exacta, ecuacion implicita, distancia punto-recta.
- [[Circle]] — circunferencia; area y longitud exactas con `pi`; intersecciones.
- [[Polygon]] — poligono de N vertices; area (shoelace exacto) y perimetro. Subclase `Triangle` con propiedades avanzadas.

## Notas relacionadas

- [[SymPy/index | SymPy]]
- [[Tree SymPy]]
