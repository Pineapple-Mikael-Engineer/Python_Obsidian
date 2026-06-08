---
title: sympy.nsimplify — reconstruir una expresion simbolica desde un numero flotante
aliases:
  - nsimplify
  - sympy.nsimplify
  - de flotante a simbolico
tags:
  - sympy
  - api/funcion
  - simplify/general
lib: sympy
mod: sympy
tipo: funcion
retorna: Expr
requiere:
  - Float
draft: false
---

# sympy.nsimplify — reconstruir una expresion simbolica desde un numero flotante

`nsimplify(num)` hace el camino **inverso a `evalf`**: parte de un **numero flotante** y trata de reconstruir la **expresion simbolica exacta** que lo produjo. Reconoce racionales simples (`nsimplify(0.5)` -> `1/2`) y, si le das una lista de constantes candidatas, combinaciones que las usan (`nsimplify(3.14159..., [pi])` -> `pi`). Es la herramienta para "adivinar" de donde salio un decimal: una raiz, una fraccion, un multiplo de `pi` o `E`. No confundir con [[sympy.simplify]] (que reescribe una expresion ya simbolica) ni con su parametro `rational`: `nsimplify` esta especializado en ir del **mundo numerico al simbolico**.

> `nsimplify` es el **puente de vuelta**: `evalf` convierte simbolico -> float (`pi.evalf()` -> `3.14159...`), y `nsimplify` intenta recuperar el simbolico desde ese float. No es magia exacta: usa tolerancia y, para constantes, necesita que le digas cuales probar.

## Firma

```python
sympy.nsimplify(
    expr,                # Expr | float: el numero (o expresion con floats) a reconstruir
    constants=(),        # lista: constantes candidatas a usar (pi, E, GoldenRatio...)
    tolerance=None,      # float: error maximo aceptado al reconstruir
    full=False,          # bool: probar formas mas elaboradas (CRootOf, etc.)
    rational=None,       # bool: forzar resultado racional (sin irracionales)
    rational_conversion="base10",
) -> Expr
```

## Valor de retorno

| Tipo | Forma | Significado |
|------|-------|-------------|
| `Expr` | racional / constante / combinacion | La expresion simbolica que reproduce el numero dentro de `tolerance` |

Si no encuentra una forma simbolica razonable, devuelve un `Float` o la expresion practicamente sin cambios.

```python
from sympy import nsimplify
nsimplify(0.5)   # 1/2
```

## Formas basicas de llamada

| Objetivo | Llamada |
|----------|---------|
| Float -> fraccion exacta | `nsimplify(0.5)` |
| Reconocer un multiplo de pi | `nsimplify(3.141592653589793, [pi])` |
| Reconocer una raiz | `nsimplify(1.4142135623730951)` |
| Reconocer E (numero de Euler) | `nsimplify(2.718281828459045, [exp(1)])` |
| Forzar resultado racional | `nsimplify(0.1, rational=True)` |
| Aflojar la exigencia | `nsimplify(0.3333, tolerance=1e-3)` |

## Parametros en detalle

### `expr` (obligatorio)

El numero flotante (o una expresion que contenga floats) que se quiere reconstruir simbolicamente.

```python
from sympy import nsimplify
nsimplify(0.5)                       # 1/2
nsimplify(0.25)                      # 1/4
nsimplify(1.4142135623730951)        # sqrt(2)   -> reconoce la raiz sin pista
```

### `constants`

Lista de constantes simbolicas que `nsimplify` puede usar para construir el resultado. Sin pistas reconoce racionales y algunas raices; para `pi`, `E` o la razon aurea **debes incluirlas** en la lista.

```python
from sympy import nsimplify, pi, exp, GoldenRatio
nsimplify(3.141592653589793, [pi])         # pi
nsimplify(2.718281828459045, [exp(1)])     # E
nsimplify(1.618033988749895, [GoldenRatio])  # GoldenRatio
```

### `rational`

Con `rational=True` fuerza un resultado **racional** (un cociente de enteros), ignorando irracionales aunque encajaran. Util cuando sabes que el numero "debe" ser una fraccion.

```python
from sympy import nsimplify
nsimplify(0.1)                   # 1/10
nsimplify(0.1, rational=True)    # 1/10   -> garantiza fraccion, no irracional
```

### `tolerance`

Error maximo permitido al reconstruir. Subirlo hace a `nsimplify` mas "indulgente" y le permite reconocer un decimal truncado como su fraccion limpia.

```python
from sympy import nsimplify
nsimplify(0.3333, tolerance=1e-3)   # 1/3   -> acepta el redondeo
```

### `full`

Con `full=True` prueba reconstrucciones mas elaboradas (incluidas raices de polinomios via `CRootOf`). Mas lento; reservar para cuando las formas simples no bastan.

## Casos de uso

### Recuperar el valor exacto de un resultado numerico

Tras un calculo que devolvio un float, `nsimplify` propone la forma cerrada de la que probablemente provino.

```python
from sympy import nsimplify, pi
# Un area calculo dio 3.141592653589793; sospechas que es pi
nsimplify(3.141592653589793, [pi])   # pi
```

### Pasar una constante medida a forma simbolica

Para seguir trabajando exacto (sin arrastrar ruido de coma flotante) se reconstruye el simbolo y se continua en el mundo exacto.

```python
from sympy import nsimplify, sqrt
val = 1.4142135623730951
expr = nsimplify(val)   # sqrt(2)
expr**2                 # 2   -> ya es exacto, sin error numerico
```

## Errores comunes

| Error | Causa | Solucion |
|-------|-------|----------|
| No reconoce un multiplo de pi/E | No incluiste la constante en `constants` | Pasar `nsimplify(num, [pi])` (o `[exp(1)]`) |
| Devuelve el float casi igual | Ninguna forma cae dentro de `tolerance` | Subir `tolerance` o anadir candidatas en `constants` |
| Resultado irracional cuando esperabas fraccion | Encajo mejor un irracional | Forzar con `rational=True` |
| Confundir con `simplify` | `simplify` reescribe simbolico; `nsimplify` va de float a simbolico | Usar `nsimplify` para reconstruir numeros |
| Reconstruccion falsa por demasiada tolerancia | `tolerance` muy alta inventa formas | Bajar `tolerance` para exigir mas exactitud |

## Limitaciones

- Es **heuristico**: puede no encontrar la forma cerrada o, con tolerancia alta, proponer una falsa.
- Para constantes irracionales necesita que le digas cuales probar via `constants`.
- Solo tiene sentido sobre **numeros** (o expresiones con floats); no simplifica algebra simbolica pura (eso es [[sympy.simplify]]).
- Es el inverso conceptual de `evalf`, pero no su inversa exacta: `evalf` siempre da un numero; `nsimplify` solo a veces recupera el simbolo original.

## Notas relacionadas

- [[sympy.simplify]]
- [[sympy.cancel]]
- [[sympy.simplify/general/index | general]]
