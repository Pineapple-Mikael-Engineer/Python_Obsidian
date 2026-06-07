---
title: Métodos de Instancia
order: 1
tags:
  - python
  - teoria
  - metodos
draft: false
aliases:
  - Métodos de Instancia
  - Instance methods
---

# Métodos de Instancia

> [!definicion]
> Un **método de instancia** es el tipo de método **por defecto**: una función definida en el cuerpo de la clase cuyo **primer parámetro es `self`**, la referencia a la instancia concreta sobre la que se invoca. Opera sobre el **estado de esa instancia**, pudiendo leer y modificar sus atributos.

```python
class Contador:
    def __init__(self, inicio=0):
        self.valor = inicio          # estado de instancia
    def incrementar(self):           # método de instancia: recibe self
        self.valor += 1
        return self.valor

c = Contador()
c.incrementar()   # 1
c.incrementar()   # 2
```

No se escribe el argumento de `self` al llamar: `c.incrementar()` lo inyecta automáticamente. La invocación `obj.metodo(args)` equivale exactamente a `Clase.metodo(obj, args)`.

## Método ligado: `obj.metodo` captura la instancia

Acceder a un método a través de una instancia produce un **método ligado** (*bound method*): un objeto que recuerda a qué instancia pertenece. Al llamarlo, esa instancia se pasa como `self` sin escribirla.

```python
c = Contador(10)
m = c.incrementar     # método LIGADO a c (aún no se ejecuta)
type(m)               # <class 'method'>
m()                   # 11  -> self es c, implícito
```

> [!info]
> Accedido desde la **clase**, `Clase.metodo` es una **función ordinaria** (*unbound*) y requiere pasar la instancia a mano: `Contador.incrementar(c)`. Accedido desde la **instancia**, `c.incrementar` ya viene ligado. El responsable de inyectar `self` es el [[03 El parametro self | parámetro self]].

## Acceso al estado: instancia y clase

Desde `self` se alcanza tanto el estado propio de la instancia como los atributos compartidos de la clase. La búsqueda de un atributo en `self.x` recorre primero la instancia y luego la clase.

```python
class Empleado:
    bono = 100                       # atributo de CLASE (compartido)
    def __init__(self, sueldo):
        self.sueldo = sueldo         # atributo de INSTANCIA
    def total(self):
        return self.sueldo + self.bono   # lee instancia Y clase

e = Empleado(2000)
e.total()                            # 2100
```

> [!warning]
> Asignar `self.bono = 0` **no** modifica el atributo de clase: crea un atributo de instancia que lo **enmascara** solo en ese objeto. Para alterar el valor compartido por todos hay que escribir sobre la clase (`Empleado.bono = 0`) o usar un [[02 Metodos de Clase (classmethod) | método de clase]]. El reparto instancia/clase se detalla en [[12 Atributos/index | Atributos]].

## Contraste con los otros dos tipos

| | Instancia | Clase | Estático |
| --- | --- | --- | --- |
| Primer parámetro | `self` | `cls` | ninguno |
| Decorador | — | `@classmethod` | `@staticmethod` |
| Ve la instancia | Sí | No | No |

- Un método de **instancia** necesita un objeto concreto: `Contador.incrementar()` sin instancia falla por falta de `self`.
- Si un método **no usa `self`**, probablemente debería ser un [[03 Metodos Estaticos (staticmethod) | método estático]].
- Si solo necesita la **clase** (p. ej. fabricar instancias), corresponde a un [[02 Metodos de Clase (classmethod) | método de clase]].
