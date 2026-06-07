---
title: Paquetes Anidados
order: 3
tags:
  - python
  - teoria
  - paquetes
draft: false
aliases:
  - Nested packages
  - Subpaquetes
  - Paquetes anidados
---

# Paquetes Anidados

> [!definicion]
> Un **paquete anidado** (o **subpaquete**) es un paquete que vive **dentro de otro paquete**: un directorio con su propio `__init__.py` situado en la carpeta de un paquete padre. La anidación genera una **jerarquía** que se nombra con puntos —`paquete.subpaquete.modulo`— de cualquier profundidad. Cada nivel es, a su vez, un [[02 Namespace de Paquetes | namespace]] con su propio `__path__`.

```python
# mi_pkg/
#   __init__.py
#   geometria.py
#   utils/                 <- subpaquete: tiene su propio __init__.py
#     __init__.py
#     validar.py
#     formato.py

import mi_pkg.utils.validar          # jerarquía: paquete.subpaquete.modulo
from mi_pkg.utils import formato     # trae el módulo 'formato' del subpaquete
```

Cada `__init__.py` de la cadena declara su nivel como paquete; la ruta de puntos refleja **exactamente** la ruta de directorios en disco.

## Cómo se importa la cadena

> [!regla]
> Importar `mi_pkg.utils.validar` ejecuta, **en orden y una sola vez cada uno**, los `__init__.py` de **todos los paquetes intermedios**: primero `mi_pkg/__init__.py`, luego `mi_pkg/utils/__init__.py`, y por último carga `validar.py`. No se puede saltar un nivel: cada paquete de la ruta debe ser importable.

```python
import mi_pkg.utils.validar
# ejecuta:  mi_pkg/__init__.py  ->  mi_pkg/utils/__init__.py  ->  validar.py
import sys
"mi_pkg" in sys.modules                # True
"mi_pkg.utils" in sys.modules          # True  -> los intermedios también se cachean
"mi_pkg.utils.validar" in sys.modules  # True
```

## Acceso por atributos tras importar

> [!info]
> Tras `import mi_pkg.utils.validar`, los paquetes intermedios quedan accesibles como **atributos encadenados** del paquete raíz: `mi_pkg.utils` y `mi_pkg.utils.validar` se resuelven por punto. Esto ocurre porque cada paquete registra a su subpaquete como atributo de su namespace al importarlo.

```python
import mi_pkg.utils.validar
mi_pkg.utils                   # <module 'mi_pkg.utils'>
mi_pkg.utils.validar           # <module 'mi_pkg.utils.validar'>
mi_pkg.utils.validar.es_valido(3)
```

## Cómo organizar la jerarquía

> [!ejemplo]
> Los subpaquetes agrupan submódulos por **afinidad**: cada uno reúne lo cohesivo y se nombra por su responsabilidad. El `__init__.py` de un subpaquete puede reexportar su propia API para acortar las rutas de import.

```python
# mi_pkg/utils/__init__.py
from .validar import es_valido
from .formato import a_titulo
# permite:  from mi_pkg.utils import es_valido   (sin nombrar 'validar')
```

```python
# mi_proyecto/
#   __init__.py
#   core/            -> lógica central
#   io/              -> entrada/salida
#   utils/           -> utilidades transversales
#     io/            -> anidación de cualquier profundidad
```

La anidación es la forma estructural de aplicar **alta cohesión** a escala de proyecto. Cómo se referencian estos niveles entre sí —ruta completa o relativa— es trabajo de los [[32 Sistemas de Importacion/index | sistemas de importación]]; la organización de directorios resultante se trata en [[50 Organizacion de Proyectos/index | Organización de Proyectos]].
