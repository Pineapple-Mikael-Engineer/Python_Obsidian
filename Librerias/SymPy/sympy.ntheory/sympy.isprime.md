---
title: sympy.isprime — verificar si un entero es primo
aliases:
  - isprime
  - primo
tags:
  - sympy
  - api/funcion
  - ntheory
lib: sympy
mod: sympy.ntheory
tipo: funcion
retorna: bool
requiere: []
draft: false
---

# sympy.isprime — verificar si un entero es primo

`isprime(n)` devuelve `True` si el entero `n` es primo y `False` en cualquier otro caso. Opera directamente sobre **enteros Python** (no sobre `Expr` simbolicas): la entrada debe ser un `int`. Es el punto de partida habitual de cualquier algoritmo de teoria de numeros que necesite confirmar primalidad antes de factorizar, generar primos o calcular funciones aritmeticas.

> El resultado es **determinista** para `n < 2^64`: usa tests de Miller-Rabin con un conjunto fijo de testigos que cubren ese rango sin error. Para `n >= 2^64` el test es **probabilistico** (muy alta confianza, pero no garantia absoluta).

## Firma

```python
sympy.isprime(
    n,    # int: el entero a verificar
) -> bool
```

## Valor de retorno

| Valor | Significado |
|-------|-------------|
| `True` | `n` es primo |
| `False` | `n` no es primo (incluye negativos, 0, 1 y compuestos) |

```python
from sympy import isprime
isprime(7)           # True
isprime(12)          # False
isprime(1)           # False  (1 no es primo por definicion)
isprime(0)           # False
isprime(-5)          # False
```

## Formas basicas de llamada

| Objetivo | Llamada |
|----------|---------|
| Verificar un entero pequeno | `isprime(n)` |
| Verificar un primo de Mersenne | `isprime(2**31 - 1)` |
| Filtrar una lista de enteros | `[x for x in rango if isprime(x)]` |
| Usar como predicado en generador | `filter(isprime, iterable)` |

```python
from sympy import isprime
isprime(2)           # True
isprime(2**31 - 1)   # True   (primo de Mersenne M31)
isprime(2**32 - 1)   # False  (= 3 * 5 * 17 * 257 * 65537)
```

## Parametros en detalle

### `n` (obligatorio)

Entero Python (`int`). Admite enteros grandes arbitrariamente:

```python
from sympy import isprime
# Primo de Mersenne grande (determinista porque < 2^64)
isprime(2**61 - 1)    # True
# Numero grande > 2^64 (test probabilistico)
isprime(10**30 + 7)   # True   (con muy alta probabilidad)
```

Pasar un `float`, una `Expr` simbolica u otro tipo no esta soportado: convertir a `int` antes con `int(n)`.

## Casos de uso

### Verificar candidatos primos en un calculo

```python
from sympy import isprime

candidatos = [2, 3, 4, 5, 97, 100, 101]
primos = [n for n in candidatos if isprime(n)]
# [2, 3, 5, 97, 101]
```

### Combinar con [[sympy.factorint]] para confirmar primalidad antes de factorizar

```python
from sympy import isprime, factorint

n = 360
if not isprime(n):
    print(factorint(n))   # {2: 3, 3: 2, 5: 1}
```

### Generar el primer primo mayor que un valor

```python
from sympy import isprime

n = 100
while not isprime(n):
    n += 1
# n = 101  (equivalente a nextprime(100))
```

## Errores comunes

| Error | Causa | Solucion |
|-------|-------|----------|
| `isprime` devuelve `False` para un primo conocido | Se paso un `float` (`2.0`) en vez de `int` | Convertir: `isprime(int(x))` |
| Confundir determinista con probabilistico | Para `n > 2^64` el resultado puede (rara vez) ser incorrecto | Aceptable en la practica; para certeza absoluta usar tests adicionales |
| Aplicar sobre una `Symbol` de SymPy | `isprime` no opera sobre `Expr` simbolicas | Solo funciona con enteros Python concretos |
| Asumir que `isprime(1)` es `True` | Por convenio matematico, 1 no es primo | Correcto: devuelve `False` |

## Notas relacionadas

- [[sympy.factorint]]
- [[sympy.primerange]]
- [[sympy.gcd_entero]]
- [[sympy.ntheory/index | sympy.ntheory]]
- [[SymPy/index | SymPy]]
