---
title: sympy.printing — mostrar y exportar expresiones
tags:
  - sympy
  - indice
draft: false
---

# sympy.printing — mostrar y exportar expresiones

Esta carpeta cubre las formas de **mostrar y exportar** expresiones SymPy fuera del motor
simbolico. Una vez que una expresion existe (`x**2/3 + sqrt(2)`), hay cuatro destinos
posibles: verla bonita en **terminal**, renderizarla como **LaTeX** para un documento,
activar el render **automatico** en Jupyter, o traducirla a **codigo ejecutable** en C o
Python. Cada herramienta tiene un destino distinto y no se solapan.

El flujo tipico de trabajo es lineal:

```python
from sympy import symbols, sqrt, diff, pprint, latex, init_printing, ccode, pycode

x = symbols("x")
expr = x**2 / 3 + sqrt(2)

# 1. Cadena lineal (repr por defecto de SymPy)
print(expr)          # x**2/3 + sqrt(2)

# 2. Terminal bonita con pprint
pprint(expr)
#  2
# x       ___
# ── + ╲╱ 2
#  3

# 3. String LaTeX para un documento
latex(expr)          # '\\frac{x^{2}}{3} + \\sqrt{2}'

# 4. Codigo C o Python ejecutable
ccode(expr)          # 'pow(x, 2)/3 + sqrt(2)'
pycode(expr)         # 'x**2/3 + math.sqrt(2)'
```

## Como se relacionan

La decision clave: **quien consume la salida** — un humano leyendo una terminal, un
compilador de LaTeX, un notebook Jupyter, o un compilador de C/interprete Python.

| Herramienta | Destino | Devuelve | Cuando usarla |
|-------------|---------|---------|---------------|
| [[sympy.pprint]] | Terminal / consola | `None` (imprime a stdout) | Ver expresiones en sesion interactiva de terminal; fracciones y radicales legibles |
| [[sympy.latex]] | Documento LaTeX / Jupyter manual | `str` LaTeX | Generar codigo LaTeX para pegar en articulo, presentacion o celda Jupyter |
| [[sympy.init_printing]] | Jupyter / IPython (render automatico) | `None` (configura entorno) | Llamar una vez al inicio del notebook para que todo se muestre bonito sin esfuerzo |
| [[sympy.ccode_pycode]] | Compilador C o interprete Python | `str` codigo fuente | Traducir expresiones simbolicas a codigo de produccion o simulacion numerica |

Arbol de decision:

- ¿Trabajas en **Jupyter** y quieres cero friccion? → [[sympy.init_printing]] una vez al inicio.
- ¿Estas en **terminal** y quieres leer la expresion ahora? → [[sympy.pprint]].
- ¿Necesitas el **string LaTeX** para un documento o para construir otro texto? → [[sympy.latex]].
- ¿Quieres **codigo ejecutable** rapido a partir de tu derivada o integral simbolica? → [[sympy.ccode_pycode]].

> [!info] print vs pprint vs latex
> `print(expr)` llama a `str(expr)`: devuelve la representacion lineal de SymPy, siempre
> disponible pero sin estructura 2-D. `pprint` dibuja la estructura matematica en la
> terminal. `latex` genera el markup tipografico. Los tres coexisten y se usan en contextos
> distintos.

## Notas

- [[sympy.pprint]] — impresion **bonita en terminal** (ASCII/Unicode); fracciones apiladas,
  radicales dibujados, exponentes superindice. No retorna nada.
- [[sympy.latex]] — convierte la expresion a un **string LaTeX**; listo para documentos,
  notebooks o cualquier sistema que renderice LaTeX. Retorna `str`.
- [[sympy.init_printing]] — activa el render **automatico** en Jupyter/IPython; llamar una
  vez al inicio de la sesion para no tener que llamar `pprint`/`latex` manualmente.
- [[sympy.ccode_pycode]] — genera **codigo C** (`ccode`) o **codigo Python** (`pycode`) a
  partir de la expresion; el puente desde la manipulacion simbolica hacia la ejecucion
  numerica eficiente.

## Notas relacionadas

- [[SymPy/index | SymPy]]
