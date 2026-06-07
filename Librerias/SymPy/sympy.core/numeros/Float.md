---
title: Float — flotante de precision arbitraria de SymPy
aliases:
  - Float
  - flotante de precision arbitraria
  - numero de coma flotante simbolico
tags:
  - sympy
  - api/clase
  - core/numeros
lib: sympy
mod: sympy.core.numbers
tipo: clase
retorna: Float
requiere:
  - Integer
draft: false
---

# Float — flotante de precision arbitraria de SymPy

Representa un numero de **coma flotante de precision arbitraria**. A diferencia del `float` nativo de Python (siempre 64 bits / ~15-16 digitos decimales, respaldado por el hardware), `Float` usa **mpmath** por debajo y puede llevar tantos digitos significativos como pidas: 30, 50, 1000. Es el tipo al que llega `evalf()` cuando quieres un **valor numerico** de una expresion simbolica conservando mucha precision. No es exacto como `Rational`: sigue siendo coma flotante, pero con la precision que tu decidas. Ver [[concepto_simbolico_vs_numerico]].

## Constructor

```python
sympy.Float(
    num,            # str | float | int: el valor (preferir str para precision)
    dps=None,       # int: digitos decimales de precision deseados
    precision=None, # int: bits de precision (alternativa a dps)
)                   # -> Float
```

- `dps` = *decimal places*, los **digitos significativos** que tendra el numero.
- Por defecto, sin `dps`, usa ~15-16 digitos (53 bits, como el `float` nativo).

```python
from sympy import Float

Float("0.1")          # 0.100000000000000      -> ~15 digitos (default)
Float("0.1", 30)      # 0.100000000000000000000000000000   -> 30 digitos
Float("0.1")._prec    # 53   -> bits internos por defecto
```

## El argumento de precision (`dps`)

El segundo argumento fija cuantos **digitos significativos** se guardan. Con el puedes superar de largo la precision de un `float` de hardware.

```python
from sympy import Float, pi

Float(pi.evalf(50))   # 3.1415926535897932384626433832795028841971693993751
# 50 digitos de pi -> imposible con el float nativo (se corta en ~16)
```

## Por que `Float("0.1")` != `0.1` nativo

El detalle mas sutil: depende de **como** pasas el valor.

- Si pasas la **cadena** `"0.1"`, SymPy interpreta el decimal directamente y, con suficientes digitos, es realmente `0.1`.
- Si pasas el **`float` nativo** `0.1`, este **ya viene corrupto** desde Python (en binario `0.1` no es exacto), y pedir mas digitos solo revela la basura que ya traia.

```python
from sympy import Float, Rational

Float("0.1", 30)   # 0.100000000000000000000000000000        -> limpio: era una str
Float(0.1, 30)     # 0.100000000000000005551115123126        -> el float nativo ya venia sucio

Float("0.1", 30) == Rational(1, 10)   # False  -> sigue siendo flotante, no exacto
```

> [!regla]
> Para crear un `Float` de alta precision **pasa siempre una cadena**: `Float("0.1", 30)`. Si pasas el `float` nativo `0.1`, los digitos extra solo amplifican el error de redondeo que ya traia. Para exactitud real usa [[Rational]], no `Float`.

## Cuando usarlo

| Necesitas… | Usa |
|------------|-----|
| Un **valor numerico** con muchos digitos de una expresion exacta | `expr.evalf(n)` -> devuelve `Float` |
| Reproducir el `float` nativo dentro de SymPy | `Float(0.1)` (default 53 bits) |
| Constantes con altisima precision (`pi`, `sqrt(2)`, `E`) | `pi.evalf(50)`, `Float("...", n)` |
| Aritmetica **exacta** (fracciones, raices) | **No** uses `Float`: usa [[Rational]] / simbolico |
| Evaluar masivo sobre arrays | **No**: compila con `lambdify` a NumPy |

```python
from sympy import sqrt

sqrt(2).evalf(40)   # 1.414213562373095048801688724209698078570
# 40 digitos de sqrt(2) -> esto es un Float de precision arbitraria
```

## Mezcla con el mundo simbolico

En cuanto un `Float` participa en una operacion, **contagia** el resultado a coma flotante (deja de ser exacto). Por eso conviene trabajar simbolico el mayor tiempo posible y pasar a `Float` solo al final.

```python
from sympy import Integer, Float

1 + Float("2.5")          # 3.50000000000000
type(1 + Float("2.5"))    # <class 'sympy.core.numbers.Float'>

Integer(2) + 0.5          # 2.50000000000000   -> el Integer cayo a Float
```

## Errores comunes

| Error | Causa | Solucion |
|-------|-------|----------|
| `Float(0.1, 30)` muestra `...005551...` | Se paso el `float` nativo, ya inexacto | Pasar la cadena: `Float("0.1", 30)` |
| `Float("0.1") == Rational(1,10)` da `False` | `Float` es flotante, no exacto | Usar `Rational` si necesitas igualdad exacta |
| La precision extra "no sirve" | El operando original era `float` nativo | Nacer de una expresion simbolica + `evalf(n)` |
| Toda la expresion se vuelve `Float` | Un `Float` contagia el resultado | Mantener simbolico y evaluar al final |

## Notas relacionadas

- [[Rational]]
- [[Integer]]
- [[sympy.constantes_simbolicas]]
- [[concepto_simbolico_vs_numerico]]
- [[concepto_evalf_lambdify]]
- [[sympy.core/numeros/index | numeros]]
