---
title: Métodos de Clase (classmethod)
tags:
  - python
  - teoria
  - metodos
draft: false
aliases:
  - Métodos de Clase
  - classmethod
  - Constructores alternativos
---

# Métodos de Clase (`@classmethod`)

> [!definicion]
> Un **método de clase** está marcado con el decorador **`@classmethod`** y recibe como primer parámetro **`cls`**: la **clase misma**, no una instancia. Trabaja sobre el estado **de clase** y se invoca tanto desde la clase como desde cualquier instancia. Su uso estrella son los **constructores alternativos** (fábricas).

```python
class Fecha:
    def __init__(self, dia, mes, anio):
        self.dia, self.mes, self.anio = dia, mes, anio

    @classmethod
    def desde_string(cls, s):          # cls es Fecha
        d, m, a = map(int, s.split("-"))
        return cls(d, m, a)            # construye y devuelve una instancia

f = Fecha.desde_string("03-06-2026")  # constructor alternativo
f.anio                                # 2026
```

`cls(d, m, a)` equivale a llamar al constructor: produce una instancia nueva. Igual que `self`, el argumento `cls` se inyecta solo; no se escribe al llamar.

## Uso estrella: constructores alternativos

`__init__` define **una** forma de construir un objeto. Un método de clase ofrece **vías de construcción adicionales** a partir de otros datos de entrada, devolviendo siempre `cls(...)`.

```python
import time

class Fecha:
    def __init__(self, dia, mes, anio):
        self.dia, self.mes, self.anio = dia, mes, anio

    @classmethod
    def desde_timestamp(cls, ts):
        t = time.localtime(ts)
        return cls(t.tm_mday, t.tm_mon, t.tm_year)

    @classmethod
    def hoy(cls):
        return cls.desde_timestamp(time.time())

Fecha.hoy().anio          # 2026
```

> [!regla]
> Construir siempre con **`cls(...)`**, nunca con el nombre fijo de la clase (`Fecha(...)`). Solo así la fábrica respeta la herencia.

## Herencia: `cls` es la subclase

Como `cls` se enlaza a la clase **real** de la llamada, un constructor alternativo heredado fabrica instancias de la **subclase**, no de la clase base. Esto es lo que rompe un constructor escrito con el nombre fijo.

```python
class FechaISO(Fecha):
    def __repr__(self):
        return f"{self.anio:04d}-{self.mes:02d}-{self.dia:02d}"

x = FechaISO.desde_string("03-06-2026")
type(x)        # <class '__main__.FechaISO'>  -> cls fue FechaISO, no Fecha
```

> [!info]
> Si `desde_string` hubiera hecho `return Fecha(...)`, `FechaISO.desde_string(...)` devolvería un `Fecha` y perdería el comportamiento de la subclase. Con `cls(...)`, el método se adapta automáticamente.

## Acceso al estado de clase

Un método de clase **lee y modifica atributos de clase** a través de `cls`, pero **no ve atributos de instancia** (no recibe `self`).

```python
class Usuario:
    _contador = 0                     # atributo de clase
    def __init__(self, nombre):
        self.nombre = nombre
        Usuario._contador += 1

    @classmethod
    def total_creados(cls):
        return cls._contador          # estado COMPARTIDO

Usuario("Ana"); Usuario("Luis")
Usuario.total_creados()               # 2
```

## Contraste

| | Clase (`@classmethod`) | Instancia | Estático (`@staticmethod`) |
| --- | --- | --- | --- |
| Primer parámetro | `cls` | `self` | ninguno |
| Ve estado de clase | Sí | Sí (vía `self`) | No |
| Ve estado de instancia | No | Sí | No |
| Sensible a herencia | Sí (`cls` = subclase) | Sí | No |

- Si el método **fabrica instancias** o toca el estado compartido, es de clase.
- Si **opera sobre un objeto concreto**, es un [[01 Metodos de Instancia | método de instancia]].
- Si **no necesita ni `self` ni `cls`**, es un [[03 Metodos Estaticos (staticmethod) | método estático]].
