---
title: sympy.stats — probabilidad simbolica exacta
tags:
  - sympy
  - indice
draft: false
---

# sympy.stats — probabilidad simbolica exacta

`sympy.stats` es el submodulo de [[SymPy/index | SymPy]] dedicado a la **probabilidad simbolica**: en lugar de simular o aproximar, calcula esperanzas, varianzas y probabilidades como **expresiones exactas**. La idea central es que una distribucion de probabilidad es un **objeto simbolico** — igual que `sin(x)` es un objeto SymPy, `Normal("X", mu, sigma)` es una variable aleatoria que conoce su distribucion — y las funciones `E`, `P`, `variance`, `density` aplican calculo integral exacto sobre ese objeto y devuelven una `Expr` SymPy, no un `float`.

Ejemplo unificador: definir una normal generica y consultar sus momentos.

```python
from sympy.stats import Normal, E, P, variance, density
from sympy import symbols, oo

mu, sigma = symbols("mu sigma", positive=True)
X = Normal("X", mu, sigma)

E(X)          # mu              -> exactamente el parametro
variance(X)   # sigma**2        -> exactamente el cuadrado

X0 = Normal("X", 0, 1)
P(X0 > 0)     # 1/2             -> fraccion exacta
P(X0 > 1)     # 1/2 - erf(sqrt(2)/2)/2   -> funcion de error exacta
```

El resultado de cualquiera de estas llamadas sigue siendo una expresion SymPy: se puede simplificar, sustituir, derivar respecto a un parametro o convertir a LaTeX.

## Como se relacionan

Las dos notas de esta carpeta cubren fases distintas del mismo flujo: primero se **crea** la variable aleatoria (distribucion), luego se **consulta** sobre ella (E, P, variance, density).

| Nota | Que hace | Cuando usarla |
|---|---|---|
| [[sympy.distribuciones]] | Construye v.a. simbolicas: `Normal`, `Die`, `Bernoulli`, `Exponential`, `Uniform` | Primer paso: definir la distribucion con sus parametros |
| [[sympy.E_variance_P]] | Consulta propiedades: `E`, `variance`, `P`, `density` | Segundo paso: obtener momentos, probabilidades o la PDF |

Tabla de decision por objetivo:

| Quiero obtener... | Funcion | Ejemplo de resultado |
|---|---|---|
| La esperanza de `X` | `E(X)` | `mu`, `7/2`, `1/rate` |
| La varianza de `X` | `variance(X)` | `sigma**2`, `35/12` |
| `P(X > a)` exacta | `P(X > a)` | `1/2`, `1/3`, expresion con `erf` |
| La PDF como funcion simbolica | `density(X)(t)` | expresion en `t` |
| Una muestra numerica | `sample(X)` | `Float` (no simbolico) |

## Notas

- [[sympy.distribuciones]] — las **constructoras** de variables aleatorias simbolicas (`Normal`, `Die`, `Bernoulli`, `Exponential`, `Uniform`). Punto de entrada obligatorio; sin una v.a. no hay nada que consultar.
- [[sympy.E_variance_P]] — las **funciones de consulta** (`E`, `variance`, `P`, `density`). Aplican calculo exacto sobre la v.a. y devuelven expresiones SymPy manipulables.

## Notas relacionadas

- [[SymPy/index | SymPy]]
