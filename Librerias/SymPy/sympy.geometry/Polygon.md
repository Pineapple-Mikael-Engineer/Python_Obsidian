---
title: Polygon — poligono simbolico con area y perimetro exactos
aliases:
  - Polygon
  - poligono
  - Triangle
  - triangulo
tags:
  - sympy
  - api/clase
  - geometry
lib: sympy
mod: sympy.geometry
tipo: clase
retorna: Polygon
requiere:
  - Point
  - Symbol
draft: false
---

# Polygon — poligono simbolico con area y perimetro exactos

Representa un **poligono convexo o concavo** definido por una secuencia ordenada de [[Point]]. El area se calcula con la formula de Gauss (shoelace) sobre las coordenadas exactas, lo que garantiza un resultado racional o en radicales —nunca un float—, con el signo correcto segun la orientacion de los vertices (positivo = sentido antihorario). El perimetro es la suma de las distancias exactas entre vertices consecutivos. La subclase `Triangle` (tres vertices) añade propiedades geometricas avanzadas: alturas, circunscrita, inscrita y clasificacion del triangulo.

## Constructor

```python
sympy.geometry.Polygon(
    *vertices,   # Point: vertices en orden (minimo 3)
)                # -> Polygon  |  Triangle (si son exactamente 3)

sympy.geometry.Triangle(
    *vertices,   # Point: exactamente 3 vertices
)                # -> Triangle
```

`Polygon` con 3 vertices crea automaticamente un `Triangle`; con 4 un `Quadrilateral`; con mas, un `Polygon` generico.

## Atributos y metodos clave

| Miembro | Tipo | Aplica a | Significado |
|---------|------|----------|-------------|
| `.vertices` | `list[Point]` | todos | Lista de vertices en orden |
| `.sides` | `list[Segment]` | todos | Lados como segmentos |
| `.area` | `Expr` | todos | Area exacta (shoelace con signo) |
| `.perimeter` | `Expr` | todos | Perimetro exacto (suma de lados) |
| `.is_convex()` | metodo | todos | `True` si el poligono es convexo |
| `.encloses_point(p)` | metodo | todos | `True` si `p` esta dentro |
| `.altitudes` | `dict` | `Triangle` | Alturas: `{vertice: segmento}` |
| `.circumcircle` | `Circle` | `Triangle` | Circunscrita (pasa por los 3 vertices) |
| `.incircle` | `Circle` | `Triangle` | Inscrita (tangente a los 3 lados) |
| `.medians` | `dict` | `Triangle` | Medianas desde cada vertice |
| `.is_equilateral()` | metodo | `Triangle` | `True` si los 3 lados son iguales |
| `.is_right` | atributo | `Triangle` | `True` si tiene un angulo recto |

## Ejemplo

```python
from sympy.geometry import Polygon, Triangle, Point

# Cuadrado unitario
Q = Polygon(Point(0,0), Point(1,0), Point(1,1), Point(0,1))
Q.area         # 1
Q.perimeter    # 4
Q.is_convex()  # True

# Triangulo rectangulo 3-4-5
T = Triangle(Point(0,0), Point(4,0), Point(0,3))
T.area         # 6
T.perimeter    # 12   (3 + 4 + 5)
T.is_right     # True

# Propiedades avanzadas de Triangle
T.circumcircle           # Circle(Point2D(2, 3/2), 5/2)
T.incircle               # Circle(Point2D(1, 1), 1)

# Vertices simbolicos
from sympy import symbols
a = symbols("a", positive=True)
Ts = Triangle(Point(0,0), Point(a,0), Point(0,a))
Ts.area        # a**2/2
Ts.perimeter   # a*(2 + sqrt(2))
```

> [!info] Signo del area
> El area tiene signo segun la orientacion: vertices en sentido **antihorario** dan area positiva; en sentido horario, negativa. Para obtener el valor absoluto usa `Abs(T.area)` o simplemente comprueba el orden de tus vertices. `Triangle` siempre devuelve area positiva independientemente del orden.

## Tabla de decision — Polygon vs Triangle vs RegularPolygon

| Situacion | Clase recomendada |
|-----------|-------------------|
| 3 vertices cualesquiera, con propiedades geometricas (circunscrita, alturas...) | `Triangle` |
| 4 o mas vertices, proposito general | `Polygon` |
| Poligono regular de N lados (pentagono, hexagono...) | `RegularPolygon(centro, radio, n)` |
| Solo area/perimetro de un poligono simple | `Polygon` |

## Errores comunes

| Error | Causa | Solucion |
|-------|-------|----------|
| `GeometryError: Polygon requires at least 3 vertices` | Menos de 3 puntos | Añade el tercer vertice |
| `.area` devuelve `0` | Los vertices son colineales (degenerado) | Comprueba que no esten todos en la misma recta |
| `.circumcircle` da error en `Polygon` | Solo disponible en `Triangle` | Usa exactamente 3 vertices o construye con `Triangle(...)` |
| `Abs` en el area | Vertices en sentido horario | Reordena los vertices en sentido antihorario |

## Notas relacionadas

- [[Point]]
- [[Line]]
- [[Circle]]
- [[sympy.geometry/index | sympy.geometry]]
