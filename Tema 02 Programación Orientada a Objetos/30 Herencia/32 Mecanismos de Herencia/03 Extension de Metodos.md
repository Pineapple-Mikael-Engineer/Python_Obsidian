---
title: Extensión de Métodos
order: 3
tags:
  - python
  - teoria
  - herencia
draft: false
aliases:
  - Extensión de Métodos
  - Extender método
  - Method Extension
---

# Extensión de Métodos

> [!definicion]
> La **extensión** es un caso particular de [[02 Sobrescritura de Metodos (override) | sobrescritura]] en el que la subclase **no reemplaza** el método del padre, sino que lo **invoca** con [[01 super() y Constructor del Padre | super()]] y **añade** comportamiento antes o después. El resultado combina la lógica del padre con la de la subclase. Patrón: **extender, no reemplazar**.

```python
class Empleado:
    def __init__(self, nombre, salario):
        self.nombre = nombre
        self.salario = salario
    def to_dict(self):
        return {"nombre": self.nombre, "salario": self.salario}

class Gerente(Empleado):
    def __init__(self, nombre, salario, equipo):
        super().__init__(nombre, salario)
        self.equipo = equipo
    def to_dict(self):
        d = super().to_dict()      # lo que ya hace el padre
        d["equipo"] = self.equipo  # AÑADE lo propio
        return d

Gerente("Ana", 5000, ["Luis", "Eva"]).to_dict()
# {'nombre': 'Ana', 'salario': 5000, 'equipo': ['Luis', 'Eva']}
```

`Gerente.to_dict` no repite las claves del padre: delega en `super().to_dict()` y solo agrega `"equipo"`. Si `Empleado.to_dict` cambia, la versión del gerente hereda el cambio sin tocarse.

## Anatomía: antes y después

La extensión decide **dónde** se inserta el trabajo propio respecto a la llamada al padre.

```python
class Base:
    def procesar(self, x):
        return x * 2

class Trazado(Base):
    def procesar(self, x):
        print(f"entrada: {x}")          # trabajo ANTES
        resultado = super().procesar(x)  # delega en el padre
        print(f"salida: {resultado}")   # trabajo DESPUÉS
        return resultado
```

> [!regla]
> Si la lógica del padre sigue siendo correcta y solo hay que añadir, **extender** (`super()` + extra), no reescribir. Reescribir copiando el cuerpo del padre duplica conocimiento y se desincroniza al evolucionar la base.

## Override total vs. extensión

La diferencia es una sola línea —la llamada a `super()`— pero cambia la semántica por completo.

| | Override total | Extensión |
| --- | --- | --- |
| Llama a `super().metodo()` | No | Sí |
| Comportamiento del padre | descartado | conservado |
| La subclase aporta | toda la lógica | solo el incremento |
| Acoplamiento a la base | mínimo | reutiliza al padre |
| Caso típico | el padre no aplica | el padre aplica y falta un paso |

```python
# Override TOTAL: ignora al padre
class A(Empleado):
    def to_dict(self):
        return {"id": id(self)}          # nada del padre

# EXTENSIÓN: parte del padre + extra
class B(Empleado):
    def to_dict(self):
        d = super().to_dict()
        d["activo"] = True
        return d
```

> [!info]
> La extensión es el modo natural de `__init__` en una subclase: `super().__init__(...)` inicializa la parte heredada y luego se añaden los atributos propios. Ese es el mismo patrón de [[01 super() y Constructor del Padre | super() y el constructor del padre]] aplicado a un método cualquiera.

## Relación con otras notas

La extensión combina [[01 super() y Constructor del Padre | super()]] con la [[02 Sobrescritura de Metodos (override) | sobrescritura]]. En jerarquías con varios padres, el `super()` de una cadena de extensiones recorre el [[33 MRO y super() Cooperativo/index | MRO]], lo que da lugar al patrón [[02 super() Cooperativo]], donde cada clase extiende y delega en la siguiente sin conocerla.
