---
title: sympy.init_printing — activar render bonito automatico
aliases:
  - init_printing
  - iniciar impresion
tags:
  - sympy
  - api/funcion
  - printing
lib: sympy
mod: sympy.printing
tipo: funcion
retorna: None
requiere: []
draft: false
---

# sympy.init_printing — activar render bonito automatico

`init_printing()` configura el entorno interactivo (Jupyter, IPython o terminal) para que
**todas las expresiones SymPy se muestren automaticamente en su forma mas legible** sin
necesidad de llamar a [[sympy.pprint]] o [[sympy.latex]] de forma explicita en cada celda.
En Jupyter activa el render LaTeX nativo del notebook; en IPython/terminal activa el
pretty-printer Unicode de SymPy.

Se llama **una sola vez al inicio** del notebook o sesion. Tras esa llamada, cualquier
expresion que sea el ultimo valor de una celda se renderiza bonita.

## Firma

```python
sympy.init_printing(
    pretty_print=True,     # bool: activar pprint en terminal
    order=None,            # str | None: orden de los terminos ('grlex', 'rev-lex', ...)
    use_unicode=None,      # bool | None: forzar Unicode en terminal
    use_latex=None,        # bool | None | 'mathjax' | 'svg': modo LaTeX en Jupyter
    wrap_line=None,        # bool | None: partir lineas largas en pprint
    num_columns=None,      # int | None: ancho maximo para pprint
    no_global=False,       # bool: si True, no modifica el estado global
    ip=None,               # InteractiveShell | None: instancia IPython (raramente necesario)
) -> None
```

## Valor de retorno

| Tipo | Significado |
|------|-------------|
| `None` | Configura el estado global del pretty-printer; no retorna nada |

## Formas basicas de llamada

| Objetivo | Llamada |
|----------|---------|
| Activar todo (Jupyter + terminal) | `init_printing()` |
| Solo terminal con Unicode | `init_printing(use_latex=False)` |
| Solo LaTeX en Jupyter | `init_printing(pretty_print=False, use_latex=True)` |
| Fijar ancho en terminal | `init_printing(num_columns=80)` |

## Casos de uso

### Inicio tipico de un notebook Jupyter

```python
from sympy import init_printing, symbols, sqrt, Rational

init_printing()            # llamar una vez; sin argumentos es suficiente en Jupyter

x = symbols("x")
x**2 / 3 + sqrt(2)        # la celda muestra LaTeX renderizado automaticamente
```

### Sesion de terminal / IPython

```python
from sympy import init_printing, symbols, sin

init_printing(use_latex=False, use_unicode=True)

x = symbols("x")
sin(x) / x
# IPython muestra:
# sin(x)
# ──────
#   x
```

### Desactivar el render automatico temporalmente

```python
from sympy import init_printing, pprint, symbols

init_printing(pretty_print=False, use_latex=False)

x = symbols("x")
x**2 + 1    # muestra la representacion lineal: x**2 + 1
# Para ver bonito manualmente:
pprint(x**2 + 1)
```

## Errores comunes

| Error | Causa | Solucion |
|-------|-------|----------|
| Llamar `init_printing()` en cada celda | Redundante; modifica el estado global cada vez | Llamar solo en la primera celda del notebook |
| Expresiones no se renderizan en Jupyter | `use_latex` quedo en `False` o IPython no esta disponible | Llamar sin argumentos o con `use_latex=True` |
| Salida cambia de aspecto inesperadamente | `init_printing` fue llamada con parametros distintos en otro modulo | Revisar si algun import llama `init_printing` internamente |

## Limitaciones

- Modifica el **estado global** de SymPy; en scripts de produccion (no interactivos) puede
  generar efectos colaterales. Preferir `pprint` o `latex` explicitos en ese contexto.
- La calidad del render LaTeX en Jupyter depende del backend de MathJax disponible en el
  entorno, no de SymPy.
- No afecta la salida de `str(expr)` ni `repr(expr)`; solo el display interactivo.

## Notas relacionadas

- [[sympy.pprint]]
- [[sympy.latex]]
- [[sympy.printing/index | sympy.printing]]
