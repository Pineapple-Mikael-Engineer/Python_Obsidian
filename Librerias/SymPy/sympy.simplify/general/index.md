---
title: sympy.simplify/general — general
tags:
  - sympy
  - indice
draft: false
---

# general

Esta carpeta reune las simplificaciones de **proposito general**: las que aplicas cuando quieres dejar una expresion "mas limpia" sin que sea una transformacion algebraica de un solo tipo. Conviven aqui tres herramientas de naturaleza muy distinta. Una es el **comodin** que prueba de todo cuando no sabes que necesitas ([[sympy.simplify]]); otra es una operacion **especifica y predecible** sobre cocientes de polinomios ([[sympy.cancel]]); y la tercera es el **puente inverso** que recupera una expresion simbolica a partir de un numero flotante ([[sympy.nsimplify]]). La idea que las hilvana es una sola decision practica: **¿sabes que forma quieres?** Si la sabes, usa la funcion especifica (rapida y canonica); si no, deja que `simplify` lo intente por ti.

Las tres, vistas en un mismo bloque:

```python
from sympy import symbols, simplify, cancel, nsimplify, sin, cos
x = symbols("x")

simplify(sin(x)**2 + cos(x)**2)   # 1            -> comodin: reconoce la identidad
cancel((x**2 - 1)/(x - 1))        # x + 1        -> especifico: reduce el cociente
nsimplify(0.5)                    # 1/2          -> puente: de float a simbolico
```

## Como se relacionan

El modelo mental es: un **comodin lento y no canonico**, una **operacion especifica y predecible** sobre racionales, y un **puente** que viene del mundo numerico.

- **`simplify`** es el comodin: prueba muchas transformaciones (trig, gammas, fracciones, potencias) y devuelve la que mide como mas simple. Potente cuando no sabes que quieres, pero **lento** y **no canonico** (no garantiza una forma concreta).
- **`cancel`** es lo contrario en filosofia: hace **una** cosa —cancelar factores comunes y dejar `p/q` reducido— siempre igual y rapido. Es lo que internamente usa `simplify` para la parte racional, pero llamado directo es predecible.
- **`nsimplify`** no compite con las otras dos: opera sobre **numeros**, no sobre algebra simbolica. Es el inverso conceptual de `evalf` (simbolico -> float); reconstruye el simbolico desde el float.

| Funcion | Que hace | Naturaleza |
|---------|----------|------------|
| [[sympy.simplify]] | Prueba muchas transformaciones y devuelve "la mas simple" | Comodin general, lento, **no canonico** |
| [[sympy.cancel]] | Cancela factores comunes -> `p/q` reducido y canonico | Especifico (racionales), rapido, **predecible** |
| [[sympy.nsimplify]] | Reconstruye un simbolico desde un float (`0.5` -> `1/2`) | Puente inverso de `evalf` (numerico -> simbolico) |

> [!info] ¿Que funcion uso?
> **¿Sabes que forma quieres?**
> - Si, y es reducir un cociente -> [[sympy.cancel]] (o `factor`, `trigsimp`… la especifica del caso).
> - Si, pero partes de un **numero** y quieres su forma exacta -> [[sympy.nsimplify]].
> - No sabes que transformacion aplicar -> [[sympy.simplify]] (asume lentitud y forma no garantizada).

## Notas

- [[sympy.simplify]] — el comodin de la carpeta: heuristico, prueba muchas transformaciones y devuelve la mas simple; usalo cuando **no sabes** que quieres, sabiendo que es lento y no canonico. La alternativa especifica casi siempre existe y es mejor.
- [[sympy.cancel]] — el opuesto del comodin: operacion **especifica y predecible** que cancela factores comunes de un racional y deja `p/q` reducido. Es la parte "fracciones" que `simplify` hace por dentro, pero rapida y canonica.
- [[sympy.nsimplify]] — el **puente inverso**: no simplifica algebra, recupera un simbolico (`1/2`, `pi`, `sqrt(2)`) a partir de un float; el camino de vuelta de `evalf`.

## Notas relacionadas

- [[sympy.simplify/index | sympy.simplify]]
