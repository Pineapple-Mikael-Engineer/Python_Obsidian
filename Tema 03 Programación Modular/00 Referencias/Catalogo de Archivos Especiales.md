---
title: Catálogo de Archivos Especiales
order: 1
tags:
  - python
  - teoria
  - modular
draft: false
aliases:
  - Catálogo de Archivos y Atributos Especiales
  - Archivos Especiales del Sistema Modular
  - Dunder de Módulo
---

# Catálogo de Archivos Especiales

Tabla de consulta de los **archivos** (`__x__.py`) y **atributos** (`__x__`) que Python reconoce de forma especial al construir el sistema modular. Unos son ficheros que el intérprete busca por nombre; otros son nombres que el sistema de importación **inyecta** en el namespace de cada módulo o paquete. El desarrollo de cada uno vive en [[51 Archivos Especiales/index | Archivos Especiales]] y en [[50 Organizacion de Proyectos/index | Organización de Proyectos]].

> [!info] Archivo vs atributo
> `__init__.py`, `__main__.py` y `__version__.py` son **archivos** en disco. `__all__`, `__name__`, `__path__` y `__package__` son **atributos** del objeto módulo: el sistema de importación los define automáticamente (salvo `__all__`, que escribes tú) y se leen con `modulo.__x__`.

## Resumen

| Nombre | Tipo | Dónde vive | Propósito |
| ------ | ---- | ---------- | --------- |
| `__init__.py` | archivo | raíz de un paquete (directorio) | Declara el directorio como paquete; inicializa y expone su API. Ver [[01 __init__.py \| __init__.py]] |
| `__main__.py` | archivo | raíz de un paquete ejecutable | Punto de entrada de `python -m paquete`. Ver [[02 __main__.py \| __main__.py]] |
| `__version__.py` | archivo | dentro del paquete | Convención para alojar la versión en una sola fuente. Ver [[03 __version__.py \| __version__.py]] |
| `__all__` | atributo | en un módulo o `__init__.py` | Lista de nombres que exporta `from modulo import *`. Ver [[62 Exposicion Selectiva (__all__) \| __all__]] |
| `__name__` | atributo | todo módulo | Nombre del módulo; vale `"__main__"` si se ejecuta directamente. Ver [[03 __name__ y __main__ \| __name__]] |
| `__path__` | atributo | solo paquetes | Lista de rutas donde se buscan los submódulos del paquete |
| `__package__` | atributo | todo módulo | Nombre del paquete contenedor; base de los imports relativos |

## Archivos en disco

### `__init__.py`

Su sola presencia convierte un directorio en **paquete regular**. Suele estar vacío, o reexportar la API pública del paquete para acortar las rutas de import.

```python
# mi_paquete/__init__.py
from .geometria import area_circulo, area_rectangulo
from .io_datos import cargar, guardar

__all__ = ["area_circulo", "area_rectangulo", "cargar", "guardar"]
__version__ = "1.0.0"

# Permite:  from mi_paquete import area_circulo
# en vez de: from mi_paquete.geometria import area_circulo
```

### `__main__.py`

Hace **ejecutable** un paquete con `python -m mi_paquete`. Es al paquete lo que el bloque `if __name__ == "__main__":` es a un módulo suelto.

```python
# mi_paquete/__main__.py
from .cli import main

if __name__ == "__main__":
    main()

# Se lanza con:  python -m mi_paquete
```

### `__version__.py`

Aloja la versión en **una sola fuente de verdad** (*single source of truth*), que luego leen `__init__.py` y la configuración de empaquetado.

```python
# mi_paquete/__version__.py
__version__ = "1.0.0"

# mi_paquete/__init__.py
from .__version__ import __version__

# Uso:  import mi_paquete; mi_paquete.__version__   -> "1.0.0"
```

## Atributos inyectados

### `__all__`

Lista de cadenas con los nombres que `from modulo import *` traerá. Controla la **interfaz pública** y silencia los nombres no listados; no afecta a los imports explícitos.

```python
# calculo.py
__all__ = ["sumar", "restar"]      # multiplicar queda fuera del import *

def sumar(a, b): return a + b
def restar(a, b): return a - b
def multiplicar(a, b): return a * b

# from calculo import *   ->  expone sumar, restar (NO multiplicar)
```

### `__name__`

Nombre con el que se conoce el módulo. Vale `"__main__"` cuando el archivo se ejecuta como script y el nombre de import (`"paquete.modulo"`) cuando se importa. Base del *idiom* de doble uso.

```python
# script.py
print(__name__)                    # importado: "script"  |  ejecutado: "__main__"

if __name__ == "__main__":
    print("ejecutado directamente, no importado")
```

### `__path__`

Solo existe en **paquetes**. Lista de directorios donde Python busca los submódulos del paquete; su manipulación es la base de los *namespace packages*.

```python
import os
print(os.__path__)         # no existe -> os es un modulo, no un paquete

import xml
print(xml.__path__)        # ['/usr/lib/python3.x/xml']  -> xml es un paquete
```

### `__package__`

Nombre del paquete al que pertenece el módulo. El sistema de importación lo usa para **resolver los imports relativos** (`from . import x`). En un script ejecutado directamente vale `""` o `None`, por eso los imports relativos fallan ahí.

```python
# dentro de mi_paquete/sub/modulo.py
print(__package__)         # "mi_paquete.sub"

from . import otro         # resuelto contra __package__
```

> [!warning] Por qué fallan los imports relativos en un script
> Al ejecutar `python modulo.py`, su `__name__` es `"__main__"` y su `__package__` queda vacío: sin paquete base, `from . import x` lanza `ImportError`. La solución es ejecutar con `python -m paquete.modulo`, que sí fija `__package__`. Ver [[02 Import Relativo \| Import Relativo]].
