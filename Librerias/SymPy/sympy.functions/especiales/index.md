---
title: sympy.functions/especiales — funciones especiales y distribucionales
tags:
  - sympy
  - indice
draft: false
---

# especiales

Esta carpeta agrupa las funciones de `sympy.functions` que **van mas alla del calculo elemental**: no son trig, exp ni log, sino las funciones que aparecen en combinatoria avanzada, probabilidad, analisis de senales y ecuaciones diferenciales con discontinuidades. El denominador comun es que todas operan en el dominio **simbolico exacto** —produciendo `sqrt(pi)`, `120` o `DiracDelta(x)` sin perder precision— y tienen contraparte distribucional o combinatoria que el calculo basico no cubre.

El eje conceptual de la carpeta son dos pares de funciones relacionadas: `gamma`-`factorial` (continuacion del factorial a los reales) y `Heaviside`-`DiracDelta` (modelado de discontinuidades). `Piecewise` es el mecanismo general que los unifica: tanto `Heaviside` como `Abs` pueden reescribirse como casos particulares de `Piecewise`.

## Ejemplo unificador

`gamma` y `factorial` son la misma funcion vista desde angulos distintos; `Heaviside` integrado sobre un intervalo devuelve exactamente la longitud del subintervalo positivo:

```python
from sympy import symbols, gamma, factorial, Heaviside, DiracDelta, integrate, oo, Rational

x = symbols("x")

# gamma como factorial continuo
gamma(5)               # 24         (= 4!)
factorial(4)           # 24
gamma(Rational(1, 2))  # sqrt(pi)   (valor exacto en semientero)

# Heaviside: el escalon como primitiva de DiracDelta
integrate(Heaviside(x), (x, -1, 2))           # 2    (longitud del tramo positivo [0,2])
integrate(DiracDelta(x - 2) * x**2, (x, -oo, oo))  # 4    (propiedad de muestreo: f(2))
```

## Como se relacionan

La decision clave: **que tipo de funcion especial necesitas** para el problema en cuestion.

| Funcion \| Clase | Dominio principal | Cuando usarla |
|------------------|-------------------|---------------|
| [[sympy.gamma]] | Analisis, probabilidad | Generalizar `factorial` a reales/complejos; integrales de Euler; distribucion Gamma |
| [[sympy.factorial_binomial]] | Combinatoria, series | Valores exactos de `n!`, `C(n,k)`, `n!!`; coeficientes en series de Taylor |
| [[Piecewise]] | Funciones por ramos | Definir funciones discontinuas; modelar entradas por tramos en EDOs; reescribir `Abs` |
| [[sympy.Heaviside_DiracDelta]] | Senales, control, EDOs | Escalon unitario; muestreo con delta de Dirac; derivadas distribucionales |

Arbol de decision:

- ¿Necesitas el **factorial generalizado** a reales o semienteros? -> [[sympy.gamma]].
- ¿Calculos **combinatorios exactos** (`n!`, `C(n,k)`, `n!!`) o coeficientes de serie? -> [[sympy.factorial_binomial]].
- ¿Quieres una funcion **definida por casos** o condiciones? -> [[Piecewise]]; es el mecanismo general.
- ¿Modelas un **escalon** o un **impulso** (sistemas de control, señales, EDOs con discontinuidades)? -> [[sympy.Heaviside_DiracDelta]].

> [!info] Piecewise como mecanismo unificador
> `Heaviside` puede verse como un `Piecewise((0, x < 0), (S.Half, Eq(x, 0)), (1, True))`, y `Abs(x)` como `Piecewise((x, x > 0), (-x, True))`. Usar `Heaviside` y `DiracDelta` directamente cuando el contexto es distribucional (integrales, derivadas); usar `Piecewise` cuando se necesita definir la funcion explicitamente por ramos.

## Notas

- [[sympy.gamma]] — funcion gamma simbolica; generaliza `factorial` a los reales/complejos. `gamma(n+1) == factorial(n)`. Valores exactos en semienteros: `gamma(Rational(1,2)) -> sqrt(pi)`.
- [[sympy.factorial_binomial]] — agrupa `factorial(n)`, `binomial(n, k)` y `factorial2(n)` (doble factorial). Exactos para enteros; permanecen sin evaluar para simbolos. Base de la combinatoria y las series de potencias.
- [[Piecewise]] — clase para funciones definidas a trozos. Cada par `(expr, condicion)` define un ramo; el ultimo con `True` actua como caso por defecto. Soporta `diff` e `integrate` simbolicos directamente.
- [[sympy.Heaviside_DiracDelta]] — escalon unitario `Heaviside(x)` e impulso `DiracDelta(x)`. `DiracDelta` es la derivada distribucional de `Heaviside`; su integral aplica la propiedad de muestreo `f(a)`.

## Notas relacionadas

- [[sympy.functions/index | sympy.functions]]
