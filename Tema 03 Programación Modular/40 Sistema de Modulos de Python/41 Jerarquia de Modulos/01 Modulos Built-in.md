---
title: Módulos Built-in
order: 1
tags:
  - python
  - teoria
  - sistema-modulos
draft: false
aliases:
  - Built-in modules
  - Módulos compilados
---

# Módulos Built-in

> [!definicion]
> Los **módulos built-in** están **compilados dentro del intérprete** de Python (escritos en C y enlazados al ejecutable). **No tienen archivo `.py`**: forman parte del propio Python, por lo que siempre están disponibles sin necesidad de instalar ni de buscarlos en disco. Ejemplos: `sys`, `builtins`, `gc`, `_thread`, `marshal`.

```python
import sys
import gc

sys.version          # versión del intérprete
gc.collect()         # fuerza una recolección de basura
```

Son la capa más interna de la [[41 Jerarquia de Modulos/index | jerarquía de módulos]]: el intérprete los lleva incorporados, a diferencia de la [[02 Libreria Estandar | librería estándar]], que sí son archivos `.py` en disco.

## La lista oficial: `sys.builtin_module_names`

> [!regla]
> `sys.builtin_module_names` es una **tupla** con los nombres de los módulos compilados en **este** intérprete. La lista **depende de la build**: un Python puede traer compilados módulos que en otro son archivos `.py`. Es la fuente de verdad para saber si un módulo es built-in.

```python
import sys

sys.builtin_module_names
# ('_abc', '_ast', '_codecs', 'builtins', 'gc', 'marshal', 'sys', ...)

'sys' in sys.builtin_module_names        # True  -> built-in
'os'  in sys.builtin_module_names        # False -> es un .py de la estándar
```

## No tienen archivo: `__file__` ausente

> [!info]
> Un módulo normal expone el atributo `__file__` con la ruta de su `.py`. Los built-in **carecen de `__file__`** porque no provienen de un archivo: su código vive dentro del ejecutable del intérprete. Intentar leer `__file__` en uno de ellos lanza `AttributeError`.

```python
import os
import sys

os.__file__          # '/usr/lib/python3.12/os.py'  -> tiene archivo
sys.__file__         # AttributeError: module 'sys' has no attribute '__file__'
```

## `builtins`: lo que está siempre disponible

> [!info]
> El módulo built-in `builtins` contiene los nombres del *namespace* global predefinido: `print`, `len`, `range`, `int`, las excepciones, etc. Python lo importa **automáticamente** en cada módulo, por eso usas `print` sin escribir `import builtins`.

```python
import builtins

builtins.len([1, 2, 3])      # 3   -> el mismo len que usas siempre
len is builtins.len          # True
```

Los built-in se localizan **sin recorrer `sys.path`**: el importador los resuelve directamente desde el intérprete, antes que cualquier ruta de disco. Ese orden de búsqueda se detalla en [[42 Mecanismos de Importacion/01 sys.path y PYTHONPATH | sys.path y PYTHONPATH]].
