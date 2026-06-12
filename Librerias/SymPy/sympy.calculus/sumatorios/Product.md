---
title: Product — productorio simbolico no evaluado
aliases:
  - Product
  - productorio simbolico
  - product
tags:
  - sympy
  - api/clase
  - calculus/sumatorios
lib: sympy
mod: sympy.concrete.products
tipo: clase
retorna: Product | Expr
requiere:
  - Symbol
draft: false
---

# Product — productorio simbolico no evaluado

Representa un **productorio** $\prod_{i=a}^{b} f(i)$ en forma simbolica y **sin evaluar**. Es el analogo multiplicativo de [[Sum]]: construir `Product(f, (i, a, b))` no calcula nada, deja el producto como objeto inerte. El calculo ocurre al llamar `.doit()`, que busca una **forma cerrada** cuando existe. El caso emblematico es `Product(i, (i, 1, n)).doit()`, que se cierra a `factorial(n)` — el productorio de los primeros `n` enteros es, por definicion, el **factorial**. La funcion auxiliar `product(...)` construye y evalua en un solo paso.

## Constructor

```python
sympy.Product(
    function,     # Expr: el termino general f(i) a multiplicar
    *limits,      # tupla(s) (i, a, b): indice y limites inferior/superior (b puede ser oo)
)                 # -> Product  (objeto NO evaluado)
```

El indice `i` es una `Symbol`; `a` y `b` son los limites. Como en `Sum`, se admiten **varios** `(i, a, b)` para productos anidados.

## Formas basicas de construccion

| Objetivo | Llamada | Resultado |
|----------|---------|-----------|
| Producto finito simbolico | `Product(i, (i, 1, n))` | `Product(i, (i, 1, n))` (sin evaluar) |
| Producto de constante | `Product(k, (i, 1, n))` | `Product(k, (i, 1, n))` |
| Evaluar a forma cerrada | `Product(i, (i, 1, n)).doit()` | `factorial(n)` |
| Producto numerico | `Product(i, (i, 1, 5)).doit()` | `120` |

## `.doit()` — evaluar el producto

`.doit()` dispara el calculo y devuelve una `Expr`: una **forma cerrada** si SymPy la encuentra, o el producto intacto si no.

```python
from sympy import Product, symbols

i, n, k = symbols("i n k")

Product(i, (i, 1, n)).doit()    # factorial(n)        -> n! = 1*2*...*n
Product(i, (i, 1, 5)).doit()    # 120                 -> 5! exacto
Product(k, (i, 1, n)).doit()    # k**n                -> constante repetida n veces
Product(2, (i, 1, n)).doit()    # 2**n
```

## Relacion con el factorial

El productorio de los enteros `1..n` **es** el factorial; SymPy lo reconoce y devuelve `factorial(n)`:

```python
from sympy import Product, factorial, symbols

i, n = symbols("i n")

Product(i, (i, 1, n)).doit()           # factorial(n)
Product(i, (i, 1, n)).doit() == factorial(n)   # True
Product(i, (i, 1, 5)).doit()           # 120  ==  factorial(5)
```

> [!info]
> Un producto sobre un rango **vacio** vale `1` (elemento neutro), igual que una `Sum` vacia vale `0`.

## product(...) — atajo de construir y evaluar

La funcion auxiliar `product(...)` equivale a `Product(...).doit()` en una sola llamada:

```python
from sympy import product, symbols

i, n = symbols("i n")

product(i, (i, 1, 4))       # 24            -> 4!
product(i, (i, 1, n))       # factorial(n)
```

## Atributos clave

| Atributo | Tipo | Significado |
|----------|------|-------------|
| `.function` | `Expr` | El termino general `f(i)` |
| `.limits` | `tuple` | Tupla de limites `((i, a, b), ...)` |
| `.variables` | `list` | Los indices del producto |

```python
from sympy import Product, symbols

i, n = symbols("i n")
p = Product(i, (i, 1, n))

p.function   # i
p.limits     # ((i, 1, n),)
```

## Errores comunes

| Error | Causa | Solucion |
|-------|-------|----------|
| `Product(...)` "no multiplica nada" | El constructor NO evalua, solo representa | Llamar `.doit()` o usar `product(...)` |
| `.doit()` devuelve el mismo `Product` | No hay forma cerrada conocida | Es esperado; usar limites numericos o `.evalf()` |
| Limites como `(1, n)` sin indice | Falta la variable en la tupla | Forma correcta: `(i, 1, n)` |
| Confundir indice con constante | `Product(k, (i, 1, n))` repite `k`, da `k**n` | Para `n!` el termino debe ser el propio indice `i` |

## Notas relacionadas

- [[Sum]]
- [[sympy.calculus/sumatorios/index | sumatorios]]
- [[Rational]]
