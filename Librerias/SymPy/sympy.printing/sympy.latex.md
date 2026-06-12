---
title: sympy.latex — convertir una expresion a string LaTeX
aliases:
  - latex
  - sympy latex
tags:
  - sympy
  - api/funcion
  - printing
lib: sympy
mod: sympy.printing
tipo: funcion
retorna: str
requiere: []
draft: false
---

# sympy.latex — convertir una expresion a string LaTeX

`latex(expr)` convierte cualquier expresion SymPy en una **cadena de texto LaTeX** lista para
pegar en un documento, en un notebook Jupyter o en una presentacion. Devuelve un `str`; no
imprime nada por si misma. El resultado es matematicamente equivalente a la expresion
original: `Rational(1, 3)` se convierte en `'\\frac{1}{3}'`, `sqrt(x)` en `'\\sqrt{x}'`,
matrices en entornos `pmatrix`, etc.

Es la herramienta de exportacion cuando el destino final no es la terminal sino un documento
tipografico. Para mostrar directamente en Jupyter sin llamar `latex` a mano, ver
[[sympy.init_printing]].

## Firma

```python
sympy.latex(
    expr,                  # Expr | Matrix | cualquier objeto SymPy
    mode='plain',          # str: 'plain' | 'inline' | 'equation' | 'equation*'
    itex=False,            # bool: generar formato iTeX (para ciertas wikis)
    fold_frac_powers=False,# bool: escribir x^{1/2} en lugar de sqrt{x}
    fold_short_frac=None,  # bool | None: fracciones cortas como a/b en vez de \frac
    mul_symbol=None,       # str | None: simbolo para multiplicacion ('dot', 'times', None)
    inv_trig_style='abbreviated', # str: 'abbreviated' | 'full' | 'power'
    mat_str=None,          # str | None: entorno LaTeX para matrices ('pmatrix', 'bmatrix', ...)
    **settings,
) -> str
```

## Valor de retorno

| Tipo | Significado |
|------|-------------|
| `str` | Cadena LaTeX **sin delimitadores** en modo `'plain'` (por defecto) |
| `str` | Cadena envuelta en `$...$` si `mode='inline'` |
| `str` | Cadena envuelta en `$$...$$` si `mode='equation'` |

## Formas basicas de llamada

| Objetivo | Llamada |
|----------|---------|
| String LaTeX plano | `latex(expr)` |
| Listo para inline `$...$` | `latex(expr, mode='inline')` |
| Listo para display `$$...$$` | `latex(expr, mode='equation')` |
| Matrices con corchetes | `latex(M, mat_str='bmatrix')` |
| Multiplicacion con punto | `latex(expr, mul_symbol='dot')` |

## Casos de uso

### Expresiones algebraicas basicas

```python
from sympy import symbols, sqrt, Rational, latex

x = symbols("x")
latex(x**2 / 3 + sqrt(2))    # '\\frac{x^{2}}{3} + \\sqrt{2}'
latex(Rational(1, 3))         # '\\frac{1}{3}'
latex(x**2 / 3, mode='equation')  # '$$\\frac{x^{2}}{3}$$'
```

### Funciones trigonometricas e integrales

```python
from sympy import symbols, sin, cos, integrate, latex

x = symbols("x")
latex(sin(x) * cos(x))        # '\\sin{\\left(x \\right)} \\cos{\\left(x \\right)}'
latex(integrate(sin(x), x))   # '- \\cos{\\left(x \\right)}'
```

### Matrices

```python
from sympy import Matrix, latex

M = Matrix([[1, 2], [3, 4]])
latex(M)                       # '\\left[\\begin{matrix}1 & 2\\\\3 & 4\\end{matrix}\\right]'
latex(M, mat_str='bmatrix')    # usa entorno bmatrix
```

### Multiplicacion con simbolo explicito

```python
from sympy import symbols, latex

x, y = symbols("x y")
latex(2 * x * y, mul_symbol='times')  # '2 x \\times y'
latex(2 * x * y, mul_symbol='dot')    # '2 x \\cdot y'
```

## Errores comunes

| Error | Causa | Solucion |
|-------|-------|----------|
| Copiar la cadena cruda y ver `\\frac` con doble barra | Python escapa las `\` en `repr` | Usar `print(latex(expr))` para ver la cadena real |
| Resultado no renderiza en LaTeX externo | Faltan delimitadores `$...$` | Usar `mode='inline'` o `mode='equation'` |
| Matrices con entorno inesperado | `mat_str` por defecto es `'matrix'` | Especificar `mat_str='pmatrix'` o `'bmatrix'` segun el documento |

## Limitaciones

- `latex` convierte; no simplifica. Encadenar `simplify(expr)` antes si la forma importa.
- Algunas expresiones muy complejas generan LaTeX valido pero difici de leer; en esos casos
  puede valer la pena reestructurar la expresion primero.
- Para codigo ejecutable (no LaTeX) usar [[sympy.ccode_pycode]].

## Notas relacionadas

- [[sympy.pprint]]
- [[sympy.init_printing]]
- [[sympy.ccode_pycode]]
- [[sympy.printing/index | sympy.printing]]
