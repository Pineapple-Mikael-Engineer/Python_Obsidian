---
title: Integer — entero exacto de SymPy
aliases:
  - Integer
  - entero simbolico
tags:
  - sympy
  - api/clase
  - core/numeros
lib: sympy
mod: sympy.core.numbers
tipo: clase
retorna: Integer
requiere:
  - Rational
draft: false
---

# Integer — entero exacto de SymPy

Representa un **entero exacto** dentro del mundo simbolico de SymPy. Es el equivalente al `int` de Python, pero es un objeto `Expr`: vive en el arbol de expresiones y por eso puede mezclarse con simbolos, racionales y demas objetos de SymPy sin convertirse a flotante. Cuando operas un `int` de Python con una expresion de SymPy, este se **convierte automaticamente** a `Integer`. La diferencia clave frente al `int` nativo aparece en la division: `Integer(1)/3` da un `Rational` exacto, no un `float`. Ver [[concepto_simbolico_vs_numerico]].

## Constructor

```python
sympy.Integer(
    i,            # int | str: el valor entero
)                 # -> Integer
```

```python
from sympy import Integer

Integer(7)          # 7
type(Integer(7))    # <class 'sympy.core.numbers.Integer'>
Integer("42")       # 42
```

## Diferencia con el `int` de Python

`Integer` **no** es un `int`: es una expresion simbolica que envuelve el valor. Soporta las mismas operaciones aritmeticas pero permanece en el mundo simbolico.

```python
from sympy import Integer

isinstance(Integer(3), int)   # False  -> NO es int de Python
int(Integer(3))               # 3      -> convertir explicitamente SI da int

Integer(7) // 2               # 3   (division entera, igual que int)
Integer(7) % 2                # 1   (modulo, igual que int)
```

## Conversion automatica al operar con expresiones

No hace falta envolver a mano cada numero: en cuanto un `int` de Python participa en una operacion con un objeto SymPy, se sympifica a `Integer`.

```python
from sympy import symbols, Integer

x = symbols("x")

(x + 2)                 # x + 2   -> el 2 se volvio Integer dentro de la expr
type((x + 2).args[0])   # <class 'sympy.core.numbers.Integer'>

Integer(4) * 2          # 8       -> sigue siendo Integer
type(Integer(4) * 2)    # <class 'sympy.core.numbers.Integer'>
```

## Division: `Integer(1)/3 -> Rational`

Aqui esta la gran diferencia con Python. El `/` entre enteros nativos da `float`; el `/` con un `Integer` da una **fraccion exacta** (`Rational`).

```python
from sympy import Integer

1 / 3                   # 0.3333333333333333   -> float de Python
Integer(1) / 3          # 1/3                   -> Rational exacto
type(Integer(1) / 3)    # <class 'sympy.core.numbers.Rational'>

Integer(6) / 3          # 2     -> divide exacto: vuelve a ser Integer
```

> [!regla]
> Basta con que **uno** de los operandos sea SymPy para que toda la operacion sea exacta: `Integer(1)/3` o `S(1)/3` dan `1/3`. Ver [[concepto_simbolico_vs_numerico]].

## Mezcla con flotantes

Si mezclas un `Integer` con un `float` de Python, el resultado **cae a `Float`** y pierde exactitud. Mantente en el mundo simbolico mientras puedas.

```python
from sympy import Integer

Integer(2) + 0.5          # 2.50000000000000   -> ahora es Float, ya no exacto
type(Integer(2) + 0.5)    # <class 'sympy.core.numbers.Float'>
```

## Errores comunes

| Error | Causa | Solucion |
|-------|-------|----------|
| `isinstance(Integer(3), int)` da `False` | `Integer` no hereda de `int` | Usar `int(Integer(3))` si necesitas un `int` real |
| `1/3` sigue dando float dentro de SymPy | Ningun operando era SymPy | `Integer(1)/3` o `S(1)/3` |
| Resultado se vuelve `Float` | Se mezclo con un `float` de Python | No mezclar `float`; mantener todo simbolico |
| Esperabas `Rational` y sale `Integer` | La division fue exacta | Es correcto: `Integer(6)/3` es `2` |

## Notas relacionadas

- [[Rational]]
- [[Float]]
- [[sympy.constantes_simbolicas]]
- [[concepto_simbolico_vs_numerico]]
- [[sympy.core/numeros/index | numeros]]
