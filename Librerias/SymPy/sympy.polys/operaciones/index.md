---
title: sympy.polys/operaciones — operaciones
tags:
  - sympy
  - indice
draft: false
---

# operaciones

Esta carpeta reune las **operaciones aritmeticas y de raices sobre polinomios**: dividir, hallar factores comunes y multiplos, medir el grado y extraer las raices reales exactas. Son las herramientas de "algebra de polinomios" del dia a dia, todas top-level (no hace falta construir un `Poly` a mano: aceptan expresiones directamente). El hilo que las une es que casi todas se apoyan, directa o indirectamente, en la **division con resto**: el algoritmo de Euclides polinomico que implementa [[sympy.div]] es la base de la que nacen el maximo comun divisor y el minimo comun multiplo.

Un ejemplo unificador sobre dos polinomios `f` y `g`:

```python
from sympy import symbols, div, gcd, lcm, degree, real_roots
x = symbols("x")
f = x**2 - 1          # (x-1)(x+1)
g = x**2 - 3*x + 2    # (x-1)(x-2)

div(f, g)        # (1, 3*x - 3)              -> cociente y resto
gcd(f, g)        # x - 1                     -> factor comun
lcm(f, g)        # x**3 - 2*x**2 - x + 2     -> menor multiplo comun
degree(f, x)     # 2                         -> consulta de grado
real_roots(f)    # [-1, 1]                   -> raices reales exactas
```

## Como se relacionan

El modelo mental: `div` es el motor, `gcd`/`lcm` son la pareja que se construye sobre el, `degree` es una consulta de apoyo y `real_roots` es la salida a las raices.

| Funcion | Papel | Devuelve | Cuando usarla |
|---------|-------|----------|---------------|
| [[sympy.div]] | **Base aritmetica** (division con resto) | `tuple` `(cociente, resto)` | Dividir polinomios, comprobar divisibilidad (resto 0); cimiento de `gcd`/`lcm` |
| [[sympy.gcd]] | Factor **comun** (pareja con `lcm`) | `Expr` | Simplificar fracciones, hallar el factor compartido, comprobar coprimalidad |
| [[sympy.lcm]] | Multiplo **comun** (pareja con `gcd`) | `Expr` | Denominador comun de fracciones; ligado a `gcd` por `gcd*lcm = f*g` |
| [[sympy.degree]] | **Consulta** de estructura | `Integer` | Saber el grado: cuantas raices esperar, validar un cociente |
| [[sympy.real_roots]] | **Raices** reales exactas | `list` | Raices reales (con multiplicidad), de cualquier grado, exactas |

Como elegir:

- ¿Necesitas **dividir** o saber si un polinomio divide a otro? -> [[sympy.div]] (resto 0 = divide).
- ¿Buscas el **factor comun** o simplificar una fraccion de polinomios? -> [[sympy.gcd]].
- ¿Buscas el **denominador comun** o el menor multiplo comun? -> [[sympy.lcm]].
- ¿Solo quieres el **grado**? -> [[sympy.degree]].
- ¿Quieres las **raices reales** exactas (con su multiplicidad)? -> [[sympy.real_roots]].

> [!info] div como cimiento
> `gcd` y `lcm` no son magia: ambos se calculan mediante divisiones sucesivas (Euclides). Entender [[sympy.div]] aclara por que `gcd`/`lcm` se normalizan monicos y por que `gcd*lcm = f*g`.

## Notas

- [[sympy.div]] — la **division con resto**, motor de toda la aritmetica de esta carpeta; sobre ella se construyen `gcd` y `lcm`.
- [[sympy.gcd]] — el **factor comun**; pareja inseparable de `lcm`, con el que cumple `gcd*lcm = f*g`. Sirve igual para polinomios y enteros.
- [[sympy.lcm]] — el **multiplo comun**; la otra mitad de la pareja con `gcd`, util para denominadores comunes.
- [[sympy.degree]] — la **consulta** de grado; complementa a las demas diciendo cuantas raices esperar o que grado tiene un resto/cociente.
- [[sympy.real_roots]] — las **raices reales exactas**; cierra el ciclo pasando del polinomio a sus ceros reales, distinta de la version numerica o de la que incluye complejas.

## Notas relacionadas

- [[sympy.polys/index | sympy.polys]]
