---
title: sympy.simplify — simplificador heuristico general de una expresion
aliases:
  - simplify
  - sympy.simplify
  - simplificar
tags:
  - sympy
  - api/funcion
  - simplify/general
lib: sympy
mod: sympy
tipo: funcion
retorna: Expr
requiere:
  - Symbol
draft: false
---

# sympy.simplify — simplificador heuristico general de una expresion

`simplify(expr)` intenta devolver "la forma mas simple" de una expresion **probando muchas transformaciones distintas** (factorizacion, cancelacion, identidades trigonometricas, simplificacion de potencias, gammas, etc.) y quedandose con el resultado que mide como mas sencillo. Es la herramienta **comodin**: util cuando no sabes que tipo de simplificacion necesitas. A cambio es **lenta** (explora muchos caminos) y **no canonica**: no garantiza una forma concreta ni que dos expresiones equivalentes lleguen al mismo resultado. Por eso, cuando ya sabes que quieres (cancelar una fraccion, factorizar, simplificar trig), conviene llamar a la funcion **especifica** —[[sympy.cancel]], `factor`, `trigsimp`— que es predecible y rapida. Ver [[concepto_simplificacion_automatica]] para la diferencia entre la auto-simplificacion que SymPy hace siempre y esta simplificacion bajo demanda.

> `simplify` no es una operacion matematica concreta, sino una **heuristica**: "prueba cosas y devuelve la que parezca mas simple". No esperes una forma garantizada; espera un buen intento.

## Firma

```python
sympy.simplify(
    expr,                # Expr: la expresion a simplificar
    ratio=1.7,           # float: cota de cuanto puede crecer el resultado vs original
    measure=count_ops,   # callable: funcion que mide la "complejidad" (cuenta operaciones)
    rational=False,      # bool | None: convertir floats a Rational antes de simplificar
    inverse=False,       # bool: permitir simplificar funciones inversas (asume dominios)
    doit=True,           # bool: evaluar objetos sin evaluar (Integral, Derivative...)
    ...
) -> Expr
```

## Valor de retorno

| Tipo | Forma | Significado |
|------|-------|-------------|
| `Expr` | la expresion reescrita | La forma que `measure` considero mas simple entre las probadas |

Si ninguna transformacion mejora la medida (o el resultado crece mas que `ratio`), devuelve la expresion **sin cambios**.

```python
from sympy import symbols, simplify, sin, cos
x = symbols("x")
simplify(sin(x)**2 + cos(x)**2)   # 1
```

## Formas basicas de llamada

| Objetivo | Llamada |
|----------|---------|
| Simplificar sin saber el tipo | `simplify(expr)` |
| Reconocer identidad trigonometrica | `simplify(sin(x)**2 + cos(x)**2)` |
| Simplificar cociente de gammas | `simplify(gamma(x)/gamma(x - 2))` |
| Tratar floats como racionales | `simplify(expr, rational=True)` |
| Cambiar el criterio de "simple" | `simplify(expr, measure=mi_medida)` |

## Parametros en detalle

### `expr` (obligatorio)

La expresion a simplificar. SymPy le aplica una bateria de transformaciones y elige la mejor segun `measure`.

```python
from sympy import symbols, simplify, sin, cos, gamma
x = symbols("x")
simplify(sin(x)**2 + cos(x)**2)   # 1                  -> identidad trig
simplify(gamma(x)/gamma(x - 2))   # (x - 2)*(x - 1)    -> simplifica gammas
simplify((x**2 - 1)/(x - 1))      # x + 1              -> cancela la fraccion
```

### `measure`

La funcion que decide que resultado es "mas simple". Por defecto es `count_ops` (cuenta operaciones: cuantas mas, mas complejo). Cambiarla altera que forma se elige; rara vez se toca.

### `ratio`

Cota de seguridad: si el resultado simplificado tiene mas de `ratio` veces las operaciones del original, se descarta y se devuelve el original. Evita que `simplify` "simplifique" hacia algo mas grande.

### `rational`

Con `rational=True`, los flotantes de la expresion se convierten a `Rational` (exactos) antes de simplificar, evitando que el ruido de coma flotante bloquee identidades. Para reconstruir una constante simbolica concreta a partir de un float, la herramienta es [[sympy.nsimplify]], no esta.

```python
from sympy import simplify
simplify(0.5 + 0.5)                  # 1.00000000000000   -> sigue siendo float
simplify(0.5, rational=True)         # 1/2                -> exacto
```

### `doit`

Con `doit=True` (por defecto), evalua objetos sin evaluar (`Integral`, `Derivative`, `Sum`) como parte de la simplificacion. Con `doit=False` los deja intactos.

## Casos de uso

### Verificar que dos expresiones son equivalentes

Restar y simplificar a `0` confirma la igualdad cuando no es obvia a la vista.

```python
from sympy import symbols, simplify, sin, cos
x = symbols("x")
simplify(sin(2*x) - 2*sin(x)*cos(x))   # 0   -> son la misma expresion
```

### Limpiar un resultado de otra operacion

Tras `solve`, `integrate` o `dsolve`, el resultado suele venir en forma poco legible; `simplify` lo asea cuando no sabes que transformacion concreta aplicar.

```python
from sympy import symbols, simplify, sin, cos
x = symbols("x")
expr = (sin(x)/cos(x)) * cos(x)
simplify(expr)   # sin(x)
```

## Errores comunes

| Error | Causa | Solucion |
|-------|-------|----------|
| Esperar una forma concreta garantizada | `simplify` es heuristico, no canonico | Usar la funcion especifica ([[sympy.cancel]], `factor`, `trigsimp`) |
| Lentitud en expresiones grandes | Explora muchas transformaciones | Llamar directamente a la operacion que sabes que quieres |
| No simplifica un float a fraccion | `simplify` no reconstruye constantes simbolicas | Usar [[sympy.nsimplify]] (`nsimplify(0.5)` -> `1/2`) |
| Dos equivalentes dan formas distintas | No produce forma canonica | Comparar con `simplify(a - b) == 0`, no `simplify(a) == simplify(b)` |
| Resultado mas largo de lo esperado | El criterio `measure`/`ratio` no lo recorto | Ajustar `measure` o aplicar la transformacion especifica |

## Limitaciones

- **No es canonico**: dos expresiones iguales pueden simplificarse a formas distintas; para comparar, simplifica la **diferencia** a `0`.
- **Lento** frente a las funciones especificas, porque prueba muchos caminos.
- No reconstruye constantes simbolicas desde floats (eso es [[sympy.nsimplify]]).
- Cuando ya sabes el tipo de simplificacion, casi siempre hay una funcion dedicada mas rapida y predecible.

## Notas relacionadas

- [[sympy.cancel]]
- [[sympy.nsimplify]]
- [[concepto_simplificacion_automatica]]
- [[sympy.simplify/general/index | general]]
