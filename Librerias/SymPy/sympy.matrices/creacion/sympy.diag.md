---
title: sympy.diag — diagonal o bloques diagonales
aliases:
  - diag
  - diagonal
  - bloques diagonales
tags:
  - sympy
  - api/funcion
  - matrices/creacion
lib: sympy
mod: sympy.matrices
tipo: funcion
retorna: Matrix
requiere:
  - Matrix
draft: false
---

# sympy.diag — diagonal o bloques diagonales

`diag(*args)` construye una **matriz diagonal** o de **bloques diagonales** a partir de una secuencia de escalares y/o matrices. Cada argumento ocupa un bloque en la diagonal principal: los escalares se tratan como bloques 1×1 y las matrices (de cualquier tamano) se colocan en el siguiente espacio disponible; el resto de la matriz se rellena con ceros. Es la forma idiomatica de montar matrices de bloques en SymPy sin escribir listas de listas a mano. Aparece en control (matrices de sistema de estado por bloques), mecanica (matrices de masa/rigidez) y algebra lineal (forma diagonal de una transformacion).

## Firma

```python
sympy.diag(
    *args,          # escalares y/o Matrix: los bloques en orden de la diagonal
    unpack=False,   # bool: si True y solo hay un argumento, desempaqueta la lista
) -> Matrix
```

## Valor de retorno

| Tipo | Forma | Significado |
|------|-------|-------------|
| `Matrix` | n x n (cuadrada) | Bloques en la diagonal; ceros fuera de ellos |

La dimension n es la suma de los tamanos de todos los bloques.

## Formas basicas de llamada

| Objetivo | Llamada |
|----------|---------|
| Diagonal de escalares | `diag(a, b, c)` |
| Bloque matricial + escalar | `diag(M, k)` |
| Varios bloques matriciales | `diag(A, B, C)` |
| Diagonal desde lista | `diag(*lista)` |

```python
from sympy import diag, eye, symbols
x = symbols("x")

diag(1, 2, 3)          # Matrix([[1, 0, 0], [0, 2, 0], [0, 0, 3]])
diag(x, 2)             # Matrix([[x, 0], [0, 2]])
diag(eye(2), 3)        # Matrix([[1, 0, 0], [0, 1, 0], [0, 0, 3]])
```

## Parametros en detalle

### `*args` (obligatorio)

Uno o mas **escalares** (int, `Symbol`, `Expr`) o **matrices** (`Matrix`). Se colocan en la diagonal en el orden en que se pasan. Un escalar equivale a una submatriz 1×1.

```python
from sympy import diag, Matrix, symbols
a, b = symbols("a b")

diag(a, b)                          # Matrix([[a, 0], [0, b]])
diag(Matrix([[1, 2], [3, 4]]), 5)   # Matrix([[1, 2, 0], [3, 4, 0], [0, 0, 5]])
```

Con tres matrices de distintos tamanos:

```python
from sympy import diag, eye, Matrix
A = eye(2)
B = Matrix([[5, 6], [7, 8]])
C = Matrix([[9]])
diag(A, B, C)
# Matrix([
#   [1, 0, 0, 0, 0],
#   [0, 1, 0, 0, 0],
#   [0, 0, 5, 6, 0],
#   [0, 0, 7, 8, 0],
#   [0, 0, 0, 0, 9]])
```

### `unpack` (opcional, defecto `False`)

Si `True` y se pasa un solo argumento que es una lista o matriz, la desempaqueta como si sus elementos fueran los argumentos individuales. Util cuando los bloques vienen en una lista Python.

```python
from sympy import diag
bloques = [1, 2, 3]
diag(*bloques)           # Matrix([[1, 0, 0], [0, 2, 0], [0, 0, 3]])
```

## Casos de uso

### Matriz diagonal simbolica

```python
from sympy import diag, symbols
l1, l2, l3 = symbols("lambda1 lambda2 lambda3")
D = diag(l1, l2, l3)
# Matrix([[lambda1, 0, 0], [0, lambda2, 0], [0, 0, lambda3]])
```

### Sistema de estado por bloques (control)

```python
from sympy import diag, Matrix, symbols
s = symbols("s")
A1 = Matrix([[0, 1], [-2, -3]])
A2 = Matrix([[-5]])
A_bloques = diag(A1, A2)
# Matrix([[0, 1, 0], [-2, -3, 0], [0, 0, -5]])
```

### Combinar identidad y escalar para matrices de masa

```python
from sympy import diag, eye, symbols
m, k = symbols("m k", positive=True)
M_masa = diag(m, m, k)
# Matrix([[m, 0, 0], [0, m, 0], [0, 0, k]])
```

### Construir la forma de Jordan de una matriz

```python
from sympy import diag, Matrix
bloque = Matrix([[2, 1], [0, 2]])   # bloque de Jordan 2x2, autovalor=2
J = diag(bloque, 3)
# Matrix([[2, 1, 0], [0, 2, 0], [0, 0, 3]])
```

## Errores comunes

| Error | Causa | Solucion |
|-------|-------|----------|
| Pasar una lista sin desempaquetar (`diag([1,2,3])`) | Interpreta la lista como un unico bloque 1D | Usar `diag(*lista)` o `unpack=True` |
| Esperar matriz no cuadrada | `diag` siempre produce cuadrada si todos los bloques son cuadrados | Si un bloque no es cuadrado, el resultado tampoco lo sera |
| Confundir con `.diagonalize()` | `diag` construye; `.diagonalize()` factoriza | Metodo de `Matrix`: `A.diagonalize()` → `(P, D)` |
| Olvidar que los ceros son exactos | Los ceros fuera de los bloques son `0`, no `0.0` | Comportamiento correcto en SymPy; es exacto |

## Notas relacionadas

- [[sympy.eye]]
- [[sympy.zeros]]
- [[sympy.ones]]
- [[sympy.matrices/creacion/index | creacion]]
- [[sympy.matrices/index | sympy.matrices]]
