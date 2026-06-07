---
title: sympy.trigsimp — simplificar usando identidades trigonometricas
aliases:
  - trigsimp
  - sympy.trigsimp
  - simplificar trigonometricas
tags:
  - sympy
  - api/funcion
  - simplify/trig_y_radicales
lib: sympy
mod: sympy.simplify
tipo: funcion
retorna: Expr
requiere:
  - Symbol
draft: false
---

# sympy.trigsimp — simplificar usando identidades trigonometricas

`trigsimp(expr)` reescribe una expresion aplicando **identidades trigonometricas** (pitagorica, suma de angulos, doble angulo, paso a tangente) para dejarla en la forma mas compacta posible. Es el simplificador **especializado** en trigonometria: ataca expresiones donde aparecen `sin`, `cos`, `tan`, `sinh`, `cosh`, etc., y reduce combinaciones que el `simplify` general podria no tocar de forma fiable. El caso canonico es colapsar la identidad pitagorica: `trigsimp(sin(x)**2 + cos(x)**2)` devuelve `1`. Tambien reconoce las identidades hiperbolicas.

> `trigsimp` **contrae** (de muchos terminos a pocos). La operacion **inversa**, que abre las trigonometricas usando las mismas identidades hacia el otro lado (`sin(x + y) -> sin(x)*cos(y) + sin(y)*cos(x)`), es `expand_trig` (no documentada aqui, vive en el codigo; equivale a `expand(..., trig=True)`).

## Firma

```python
sympy.trigsimp(
    expr,                # Expr: expresion con funciones trigonometricas
    method="matching",   # str: estrategia interna ("matching", "fu", "groebner"...)
    ...
) -> Expr
```

## Valor de retorno

| Tipo | Forma | Significado |
|------|-------|-------------|
| `Expr` | expresion simplificada | La misma expresion reescrita con menos terminos via identidades trigonometricas |

Si no encuentra ninguna simplificacion trigonometrica, devuelve la expresion **sin cambios** (no falla).

```python
from sympy import symbols, trigsimp, sin, cos
x = symbols("x")
trigsimp(sin(x)**2 + cos(x)**2)   # 1
```

## Formas basicas de llamada

| Objetivo | Llamada |
|----------|---------|
| Colapsar la identidad pitagorica | `trigsimp(sin(x)**2 + cos(x)**2)` |
| Pasar sin/cos a tangente | `trigsimp(sin(x)/cos(x))` |
| Simplificar identidades hiperbolicas | `trigsimp(cosh(x)**2 - sinh(x)**2)` |
| Elegir estrategia | `trigsimp(expr, method="fu")` |

## Parametros en detalle

### `expr` (obligatorio)

La expresion a simplificar. Reconoce las identidades fundamentales y las aplica en la direccion que reduce el numero de terminos.

```python
from sympy import symbols, trigsimp, sin, cos
x = symbols("x")
trigsimp(sin(x)**2 + cos(x)**2)     # 1
trigsimp(2*sin(x)**2 + 2*cos(x)**2) # 2
trigsimp(sin(x)/cos(x))             # tan(x)
trigsimp(cos(x)**4 - sin(x)**4)     # cos(2*x)
```

Tambien colapsa las identidades **hiperbolicas**:

```python
from sympy import symbols, trigsimp, cosh, sinh
x = symbols("x")
trigsimp(cosh(x)**2 - sinh(x)**2)   # 1
```

### `method`

Selecciona la estrategia interna de simplificacion. El valor por defecto (`"matching"`) cubre el caso comun; `"fu"` aplica el algoritmo de Fu (mas exhaustivo para identidades complicadas) y `"groebner"` usa bases de Groebner. Para expresiones que no se reducen con el metodo por defecto, conviene probar `"fu"`.

```python
from sympy import symbols, trigsimp, sin, cos
x = symbols("x")
trigsimp(cos(x)**4 - sin(x)**4, method="fu")   # cos(2*x)
```

## Casos de uso

### Normalizar un resultado trigonometrico antes de compararlo

Tras derivar o integrar, una expresion trigonometrica puede quedar en una forma poco reconocible; `trigsimp` la lleva a forma canonica para compararla o leerla.

```python
from sympy import symbols, trigsimp, sin, cos
x = symbols("x")
expr = sin(x)**2 + cos(x)**2 + sin(x)**2 + cos(x)**2
trigsimp(expr)   # 2
```

### Reducir una identidad antes de seguir operando

Colapsar la parte trigonometrica deja una expresion mas barata para los pasos siguientes (sustituir, evaluar, resolver).

```python
from sympy import symbols, trigsimp, sin, cos
x = symbols("x")
trigsimp(cos(x)**4 - sin(x)**4)   # cos(2*x)
```

## Errores comunes

| Error | Causa | Solucion |
|-------|-------|----------|
| `trigsimp` no expande `sin(x + y)` | Expande **abrir**, no es su trabajo: solo contrae | Usar `expand_trig` o `expand(..., trig=True)` |
| No reduce una identidad complicada | El metodo por defecto no la cubre | Probar `trigsimp(expr, method="fu")` |
| Esperar que toque potencias o radicales | `trigsimp` solo ataca trigonometricas | Usar [[sympy.powsimp]] o [[sympy.radsimp]] |
| Resultado sin cambios | No habia identidad aplicable | Verificar que la expresion realmente se simplifica |

## Notas relacionadas

- [[sympy.radsimp]]
- [[sympy.powsimp]]
- [[sympy.simplify/trig_y_radicales/index | trig_y_radicales]]
- [[sympy.expand]]
