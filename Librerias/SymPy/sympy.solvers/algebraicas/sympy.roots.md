---
title: sympy.roots — raices de un polinomio con su multiplicidad
aliases:
  - roots
  - sympy.roots
  - raices con multiplicidad
tags:
  - sympy
  - api/funcion
  - solvers/algebraicas
lib: sympy
mod: sympy.solvers
tipo: funcion
retorna: dict
draft: false
---

# sympy.roots — raices de un polinomio con su multiplicidad

`roots(poly, x)` calcula las raices de un **polinomio** y devuelve un **diccionario** `{raiz: multiplicidad}`, indicando cuantas veces se repite cada raiz. Es la herramienta indicada cuando importa la **multiplicidad** (raices dobles, triples…), informacion que [[sympy.solve]] pierde al devolver una lista plana. Solo trabaja con **polinomios**: para ecuaciones generales (trigonometricas, exponenciales…) hay que usar `solve` o [[sympy.solveset]].

> Diferencia con `solve`: `solve(x**2, x)` da `[0]` (no dice que es doble), mientras que `roots(x**2, x)` da `{0: 2}`, explicitando la multiplicidad.

## Firma

```python
sympy.roots(
    f,                   # Expr | Poly: el polinomio
    *gens,               # Symbol(s): variable(s) del polinomio
    cubics=True,         # bool: usar formulas para cubicas
    quartics=True,       # bool: usar formulas para cuarticas
    multiple=False,      # bool: True -> devuelve una lista con repeticiones, no el dict
    ...
) -> dict
```

## Valor de retorno

| Caso | Tipo | Significado |
|------|------|-------------|
| Por defecto | `dict` | `{raiz: multiplicidad}`; la suma de multiplicidades = grado |
| `multiple=True` | `list` | Lista plana con cada raiz repetida segun su multiplicidad |

```python
from sympy import symbols, roots
x = symbols("x")
roots(x**2 - 4, x)         # {-2: 1, 2: 1}   -> dos raices simples
```

## Formas basicas de llamada

| Objetivo | Llamada |
|----------|---------|
| Raices con multiplicidad | `roots(poly, x)` |
| Lista plana (como `solve`) | `roots(poly, x, multiple=True)` |

## Parametros en detalle

### `f` (obligatorio)

El polinomio, como `Expr` o como `Poly`. Si no es polinomico, `roots` no es la funcion adecuada.

```python
from sympy import symbols, roots
x = symbols("x")
roots(x**2 - 4, x)         # {-2: 1, 2: 1}
```

### Raices repetidas (multiplicidad > 1)

El valor del diccionario es la multiplicidad. Aqui es donde `roots` aporta frente a `solve`.

```python
from sympy import symbols, roots
x = symbols("x")
roots((x - 1)**2 * (x - 2), x)   # {1: 2, 2: 1}   -> 1 es raiz doble, 2 simple
roots(x**3 - 3*x**2 + 3*x - 1, x)  # {1: 3}       -> (x-1)**3
```

### Raices complejas

Incluye las raices **complejas** (con `I`), tambien con su multiplicidad.

```python
from sympy import symbols, roots
x = symbols("x")
roots(x**2 + 1, x)         # {-I: 1, I: 1}
```

### `multiple=True`

Devuelve una **lista** con cada raiz repetida tantas veces como su multiplicidad, util para iterar sin mirar el diccionario.

```python
from sympy import symbols, roots
x = symbols("x")
roots((x - 1)**2 * (x - 2), x, multiple=True)   # [1, 1, 2]
```

## Casos de uso

### Verificar que un sistema tiene polos repetidos

```python
from sympy import symbols, roots
s = symbols("s")
# polinomio caracteristico con raiz doble en s = -1
roots(s**2 + 2*s + 1, s)   # {-1: 2}   -> polo doble
```

### Sumar multiplicidades = grado del polinomio

```python
from sympy import symbols, roots
x = symbols("x")
r = roots(x**4 - 1, x)     # {-1: 1, 1: 1, -I: 1, I: 1}
sum(r.values())            # 4   -> coincide con el grado
```

## Errores comunes

| Error | Causa | Solucion |
|-------|-------|----------|
| Usar `roots` en ecuacion no polinomica | Solo soporta polinomios | Usar [[sympy.solve]] o [[sympy.solveset]] |
| Esperar una lista | Devuelve un `dict` por defecto | Usar `multiple=True`, o `list(r.keys())` para solo las raices |
| Diccionario vacio | El polinomio es de grado alto sin formula radical cerrada | Usar `solve`/`solveset`, o raices numericas con `nroots` / [[sympy.nsolve]] |
| Ignorar la multiplicidad | Leer solo las claves | El **valor** del dict es la multiplicidad; usarlo |

## Limitaciones

- Solo **polinomios**; para ecuaciones generales, [[sympy.solve]] o [[sympy.solveset]].
- Para grados altos puede no haber solucion radical cerrada y devolver un diccionario incompleto o vacio; en ese caso conviene una raiz **numerica** ([[sympy.nsolve]] o `Poly.nroots`).
- Da raices **exactas**: si solo se quieren valores numericos, usar el modo numerico.

## Notas relacionadas

- [[sympy.solve]]
- [[sympy.solveset]]
- [[sympy.nsolve]]
- [[sympy.solvers/algebraicas/index | algebraicas]]
