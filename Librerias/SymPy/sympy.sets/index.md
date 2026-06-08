---
title: sympy.sets — conjuntos simbolicos exactos
tags:
  - sympy
  - indice
draft: false
---

# sympy.sets — conjuntos simbolicos exactos

`sympy.sets` es el submodulo que convierte los conjuntos matematicos en **ciudadanos de primera clase** dentro del mundo simbolico de SymPy. Su razon de ser es directa: [[sympy.solveset]] — el resolutor moderno — no devuelve listas, devuelve **conjuntos**. Entender `sympy.sets` es entender que tipo de objeto se recibe al resolver una ecuacion y como operar con el.

El modelo mental es el de la **teoria de conjuntos aplicada a la aritmetica simbolica exacta**: un `Interval(0, 1)` no es un rango de floats sino un objeto matematico que sabe si el 0.5 pertenece a el, cual es su medida y como se intersecta con otro intervalo. Un `FiniteSet(-2, 2)` no es una lista Python; es un conjunto que soporta union, interseccion y diferencia con cualquier otro conjunto SymPy, incluyendo los infinitos (`S.Reals`, `S.Integers`).

## Ejemplo unificador

La misma ecuacion resuelta en distintos dominios produce distintos tipos de conjuntos, y con esos conjuntos se puede seguir operando:

```python
from sympy import symbols, solveset, S, Interval, Union, Intersection

x = symbols("x")

# Dominio real -> FiniteSet con las dos raices reales
sol_reales = solveset(x**2 - 4, x, domain=S.Reals)        # {-2, 2}

# Sin solucion real -> EmptySet
sin_sol = solveset(x**2 + 1, x, domain=S.Reals)           # EmptySet

# Dominio complejo -> incluye raices imaginarias
sol_complejos = solveset(x**2 + 1, x, domain=S.Complexes) # {-I, I}

# Inecuacion -> devuelve un Interval
dominio = solveset(x**2 - 1 < 0, x, domain=S.Reals)       # Interval.open(-1, 1)

# Operar con los resultados como conjuntos
sol2 = solveset(x**2 - 9, x, domain=S.Reals)              # {-3, 3}
Union(sol_reales, sol2)                                    # {-3, -2, 2, 3}
sol_reales.intersect(sol2)                                 # EmptySet

# Intersectar con un dominio
Intersection(sol_reales, S.Naturals)                       # {2}  -> solo la raiz positiva
```

## Como se relacionan

La pregunta central: **que tipo de conjunto necesito** para representar el objeto matematico en cuestion.

| Tipo | Representa | Cuando usarlo | Ejemplo tipico |
|------|------------|---------------|----------------|
| [[FiniteSet]] | Conjunto discreto finito | Soluciones de una ecuacion algebraica; resultado de `solveset` para ecuaciones con raices contables | `solveset(x**2 - 4, x)` → `{-2, 2}` |
| [[Interval]] | Rango continuo de la recta real | Dominio de una funcion; solucion de una inecuacion; restricciones de integracion | `solveset(x**2 < 1, x)` → `(-1, 1)` |
| `S.Reals` \| `S.Integers` \| … | Conjuntos numericos estandar | Argumento `domain` en `solveset`; pertenencia de un valor; restricciones globales | `solveset(eq, x, domain=S.Reals)` |
| [[sympy.operaciones_conjuntos]] | Combinaciones de conjuntos | Combinar o filtrar resultados de `solveset`; representar dominios complejos | `Union(Interval(0,1), Interval(2,3))` |

Arbol de decision para elegir el tipo:

- ¿El resultado es un numero finito de puntos? → `FiniteSet` (lo que devuelve `solveset` por defecto).
- ¿Es un rango continuo o la solucion de una inecuacion? → `Interval`.
- ¿Quieres especificar el espacio de busqueda de `solveset`? → `S.Reals`, `S.Integers`, `S.Naturals0`, `S.Complexes`.
- ¿Quieres combinar, filtrar o restar conjuntos? → `Union`, `Intersection`, `Complement` de [[sympy.operaciones_conjuntos]].

> [!info] Por que conjuntos y no listas
> `solve` devuelve una lista Python (`[-2, 2]`), comoda de indexar pero incapaz de representar infinitas soluciones (`sin(x) = 0` tiene infinitas raices). `solveset` devuelve siempre un `Set` que puede ser `FiniteSet`, `Interval`, `ImageSet` (infinito periodico) o `EmptySet`, cubriendo todos los casos de forma uniforme. La consecuencia: para indexar el resultado de `solveset` hay que convertirlo con `list(sol)`.

## Notas

- [[Interval]] — intervalo real `[a, b]`, `(a, b)`, `[a, b)` o `(a, b]`. Tiene `.measure` (longitud), `.contains()` y metodos de conjuntos. Resultado tipico de `solveset` con inecuaciones.
- [[FiniteSet]] — conjunto finito de `Expr` SymPy. Resultado tipico de `solveset` para ecuaciones con raices discretas. Soporta `union`, `intersect` y diferencia.
- [[sympy.conjuntos_predefinidos]] — singletons `S.Reals`, `S.Integers`, `S.Naturals`, `S.Naturals0`, `S.Complexes`. Se usan principalmente como argumento `domain` en `solveset` y para verificar pertenencia.
- [[sympy.operaciones_conjuntos]] — `Union`, `Intersection`, `Complement`, `SymmetricDifference`. Disponibles como funciones y como metodos de cualquier `Set`. Permiten combinar y filtrar los resultados de `solveset`.

## Notas relacionadas

- [[SymPy/index | SymPy]]
- [[Tree SymPy]]
