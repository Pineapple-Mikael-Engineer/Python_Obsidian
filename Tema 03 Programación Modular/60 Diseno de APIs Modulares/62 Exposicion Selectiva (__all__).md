---
title: Exposición Selectiva (__all__)
order: 62
tags:
  - python
  - teoria
  - apis
draft: false
aliases:
  - __all__
  - Exposición Selectiva
  - Selective Export
---

# Exposición Selectiva (__all__)

> [!definicion]
> `__all__` es una **lista de cadenas** —nombres— que un módulo define para declarar **qué exporta `from modulo import *`**. Cuando existe, `import *` trae **solo** los nombres listados en `__all__`; cuando no existe, trae todos los nombres del módulo que **no empiezan por guion bajo**. Es la forma de **declarar explícitamente la superficie pública** del módulo.

```python
# texto.py
__all__ = ["limpiar", "Titulo"]   # solo estos salen con import *

def limpiar(s): return s.strip()
class Titulo: ...
def _interno(s): return s.lower() # privado, no esta en __all__
```

```python
from texto import *
limpiar("  hi ")                  # OK    -> esta en __all__
Titulo()                          # OK    -> esta en __all__
_interno("X")                     # NameError -> import * no lo trajo
```

`__all__` es la versión **explícita** de la frontera que la convención `_nombre` marca de forma implícita; ver [[61 Interfaces Publicas vs Privadas | Interfaces Públicas vs Privadas]].

## Controla la superficie, no el acceso

> [!warning]
> `__all__` **solo afecta a `from modulo import *`**. **No impide** importar un nombre directamente: `from texto import _interno` y `texto._interno` siguen funcionando aunque no estén en `__all__`. No es un mecanismo de protección, sino una **declaración de intención** sobre qué es público.

```python
import texto
texto._interno("X")               # funciona: __all__ no bloquea el acceso
from texto import _interno        # tambien funciona, es import explicito
```

Lo que `__all__` controla es el **`import *`**, la única forma de importación que de otro modo arrastra todo el namespace. Por eso define la *cara* del módulo sin restringir su *interior*.

## Útil tanto en módulo como en paquete

> [!info]
> En un **módulo** (`.py`), `__all__` filtra qué se exporta con `import *`. En el **`__init__.py`** de un **paquete**, `__all__` cumple lo mismo a nivel de paquete: lista los nombres que el paquete ofrece como API, normalmente re-exportados desde sus submódulos. Así el paquete presenta una superficie curada en vez de exponer su estructura interna.

```python
# mi_pkg/__init__.py
from .nucleo import Motor, arrancar
from .util import formatear

__all__ = ["Motor", "arrancar"]   # 'formatear' queda fuera del import *
```

```python
from mi_pkg import *
Motor(); arrancar()               # API publica del paquete
formatear("x")                    # NameError -> no esta en __all__ del paquete
```

Declarar `__all__` en el `__init__.py` es la base del [[63 Facade Pattern | Facade Pattern]]: el paquete re-exporta lo esencial y oculta el resto. La sintaxis `from .modulo import X` que aparece aquí es [[03 Import Selectivo (from import) | from import]] aplicado al paquete, y el papel del [[01 __init__.py | __init__.py]] como punto de entrada se trata en su propia nota.

## Cuándo definirlo

> [!regla]
> Define `__all__` cuando quieras **fijar de forma explícita** la API pública: en módulos pensados para reutilizarse y, sobre todo, en `__init__.py` de paquetes. Si no lo defines, el comportamiento por defecto (exportar lo que no empieza por `_`) suele bastar para scripts y módulos internos.

```python
# Sin __all__: import * trae todo lo que no empiece por _
# Con __all__:  import * trae exactamente la lista -> contrato explicito
__all__ = ["procesar", "Config"]
```

`__all__` es la pieza intermedia del [[60 Diseno de APIs Modulares/index | diseño de la API]]: convierte la **convención** en **declaración**, y prepara el terreno para que un paquete ofrezca una sola fachada limpia con el [[63 Facade Pattern | Facade Pattern]].
