---
title: Funciones Lambda
draft: false
tags:
  - python
  - teoria
  - funciones
---
# Funciones Lambda

Las **funciones lambda** son funciones anónimas de una sola expresión, definidas en línea. Sintaxis: `lambda argumentos: expresión`. Su valor de retorno es el resultado de la expresión, sin `return` explícito.

## Sintaxis básica

```python
# Sintaxis: lambda argumentos: expresión

# Lambda simple
suma = lambda a, b: a + b
print(suma(5, 3))  # 8

# Lambda sin usar variable (anónima realmente)
print((lambda x: x ** 2)(5))  # 25

# Lambda con múltiples argumentos
multiplica = lambda x, y, z: x * y * z
print(multiplica(2, 3, 4))  # 24

# Lambda condicional
es_par = lambda x: x % 2 == 0
print(es_par(4))  # True
print(es_par(5))  # False
```

## Usos comunes

Las lambdas brillan como argumento `key` o callback de funciones de [[07 Funciones de Orden Superior | orden superior]] (`sorted`, `map`, `filter`, `reduce`).

```python
# 1. Con sorted() - ordenamiento personalizado
personas = [
    ("Ana", 25, "Madrid"),
    ("Juan", 30, "Barcelona"),
    ("Carlos", 22, "Valencia")
]

# Ordenar por edad
ordenado_edad = sorted(personas, key=lambda p: p[1])
print(ordenado_edad)  # [('Carlos',22), ('Ana',25), ('Juan',30)]

# Ordenar por ciudad
ordenado_ciudad = sorted(personas, key=lambda p: p[2])
print(ordenado_ciudad)  # Barcelona, Madrid, Valencia

# 2. Con map() - aplicar función a cada elemento
numeros = [1, 2, 3, 4, 5]
cuadrados = list(map(lambda x: x ** 2, numeros))
print(cuadrados)  # [1, 4, 9, 16, 25]

# 3. Con filter() - filtrar elementos
pares = list(filter(lambda x: x % 2 == 0, numeros))
print(pares)  # [2, 4]

# 4. Con reduce() - acumular valores
from functools import reduce
producto = reduce(lambda a, b: a * b, numeros)
print(producto)  # 120 (1*2*3*4*5)

# 5. En list comprehensions (aunque mejor sin lambda)
# Con lambda (menos eficiente)
cuadrados_lambda = [(lambda x: x ** 2)(x) for x in numeros]
# Sin lambda (mejor)
cuadrados_directo = [x ** 2 for x in numeros]
```

## Lambdas en diccionarios

Despacho de operaciones por clave: un diccionario de lambdas sustituye a una cadena de `if/elif`.

```python
# Diccionario de operaciones con lambdas
operaciones = {
    "suma": lambda a, b: a + b,
    "resta": lambda a, b: a - b,
    "multiplica": lambda a, b: a * b,
    "divide": lambda a, b: a / b if b != 0 else None,
    "potencia": lambda a, b: a ** b
}

# Usar según necesidad
print(operaciones["suma"](10, 5))       # 15
print(operaciones["potencia"](2, 3))    # 8
print(operaciones["divide"](10, 2))     # 5.0

# Calculadora simple
def calculadora(operacion, a, b):
    if operacion in operaciones:
        return operaciones[operacion](a, b)
    return "Operación no válida"

print(calculadora("suma", 15, 7))       # 22
print(calculadora("resta", 15, 7))      # 8
```

## Lambdas con condicionales

```python
# Lambda con if-else (operador ternario)
clasificar = lambda x: "par" if x % 2 == 0 else "impar"
print(clasificar(4))   # par
print(clasificar(5))   # impar

# Lambda con múltiples condiciones
calificar = lambda nota: (
    "Sobresaliente" if nota >= 9 else
    "Notable" if nota >= 7 else
    "Bien" if nota >= 6 else
    "Suficiente" if nota >= 5 else
    "Insuficiente"
)

print(calificar(8.5))  # Notable
print(calificar(4.9))  # Insuficiente

# Lambda con and/or (no recomendado, mejor if-else)
maximo = lambda a, b: a if a > b else b
print(maximo(10, 20))  # 20
```

## Limitaciones

Una lambda solo contiene **una expresión**: no admite statements (asignaciones, bucles, `return`, `raise`) ni múltiples líneas.

```python
# ❌ No pueden contener statements (asignaciones, bucles, etc.)
# lambda x: x = 5  # SyntaxError

# ❌ No pueden tener múltiples líneas
# lambda x:
#     x = x + 1
#     return x  # SyntaxError

# ✅ Pero pueden contener expresiones complejas
procesar = lambda x: (
    x ** 2 if x > 0 else
    abs(x) ** 0.5 if x < 0 else
    0
)

print(procesar(4))   # 16
print(procesar(-4))  # 2.0

# Comparación: lambda vs función normal
# Lambda
cuadrado_lambda = lambda x: x ** 2

# Función normal
def cuadrado_funcion(x):
    return x ** 2

# Para lógica simple, lambda es más conciso
# Para lógica compleja, función normal es más clara
```

## Buenas prácticas

```python
# ✅ Usar lambda para operaciones simples
cuadrados = list(map(lambda x: x**2, range(10)))

# ✅ Usar lambda con sorted() para ordenamiento personalizado
personas.sort(key=lambda p: p.edad)

# ❌ NO usar lambda para lógica compleja
# operacion = lambda x: (x**2 if x > 0 else abs(x)**0.5 if x < 0 else 0)
# Mejor:
def operacion_compleja(x):
    if x > 0:
        return x ** 2
    elif x < 0:
        return abs(x) ** 0.5
    return 0
```
