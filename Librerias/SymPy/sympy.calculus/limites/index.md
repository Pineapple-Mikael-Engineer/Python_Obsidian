---
title: sympy.calculus/limites — limites
tags:
  - sympy
  - indice
draft: false
---

# limites

El **calculo de limites** en SymPy: el valor al que tiende una expresion cuando su variable se acerca a un punto, incluido el **infinito**. Resuelve las indeterminaciones clasicas (`0/0`, `inf/inf`, `1**inf`) con el algoritmo de Gruntz, asi que `sin(x)/x` cuando `x -> 0` da `1` directamente. Es el sustento teorico del resto del calculo (derivadas, integrales, series) y la herramienta para detectar asintotas y comportamiento asintotico.

Sigue el patron transversal de la seccion: la **funcion** [[sympy.limit]] (en minuscula) *evalua ya* el limite; la **clase** [[Limit]] (en mayuscula) lo *plantea sin evaluar* y lo deja diferido hasta `.doit()`. Dos rasgos propios de los limites: los **laterales** via `dir` (`"+"` derecha por defecto, `"-"` izquierda, `"+-"` bilateral) y los puntos en el **infinito** con `oo`/`-oo` de SymPy (nunca `float('inf')`).

```python
from sympy import symbols, limit, Limit, sin, oo
x = symbols("x")

limit(sin(x)/x, x, 0)        # 1     -> la funcion evalua ya
limit(1/x, x, oo)            # 0     -> limite en el infinito
limit(1/x, x, 0, "-")        # -oo   -> limite por la izquierda
Limit(sin(x)/x, x, 0).doit() # 1     -> la clase, evaluada con .doit()
```

> Por defecto `dir="+"`: `limit(1/x, x, 0)` da `oo`, no `zoo`. Para el bilateral "de libro" pide `dir="+-"`.

## Como se relacionan

| Aspecto | `limit` (funcion) | `Limit` (clase) |
|---------|-------------------|-----------------|
| Que hace al llamarla | **evalua** y devuelve el valor del limite | **no evalua**: deja el limite planteado |
| Tipo de salida | `Expr` (finita, `oo`, `zoo` o `nan`) | objeto `Limit` (una `Expr` inerte) |
| Como obtener el valor | directo | con `.doit()` |
| Caso de uso | quiero el resultado | quiero **mostrar** lim o encadenar pasos |
| Argumentos | identicos en ambas | `(f, x, x0, dir)` |

La equivalencia es exacta: `limit(f, x, x0, dir)` es `Limit(f, x, x0, dir).doit()`. La clase es la forma "perezosa" — util para renderizar el simbolo lim en LaTeX o mostrar una deduccion antes de resolverla.

## Notas

- [[sympy.limit | sympy.limit]] — la funcion que evalua el limite; soporta laterales (`dir`) e infinito (`oo`).
- [[Limit | Limit]] — la clase que plantea el limite sin evaluar, para mostrarlo o manipularlo; se dispara con `.doit()`.

## Notas relacionadas

- [[sympy.calculus/index | sympy.calculus]]
