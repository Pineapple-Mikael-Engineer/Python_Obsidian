---
title: Point — punto en el plano con coordenadas simbolicas
aliases:
  - Point
  - Point2D
  - punto
tags:
  - sympy
  - api/clase
  - geometry
lib: sympy
mod: sympy.geometry
tipo: clase
retorna: Point
requiere:
  - Symbol
draft: false
---

# Point — punto en el plano con coordenadas simbolicas

Representa un **punto en el plano** (o en N dimensiones) cuyas coordenadas son expresiones simbolicas exactas, no flotantes. `Point(0, 0)` y `Point(sqrt(2), Rational(1, 3))` son igualmente validos. Internamente SymPy crea un `Point2D` para dos coordenadas; el alias `Point` es el constructor recomendado. Los puntos soportan **aritmetica vectorial** (suma, resta, escala) y los metodos geometricos clave —distancia exacta y punto medio— devuelven siempre [[concepto_expr_arbol | Expr]] exactas.

## Constructor

```python
sympy.geometry.Point(
    *coords,          # numericos o Expr: las coordenadas del punto
    evaluate=True,    # si simplifica las coordenadas al construir
)                     # -> Point2D  (para 2 coordenadas)
```

## Atributos y metodos clave

| Miembro | Tipo | Significado |
|---------|------|-------------|
| `.x` | `Expr` | Primera coordenada |
| `.y` | `Expr` | Segunda coordenada |
| `.distance(other)` | metodo | Distancia exacta entre dos `Point` (`sqrt` sin evaluar a float) |
| `.midpoint(other)` | metodo | Punto medio exacto; devuelve un nuevo `Point2D` |
| `.translate(x, y)` | metodo | Desplaza el punto; devuelve nuevo `Point2D` |
| `.rotate(angle, pt)` | metodo | Rota respecto a `pt` (angulo en radianes simbolicos) |
| `.distance(Line)` | metodo | Distancia del punto a una [[Line]] (shortcut de `Line.distance`) |

## Ejemplo

```python
from sympy.geometry import Point
from sympy import sqrt, Rational

P1 = Point(0, 0)
P2 = Point(3, 4)

P1.distance(P2)           # 5
P1.midpoint(P2)           # Point2D(3/2, 2)

# Aritmetica vectorial
P1 + P2                   # Point2D(3, 4)
P2 - P1                   # Point2D(3, 4)
2 * P2                    # Point2D(6, 8)

# Coordenadas simbolicas
from sympy import symbols
a, b = symbols("a b", real=True)
P = Point(a, b)
P.distance(Point(0, 0))   # sqrt(a**2 + b**2)
```

> [!info] Exactitud garantizada
> `Point(3, 4).distance(Point(0, 0))` devuelve `5` (entero exacto), no `5.0`. SymPy simplifica el radical cuando es perfecto; de lo contrario conserva la forma `sqrt(...)`. Si necesitas un float, aplica `.evalf()` al resultado.

## Errores comunes

| Error | Causa | Solucion |
|-------|-------|----------|
| `TypeError: ... not a valid coordinate` | Se paso una lista/tupla en vez de argumentos separados | `Point(3, 4)`, no `Point([3, 4])` |
| Distancia devuelve `sqrt(...)` sin simplificar | Las coordenadas contienen simbolos sin supuestos | Añade `real=True` o `positive=True` al crear los simbolos |
| `AttributeError: 'Point3D' object has no attribute 'y'` nunca ocurre pero dimensiones mezcladas dan error | Mezcla de `Point2D` con `Point3D` | Usa siempre la misma dimension; `Point(x, y, z)` crea `Point3D` |

## Notas relacionadas

- [[Line]]
- [[Circle]]
- [[Polygon]]
- [[sympy.geometry/index | sympy.geometry]]
