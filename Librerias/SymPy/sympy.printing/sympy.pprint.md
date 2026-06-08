---
title: sympy.pprint — impresion bonita en terminal (ASCII/Unicode)
aliases:
  - pprint
  - pretty print
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

# sympy.pprint — impresion bonita en terminal (ASCII/Unicode)

`pprint(expr)` imprime una expresion SymPy en la terminal como **texto formateado de dos
dimensiones**: las fracciones se apilan verticalmente, las raices se dibujan con radicales y
los exponentes aparecen como superindices ASCII o Unicode. El resultado es visualmente
similar a como se escribe en papel, lo que facilita leer expresiones complejas sin necesidad
de un entorno grafico. **No devuelve nada**: escribe directamente a `stdout`. Para obtener la
representacion como cadena usar [[sympy.pretty]] (si se necesita capturar el texto).

La diferencia critica con `print(expr)`: `print` muestra la cadena lineal de SymPy
(`x**2/3 + sqrt(2)`), mientras que `pprint` dibuja la estructura matematica en 2-D.

## Firma

```python
sympy.pprint(
    expr,                  # Expr: la expresion a mostrar
    num_columns=None,      # int | None: ancho maximo en columnas
    use_unicode=True,      # bool: usar caracteres Unicode (recomendado en terminales modernas)
    wrap_line=True,        # bool: si True, divide lineas largas
    root_notation=True,    # bool: si True, dibuja n-esimas raices con radical
    settings=None,         # dict | None: opciones extra del pretty-printer
) -> None
```

## Valor de retorno

| Tipo | Significado |
|------|-------------|
| `None` | Imprime a `stdout`; no retorna nada. Para capturar el resultado usar `sympy.pretty(expr)` |

## Formas basicas de llamada

| Objetivo | Llamada |
|----------|---------|
| Imprimir con Unicode (modo por defecto) | `pprint(expr)` |
| Forzar ASCII puro (terminal sin Unicode) | `pprint(expr, use_unicode=False)` |
| Limitar ancho de salida | `pprint(expr, num_columns=60)` |
| Imprimir sin partir lineas largas | `pprint(expr, wrap_line=False)` |

## Casos de uso

### Visualizar una expresion algebraica

```python
from sympy import symbols, sqrt, Rational, pprint

x = symbols("x")
expr = x**2 / 3 + sqrt(2)

print(expr)    # x**2/3 + sqrt(2)   -> cadena lineal
pprint(expr)
# Salida a stdout:
#  2
# x       ___
# ── + ╲╱ 2
#  3
```

### Fraccion y potencia anidada

```python
from sympy import symbols, pprint

x = symbols("x")
pprint((x + 1) / (x**2 - 1))
# Salida:
#   x + 1
# ────────
#  2
# x  - 1
```

### Modo ASCII puro

```python
from sympy import symbols, sqrt, pprint

x = symbols("x")
pprint(sqrt(x + 1), use_unicode=False)
# Salida:
#   ________
# \/ x + 1
```

## Errores comunes

| Error | Causa | Solucion |
|-------|-------|----------|
| Asignar `result = pprint(expr)` y esperar texto | `pprint` retorna `None` | Usar `sympy.pretty(expr)` para capturar la cadena |
| Salida ilegible en terminal antigua | Unicode no soportado | Llamar con `use_unicode=False` |
| Lineas que desbordan la terminal | `wrap_line=True` por defecto puede partir mal | Ajustar `num_columns` al ancho real de la terminal |

## Limitaciones

- Solo sirve para visualizar en texto plano; para entornos Jupyter usar [[sympy.init_printing]].
- No hay forma de controlar el color de la salida; `pprint` solo usa caracteres de texto.
- Para exportar a LaTeX ver [[sympy.latex]].

## Notas relacionadas

- [[sympy.latex]]
- [[sympy.init_printing]]
- [[sympy.printing/index | sympy.printing]]
- [[Tree SymPy]]
