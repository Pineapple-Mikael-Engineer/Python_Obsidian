---
title: Closures
draft: false
tags:
  - python
  - teoria
  - funciones
---
# Closures

Un **closure** es una función anidada que captura y "recuerda" variables del ámbito envolvente donde fue definida, aun después de que dicho ámbito haya terminado de ejecutarse. La función interna se retorna y conserva el estado capturado. Véase [[index | Ámbito y Espacios de Nombres]] para las reglas de resolución de nombres.

```python
# Fábrica de multiplicadores: cada closure captura su propio 'factor'
def crear_multiplicador(factor):
    def multiplicar(x):
        return x * factor  # 'factor' se captura del ámbito envolvente
    return multiplicar

duplicar = crear_multiplicador(2)
triplicar = crear_multiplicador(3)
print(duplicar(10))   # 20
print(triplicar(10))  # 30

# Las variables libres capturadas son inspeccionables
print(duplicar.__closure__[0].cell_contents)  # 2
print([v for v in crear_multiplicador.__code__.co_varnames])  # ['factor', 'multiplicar']
```

## Estado persistente con nonlocal

Para **modificar** (no solo leer) una variable del ámbito envolvente desde la función interna se requiere la palabra clave `nonlocal`; sin ella, la asignación crearía una variable local nueva.

```python
def acumulador():
    total = 0
    def sumar(x):
        nonlocal total      # Sin esto, 'total' sería local a sumar()
        total += x
        return total
    return sumar

acc = acumulador()
print(acc(10))  # 10
print(acc(5))   # 15
print(acc(3))   # 18 (el estado persiste entre llamadas)

# Contador encapsulado: el estado es privado, inaccesible desde fuera
def crear_contador():
    n = 0
    def contar():
        nonlocal n
        n += 1
        return n
    return contar

siguiente = crear_contador()
print(siguiente(), siguiente(), siguiente())  # 1 2 3
```

> [!info]
> Cada invocación de la fábrica genera un closure independiente con su propio estado. Dos contadores creados por separado no comparten su variable `n`.
