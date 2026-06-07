---
title: sympy.factorial_binomial — factorial, binomial y doble factorial
aliases: [factorial, binomial, factorial2, doble factorial, coeficiente binomial]
tags: [sympy, api/funcion, functions/especiales]
lib: sympy
mod: sympy.functions
tipo: concepto
draft: false
---

# sympy.factorial_binomial — factorial, binomial y doble factorial

Esta nota agrupa las tres funciones combinatorias fundamentales de `sympy.functions`: `factorial(n)`, `binomial(n, k)` y `factorial2(n)`. Las tres operan de forma **exacta** sobre enteros y permanecen **sin evaluar** cuando reciben argumentos simbolicos, lo que las hace utiles tanto para calculos numericos directos como para manipulacion algebraica de series de potencias, coeficientes binomiales y expresiones combinatorias. Se relacionan entre si a traves de la [[sympy.gamma|funcion gamma]]: `factorial(n) == gamma(n+1)`.

## Firmas

```python
sympy.factorial(n)        -> Integer | Expr
sympy.binomial(n, k)      -> Integer | Expr
sympy.factorial2(n)       -> Integer | Expr
```

| Funcion | Parametros | Descripcion |
|---------|------------|-------------|
| `factorial(n)` | `n`: entero no negativo o simbolo | `n! = 1*2*...*n` |
| `binomial(n, k)` | `n`, `k`: enteros o simbolos | `C(n,k) = n! / (k! * (n-k)!)` |
| `factorial2(n)` | `n`: entero no negativo o simbolo | `n!! = n*(n-2)*...*` hasta 1 o 2 |

## Valor de retorno

| Funcion | Argumento entero | Argumento simbolico |
|---------|-----------------|---------------------|
| `factorial` | `Integer` exacto | `factorial(n)` sin evaluar |
| `binomial` | `Integer` exacto | `binomial(n, k)` sin evaluar |
| `factorial2` | `Integer` exacto | `factorial2(n)` sin evaluar |

## Casos de uso

### Valores numericos directos

```python
from sympy import factorial, binomial, factorial2

factorial(5)    # 120       (5! = 5*4*3*2*1)
factorial(0)    # 1         (por convencion)
factorial(10)   # 3628800

binomial(5, 2)  # 10        (C(5,2) = 10)
binomial(6, 3)  # 20
binomial(10, 0) # 1

factorial2(5)   # 15        (5!! = 5*3*1)
factorial2(6)   # 48        (6!! = 6*4*2)
factorial2(7)   # 105       (7!! = 7*5*3*1)
factorial2(8)   # 384       (8!! = 8*6*4*2)
```

### Expresiones simbolicas

Cuando el argumento es un simbolo, las funciones quedan sin evaluar y pueden combinarse algebraicamente.

```python
from sympy import symbols, factorial, binomial, factorial2

n, k = symbols("n k")

factorial(n)    # factorial(n)
binomial(n, k)  # binomial(n, k)
binomial(n, 2)  # binomial(n, 2)   (no simplifica automaticamente)

# Para obtener la forma racional:
binomial(n, 2).rewrite(factorial)   # factorial(n)/(2*factorial(n - 2))
```

### Relacion con gamma

`factorial(n) == gamma(n+1)` para enteros no negativos. Se puede reescribir en cualquier sentido.

```python
from sympy import symbols, factorial, gamma, Rational

n = symbols("n", positive=True, integer=True)

factorial(5)          # 120
gamma(6)              # 120    (= 5! = gamma(5+1))

# Reescritura:
factorial(n).rewrite(gamma)   # gamma(n + 1)
```

### Uso en series de potencias (coeficientes)

```python
from sympy import symbols, binomial, factorial, expand

n, x = symbols("n x")

# Termino k-esimo del desarrollo de (1+x)^n:
k = symbols("k", nonneg=True, integer=True)
# Coeficiente: binomial(n, k) * x**k
binomial(5, 0) + binomial(5, 1) + binomial(5, 2) + binomial(5, 3) + binomial(5, 4) + binomial(5, 5)
# 1 + 5 + 10 + 10 + 5 + 1 = 32 = 2**5
```

## Errores comunes

| Error | Causa | Solucion |
|-------|-------|----------|
| `factorial(-1)` | El factorial no esta definido para negativos | Verificar dominio; usar `gamma` para extensiones |
| Confundir `factorial2(n)` con `factorial(n/2)` | Son funciones distintas; `factorial2` salta de 2 en 2 | Recordar: `n!! = n*(n-2)*...*1` o `...*2` |
| `binomial(n, 2)` no simplifica | SymPy lo deja como `binomial(n, 2)` | Usar `.rewrite(factorial)` o `expand` |
| Esperar `factorial(n) == gamma(n)` | La relacion es `factorial(n) == gamma(n+1)` | El desplazamiento de 1 es la diferencia |

## Limitaciones

- `factorial` y `factorial2` solo estan definidas para enteros no negativos; para argumentos negativos o no enteros, usar [[sympy.gamma]].
- `binomial(n, k)` con `k` simbolico no siempre simplifica a una forma racional; usar `.rewrite(factorial)` si se necesita forma explicita.
- El doble factorial `factorial2` no tiene una relacion tan directa con `gamma` fuera de casos especificos (semienteros).

## Notas relacionadas

- [[sympy.gamma]]
- [[sympy.functions/especiales/index | especiales]]
- [[sympy.functions/index | sympy.functions]]
