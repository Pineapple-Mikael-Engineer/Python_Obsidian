---
title: __init__.py
order: 1
tags:
  - python
  - teoria
  - proyectos
draft: false
aliases:
  - init py
  - Inicializador de paquete
  - Package initializer
---

# __init__.py

> [!definicion]
> `__init__.py` es el archivo que **marca un directorio como paquete** y que **se ejecuta una sola vez al importar ese paquete**. Su cuerpo inicializa el paquete (ejecuta código de arranque) y, sobre todo, **define la API pública**: los nombres que se re-exportan ahí son los que el usuario obtiene al hacer `import mi_paquete`.

```python
# mi_paquete/__init__.py
print("inicializando mi_paquete")        # se ejecuta al importar el paquete
from .core import Motor, arrancar         # re-exporta símbolos al nivel del paquete
__all__ = ["Motor", "arrancar"]           # define qué expone  from mi_paquete import *

# uso desde fuera
import mi_paquete                          # imprime "inicializando mi_paquete"
mi_paquete.Motor                           # accesible aunque viva en core.py
```

El usuario escribe `mi_paquete.Motor`, no `mi_paquete.core.Motor`: el `__init__.py` **eleva** el símbolo desde el módulo interno hasta la superficie del paquete. Esa elevación es lo que convierte una colección de archivos en una **interfaz única y limpia**.

## Se ejecuta al importar el paquete

> [!regla]
> El código de `__init__.py` corre **la primera vez** que se importa el paquete (o cualquier módulo dentro de él) y **no se vuelve a ejecutar**: el resultado queda cacheado en `sys.modules`. Importar `mi_paquete.core` ejecuta primero el `__init__.py` del paquete y luego `core`.

```python
import mi_paquete            # ejecuta __init__.py  -> "inicializando mi_paquete"
import mi_paquete            # NO reimprime: ya está en sys.modules

mi_paquete.__name__          # "mi_paquete"
mi_paquete.__file__          # ".../mi_paquete/__init__.py"
```

## Re-exportar para aplanar la API

> [!info]
> Sin `__init__.py` el usuario tendría que conocer la **estructura interna** (`from mi_paquete.core.motor import Motor`). Re-exportando en `__init__.py` se ofrece una ruta **plana y estable** (`from mi_paquete import Motor`): si mañana `Motor` cambia de archivo, solo se toca el `__init__.py`, no el código de quien lo usa.

```python
# mi_paquete/__init__.py
from .motor import Motor          # antes vivía en core.py; ahora en motor.py
from .ruedas import Rueda         # el usuario no nota el cambio de archivo

# el usuario siempre escribe lo mismo:
from mi_paquete import Motor, Rueda
```

## Controla __all__

> [!ejemplo]
> Definir `__all__` en `__init__.py` fija **qué nombres** trae `from mi_paquete import *` y documenta la **API pública oficial** del paquete. Lo que no esté en `__all__` se considera detalle interno, aunque sea accesible explícitamente.

```python
# mi_paquete/__init__.py
from .core import Motor, arrancar, _helper_privado
__all__ = ["Motor", "arrancar"]     # _helper_privado queda fuera

# desde fuera
from mi_paquete import *
Motor                                # OK
_helper_privado                      # NameError: no lo trajo el  *
```

Un `__init__.py` **vacío** es válido y suficiente para declarar el paquete; los paquetes *namespace* (PEP 420) incluso prescinden de él. El detalle de cómo `__all__` modela la frontera público/privado se desarrolla en [[62 Exposicion Selectiva (__all__) | __all__]]; el siguiente archivo especial, [[02 __main__.py | __main__.py]], hace **ejecutable** el paquete que este declara.
