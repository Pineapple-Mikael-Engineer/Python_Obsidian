---
title: sympy.simplify/trig_y_radicales — trig y radicales
tags:
  - sympy
  - indice
draft: false
---

# trig y radicales

Esta carpeta reune los simplificadores **especializados por dominio**: cada uno sabe reescribir un **tipo concreto** de expresion mejor de lo que lo haria el `simplify` general. `simplify` es una heuristica que prueba muchas transformaciones y se queda con la "mas simple"; util, pero lento y a veces impredecible. Cuando ya sabes **que clase** de expresion tienes entre manos (una identidad trigonometrica, un denominador con raices, un producto de potencias), llamar al simplificador especializado es mas rapido, mas predecible y mas potente. La idea que hilvana la carpeta es justamente esa: **elegir la herramienta segun el tipo de expresion**, en vez de delegar a ciegas en `simplify`.

Cada simplificador ataca su propio dominio:

```python
from sympy import symbols, sin, cos, sqrt, trigsimp, radsimp, powsimp
x, a, b = symbols("x a b")

trigsimp(sin(x)**2 + cos(x)**2)   # 1            -> identidades trigonometricas
radsimp(1/(sqrt(2) + 1))          # -1 + sqrt(2) -> racionaliza el denominador
powsimp(x**a * x**b)              # x**(a + b)   -> combina potencias
```

## Como se relacionan

No son pares inversos ni se solapan: cada uno cubre **un tipo de expresion distinto**, y por eso conviven sin pisarse. El criterio para elegir es mirar **que** estorba en la expresion.

| Funcion | Tipo de expresion que ataca | Que hace | Inversa (en codigo) |
|---------|-----------------------------|----------|---------------------|
| [[sympy.trigsimp]] | trigonometricas / hiperbolicas | Aplica identidades para contraer: `sin(x)**2 + cos(x)**2 \| -> 1` | `expand_trig` |
| [[sympy.radsimp]] | radicales en el denominador | Racionaliza: mueve las raices fuera del denominador | `sqrtdenest` (desanida raices) |
| [[sympy.powsimp]] | potencias / exponenciales | Combina por base o exponente: `x**a * x**b \| -> x**(a + b)` | `expand_power_exp` |

> [!info] Que herramienta usar
> Si lo que estorba es **trigonometria** (sin/cos/tan, identidades): `trigsimp`. Si es una **raiz en el denominador**: `radsimp`. Si son **potencias o exponenciales** sueltas que deberian juntarse: `powsimp`. Si **no sabes** que tipo es, o quieres un intento generico: `simplify` (mas lento y menos predecible). Cada especializado tiene ademas su operacion **inversa** en el codigo (`expand_trig`, `sqrtdenest`, `expand_power_exp`) para mover la expresion en la direccion contraria.

## Notas

- [[sympy.trigsimp]] — el especialista en **trigonometricas**: contrae identidades (pitagorica, doble angulo) hasta la forma minima; su inversa `expand_trig` las abre. No toca radicales ni potencias.
- [[sympy.radsimp]] — el especialista en **radicales**: racionaliza denominadores con raices; emparejado con `sqrtdenest`, que desanida raices dentro de raices. No toca trigonometricas ni potencias.
- [[sympy.powsimp]] — el especialista en **potencias**: junta exponentes de la misma base o bases con el mismo exponente (con `force=True` cuando faltan supuestos); su inversa `expand_power_exp` las separa.

## Notas relacionadas

- [[sympy.simplify/index | sympy.simplify]]
