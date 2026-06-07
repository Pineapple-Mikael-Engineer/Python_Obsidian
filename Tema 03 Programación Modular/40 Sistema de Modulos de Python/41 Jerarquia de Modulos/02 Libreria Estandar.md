---
title: Librería Estándar
order: 2
tags:
  - python
  - teoria
  - sistema-modulos
draft: false
aliases:
  - Standard library
  - Batteries included
---

# Librería Estándar

> [!definicion]
> La **librería estándar** es el conjunto de módulos que **acompaña a toda instalación de Python**, sin necesidad de instalar nada. A diferencia de los [[01 Modulos Built-in | built-in]], son **archivos `.py`** (más algunos módulos de extensión) que viven en el directorio de la instalación. Es la filosofía **"batteries included"**: lo esencial ya viene puesto.

```python
import os              # sistema operativo, rutas, procesos
import json            # serializar / deserializar JSON
import datetime        # fechas y horas
import collections     # estructuras de datos (deque, Counter, defaultdict)

datetime.date.today()              # date(2026, 6, 6)
collections.Counter("abracadabra") # Counter({'a': 5, 'b': 2, 'r': 2, ...})
```

Ocupa la segunda capa de la [[41 Jerarquia de Modulos/index | jerarquía de módulos]]: viene con Python como los built-in, pero —al ser archivos en disco— sí expone `__file__` y se localiza recorriendo `sys.path`.

## Vienen con Python, pero son archivos `.py`

> [!regla]
> Los módulos de la estándar **no se instalan con `pip`**: ya están en la instalación. Pero, salvo los compilados, son `.py` ordinarios: tienen `__file__`, se pueden leer y depurar, y se importan exactamente igual que cualquier módulo propio.

```python
import json

json.__file__        # '/usr/lib/python3.12/json/__init__.py'  -> es un .py
json.dumps({"a": 1}) # '{"a": 1}'
```

## Panorama de módulos frecuentes

> [!info]
> La estándar cubre la mayoría de tareas comunes sin dependencias externas. Una visión general por áreas:

| Área | Módulos | Para qué |
| ---- | ------- | -------- |
| Sistema y rutas | `os`, `sys`, `pathlib`, `shutil` | archivos, procesos, entorno |
| Datos y formatos | `json`, `csv`, `pickle`, `sqlite3` | serializar y persistir |
| Fechas y tiempo | `datetime`, `time`, `calendar` | fechas, relojes |
| Estructuras | `collections`, `itertools`, `functools` | datos y utilidades funcionales |
| Texto y números | `re`, `math`, `random`, `decimal` | regex, matemáticas |
| Red y web | `urllib`, `http`, `socket` | peticiones, sockets |

```python
import pathlib

ruta = pathlib.Path("datos") / "config.json"
ruta.suffix          # '.json'   -> sin instalar nada externo
```

## Estándar frente a built-in y terceros

> [!regla]
> **Built-in**: compilados, sin `.py`, siempre presentes. **Estándar**: archivos `.py`, vienen con Python, sin `pip`. **Terceros**: archivos `.py`, **se instalan con `pip`** y viven en `site-packages`. Las tres se importan igual; cambia solo el origen.

```python
import sys, json

'json' in sys.builtin_module_names   # False -> NO es built-in
hasattr(json, '__file__')            # True  -> es un .py de la estándar
```

Cuando una tarea excede lo que cubre la estándar, se recurre a los [[03 Modulos de Terceros | módulos de terceros]] de PyPI; cuando es lógica propia del proyecto, a los [[04 Modulos Personalizados | módulos personalizados]].
