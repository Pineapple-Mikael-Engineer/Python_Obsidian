---
title: sympy.solvers/algebraicas — algebraicas
tags:
  - sympy
  - indice
draft: false
---

# algebraicas

Esta carpeta agrupa los resolutores de **ecuaciones de una incognita**: dada una ecuacion como `f(x) = 0`, encontrar los valores de `x` que la cumplen. SymPy ofrece cuatro funciones para esta tarea aparentemente unica, y la pregunta clave del index es **cual usar**. No son redundantes: difieren en si la solucion es exacta o numerica, en **que devuelven** (lista, conjunto, diccionario o un solo `Float`) y en para que tipo de ecuacion estan pensadas. `solve` es el caballo de batalla clasico; `solveset` su sucesor moderno basado en conjuntos; `roots` el especialista en polinomios; `nsolve` la salida numerica cuando no hay forma cerrada.

La misma ecuacion `x**2 - 4 = 0` vista por las cuatro funciones:

```python
from sympy import symbols, solve, solveset, roots, nsolve
x = symbols("x")

solve(x**2 - 4, x)         # [-2, 2]          -> lista
solveset(x**2 - 4, x)      # {-2, 2}          -> conjunto (FiniteSet)
roots(x**2 - 4, x)         # {-2: 1, 2: 1}    -> {raiz: multiplicidad}
nsolve(x**2 - 4, x, 1)     # 2.00000000000000 -> Float, la raiz cerca de x0=1
```

## Como se relacionan

La decision clave: **exacto vs numerico**, y dentro de lo exacto, **que estructura** quieres de vuelta.

| Funcion | Exacto / numerico | Devuelve | Cuando usarla |
|---------|-------------------|----------|---------------|
| [[sympy.solve]] | exacto | `list` (o `list[dict]`) | Por defecto y para casi todo; comodo, flexible, tambien sistemas |
| [[sympy.solveset]] | exacto | `Set` (`FiniteSet`, `Interval`, `ImageSet`, `EmptySet`) | Soluciones **infinitas**, inecuaciones, control explicito del `domain` |
| [[sympy.roots]] | exacto | `dict` `{raiz: multiplicidad}` | Solo **polinomios**, cuando importa la **multiplicidad** (raices dobles, triples) |
| [[sympy.nsolve]] | numerico | `Float` | **No hay forma cerrada** (trascendentes) o solo se quiere un valor cerca de un `x0` |

Arbol de decision:

- ¿La ecuacion **no** tiene solucion en forma cerrada, o solo quieres un numero cerca de un punto? -> [[sympy.nsolve]] (requiere estimacion inicial `x0`).
- ¿Es un **polinomio** y te interesa la **multiplicidad** de las raices? -> [[sympy.roots]].
- ¿Esperas **infinitas** soluciones (trigonometricas), una **inecuacion**, o quieres fijar el `domain` (reales vs complejos)? -> [[sympy.solveset]].
- En cualquier otro caso, o si dudas -> [[sympy.solve]], el resolutor clasico de proposito general.

> [!info] solve vs solveset
> Es la disyuntiva central de esta carpeta. `solve` (clasico) devuelve una **lista** finita comoda de manipular, pero no puede expresar las infinitas soluciones de `sin(x) = 0`. `solveset` (moderno) devuelve siempre un `Set` consistente que **si** representa familias infinitas (`ImageSet`) y la ausencia de solucion (`EmptySet`), a costa de tener que convertirlo a lista para indexarlo.

## Notas

- [[sympy.solve]] — el resolutor **clasico** de proposito general; devuelve una lista (o dicts). Punto de partida por defecto; del que `roots`, `solveset` y `nsolve` son especializaciones.
- [[sympy.solveset]] — el resolutor **moderno**; misma tarea que `solve` pero devolviendo conjuntos, lo que le permite expresar soluciones infinitas y el dominio de busqueda.
- [[sympy.roots]] — especialista en **polinomios**; lo que `solve` pierde (la multiplicidad de cada raiz) `roots` lo conserva en un diccionario.
- [[sympy.nsolve]] — la via **numerica**; donde los tres anteriores fallan por no existir forma cerrada, `nsolve` aproxima una raiz a partir de un `x0`.

## Notas relacionadas

- [[sympy.solvers/index | sympy.solvers]]
