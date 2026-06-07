---
title: Funciones Built-in
order: 1
draft: false
tags:
  - python
  - teoria
  - funciones
---
# Funciones Built-in

Las **funciones built-in** vienen incluidas en el intérprete de Python y están siempre disponibles sin importar módulos. Cubren entrada/salida, conversión de tipos, matemáticas, manejo de iterables e introspección.

## Entrada / Salida

```python
# print() - mostrar información
print("Hola mundo")  # Hola mundo
print("Valor:", 42)  # Valor: 42
print("a", "b", "c", sep="-")  # a-b-c
print("Sin salto", end="")  # No añade nueva línea

# input() - recibir entrada del usuario
nombre = input("¿Cómo te llamas? ")
edad = int(input("¿Cuántos años tienes? "))  # Convertir a entero
```

## Conversión de tipos

```python
# Conversión a enteros
entero1 = int("42")        # 42
entero2 = int(3.14)        # 3 (trunca)
entero3 = int("1010", 2)   # 10 (binario a decimal)

# Conversión a flotantes
flotante1 = float("3.14")  # 3.14
flotante2 = float(5)       # 5.0

# Conversión a strings
texto1 = str(42)           # "42"
texto2 = str([1, 2, 3])    # "[1, 2, 3]"

# Conversión a booleanos
bool(0)        # False
bool(1)        # True
bool("")       # False
bool("Hola")   # True
bool([])       # False
bool([1, 2])   # True

# Conversión a colecciones
lista = list("abc")        # ['a', 'b', 'c']
tupla = tuple([1, 2, 3])   # (1, 2, 3)
conjunto = set([1, 2, 2, 3])  # {1, 2, 3}
```

## Matemáticas

```python
# abs() - valor absoluto
print(abs(-5))        # 5
print(abs(3.14))      # 3.14

# sum() - suma de iterable
print(sum([1, 2, 3, 4]))     # 10
print(sum([1, 2, 3], 10))    # 16 (10 + suma)

# round() - redondeo
print(round(3.14159, 2))     # 3.14
print(round(3.5))            # 4 (redondeo bancario)

# max() / min() - máximo y mínimo
print(max(1, 5, 3, 9, 2))    # 9
print(min([4, 2, 8, 1]))     # 1
print(max("python"))          # 'y' (orden alfabético)

# pow() - potencia
print(pow(2, 3))             # 8
print(pow(2, 3, 5))          # 3 (2^3 % 5)

# divmod() - división con resto
cociente, resto = divmod(17, 5)
print(f"17 ÷ 5 = {cociente}, resto {resto}")  # 3, resto 2
```

## Iterables

```python
# len() - longitud
print(len("Python"))          # 6
print(len([1, 2, 3, 4]))      # 4
print(len({"a": 1, "b": 2}))  # 2

# range() - generar secuencias
list(range(5))                # [0, 1, 2, 3, 4]
list(range(2, 8))             # [2, 3, 4, 5, 6, 7]
list(range(1, 10, 2))         # [1, 3, 5, 7, 9]

# enumerate() - índice y valor
frutas = ["manzana", "banana", "cereza"]
for i, fruta in enumerate(frutas, start=1):
    print(f"{i}. {fruta}")

# zip() - combinar iterables
nombres = ["Ana", "Juan", "Carlos"]
edades = [25, 30, 35]
for nombre, edad in zip(nombres, edades):
    print(f"{nombre} tiene {edad} años")

# all() / any() - condiciones sobre iterables
numeros = [1, 2, 3, 4, 5]
print(all(n > 0 for n in numeros))   # True (todos positivos)
print(any(n > 10 for n in numeros))  # False (ninguno > 10)

# sorted() - ordenar
print(sorted([3, 1, 4, 2]))          # [1, 2, 3, 4]
print(sorted(["ana", "Juan", "carlos"], key=str.lower))  # Orden sin distinguir mayúsculas

# reversed() - invertir
print(list(reversed([1, 2, 3])))     # [3, 2, 1]
```

## Utilitarias e introspección

```python
# type() - obtener tipo
print(type(42))           # <class 'int'>
print(type("hola"))       # <class 'str'>
print(type([1, 2]))       # <class 'list'>

# id() - identidad del objeto
x = [1, 2, 3]
y = x
print(id(x) == id(y))     # True (mismo objeto)

# help() - documentación
# help(print)  # Muestra ayuda sobre print
# help(str)    # Muestra ayuda sobre strings

# dir() - atributos y métodos
print(dir([]))            # Lista métodos de lista
print(dir(str))           # Lista métodos de string

# isinstance() - verificar tipo
print(isinstance(42, int))           # True
print(isinstance("hola", (str, list)))  # True (es string)

# callable() - verificar si es llamable
def funcion():
    pass
print(callable(funcion))  # True
print(callable(42))       # False
```

## Funciones de módulos específicos (requieren import)

No son built-in propiamente, pero suelen confundirse con ellas: residen en módulos de la biblioteca estándar y exigen `import`.

```python
import math
import random
import datetime

# math
print(math.pi)                    # 3.141592653589793
print(math.sqrt(16))              # 4.0
print(math.floor(3.7))            # 3
print(math.ceil(3.2))             # 4

# random
print(random.randint(1, 10))      # Aleatorio entre 1 y 10
print(random.choice(["rojo", "verde", "azul"]))  # Aleatorio de lista

# datetime
hoy = datetime.date.today()
print(hoy)                        # Fecha actual
```

## Buenas prácticas

```python
# ✅ Conocer y usar built-ins apropiados
numeros = [3, 1, 4, 1, 5]
# Mejor usar sum()
total = sum(numeros)  # ✅
# total = 0; for n in numeros: total += n  # ❌

# Mejor usar max()/min()
maximo = max(numeros)  # ✅
# maximo = numeros[0]; for n in numeros: if n > maximo: maximo = n  # ❌
```
