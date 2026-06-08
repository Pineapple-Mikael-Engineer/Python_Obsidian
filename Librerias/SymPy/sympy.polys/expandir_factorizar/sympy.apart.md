---
title: sympy.apart — descomposicion en fracciones parciales
aliases:
  - apart
  - sympy.apart
  - fracciones parciales
tags:
  - sympy
  - api/funcion
  - polys/expandir_factorizar
lib: sympy
mod: sympy
tipo: funcion
retorna: Expr
requiere:
  - Symbol
draft: false
---

# sympy.apart — descomposicion en fracciones parciales

`apart(expr)` descompone una **fraccion racional** en suma de **fracciones parciales**: separa una fraccion con denominador factorizable en la suma de fracciones mas simples, una por cada factor del denominador. Convierte `1/(x**2 - 1)` en `-1/(2*(x + 1)) + 1/(2*(x - 1))`. Es la operacion **inversa** de [[sympy.together]] (que recombina las fracciones en una sola) y la herramienta clasica para preparar una integral de una funcion racional o para analizar polos por separado.

> `apart` **separa** una fraccion en sumandos y `together` los **vuelve a unir** en una sola fraccion: son inversas. `together(apart(f))` recupera la fraccion original.

## Firma

```python
sympy.apart(
    f,                   # Expr: fraccion racional a descomponer
    x=None,              # Symbol: variable principal (se deduce si hay una sola)
    full=False,          # bool: True -> usa raices complejas/RootSum (denominadores no factorizables sobre Q)
    ...
) -> Expr
```

## Valor de retorno

| Tipo | Forma | Significado |
|------|-------|-------------|
| `Expr` | suma de fracciones | La descomposicion en fracciones parciales (un sumando por factor del denominador) |

Si la expresion no es una fraccion descomponible, la devuelve sin cambios.

```python
from sympy import symbols, apart
x = symbols("x")
apart(1/(x**2 - 1))       # -1/(2*(x + 1)) + 1/(2*(x - 1))
```

## Formas basicas de llamada

| Objetivo | Llamada |
|----------|---------|
| Descomponer una fraccion | `apart(1/(x**2 - 1))` |
| Indicar la variable | `apart(expr, x)` |
| Con numerador no trivial | `apart((x + 2)/(x**2 + x))` |
| Forzar uso de raices complejas | `apart(expr, full=True)` |

## Parametros en detalle

### `f` (obligatorio)

La fraccion racional a descomponer. SymPy factoriza el denominador sobre **Q** y reparte el numerador entre un sumando por cada factor.

```python
from sympy import symbols, apart
x = symbols("x")
apart(1/(x**2 - 1))           # -1/(2*(x + 1)) + 1/(2*(x - 1))
apart((x + 2)/(x**2 + x))     # -1/(x + 1) + 2/x
```

### `x`

La variable principal respecto a la cual descomponer. Es **opcional** si la expresion tiene una sola variable, pero conviene indicarla cuando hay parametros para no descomponer respecto al simbolo equivocado.

```python
from sympy import symbols, apart
x = symbols("x")
apart(1/(x*(x + 1)), x)       # -1/(x + 1) + 1/x
```

### `full`

Por defecto `apart` solo separa segun la factorizacion sobre **Q**. Con `full=True` usa tambien las **raices complejas** del denominador (via `RootSum`), descomponiendo factores que sobre los racionales quedaban irreducibles. Suele requerir luego `.doit()` para materializar la suma.

## Casos de uso

### Preparar una integral de funcion racional

La integral de una fraccion racional se vuelve trivial tras descomponerla: cada `1/(x - r)` integra a un logaritmo.

```python
from sympy import symbols, apart, integrate
x = symbols("x")
apart(1/(x**2 - 1))                  # -1/(2*(x + 1)) + 1/(2*(x - 1))
integrate(1/(x**2 - 1), x)           # log(x - 1)/2 - log(x + 1)/2
```

### Separar polos de una funcion de transferencia

Cada fraccion parcial corresponde a un polo aislado, util para analizar la respuesta de un sistema termino a termino.

```python
from sympy import symbols, apart
s = symbols("s")
apart((s + 3)/(s**2 + 3*s + 2))      # -1/(s + 2) + 2/(s + 1)
```

## Errores comunes

| Error | Causa | Solucion |
|-------|-------|----------|
| `apart` deja la fraccion igual | El denominador no factoriza sobre Q | Probar `full=True` para usar raices complejas |
| Descomponer respecto al simbolo equivocado | Varias variables y no se indico cual | Pasar la variable: `apart(expr, x)` |
| Esperar una sola fraccion de vuelta | `apart` separa, no combina | Usar [[sympy.together]] para el camino inverso |
| Resultado con `RootSum` sin evaluar | `full=True` deja la suma simbolica | Aplicar `.doit()` al resultado |

## Notas relacionadas

- [[sympy.together]]
- [[sympy.factor]]
- [[sympy.cancel]]
- [[sympy.polys/expandir_factorizar/index | expandir_factorizar]]
