---
title: sympy.factorint — factorizacion entera en primos
aliases:
  - factorint
  - factorizacion entera
tags:
  - sympy
  - api/funcion
  - ntheory
lib: sympy
mod: sympy.ntheory
tipo: funcion
retorna: dict
requiere: []
draft: false
---

# sympy.factorint — factorizacion entera en primos

`factorint(n)` descompone un entero `n` en sus **factores primos** y devuelve un `dict` de la forma `{primo: exponente}`. Es la funcion central de teoria de numeros entera en SymPy: a partir de su resultado se pueden calcular divisores, la funcion de Euler, el MCD y cualquier propiedad multiplicativa de `n`. Opera sobre **enteros Python**, no sobre polinomios ni expresiones simbolicas.

> `factorint` no debe confundirse con `sympy.gcd` del submodulo `polys`, que opera sobre polinomios (`Poly`). Para factorizar un **entero**, usa siempre `factorint`; para factorizar un **polinomio** en irreducibles, usa `factor`.

## Firma

```python
sympy.factorint(
    n,                    # int: el entero a factorizar
    limit=None,           # int | None: maximo factor primo a probar (criba parcial)
    use_trial=True,       # bool: usar division por prueba
    use_rho=True,         # bool: usar algoritmo rho de Pollard
    use_pm1=True,         # bool: usar algoritmo p-1 de Pollard
    visual=False,         # bool: devolver Mul legible en vez de dict
    multiple=False,       # bool: devolver lista de factores (con repeticion)
) -> dict | Expr | list
```

## Valor de retorno

| Modo | Tipo | Ejemplo para `n = 360` |
|------|------|------------------------|
| Por defecto | `dict {primo: exp}` | `{2: 3, 3: 2, 5: 1}` |
| `visual=True` | `Expr` (`Mul`) | `2**3 * 3**2 * 5**1` |
| `multiple=True` | `list` de primos | `[2, 2, 2, 3, 3, 5]` |

```python
from sympy import factorint
factorint(360)                 # {2: 3, 3: 2, 5: 1}
factorint(360, visual=True)    # 2**3*3**2*5
factorint(360, multiple=True)  # [2, 2, 2, 3, 3, 5]
```

## Formas basicas de llamada

| Objetivo | Llamada |
|----------|---------|
| Factorizacion estandar | `factorint(n)` |
| Representacion legible | `factorint(n, visual=True)` |
| Lista de factores con repeticion | `factorint(n, multiple=True)` |
| Criba hasta un limite (factores grandes quedan) | `factorint(n, limit=100)` |
| Solo factores primos (claves del dict) | `factorint(n).keys()` |
| Exponentes de la factorizacion | `factorint(n).values()` |

```python
from sympy import factorint
factorint(12)                  # {2: 2, 3: 1}
factorint(1)                   # {}             -> producto vacio
factorint(-12)                 # {-1: 1, 2: 2, 3: 1}
```

## Parametros en detalle

### `n` (obligatorio)

Entero Python. Acepta negativos (agrega `-1: 1` al dict) y `1` (dict vacio).

```python
from sympy import factorint
factorint(2**10)               # {2: 10}
factorint(-7)                  # {-1: 1, 7: 1}
```

### `limit`

Si se indica, `factorint` solo busca factores primos `<= limit`. Los cofactores restantes (posiblemente no primos) quedan en el dict marcados como posibles compuestos. Util para comprobar rapidamente si `n` tiene factores pequenos sin completar la factorizacion entera.

```python
from sympy import factorint
# 1001 = 7 * 11 * 13; con limit=10 solo encuentra 7, el resto queda como cofactor
factorint(1001, limit=10)      # {7: 1, 143: 1}  (143 = 11*13, no primo)
factorint(1001)                # {7: 1, 11: 1, 13: 1}
```

### `visual=True`

Devuelve una `Expr` de SymPy (producto de potencias) en vez del dict. Comodo para mostrar, no para calcular.

```python
from sympy import factorint
factorint(360, visual=True)    # 2**3*3**2*5
```

## Casos de uso

### Obtener todos los divisores de un numero

```python
from sympy import factorint, divisors
n = 360
factores = factorint(n)        # {2: 3, 3: 2, 5: 1}
divisors(n)                    # [1, 2, 3, 4, 5, 6, 8, 9, 10, ...]
```

### Verificar si es potencia de primo

```python
from sympy import factorint
def es_potencia_de_primo(n):
    d = factorint(n)
    return len(d) == 1

es_potencia_de_primo(8)        # True   (2**3)
es_potencia_de_primo(12)       # False  ({2:2, 3:1})
```

### Combinar con [[sympy.isprime]] en un pipeline

```python
from sympy import isprime, factorint, primerange

numeros = list(primerange(2, 50))
# factorizar solo los compuestos entre 2 y 100
compuestos = [n for n in range(2, 101) if not isprime(n)]
for n in compuestos[:5]:
    print(n, factorint(n))
# 4  {2: 2}
# 6  {2: 1, 3: 1}
# 8  {2: 3}
# 9  {3: 2}
# 10 {2: 1, 5: 1}
```

## Errores comunes

| Error | Causa | Solucion |
|-------|-------|----------|
| Pasar un `float` | `factorint(3.0)` falla | Convertir: `factorint(int(n))` |
| Esperar factorizacion de polinomios | `factorint` es solo para enteros | Para polinomios usar `factor(expr)` |
| Confundir `limit` con "maximo primo" | Con `limit` los cofactores grandes no son necesariamente primos | Revisar si las claves del dict son primas con [[sympy.isprime]] |
| `factorint(1)` devuelve `{}` | Correcto: 1 es el producto vacio | No hay factores primos de 1 |

## Notas relacionadas

- [[sympy.isprime]]
- [[sympy.primerange]]
- [[sympy.gcd_entero]]
- [[sympy.ntheory/index | sympy.ntheory]]
- [[SymPy/index | SymPy]]
