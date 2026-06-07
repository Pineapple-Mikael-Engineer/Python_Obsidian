---
title: sympy.rsolve — resolver relaciones de recurrencia
aliases:
  - rsolve
  - resolver recurrencias
  - relaciones de recurrencia
tags:
  - sympy
  - api/funcion
  - solvers/recurrencias
lib: sympy
mod: sympy.solvers
tipo: funcion
retorna: Expr | None
requiere:
  - Symbol
  - Function
draft: false
---

# sympy.rsolve — resolver relaciones de recurrencia

Resuelve una **relacion de recurrencia** lineal y devuelve su solucion como **forma cerrada** `f(n)`, una `Expr` en funcion del indice `n`. La recurrencia se plantea como una ecuacion sobre una funcion incognita `y(n)` (una `Function` sin definir): por ejemplo `y(n) - y(n-1) - y(n-2)` describe Fibonacci. Sin condiciones iniciales devuelve la **solucion general** con constantes libres `C0, C1, ...`; con un diccionario `{y(0): ..., y(1): ...}` resuelve esas constantes y entrega la **solucion particular**. Es el analogo discreto de [[sympy.dsolve]] (que resuelve ecuaciones diferenciales).

> La recurrencia se pasa como una `Expr` igualada a `0`, igual que con `solve`: `y(n) - y(n-1) - y(n-2)` significa `y(n) - y(n-1) - y(n-2) = 0`. Tambien se admite un `Eq(lhs, rhs)`.

## Firma

```python
sympy.rsolve(
    f,             # Expr | Eq: la recurrencia en y(n), y(n-1), ... igualada a 0
    y,             # la incognita evaluada: y(n)  (Function aplicada al indice)
    init=None,     # dict | list: condiciones iniciales {y(0): a, y(1): b, ...}
) -> Expr | None
```

## Valor de retorno

| Caso | Tipo | Significado |
|------|------|-------------|
| Sin `init` | `Expr` | Solucion general con constantes `C0, C1, ...` |
| Con `init` | `Expr` | Solucion particular (constantes ya resueltas) |
| Sin forma cerrada | `None` | SymPy no halla solucion hipergeometrica |

```python
sol = rsolve(eq, y(n))                 # Expr con C0, C1
sol = rsolve(eq, y(n), {y(0): 0, y(1): 1})   # Expr ya determinada
```

## Formas basicas de llamada

| Objetivo | Llamada |
|----------|---------|
| Solucion general | `rsolve(y(n) - 2*y(n-1), y(n))` |
| Con una condicion inicial | `rsolve(y(n) - 2*y(n-1), y(n), {y(0): 1})` |
| Fibonacci (orden 2) | `rsolve(y(n) - y(n-1) - y(n-2), y(n))` |
| Fibonacci con condiciones | `rsolve(y(n) - y(n-1) - y(n-2), y(n), {y(0): 0, y(1): 1})` |
| Recurrencia no homogenea | `rsolve(y(n) - y(n-1) - 1, y(n))` |

## Parametros en detalle

### `f` (obligatorio)

La recurrencia como `Expr` (asumida `= 0`) o `Eq`. Se escribe con la incognita en distintos indices: `y(n)`, `y(n-1)`, `y(n-2)`. Los coeficientes pueden ser constantes (recurrencia lineal con **coeficientes constantes**) o depender de `n` (coeficientes variables).

```python
from sympy import Function, symbols, rsolve

y = Function("y")
n = symbols("n", integer=True)

# Recurrencia geometrica: y(n) = 2*y(n-1)
rsolve(y(n) - 2*y(n-1), y(n))     # 2**n*C0   -> solucion general
```

### `y` (obligatorio)

La incognita **aplicada al indice**, `y(n)`, no la `Function` `y` suelta. Define cual es el termino "actual" de la recurrencia.

> En SymPy 1.14 conviene plantear la recurrencia con indices **hacia atras** (`y(n)`, `y(n-1)`, `y(n-2)`) y pasar `y(n)`. La forma adelantada `y(n+2) - y(n+1) - 6*y(n)` con `y(n+2)` puede fallar con `PolynomialError`.

### `init`

Diccionario de **condiciones iniciales** `{y(0): a0, y(1): a1, ...}`. Hacen falta tantas como el **orden** de la recurrencia (orden 2 -> dos condiciones) para fijar todas las constantes `Ck`.

```python
from sympy import Function, symbols, rsolve

y = Function("y")
n = symbols("n", integer=True)

eq = y(n) - 2*y(n-1)
rsolve(eq, y(n))                  # 2**n*C0     -> general
rsolve(eq, y(n), {y(0): 1})       # 2**n        -> particular (C0 = 1)
```

## Casos de uso

### Fibonacci: de la recurrencia a la forma cerrada (Binet)

```python
from sympy import Function, symbols, rsolve

y = Function("y")
n = symbols("n", integer=True)

eq = y(n) - y(n-1) - y(n-2)       # F(n) = F(n-1) + F(n-2)

# Solucion general: combinacion de las raices del polinomio caracteristico
rsolve(eq, y(n))
# C0*(1/2 - sqrt(5)/2)**n + C1*(1/2 + sqrt(5)/2)**n

# Con F(0)=0, F(1)=1 -> formula de Binet
fib = rsolve(eq, y(n), {y(0): 0, y(1): 1})
# -sqrt(5)*(1/2 - sqrt(5)/2)**n/5 + sqrt(5)*(1/2 + sqrt(5)/2)**n/5

# Verificacion: el termino 10 es 55
fib.subs(n, 10).simplify()        # 55
```

### Recurrencia lineal de orden 2 con coeficientes constantes

```python
from sympy import Function, symbols, rsolve

y = Function("y")
n = symbols("n", integer=True)

# y(n) = y(n-1) + 6*y(n-2)  ->  raices del caracteristico: -2 y 3
eq = y(n) - y(n-1) - 6*y(n-2)

rsolve(eq, y(n))                          # (-2)**n*C0 + 3**n*C1
rsolve(eq, y(n), {y(0): 1, y(1): 2})      # (-2)**n/5 + 4*3**n/5
```

### Recurrencia no homogenea

```python
from sympy import Function, symbols, rsolve

y = Function("y")
n = symbols("n", integer=True)

# y(n) = y(n-1) + 1  ->  contador
eq = y(n) - y(n-1) - 1
rsolve(eq, y(n))                  # C0 + n
rsolve(eq, y(n), {y(0): 0})       # n
```

### Coeficientes variables: el factorial

```python
from sympy import Function, symbols, rsolve

y = Function("y")
n = symbols("n", integer=True)

# y(n) = n*y(n-1)  ->  definicion del factorial
eq = y(n) - n*y(n-1)
rsolve(eq, y(n))                  # C0*factorial(n)
rsolve(eq, y(n), {y(0): 1})       # factorial(n)
```

## Errores comunes

| Error | Causa | Solucion |
|-------|-------|----------|
| `PolynomialError: generator must be a Symbol` | Recurrencia planteada con indice adelantado `y(n+2)` | Usar forma hacia atras `y(n)`, `y(n-1)`, `y(n-2)` |
| `ValueError: 'y(n + k)' expected` | La ecuacion no es lineal en `y` (p.ej. `y(n)**2`) | `rsolve` solo resuelve recurrencias **lineales** |
| Devuelve `None` | No existe solucion hipergeometrica cerrada | Esperado; probar otra formulacion o resolver numericamente |
| Quedan constantes `C0, C1` sin querer | No se pasaron condiciones iniciales | Aportar `init` con tantas condiciones como el orden |
| `n` tratado como real continuo | Indice sin supuesto entero | Declararlo `symbols("n", integer=True)` |

## Notas relacionadas

- [[sympy.dsolve]]
- [[Sum]]
- [[sympy.solvers/recurrencias/index | recurrencias]]
- [[Tree SymPy]]
