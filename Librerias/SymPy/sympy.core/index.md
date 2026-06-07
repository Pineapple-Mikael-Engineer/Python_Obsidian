---
title: sympy.core — sympy.core
tags:
  - sympy
  - indice
draft: true
---

# sympy.core

El **nucleo** de SymPy: el mecanismo con el que se crean, se representan y se evaluan las expresiones simbolicas. Todo lo que hacen los demas submodulos (simplificar, derivar, resolver, factorizar) se apoya en las piezas que viven aqui: un simbolo es un objeto de `core`, un numero exacto es un objeto de `core`, y la `Expr` —el arbol sobre el que opera toda la libreria— se define en `core`. Entender este submodulo es entender el modelo mental de SymPy; conviene tener presente [[concepto_simbolico_vs_numerico]] y [[concepto_expr_arbol]].

El submodulo se organiza siguiendo el **flujo** natural de trabajo: primero se crean los simbolos (las incognitas), con ellos y con numeros exactos se **construye** una `Expr` (un arbol de operaciones que no calcula nada todavia), y al final esa expresion se **evalua** a un numero concreto cuando hace falta salir del mundo simbolico.

```python
from sympy import symbols, Rational

x = symbols("x")                 # 1. crear el simbolo (incognita)
expr = x**2 + Rational(1, 2)     # 2. construir la Expr (arbol exacto, no evalua)
expr.subs(x, 3)                  # 3. transformar: 19/2
expr.subs(x, 3).evalf()          # 4. evaluar a numero: 9.50000000000000
```

## Como se relacionan

Las cuatro subcarpetas son las cuatro etapas de ese flujo: cada una responde a un "que tengo y que quiero" distinto.

| Subcarpeta | Papel en el flujo | Que entra / que sale |
|------------|-------------------|----------------------|
| [[sympy.core/simbolos/index \| simbolos]] | **Crear** las incognitas y dar entrada al mundo simbolico | nombre/cadena \| `Symbol`, `Expr` |
| [[sympy.core/numeros/index \| numeros]] | Los **valores exactos** (y constantes) con que se construyen las expresiones | `int`/`str` \| `Integer`, `Rational`, `Float` |
| [[sympy.core/expresiones/index \| expresiones]] | La **`Expr`**: el arbol que combina simbolos y numeros, y como inspeccionarlo o transformarlo | simbolos + numeros \| `Expr` |
| [[sympy.core/evaluacion/index \| evaluacion]] | El **puente** del mundo simbolico al numerico (un valor o muchos) | `Expr` \| `Float` / funcion NumPy |

El hilo conductor: `simbolos` + `numeros` son las **piezas**, `expresiones` es la **estructura** que las combina (y la unica que permanece exacta e inmutable), y `evaluacion` es la **salida** hacia un numero. Se recorre casi siempre en ese orden.

## Subtemas

- [[sympy.core/simbolos/index \| simbolos]] — De donde nacen las expresiones: `symbols` crea las incognitas, `Symbol` es la clase, `sympify`/`S` mete cadenas y numeros de Python al mundo simbolico.
- [[sympy.core/numeros/index \| numeros]] — Los ladrillos numericos exactos (`Integer`, `Rational`), el `Float` de precision arbitraria y las constantes (`pi`, `E`, `oo`, `I`); aqui vive la exactitud que distingue a SymPy.
- [[sympy.core/expresiones/index \| expresiones]] — La clase `Expr` (el arbol), como inspeccionarlo con `srepr` y como transformarlo con `subs` sin romper su inmutabilidad.
- [[sympy.core/evaluacion/index \| evaluacion]] — El final del flujo: `evalf` para un valor de alta precision y `lambdify` para evaluar masivo sobre arrays de NumPy.

## Notas relacionadas

- [[SymPy/index | SymPy]]
- [[Tree SymPy]]
- [[concepto_simbolico_vs_numerico]]
- [[concepto_expr_arbol]]
