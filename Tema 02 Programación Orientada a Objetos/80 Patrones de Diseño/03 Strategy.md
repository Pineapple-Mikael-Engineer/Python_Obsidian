---
title: Strategy
tags:
  - python
  - teoria
  - patrones
draft: false
aliases:
  - Estrategia
  - Política
---

# Strategy

> [!definicion]
> El **Strategy** encapsula una familia de **algoritmos intercambiables** tras una interfaz común y permite **seleccionar uno en tiempo de ejecución**. El cliente delega el algoritmo en un objeto (o función) externo, de modo que cambiar de comportamiento es cambiar de estrategia, no de código del cliente.

```python
# Idiomático: la estrategia es una función pasada como argumento
def procesar(datos, estrategia):
    return estrategia(datos)                        # delega el algoritmo

procesar([3, 1, 2], sorted)                         # [1, 2, 3]
procesar([3, 1, 2], sum)                            # 6
procesar([3, 1, 2], lambda d: max(d) - min(d))     # 2
```

## Versión idiomática: funciones de primera clase

> [!regla]
> En Python las **funciones son objetos de primera clase**: se pasan como argumentos, se guardan en variables y se devuelven. Por eso una estrategia suele ser **simplemente una función (o cualquier *callable*)**, sin necesidad de una jerarquía de clases `Strategy`.

```python
def ordenar(items, clave):                          # la estrategia es 'clave'
    return sorted(items, key=clave)

personas = [("Ana", 30), ("Luis", 25)]
ordenar(personas, key := lambda p: p[1])           # por edad: [("Luis",25),("Ana",30)]
ordenar(personas, lambda p: p[0])                  # por nombre: [("Ana",30),("Luis",25)]
```

El parámetro `key` de `sorted`, `min`, `max` o `map` es Strategy puro incorporado en el lenguaje: el algoritmo de comparación se inyecta desde fuera.

## Versión clásica: jerarquía de clases

> [!ejemplo]
> La formulación original usa una **clase por estrategia** con un método común y duck typing: el contexto guarda una estrategia y le delega. Es más verbosa y solo se justifica si la estrategia necesita **estado propio** o varios métodos.

```python
class DescuentoFijo:
    def __init__(self, monto): self.monto = monto
    def aplicar(self, total): return total - self.monto

class DescuentoPorcentual:
    def __init__(self, pct): self.pct = pct
    def aplicar(self, total): return total * (1 - self.pct)

class Carrito:
    def __init__(self, estrategia): self.estrategia = estrategia
    def total(self, base): return self.estrategia.aplicar(base)

Carrito(DescuentoPorcentual(0.1)).total(100)        # 90.0
Carrito(DescuentoFijo(15)).total(100)               # 85
```

> [!info]
> Contraste: la versión con clases exige definir una interfaz, instanciar y mantenerla; la versión con funciones logra lo mismo pasando un *callable*. Solo cuando la estrategia acumula estado o configuración conviene una clase; en caso contrario, una función es la opción preferida en Python.

El intercambio de comportamiento en runtime conecta con el [[40 Polimorfismo/index | Polimorfismo]]: distintas estrategias responden al mismo punto de invocación.
