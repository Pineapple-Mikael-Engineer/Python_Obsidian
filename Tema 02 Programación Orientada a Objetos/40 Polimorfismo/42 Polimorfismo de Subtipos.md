---
title: Polimorfismo de Subtipos
order: 42
tags:
  - python
  - teoria
  - polimorfismo
draft: false
aliases:
  - Subtype polymorphism
  - Polimorfismo de inclusión
  - Despacho dinámico
---

# Polimorfismo de Subtipos

> [!definicion]
> El **polimorfismo de subtipos** es el polimorfismo clásico vía herencia: una variable declarada o tratada como del **tipo base** puede referenciar instancias de cualquier **subclase**, y al invocar un método sobrescrito se ejecuta la versión de la **clase real** del objeto, no la del tipo base. Esta resolución en tiempo de ejecución es el **despacho dinámico**.

```python
class Figura:
    def area(self):
        raise NotImplementedError

class Circulo(Figura):
    def __init__(self, r): self.r = r
    def area(self): return 3.1416 * self.r ** 2     # sobrescribe

class Cuadrado(Figura):
    def __init__(self, l): self.l = l
    def area(self): return self.l ** 2              # sobrescribe

f = Circulo(2)       # variable tratada como Figura
f.area()             # 12.5664  -> ejecuta Circulo.area, la clase real
```

Aunque `f` se use como `Figura`, la llamada `f.area()` se resuelve sobre `Circulo`, la clase concreta del objeto. Se apoya por completo en la [[02 Sobrescritura de Metodos (override)]]: sin redefinir el método en la subclase, el despacho dinámico ejecutaría siempre la versión heredada.

## Lista heterogénea y bucle uniforme

> [!ejemplo]
> El patrón canónico: una colección de instancias de **distintas subclases** recorrida con un bucle que invoca el **mismo método** sobre cada elemento. El código cliente ignora la clase concreta; cada objeto responde con su propia implementación.

```python
figuras = [Circulo(1), Cuadrado(3), Circulo(2)]   # tipos mezclados

for fig in figuras:
    print(fig.area())     # 3.1416  /  9  /  12.5664
                          # misma llamada, tres comportamientos
```

`fig.area()` no contiene ningún `if isinstance(...)`: la elección de la versión correcta la hace el despacho dinámico al consultar la clase real de cada `fig`. Añadir una nueva figura no obliga a tocar el bucle, solo a crear la subclase con su `area`.

## Despacho dinámico: cómo se resuelve

> [!info]
> Al evaluar `fig.area()`, Python busca `area` recorriendo el **MRO** del objeto desde su clase concreta hacia las bases, y ejecuta la primera coincidencia. Por eso el método elegido depende del tipo **real** del objeto en ejecución, no del tipo aparente de la variable. El recorrido del MRO se detalla en [[32 Mecanismos de Herencia/index | Mecanismos de Herencia]].

```python
type(fig)            # <class '__main__.Circulo'>  -> determina la versión
fig.area.__qualname__  # 'Circulo.area'
```

A diferencia de C++ o Java, en Python **todos** los métodos son virtuales por defecto: no hace falta marcar nada para habilitar el despacho dinámico; es el comportamiento estándar de la resolución de atributos.

## Principio de sustitución de Liskov

> [!regla]
> **Principio de sustitución de Liskov (LSP):** una instancia de subclase debe poder usarse en todo punto donde se espere la clase base **sin alterar la corrección** del programa. El polimorfismo de subtipos es seguro solo si las subclases respetan el contrato del tipo base: misma firma efectiva, precondiciones no más estrictas, postcondiciones no más débiles.

Una subclase que sobrescribe `area` devolviendo un tipo incompatible, o que exige condiciones que la base no imponía, viola el LSP y rompe el código cliente que la trata polimórficamente. El polimorfismo de subtipos requiere herencia y contrato compartido; cuando solo importa la interfaz y no el linaje, aplica el [[41 Duck Typing | duck typing]].
