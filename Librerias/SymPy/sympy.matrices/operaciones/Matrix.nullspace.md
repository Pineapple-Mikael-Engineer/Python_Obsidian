---
title: Matrix.nullspace — espacio nulo (kernel) de la matriz
aliases:
  - nullspace
  - espacio nulo
  - kernel
tags:
  - sympy
  - api/metodo
  - matrices/operaciones
lib: sympy
mod: sympy.matrices
tipo: metodo
obj: Matrix
retorna: list
requiere:
  - Matrix
  - Matrix.rref
draft: false
---

# Matrix.nullspace — espacio nulo (kernel) de la matriz

Calcula una **base del espacio nulo** (kernel) de una [[Matrix]]: el conjunto de todos los vectores `v` tales que `M @ v = 0`. Internamente aplica [[Matrix.rref | RREF]] para identificar las variables libres y expresa cada una como un vector de la base. Acepta matrices de cualquier forma (no solo cuadradas). Si la base resultante esta vacia, el unico vector del kernel es el vector cero.

## Firma

```python
M.nullspace(simplify=False, iszerofunc=<lambda>)
```

| Parametro | Tipo | Descripcion |
|-----------|------|-------------|
| `simplify` | `bool \| callable` | Si aplicar simplificacion durante la eliminacion |
| `iszerofunc` | `callable` | Funcion para decidir si una expresion es cero |

## Valor de retorno

| Caso | Retorno | Interpretacion |
|------|---------|----------------|
| Kernel no trivial | `list[Matrix]` (una o mas columnas) | Base del espacio nulo; cada `Matrix` es un vector columna |
| Kernel trivial (solo `v = 0`) | `[]` (lista vacia) | La matriz tiene rango lleno (todas las columnas son pivote) |

La **dimension del kernel** = `len(M.nullspace())` = numero de columnas libres = `n_cols - rango`.

## Casos de uso

```python
from sympy import Matrix

# --- matriz 3x3 singular: kernel de dimension 1 ---
B = Matrix([[1, 2, 3],
            [4, 5, 6],
            [7, 8, 9]])
B.nullspace()
# [Matrix([1, -2, 1])]   -> un solo vector base; rango = 2

# --- verificar que efectivamente da cero ---
ns = B.nullspace()
B * ns[0]
# Matrix([[0], [0], [0]])   -> confirmado

# --- matriz identidad: kernel trivial ---
from sympy import eye
eye(3).nullspace()
# []   -> kernel = {0}, rango lleno

# --- sistema Ax = 0 con dos variables libres ---
A = Matrix([[1, 2, 3, 4],
            [2, 4, 6, 8]])   # fila 2 = 2 * fila 1
A.nullspace()
# tres vectores base -> kernel de dimension 3 (n_cols=4, rango=1)
```

## Relacion con rref y rango

```python
# El rango se lee de los pivotes de rref; la dimension del kernel lo complementa
B = Matrix([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
_, pivs = B.rref()
rango   = len(pivs)            # 2
dim_ker = B.cols - rango       # 3 - 2 = 1   -> coincide con len(B.nullspace())
```

## Errores comunes

| Error | Causa | Solucion |
|-------|-------|----------|
| `nullspace()` da lista vacia inesperadamente | Expresiones simbolicas no identificadas como cero | Pasa `simplify=True` o añade supuestos a los simbolos |
| Vectores de base no simplificados | SymPy devuelve la forma directa sin factorizar | Aplica `simplify()` a cada vector si se necesita forma compacta |
| Confusion con `columnspace()` | `nullspace` es el kernel (Mv=0); `columnspace` es el espacio imagen | Usar el metodo correcto segun el problema |

## Notas relacionadas

- [[Matrix.rref]]
- [[Matrix.eigenvects]]
- [[Matrix]]
- [[sympy.matrices/operaciones/index | operaciones]]
