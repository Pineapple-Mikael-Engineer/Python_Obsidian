---
title: sympy.calculus — sympy.calculus
tags:
  - sympy
  - indice
draft: true
---

# sympy.calculus

El **calculo simbolico** de SymPy: derivar, integrar, tomar limites, desarrollar en serie y sumar/multiplicar terminos, todo de forma **exacta** (sobre `Expr`, no flotantes). A diferencia del calculo numerico (NumPy/SciPy, que aproxima con numeros), aqui el resultado es una formula: `integrate(x**2, (x, 0, 1))` da `1/3`, no `0.333...`. Es el corazon "analitico" de la libreria y donde mejor se ve el caracter exacto de SymPy.

Toda la seccion comparte un mismo hilo conductor, el patron **funcion-vs-clase-sin-evaluar**: para cada operacion hay una **funcion en minuscula** que la *resuelve ya* (`diff`, `integrate`, `limit`, `series`) y una **clase en mayuscula** que la *plantea sin evaluar* (`Derivative`, `Integral`, `Limit`, `Sum`, `Product`). La clase guarda la operacion como objeto inerte — util para mostrarla, manipularla o renderizar el simbolo matematico — y se dispara con `.doit()`. Son las dos caras del mismo dato.

```python
from sympy import symbols, diff, Integral
x = symbols("x")

diff(x**3, x)              # 3*x**2   -> la funcion evalua ya
Integral(x**3, x)          # Integral(x**3, x)   -> la clase plantea sin evaluar
Integral(x**3, x).doit()   # x**4/4   -> .doit() dispara el calculo
```

## Como se relacionan

| Subcarpeta | Operacion | Funcion (evalua ya) | Clase (sin evaluar, `.doit()`) |
|------------|-----------|---------------------|--------------------------------|
| [[sympy.calculus/derivadas/index \| derivadas]] | derivar | `diff` | `Derivative` |
| [[sympy.calculus/integrales/index \| integrales]] | integrar | `integrate` | `Integral` |
| [[sympy.calculus/limites/index \| limites]] | tomar limite | `limit` | `Limit` |
| [[sympy.calculus/series/index \| series]] | desarrollar en serie | `series`, `fourier_series` | (sin clase diferida tipica) |
| [[sympy.calculus/sumatorios/index \| sumatorios]] | sumar / multiplicar | `summation`, `product` | `Sum`, `Product` |

Las cinco operaciones se encadenan en el flujo analitico habitual: se **deriva** o se **integra** una expresion, se estudia su comportamiento con un **limite** (asintotas, indeterminaciones), se aproxima localmente con una **serie**, y se cierran sumas/productos infinitos con los **sumatorios**. Derivacion e integracion son operaciones inversas; los limites son la base teorica de las otras cuatro.

## Subtemas

- [[sympy.calculus/derivadas/index | derivadas]] — diferenciacion simbolica; `diff` evalua, `Derivative` plantea sin evaluar.
- [[sympy.calculus/integrales/index | integrales]] — integracion indefinida y definida; misma pareja `integrate` / `Integral`. Operacion inversa de derivar.
- [[sympy.calculus/limites/index | limites]] — limites en un punto, laterales y en el infinito; `limit` / `Limit`. Sustento de derivadas, integrales y series.
- [[sympy.calculus/series/index | series]] — aproximacion por series: `series` (Taylor/Laurent, local en `x`) y `fourier_series` (periodicas, global en armonicos).
- [[sympy.calculus/sumatorios/index | sumatorios]] — `Sum` (sumatorio) y `Product` (productorio) simbolicos; `.doit()` busca la forma cerrada.

## Notas relacionadas

- [[SymPy/index | SymPy]]
- [[Tree SymPy]]
