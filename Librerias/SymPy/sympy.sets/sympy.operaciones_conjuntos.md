---
title: sympy.operaciones_conjuntos — Union, Intersection, Complement y SymmetricDifference
aliases: [operaciones de conjuntos, Union, Intersection, Complement, SymmetricDifference]
tags: [sympy, api/objeto, sets]
lib: sympy
mod: sympy.sets
tipo: concepto
draft: false
---

# sympy.operaciones_conjuntos — Union, Intersection, Complement y SymmetricDifference

SymPy expone las cuatro operaciones clasicas de la teoria de conjuntos como **clases de alto nivel**: `Union`, `Intersection`, `Complement` y `SymmetricDifference`. Aceptan cualquier combinacion de [[Interval]], [[FiniteSet]] y [[sympy.conjuntos_predefinidos]] como operandos y devuelven la forma mas simplificada posible — o la propia clase sin evaluar si no hay simplificacion. Estan disponibles de dos formas: como **funciones/clases** (`Union(A, B)`) o como **metodos** de cualquier `Set` (`A.union(B)`, `A.intersect(B)`). El resultado siempre es otro objeto `Set` de SymPy, que puede encadenarse con nuevas operaciones.

## Firmas

```python
from sympy import Union, Intersection, Complement, SymmetricDifference

Union(*sets)                         # A ∪ B ∪ C …
Intersection(*sets)                  # A ∩ B ∩ C …
Complement(A, B)                     # A \ B  (elementos de A que no estan en B)
SymmetricDifference(A, B)            # (A ∪ B) \ (A ∩ B) = A △ B
```

Equivalentes como metodos de cualquier `Set`:

```python
A.union(B)                           # Union(A, B)
A.intersect(B)                       # Intersection(A, B)
A - B                                # Complement(A, B)   (operador resta)
```

## Catalogo de operaciones

| Operacion | Funcion | Metodo | Simbolo |
|-----------|---------|--------|---------|
| Union | `Union(A, B)` | `A.union(B)` | A ∪ B |
| Interseccion | `Intersection(A, B)` | `A.intersect(B)` | A ∩ B |
| Complemento (diferencia) | `Complement(A, B)` | `A - B` | A \\ B |
| Diferencia simetrica | `SymmetricDifference(A, B)` | — | A △ B |

## Casos de uso

### Union de intervalos

```python
from sympy import Union, Interval
Union(Interval(0, 1), Interval(2, 3))   # Union(Interval(0, 1), Interval(2, 3))
Union(Interval(0, 2), Interval(1, 3))   # Interval(0, 3)  -> se fusionan al solaparse
```

### Interseccion: filtrar soluciones a un dominio

```python
from sympy import Intersection, S, FiniteSet
Intersection(S.Reals, FiniteSet(1, 2, 3))        # {1, 2, 3}
Intersection(S.Integers, FiniteSet(1, 2.5, 3))   # {1, 3}   -> 2.5 no es entero
Intersection(Interval(0, 2), Interval(1, 3))     # Interval(1, 2)
```

### Complemento: excluir puntos de un conjunto

```python
from sympy import Complement, S, FiniteSet, Interval
Complement(S.Reals, FiniteSet(0))          # Complement(Reals, {0})  -> reales sin el 0
Complement(S.Integers, S.Naturals)         # {..., -2, -1, 0}        -> enteros no positivos
Complement(Interval(0, 3), Interval(1, 2)) # Union(Interval.Ropen(0, 1), Interval.Lopen(2, 3))
```

### Diferencia simetrica

```python
from sympy import SymmetricDifference, FiniteSet
A = FiniteSet(1, 2, 3)
B = FiniteSet(2, 3, 4)
SymmetricDifference(A, B)   # {1, 4}  -> elementos exclusivos de cada uno
```

### Encadenar operaciones sobre resultados de solveset

La motivacion principal: `solveset` devuelve conjuntos y se pueden operar directamente.

```python
from sympy import symbols, solveset, S, Union
x = symbols("x")

sol1 = solveset(x**2 - 4, x, domain=S.Reals)   # {-2, 2}
sol2 = solveset(x**2 - 9, x, domain=S.Reals)   # {-3, 3}

Union(sol1, sol2)            # {-3, -2, 2, 3}
sol1.intersect(sol2)         # EmptySet   -> no comparten elementos
```

### Operador resta como Complement

```python
from sympy import S, FiniteSet
S.Reals - FiniteSet(0)   # Complement(Reals, {0})
```

## Errores comunes

| Error | Causa | Solucion |
|-------|-------|----------|
| `Union` no simplifica intervalos distantes | Intervalos disjuntos se dejan como `Union(...)` sin evaluar | Es el comportamiento correcto: la union no es un intervalo simple |
| `Complement(A, B)` con tipos mixtos | SymPy puede dejarlo sin evaluar | Verificar que los tipos sean compatibles; algunos complementos no tienen forma cerrada |
| Usar `A - B` esperando diferencia simetrica | `-` es `Complement`, no `SymmetricDifference` | Usar `SymmetricDifference(A, B)` explicitamente |
| `A.intersect` vs `Intersection` difieren | Son equivalentes; preferir el que sea mas legible | Ambos aceptan mas de dos argumentos: `Intersection(A, B, C)` |

## Limitaciones

- `Union` de intervalos no siempre produce un solo `Interval`; si los intervalos son disjuntos, el resultado es una `Union` sin evaluar.
- `SymmetricDifference` no tiene metodo de instancia equivalente (a diferencia de `union`/`intersect`).
- `Complement(S.Reals, FiniteSet(0))` no simplifica a una forma mas descriptiva como "reales sin cero"; se mantiene como objeto `Complement`.

## Notas relacionadas

- [[Interval]]
- [[FiniteSet]]
- [[sympy.conjuntos_predefinidos]]
- [[sympy.sets/index | sympy.sets]]
