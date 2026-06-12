---
title: conceptos_transversales — conceptos_transversales
tags:
  - sympy
  - indice
draft: false
---

# conceptos_transversales

Estos cinco conceptos no son un submodulo de la API: son el **modelo mental** de SymPy, las ideas que gobiernan como se comporta toda la libreria. Antes de tocar `solve`, `integrate` o `Matrix` conviene tenerlos claros, porque explican los "porques" que de otro modo parecen rarezas: por que `1/3` da `0.333...` y no `1/3`, por que `e.subs(...)` no cambia `e`, por que una raiz "obvia" no se simplifica sola o por que graficar con SymPy es lentisimo. Casi todo lo que sorprende de SymPy se reduce a uno de estos cinco temas; leerlos primero evita pelear contra la libreria mas adelante.

La idea que los une es que SymPy trabaja con **expresiones exactas** (arboles de `Expr` inmutables), no con flotantes, y que el control fino sobre que se simplifica y cuando se pasa a numero esta en tus manos, no en una caja negra.

## Orden de lectura recomendado

Hay un hilo conductor natural, de lo conceptual a lo operativo:

1. **Que es simbolico** — [[concepto_simbolico_vs_numerico]]: exacto frente a flotante, el porque de toda la libreria.
2. **Como se representa** — [[concepto_expr_arbol]]: cada expresion es un arbol inmutable de `Expr` (`.func`/`.args`).
3. **Como se nombran las incognitas** — [[concepto_symbols_assumptions]]: `Symbol` y los supuestos que cambian el resultado.
4. **Que se simplifica solo** — [[concepto_simplificacion_automatica]]: lo automatico (trivial) frente a lo que hay que pedir.
5. **Como volver a numero** — [[concepto_evalf_lambdify]]: el puente final con `subs`, `evalf` y `lambdify`.

Es tambien el ciclo de un problema real: decides quedarte en simbolico (1), construyes la expresion (2), declaras las incognitas y sus supuestos (3), la manipulas y simplificas (4) y, al final, obtienes un valor o una grafica (5).

## Como se relacionan

| Concepto | Pregunta que responde | De que depende |
|----------|------------------------|----------------|
| [[concepto_simbolico_vs_numerico]] | ¿Por que SymPy es exacto y no usa flotantes? ¿Cuando conviene? | Marco general; se apoya en `Expr` para "ser exacto" |
| [[concepto_expr_arbol]] | ¿Como se representa una expresion por dentro (`.func`/`.args`, inmutabilidad)? | Es el sustrato; explica por que `==` es estructural y por que hay que reasignar |
| [[concepto_symbols_assumptions]] | ¿Como se crea una incognita y por que sus supuestos cambian el algebra? | Los simbolos son los atomos del arbol (`Expr`); habilitan o no las simplificaciones |
| [[concepto_simplificacion_automatica]] | ¿Que reescribe SymPy solo y que hay que pedir con `simplify`/`factor`...? | Actua sobre el arbol y depende de los supuestos; pierde exactitud si entra un `float` |
| [[concepto_evalf_lambdify]] | ¿Como paso de simbolico a un numero o a una funcion rapida? | Es la salida del mundo exacto; cierra el ciclo hacia lo numerico |

## Notas

- [[concepto_simbolico_vs_numerico]] — exacto frente a flotante: el porque de SymPy. Es la raiz: justifica trabajar simbolico el mayor tiempo posible y dejar lo numerico para el final.
- [[concepto_expr_arbol]] — `Expr`, `.func`/`.args`, `srepr` e inmutabilidad. Define **como** se materializa esa exactitud y por que las expresiones son inmutables y hashables; es el sustrato de los otros cuatro.
- [[concepto_symbols_assumptions]] — `Symbol` y los supuestos (`real`, `positive`, `integer`...). Los simbolos son los atomos del arbol; sus supuestos deciden que puede simplificar SymPy.
- [[concepto_simplificacion_automatica]] — auto-simplify frente a `simplify`/`expand`/`factor`. Distingue lo trivial que se hace solo de lo que hay que invocar; usa los supuestos y mantiene la exactitud solo si no se cuela un `float`.
- [[concepto_evalf_lambdify]] — de simbolico a numerico con `subs`/`evalf`/`lambdify`. Cierra el ciclo: el puente para obtener un valor o una funcion vectorizada hacia NumPy.

## Notas relacionadas

- [[SymPy/index | SymPy]]
