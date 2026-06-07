---
title: Import Relativo
order: 2
tags:
  - python
  - teoria
  - paquetes
draft: false
aliases:
  - Relative import
  - Importación relativa
---

# Import Relativo

> [!definicion]
> Un **import relativo** nombra el módulo **desde el paquete actual**, usando puntos iniciales como referencia: un punto (`.`) es el paquete que contiene el archivo, dos puntos (`..`) suben un nivel, y así sucesivamente. `from . import x` trae `x` del paquete actual; `from ..pkg import y` sube uno y baja a `pkg`. Solo tiene forma `from`: no existe `import .modulo`.

```python
# dentro de mi_pkg/core/procesar.py
from . import validar              # 'validar' del MISMO paquete (mi_pkg.core)
from .ayudas import limpiar        # símbolo de un módulo hermano
from ..utils import formato        # sube a mi_pkg, baja a utils
from ..utils.validar import es_valido
```

El número de puntos indica **cuántos niveles subir** en la jerarquía antes de resolver el resto del nombre; un punto no sube, parte del paquete actual.

## El punto es el paquete, no el archivo

> [!regla]
> Los puntos cuentan **paquetes**, no archivos:
> - `.` — el paquete que **contiene** el módulo actual.
> - `..` — el paquete **padre** de ese paquete.
> - `...` — el abuelo, y así sucesivamente.
>
> La referencia se calcula a partir de `__package__` del módulo, no de su ruta en disco.

```python
# mi_pkg/core/procesar.py   ->   __package__ == "mi_pkg.core"
from . import validar       # busca en  mi_pkg.core
from .. import config       # busca en  mi_pkg
```

## Solo válido dentro de paquetes

> [!warning]
> Un import relativo **falla** si el archivo se ejecuta como **script directo** (`python procesar.py`): en ese caso `__package__` queda vacío y Python lanza `ImportError: attempted relative import with no known parent package`. Los imports relativos solo funcionan cuando el módulo se importa **como parte de un paquete**.
>
> Para ejecutar un módulo de paquete usa `python -m mi_pkg.core.procesar` desde la raíz: así `__package__` se fija correctamente y los relativos resuelven.

```python
# python mi_pkg/core/procesar.py   -> ImportError (no hay paquete padre)
# python -m mi_pkg.core.procesar   -> OK: __package__ = "mi_pkg.core"
```

## Cuándo conviene

> [!ejemplo]
> El import relativo gana cuando, **dentro de un paquete**, la ruta absoluta es larga y repetitiva, o cuando quieres que el paquete sea **renombrable/movible** sin tocar sus imports internos: al no nombrar la raíz, mover `mi_pkg` a otro nombre no rompe sus referencias internas.

```python
# import RELATIVO  -> conciso, no nombra la raíz 'mi_pkg'
from ..utils.validar import es_valido

# import ABSOLUTO equivalente -> robusto pero repite la raíz en cada archivo
from mi_pkg.utils.validar import es_valido
```

PEP 8 prefiere el [[01 Import Absoluto | import absoluto]] por su claridad, y reserva el relativo para imports **internos** de paquetes complejos. Su dependencia de `__package__` lo liga a la ejecución como paquete; los detalles de esa maquinaria están en [[40 Sistema de Modulos de Python/index | Sistema de Módulos de Python]].
