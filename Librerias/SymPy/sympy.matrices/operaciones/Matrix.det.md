---
title: Matrix.det — determinante simbolico exacto
aliases:
  - det
  - determinante
tags:
  - sympy
  - api/metodo
  - matrices/operaciones
lib: sympy
mod: sympy.matrices
tipo: metodo
obj: Matrix
retorna: Expr
requiere:
  - Matrix
draft: false
---

# Matrix.det — determinante simbolico exacto

Calcula el determinante de una [[Matrix]] de forma **exacta y simbolica**, sin redondeo. Para matrices pequenas (2×2, 3×3) aplica expansion por cofactores; para matrices mas grandes usa el algoritmo de Bareiss (libre de fracciones) o LU segun el metodo solicitado. El resultado es una `Expr` que puede contener simbolos, radicales o enteros exactos.

## Firma

```python
M.det(method=None)
```

| Parametro | Tipo | Descripcion |
|-----------|------|-------------|
| `method` | `str \| None` | Algoritmo a usar. `None` = seleccion automatica |

Metodos disponibles para `method`:

| Valor | Algoritmo | Cuando usarlo |
|-------|-----------|---------------|
| `None` | automatico | Siempre (elige el mejor segun el tamano) |
| `'bareiss'` | Bareiss (division entera) | Matrices grandes con coeficientes enteros |
| `'berkowitz'` | Berkowitz | Matrices simbolicas sin supuestos de dominio |
| `'lu'` | Descomposicion LU | Matrices numericas o cuando LU ya esta disponible |

## Valor de retorno

| Entrada | Retorno | Descripcion |
|---------|---------|-------------|
| Matriz 2×2 simbolica | `Expr` con simbolos | Forma algebraica exacta |
| Matriz numerica entera | `Integer` | Entero exacto sin punto flotante |
| Matriz singular | `Integer(0)` o `Expr == 0` | El determinante es cero |

## Casos de uso

```python
from sympy import symbols, Matrix

a, b, c, d = symbols("a b c d")

# --- caso simbolico 2x2 ---
M = Matrix([[a, b], [c, d]])
M.det()              # a*d - b*c

# --- caso numerico ---
A = Matrix([[1, 2], [3, 4]])
A.det()              # -2

# --- matriz 3x3 ---
from sympy import Matrix
B = Matrix([[1, 2, 3],
            [4, 5, 6],
            [7, 8, 9]])
B.det()              # 0   -> singular (filas linealmente dependientes)

# --- matriz con radicales ---
from sympy import sqrt
R = Matrix([[sqrt(2), 1], [1, sqrt(2)]])
R.det()              # 1   -> exacto
```

## Errores comunes

| Error | Causa | Solucion |
|-------|-------|----------|
| `ShapeError` | Matriz no cuadrada | `det()` solo aplica a matrices cuadradas |
| Resultado inesperadamente complejo | Simbolos sin supuestos (`positive`, `real`) | Define supuestos en `symbols(...)` o simplifica con `simplify()` |
| Lentitud en matrices grandes simbolicas | El algoritmo por defecto puede ser costoso | Prueba `method='berkowitz'` o reduce el tamano |

## Notas relacionadas

- [[Matrix.inv]]
- [[Matrix.rref]]
- [[Matrix]]
- [[sympy.matrices/operaciones/index | operaciones]]
