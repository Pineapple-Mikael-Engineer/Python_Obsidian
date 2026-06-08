---
title: sympy.nsolve — raiz numerica con estimacion inicial
aliases:
  - nsolve
  - sympy.nsolve
  - raiz numerica
tags:
  - sympy
  - api/funcion
  - solvers/algebraicas
lib: sympy
mod: sympy.solvers
tipo: funcion
retorna: Float
requiere:
  - Symbol
  - mpmath
draft: false
---

# sympy.nsolve — raiz numerica con estimacion inicial

`nsolve(f, x, x0)` halla una raiz **numerica** de la ecuacion `f = 0` partiendo de una **estimacion inicial** `x0`, usando `mpmath` (precision arbitraria, metodo tipo Newton). A diferencia de [[sympy.solve]] y [[sympy.solveset]], que buscan soluciones **simbolicas exactas**, `nsolve` devuelve un `Float` aproximado. Es la herramienta adecuada cuando la ecuacion **no tiene solucion en forma cerrada** (trascendentes mezcladas, polinomios de grado alto) o cuando solo se quiere un valor numerico concreto cerca de un punto conocido.

> `nsolve` encuentra **una** raiz, la mas cercana a `x0`. La estimacion inicial es obligatoria y determina a cual converge: para varias raices, llamar con distintos `x0`.

## Firma

```python
sympy.nsolve(
    f,                   # Expr | Eq | lista: ecuacion(es) (Expr suelta -> = 0)
    symbols,             # Symbol | lista de Symbols: incognita(s)
    x0,                  # numero | lista/Matrix: estimacion inicial (obligatoria)
    dict=False,          # bool: True -> devuelve [{simbolo: valor}]
    prec=None,           # int: digitos de precision del resultado
    ...
) -> Float | Matrix
```

## Valor de retorno

| Caso | Tipo | Significado |
|------|------|-------------|
| Una incognita | `Float` | La raiz numerica mas cercana a `x0` |
| Sistema | `Matrix` | Vector columna con la solucion numerica |
| `dict=True` | `list[dict]` | `[{x: valor}]` |

```python
from sympy import symbols, nsolve, cos
x = symbols("x")
nsolve(cos(x) - x, x, 1)   # 0.739085133215161   -> Float, no exacto
```

## Formas basicas de llamada

| Objetivo | Llamada |
|----------|---------|
| Raiz cerca de `x0` | `nsolve(f, x, x0)` |
| Resolver `lhs = rhs` | `nsolve(Eq(lhs, rhs), x, x0)` |
| Sistema con vector inicial | `nsolve([f1, f2], [x, y], [x0, y0])` |
| Mayor precision | `nsolve(f, x, x0, prec=50)` |

## Parametros en detalle

### `f` (obligatorio)

La ecuacion. Una `Expr` suelta se asume `= 0`; explicitas con `Eq(lhs, rhs)`. Una **lista** plantea un sistema (requiere vector inicial).

```python
from sympy import symbols, nsolve
x = symbols("x")
nsolve(x**2 - 2, x, 1)     # 1.41421356237310   -> aprox a sqrt(2)
```

### `symbols` (obligatorio)

La(s) incognita(s). Un solo `Symbol` para una ecuacion, o una **lista** de simbolos para un sistema.

### `x0` (obligatorio)

La **estimacion inicial**, requerida. El metodo converge a la raiz mas proxima a `x0`; un mal punto inicial puede no converger o llevar a otra raiz. Para sistemas, `x0` es una **lista** (o vector) con una estimacion por incognita.

```python
from sympy import symbols, nsolve, sin
x = symbols("x")
nsolve(sin(x), x, 3)       # 3.14159265358979   -> converge a pi (la raiz cerca de 3)
nsolve(sin(x), x, 0)       # 0   -> con x0=0 converge a la raiz en 0
```

### Sistemas con vector inicial

Con una lista de ecuaciones, una lista de incognitas y un vector inicial, resuelve el sistema **no lineal** numericamente; devuelve una `Matrix` columna.

```python
from sympy import symbols, nsolve
x, y = symbols("x y")
nsolve([x**2 + y**2 - 1, x - y], [x, y], [1, 1])
# Matrix([[0.707106781186548],
#         [0.707106781186548]])
```

### `prec`

Digitos de precision del resultado; `mpmath` trabaja con precision arbitraria.

```python
from sympy import symbols, nsolve, cos
x = symbols("x")
nsolve(cos(x) - x, x, 1, prec=30)   # 0.739085133215160641655312087674
```

## Casos de uso

### Ecuacion trascendente sin forma cerrada

```python
from sympy import symbols, nsolve, exp
x = symbols("x")
nsolve(exp(x) + x - 2, x, 0)   # 0.442854401002389
```

### Punto de operacion de un sistema no lineal

```python
from sympy import symbols, nsolve
i, v = symbols("i v")
# diodo + resistencia: hallar (i, v) cerca de (0.01, 0.7)
nsolve([i - 1e-12*(exp(v/0.026) - 1), v + 1000*i - 5], [i, v], [0.004, 0.7])
```

## Errores comunes

| Error | Causa | Solucion |
|-------|-------|----------|
| No converge / `ValueError` | Estimacion inicial `x0` lejana o mala | Probar otro `x0` mas cercano a la raiz buscada |
| Falta `x0` | La estimacion inicial es **obligatoria** | Siempre pasar un punto inicial |
| Encuentra otra raiz, no la deseada | `nsolve` da la mas cercana a `x0` | Ajustar `x0` cerca de la raiz que se quiere |
| Esperar resultado exacto/simbolico | `nsolve` es **numerico** | Usar [[sympy.solve]] / [[sympy.solveset]] para exacto |
| Sistema sin vector inicial completo | Falta una estimacion por incognita | Pasar `x0` como lista del mismo tamaño que las incognitas |

## Limitaciones

- Devuelve **una** raiz numerica, no todas; para el conjunto exacto, [[sympy.solveset]]; para multiplicidades, [[sympy.roots]].
- Depende fuertemente de la **estimacion inicial**: sin un buen `x0` puede no converger.
- Resultado **aproximado** (`Float`), no simbolico: usar `solve` cuando exista solucion cerrada.

## Notas relacionadas

- [[sympy.solve]]
- [[sympy.solveset]]
- [[sympy.roots]]
- [[sympy.solvers/algebraicas/index | algebraicas]]
