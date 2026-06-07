---
title: Funciones de Orden Superior
order: 7
draft: false
tags:
  - python
  - teoria
  - funciones
---
# Funciones de Orden Superior

Una **función de orden superior** (HOF) recibe una o más funciones como argumento, retorna una función, o ambas. Se apoyan en que las funciones son objetos de primera clase.

```python
# Recibe una función como argumento
def aplicar_dos_veces(func, valor):
    return func(func(valor))

print(aplicar_dos_veces(lambda x: x + 3, 10))  # 16

# Retorna una función
def potencia_de(exponente):
    def elevar(base):
        return base ** exponente
    return elevar

cuadrado = potencia_de(2)
print(cuadrado(5))  # 25
```

## map, filter y reduce

Las tres HOF clásicas operan sobre iterables y se combinan habitualmente con [[03 Funciones Lambda | lambda]]. `map` y `filter` retornan iteradores perezosos; `reduce` retorna un único valor acumulado.

```python
from functools import reduce

numeros = [1, 2, 3, 4, 5, 6]

# map(func, iterable) - aplica func a cada elemento
dobles = list(map(lambda x: x * 2, numeros))
print(dobles)  # [2, 4, 6, 8, 10, 12]

# filter(func, iterable) - conserva los elementos donde func es verdadera
pares = list(filter(lambda x: x % 2 == 0, numeros))
print(pares)  # [2, 4, 6]

# reduce(func, iterable[, inicial]) - acumula de izquierda a derecha
suma_total = reduce(lambda acc, x: acc + x, numeros)
print(suma_total)  # 21
maximo = reduce(lambda a, b: a if a > b else b, numeros)
print(maximo)  # 6

# map admite varios iterables (los recorre en paralelo)
sumas = list(map(lambda a, b: a + b, [1, 2, 3], [10, 20, 30]))
print(sumas)  # [11, 22, 33]
```

| HOF | Firma | Efecto | Retorno |
|-----|-------|--------|---------|
| **`map`** | `map(func, it)` | Aplica `func` a cada elemento | Iterador con un valor por elemento |
| **`filter`** | `filter(func, it)` | Conserva elementos donde `func(x)` es verdadera | Iterador con un subconjunto |
| **`reduce`** | `reduce(func, it[, ini])` | Acumula pares `(acc, x)` reduciendo a un valor | Un único valor escalar |

> [!tip] Comprehensions vs map/filter
> En Python idiomático, una list/generator comprehension suele ser más legible que `map`/`filter` con `lambda`. `list(map(lambda x: x*2, nums))` se escribe mejor como `[x * 2 for x in nums]`, y `list(filter(lambda x: x % 2 == 0, nums))` como `[x for x in nums if x % 2 == 0]`. `map`/`filter` siguen siendo útiles al reutilizar una función ya nombrada (ej. `map(str.strip, lineas)`).
