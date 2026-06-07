---
title: Import Selectivo (from import)
order: 3
tags:
  - python
  - teoria
  - modulos
draft: false
aliases:
  - from import
  - Import selectivo
  - from modulo import *
---

# Import Selectivo (from import)

> [!definicion]
> El **import selectivo** —`from modulo import a, b`— trae **nombres concretos** del módulo directamente al namespace actual, sin el prefijo del módulo. Tras él se usan como `a`, `b`, no como `modulo.a`. Es más conciso que el [[01 Import Simple | import simple]], a costa de **perder de vista el origen** de cada nombre.

```python
from math import pi, sqrt        # trae solo pi y sqrt

pi                               # 3.141592653589793   -> sin prefijo
sqrt(16)                         # 4.0
# math                          -> NameError: el modulo no queda accesible
```

Lo importado puede llevar su propio alias: `from math import sqrt as raiz`. Solo entran al namespace los nombres listados; el resto del módulo no queda accesible por nombre, aunque el módulo sí se ejecuta y cachea entero.

## `from modulo import *`: traerlo todo

> [!warning]
> `from modulo import *` importa **todos** los nombres públicos del módulo de golpe. Es **desaconsejado** fuera de sesiones interactivas: contamina el namespace, **sobrescribe** silenciosamente nombres ya definidos y vuelve imposible saber de dónde viene cada cosa al leer el código.

```python
from math import *               # trae pi, sqrt, sin, cos, ... todos
sqrt(9)                          # 3.0
# ¿de donde salio "gamma"? imposible saberlo a simple vista
```

## `__all__` controla qué exporta el `*`

> [!regla]
> Si el módulo define la lista `__all__`, `from modulo import *` importa **exactamente** los nombres de esa lista, ignorando el resto. Si **no** está definida, el `*` trae todos los nombres que **no empiezan por guion bajo**. Por eso `__all__` es la herramienta para acotar y documentar la interfaz pública de un módulo.

```python
# colores.py
__all__ = ["ROJO", "VERDE"]      # solo estos salen con import *
ROJO = "#ff0000"
VERDE = "#00ff00"
_INTERNO = "no exportar"

from colores import *            # trae ROJO y VERDE; NO _INTERNO ni nada mas
```

El detalle de cómo se diseña `__all__` para definir la interfaz pública se trata en [[62 Exposicion Selectiva (__all__) | Exposición Selectiva (`__all__`)]]. Frente al import selectivo, el [[02 Import con Alias | alias]] conserva el prefijo del módulo; y cuando dos módulos se importan nombres entre sí puede aparecer la [[04 Importacion Circular y Soluciones | importación circular]].
