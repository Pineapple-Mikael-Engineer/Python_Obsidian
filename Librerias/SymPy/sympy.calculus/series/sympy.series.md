---
title: sympy.series — desarrollo en serie de Taylor/potencias de una expresion
aliases:
  - series
  - sympy.series
  - serie de Taylor
tags:
  - sympy
  - api/funcion
  - calculus/series
lib: sympy
mod: sympy.series
tipo: funcion
retorna: Expr
requiere:
  - Symbol
draft: false
---

# sympy.series — desarrollo en serie de Taylor/potencias de una expresion

Calcula el **desarrollo en serie de potencias** (Taylor) de una expresion `f` alrededor de un punto `x0`, hasta el orden pedido `n`. Devuelve una `Expr` con la suma de los primeros terminos mas un **termino de orden** `O(x**n)` que representa el resto truncado. Si la expresion tiene un polo en `x0` (p. ej. `1/x`), produce una **serie de Laurent** con potencias negativas. Es la herramienta tipica para aproximar localmente una funcion, linealizar un modelo o calcular limites delicados. Existe tambien la forma metodo `f.series(...)`, equivalente.

> [!info] Exactitud simbolica
> Los coeficientes son **exactos** (`x**3/6`, no `0.1666...`). Para evaluar la aproximacion sobre numeros conviene primero quitar el resto con `.removeO()` y luego compilar con [[sympy.lambdify]].

## Firma

```python
sympy.series(
    expr,        # Expr: expresion a desarrollar
    x=None,      # Symbol: variable del desarrollo (si hay una sola, se infiere)
    x0=0,        # valor: punto alrededor del cual se expande (puede ser oo)
    n=6,         # int | None: orden del corte; el resto es O((x-x0)**n)
    dir="+",     # str: lado de aproximacion en x0 ("+" derecha, "-" izquierda)
) -> Expr
```

## Valor de retorno

| Aspecto | Detalle |
|---------|---------|
| Tipo | `Expr` (suma de terminos + un termino `O(...)`) |
| Contenido | Coeficientes exactos hasta grado `n-1` |
| Termino `O` | `O((x-x0)**n)`: marca el orden del resto despreciado |
| Laurent | Si hay polo en `x0`, aparecen potencias negativas (`1/x`, ...) |

```python
from sympy import symbols, exp
x = symbols("x")
exp(x).series(x, 0, 5)    # 1 + x + x**2/2 + x**3/6 + x**4/24 + O(x**5)
```

## Formas basicas de llamada

| Objetivo | Llamada |
|----------|---------|
| Maclaurin (en 0) hasta orden 6 | `series(f, x)` |
| Orden concreto | `series(f, x, 0, n)` |
| Alrededor de otro punto `x0` | `series(f, x, x0, n)` |
| Forma metodo (equivalente) | `f.series(x, x0, n)` |
| Quitar el resto `O(...)` | `f.series(x, 0, n).removeO()` |
| Serie en el infinito | `series(f, x, oo, n)` |

## Parametros en detalle

### `expr`

Expresion a desarrollar. SymPy elige automaticamente entre serie de Taylor (si `expr` es regular en `x0`) o **Laurent** (si tiene un polo): en ese caso el resultado incluye potencias negativas.

```python
from sympy import symbols, sin, cot, series
x = symbols("x")
sin(x).series(x, 0, 8)      # x - x**3/6 + x**5/120 - x**7/5040 + O(x**8)
series(cot(x), x, 0, 4)     # 1/x - x/3 - x**3/45 + O(x**4)   -> Laurent (polo en 0)
```

### `x`

Variable respecto a la cual se desarrolla. Si la expresion tiene una unica variable libre puede omitirse; con varias es **obligatoria** para resolver la ambiguedad.

### `x0`

Punto del desarrollo. Por defecto `0` (serie de Maclaurin). Con otro valor, las potencias aparecen como `(x - x0)`. Admite `oo` para el comportamiento asintotico.

```python
from sympy import symbols, exp, series
x = symbols("x")
series(exp(x), x, 1, 3)     # E + E*(x - 1) + E*(x - 1)**2/2 + O((x - 1)**3, (x, 1))
```

### `n`

Orden del corte: se incluyen terminos hasta grado `n-1` y se anota el resto como `O((x-x0)**n)`. Subirlo da mas terminos a mayor coste; pasar `n=None` devuelve un **generador** perezoso de terminos en lugar de una suma truncada.

```python
from sympy import symbols, series
x = symbols("x")
series(1/(1-x), x, 0, 5)    # 1 + x + x**2 + x**3 + x**4 + O(x**5)   -> geometrica
```

### `dir`

Lado desde el que se aproxima a `x0` (`"+"` por la derecha, `"-"` por la izquierda). Solo importa en puntos donde la expresion no es simetrica (ramas, valores absolutos, logaritmos).

## El termino de orden y `.removeO()`

El sumando `O(x**n)` no es un numero: es un **simbolo de Landau** que indica "mas terminos de orden ≥ n". Mientras este presente, la expresion no es un polinomio evaluable. Para obtener el **polinomio de aproximacion** se elimina con `.removeO()`.

```python
from sympy import symbols, exp
x = symbols("x")
aprox = exp(x).series(x, 0, 5)
aprox                 # 1 + x + x**2/2 + x**3/6 + x**4/24 + O(x**5)
aprox.removeO()       # x**4/24 + x**3/6 + x**2/2 + x + 1   -> ya es polinomio
```

## Casos de uso

### Linealizar un modelo (aproximacion de primer orden)

```python
from sympy import symbols, sin, series
x = symbols("x")
series(sin(x), x, 0, 2).removeO()    # x   -> sin(x) ≈ x para x pequeño
```

### Comparar la aproximacion con la funcion exacta

El patron tipico: desarrollar simbolico, quitar el resto y compilar a numerico.

```python
import numpy as np
from sympy import symbols, exp, lambdify
x = symbols("x")
p = exp(x).series(x, 0, 4).removeO()   # 1 + x + x**2/2 + x**3/6
f = lambdify(x, p, "numpy")
f(np.array([0.0, 0.5]))                # array([1., 1.6458333])  -> aprox de exp
```

### Serie de log y de funciones trigonometricas

```python
from sympy import symbols, log, tan, series
x = symbols("x")
series(log(1 + x), x, 0, 5)    # x - x**2/2 + x**3/3 - x**4/4 + O(x**5)
tan(x).series(x, 0, 6)         # x + x**3/3 + 2*x**5/15 + O(x**6)
```

## Errores comunes

| Error | Causa | Solucion |
|-------|-------|----------|
| Tratar el resultado como polinomio | sigue presente el termino `O(...)` | aplicar `.removeO()` antes de evaluar |
| `ValueError` sobre la variable | varias variables libres y no se indico `x` | pasar `x` explicito: `series(f, x, 0, n)` |
| Aparecen `1/x`, `1/x**2` inesperados | la expresion tiene un polo en `x0` (Laurent) | es correcto; elegir otro `x0` si se quiere Taylor |
| Pocos terminos | `n` por defecto es 6 (grado ≤ 5) | subir `n` al orden deseado |
| Resultado raro en un punto con rama | `dir` por defecto `"+"` | fijar `dir="-"` segun el lado |

## Limitaciones

- El resultado **incluye** el termino `O(...)`; no es directamente numerico hasta usar `.removeO()`.
- No toda expresion admite desarrollo en un punto dado (singularidades esenciales, no analiticidad).
- Para series formales con coeficientes generales o productos de series, ver utilidades de `sympy.series.formal`.

## Notas relacionadas

- [[sympy.fourier_series]]
- [[sympy.lambdify]]
- [[sympy.calculus/series/index | series]]
