---
title: Enteros (int)
order: 1
draft: false
tags: [python, teoria, numericos]
---

# Enteros-`int`

Representa **números abstractos sin parte fraccionaria**. Incluye números positivos, negativos y el cero. En Python, los enteros tienen **precisión arbitraria**, lo que significa que el único límite para el tamaño de un número es la memoria disponible de tu computadora. Es un tipo **inmutable** y de longitud variable.

| Propiedad         | Valor                                                                 |
| ----------------- | --------------------------------------------------------------------- |
| Clase             | `int`                                                                 |
| Mutabilidad       | Inmutable                                                             |
| Precisión         | Arbitraria (limitada por memoria)                                     |
| Constructor       | `int()`, `int(x)`, `int(s, base)`                                     |
| Valor por defecto | `int()` → `0`                                                         |
| Jerarquía         | `int` ⊂ `numbers.Integral` ⊂ `numbers.Rational` ⊂ `numbers.Number`   |

## Representación
Python permite escribir literales enteros en diferentes bases numéricas, lo cual es muy útil para [[programación de bajo nivel o sistemas | programación de bajo nivel o sistemas]]:

| Tipo                      | Funcionamiento      | Ejemplo                  |
| ------------------------- | ------------------- | ------------------------ |
| **Decimal (Base 10)**     | El estándar         | `10`,`-50`               |
| **Binario (Base 2)**      | Se le antepone `0b` | `0b1010` (10 en decimal) |
| **Octal (Base 8)**        | Se le antepone `0o` | `0o12` (10 en decimal)   |
| **Hexadecimal (Base 16)** | Se le antepone `0x` | `0xA` (10 en decimal)    |

El prefijo es indiferente a mayúsculas (`0B`, `0O`, `0X`, `0xff` == `0xFF`). Internamente **todos los literales producen el mismo objeto `int`**: la base es solo notación de escritura, no un tipo distinto.

```python
0b1010      # 10
0o12        # 10
0xA         # 10
10 == 0b1010 == 0o12 == 0xA   # True
```

> [!tip] Separador `_`
> Se pueden usar guiones bajos como separadores visuales para mejorar la legibilidad: `1_000_000` es lo mismo que `1000000`. Funciona en cualquier base y agrupa libremente, pero **no puede ir al inicio, al final, ni duplicado**, ni junto al prefijo de base.
> ```python
> 1_000_000        # 1000000
> 0b_1010_0001     # 161  (válido tras el prefijo)
> 0xDE_AD_BE_EF    # 3735928559
> # 1__000  -> SyntaxError (doble _)
> # _1000   -> es un NOMBRE de variable, no un número
> ```

### Construcción desde cadena: `int(s, base)`
`int(s, base)` interpreta una cadena en la base indicada (`2`–`36`). Con `base=0`, deduce la base del prefijo presente en la cadena.

```python
int("1010", 2)     # 10
int("FF", 16)      # 255
int("0xFF", 16)    # 255  (acepta el prefijo redundante)
int("777", 8)      # 511
int("z", 36)       # 35   (dígitos 0-9 y a-z)
int("0b1010", 0)   # 10   (base deducida del prefijo)
int("1010", 0)     # 1010 (sin prefijo, se asume decimal)
int("  42 ")       # 42   (recorta espacios)
int("3.0")         # ValueError: no acepta punto decimal
```

> [!warning] `int(float)` trunca hacia cero
> `int(x)` sobre un `float` **trunca** (no redondea) y descarta la parte fraccionaria: `int(3.9)` → `3`, `int(-3.9)` → `-3`. Para redondear usa `round()`; para piso/techo `math.floor`/`math.ceil`.

## Operaciones aritméticas
Los enteros soportan las operaciones aritméticas estándar. Es vital distinguir entre los dos tipos de división:

| Operación        | Función                                              | Ejemplo                   |
| ---------------- | ---------------------------------------------------- | ------------------------- |
| `+` `-` `*`      | Suma, resta, multiplicación. Resultado `int`.        | `3 * 4` → `12`            |
| `/`              | División real. **Siempre** devuelve `float`.         | `10 / 2` → `5.0`          |
| `//`             | División entera (piso). Devuelve la parte entera.    | `7 // 2` → `3`            |
| `%`              | Módulo. Devuelve el residuo.                         | `7 % 2` → `1`             |
| `**`             | Potenciación. Eleva a una potencia.                  | `2 ** 3` → `8`            |
| `divmod(a, b)`   | Tupla `(a // b, a % b)` en una sola operación.       | `divmod(7, 2)` → `(3, 1)` |

### Piso, módulo y signo
`//` redondea hacia **menos infinito** (piso), no hacia cero. El signo de `%` sigue al **divisor**. Se cumple siempre la invariante `(a // b) * b + (a % b) == a`.

```python
7 // 2      #  3
-7 // 2     # -4   (piso, no -3)
7 // -2     # -4
-7 // -2    #  3

7 % 3       #  1
-7 % 3      #  2   (signo del divisor)
7 % -3      # -2
divmod(-7, 3)   # (-3, 2)
```

> [!info] Truncamiento vs piso
> Para obtener división truncada hacia cero (como C/Java) usa `math.trunc(a / b)` o el patrón `int(a / b)` con precaución de precisión, o `math.fmod` para módulo con signo del dividendo.

### Potenciación y `pow`
`**` y `pow()` son equivalentes en dos argumentos. La forma de **tres argumentos** `pow(base, exp, mod)` calcula `(base ** exp) % mod` de manera eficiente (exponenciación modular), clave en criptografía.

```python
2 ** 10            # 1024
pow(2, 10)         # 1024
pow(2, 1000) % 7   # calcula el gigante y LUEGO el módulo
pow(2, 1000, 7)    # 2   mismo resultado, sin materializar el número enorme

pow(3, -1, 7)      # 5   inverso modular (exp negativo requiere mod, 3.8+)
2 ** -1            # 0.5 (exp negativo sin mod -> float)
```

> [!note] Operadores adicionales
> Para ver más operadores (asignación aumentada, comparación, etc.) revisar [[Operadores de Variables | Operadores de Variable]].

## Precisión arbitraria y memoria
Esta es una de las características más interesantes de Python. Mientras lenguajes como Java o C++ tienen un límite máximo para un entero (usualmente $2^{63}-1$ para un _long_ de 64 bits), Python maneja el crecimiento de forma dinámica.

**Funcionamiento:** un `int` de CPython se almacena como un arreglo de "dígitos" de 30 bits (en builds de 64 bits). Cuando un número supera el tamaño de palabra del procesador, Python **expande automáticamente** la memoria del objeto agregando más dígitos.

- **Sin desbordamiento (Overflow):** no existe `OverflowError` en operaciones con enteros; el número crece hasta agotar la RAM.
- **Coste:** la aritmética sobre enteros pequeños es O(1); sobre enteros enormes, las operaciones escalan con el número de dígitos.
- **Ejemplo:** puedes calcular $2^{1000}$ y Python entrega el número exacto con todos sus dígitos.

```python
import sys
sys.getsizeof(0)            # 28  (objeto vacío)
sys.getsizeof(2**30)        # 32  (un "dígito" extra)
sys.getsizeof(2**1000)      # 160 (memoria crece con la magnitud)
2 ** 1000                   # 10715086071862673209484250490600018105...
```

> [!warning] Límite de conversión a/desde `str` (3.11+)
> Por seguridad (DoS), convertir enteros con más de **4300 dígitos** a/desde texto lanza `ValueError`. Ajustable con `sys.set_int_max_str_digits()`. No afecta la aritmética, solo `str(n)`/`int(s)`.
> ```python
> str(10 ** 5000)   # ValueError: Exceeds the limit (4300 digits)
> ```

## Operaciones de bits
Operan sobre la representación binaria en **complemento a dos** (los enteros negativos se tratan como una secuencia infinita de bits de signo a la izquierda).

| Operador | Nombre              | Descripción                                | Ejemplo (`a=12 0b1100`, `b=10 0b1010`) |
| -------- | ------------------- | ------------------------------------------ | -------------------------------------- |
| `&`      | AND                 | 1 si **ambos** bits son 1                  | `a & b` → `8` (`0b1000`)               |
| `\|`     | OR                  | 1 si **alguno** es 1                        | `a \| b` → `14` (`0b1110`)             |
| `^`      | XOR                 | 1 si **difieren**                          | `a ^ b` → `6` (`0b0110`)               |
| `~`      | NOT (complemento)   | Invierte bits: `~x == -(x+1)`              | `~12` → `-13`                          |
| `<<`     | Desplazar izquierda | Multiplica por `2**n`                      | `3 << 2` → `12`                        |
| `>>`     | Desplazar derecha   | Divide por `2**n` (piso)                   | `13 >> 2` → `3`                        |

```python
0b1100 & 0b1010    # 8   AND
0b1100 | 0b1010    # 14  OR
0b1100 ^ 0b1010    # 6   XOR
~0b1100            # -13 (~x = -(x+1))
3 << 4             # 48  (3 * 2**4)
255 >> 1           # 127 (255 // 2)

# Patrones idiomáticos
n = 13
n & 1              # 1  -> impar (bit menos significativo)
flags = 0
flags |= 0b0100    # activar un flag
flags &= ~0b0100   # apagar un flag
mask = (1 << 8) - 1  # 255, máscara de 8 bits
```

> [!tip] XOR para intercambiar / detectar
> `a ^ b ^ b == a`. Se usa para intercambiar sin variable temporal (`a ^= b; b ^= a; a ^= b`) y para hallar el único elemento sin par en una lista (`reduce(xor, lista)`).

## Métodos y conversiones del `int`
El tipo `int` expone métodos para inspección de bits y serialización.

| Método / función           | Resultado                                                        | Ejemplo                                |
| -------------------------- | --------------------------------------------------------------- | -------------------------------------- |
| `n.bit_length()`           | Bits necesarios para representar `abs(n)` (sin signo)           | `(255).bit_length()` → `8`             |
| `n.bit_count()` (3.10+)    | Número de bits en 1 (peso de Hamming) de `abs(n)`               | `(7).bit_count()` → `3`                |
| `n.to_bytes(len, order)`   | Serializa a `bytes` (`order='big'`/`'little'`)                  | `(255).to_bytes(2,'big')` → `b'\x00\xff'` |
| `int.from_bytes(b, order)` | Deserializa `bytes` a `int`                                     | `int.from_bytes(b'\xff','big')` → `255`   |
| `n.as_integer_ratio()`     | Tupla `(numerador, denominador)`; para `int` siempre `(n, 1)`   | `(5).as_integer_ratio()` → `(5, 1)`    |
| `bin(n)` / `oct(n)` / `hex(n)` | Cadena con prefijo en base 2 / 8 / 16                       | `hex(255)` → `'0xff'`                   |
| `format(n, fmt)`           | Formato sin prefijo / con relleno                              | `format(255,'08b')` → `'11111111'`     |

```python
n = 255

n.bit_length()              # 8
n.bit_count()               # 8   (255 = 0b11111111)
(-7).bit_count()            # 3   (usa abs)

bin(255)                    # '0b11111111'
oct(255)                    # '0o377'
hex(255)                    # '0xff'
format(255, '#06x')         # '0x00ff'  (prefijo + relleno)
f"{255:08b}"                # '11111111'

# Serialización binaria (red, archivos, protocolos)
n.to_bytes(4, 'big')        # b'\x00\x00\x00\xff'
n.to_bytes(4, 'little')     # b'\xff\x00\x00\x00'
int.from_bytes(b'\x01\x00', 'big')     # 256
int.from_bytes(b'\xff', 'big', signed=True)   # -1

(5).as_integer_ratio()      # (5, 1)
```

> [!info] `to_bytes` sin argumentos (3.11+)
> Desde 3.11 `length` y `byteorder` tienen defaults (`length=1`, `byteorder='big'`), por lo que `(255).to_bytes()` → `b'\xff'`. Con `signed=False` (default), un valor que no cabe lanza `OverflowError`.

## Comparación y `bool` como `int`
Los enteros soportan los operadores de comparación (`<`, `<=`, `>`, `>=`, `==`, `!=`) y **encadenamiento** (`0 < x < 10`). Comparan por valor matemático, incluso entre tipos numéricos (`int` vs `float` vs `bool`).

```python
1 == 1.0           # True   (compara por valor)
0 < 5 < 10         # True   (encadenado: 0<5 and 5<10)
2 ** 100 > 10**30  # True   (precisión exacta, sin error de float)
```

`bool` es **subclase de `int`**: `True` vale `1` y `False` vale `0`. Esto permite usar booleanos en aritmética y como índices.

```python
True + True        # 2
False * 10         # 0
sum([True, True, False, True])   # 3   (contar verdaderos)
[10, 20][True]     # 20  (True actúa como índice 1)
isinstance(True, int)   # True
True == 1          # True
True is 1          # False (mismo valor, objetos distintos)
```

> [!note] Tipos numéricos hermanos
> El [[04 Booleanos (bool) | bool]] es una **subclase de `int`** (`True == 1`, `False == 0`). Para decimales con punto flotante ver [[02 Flotantes (float) | float]] y para números con parte imaginaria ver [[03 Complejos (complex) | complex]].
