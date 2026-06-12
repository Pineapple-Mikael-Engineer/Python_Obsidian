---
title: sympy.solvers/sistemas — sistemas
tags:
  - sympy
  - indice
draft: false
---

# sistemas

Esta carpeta cubre la resolucion de **sistemas de varias ecuaciones con varias incognitas**, cuya solucion es una **tupla** de valores (uno por incognita) en lugar de un solo numero. SymPy separa el problema en dos algoritmos segun la **naturaleza** de las ecuaciones: `linsolve` para sistemas **lineales** (eliminacion de Gauss, rapida y completa) y `nonlinsolve` para sistemas **no lineales** (potencias, productos de incognitas, trigonometricas). Ambas devuelven un `FiniteSet` de tuplas ordenadas segun los simbolos que les pasas; elegir bien evita tanto resultados erroneos como sobrecoste de calculo.

El mismo planteamiento, pero la linealidad decide el resolutor:

```python
from sympy import symbols, linsolve, nonlinsolve
x, y = symbols("x y")

# lineal: solo sumas de x, y por constantes
linsolve([x + y - 3, x - y - 1], x, y)     # {(2, 1)}

# no lineal: aparece x**2
nonlinsolve([x**2 - y, y - x - 2], [x, y]) # {(-1, 1), (2, 4)}
```

## Como se relacionan

| Funcion | Tipo de sistema | Algoritmo | Devuelve |
|---------|-----------------|-----------|----------|
| [[sympy.linsolve]] | **lineal** en las incognitas | eliminacion de Gauss | `FiniteSet` de tuplas (o `EmptySet`) |
| [[sympy.nonlinsolve]] | **no lineal** (potencias, productos, trascendentes) | resolucion simbolica general | `FiniteSet` de tuplas (reales y complejas) |

Como elegir:

- ¿Cada incognita aparece **solo** sumada y multiplicada por constantes (sin `x**2`, sin `x*y`, sin `sin(x)`)? -> sistema lineal -> [[sympy.linsolve]]. Acepta ademas la forma matricial `(A, b)` y la matriz aumentada `[A|b]`, y parametriza limpiamente los sistemas indeterminados (infinitas soluciones).
- ¿Hay **potencias**, **productos de incognitas** o funciones trascendentes? -> sistema no lineal -> [[sympy.nonlinsolve]], que busca el conjunto **completo** de soluciones, incluidas las complejas.

> [!tip] No malgastes nonlinsolve en lo lineal
> `linsolve` es mas rapido y predecible para el caso lineal; reserva `nonlinsolve` para cuando realmente haya no linealidad. A la inversa, usar `linsolve` en un sistema con `x**2` da un resultado **incorrecto** porque asume linealidad.

Relacion con los algebraicos: [[sympy.solve]] tambien resuelve sistemas y devuelve una **lista** de tuplas o dicts; es comodo cuando solo interesan las soluciones discretas en formato lista. `linsolve`/`nonlinsolve` se prefieren por su trato uniforme de los casos limite (`EmptySet`, parametrizacion) y por devolver siempre un conjunto. Para una solucion **numerica** de un sistema dificil que no converge en simbolico, se usa `nsolve` con un vector inicial (ver [[sympy.nsolve]]).

## Notas

- [[sympy.linsolve]] — el caso **lineal**; resuelve por Gauss y representa con un mismo lenguaje la solucion unica, las infinitas (parametrizadas) y la inconsistencia (`EmptySet`).
- [[sympy.nonlinsolve]] — el caso **no lineal**; la contraparte de `linsolve` cuando aparecen potencias o productos, devolviendo el conjunto completo de soluciones.

## Notas relacionadas

- [[sympy.solvers/index | sympy.solvers]]
