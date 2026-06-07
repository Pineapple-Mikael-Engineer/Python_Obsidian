---
title: sympy.powsimp — combinar potencias de la misma base o exponente
aliases:
  - powsimp
  - sympy.powsimp
  - combinar potencias
tags:
  - sympy
  - api/funcion
  - simplify/trig_y_radicales
lib: sympy
mod: sympy.simplify
tipo: funcion
retorna: Expr
requiere:
  - Symbol
draft: false
---

# sympy.powsimp — combinar potencias de la misma base o exponente

`powsimp(expr)` **combina potencias** que comparten base o exponente usando las leyes de los exponentes: junta `x**a * x**b` en `x**(a + b)` (misma base) y `x**a * y**a` en `(x*y)**a` (mismo exponente). Es el simplificador **especializado** en potencias y exponenciales, el contrapunto del `simplify` general cuando lo unico que quieres es agrupar exponentes. El caso canonico es `powsimp(x**a * x**b)` que devuelve `x**(a + b)`. Por defecto solo combina cuando la transformacion es valida **sin supuestos**; con `force=True` la aplica aunque las bases o los exponentes no garanticen la igualdad.

> `powsimp` **junta** potencias. La operacion **inversa**, que las separa (`x**(a + b) -> x**a * x**b`), es `expand_power_exp` (equivalente a `expand(..., power_exp=True)`): una contrae exponentes, la otra los reparte.

## Firma

```python
sympy.powsimp(
    expr,                # Expr: expresion con potencias a combinar
    deep=False,          # bool: aplicar tambien en subexpresiones anidadas
    combine="all",       # str: "all" | "exp" (misma base) | "base" (mismo exponente)
    force=False,         # bool: combinar aunque falten supuestos que lo garanticen
) -> Expr
```

## Valor de retorno

| Tipo | Forma | Significado |
|------|-------|-------------|
| `Expr` | expresion con potencias agrupadas | La misma expresion con los exponentes combinados segun `combine` |

Si no hay potencias que combinar, devuelve la expresion **sin cambios**.

```python
from sympy import symbols, powsimp
x, a, b = symbols("x a b")
powsimp(x**a * x**b)   # x**(a + b)
```

## Formas basicas de llamada

| Objetivo | Llamada |
|----------|---------|
| Sumar exponentes de la misma base | `powsimp(x**a * x**b)` |
| Combinar exponenciales | `powsimp(exp(x)*exp(y))` |
| Juntar mismo exponente (con supuestos) | `powsimp(x**a * y**a)` |
| Forzar la combinacion | `powsimp(x**a * y**a, force=True)` |
| Solo misma base | `powsimp(expr, combine="exp")` |

## Parametros en detalle

### `expr` (obligatorio)

La expresion cuyas potencias se quieren combinar. Junta exponentes de la misma base de forma incondicional (siempre es valido).

```python
from sympy import symbols, powsimp
x, a, b = symbols("x a b")
powsimp(x**a * x**b)   # x**(a + b)
powsimp(x**2 * x**3)   # x**5
```

Tambien combina **exponenciales** de la misma base:

```python
from sympy import symbols, powsimp, exp
x, y = symbols("x y")
powsimp(exp(x)*exp(y))   # exp(x + y)
```

### `force=True`

Combinar potencias de **distinta base** con el mismo exponente (`x**a * y**a -> (x*y)**a`) solo es valido bajo supuestos (p.ej. bases positivas). Sin `force`, `powsimp` deja la expresion intacta para no introducir un cambio incorrecto; con `force=True` la aplica de todos modos.

```python
from sympy import symbols, powsimp
x, y, a = symbols("x y a")
powsimp(x**a * y**a)              # x**a*y**a   (sin cambios: faltan supuestos)
powsimp(x**a * y**a, force=True)  # (x*y)**a
```

Para evitar `force`, declarar las bases positivas hace la combinacion segura sin forzar:

```python
from sympy import symbols, powsimp
p, q, a = symbols("p q a", positive=True)
powsimp(p**a * q**a)   # (p*q)**a
```

### `combine`

Controla **que** se combina: `"exp"` solo junta exponentes de la misma base, `"base"` solo junta bases con el mismo exponente, y `"all"` (por defecto) hace ambas.

```python
from sympy import symbols, powsimp
x, y, a, b = symbols("x y a b")
powsimp(x**a * y**a * x**b, combine="all")   # x**(a + b)*y**a
```

## Casos de uso

### Compactar exponentes tras operar

Multiplicar potencias deja terminos como `x**a * x**b`; `powsimp` los junta en una sola potencia, mas legible y barata de manipular.

```python
from sympy import symbols, powsimp
x, a, b = symbols("x a b")
powsimp(x**a * x**b)   # x**(a + b)
```

### Reunir exponenciales en un solo exp

Util al simplificar productos de exponenciales (frecuente tras resolver EDOs o trabajar con transformadas).

```python
from sympy import symbols, powsimp, exp
x, y = symbols("x y")
powsimp(exp(x)*exp(y))   # exp(x + y)
```

## Errores comunes

| Error | Causa | Solucion |
|-------|-------|----------|
| `x**a * y**a` no se combina | Distinta base: requiere supuestos | Pasar `force=True` o declarar las bases `positive=True` |
| Esperar que **separe** exponentes | `powsimp` junta, no abre | Usar `expand_power_exp` o `expand(..., power_exp=True)` |
| No toca trigonometricas o radicales | `powsimp` solo ataca potencias | Usar [[sympy.trigsimp]] o [[sympy.radsimp]] |
| No combina en subexpresiones | Por defecto `deep=False` | Pasar `deep=True` |

## Notas relacionadas

- [[sympy.trigsimp]]
- [[sympy.radsimp]]
- [[sympy.simplify/trig_y_radicales/index | trig_y_radicales]]
- [[sympy.expand]]
