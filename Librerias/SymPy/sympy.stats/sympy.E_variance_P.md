---
title: sympy.E_variance_P — consultar variables aleatorias simbolicas
aliases:
  - E
  - variance
  - P
  - density
  - valor esperado
tags:
  - sympy
  - api/concepto
  - stats
lib: sympy
mod: sympy.stats
tipo: concepto
draft: false
---

# sympy.E_variance_P — consultar variables aleatorias simbolicas

`E`, `variance`, `P` y `density` son las **funciones de consulta** de `sympy.stats`: reciben una variable aleatoria simbolica (creada con [[sympy.distribuciones]]) y devuelven una **expresion SymPy exacta**, no un numero flotante. `E(X)` es la esperanza matematica; `variance(X)` es la varianza; `P(cond)` es la probabilidad de una condicion; `density(X)(t)` es la funcion de densidad evaluada en el simbolo `t`. El resultado de cualquiera de estas funciones vive en el mundo simbolico y puede seguir siendo manipulado con `simplify`, `subs`, `diff` o `latex`.

## Como funciona

La idea central: las funciones de consulta **no numeran**, **calculan exactamente**. Cuando los parametros son simbolos, el resultado es una expresion en esos mismos simbolos. Cuando son numeros concretos, el resultado puede ser una fraccion exacta o una expresion con funciones especiales (como `erf`).

```python
from sympy.stats import Normal, Die, E, P, variance, density
from sympy import symbols, oo

mu, sigma = symbols("mu sigma", positive=True)
X = Normal("X", mu, sigma)

E(X)          # mu
variance(X)   # sigma**2

X0 = Normal("X", 0, 1)
P(X0 > 0)     # 1/2

D = Die("D", 6)
E(D)          # 7/2
P(D > 4)      # 1/3
```

## Formas de llamada

| Funcion | Argumentos | Devuelve | Ejemplo |
|---|---|---|---|
| `E(X)` | v.a. `X` | `Expr` (esperanza) | `E(Normal("X", mu, sigma))` → `mu` |
| `E(X, cond)` | v.a. + condicion | `Expr` (esperanza condicional) | `E(X, X > 0)` |
| `variance(X)` | v.a. `X` | `Expr` (varianza) | `variance(Normal("X", mu, sigma))` → `sigma**2` |
| `P(cond)` | condicion booleana | `Expr` (probabilidad) | `P(X0 > 0)` → `1/2` |
| `P(cond, cond2)` | condicion + condicion | `Expr` (prob. condicional) | `P(X0 > 1, X0 > 0)` |
| `density(X)(t)` | v.a. + simbolo `t` | `Expr` (densidad en `t`) | ver abajo |

## Parametros en detalle

### `E(X)` — esperanza

Devuelve la esperanza matematica de `X`. Si `X` tiene parametros simbolicos, el resultado es exactamente esos parametros (por definicion de la distribucion). Acepta un segundo argumento `cond` para esperanza condicional.

```python
from sympy.stats import Normal, Exponential, E
from sympy import symbols

mu, sigma = symbols("mu sigma", positive=True)
rate = symbols("rate", positive=True)

E(Normal("X", mu, sigma))         # mu
E(Exponential("T", rate))         # 1/rate
```

### `variance(X)` — varianza

Devuelve la varianza de `X`. Equivale a `E(X**2) - E(X)**2`, pero SymPy la calcula directamente desde la distribucion.

```python
from sympy.stats import Normal, Die, variance
from sympy import symbols, Rational

sigma = symbols("sigma", positive=True)

variance(Normal("X", 0, sigma))   # sigma**2
variance(Die("D", 6))             # 35/12
```

### `P(cond)` — probabilidad

Recibe una **condicion booleana** sobre una v.a. y devuelve su probabilidad como `Expr`. Para distribuciones continuas el resultado puede contener `erf` o `erfc`.

```python
from sympy.stats import Normal, Die, P
from sympy import symbols

X0 = Normal("X", 0, 1)
P(X0 > 0)          # 1/2
P(X0 > 1)          # 1/2 - erf(sqrt(2)/2)/2
P(X0 > 1, X0 > 0)  # probabilidad condicional P(X>1 | X>0)

D = Die("D", 6)
P(D > 4)            # 1/3
P(D > 3)            # 1/2
```

### `density(X)(t)` — funcion de densidad

`density(X)` devuelve un objeto **callable**; al evaluarlo en un simbolo `t` se obtiene la expresion de la PDF en ese punto.

```python
from sympy.stats import Normal, density
from sympy import symbols

t = symbols("t")
X0 = Normal("X", 0, 1)
density(X0)(t)    # sqrt(2)*exp(-t**2/2)/(2*sqrt(pi))
```

## Casos de uso

### Demostrar propiedades de distribuciones con parametros genericos

```python
from sympy.stats import Exponential, E, variance
from sympy import symbols, simplify

rate = symbols("rate", positive=True)
T = Exponential("T", rate)

simplify(variance(T) - E(T)**2)   # 0  -> varianza = 1/rate^2 = (E[T])^2
```

### Calcular probabilidades exactas con fracciones

```python
from sympy.stats import Die, P

D = Die("D", 6)
P(D > 4)      # 1/3   (caras 5 y 6)
P(D > 3)      # 1/2   (caras 4, 5 y 6)
```

### Obtener la densidad para integrar o graficar

```python
from sympy.stats import Normal, density
from sympy import symbols, integrate, oo

t = symbols("t")
X0 = Normal("X", 0, 1)
f = density(X0)(t)
integrate(f, (t, -oo, oo))   # 1  -> confirma que es una densidad valida
```

## Errores comunes

| Error | Causa | Solucion |
|---|---|---|
| `E(X)` devuelve `Integral(...)` sin evaluar | SymPy no pudo integrar la distribucion | Usar `.doit()` o `simplify` sobre el resultado |
| `P(X > a)` con `a` sin supuestos devuelve expresion con `Abs` | SymPy no sabe si `a > 0` | Declarar `a = symbols("a", real=True)` o dar un valor concreto |
| `density(X)` olvidar llamarlo con `(t)` | `density(X)` es un objeto, no una expresion | Escribir siempre `density(X)(t)` con el simbolo destino |
| Confundir `variance` con desviacion estandar | `variance(X)` es `sigma**2`, no `sigma` | Para la desviacion: `sqrt(variance(X))` |

## Limitaciones

- Para distribuciones con integrales sin forma cerrada (algunas mixtas o truncadas), `E` y `P` pueden devolver integrales sin evaluar. En ese caso `nsolve` o SciPy son alternativas numericas.
- `density` solo aplica a v.a. continuas; para discretas usar `density` produce una `DiracDelta` o directamente no aplica — usar `P(X.eq(k))` para probabilidades puntuales.

## Notas relacionadas

- [[sympy.distribuciones]]
- [[sympy.stats/index | sympy.stats]]
- [[Tree SymPy]]
