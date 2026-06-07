---
title: Factory Method
order: 82
tags:
  - python
  - teoria
  - patrones
draft: false
aliases:
  - Método fábrica
  - Fábrica
---

# Factory Method

> [!definicion]
> El **Factory Method** delega la **creación** de objetos a un método o función dedicada, de modo que el cliente pide un objeto **sin nombrar la clase concreta**. Quien decide qué tipo instanciar es la fábrica; el cliente solo conoce la interfaz común.

```python
class Circulo:
    def area(self): return 3.14 * self.r ** 2
    def __init__(self, r): self.r = r

class Cuadrado:
    def area(self): return self.l ** 2
    def __init__(self, l): self.l = l

def crear_forma(tipo, medida):
    formas = {"circulo": Circulo, "cuadrado": Cuadrado}
    return formas[tipo](medida)                     # devuelve la clase adecuada

f = crear_forma("circulo", 2)
f.area()                                            # 12.56
```

El cliente trabaja con `f.area()` sin saber si es un `Circulo` o un `Cuadrado`: la fábrica desacopla el **qué se usa** del **qué se crea**, apoyándose en el polimorfismo de un método común.

## Diccionario despachador frente a if/elif

> [!regla]
> Para elegir la clase según un parámetro, un **diccionario `{clave: clase}`** es más extensible que una cadena `if/elif`: añadir un tipo es añadir una entrada, y las clases son objetos de primera clase que se almacenan sin instanciar.

```python
REGISTRO = {"circulo": Circulo, "cuadrado": Cuadrado}

def crear_forma(tipo, medida):
    try:
        return REGISTRO[tipo](medida)
    except KeyError:
        raise ValueError(f"forma desconocida: {tipo}")

REGISTRO["triangulo"] = Triangulo                   # se amplía sin tocar la función
```

## Constructores alternativos con @classmethod

> [!ejemplo]
> La variante más idiomática del patrón en Python es un **`@classmethod`** que actúa como **constructor alternativo**: recibe `cls`, construye una instancia de la clase desde otra fuente de datos y la devuelve. Es el papel de `dict.fromkeys` o `datetime.fromtimestamp`.

```python
class Fecha:
    def __init__(self, dia, mes, anio):
        self.dia, self.mes, self.anio = dia, mes, anio

    @classmethod
    def desde_cadena(cls, texto):                   # "03-06-2026"
        dia, mes, anio = map(int, texto.split("-"))
        return cls(dia, mes, anio)                  # construye y devuelve

f = Fecha.desde_cadena("03-06-2026")               # Fecha(3, 6, 2026)
```

Usar `cls` (no el nombre de la clase) hace que el constructor alternativo se herede correctamente y produzca instancias de la subclase. Ver [[02 Metodos de Clase (classmethod)]].

> [!info]
> Ambas formas comparten la idea central: centralizar la lógica de construcción en un punto único. La función fábrica decide **entre varias clases**; el `@classmethod` ofrece **varias rutas de construcción** para una misma clase.
