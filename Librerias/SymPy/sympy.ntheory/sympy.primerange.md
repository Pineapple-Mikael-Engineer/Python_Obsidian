---
title: sympy.primerange — generador de primos en un rango
aliases:
  - primerange
  - nextprime
  - prevprime
  - primos en rango
tags:
  - sympy
  - api/funcion
  - ntheory
lib: sympy
mod: sympy.ntheory
tipo: funcion
retorna: generator
requiere: []
draft: false
---

# sympy.primerange — generador de primos en un rango

`primerange(a, b)` es un **generador** que produce todos los primos en el intervalo `[a, b)` de forma lazy: no construye la lista completa en memoria, sino que los entrega uno a uno. Es la herramienta correcta cuando se necesita **iterar** sobre primos dentro de un rango, especialmente si el rango es grande. Para navegar puntualmente a partir de un entero conocido, las funciones complementarias `nextprime(n)` y `prevprime(n)` devuelven el primo inmediato siguiente o anterior a `n`.

> `primerange` no es una lista: es un generador. Si necesitas indexar (`primes[0]`), envuelve con `list(primerange(a, b))`. Para un primo concreto por posicion existe `prime(k)` (el k-esimo primo).

## Firma

```python
sympy.primerange(
    a,    # int: inicio del rango (inclusive si a es primo)
    b,    # int: fin del rango (exclusivo)
) -> generator[int]

sympy.nextprime(
    n,          # int: entero de referencia
    ith=1,      # int: cuantos primos adelante (por defecto el inmediato)
) -> int

sympy.prevprime(
    n,    # int: entero de referencia (debe haber al menos un primo antes)
) -> int
```

## Valor de retorno

| Funcion | Tipo | Ejemplo |
|---------|------|---------|
| `primerange(a, b)` | `generator` de `int` | `primerange(10, 30)` -> `11, 13, 17, 19, 23, 29` |
| `nextprime(n)` | `int` | `nextprime(10)` -> `11` |
| `prevprime(n)` | `int` | `prevprime(10)` -> `7` |

```python
from sympy import primerange, nextprime, prevprime

list(primerange(10, 30))   # [11, 13, 17, 19, 23, 29]
nextprime(10)              # 11
prevprime(10)              # 7
```

## Formas basicas de llamada

| Objetivo | Llamada |
|----------|---------|
| Lista de primos en `[a, b)` | `list(primerange(a, b))` |
| Iterar sin materializar en memoria | `for p in primerange(a, b):` |
| Primo inmediato siguiente a `n` | `nextprime(n)` |
| Primo inmediato anterior a `n` | `prevprime(n)` |
| Segundo primo siguiente a `n` | `nextprime(n, 2)` |
| Numero de primos en `[a, b)` | `sum(1 for _ in primerange(a, b))` |

```python
from sympy import primerange, nextprime, prevprime

list(primerange(1, 20))    # [2, 3, 5, 7, 11, 13, 17, 19]
list(primerange(2, 3))     # [2]
list(primerange(4, 7))     # [5]
nextprime(97)              # 101
nextprime(10, 2)           # 13   -> segundo primo despues de 10
prevprime(11)              # 7
```

## Parametros en detalle

### `a`, `b` en `primerange`

El rango es **cerrado por la izquierda y abierto por la derecha**: `[a, b)`. Si `a` es primo, se incluye; si `b` es primo, no se incluye.

```python
from sympy import primerange
list(primerange(11, 13))   # [11]   -> 11 incluido, 13 excluido
list(primerange(11, 14))   # [11, 13]
list(primerange(14, 11))   # []     -> rango vacio si a >= b
```

### `ith` en `nextprime`

Permite saltar varios primos de golpe. `nextprime(n, ith=k)` devuelve el k-esimo primo estrictamente mayor que `n`.

```python
from sympy import nextprime
nextprime(10, 1)    # 11
nextprime(10, 3)    # 17   -> tercer primo despues de 10
```

## Casos de uso

### Sumatoria sobre primos menores que N

```python
from sympy import primerange
N = 100
suma = sum(primerange(2, N))    # 1060
```

### Generar tabla de primos en un rango

```python
from sympy import primerange
for p in primerange(50, 80):
    print(p, end=" ")
# 53 59 61 67 71 73 79
```

### Usar con [[sympy.factorint]] e [[sympy.isprime]] en un pipeline

```python
from sympy import isprime, factorint, primerange

# Primos entre 100 y 130
primos = list(primerange(100, 130))   # [101, 103, 107, 109, 113, 127]

# Compuestos en ese rango y su factorizacion
for n in range(100, 130):
    if not isprime(n):
        print(n, factorint(n))
# 100 {2: 2, 5: 2}
# 102 {2: 1, 3: 1, 17: 1}
# ...
```

### Salto entre primos consecutivos (brechas)

```python
from sympy import nextprime
p = 2
for _ in range(10):
    q = nextprime(p)
    print(f"brecha entre {p} y {q}: {q - p}")
    p = q
```

## Errores comunes

| Error | Causa | Solucion |
|-------|-------|----------|
| `primerange(a, b)[0]` falla | Es un generador, no una lista | `list(primerange(a, b))[0]` o usar `next(primerange(a, b))` |
| `prevprime(2)` lanza excepcion | No existe primo anterior a 2 | Verificar que `n > 2` antes de llamar |
| Rango muy grande materializado en lista | `list(primerange(2, 10**8))` usa mucha RAM | Iterar con `for p in primerange(...)` sin convertir a lista |
| `primerange(a, b)` no incluye `b` | El limite superior es exclusivo | Usar `primerange(a, b+1)` si se quiere incluir `b` |

## Notas relacionadas

- [[sympy.isprime]]
- [[sympy.factorint]]
- [[sympy.gcd_entero]]
- [[sympy.ntheory/index | sympy.ntheory]]
- [[SymPy/index | SymPy]]
