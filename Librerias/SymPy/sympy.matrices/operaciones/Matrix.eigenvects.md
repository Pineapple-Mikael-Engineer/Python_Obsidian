---
title: Matrix.eigenvects — autovalores y autovectores
aliases:
  - eigenvects
  - autovectores
  - vectores propios
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
  - Matrix.eigenvals
  - Matrix.nullspace
draft: false
---

# Matrix.eigenvects — autovalores y autovectores

Calcula **autovalores y autovectores** de una [[Matrix]] cuadrada en una sola llamada. Para cada autovalor `lambda` resuelve el sistema `(M - lambda*I)v = 0` (equivalente a hallar el [[Matrix.nullspace | espacio nulo]] de `M - lambda*I`) y devuelve los vectores de base de ese espacio. Es mas completo —y mas lento— que [[Matrix.eigenvals]], que solo devuelve los autovalores.

## Firma

```python
M.eigenvects(error_when_incomplete=True, **flags)
```

| Parametro | Tipo | Descripcion |
|-----------|------|-------------|
| `error_when_incomplete` | `bool` | Si lanzar error cuando no se pueden hallar todos (default `True`) |
| `**flags` | kwargs | Pasados internamente a `eigenvals()` |

## Valor de retorno

Lista de tuplas con tres elementos cada una:

| Posicion | Tipo | Descripcion |
|----------|------|-------------|
| `[0]` | `Expr` | El autovalor exacto |
| `[1]` | `int` | Multiplicidad **algebraica** |
| `[2]` | `list[Matrix]` | Lista de autovectores (columnas) que forman base del autoespacio |

La longitud de `[2]` es la **multiplicidad geometrica** (dimension del autoespacio).

## Casos de uso

```python
from sympy import Matrix

# --- caso simple: dos autovalores distintos ---
D = Matrix([[1, 0], [0, 2]])
D.eigenvects()
# [(1, 1, [Matrix([1, 0])]), (2, 1, [Matrix([0, 1])])]
# -> autovalor 1 con mult 1, autovector [1, 0]
# -> autovalor 2 con mult 1, autovector [0, 1]

# --- autovalor doble, un solo autovector (no diagonalizable) ---
C = Matrix([[3, 1], [0, 3]])
C.eigenvects()
# [(3, 2, [Matrix([1, 0])])]
# -> mult algebraica 2, mult geometrica 1 -> no diagonalizable

# --- desempaquetar en un bucle ---
for eigenval, mult_alg, vects in D.eigenvects():
    print(eigenval, mult_alg, vects)
# 1  1  [Matrix([[1], [0]])]
# 2  1  [Matrix([[0], [1]])]
```

## Relacion entre multiplicidades

| Concepto | Definicion | En el resultado |
|----------|-----------|-----------------|
| Multiplicidad algebraica | Orden de la raiz en el polinomio caracteristico | Componente `[1]` de la tupla |
| Multiplicidad geometrica | Dimension del autoespacio (num. autovectores) | `len(tupla[2])` |

Si multiplicidad algebraica > geometrica, la matriz **no es diagonalizable** (es defectiva).

## Errores comunes

| Error | Causa | Solucion |
|-------|-------|----------|
| Calculo muy lento | Matriz grande o simbolica con polinomio de grado alto | Usa primero [[Matrix.eigenvals]] para ver los autovalores; si son conocidos, calcula autovectores a mano con `nullspace` |
| `eigenvects` da lista vacia en `[2]` | No deberia ocurrir con matrices validas; si pasa es un bug | Verifica que la matriz sea cuadrada y no tenga simbolos con supuestos contradictorios |
| Autovectores no normalizados | SymPy devuelve la base, no vectores unitarios | Normaliza con `v / v.norm()` si se necesita |

## Notas relacionadas

- [[Matrix.eigenvals]]
- [[Matrix.nullspace]]
- [[Matrix]]
- [[sympy.matrices/operaciones/index | operaciones]]
