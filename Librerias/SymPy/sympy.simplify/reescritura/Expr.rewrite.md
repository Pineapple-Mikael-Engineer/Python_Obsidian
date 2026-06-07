---
title: Expr.rewrite — reexpresar una expresion en terminos de otra funcion
aliases:
  - rewrite
  - Expr.rewrite
  - reescritura simbolica
tags:
  - sympy
  - api/metodo
  - simplify/reescritura
lib: sympy
mod: sympy.core
tipo: metodo
obj: Expr
retorna: Expr
requiere:
  - Expr
  - concepto_expr_arbol
draft: false
---

# Expr.rewrite — reexpresar una expresion en terminos de otra funcion

`expr.rewrite(funcion)` reexpresa la expresion usando **otra familia de funciones equivalente**, sin intentar "simplificar": solo cambia la **base de representacion**. Por ejemplo `tan(x).rewrite(cos)` lo deja en terminos de coseno, `cos(x).rewrite(exp)` lo pasa a la forma exponencial de Euler, y `factorial(n).rewrite(gamma)` cambia el factorial por la funcion gamma. El resultado es matematicamente igual al original, pero escrito con otras funciones; devuelve una **expresion NUEVA** (la original no cambia, ver [[concepto_expr_arbol]]).

Es la herramienta para **cambiar de lenguaje** una expresion: util cuando un solver, un integrador o una identidad espera todo en una misma familia (todo en `exp`, todo en `sin`/`cos`, todo en `gamma`). No confundir con [[Expr.subs]] (sustituye simbolos o subexpresiones concretas) ni con `simplify` (busca la forma "mas corta", no una base fija).

> El argumento es la **funcion destino como objeto** (`sin`, `cos`, `exp`, `gamma`, `Piecewise`…), no una cadena de texto: se pasa `expr.rewrite(cos)`, no `expr.rewrite("cos")`.

## Firma

```python
expr.rewrite(
    *args,               # una o varias funciones destino (sin, cos, exp, gamma, ...)
    deep=True,           # bool: reescribir tambien las subexpresiones
    **hints,             # pistas opcionales segun la clase (p.ej. variable de Piecewise)
) -> Expr
```

## Valor de retorno

| Tipo | Significado |
|------|-------------|
| `Expr` | Una expresion **nueva**, equivalente, escrita en terminos de la funcion destino; la original queda intacta |
| `Expr` (sin cambios) | Si la reescritura pedida no esta definida para esa funcion, devuelve la expresion **tal cual**, sin error |

```python
from sympy import symbols, cos, exp
x = symbols("x")
cos(x).rewrite(exp)     # exp(I*x)/2 + exp(-I*x)/2    -> Expr nueva (Euler)
```

## Formas de llamada

| Objetivo | Llamada |
|----------|---------|
| Trig a exponencial (Euler) | `cos(x).rewrite(exp)` |
| Exponencial a trig | `exp(I*x).rewrite(cos)` |
| Una trig en terminos de otra | `tan(x).rewrite(cos)` |
| Factorial a gamma | `factorial(n).rewrite(gamma)` |
| Valor absoluto a a trozos | `Abs(x).rewrite(Piecewise)` |

```python
from sympy import symbols, sin, cos, exp, I, tan, factorial, gamma
x, n = symbols("x n")
sin(x).rewrite(exp)             # -I*(exp(I*x) - exp(-I*x))/2
exp(I*x).rewrite(cos)           # I*sin(x) + cos(x)
tan(x).rewrite(cos)             # cos(x - pi/2)/cos(x)
factorial(n).rewrite(gamma)     # gamma(n + 1)
```

## Parametros en detalle

### funcion destino (`*args`)

Se pasa la **clase de la funcion** a la que se quiere migrar. Las parejas tipicas son trigonometricas <-> exponencial compleja (Euler), trigonometricas entre si, e hiperbolicas/especiales hacia su forma canonica.

```python
from sympy import symbols, cos, exp, I
x = symbols("x")
cos(x).rewrite(exp)     # exp(I*x)/2 + exp(-I*x)/2
exp(I*x).rewrite(cos)   # I*sin(x) + cos(x)   -> camino inverso
```

Si la reescritura no esta definida, no falla: devuelve la entrada sin tocar.

```python
from sympy import symbols, Abs, sqrt
x = symbols("x")
Abs(x).rewrite(sqrt)    # Abs(x)   -> sin regla aplicable, lo deja igual
```

### `Piecewise` y supuestos

`Abs(x).rewrite(Piecewise)` solo produce la forma a trozos cuando el simbolo permite ordenar (p.ej. `real=True`); con un simbolo generico complejo lo deja como `Abs`.

```python
from sympy import symbols, Abs, Piecewise
x = symbols("x", real=True)
Abs(x).rewrite(Piecewise)   # Piecewise((x, x >= 0), (-x, True))
```

### `deep`

Por defecto `deep=True` reescribe tambien las subexpresiones anidadas. Con `deep=False` solo se reescribe el nodo de mas alto nivel.

## Casos de uso

### Llevar todo a forma exponencial para integrar o factorizar

```python
from sympy import symbols, sin, cos, exp, expand
x = symbols("x")
expr = sin(x)**2 + cos(x)**2
expr.rewrite(exp)       # (-I*(exp(I*x) - exp(-I*x))/2)**2 + (exp(I*x)/2 + exp(-I*x)/2)**2
```

### Unificar funciones especiales en gamma

```python
from sympy import symbols, factorial, gamma
n = symbols("n")
factorial(n).rewrite(gamma)     # gamma(n + 1)   -> base comun para combinarlas
```

### Convertir un valor absoluto en una definicion por tramos

```python
from sympy import symbols, Abs, Piecewise
x = symbols("x", real=True)
Abs(x).rewrite(Piecewise)       # Piecewise((x, x >= 0), (-x, True))
```

## Errores comunes

| Error | Causa | Solucion |
|-------|-------|----------|
| `rewrite("cos")` falla o no hace nada | Se paso la funcion como **cadena** en vez de objeto | Pasar la clase: `expr.rewrite(cos)` (importada) |
| La salida no parece "mas simple" | `rewrite` **no** simplifica, solo cambia de base | Encadenar con `simplify`/`trigsimp` si quieres reducir |
| `Abs(x).rewrite(Piecewise)` devuelve `Abs(x)` | El simbolo es generico (complejo); no hay orden | Declarar `symbols("x", real=True)` |
| `rewrite` "no cambia nada" | No hay regla definida hacia esa funcion destino | Probar otra funcion destino o `simplify` |
| Se esperaba sustituir un simbolo | Confundir con `subs` | Para reemplazar simbolos usar [[Expr.subs]] |

## Limitaciones

- `rewrite` cambia la **representacion**, no busca la forma minima: `tan(x).rewrite(cos)` da `cos(x - pi/2)/cos(x)`, que `simplify` puede volver a `tan(x)`.
- No toda funcion admite reescritura hacia cualquier otra; si no hay regla, devuelve la expresion sin avisar.
- El resultado puede crecer mucho (la forma `exp` de identidades trig genera expresiones largas); combinar con `simplify`/`expand` si conviene.

## Notas relacionadas

- [[Expr.subs]]
- [[concepto_expr_arbol]]
- [[Expr]]
- [[sympy.simplify/reescritura/index | reescritura]]
- [[sympy.simplify/index | sympy.simplify]]
