---
title: Matrix.eigenvals — autovalores con multiplicidades
aliases:
  - eigenvals
  - autovalores
  - valores propios
tags:
  - sympy
  - api/metodo
  - matrices/operaciones
lib: sympy
mod: sympy.matrices
tipo: metodo
obj: Matrix
retorna: dict
requiere:
  - Matrix
  - Matrix.det
draft: false
---

# Matrix.eigenvals — autovalores con multiplicidades

Calcula los **autovalores** (valores propios) de una [[Matrix]] cuadrada resolviendo el polinomio caracteristico `det(M - lambda*I) = 0`. Devuelve un diccionario `{autovalor: multiplicidad_algebraica}` con resultados **exactos**: enteros, racionales, radicales o expresiones simbolicas. Es mas rapido que [[Matrix.eigenvects]] porque no calcula los autovectores asociados.

## Firma

```python
M.eigenvals(error_when_incomplete=True, **flags)
```

| Parametro | Tipo | Descripcion |
|-----------|------|-------------|
| `error_when_incomplete` | `bool` | Si lanzar error cuando no se pueden hallar todos los autovalores (default `True`) |
| `**flags` | kwargs | Opciones pasadas internamente a `roots()` (p. ej. `multiple=True`) |

## Valor de retorno

| Tipo | Estructura | Descripcion |
|------|-----------|-------------|
| `dict` | `{Expr: int}` | Cada clave es un autovalor exacto; el valor es su multiplicidad algebraica |

Si la multiplicidad es 1 para todos, la matriz es **no defectiva** (diagonalizable sobre C).

## Casos de uso

```python
from sympy import Matrix

# --- matriz diagonal (autovalores triviales) ---
D = Matrix([[1, 0], [0, 2]])
D.eigenvals()     # {1: 1, 2: 1}   -> dos autovalores simples

# --- autovalor doble (matriz no diagonalizable) ---
C = Matrix([[3, 1], [0, 3]])
C.eigenvals()     # {3: 2}   -> autovalor 3 con multiplicidad algebraica 2

# --- matriz simbolica ---
from sympy import symbols
a = symbols("a")
S = Matrix([[a, 0], [0, a + 1]])
S.eigenvals()     # {a: 1, a + 1: 1}

# --- comprobar si es diagonalizable (multiplicidades todas = 1) ---
M = Matrix([[1, 2], [3, 4]])
ev = M.eigenvals()
# {-sqrt(33)/2 + 5/2: 1, sqrt(33)/2 + 5/2: 1}
# multiplicidades todas 1 -> diagonalizable sobre R (ambos positivos)
```

## Errores comunes

| Error | Causa | Solucion |
|-------|-------|----------|
| `MatrixError` o resultado incompleto | Polinomio caracteristico de grado alto sin forma cerrada | Usa `error_when_incomplete=False` y acepta los que SymPy puede hallar |
| Autovalores como expresiones largas | Matriz simbolica con polinomio de grado > 4 | Evalua numericamente con `.evalf()` sobre cada clave del dict |
| `ShapeError` | Matriz no cuadrada | `eigenvals()` solo aplica a matrices cuadradas |

## Notas relacionadas

- [[Matrix.eigenvects]]
- [[Matrix.det]]
- [[Matrix]]
- [[sympy.matrices/operaciones/index | operaciones]]
