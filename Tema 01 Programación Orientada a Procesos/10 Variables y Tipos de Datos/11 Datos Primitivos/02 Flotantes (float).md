---
title: 02 Flotantes (float)
draft: false
tags: [python, teoria, numericos]
---

# Flotantes-`float`

Representa números con **punto decimal**. Se llaman "punto flotante" porque el punto decimal puede "flotar" entre los dígitos significativos, permitiendo representar números muy grandes o muy pequeños. Es un tipo **inmutable**, escalar y de tamaño fijo (a diferencia de los [[01 Enteros (int) | enteros]], que son de precisión arbitraria).

> [!note] Nota
> En Python (CPython) los `float` se implementan como un `double` de C: formato **IEEE-754 de doble precisión (64 bits)**.

## Construcción y sintaxis literal

| Forma | Ejemplo | Resultado |
| --- | --- | --- |
| Literal con punto | `3.14` | `3.14` |
| Notación científica | `1.5e3`, `2E-4` | `1500.0`, `0.0002` |
| Solo parte fraccionaria | `.5`, `5.` | `0.5`, `5.0` |
| Separador de legibilidad | `1_000.000_1` | `1000.0001` |
| Constructor desde `str`/`int` | `float("2.5")`, `float(7)` | `2.5`, `7.0` |
| Valores especiales | `float("inf")`, `float("nan")` | `inf`, `nan` |

```python
type(3.14)        # <class 'float'>
float("  3.5  ")  # 3.5   (tolera espacios alrededor)
float("1_000.5")  # 1000.5
float("1e309")    # inf   (excede el máximo representable)
float("abc")      # ValueError: could not convert string to float
```

> [!info] La división `/` siempre produce `float`
> `10 / 2` devuelve `5.0`, no `5`. Para resultado entero usar `//`. Ver [[01 Enteros (int) | enteros]].

## Representación interna (IEEE-754, doble precisión)

Un `float` de 64 bits se reparte en tres campos: $valor = (-1)^{s} \times 1.m \times 2^{e-1023}$.

| Campo | Bits | Función |
| --- | --- | --- |
| Signo (`s`) | 1 | 0 = positivo, 1 = negativo |
| Exponente (`e`) | 11 | Sesgado en 1023 (rango efectivo $-1022$ a $+1023$) |
| Mantisa (`m`) | 52 | Dígitos significativos (más 1 bit implícito) |

Consecuencias directas:

- **Precisión:** 52 bits de mantisa equivalen a **~15 a 17 dígitos decimales significativos**. Más allá de eso, Python "corta" el resto.
- **Máximo finito:** `sys.float_info.max` $\approx 1.8 \times 10^{308}$. Superarlo da `inf`.
- **Mínimo normal positivo:** `sys.float_info.min` $\approx 2.2 \times 10^{-308}$. Bajo eso hay subnormales hasta `~5e-324`; más cerca de cero, colapsa a `0.0`.
- **Epsilon:** `sys.float_info.epsilon` $\approx 2.22 \times 10^{-16}$, la menor diferencia distinguible respecto a `1.0`.

```python
import sys
sys.float_info.max      # 1.7976931348623157e+308
sys.float_info.min      # 2.2250738585072014e-308
sys.float_info.epsilon  # 2.220446049250313e-16
sys.float_info.dig      # 15  (dígitos decimales garantizados)
```

## `repr` vs `str`

Desde Python 3.1 ambos coinciden para `float`: `repr()` produce la cadena **más corta** que, al releerla, reconstruye exactamente el mismo `float` (round-trip garantizado).

```python
x = 0.1
repr(x)          # '0.1'
str(x)           # '0.1'
x == float(repr(x))  # True  (round-trip exacto)

# Pero el valor real almacenado tiene más dígitos:
f"{x:.17f}"      # '0.10000000000000001'
f"{x:.55f}"      # '0.1000000000000000055511151231257827021181583404541015625'
```

> [!tip] Ver el valor exacto
> `Decimal(x)` revela la fracción binaria real almacenada en el `float`, sin redondeo de visualización:
> ```python
> from decimal import Decimal
> Decimal(0.1)  # Decimal('0.1000000000000000055511151231257827021181583404541015625')
> ```

## Problemas de Punto Flotante

El problema nace de que las computadoras cuentan en base 2 (binario) pero nosotros en base 10 (decimal).

### El Dilema del `0.1 + 0.2`

En base 10, `0.1` es una fracción simple ($\frac{1}{10}$). En binario es una **fracción periódica infinita** (como $\frac{1}{3}=0.333\dots$ en decimal). La máquina trunca esa secuencia, generando un error de redondeo que se acumula al operar.

```python
print(0.1 + 0.2)        # 0.30000000000000004
0.1 + 0.2 == 0.3        # False
(0.1 + 0.2) - 0.3       # 5.551115123125783e-17
```

### Comparación correcta: `math.isclose()`

> [!warning] Nunca compares flotantes con `==`
> El error de redondeo hace que igualdades "obvias" fallen. Compara por cercanía.

```python
import math

# Mal:
0.1 + 0.2 == 0.3                       # False

# Bien (Python 3.5+):
math.isclose(0.1 + 0.2, 0.3)           # True

# Control fino de tolerancias:
math.isclose(a, b, rel_tol=1e-9, abs_tol=0.0)
```

| Parámetro | Significado | Uso |
| --- | --- | --- |
| `rel_tol` | Tolerancia **relativa** (por defecto `1e-09`) | Comparar magnitudes grandes/normales |
| `abs_tol` | Tolerancia **absoluta** (por defecto `0.0`) | Imprescindible cuando alguno es `0.0` |

La condición es `abs(a-b) <= max(rel_tol * max(abs(a), abs(b)), abs_tol)`. Para valores cercanos a cero, `rel_tol` no sirve (todo es relativo a ~0) y hay que dar `abs_tol`:

```python
math.isclose(0.0, 1e-12)                   # False  (rel_tol inútil cerca de 0)
math.isclose(0.0, 1e-12, abs_tol=1e-9)     # True
```

> [!info] Pérdida de importancia (loss of significance)
> Al sumar un número muy pequeño a uno muy grande, el pequeño puede desaparecer por completo al exceder los 15-17 dígitos de precisión: `1e16 + 1.0 == 1e16` es `True`.

## Valores especiales: `inf`, `-inf`, `nan`

IEEE-754 define tres valores que no son números finitos. Surgen de operaciones de overflow, indeterminaciones o explícitamente.

| Valor | Cómo surge | Detección |
| --- | --- | --- |
| `inf` | `1e309`, `1e308 * 10`, `1.0 / 0.0` (no, da error), `math.inf` | `math.isinf(x)` |
| `-inf` | `-1e309`, `float("-inf")`, `-math.inf` | `math.isinf(x)` |
| `nan` | `inf - inf`, `inf / inf`, `0.0 * inf`, `float("nan")` | `math.isnan(x)` |

```python
import math

x = 1e308 * 10        # inf  (overflow, NO lanza error)
math.inf - math.inf   # nan
math.isinf(x)         # True
math.isfinite(2.5)    # True   (ni inf ni nan)
```

> [!warning] `nan` no es igual a nada, ni a sí mismo
> Esta es la propiedad más sorprendente: cualquier comparación con `nan` da `False` (excepto `!=`, que da `True`). Por eso **`x != x` es el test clásico de `nan`**, aunque `math.isnan(x)` es más claro.
> ```python
> nan = float("nan")
> nan == nan          # False
> nan != nan          # True   <- única comparación verdadera
> nan < 1, nan > 1    # (False, False)
> math.isnan(nan)     # True
> ```

> [!info] División entre cero
> A diferencia de IEEE puro, en Python `1.0 / 0.0` lanza `ZeroDivisionError`. Para obtener `inf` hay que usar `math.inf` o `float("inf")` explícitamente.

## Redondeo: `round()` y redondeo bancario

`round(x, ndigits)` devuelve `x` redondeado a `ndigits` decimales (por defecto `0`, devolviendo `int`). Usa **redondeo bancario** (*round half to even*, "banker's rounding"): cuando el dígito está exactamente a la mitad, redondea al **par más cercano**, no siempre hacia arriba.

```python
round(2.5)     # 2   (al par)   <- NO 3
round(3.5)     # 4   (al par)
round(0.5)     # 0
round(1.5)     # 2
round(2.675, 2)  # 2.67  <- esperabas 2.68, pero 2.675 se almacena como 2.6749999...
```

| Llamada | Resultado | Motivo |
| --- | --- | --- |
| `round(2.5)` | `2` | Mitad → al par |
| `round(3.5)` | `4` | Mitad → al par |
| `round(2.675, 2)` | `2.67` | El `float` real es `2.67499...` |
| `round(3.14159, 2)` | `3.14` | Redondeo normal |
| `round(-2.5)` | `-2` | Mitad → al par |

> [!warning] `round()` no es fiable para dinero
> Por el redondeo bancario y por la imprecisión binaria, `round` sobre `float` da sorpresas. Para finanzas usar `decimal.Decimal` con su redondeo controlado (ver abajo).

## Módulo `math`

Funciones esenciales para `float` (operan y devuelven `float`, salvo donde se indica).

| Función | Descripción | Ejemplo → salida |
| --- | --- | --- |
| `math.floor(x)` | Redondea hacia $-\infty$ (devuelve `int`) | `math.floor(2.9)` → `2`; `math.floor(-2.1)` → `-3` |
| `math.ceil(x)` | Redondea hacia $+\infty$ (devuelve `int`) | `math.ceil(2.1)` → `3`; `math.ceil(-2.9)` → `-2` |
| `math.trunc(x)` | Elimina la parte fraccionaria hacia `0` (devuelve `int`) | `math.trunc(2.9)` → `2`; `math.trunc(-2.9)` → `-2` |
| `math.isnan(x)` | `True` si es `nan` | `math.isnan(float("nan"))` → `True` |
| `math.isinf(x)` | `True` si es `±inf` | `math.isinf(1e400)` → `True` |
| `math.isfinite(x)` | `True` si no es `inf` ni `nan` | `math.isfinite(3.0)` → `True` |
| `math.isclose(a, b)` | Comparación por cercanía | `math.isclose(.1+.2, .3)` → `True` |
| `math.modf(x)` | Devuelve `(fraccionaria, entera)` ambas `float` | `math.modf(2.75)` → `(0.75, 2.0)` |
| `math.fsum(it)` | Suma de un iterable sin acumular error | `math.fsum([.1]*10)` → `1.0` |

```python
import math

# floor / ceil / trunc difieren con negativos:
#   x      floor  ceil  trunc
#  2.7      2      3      2
# -2.7     -3     -2     -2

# fsum vs sum (fsum evita el error acumulado):
sum([0.1] * 10)        # 0.9999999999999999
math.fsum([0.1] * 10)  # 1.0
```

## Métodos del propio `float`

| Método | Devuelve | Ejemplo → salida |
| --- | --- | --- |
| `x.is_integer()` | `bool`: ¿el `float` no tiene parte fraccionaria? | `(5.0).is_integer()` → `True`; `(5.5).is_integer()` → `False` |
| `x.as_integer_ratio()` | `(num, den)`: fracción exacta que iguala el `float` | `(0.5).as_integer_ratio()` → `(1, 2)` |
| `x.hex()` | `str`: representación hexadecimal exacta (sin pérdida) | `(0.1).hex()` → `'0x1.999999999999ap-4'` |
| `float.fromhex(s)` | `float`: reconstruye desde la cadena hex | `float.fromhex('0x1.8p+1')` → `3.0` |

```python
(0.1).as_integer_ratio()
# (3602879701896397, 36028797018963968)  <- la fracción binaria EXACTA de 0.1

# hex() + fromhex() dan round-trip perfecto (útil para serializar sin perder bits):
h = (0.1).hex()          # '0x1.999999999999ap-4'
float.fromhex(h) == 0.1  # True
```

## Formateo de salida

Mini-lenguaje de formato (`f-strings`, `format()`, `%`). El tipo de presentación va tras los dos puntos.

| Especificador | Significado | Ejemplo → salida |
| --- | --- | --- |
| `:.2f` | Fijo, 2 decimales | `f"{3.14159:.2f}"` → `'3.14'` |
| `:.0f` | Fijo, sin decimales (redondea) | `f"{2.7:.0f}"` → `'3'` |
| `:e` / `:.2e` | Científica | `f"{12345.6:.2e}"` → `'1.23e+04'` |
| `:g` | General: elige fijo o científico, descarta ceros | `f"{0.0001234:g}"` → `'0.0001234'`; `f"{1234567.0:g}"` → `'1.23457e+06'` |
| `:%` | Porcentaje (multiplica por 100) | `f"{0.25:.1%}"` → `'25.0%'` |
| `:,` | Separador de miles | `f"{1234567.89:,.2f}"` → `'1,234,567.89'` |
| `:+.2f` | Fuerza signo | `f"{3.5:+.2f}"` → `'+3.50'` |
| `:>10.2f` | Alineado, ancho 10 | `f"{3.14:>10.2f}"` → `'      3.14'` |

```python
n = 1234567.891
print(f"{n:.2f}")     # 1234567.89
print(f"{n:,.2f}")    # 1,234,567.89
print(f"{n:.3e}")     # 1.235e+06
print(f"{n:g}")       # 1.23457e+06
```

## Alternativas de precisión exacta

Cuando el error binario es inaceptable, Python ofrece dos tipos del [[Modulo y Paquetes | módulo]] estándar.

### `decimal.Decimal` — base 10 exacta

Aritmética decimal exacta con precisión y modo de redondeo configurables. **Estándar para dinero y finanzas.**

```python
from decimal import Decimal, getcontext, ROUND_HALF_UP

Decimal("0.1") + Decimal("0.2")   # Decimal('0.3')  <- exacto
Decimal("0.1") + Decimal("0.2") == Decimal("0.3")  # True

# CLAVE: construir desde str, no desde float (el float ya viene contaminado):
Decimal(0.1)     # Decimal('0.1000000000000000055511151231257827021181583404541015625')
Decimal("0.1")   # Decimal('0.1')

# Redondeo controlado (a diferencia del bancario de round()):
Decimal("2.675").quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)  # Decimal('2.68')

getcontext().prec = 50   # 50 dígitos significativos de precisión global
```

### `fractions.Fraction` — racionales exactos

Representa números como fracción `numerador/denominador` exacta, sin error alguno. Ideal cuando se necesitan **proporciones exactas** o aritmética simbólica simple.

```python
from fractions import Fraction

Fraction(1, 3) + Fraction(1, 6)   # Fraction(1, 2)  <- exacto, sin redondeo
Fraction("0.1") + Fraction("0.2") # Fraction(3, 10)
Fraction(0.1)                     # Fraction(3602879701896397, 36028797018963968)  (¡desde float!)
float(Fraction(1, 3))             # 0.3333333333333333
```

| Tipo | Base | Precisión | Velocidad | Usar cuando |
| --- | --- | --- | --- | --- |
| `float` | 2 (binaria) | ~15-17 díg., con error | Muy rápida (hardware) | Cálculo científico, gráficos, general |
| `Decimal` | 10 | Configurable, exacta en decimal | Lenta (software) | Dinero, finanzas, contabilidad |
| `Fraction` | Racional | Exacta absoluta | Lenta, crece el denominador | Proporciones, fracciones exactas |

> [!tip] Regla práctica
> `float` por defecto. `Decimal` para dinero. `Fraction` cuando necesites fracciones exactas. Y **siempre construye `Decimal`/`Fraction` desde `str`**, no desde un `float` ya contaminado.

> [!note] Tipos numéricos hermanos
> El [[04 Booleanos (bool) | bool]] y el [[01 Enteros (int) | int]] conviven con `float` en la jerarquía numérica. Para números con parte imaginaria ver [[03 Complejos (complex) | complex]]. Para más operaciones ver [[Operadores de Variables | Operadores de Variable]].
