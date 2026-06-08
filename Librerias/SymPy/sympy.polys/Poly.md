---
title: Poly — representacion densa de un polinomio
aliases:
  - Poly
  - polinomio denso
  - representacion densa
tags:
  - sympy
  - api/clase
  - polys
lib: sympy
mod: sympy.polys
tipo: clase
retorna: Poly
requiere:
  - Symbol
draft: false
---

# Poly — representacion densa de un polinomio

Envuelve una expresion polinomica en una **representacion densa y explicita**: en lugar de un arbol de operaciones como cualquier [[concepto_expr_arbol | Expr]] normal, guarda el polinomio como una **lista de coeficientes** ordenada por la variable generadora. Esa estructura hace que las operaciones polinomicas —grado, division, factorizacion, mcd— sean **mas rapidas y exactas**, y da **acceso directo** a coeficientes y grado sin tener que reconstruirlos desde la expresion. Se construye con `Poly(expr, x)` y se vuelve a una `Expr` con `.as_expr()`.

## Constructor

```python
sympy.Poly(
    expr,        # Expr | str: la expresion polinomica a representar
    *gens,       # Symbol(s): variable(s) generadora(s); se infieren si se omiten
    domain=None, # dominio de los coeficientes (ZZ, QQ, RR...); se deduce por defecto
)                # -> Poly
```

## Atributos y metodos clave

| Miembro | Tipo | Significado |
|---------|------|-------------|
| `.degree()` | metodo | Grado del polinomio (mayor exponente) |
| `.coeffs()` | metodo | Coeficientes **no nulos**, de mayor a menor grado |
| `.all_coeffs()` | metodo | **Todos** los coeficientes incluyendo ceros (densa real) |
| `.LC()` | metodo | Coeficiente lider (*leading coefficient*) |
| `.TC()` | metodo | Coeficiente independiente (*trailing coefficient*) |
| `.gens` | `tuple` | Variables generadoras `\|` p.ej. `(x,)` |
| `.as_expr()` | metodo | Devuelve la `Expr` equivalente (sale del mundo `Poly`) |
| `p + q`, `p * q`, ... | aritmetica | Operan entre `Poly` y devuelven otro `Poly` |

## Coeffs frente a all_coeffs

La diferencia clave entre ambos: `.coeffs()` omite los exponentes ausentes; `.all_coeffs()` rellena con ceros, dando la lista densa completa que define la representacion interna.

```python
from sympy import symbols, Poly
x = symbols("x")

p = Poly(x**3 + 1, x)      # faltan los terminos x**2 y x
p.coeffs()                  # [1, 1]
p.all_coeffs()              # [1, 0, 0, 1]   -> con los ceros
```

## Ejemplo

```python
from sympy import symbols, Poly
x = symbols("x")

p = Poly(x**3 + 2*x**2 - 5*x - 6, x)
p                           # Poly(x**3 + 2*x**2 - 5*x - 6, x, domain='ZZ')

p.degree()                  # 3
p.coeffs()                  # [1, 2, -5, -6]
p.LC()                      # 1    -> coeficiente lider
p.TC()                      # -6   -> coeficiente independiente
p.gens                      # (x,)

q = Poly(x**2 - 1, x)
p * q                       # Poly(x**5 + 2*x**4 - 6*x**3 - 8*x**2 + 5*x + 6, x, domain='ZZ')

p.as_expr()                 # x**3 + 2*x**2 - 5*x - 6   -> vuelve a Expr
```

> [!info] Aritmetica cerrada
> Las operaciones entre `Poly` devuelven **otro `Poly`** (mas eficiente), no una `Expr`. Incluso mezclando con una expresion suelta el resultado se mantiene como `Poly`: `Poly(x**2, x) + x` da `Poly(x**2 + x, x, domain='ZZ')`.

## Cuando usar Poly y cuando no

| Situacion | Recomendacion |
|-----------|---------------|
| Necesitas coeficientes/grado de forma directa | `Poly` (`.all_coeffs()`, `.degree()`, `.LC()`) |
| Muchas operaciones polinomicas seguidas (div, gcd, factor) | `Poly`: evita re-parsear la `Expr` cada vez |
| Trabajo simbolico general (subs, simplify, derivar, integrar) | Una `Expr` normal; `Poly` no las soporta todas |
| El objeto NO es polinomico (tiene `sin(x)`, `1/x`...) | `Expr`; `Poly` fallaria o trataria la parte rara como generador |
| Solo una operacion puntual | La funcion del submodulo directamente sobre la `Expr` |

## Relacion con las funciones del submodulo

Las funciones de [[sympy.polys/index | sympy.polys]] —`[[sympy.degree | degree]]`, `[[sympy.factor | factor]]`, `[[sympy.div | div]]`, `[[sympy.gcd | gcd]]`— aceptan **tanto una `Expr` como un `Poly`**, asi que no es obligatorio envolver para usarlas:

```python
from sympy import symbols, degree, factor, div, gcd, Poly
x = symbols("x")

degree(x**3 + 2*x**2 - 5*x - 6, x)   # 3
factor(x**3 + 2*x**2 - 5*x - 6)      # (x - 2)*(x + 1)*(x + 3)
div(x**3 - 1, x - 1)                 # (x**2 + x + 1, 0)   -> (cociente, resto)
gcd(x**2 - 1, x**2 - 3*x + 2)        # x - 1
```

`Poly` rinde cuando vas a encadenar varias de estas operaciones sobre el mismo polinomio: lo conviertes una vez y operas siempre sobre la forma densa. Pasar una `Expr` a estas funciones internamente construye un `Poly` de todos modos.

> [!regla]
> `factor(Poly(...))` devuelve **otro `Poly`**, no la expresion factorizada legible. Si quieres la forma `(x - 2)*(x + 1)*(x + 3)`, pasa la `Expr` directamente o aplica `.as_expr()` al resultado.

## Errores comunes

| Error | Causa | Solucion |
|-------|-------|----------|
| `.coeffs()` "se salta" coeficientes | Devuelve solo los **no nulos** | Usa `.all_coeffs()` para la lista densa con ceros |
| `GeneratorsNeeded` al construir | Expresion sin variable clara (`Poly(3)`) | Indica la generadora: `Poly(3, x)` |
| Resultado raro con `sin(x)`, `1/x`... | `Poly` toma lo no-polinomico como un generador mas | Verifica que la expresion sea **polinomica** antes de envolver |
| `factor(Poly(...))` no se ve factorizado | Devuelve un `Poly`, no una `Expr` | Aplica `.as_expr()` o factoriza la `Expr` directa |
| Esperabas operar `Poly` con `simplify`/`integrate` | `Poly` no implementa todo el algebra simbolica | Vuelve a `Expr` con `.as_expr()` para esas operaciones |

## Notas relacionadas

- [[sympy.degree]]
- [[sympy.factor]]
- [[sympy.div]]
- [[sympy.gcd]]
- [[concepto_expr_arbol]]
- [[sympy.polys/index | sympy.polys]]
