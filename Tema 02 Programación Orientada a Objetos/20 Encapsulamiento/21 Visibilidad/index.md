---
title: 21 Visibilidad
draft: false
description: Los tres niveles convencionales de acceso a atributos en Python
tags:
  - Index
  - Tema
aliases:
  - Visibilidad
  - Niveles de acceso
---
# Visibilidad

La **visibilidad** describe quién debería acceder a cada atributo o método de un objeto. En Python no existen modificadores de acceso reales (`public`, `protected`, `private` como en Java o C++): el lenguaje **no impide** nada en tiempo de ejecución. Lo que hay son **convenciones de nombre** —el guion bajo inicial— y un único mecanismo técnico —el *name mangling*— que reescribe ciertos nombres pero **tampoco bloquea** el acceso.

La regla cultural es *"todos somos adultos responsables"*: la intención se **señala** con la forma del nombre, y se confía en que quien usa la clase la respete.

```python
class Cuenta:
    def __init__(self, saldo):
        self.titular = "Ana"      # público: forma la API
        self._saldo = saldo       # protegido: uso interno (convención)
        self.__pin = 1234         # privado: name mangling -> _Cuenta__pin

c = Cuenta(100)
c.titular                         # "Ana"   acceso normal
c._saldo                          # 100     accesible, pero "no deberías"
c.__pin                           # AttributeError: no existe ese nombre
c._Cuenta__pin                    # 1234    sigue accesible vía mangling
```

## Subtemas

- [[01 Atributos Publicos | Atributos Públicos]] — sin guion bajo; acceso libre; forman la API del objeto.
- [[02 Atributos Protegidos (_) | Atributos Protegidos]] — un guion bajo `_nombre`; convención de uso interno, no impuesta.
- [[03 Privados y Name Mangling (__) | Privados y Name Mangling]] — dos guiones bajos `__nombre`; renombrado a `_Clase__nombre` para evitar colisiones.

## Los tres niveles

| Convención | Señal | Significado | Lo aplica |
| ---------- | ----- | ----------- | --------- |
| `nombre` | — | **Público**: parte de la API, acceso libre | Convención |
| `_nombre` | un guion bajo | **Protegido**: uso interno, no toques desde fuera | Convención (no impuesta) |
| `__nombre` | dos guiones bajos | **Privado**: *name mangling* a `_Clase__nombre` | Python (renombra, no oculta) |

> [!regla]
> Ningún nivel impide realmente el acceso. El guion bajo es una **señal de intención**; el doble guion bajo añade *name mangling* para **evitar colisiones de nombres**, no para dar seguridad. Para un acceso verdaderamente controlado (validación, solo-lectura, cálculo) se usan [[22 Properties/index | Properties]].
