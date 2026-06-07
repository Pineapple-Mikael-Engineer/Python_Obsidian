---
title: Módulos Personalizados
order: 4
tags:
  - python
  - teoria
  - sistema-modulos
draft: false
aliases:
  - Custom modules
  - Módulos propios
  - Módulos del proyecto
---

# Módulos Personalizados

> [!definicion]
> Los **módulos personalizados** son los **archivos `.py` del propio proyecto**: el código que tú escribes. No se instalan ni vienen con Python; Python los encuentra porque sus directorios están en `sys.path`, encabezado por la **raíz desde la que se ejecuta** el programa.

```python
# geometria.py  -> módulo personalizado en la raíz del proyecto
PI = 3.14159
def area_circulo(r):
    return PI * r ** 2

# main.py  -> lo importa por su nombre, sin ruta ni instalación
import geometria
geometria.area_circulo(2)        # 12.566...
```

Son la última capa de la [[41 Jerarquia de Modulos/index | jerarquía de módulos]]: a diferencia de los [[03 Modulos de Terceros | de terceros]], no pasan por `pip` ni por `site-packages`; viven junto a tu código y se resuelven por proximidad.

## Cómo los encuentra Python: la raíz del proyecto

> [!regla]
> Al lanzar `python main.py`, Python coloca el **directorio del script** (`main.py`) al **inicio de `sys.path`**. Por eso `import geometria` encuentra `geometria.py` si está junto a `main.py`: la **raíz de ejecución** es el primer lugar donde se busca, antes que la estándar o los terceros.

```python
import sys

sys.path[0]          # '' o la carpeta del script -> la raíz de ejecución
# desde ahí Python ve los .py hermanos como módulos importables
```

## El nombre del archivo es el nombre del módulo

> [!info]
> El nombre del módulo personalizado es el del archivo **sin la extensión `.py`**: `geometria.py` se importa como `geometria`. Debe ser un identificador válido (sin guiones ni empezar por dígito) para poder usarse en un `import`.

```python
# archivo: utils_io.py   -> import utils_io      (válido)
# archivo: utils-io.py   -> import utils-io      (SyntaxError: el guion no es válido)
import utils_io
utils_io.__name__        # 'utils_io'
```

## Cuando el módulo no está en la raíz

> [!regla]
> Si el módulo vive en otra carpeta no incluida en `sys.path`, el `import` falla con `ModuleNotFoundError`. Las salidas habituales: ejecutar con `python -m paquete.modulo` desde la raíz, organizar el código como [[30 Paquetes y Subpaquetes/index | paquete]], o ajustar la ruta de búsqueda.

```python
import sys
sys.path.append("/ruta/a/mis/modulos")   # añade la carpeta a la búsqueda
import mi_modulo                          # ahora sí lo encuentra
```

La lista exacta de rutas y cómo ampliarla —con `sys.path` o con la variable `PYTHONPATH`— se trata en [[42 Mecanismos de Importacion/01 sys.path y PYTHONPATH | sys.path y PYTHONPATH]]; la forma limpia de agrupar varios módulos propios es convertirlos en un [[30 Paquetes y Subpaquetes/index | paquete]].
