---
title: sys.path y PYTHONPATH
order: 1
tags:
  - python
  - teoria
  - sistema-modulos
draft: false
aliases:
  - sys.path
  - PYTHONPATH
  - Ruta de búsqueda de módulos
---

# sys.path y PYTHONPATH

> [!definicion]
> **`sys.path`** es la **lista de rutas** donde Python busca un módulo al importarlo. Ante `import M`, recorre `sys.path` **en orden** y usa la **primera** carpeta que contenga `M`. **`PYTHONPATH`** es la variable de entorno que **añade rutas** a esa lista antes de arrancar el intérprete.

```python
import sys

sys.path
# ['', '/usr/lib/python312.zip', '/usr/lib/python3.12',
#  '.../site-packages', ...]
```

`sys.path` es el "dónde" del [[42 Mecanismos de Importacion/index | mecanismo de importación]]: solo entra en juego para los módulos que se buscan en disco; los [[41 Jerarquia de Modulos/01 Modulos Built-in | built-in]] se resuelven antes, dentro del intérprete.

## El orden de búsqueda

> [!regla]
> Python busca un módulo en este orden: **(1)** los **built-in** (compilados, sin tocar `sys.path`); **(2)** la **caché** `sys.modules`; **(3)** las rutas de `sys.path` **de izquierda a derecha**, deteniéndose en la primera coincidencia. El orden importa: una carpeta anterior **eclipsa** un módulo del mismo nombre en una posterior.

```python
import sys

sys.path[0]          # '' o la carpeta del script -> se busca AQUÍ primero
# un geometria.py local gana sobre uno instalado en site-packages
```

## Cómo se compone `sys.path`

> [!info]
> Al arrancar, Python construye `sys.path` con: la **carpeta del script** (o `''` para el directorio actual en el REPL), las rutas de **`PYTHONPATH`**, las de la **librería estándar** y el **`site-packages`** de la instalación o el entorno virtual.

```python
import sys
for ruta in sys.path:
    print(ruta or "(directorio actual)")
```

## Modificar la ruta en caliente: `sys.path`

> [!regla]
> `sys.path` es una **lista normal**: se puede `append` o `insert` en tiempo de ejecución para añadir carpetas de búsqueda. `insert(0, ...)` le da **prioridad máxima**; `append` la deja de última. El cambio solo dura lo que dure el proceso.

```python
import sys

sys.path.append("/ruta/extra")       # se busca de último
sys.path.insert(0, "/ruta/extra")    # se busca de primero (eclipsa al resto)
import mi_modulo                      # ahora localizable
```

## Añadir rutas desde fuera: `PYTHONPATH`

> [!info]
> **`PYTHONPATH`** es una variable de entorno con carpetas separadas por `:` (Linux/macOS) o `;` (Windows). Sus rutas se insertan en `sys.path` **antes** de las de la estándar, sin tocar el código. Útil para que un proyecto encuentre sus módulos sin modificar `sys.path` a mano.

```bash
export PYTHONPATH="/ruta/a/mis/modulos"   # Linux/macOS
python main.py                            # ya ve esos módulos
```

```python
import sys
'/ruta/a/mis/modulos' in sys.path         # True dentro del proceso
```

Una vez localizado por `sys.path`, el módulo se ejecuta y se guarda en la caché [[02 sys.modules (Cache) | sys.modules]], que evita repetir la búsqueda y la ejecución en los siguientes `import`.
