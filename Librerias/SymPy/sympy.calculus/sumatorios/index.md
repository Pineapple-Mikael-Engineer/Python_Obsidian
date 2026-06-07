---
title: sympy.calculus/sumatorios — sumatorios
tags:
  - sympy
  - indice
draft: true
---

# sumatorios

El **calculo concreto** de SymPy: sumatorios y productorios simbolicos. [[Sum]] representa una suma $\sum_{i=a}^{b} f(i)$ y [[Product]] un producto $\prod_{i=a}^{b} f(i)$, ambos de forma **exacta** y con limites que pueden ser numericos, simbolicos o `oo`. Lo potente es que `.doit()` no suma/multiplica termino a termino: busca una **forma cerrada** (Gauss, series conocidas, factorial, hipergeometricas), de modo que `Sum(i, (i, 1, n))` se cierra a `n*(n+1)/2` y `Product(i, (i, 1, n))` a `factorial(n)`.

Esta carpeta encaja en el patron transversal de la seccion por el lado de las **clases en mayuscula sin evaluar**: `Sum` y `Product` construidos no calculan nada — son objetos inertes que se disparan con `.doit()`. Sus atajos en minuscula `summation(...)` y `product(...)` hacen construir + `.doit()` en un paso (el equivalente a `diff`/`integrate` para el resto del calculo).

```python
from sympy import symbols, Sum, Product, oo
i, n = symbols("i n")

Sum(i, (i, 1, n)).doit()        # n**2/2 + n/2   -> Gauss, forma cerrada
Product(i, (i, 1, n)).doit()    # factorial(n)   -> el factorial
Sum(1/i**2, (i, 1, oo)).doit()  # pi**2/6        -> serie de Basilea
```

## Como se relacionan

| Aspecto | `Sum` | `Product` |
|---------|-------|-----------|
| Operacion | sumatorio $\sum f(i)$ | productorio $\prod f(i)$ |
| Elemento neutro (rango vacio) | `0` | `1` |
| Forma cerrada emblematica | `Sum(i, (i, 1, n))` = `n*(n+1)/2` | `Product(i, (i, 1, n))` = `factorial(n)` |
| Atajo (construir + evaluar) | `summation(...)` | `product(...)` |
| Sin evaluar al construir | si, hasta `.doit()` | si, hasta `.doit()` |

Son analogos: `Product` es a la multiplicacion lo que `Sum` a la suma, con la misma sintaxis `(i, a, b)`, los mismos atributos (`.function`, `.limits`, `.variables`) y el mismo comportamiento de `.doit()` (forma cerrada si existe, o el objeto intacto si no). Con `b = oo` evaluan la **serie**/producto infinito cuando converge a un valor conocido.

## Notas

- [[Sum | Sum]] — sumatorio simbolico sin evaluar; `.doit()` busca la forma cerrada, `summation(...)` es el atajo.
- [[Product | Product]] — productorio simbolico, analogo multiplicativo de `Sum`; `.doit()` da la forma cerrada (factorial y otros), `product(...)` el atajo.

## Notas relacionadas

- [[sympy.calculus/index | sympy.calculus]]
- [[Tree SymPy]]
