---
title: sympy.sympify — convertir objetos de Python en objetos de SymPy
aliases:
  - sympify
  - sympy.sympify
  - S
  - simbolizar
tags:
  - sympy
  - api/funcion
  - core/simbolos
lib: sympy
mod: sympy
tipo: funcion
retorna: Expr
requiere:
  - concepto_simbolico_vs_numerico
draft: false
---

# sympy.sympify — convertir objetos de Python en objetos de SymPy

Convierte un objeto de Python (`str`, `int`, `float`, listas, tuplas, diccionarios…) en su **equivalente simbolico** de SymPy, devolviendo una [[Symbol|Expr]] (o una estructura de objetos SymPy). Es el puente de entrada al mundo simbolico: casi todas las funciones de SymPy la llaman por dentro, por eso aceptan cadenas como `"x**2 + 1"`. Su atajo es la **`S`** (singleton), que ademas sirve para forzar **exactitud**: `S(1)/3` da el racional exacto `1/3`, no el `float` `0.333…`. Acepta el argumento `strict` para rechazar lo que no sepa convertir.

> [!warning] Evalua la cadena
> `sympify` **interpreta y evalua** la cadena que recibe (internamente usa `eval` sobre un espacio de nombres de SymPy). **No** pases a `sympify` cadenas de **fuentes no confiables**: equivale a ejecutar codigo. Para entrada externa usa `parse_expr` con un entorno restringido o valida antes.

## Firma

```python
sympy.sympify(
    a,                  # objeto a convertir: str, int, float, Rational, lista, dict, ...
    locals=None,        # dict: nombres extra reconocibles al parsear una cadena
    convert_xor=True,   # bool: en cadenas, interpretar '^' como potencia (**)
    strict=False,       # bool: True -> error si no sabe convertir (no cae a Symbol/str)
    rational=False,     # bool: convertir floats de la cadena a Rational exactos
    evaluate=True,      # bool: aplicar la auto-simplificacion al construir
) -> Expr
```

`S` es el atajo equivalente para los usos comunes: `S("x**2")`, `S(1)/3`.

## Valor de retorno

| Entrada | Devuelve | Significado |
|---------|----------|-------------|
| `"x**2 + 1"` | `Expr` | La expresion simbolica parseada |
| `1`, `2` (int) | `Integer` | Entero exacto de SymPy |
| `1.5` (float) | `Float` | Flotante de precision arbitraria |
| `[1, 2, 3]` | `list` de objetos SymPy | Misma estructura, elementos sympificados |
| `{...}`, `(...)` | `dict` / `Tuple` | Estructura con elementos convertidos |

```python
from sympy import sympify, S
sympify("x**2 + 1")    # x**2 + 1   -> Expr
type(S(2))             # <class 'sympy.core.numbers.Integer'>
```

## Formas basicas de llamada

| Objetivo | Llamada |
|----------|---------|
| Parsear una expresion en cadena | `sympify("x*y + 1")` |
| Numero entero exacto | `S(2)` |
| Fraccion exacta | `S(1)/3` |
| Float exacto desde cadena | `sympify("0.1", rational=True)` |
| Reconocer un nombre propio | `sympify("f(x)", locals={"f": f})` |
| Rechazar lo no convertible | `sympify(obj, strict=True)` |

## Parametros en detalle

### `a` (obligatorio)

El objeto a convertir. Un `int`/`float` de Python se vuelve `Integer`/`Float`; una **cadena** se **parsea** como expresion; los contenedores se recorren elemento a elemento.

```python
from sympy import sympify
sympify(2)             # 2            -> Integer
sympify(2.5)           # 2.50000000000000   -> Float
sympify("x + 2*y")     # x + 2*y      -> Expr
sympify([1, "x", 3])   # [1, x, 3]    -> lista con elementos SymPy
```

### `S(...)` y la exactitud (`S(1)/3`)

El problema tipico: dividir dos `int` de Python da un `float`, perdiendo exactitud. Envolver con `S` mete el numero al mundo SymPy **antes** de operar, y la division queda como `Rational` exacto.

```python
from sympy import S
1/3            # 0.3333333333333333   -> float de Python (inexacto)
S(1)/3         # 1/3                  -> Rational exacto de SymPy
S(1)/3 + S(1)/6   # 1/2               -> aritmetica exacta
```

### `rational`

Con `rational=True`, los **floats dentro de una cadena** se convierten a `Rational` exactos en vez de `Float`, util para no arrastrar el error binario de `0.1`.

```python
from sympy import sympify
sympify("0.1")                  # 0.100000000000000   -> Float
sympify("0.1", rational=True)   # 1/10                -> Rational exacto
```

### `locals`

Diccionario de nombres extra que el parser debe reconocer al leer una cadena. Sin el, un nombre desconocido se vuelve un `Symbol` cualquiera.

```python
from sympy import sympify, Function, symbols
f = Function("f")
x = symbols("x")
sympify("f(x) + 1", locals={"f": f, "x": x})   # f(x) + 1
```

### `strict`

Por defecto, si `sympify` no sabe convertir algo intenta tratarlo como cadena/`Symbol`. Con `strict=True` lanza `SympifyError` en vez de adivinar, util para validar entradas.

```python
from sympy import sympify
from sympy.core.sympify import SympifyError
try:
    sympify(object(), strict=True)
except SympifyError:
    pass    # rechaza lo que no sabe convertir
```

### `convert_xor`

En cadenas, por defecto `^` se reinterpreta como potencia `**` (notacion matematica). Con `convert_xor=False` se respeta el XOR de Python.

```python
from sympy import sympify
sympify("x^2")                     # x**2   -> '^' como potencia
sympify("x^2", convert_xor=False)  # Xor(x, 2)
```

## Casos de uso

### Mantener exactitud en una constante fraccionaria

```python
from sympy import S, pi
area = S(1)/2 * pi      # pi/2   -> exacto, no 1.5707...
```

### Leer un modelo desde texto (entrada confiable)

```python
from sympy import sympify, symbols
x = symbols("x")
modelo = sympify("3*x**2 - 2*x + 5")   # Expr lista para derivar/evaluar
modelo.subs(x, 2)                       # 13
```

### Convertir datos tabulados a objetos exactos

```python
from sympy import sympify
coefs = sympify(["1/2", "3/4", "5/6"])   # [1/2, 3/4, 5/6]  -> Rationals exactos
```

## Errores comunes

| Error | Causa | Solucion |
|-------|-------|----------|
| `1/3` da `0.333...` y no `1/3` | Division entre `int` de Python, no de SymPy | Envolver con `S`: `S(1)/3` |
| `SympifyError` al parsear | Cadena mal formada o nombre no reconocido | Corregir sintaxis o pasar `locals=` |
| `0.1` arrastra error binario | Float convierte el flotante tal cual | Usar `rational=True` o `Rational(1, 10)` |
| Ejecuta codigo inesperado | `sympify` evalua la cadena (`eval`) | No sympificar entrada no confiable; usar `parse_expr` |
| `x^2` no es XOR como esperaba | `convert_xor=True` por defecto | Pasar `convert_xor=False` si se quiere XOR |

## Notas relacionadas

- [[Symbol]]
- [[sympy.symbols]]
- [[concepto_simbolico_vs_numerico]]
- [[sympy.core/simbolos/index | simbolos]]
