---
title: Matrix.inv — inversa simbolica exacta
aliases:
  - inv
  - inversa de matriz
tags:
  - sympy
  - api/metodo
  - matrices/operaciones
lib: sympy
mod: sympy.matrices
tipo: metodo
obj: Matrix
retorna: Matrix
requiere:
  - Matrix
  - Matrix.det
draft: false
---

# Matrix.inv — inversa simbolica exacta

Calcula la inversa de una [[Matrix]] de forma **exacta y simbolica**. Requiere que la matriz sea cuadrada y no singular (determinante distinto de cero). Por defecto usa eliminacion de Gauss-Jordan (`'GE'`), que es eficiente para la mayoria de casos; los metodos `'ADJ'` (por adjunta) y `'LU'` estan disponibles cuando se necesita controlar el algoritmo.

## Firma

```python
M.inv(method=None)
```

| Parametro | Tipo | Descripcion |
|-----------|------|-------------|
| `method` | `str \| None` | Algoritmo de inversion. `None` equivale a `'GE'` |

| Valor de `method` | Algoritmo | Cuando usarlo |
|-------------------|-----------|---------------|
| `None` / `'GE'` | Gauss-Jordan | Caso general; default recomendado |
| `'ADJ'` | Formula de la adjunta (cofactores) | Matrices muy pequenas (2×2, 3×3) o cuando se quiere la formula explicita |
| `'LU'` | Descomposicion LU | Matrices numericas grandes o cuando LU ya esta disponible |

## Valor de retorno

| Entrada | Retorno |
|---------|---------|
| Matriz invertible n×n | `Matrix` n×n con entradas exactas (`Rational`, `Expr`) |
| Matriz singular | Lanza `NonInvertibleMatrixError` |

## Casos de uso

```python
from sympy import symbols, Matrix

# --- caso numerico ---
A = Matrix([[1, 2], [3, 4]])
A.inv()
# Matrix([[-2, 1], [3/2, -1/2]])   -> Rational exacto, no float

# --- verificacion: A * A^{-1} = I ---
A * A.inv()
# Matrix([[1, 0], [0, 1]])

# --- caso simbolico ---
a, b, c, d = symbols("a b c d")
M = Matrix([[a, b], [c, d]])
M.inv()
# Matrix([[d/(a*d - b*c), -b/(a*d - b*c)], [-c/(a*d - b*c), a/(a*d - b*c)]])

# --- metodo por adjunta ---
A.inv(method='ADJ')
# Matrix([[-2, 1], [3/2, -1/2]])   -> mismo resultado, diferente camino
```

## Errores comunes

| Error | Causa | Solucion |
|-------|-------|----------|
| `NonInvertibleMatrixError` | La matriz es singular (`det = 0`) | Verifica con [[Matrix.det]] antes de invertir |
| `ShapeError` | Matriz no cuadrada | `inv()` solo aplica a matrices cuadradas |
| Resultado con `zoo` o `nan` | Simbolo en denominador que puede ser cero | Añade supuestos `nonzero=True` o evalua con valores concretos |
| Fracciones no simplificadas | La expresion es valida pero no compacta | Aplica `simplify()` al resultado si se necesita legibilidad |

## Notas relacionadas

- [[Matrix.det]]
- [[Matrix.rref]]
- [[Matrix]]
- [[sympy.matrices/operaciones/index | operaciones]]
