---
title: sympy.conjuntos_predefinidos — S.Reals, S.Integers y companeros
aliases: [conjuntos predefinidos, S.Reals, S.Integers, S.Naturals, S.Complexes]
tags: [sympy, api/objeto, sets]
lib: sympy
mod: sympy.sets
tipo: concepto
draft: false
---

# sympy.conjuntos_predefinidos — S.Reals, S.Integers y companeros

SymPy expone los grandes conjuntos numericos matematicos como **objetos singleton** accesibles a traves del namespace `S`. Son instancias de clases especializadas (`Reals`, `Integers`, `Naturals`, etc.) que se comportan como conjuntos SymPy: soportan pertenencia, operaciones (`union`, `intersect`, `Complement`) y se usan directamente como argumento `domain` en [[sympy.solveset]]. No se instancian con constructor propio; siempre se accede a ellos via `S.<Nombre>`.

## Firma

No hay constructor: son objetos singleton del modulo `sympy.core.singleton`.

```python
from sympy import S

S.Reals       # Reals     — todos los numeros reales (ℝ)
S.Integers    # Integers  — enteros (ℤ)
S.Naturals    # Naturals  — enteros positivos {1, 2, 3, …} (ℕ)
S.Naturals0   # Naturals0 — enteros no negativos {0, 1, 2, …} (ℕ₀)
S.Complexes   # Complexes — todos los numeros complejos (ℂ)
```

## Catalogo de conjuntos predefinidos

| Objeto | Notacion matematica | Descripcion | Ejemplos de elementos |
|--------|--------------------|--------------|-----------------------|
| `S.Reals` | ℝ | Recta real completa | `0`, `pi`, `sqrt(2)`, `-oo` a `oo` |
| `S.Integers` | ℤ | Todos los enteros | `…, -2, -1, 0, 1, 2, …` |
| `S.Naturals` | ℕ | Enteros positivos (sin cero) | `1, 2, 3, …` |
| `S.Naturals0` | ℕ₀ | Enteros no negativos (con cero) | `0, 1, 2, …` |
| `S.Complexes` | ℂ | Plano complejo completo | `1 + 2*I`, `pi`, `sqrt(-1)` |

> [!info] Convencion ℕ en SymPy
> `S.Naturals` excluye el cero (ℕ = {1, 2, 3, …}), siguiendo la convencion matematica estricta. Si se necesita incluir el cero, usar `S.Naturals0`.

## Casos de uso

### Dominio en solveset

El uso mas comun: fijar el espacio de busqueda para obtener el tipo de solucion correcto.

```python
from sympy import symbols, solveset, S
x = symbols("x")

solveset(x**2 - 4, x, domain=S.Reals)      # {-2, 2}       (FiniteSet)
solveset(x**2 + 1, x, domain=S.Reals)      # EmptySet      (sin raices reales)
solveset(x**2 + 1, x, domain=S.Complexes)  # {-I, I}       (raices complejas)
solveset(x**2 - 4, x, domain=S.Integers)   # {-2, 2}
```

### Pertenencia de un valor al conjunto

```python
from sympy import S, pi, sqrt, I
pi in S.Reals        # True
sqrt(2) in S.Reals   # True
I in S.Reals         # False
I in S.Complexes     # True
1 in S.Naturals      # True
0 in S.Naturals      # False   -> Naturals excluye el cero
0 in S.Naturals0     # True
```

### Operaciones con conjuntos predefinidos

Los conjuntos predefinidos participan en operaciones de la misma forma que [[Interval]] o [[FiniteSet]].

```python
from sympy import S, Intersection, FiniteSet, Complement
Intersection(S.Reals, FiniteSet(1, 2, 3))    # {1, 2, 3}
Complement(S.Reals, FiniteSet(0))            # Complement(Reals, {0})
S.Integers.intersect(S.Naturals0)            # Naturals0
```

### Verificar contencion entre conjuntos

```python
from sympy import S
S.Naturals.is_subset(S.Integers)    # True
S.Integers.is_subset(S.Reals)       # True
S.Reals.is_subset(S.Complexes)      # True
```

## Errores comunes

| Error | Causa | Solucion |
|-------|-------|----------|
| `S.Naturals` incluye el cero | Confusion con `S.Naturals0` | Recordar: `S.Naturals` = {1,2,3,…}; para incluir el 0 usar `S.Naturals0` |
| `x in S.Reals` devuelve expresion si `x` es `Symbol` | La pertenencia simbolica no se evalua a `True`/`False` | Usar con valores numericos concretos o trabajar con la expresion booleana |
| Intentar instanciar `Reals()` | Son singletons; no tienen constructor publico | Acceder siempre via `S.Reals`, `S.Integers`, etc. |

## Limitaciones

- Los conjuntos predefinidos son **infinitos**: no se puede iterar sobre ellos directamente.
- La pertenencia de un `Symbol` devuelve una expresion booleana; para evaluar se necesita un valor numerico concreto.
- `Complement(S.Reals, FiniteSet(0))` no simplifica a una forma mas compacta; SymPy lo deja como `Complement` sin evaluar.

## Notas relacionadas

- [[Interval]]
- [[FiniteSet]]
- [[sympy.operaciones_conjuntos]]
- [[sympy.sets/index | sympy.sets]]
- [[Tree SymPy]]
