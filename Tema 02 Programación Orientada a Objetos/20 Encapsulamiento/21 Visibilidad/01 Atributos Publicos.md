---
title: Atributos Públicos
order: 1
tags:
  - python
  - teoria
  - poo
draft: false
aliases:
  - Public attributes
  - Atributos públicos
---

# Atributos Públicos

> [!definicion]
> Un **atributo público** es aquel cuyo nombre **no lleva guion bajo inicial**. Es de **acceso libre**: cualquier código puede leerlo y escribirlo. Forma parte de la **API del objeto**, es decir, del contrato que la clase ofrece al exterior. En Python es el nivel **por defecto**: todo atributo es público salvo que su nombre indique lo contrario.

```python
class Punto:
    def __init__(self, x, y):
        self.x = x          # público
        self.y = y          # público

p = Punto(3, 4)
p.x                         # 3      lectura libre
p.y = 10                    # escritura libre
```

## Qué significa "público"

Ser público es un **compromiso de estabilidad**: quien usa la clase puede depender de ese atributo, y se espera que conserve su nombre y semántica entre versiones. Cambiarlo o eliminarlo rompe el código cliente.

> [!regla]
> Haz público un atributo cuando: forma parte natural de la interfaz, no tiene invariantes que validar, y puede leerse y escribirse libremente sin dejar al objeto en un estado inconsistente.

## Riesgo: exponer estado mutable con invariantes

Un atributo público se puede asignar a cualquier valor sin pasar por ningún control. Si el objeto depende de que ese valor cumpla una condición, exponerlo directamente permite **romper sus invariantes** desde fuera.

```python
class Circulo:
    def __init__(self, radio):
        self.radio = radio          # público y sin validación

c = Circulo(5)
c.radio = -3                        # nadie lo impide -> estado inválido
```

> [!warning]
> Si un atributo tiene **reglas que cumplir** (rango, formato, dependencia con otro campo), exponerlo como público deja esas reglas sin defensa. La solución no es ocultarlo "a la fuerza", sino convertirlo en una [[22 Properties/index | property]]: se sigue usando como `c.radio`, pero la escritura pasa por un *setter* que valida.

```python
class Circulo:
    def __init__(self, radio):
        self.radio = radio          # llama al setter
    @property
    def radio(self):
        return self._radio
    @radio.setter
    def radio(self, valor):
        if valor < 0:
            raise ValueError("el radio no puede ser negativo")
        self._radio = valor
```

La regla práctica: empieza con atributos **públicos y simples**; solo cuando aparezca un invariante migra a property. Como el acceso sigue siendo `obj.radio`, el cambio **no rompe** a quien ya usaba el atributo. Los datos que sí son de uso interno se marcan con [[02 Atributos Protegidos (_) | un guion bajo]].
