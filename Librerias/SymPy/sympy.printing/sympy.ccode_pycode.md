---
title: sympy.ccode / sympy.pycode — generar codigo C y Python desde expresiones
aliases:
  - ccode
  - pycode
  - code generation
tags:
  - sympy
  - api/funcion
  - printing
lib: sympy
mod: sympy.printing
tipo: concepto
requiere:
  - symbols
draft: false
---

# sympy.ccode / sympy.pycode — generar codigo C y Python desde expresiones

`ccode(expr)` y `pycode(expr)` traducen una expresion SymPy a **codigo fuente ejecutable**:
`ccode` genera una cadena de C valida; `pycode` genera una cadena de Python valida usando el
modulo `math` de la biblioteca estandar. Son el puente entre el mundo **simbolico** (donde se
deriva, simplifica y manipula) y el mundo **numerico** (donde se ejecuta rapido en produccion
o se compila).

El flujo tipico es: definir y manipular simbolicamente → simplificar → `ccode`/`pycode` →
pegar en codigo de produccion o generar archivos `.c`/`.py`. Para una alternativa de mayor
nivel que genera funciones ejecutables directamente ver `lambdify`.

## Firma

```python
sympy.ccode(
    expr,              # Expr: la expresion a traducir
    assign_to=None,    # str | None: si se indica, genera "assign_to = <expr>;"
    standard='c99',    # str: estandar C objetivo ('c89', 'c99', 'c11')
    **settings,
) -> str

sympy.pycode(
    expr,              # Expr: la expresion a traducir
    **settings,
) -> str
```

## Valor de retorno

| Funcion | Tipo | Ejemplo de salida |
|---------|------|-------------------|
| `ccode(sin(x) + x**2)` | `str` | `'sin(x) + pow(x, 2)'` |
| `ccode(expr, assign_to='y')` | `str` | `'y = sin(x) + pow(x, 2);'` |
| `pycode(sin(x))` | `str` | `'math.sin(x)'` |
| `pycode(x**2 + 1)` | `str` | `'x**2 + 1'` |

## Casos de uso

### Conversion basica

```python
from sympy import symbols, sin, sqrt, ccode, pycode

x = symbols("x")

ccode(sin(x) + x**2)          # 'sin(x) + pow(x, 2)'
ccode(sqrt(x))                # 'sqrt(x)'
pycode(sin(x))                # 'math.sin(x)'
pycode(x**2 + 1)              # 'x**2 + 1'
```

### Generar una asignacion completa en C

```python
from sympy import symbols, sin, ccode

x = symbols("x")
expr = sin(x)**2 + x

ccode(expr, assign_to='resultado')  # 'resultado = pow(sin(x), 2) + x;'
```

### Flujo simbolico → numerico: derivar y luego codificar

```python
from sympy import symbols, sin, diff, ccode, pycode

x = symbols("x")
f = sin(x) * x**2

df = diff(f, x)               # x**2*cos(x) + 2*x*sin(x)

ccode(df)    # 'pow(x, 2)*cos(x) + 2*x*sin(x)'
pycode(df)   # 'x**2*math.cos(x) + 2*x*math.sin(x)'
```

### Expresion racional

```python
from sympy import symbols, Rational, ccode, pycode

x = symbols("x")
expr = x**2 / 3

ccode(expr)    # 'pow(x, 2)/3'
pycode(expr)   # 'x**2/3'
```

## Diferencias clave entre ccode y pycode

| Aspecto | `ccode` | `pycode` |
|---------|---------|---------|
| Potencias | `pow(x, 2)` | `x**2` |
| Funciones matematicas | `sin(x)`, `sqrt(x)` (libc) | `math.sin(x)`, `math.sqrt(x)` |
| Asignacion | `assign_to='y'` → `y = expr;` | No disponible directamente |
| Estandar configurable | `standard='c99'` \| `'c89'` | No aplica |
| Salida lista para | Compilador C | Interprete Python + `import math` |

## Errores comunes

| Error | Causa | Solucion |
|-------|-------|----------|
| Salida contiene `Not supported in C` | La expresion usa operaciones sin equivalente en C (p. ej. `zoo`, `oo`) | Limpiar la expresion antes o usar `pycode` |
| `pycode` no genera `import math` | La funcion solo genera la expresion | Agregar `import math` manualmente al script destino |
| Confundir `ccode` con `lambdify` | `ccode` genera texto; `lambdify` genera una funcion Python callable | Usar `lambdify` si se quiere ejecutar directamente desde Python |

## Limitaciones

- Ambas funciones generan **texto**, no codigo ejecutable. Para obtener una funcion Python
  directamente usar `lambdify(x, expr, 'numpy')`.
- `ccode` no genera un archivo `.c` completo con `#include` ni `main()`; solo la expresion.
- Expresiones con simbolos indefinidos o constantes especiales (`oo`, `zoo`) pueden generar
  codigo invalido o advertencias.
- Para Fortran, JavaScript, Julia y otros idiomas existen funciones analogas: `fcode`,
  `jscode`, `julia_code`.

## Notas relacionadas

- [[sympy.latex]]
- [[sympy.pprint]]
- [[sympy.printing/index | sympy.printing]]
- [[Tree SymPy]]
