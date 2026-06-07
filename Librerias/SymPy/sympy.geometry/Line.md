---
title: Line — recta definida por dos puntos o punto y direccion
aliases:
  - Line
  - Line2D
  - recta
tags:
  - sympy
  - api/clase
  - geometry
lib: sympy
mod: sympy.geometry
tipo: clase
retorna: Line
requiere:
  - Point
  - Symbol
draft: false
---

# Line — recta definida por dos puntos o punto y direccion

Representa una **recta infinita** en el plano cuya definicion, pendiente, ecuacion y relaciones con otros objetos geometricos son **expresiones exactas**. A diferencia de `Segment` (un trozo de recta) o `Ray` (semirrecta), `Line` es la recta completa. Se construye con dos [[Point]] (el caso mas comun) o con un punto y un vector de direccion. Todos los atributos —pendiente, coeficientes de la ecuacion implicita— devuelven `Expr` simbolicas; las relaciones (`is_parallel`, `is_perpendicular`) devuelven `True/False` o expresiones booleanas simbolicas.

## Constructor

```python
sympy.geometry.Line(
    p1,          # Point: primer punto de la recta
    p2,          # Point | Expr: segundo punto, o coeficiente de direccion
    **kwargs,
)                # -> Line2D
```

`p2` puede ser un `Point` o un numero/expresion que actua como pendiente si `p1` es el punto base.

## Atributos y metodos clave

| Miembro | Tipo | Significado |
|---------|------|-------------|
| `.slope` | `Expr` | Pendiente exacta (`m = (y2-y1)/(x2-x1)`); `zoo` si es vertical |
| `.equation()` | metodo | Ecuacion implicita `ax + by + c = 0` como `Expr` (igualada a 0) |
| `.intersection(other)` | metodo | Lista de `Point` de corte con otra `Line`, `Segment` o `Circle` |
| `.distance(point)` | metodo | Distancia exacta de un `Point` a la recta |
| `.is_parallel(other)` | metodo | `True` si son paralelas |
| `.is_perpendicular(other)` | metodo | `True` si son perpendiculares |
| `.perpendicular_line(point)` | metodo | Recta perpendicular que pasa por `point` |
| `.parallel_line(point)` | metodo | Recta paralela que pasa por `point` |
| `.contains(point)` | metodo | `True` si el `Point` pertenece a la recta |

## Ejemplo

```python
from sympy.geometry import Line, Point
from sympy import symbols, sqrt

# Recta que pasa por el origen con pendiente 1
L1 = Line(Point(0, 0), Point(1, 1))
L1.slope                    # 1
L1.equation()               # -x + y        (= 0 implicita)

# Distancia de un punto a la recta y = x
L1.distance(Point(1, 0))    # sqrt(2)/2

# Dos rectas: paralela y perpendicular
L2 = Line(Point(0, 1), Point(1, 2))   # y = x + 1, paralela a L1
L3 = Line(Point(0, 0), Point(1, -1))  # y = -x, perpendicular a L1

L1.is_parallel(L2)          # True
L1.is_perpendicular(L3)     # True

# Interseccion
L4 = Line(Point(0, 2), Point(2, 0))   # y = -x + 2
L1.intersection(L4)         # [Point2D(1, 1)]

# Recta vertical
Lv = Line(Point(2, 0), Point(2, 5))
Lv.slope                    # zoo  (infinito simbolico)
Lv.equation()               # x - 2
```

> [!info] Ecuacion implicita
> `.equation()` devuelve la expresion `ax + by + c` que se asume igual a cero, no una `Eq`. Para construir una `Eq` explicita: `Eq(L.equation(), 0)`. Por defecto usa las variables `x` e `y`; puedes pasar `x1, y1 = symbols("x1 y1")` al metodo si tus simbolos tienen otro nombre.

## Errores comunes

| Error | Causa | Solucion |
|-------|-------|----------|
| `GeometryError: ... degenerate Line` | Los dos puntos son identicos | Verifica que `p1 != p2` antes de construir |
| `.slope` devuelve `zoo` | La recta es vertical (`x = cte`) | Es el valor correcto: pendiente infinita. Usa `.equation()` para la forma util |
| `.intersection(other)` devuelve `[]` | Las rectas son paralelas (sin corte) | Comprueba con `.is_parallel(other)` antes |
| `.distance(Line)` da error de tipo | `distance` espera un `Point`, no otra `Line` | Para distancia entre paralelas: `L1.distance(L2.p1)` |

## Notas relacionadas

- [[Point]]
- [[Circle]]
- [[Polygon]]
- [[sympy.geometry/index | sympy.geometry]]
