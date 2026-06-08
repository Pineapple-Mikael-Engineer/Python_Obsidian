---
title: sympy.matrices — algebra lineal simbolica exacta
tags:
  - sympy
  - indice
draft: false
---

# sympy.matrices

Este submodulo provee **algebra lineal simbolica exacta** sobre la clase [[Matrix]]: matrices cuyos elementos son expresiones SymPy (simbolos, racionales, radicales), no numeros de punto flotante. La consecuencia practica es que una inversa es una matriz de fracciones exactas, un autovalor puede ser un radical como `(-sqrt(33) + 5)/2`, y el espacio nulo es una base con vectores racionales. El precio es velocidad: para matrices numericas grandes, NumPy es varias ordenes de magnitud mas rapido.

El flujo tipico es: **construir** la matriz (con `Matrix(...)` o un constructor especializado) → **operar** (det, inv, rref, autosistema, nucleo) → opcionalmente **sustituir** valores con `.subs()` y evaluar con `.evalf()` o `lambdify`.

```python
from sympy import Matrix, symbols, eye

x, a, b = symbols("x a b")

# Construir una matriz simbolica 2x2
M = Matrix([[a, b], [b, a]])

# Operaciones exactas en una sola cadena
M.det()         # a**2 - b**2
M.inv()         # Matrix([[a/(a**2-b**2), -b/(a**2-b**2)], [-b/(a**2-b**2), a/(a**2-b**2)]])
M.eigenvals()   # {a - b: 1, a + b: 1}

# Sustituir y verificar
M.subs([(a, 2), (b, 1)]).det()   # 3
```

## Como se relacionan

| Pieza | Que aporta | Cuando |
|-------|------------|--------|
| [[Matrix]] | La **clase**: construir, indexar, operar con `+`, `*`, `.T`, `.subs()` | Siempre que trabajes con matrices simbolicas; es la base de todo |
| [[sympy.matrices/creacion/index \| creacion]] | **Constructores especializados**: `eye`, `zeros`, `ones`, `diag` | Inicializar patrones comunes sin escribir listas de listas; matrices identidad, diagonales, bloques |
| [[sympy.matrices/operaciones/index \| operaciones]] | **Operaciones de algebra lineal**: `det`, `inv`, `rref`, `eigenvals`, `eigenvects`, `nullspace` | Calcular propiedades de la matriz: determinante, inversa, rango, autosistema, kernel |

La division conceptual es simple: `Matrix` es el **objeto** (como se guarda y se indexa), `creacion/` son los **constructores de conveniencia** (como se genera sin teclear listas), y `operaciones/` son los **verbos del algebra lineal** (que se le puede preguntar a la matriz).

> [!info] Exactitud vs velocidad
> `sympy.matrices` es **exacto pero lento**. Para calculos numericos con matrices grandes usa NumPy (`np.linalg.det`, `np.linalg.eig`). El patron tipico: construir y analizar la estructura simbolica con SymPy → convertir con `lambdify` para evaluaciones masivas.

## Subtemas

- [[Matrix]] — la clase `Matrix`: constructor, indexacion, aritmetica matricial, `.subs()`, `.applyfunc()`, `.T`. La nota madre del submodulo.
- [[sympy.matrices/creacion/index | creacion]] — `eye`, `zeros`, `ones`, `diag`: patrones de inicializacion sin listas manuales.
- [[sympy.matrices/operaciones/index | operaciones]] — `det`, `inv`, `rref`, `eigenvals`, `eigenvects`, `nullspace`: el algebra lineal exacta sobre `Matrix`.

## Notas relacionadas

- [[SymPy/index | SymPy]]
- [[Tree SymPy]]
- [[concepto_expr_arbol]]
