---
title: __version__.py
order: 3
tags:
  - python
  - teoria
  - proyectos
draft: false
aliases:
  - version py
  - Versión del paquete
  - Package version
---

# __version__.py

> [!definicion]
> `__version__.py` es una **convención** —no un mecanismo del lenguaje— para exponer la **versión del paquete** en una única variable `__version__`. Centraliza la versión en **un solo lugar** (*single source of truth*), de modo que el código, los metadatos de empaquetado y el usuario lean siempre el mismo número.

```python
# mi_paquete/__version__.py
__version__ = "1.2.3"        # esquema SemVer: MAYOR.MENOR.PARCHE
```

```python
# mi_paquete/__init__.py
from .__version__ import __version__     # lo eleva al nivel del paquete

# desde fuera
import mi_paquete
mi_paquete.__version__        # "1.2.3"
```

Python no trata `__version__.py` de forma especial: es un módulo normal cuyo **nombre** y cuya **variable** son convención de la comunidad. Su valor está en tener la versión **aislada** de la lógica, fácil de leer y de actualizar.

## Dónde se define

> [!regla]
> El patrón habitual es declarar `__version__` en un archivo dedicado (`__version__.py` o `_version.py`) y **re-exportarlo** desde `__init__.py`. Así el archivo de versión no importa el resto del paquete —se puede leer sin ejecutar nada más— y a la vez `mi_paquete.__version__` queda disponible.

```python
# mi_paquete/__version__.py      <- fuente única, sin dependencias
__version__ = "1.2.3"

# mi_paquete/__init__.py
from .__version__ import __version__     # re-exporta
```

Algunos proyectos prescinden del archivo y ponen `__version__ = "1.2.3"` directamente en `__init__.py`; el archivo aparte se prefiere cuando las herramientas de *build* necesitan leer la versión **sin importar el paquete** (que podría tener dependencias aún no instaladas).

## Cómo se lee

> [!info]
> Para **mostrar** la versión se accede a la variable; para **leerla en tiempo de instalación** desde `pyproject.toml` se usa un `dynamic version`; y para consultar la versión de un paquete **ya instalado** sin importarlo, la vía estándar es `importlib.metadata.version`.

```python
import mi_paquete
mi_paquete.__version__                         # "1.2.3"  -> lectura directa

from importlib.metadata import version
version("mi_paquete")                          # "1.2.3"  -> desde los metadatos instalados
```

```toml
# pyproject.toml — versión dinámica leída del paquete
[project]
name = "mi_paquete"
dynamic = ["version"]

[tool.setuptools.dynamic]
version = { attr = "mi_paquete.__version__" }
```

Este archivo cierra los [[51 Archivos Especiales/index | Archivos Especiales]] de la sección. La ubicación física de `__version__.py` dentro del paquete forma parte de la [[52 Estructura de Directorios | estructura de directorios]], que ordena dónde van este y los demás archivos del proyecto.
