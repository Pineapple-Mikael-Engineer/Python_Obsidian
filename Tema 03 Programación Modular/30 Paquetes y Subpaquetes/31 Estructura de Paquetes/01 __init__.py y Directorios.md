---
title: __init__.py y Directorios
order: 1
tags:
  - python
  - teoria
  - paquetes
draft: false
aliases:
  - __init__.py
  - Package init
  - Directorio paquete
---

# __init__.py y Directorios

> [!definicion]
> Un **directorio se vuelve un paquete importable** cuando contiene un archivo llamado `__init__.py`. Ese archivo se **ejecuta una sola vez** la primera vez que el paquete se importa, y su namespace pasa a ser el del **propio paquete**. El `__init__.py` puede estar **vacío**, contener **código de inicialización** o **reexportar** símbolos de sus submódulos.

```python
# mi_pkg/
#   __init__.py        <- convierte 'mi_pkg' en paquete
#   geometria.py
#   io_datos.py

import mi_pkg                  # ejecuta mi_pkg/__init__.py una vez
import mi_pkg.geometria        # importa el submódulo
```

Sin `__init__.py`, un directorio normal no es (en general) un paquete regular: importarlo no ejecuta nada y `import mi_pkg.geometria` no resuelve por la vía tradicional. El archivo es el **marcador** que distingue una carpeta cualquiera de un paquete.

## Qué puede contener el `__init__.py`

> [!regla]
> El `__init__.py` tiene tres usos típicos, de menor a mayor implicación:
> - **Vacío** — solo marca el directorio como paquete. Opción más común y limpia.
> - **Código de inicialización** — se ejecuta al importar el paquete: configurar logging, validar dependencias, fijar constantes del paquete.
> - **Reexports** — subir símbolos de los submódulos al nivel del paquete para ofrecer una **interfaz pública** plana.

```python
# mi_pkg/__init__.py  -> caso vacío
# (sin contenido)  -> 'import mi_pkg' funciona, nada más ocurre
```

```python
# mi_pkg/__init__.py  -> con código de inicialización
import logging
logging.getLogger(__name__).addHandler(logging.NullHandler())
VERSION = "1.0.0"              # atributo del paquete: mi_pkg.VERSION
```

```python
# mi_pkg/__init__.py  -> con reexports (API plana)
from .geometria import area_circulo, PI
from .io_datos import leer, escribir
# ahora: from mi_pkg import area_circulo   en vez de   from mi_pkg.geometria import area_circulo
```

## El `__init__.py` se ejecuta una sola vez

> [!info]
> Como cualquier módulo, el paquete se **cachea** en `sys.modules` tras la primera importación. El código del `__init__.py` no se repite en imports posteriores; por eso es seguro poner inicialización ahí, pero conviene mantenerlo **ligero** (los efectos pesados retrasan todo `import` del paquete).

```python
import mi_pkg                  # ejecuta __init__.py
import mi_pkg                  # no lo reejecuta: viene de sys.modules
"mi_pkg" in __import__("sys").modules   # True
```

## Importar el paquete no importa sus submódulos

> [!warning]
> `import mi_pkg` ejecuta su `__init__.py` pero **no** carga automáticamente `mi_pkg.geometria` ni los demás submódulos: cada uno se importa por separado (o desde el `__init__.py` mediante reexports). Acceder a `mi_pkg.geometria` sin haberlo importado —ni reexportado— lanza `AttributeError`.

```python
import mi_pkg
mi_pkg.geometria               # AttributeError si el __init__.py no lo importó
import mi_pkg.geometria        # ahora sí queda disponible
```

El `__init__.py` define qué es y qué expone un paquete; ese paquete se comporta luego como un [[02 Namespace de Paquetes | namespace consultable]], y los reexports son el germen de la [[60 Diseno de APIs Modulares/index | API modular]] que se diseña más adelante. El detalle exhaustivo del archivo vive en su nota dedicada [[01 __init__.py | __init__.py]].
