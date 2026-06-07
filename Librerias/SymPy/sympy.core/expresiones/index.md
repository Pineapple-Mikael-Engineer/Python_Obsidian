---
title: sympy.core/expresiones — expresiones
tags:
  - sympy
  - indice
draft: true
---

# expresiones

El **corazon** de SymPy: la clase [[Expr]], de la que hereda toda expresion matematica (simbolos, numeros, sumas, productos, potencias, funciones). Una `Expr` no es ni texto ni un float: es un **arbol** de nodos `func`/`args` que combina los simbolos y numeros de las otras carpetas de [[sympy.core/index | sympy.core]]. Esta carpeta cubre como es ese arbol, como **inspeccionarlo** ([[sympy.srepr]]) y como **transformarlo** ([[Expr.subs]]). El modelo mental completo esta en [[concepto_expr_arbol]].

El hilo de la carpeta es la distincion **inspeccionar vs modificar** bajo una propiedad central: la `Expr` es **inmutable**. Ningun metodo la cambia en su sitio; `subs` no edita la expresion, devuelve una **nueva** (hay que reasignar). `srepr` ni siquiera produce otra expresion: solo la fotografia para leerla.

```python
from sympy import symbols, srepr

x = symbols("x")
e = x**2 + 1
srepr(e)          # "Add(Pow(Symbol('x'), Integer(2)), Integer(1))"  -> inspeccionar
e.subs(x, 3)      # 10        -> NUEVA expresion (transformar)
e                 # x**2 + 1  -> la original intacta (inmutable)
```

## Como se relacionan

Las tres notas giran sobre la misma `Expr`: una la **define**, otra la **lee** sin tocarla, otra la **transforma** devolviendo otra `Expr`.

| Nota | Que hace con la `Expr` | Sobre el arbol |
|------|------------------------|----------------|
| [[Expr]] | **Define** la clase base, el arbol `func`/`args`, su inmutabilidad y la igualdad estructural | Es el arbol |
| [[sympy.srepr]] | **Inspecciona**: imprime el arbol exacto como `str` (tipos, supuestos, orden de `args`) | Lo lee, no lo cambia |
| [[Expr.subs]] | **Transforma**: sustituye subexpresiones y devuelve una `Expr` nueva | Produce otro arbol |

Relacion en una frase: `Expr` es el objeto, `srepr` lo mira por dentro (util para depurar por que dos expresiones no son `==`, ya que la igualdad es **estructural** y no matematica), y `subs` lo reescribe respetando la inmutabilidad. Inspeccionar nunca muta; transformar siempre crea algo nuevo.

## Notas

- [[Expr]] — La clase base de toda expresion: el arbol de nodos `func`/`args`, la inmutabilidad y la igualdad estructural (no matematica). El centro de la carpeta.
- [[sympy.srepr]] — La via para **ver** la estructura interna como `str` exacto; revela tipos de numero y supuestos que `print` oculta. Herramienta de depuracion.
- [[Expr.subs]] — La via para **modificar** sin mutar: sustituye simbolos o subexpresiones y devuelve una `Expr` nueva; acepta diccionarios y `simultaneous` para intercambios.

## Notas relacionadas

- [[sympy.core/index | sympy.core]]
- [[concepto_expr_arbol]]
- [[Expr.evalf]]
- [[Tree SymPy]]
