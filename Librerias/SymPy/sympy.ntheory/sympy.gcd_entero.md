---
title: sympy.igcd / sympy.ilcm — MCD y MCM de enteros
aliases:
  - igcd
  - ilcm
  - mcd enteros
  - mcm enteros
tags:
  - sympy
  - api/funcion
  - ntheory
lib: sympy
mod: sympy.ntheory
tipo: concepto
requiere: []
draft: false
---

# sympy.igcd / sympy.ilcm — MCD y MCM de enteros

`igcd` y `ilcm` calculan el **maximo comun divisor** (MCD) y el **minimo comun multiplo** (MCM) de dos o mas enteros Python. Operan directamente sobre `int`, devuelven `int`, y aceptan multiples argumentos aplicando la operacion de forma acumulativa. Son las funciones de aritmetica entera pura de SymPy.

> `igcd`/`ilcm` no deben confundirse con `sympy.gcd` del submodulo `polys`. `sympy.gcd` opera sobre **polinomios** (recibe `Expr` o `Poly`) y devuelve una `Expr`. `igcd` opera sobre **enteros Python** y devuelve un `int`. Para enteros, usa siempre `igcd`/`ilcm`.

## Firma

```python
sympy.igcd(
    *args,    # int...: dos o mas enteros
) -> int

sympy.ilcm(
    *args,    # int...: dos o mas enteros
) -> int
```

Ambas funciones viven en `sympy.ntheory` y se importan desde ahi (o directamente desde `sympy` si estan re-exportadas en la version instalada).

```python
from sympy.ntheory import igcd, ilcm
```

## Valor de retorno

| Funcion | Tipo | Semantica |
|---------|------|-----------|
| `igcd(*args)` | `int` | Mayor entero que divide a todos los argumentos |
| `ilcm(*args)` | `int` | Menor entero positivo divisible por todos los argumentos |

```python
from sympy.ntheory import igcd, ilcm

igcd(12, 18)        # 6
ilcm(4, 6)          # 12
igcd(12, 18, 24)    # 6
ilcm(4, 6, 10)      # 60
```

## Formas basicas de llamada

| Objetivo | Llamada |
|----------|---------|
| MCD de dos enteros | `igcd(a, b)` |
| MCM de dos enteros | `ilcm(a, b)` |
| MCD de tres o mas enteros | `igcd(a, b, c, ...)` |
| MCM de tres o mas enteros | `ilcm(a, b, c, ...)` |
| MCD de una lista | `igcd(*lista)` |
| Verificar si son coprimos | `igcd(a, b) == 1` |

```python
from sympy.ntheory import igcd, ilcm

igcd(48, 36)             # 12
ilcm(12, 15)             # 60
igcd(100, 75, 50)        # 25
ilcm(3, 4, 5)            # 60
igcd(*[12, 18, 24, 36])  # 6    -> desempaquetar lista
igcd(7, 11) == 1         # True  -> coprimos
```

## Relacion con `sympy.gcd` (polys)

Esta es la diferencia critica de esta carpeta respecto al resto de SymPy:

| Funcion | Modulo | Entrada | Salida | Para que |
|---------|--------|---------|--------|---------|
| `igcd` | `sympy.ntheory` | `int` | `int` | MCD de enteros concretos |
| `ilcm` | `sympy.ntheory` | `int` | `int` | MCM de enteros concretos |
| `sympy.gcd` | `sympy.polys` | `Expr \| Poly` | `Expr` | MCD de polinomios simbolicos |

```python
from sympy.ntheory import igcd
from sympy import gcd, symbols

x = symbols("x")
igcd(12, 18)                # 6         -> enteros
gcd(x**2 - 1, x**2 - x)    # x - 1     -> polinomios
```

## Casos de uso

### Simplificar fracciones manualmente

```python
from sympy.ntheory import igcd

num, den = 360, 480
d = igcd(num, den)    # 120
print(num // d, "/", den // d)   # 3 / 4
```

### Calcular el periodo de una senal combinada (MCM de periodos)

```python
from sympy.ntheory import ilcm

T1, T2, T3 = 4, 6, 10
T_total = ilcm(T1, T2, T3)   # 60
```

### Verificar coprimalidad en criptografia basica

```python
from sympy.ntheory import igcd

def son_coprimos(a, b):
    return igcd(a, b) == 1

son_coprimos(7, 11)    # True
son_coprimos(6, 9)     # False
```

### Combinar con [[sympy.factorint]] para aritmetica modulada

```python
from sympy.ntheory import igcd
from sympy import factorint

# Confirmar que el MCD coincide con la factorizacion comun
a, b = 360, 252
print(igcd(a, b))          # 36
print(factorint(a))        # {2: 3, 3: 2, 5: 1}
print(factorint(b))        # {2: 2, 3: 2, 7: 1}
# comun: {2:2, 3:2} = 4 * 9 = 36  ✓
```

## Errores comunes

| Error | Causa | Solucion |
|-------|-------|----------|
| Usar `sympy.gcd(a, b)` con enteros y obtener `Expr` | `gcd` de polys envuelve el resultado en `Expr` | Usar `igcd(a, b)` para operar con `int` directamente |
| `ilcm(0, n)` devuelve `0` | Por definicion matematica `lcm(0, n) = 0` | Verificar que los argumentos no sean cero |
| Pasar `float` o `Expr` simbolica | `igcd`/`ilcm` esperan `int` | Convertir con `int(n)` o usar `gcd` de polys segun el caso |
| `igcd` con un solo argumento | Comportamiento no definido de forma util | Siempre pasar al menos dos argumentos |

## Notas relacionadas

- [[sympy.factorint]]
- [[sympy.isprime]]
- [[sympy.primerange]]
- [[sympy.ntheory/index | sympy.ntheory]]
- [[SymPy/index | SymPy]]
