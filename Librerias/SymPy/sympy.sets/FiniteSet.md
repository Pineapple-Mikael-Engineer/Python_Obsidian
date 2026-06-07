---
title: FiniteSet — conjunto finito simbolico
aliases: [FiniteSet, conjunto finito]
tags: [sympy, api/clase, sets]
lib: sympy
mod: sympy.sets
tipo: clase
retorna: FiniteSet
requiere: [Symbol]
draft: false
---

# FiniteSet — conjunto finito simbolico

`FiniteSet(*args)` construye un **conjunto finito** cuyos elementos son expresiones SymPy (`Expr`). Es el tipo de retorno que [[sympy.solveset]] produce cuando una ecuacion tiene un numero finito de soluciones discretas: `solveset(x**2 - 4, x)` devuelve `{-2, 2}` como `FiniteSet`, no como lista Python. A diferencia del `set` nativo de Python, `FiniteSet` es un objeto SymPy que soporta operaciones matematicas exactas (union, interseccion, complemento) y puede contener simbolos, racionales y otras `Expr`.

## Firma

```python
sympy.FiniteSet(
    *args,   # elementos del conjunto (Expr, numeros, simbolos…)
) -> FiniteSet
```

## Valor de retorno

| Tipo | Forma | Significado |
|------|-------|-------------|
| `FiniteSet` | `{a, b, c}` (repr) | Conjunto con los elementos dados, sin duplicados |
| `EmptySet` | — | Si no se pasa ningun argumento: `FiniteSet()` |

## Formas basicas de llamada

| Objetivo | Llamada |
|----------|---------|
| Conjunto de literales | `FiniteSet(1, 2, 3)` |
| Conjunto con simbolos | `FiniteSet(x, y)` |
| Union con otro conjunto | `A.union(B)` |
| Interseccion | `A.intersect(B)` |
| Cardinalidad | `len(FiniteSet(1, 2, 3))` |
| Pertenencia de un valor | `1 in FiniteSet(1, 2, 3)` |

## Parametros en detalle

### `*args` — elementos del conjunto

Los duplicados se eliminan automaticamente; el orden interno es el canonico de SymPy (no necesariamente el de insercion).

```python
from sympy import FiniteSet
FiniteSet(1, 2, 3)          # {1, 2, 3}
FiniteSet(1, 1, 2)          # {1, 2}   -> sin duplicados
FiniteSet()                 # EmptySet
```

Con expresiones simbolicas:

```python
from sympy import FiniteSet, symbols
x, y = symbols("x y")
FiniteSet(x, x + 1, y)     # {x, y, x + 1}
```

## Casos de uso

### Resultado de solveset

`solveset` devuelve siempre un `Set`; para ecuaciones con soluciones discretas el resultado es un `FiniteSet`.

```python
from sympy import symbols, solveset, S
x = symbols("x")
sol = solveset(x**2 - 4, x, domain=S.Reals)  # {-2, 2}
type(sol)                                      # <class 'sympy.sets.sets.FiniteSet'>
list(sol)                                      # [-2, 2]
```

### Pertenencia y cardinalidad

```python
from sympy import FiniteSet
A = FiniteSet(1, 2, 3)
1 in A          # True
5 in A          # False
len(A)          # 3
```

### Operaciones de conjuntos

```python
from sympy import FiniteSet
A = FiniteSet(1, 2, 3)
B = FiniteSet(2, 3, 4)
A.union(B)       # {1, 2, 3, 4}
A.intersect(B)   # {2, 3}
A - B            # {1}           -> diferencia (Complement)
```

### Interseccion con un conjunto predefinido

```python
from sympy import FiniteSet, Intersection, S
Intersection(S.Reals, FiniteSet(1, 2, 3))   # {1, 2, 3}
Intersection(S.Integers, FiniteSet(1, 2.5)) # {1}
```

### Iterar sobre las soluciones

Para operar con cada solucion basta iterar; el orden interno es el de SymPy.

```python
from sympy import symbols, solveset, S
x = symbols("x")
sols = solveset(x**2 - 9, x, domain=S.Reals)  # {-3, 3}
for s in sols:
    print(s)   # -3 \n 3
```

## Errores comunes

| Error | Causa | Solucion |
|-------|-------|----------|
| `FiniteSet(1, 2)[0]` falla | `FiniteSet` no soporta indexacion | Convertir con `list(A)[0]` o iterar |
| El orden de los elementos cambia | El orden interno es el canonico de SymPy, no el de insercion | Si importa el orden, usar `sorted(list(A))` |
| `FiniteSet` vs `set` de Python | Son tipos distintos: `{1, 2}` (Python) no tiene metodos SymPy | Usar `FiniteSet(1, 2)` para operar con SymPy |
| `solveset` devuelve `EmptySet` | La ecuacion no tiene solucion en el dominio elegido | Cambiar dominio o revisar la ecuacion |

## Limitaciones

- `FiniteSet` no admite indexacion directa; hay que convertirlo a `list`.
- El orden de los elementos en la representacion y al iterar puede diferir del orden de insercion.
- Para conjuntos infinitos (rangos continuos) se usa [[Interval]]; para familias periodicas, `ImageSet`.

## Notas relacionadas

- [[Interval]]
- [[sympy.conjuntos_predefinidos]]
- [[sympy.operaciones_conjuntos]]
- [[sympy.sets/index | sympy.sets]]
- [[Tree SymPy]]
