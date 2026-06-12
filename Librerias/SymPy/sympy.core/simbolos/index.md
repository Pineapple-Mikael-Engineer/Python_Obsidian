---
title: sympy.core/simbolos — simbolos
tags:
  - sympy
  - indice
draft: false
---

# simbolos

El **punto de entrada** al mundo simbolico: aqui se crean las incognitas con las que se construye toda expresion. Una expresion de SymPy no existe hasta que hay un `Symbol` sobre el que operar, asi que esta carpeta es la primera etapa del flujo de [[sympy.core/index | sympy.core]]. Cubre las dos formas de fabricar simbolos —[[sympy.symbols]] (la fabrica idiomatica) y la clase [[Symbol]] (lo que esa fabrica produce)— y la puerta general por la que cualquier cadena o numero de Python se convierte en objeto SymPy, [[sympy.sympify]] y su atajo `S`.

La idea clave es que un simbolo no es solo un nombre: lo definen su **nombre** y sus **supuestos** (`real`, `positive`, `integer`…), que son los que gobiernan el algebra; ver [[concepto_symbols_assumptions]].

```python
from sympy import symbols, Symbol, S

x, y = symbols("x y")            # fabrica idiomatica: varios de una vez
p = Symbol("p", positive=True)   # la clase directa, con un supuesto
S(1)/3                           # 1/3  -> sympify convierte y fuerza exactitud
```

## Como se relacionan

`symbols` y `Symbol` hacen lo mismo (crear simbolos) por dos caminos; `sympify`/`S` es de otra naturaleza: no crea incognitas, sino que **traduce** objetos de Python al mundo simbolico.

| Nota | Que hace | Cuando usarla |
|------|----------|---------------|
| [[sympy.symbols]] | **Crea** uno o varios simbolos desde una cadena (rangos, grupos, supuestos a todos) | Casi siempre; es el camino idiomatico, sobre todo para varios a la vez |
| [[Symbol]] | La **clase** del simbolo: nombre + supuestos, identidad y atributos `.is_*` | Un unico simbolo puntual, o para entender que devuelve `symbols` |
| [[sympy.sympify]] | **Convierte** `str`/`int`/`float`/listas en objetos SymPy; `S` fuerza exactitud (`S(1)/3`) | Parsear una expresion en texto, o evitar caer en `float` de Python |

Relacion en una frase: `symbols` es la fabrica, `Symbol` es el producto, y `sympify`/`S` es la aduana por la que entra todo lo que viene de Python. Las tres comparten que su salida ya vive en el arbol `Expr`.

## Notas

- [[sympy.symbols]] — La fabrica de simbolos; devuelve un `Symbol` o una tupla de ellos y reparte los supuestos. El camino recomendado.
- [[Symbol]] — La clase que `symbols` instancia: su identidad depende del par (nombre, supuestos) y expone la logica de tres valores `.is_*`.
- [[sympy.sympify]] — El conversor general str/num → `Expr`; su atajo `S` es ademas la via idiomatica para forzar aritmetica exacta.

## Notas relacionadas

- [[sympy.core/index | sympy.core]]
- [[concepto_symbols_assumptions]]
- [[concepto_simbolico_vs_numerico]]
