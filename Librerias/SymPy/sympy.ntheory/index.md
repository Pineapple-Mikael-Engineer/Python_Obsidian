---
title: sympy.ntheory — teoria de numeros entera
tags:
  - sympy
  - indice
draft: false
---

# sympy.ntheory — teoria de numeros entera

`sympy.ntheory` agrupa las funciones de **teoria de numeros** que operan sobre enteros Python concretos: verificar primalidad, descomponer en factores primos, recorrer primos en un rango y calcular MCD/MCM. La diferencia critica con el resto de SymPy es que estas funciones no trabajan con expresiones simbolicas (`Expr`, `Symbol`): reciben y devuelven `int`. No hay algebra simbolica aqui; hay aritmetica entera pura.

El ejemplo siguiente encadena las cuatro funciones del submodulo para analizar los enteros en un rango:

```python
from sympy import isprime, factorint, primerange
from sympy.ntheory import igcd, ilcm

# Primos entre 10 y 30
primos = list(primerange(10, 30))     # [11, 13, 17, 19, 23, 29]

# Verificar que todos son primos
all(isprime(p) for p in primos)       # True

# Factorizar los compuestos del mismo rango
for n in range(10, 30):
    if not isprime(n):
        print(n, factorint(n))
# 10 {2: 1, 5: 1}
# 12 {2: 2, 3: 1}
# ...

# MCD y MCM de dos primos del rango
igcd(11, 13)    # 1   -> coprimos (todo par de primos distintos lo es)
ilcm(11, 13)    # 143
```

## Como se relacionan

La decision clave es **que quieres hacer** con los enteros:

| Funcion | Que hace | Devuelve | Cuando usarla |
|---------|----------|----------|---------------|
| [[sympy.isprime]] | Test de primalidad | `bool` | Verificar si un entero concreto es primo; filtrar candidatos |
| [[sympy.factorint]] | Descomposicion en primos | `dict {primo: exp}` | Conocer la estructura multiplicativa de `n`; calcular divisores |
| [[sympy.primerange]] | Generador de primos en `[a, b)` | `generator` | Iterar sobre todos los primos de un rango sin cargar en memoria |
| [[sympy.gcd_entero]] | MCD/MCM de enteros | `int` | Simplificar fracciones, calcular periodos, verificar coprimalidad |

Arbol de decision:

- ¿Solo necesitas saber si un numero es primo? -> [[sympy.isprime]].
- ¿Necesitas la estructura completa de factores (con exponentes)? -> [[sympy.factorint]].
- ¿Necesitas todos los primos de un rango, o el primo mas cercano a un valor? -> [[sympy.primerange]] (o `nextprime`/`prevprime` que viven en el mismo modulo).
- ¿Necesitas el MCD o MCM de dos o mas enteros? -> [[sympy.gcd_entero]] (`igcd`/`ilcm`).

> [!info] ntheory vs polys
> `sympy.ntheory` trabaja con enteros Python (`int`). `sympy.polys` trabaja con polinomios (`Expr`, `Poly`). El `igcd` de `ntheory` devuelve un `int`; el `gcd` de `polys` devuelve una `Expr`. Cuando tengas enteros concretos, usa siempre `ntheory`.

## Notas

- [[sympy.isprime]] — test de primalidad determinista (para `n < 2^64`) o probabilistico. Punto de partida para cualquier filtrado de primos.
- [[sympy.factorint]] — descompone `n` en `{primo: exponente}`. La funcion mas rica del submodulo; base para calcular divisores, funcion de Euler y propiedades multiplicativas.
- [[sympy.primerange]] — generador lazy de primos en `[a, b)`; incluye `nextprime` y `prevprime` para navegar puntualmente.
- [[sympy.gcd_entero]] — agrupa `igcd` y `ilcm`; acepta multiples argumentos y opera siempre sobre `int`.

## Notas relacionadas

- [[SymPy/index | SymPy]]
