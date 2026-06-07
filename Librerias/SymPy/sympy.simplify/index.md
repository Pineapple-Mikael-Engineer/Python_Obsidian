---
title: sympy.simplify — reescribir una expresion en forma equivalente
tags:
  - sympy
  - indice
draft: false
---

# sympy.simplify

Este submodulo agrupa las herramientas para **transformar una expresion en otra equivalente**
mas conveniente. El punto de partida es que SymPy **solo auto-simplifica lo trivial** (`x + x ->
2*x`): cualquier reescritura no trivial hay que **pedirla explicitamente**, y aqui estan las
funciones para hacerlo. Ver [[concepto_simplificacion_automatica]] para el porque.

La decision central de toda la carpeta es **que tan especifico ser**:

```python
from sympy import symbols, sin, cos, simplify, trigsimp, cancel
x = symbols("x")

simplify(sin(x)**2 + cos(x)**2)   # 1   -> comodin general (lento, prueba de todo)
trigsimp(sin(x)**2 + cos(x)**2)   # 1   -> especifico de trig (rapido, predecible)
cancel((x**2 - 1)/(x - 1))        # x + 1   -> especifico de racionales
```

## Como se relacionan

| Carpeta | Que hace | Cuando |
|---------|----------|--------|
| [[sympy.simplify/general/index \| general]] | el comodin `simplify` + especificos `cancel`/`nsimplify` | cuando no sabes que forma quieres, o racionales/floats |
| [[sympy.simplify/trig_y_radicales/index \| trig_y_radicales]] | simplificadores **por dominio**: `trigsimp`, `radsimp`, `powsimp` | sabes que el problema es trig, radicales o potencias |
| [[sympy.simplify/reescritura/index \| reescritura]] | `Expr.rewrite`: cambiar de **representacion**, no simplificar | reexpresar `tan` como `sin/cos`, `exp` como `cos`, etc. |

> [!regla]
> Prefiere la **funcion especifica** (`factor`, `cancel`, `trigsimp`, `powsimp`) cuando sabes
> que tipo de transformacion buscas: es mas rapida y **predecible**. Reserva `simplify` (el
> comodin) para cuando no lo sabes; es potente pero **lento y no canonico**. Y recuerda que
> *reescribir* (`rewrite`) no es *simplificar*: cambia la base de funciones, no busca lo "mas
> simple".

Estas funciones se complementan con las de [[sympy.polys/index | sympy.polys]] (`expand`,
`factor`, `apart`): la frontera es difusa, pero `polys` se centra en la forma polinomica y
`simplify` en la simplificacion general y por dominios.

## Subtemas

- [[sympy.simplify/general/index | general]] — `simplify` (comodin general), `cancel` (racionales) y `nsimplify` (de float a simbolico).
- [[sympy.simplify/trig_y_radicales/index | trig_y_radicales]] — `trigsimp`, `radsimp`, `powsimp`: un simplificador por cada tipo de expresion.
- [[sympy.simplify/reescritura/index | reescritura]] — `Expr.rewrite`: reexpresar en terminos de otra funcion.

## Notas relacionadas

- [[SymPy/index | SymPy]]
- [[Tree SymPy]]
- [[concepto_simplificacion_automatica]]
