---
title: Module vs Package vs Subpackage
order: 53
tags:
  - python
  - teoria
  - proyectos
draft: false
aliases:
  - Módulo vs Paquete vs Subpaquete
  - Module Package Subpackage
---

# Module vs Package vs Subpackage

> [!definicion]
> Las tres piezas de la organización modular se distinguen por **qué son en el disco**: un **módulo** es un **archivo** `.py`; un **paquete** es un **directorio** con `__init__.py` que agrupa módulos; un **subpaquete** es un **paquete anidado dentro de otro paquete**. La diferencia es estructural —archivo, carpeta, carpeta dentro de carpeta— pero todos comparten ser **objetos `module`** con su propio *namespace*.

```python
mi_paquete/                 # paquete:    directorio con __init__.py
├── __init__.py
├── geometria.py            # módulo:      archivo .py dentro del paquete
└── utils/                  # subpaquete:  paquete anidado en mi_paquete
    ├── __init__.py
    └── validacion.py       # módulo del subpaquete

# rutas de import que genera esta estructura:
import mi_paquete                       # paquete
import mi_paquete.geometria             # módulo
import mi_paquete.utils                 # subpaquete
import mi_paquete.utils.validacion      # módulo del subpaquete
```

El nombre con puntos (`mi_paquete.utils.validacion`) **refleja literalmente** la jerarquía de carpetas: cada punto es un nivel de directorio, salvo el último, que es el archivo `.py`.

## Tabla comparativa

> [!regla]
> Lo que decide la categoría es la **forma en disco**, no el contenido. Un directorio **sin** `__init__.py` puede ser un *paquete namespace* (PEP 420), pero el caso clásico exige el `__init__.py` para que cuente como paquete regular.

| Pieza | Qué es en disco | Señal que la identifica | Ejemplo de import |
| ----- | --------------- | ----------------------- | ----------------- |
| **Módulo** | un archivo `.py` | extensión `.py` | `import geometria` |
| **Paquete** | un directorio | contiene `__init__.py` | `import mi_paquete` |
| **Subpaquete** | un directorio **dentro** de un paquete | `__init__.py` + estar anidado | `import mi_paquete.utils` |

## Todos son objetos module

> [!info]
> Pese a la diferencia estructural, al importar cualquiera de los tres se obtiene una **instancia de la clase `module`**. Un paquete se distingue de un módulo simple en tiempo de ejecución por tener el atributo `__path__` (la lista de directorios donde buscar sus submódulos); un módulo suelto no lo tiene.

```python
import mi_paquete
import mi_paquete.geometria

type(mi_paquete)                 # <class 'module'>
type(mi_paquete.geometria)       # <class 'module'>  -> misma clase

hasattr(mi_paquete, "__path__")             # True   -> es paquete
hasattr(mi_paquete.geometria, "__path__")   # False  -> es módulo simple
```

## La relación es de anidamiento

> [!ejemplo]
> «Subpaquete» no es una categoría aparte: es un **paquete que resulta estar dentro de otro**. La misma carpeta `utils/` es un *paquete* visto en solitario y un *subpaquete* visto desde `mi_paquete`. La distinción es **relativa a la posición**, no a la naturaleza.

```python
# utils/ visto en solitario  -> es un paquete
import utils

# utils/ visto desde mi_paquete  -> es un subpaquete
import mi_paquete.utils
```

En resumen: **módulo = archivo**, **paquete = directorio con `__init__.py`**, **subpaquete = paquete anidado**. Esta jerarquía es la que organiza la [[52 Estructura de Directorios | estructura de directorios]] del proyecto, y el `__init__.py` que convierte un directorio en paquete es el primero de los [[51 Archivos Especiales/index | Archivos Especiales]].
