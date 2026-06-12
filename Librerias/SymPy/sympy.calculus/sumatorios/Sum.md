---
title: Sum — sumatorio simbolico no evaluado
aliases:
  - Sum
  - sumatorio simbolico
  - summation
tags:
  - sympy
  - api/clase
  - calculus/sumatorios
lib: sympy
mod: sympy.concrete.summations
tipo: clase
retorna: Sum | Expr
requiere:
  - Symbol
draft: false
---

# Sum — sumatorio simbolico no evaluado

Representa un **sumatorio** $\sum_{i=a}^{b} f(i)$ en forma simbolica y **sin evaluar**. Construir `Sum(f, (i, a, b))` no calcula nada: deja la suma como un objeto inerte que puede manipularse, mostrarse o sustituirse. El calculo real ocurre al llamar .doit(), que intenta hallar una **forma cerrada** (Gauss, series conocidas, hipergeometricas) en lugar de sumar termino a termino. Asi `Sum(i, (i, 1, n))` se cierra a `n*(n+1)/2` para `n` simbolico, y `Sum(1/i**2, (i, 1, oo))` se evalua a `pi**2/6`. La funcion auxiliar `summation(...)` hace ambos pasos de una vez.

## Constructor

```python
sympy.Sum(
    function,     # Expr: el termino general f(i) a sumar
    *limits,      # tupla(s) (i, a, b): indice y limites inferior/superior (b puede ser oo)
)                 # -> Sum  (objeto NO evaluado)
```

El indice `i` es una `Symbol`; `a` y `b` son los limites (enteros, simbolos o `oo`). Se admiten **varios** `(i, a, b)` para sumas anidadas.

## Formas basicas de construccion

| Objetivo | Llamada | Resultado |
|----------|---------|-----------|
| Suma finita simbolica | `Sum(i, (i, 1, n))` | `Sum(i, (i, 1, n))` (sin evaluar) |
| Suma con limite infinito | `Sum(1/i**2, (i, 1, oo))` | `Sum(1/i**2, (i, 1, oo))` |
| Suma anidada (doble) | `Sum(i*j, (i, 1, n), (j, 1, m))` | doble sumatorio sin evaluar |
| Evaluar a forma cerrada | `Sum(i, (i, 1, n)).doit()` | `n**2/2 + n/2` |

## `.doit()` — evaluar la suma

`.doit()` dispara el calculo y devuelve una `Expr`: una **forma cerrada** si SymPy la encuentra, o la suma intacta si no.

```python
from sympy import Sum, symbols, oo

i, n = symbols("i n")

Sum(i, (i, 1, n)).doit()        # n**2/2 + n/2        -> Gauss, forma cerrada
Sum(i**2, (i, 1, n)).doit()     # n**3/3 + n**2/2 + n/6
Sum(1, (i, 1, n)).doit()        # n                   -> suma de n unos
Sum(1/i**2, (i, 1, oo)).doit()  # pi**2/6             -> serie de Basilea
```

## Sumas con limite infinito (series)

Con `b = oo`, `.doit()` evalua la **serie** si converge a un valor conocido:

```python
from sympy import Sum, symbols, oo, Rational

i = symbols("i")

Sum(Rational(1, 2)**i, (i, 0, oo)).doit()   # 2          -> serie geometrica
Sum(1/i**2, (i, 1, oo)).doit()              # pi**2/6
```

## Forma cerrada vs evaluacion numerica

Para una suma finita con limites numericos, `.doit()` devuelve el numero exacto; sobre limite simbolico, la formula:

```python
from sympy import Sum, summation, symbols

i, n = symbols("i n")

Sum(i, (i, 1, 10)).doit()       # 55                  -> numero exacto
Sum(i, (i, 1, n)).doit()        # n**2/2 + n/2        -> formula de Gauss

# summation(...) = atajo de Sum(...).doit()
summation(i, (i, 1, 10))        # 55
summation(i**2, (i, 1, n))      # n**3/3 + n**2/2 + n/6
```

## Atributos clave

| Atributo | Tipo | Significado |
|----------|------|-------------|
| `.function` | `Expr` | El termino general `f(i)` |
| `.limits` | `tuple` | Tupla de limites `((i, a, b), ...)` |
| `.variables` | `list` | Los indices de la suma |

```python
from sympy import Sum, symbols

i, n = symbols("i n")
s = Sum(i**2, (i, 1, n))

s.function   # i**2
s.limits     # ((i, 1, n),)
```

## Errores comunes

| Error | Causa | Solucion |
|-------|-------|----------|
| `Sum(...)` "no suma nada" | El constructor NO evalua, solo representa | Llamar `.doit()` o usar `summation(...)` |
| `.doit()` devuelve la misma `Sum` | No hay forma cerrada conocida | Es esperado; usar limites numericos o `.evalf()` |
| Limites como `(1, n)` sin indice | Falta la variable en la tupla | Forma correcta: `(i, 1, n)` |
| Esperabas un `float` y sale `pi**2/6` | SymPy da el resultado **exacto** | Aplicar `.evalf()` si quieres el decimal |

## Notas relacionadas

- [[Product]]
- [[sympy.calculus/sumatorios/index | sumatorios]]
- [[Rational]]
