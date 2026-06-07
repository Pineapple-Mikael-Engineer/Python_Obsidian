---
title: sympy.matrices/operaciones — algebra lineal exacta
tags:
  - sympy
  - indice
draft: false
---

# sympy.matrices/operaciones — algebra lineal exacta

Esta carpeta agrupa las operaciones de **algebra lineal simbolica exacta** sobre objetos [[Matrix]]: determinante, inversa, forma canonica, descomposicion espectral y nucleo. La palabra clave es *exacto*: SymPy no redondea ni acumula error de punto flotante; un determinante es una `Expr` algebraica, un autovalor puede ser un radical, y la base del espacio nulo son vectores con coeficientes racionales. Estas operaciones son el corazon del algebra lineal simbolica y la puerta de entrada a sistemas lineales, autosistemas y analisis estructural de matrices.

El ejemplo siguiente aplica las seis operaciones sobre la misma matriz para que la relacion entre ellas sea concreta:

```python
from sympy import Matrix

A = Matrix([[1, 2], [3, 4]])

A.det()          # -2                           -> escalar exacto
A.inv()          # Matrix([[-2, 1], [3/2, -1/2]])
A.rref()         # (Matrix([[1, 0], [0, 1]]), (0, 1))  -> identidad, rango 2
A.eigenvals()    # {-sqrt(33)/2 + 5/2: 1, sqrt(33)/2 + 5/2: 1}
A.eigenvects()   # [(lam1, 1, [v1]), (lam2, 1, [v2])]
A.nullspace()    # []   -> kernel trivial (det != 0)
```

Y sobre una matriz singular para ver el comportamiento complementario:

```python
B = Matrix([[1, 2, 3], [4, 5, 6], [7, 8, 9]])

B.det()          # 0
B.rref()         # (Matrix([[1, 0, -1], [0, 1, 2], [0, 0, 0]]), (0, 1))
B.nullspace()    # [Matrix([1, -2, 1])]
# B.inv() -> NonInvertibleMatrixError  (det = 0)
```

## Como se relacionan

La decision central: **que informacion necesitas** de la matriz.

| Metodo | Devuelve | Cuando usarlo |
|--------|----------|---------------|
| [[Matrix.det]] | `Expr` (escalar) | Verificar invertibilidad, calcular el determinante para formula de Cramer o cambio de variable |
| [[Matrix.inv]] | `Matrix` | Resolver `Ax = b` para **multiples b** a la vez, o cuando la inversa explica la estructura del sistema |
| [[Matrix.rref]] | `(Matrix, tuple)` | Resolver `Ax = b` o `Ax = 0`, calcular el rango, identificar variables libres y pivote |
| [[Matrix.eigenvals]] | `dict {val: mult}` | Solo necesitas los autovalores (rapido); diagonalizabilidad, polinomio caracteristico |
| [[Matrix.eigenvects]] | `list[(val, mult, [vects])]` | Necesitas autovalores **y** autovectores; diagonalizacion completa `P D P^{-1}` |
| [[Matrix.nullspace]] | `list[Matrix]` | Base del kernel de `M`; dimension de la solucion de `Mx = 0`; numero de variables libres |

Arbol de decision:

- ¿Solo quieres saber si la matriz es invertible? -> [[Matrix.det]] (si es cero, no es invertible).
- ¿Quieres la inversa explicita? -> [[Matrix.inv]] (lanza error si `det = 0`).
- ¿Quieres resolver un sistema o conocer el rango y las variables libres? -> [[Matrix.rref]].
- ¿Solo autovalores, sin autovectores? -> [[Matrix.eigenvals]] (mas rapido).
- ¿Autovalores **y** autovectores para diagonalizar? -> [[Matrix.eigenvects]].
- ¿Base del espacio nulo o dimension del kernel? -> [[Matrix.nullspace]].

> [!info] det y nullspace son duales
> Si `det(M) != 0`, entonces `M.nullspace()` devuelve `[]` (kernel trivial) y `M.inv()` existe.
> Si `det(M) == 0`, entonces `M.nullspace()` tiene al menos un vector no nulo y `M.inv()` falla.
> Esta dualidad es la regla de oro para verificar coherencia entre operaciones.

## Notas

- [[Matrix.det]] — determinante exacto; verifica invertibilidad y cuantifica el "volumen" de la transformacion lineal.
- [[Matrix.inv]] — inversa simbolica; requiere matriz cuadrada no singular; devuelve otra `Matrix` con entradas racionales o simbolicas.
- [[Matrix.rref]] — forma escalonada reducida; herramienta central para sistemas lineales, rango y variables libres; acepta matrices no cuadradas.
- [[Matrix.eigenvals]] — autovalores con multiplicidades en un `dict`; mas rapido que `eigenvects`; usa el polinomio caracteristico.
- [[Matrix.eigenvects]] — autovalores y autovectores juntos; base completa del autoespacio; mas lento pero mas informativo.
- [[Matrix.nullspace]] — base del kernel `{v : Mv = 0}`; complemento del rango; dimension = `n_cols - rango`.

## Notas relacionadas

- [[sympy.matrices/index | sympy.matrices]]
- [[Matrix]]
- [[Tree SymPy]]
