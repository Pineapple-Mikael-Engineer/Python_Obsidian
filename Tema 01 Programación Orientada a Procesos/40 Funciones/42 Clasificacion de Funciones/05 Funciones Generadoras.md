---
title: 05 Funciones Generadoras
draft: false
tags:
  - python
  - teoria
  - funciones
---
# Funciones Generadoras

Las **funciones generadoras** se definen con `def` pero contienen al menos un `yield` en lugar de (o además de) `return`. Al invocarse no ejecutan su cuerpo: retornan un objeto generador que produce valores bajo demanda (evaluación perezosa).

## yield vs return

```python
# return entrega un único valor y termina la función
def cuadrados_lista(n):
    return [x ** 2 for x in range(n)]  # Construye toda la lista en memoria

# yield entrega un valor y SUSPENDE la función, conservando su estado
def cuadrados_gen(n):
    for x in range(n):
        yield x ** 2  # Cede el control; reanuda aquí en la siguiente petición

g = cuadrados_gen(5)
print(g)              # <generator object cuadrados_gen at 0x...>
print(next(g))        # 0
print(next(g))        # 1
# El cuerpo se reanuda exactamente donde quedó suspendido
```

> [!info] Estado suspendido
> Cada `yield` congela el marco de ejecución completo (variables locales, posición del bucle, pila). La siguiente petición (`next()`) reanuda la ejecución justo después del `yield`. Cuando el cuerpo termina, se lanza `StopIteration`.

## Evaluación perezosa y consumo

```python
# Los valores se calculan uno a uno (lazy), no de antemano
def lineas_procesadas(ruta):
    """Lee y transforma sin cargar el archivo entero en memoria."""
    with open(ruta) as f:
        for linea in f:
            yield linea.strip().upper()

# Consumo con for (consume hasta StopIteration automáticamente)
for linea in lineas_procesadas("datos.txt"):
    print(linea)

# Consumo manual con next() y valor por defecto
gen = cuadrados_gen(3)
print(next(gen, None))  # 0
print(next(gen, None))  # 1
print(next(gen, None))  # 4
print(next(gen, None))  # None (agotado, no lanza StopIteration)
```

## Generador de secuencia infinita

```python
# Un generador puede producir una secuencia sin fin, imposible con una lista
def contador_infinito(inicio=0, paso=1):
    n = inicio
    while True:
        yield n
        n += paso

c = contador_infinito(10, 5)
print(next(c))  # 10
print(next(c))  # 15
print(next(c))  # 20
# La lista equivalente nunca terminaría de construirse

# Lectura por lotes (chunks) de un iterable grande
def por_lotes(iterable, tamaño):
    lote = []
    for elemento in iterable:
        lote.append(elemento)
        if len(lote) == tamaño:
            yield lote
            lote = []
    if lote:  # Último lote parcial
        yield lote

for lote in por_lotes(range(10), 3):
    print(lote)  # [0,1,2] [3,4,5] [6,7,8] [9]
```

## Expresiones generadoras

Sintaxis idéntica a una comprehension pero con paréntesis: produce un generador en lugar de una lista materializada.

```python
# Sintaxis: (expresión for x in iterable [if condición])
# Idéntica a una comprehension pero con paréntesis: produce un generador, no una lista

cuadrados = (x ** 2 for x in range(1_000_000))
print(cuadrados)          # <generator object ...>
print(next(cuadrados))    # 0

# Ventaja de memoria frente a la lista equivalente
import sys
lista = [x ** 2 for x in range(1_000_000)]
gen = (x ** 2 for x in range(1_000_000))
print(sys.getsizeof(lista))  # ~8 MB (todos los elementos materializados)
print(sys.getsizeof(gen))    # ~200 bytes (solo el objeto generador)

# Se pasan directamente a funciones que consumen iterables, sin paréntesis extra
total = sum(x ** 2 for x in range(100))   # No crea lista intermedia
print(total)  # 328350
```

> [!tip]
> Si solo se va a iterar una vez y se busca minimizar memoria, una expresión generadora es preferible a una lista. Si se necesita indexar, recorrer varias veces o conocer `len()`, se requiere materializar con una lista.
