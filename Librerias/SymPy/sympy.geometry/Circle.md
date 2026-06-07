---
title: Circle — circunferencia simbolica con area y perimetro exactos
aliases:
  - Circle
  - circunferencia
  - circulo
tags:
  - sympy
  - api/clase
  - geometry
lib: sympy
mod: sympy.geometry
tipo: clase
retorna: Circle
requiere:
  - Point
  - Symbol
draft: false
---

# Circle — circunferencia simbolica con area y perimetro exactos

Representa una **circunferencia** definida por su centro ([[Point]]) y su radio (una expresion simbolica). El valor diferencial frente a calcular a mano es que `.area` y `.circumference` devuelven **expresiones exactas con `pi`** —`25*pi`, `pi*r**2`— sin necesidad de invocar ninguna funcion: son atributos calculados al vuelo. `.equation()` genera la ecuacion implicita estandar `x**2 + y**2 - r**2 = 0` (igualada a cero), y `.intersection()` devuelve los puntos de corte exactos con otra circunferencia o con una `Line`.

## Constructor

```python
sympy.geometry.Circle(
    center,   # Point: centro de la circunferencia
    radius,   # Expr | int | float: radio (debe ser positivo)
)             # -> Circle
```

Alternativa: `Circle(p1, p2, p3)` construye la circunferencia que pasa por tres puntos.

## Atributos y metodos clave

| Miembro | Tipo | Significado |
|---------|------|-------------|
| `.center` | `Point` | Centro de la circunferencia |
| `.radius` | `Expr` | Radio exacto |
| `.area` | `Expr` | Area exacta (`pi * r**2`) |
| `.circumference` | `Expr` | Longitud de la circunferencia (`2 * pi * r`) |
| `.equation()` | metodo | Ecuacion implicita `x**2 + y**2 - r**2` (= 0) |
| `.intersection(other)` | metodo | Lista de `Point` de corte con otra `Circle` o `Line` |
| `.is_tangent(other)` | metodo | `True` si el objeto es tangente a la circunferencia |
| `.encloses_point(p)` | metodo | `True` si el `Point` esta estrictamente dentro |

## Ejemplo

```python
from sympy.geometry import Circle, Point, Line
from sympy import symbols, pi

# Circulo numerico
C = Circle(Point(0, 0), 5)
C.center                    # Point2D(0, 0)
C.radius                    # 5
C.area                      # 25*pi
C.circumference             # 10*pi
C.equation()                # x**2 + y**2 - 25   (= 0)

# Circulo simbolico
r = symbols("r", positive=True)
Cs = Circle(Point(0, 0), r)
Cs.area                     # pi*r**2
Cs.circumference            # 2*pi*r

# Interseccion con una recta
L = Line(Point(-5, 0), Point(5, 0))   # eje x
C.intersection(L)           # [Point2D(-5, 0), Point2D(5, 0)]

# Circulo por tres puntos
from sympy.geometry import Circle
C3 = Circle(Point(0, 0), Point(1, 0), Point(0, 1))
C3.center                   # Point2D(1/2, 1/2)
C3.radius                   # sqrt(2)/2
```

> [!info] area vs circumference
> `Circle` sigue la convencion de SymPy Geometry: `.area` es el area del **disco** (region interior) y `.circumference` es la longitud de la **curva**. Ambos son atributos (sin parentesis), no metodos.

## Errores comunes

| Error | Causa | Solucion |
|-------|-------|----------|
| `GeometryError: ... not a valid radius` | Radio negativo o cero | Usa `symbols("r", positive=True)` o un entero positivo |
| `.intersection()` devuelve `[]` | Los circulos no se cortan (disjuntos o uno dentro del otro) | Verifica distancia entre centros vs suma/diferencia de radios |
| `.equation()` usa `x` e `y` pero mis simbolos son distintos | El metodo genera con sus propias variables por defecto | Pasa `x=u, y=v` al metodo: `C.equation(x=u, y=v)` |
| `Circle(p1, p2, p3)` lanza error | Los tres puntos son colineales (no definen un circulo) | Comprueba que no esten en la misma recta |

## Notas relacionadas

- [[Point]]
- [[Line]]
- [[Polygon]]
- [[sympy.geometry/index | sympy.geometry]]
