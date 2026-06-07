---
title: Namespace del Módulo
order: 2
tags:
  - python
  - teoria
  - modulos
draft: false
aliases:
  - Espacio de nombres del modulo
  - Module namespace
  - __dict__ del modulo
---

# Namespace del Módulo

> [!definicion]
> Cada módulo tiene su **propio espacio de nombres**: una tabla que asocia cada nombre definido en el archivo con su objeto. Ese espacio es el atributo `__dict__` del módulo, y desde fuera se accede a sus miembros como `modulo.nombre`. Los nombres de dos módulos **no colisionan**: `geometria.PI` y `fisica.PI` son independientes porque viven en namespaces distintos.

```python
# geometria.py
PI = 3.14159
def area(r):
    return PI * r ** 2

import geometria
geometria.PI                     # 3.14159  -> acceso cualificado
geometria.__dict__["PI"]         # 3.14159  -> el namespace es un dict
geometria.__dict__ is vars(geometria)  # True
```

`modulo.nombre` es, literalmente, una búsqueda en `modulo.__dict__`. Asignar `geometria.PI = 3` modifica esa entrada del namespace del módulo.

## Inspeccionar el namespace

> [!regla]
> `dir(modulo)` lista **los nombres** que expone el módulo (ordenados), incluidos los *dunder* como `__name__` o `__doc__`. `vars(modulo)` y `modulo.__dict__` devuelven el **dict completo** nombre → objeto. Son la forma estándar de explorar qué define un módulo desde fuera.

```python
import math
dir(math)[:4]                    # ['__doc__', '__loader__', '__name__', '__package__']
"sqrt" in dir(math)              # True
math.__dict__["sqrt"]            # <built-in function sqrt>
```

## globals() es el namespace del propio módulo

> [!info]
> **Dentro** de un módulo, `globals()` devuelve **su propio `__dict__`**: el namespace global de un módulo es el namespace de ese módulo. Las variables de nivel superior son, por tanto, globales **del módulo**, no del programa entero —no existe un global compartido entre archivos.

```python
# datos.py
TOTAL = 100
def info():
    return globals() is datos.__dict__   # se vera True al ejecutarse

import datos
datos.__dict__ is vars(datos)    # True
# dentro de datos.py: globals()["TOTAL"]  ->  100
```

> [!warning]
> Cada archivo tiene su propio global. Una variable definida en `a.py` **no** es visible en `b.py` con solo nombrarla: hay que importarla. Esto es deliberado —es lo que evita que los módulos se pisen— y es la diferencia entre modularidad y un montón de variables sueltas.

El namespace aislado es lo que hace seguro reutilizar nombres entre archivos; ese mismo módulo distingue si se está **ejecutando** o **importando** a través de [[03 __name__ y __main__ | `__name__`]], y traer sus nombres al namespace propio es el trabajo de la [[22 Importacion de Modulos/index | importación]].
