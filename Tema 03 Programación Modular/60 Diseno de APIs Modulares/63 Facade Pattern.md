---
title: Facade Pattern
order: 63
tags:
  - python
  - teoria
  - apis
draft: false
aliases:
  - Facade Pattern
  - Patrón Facade
  - Fachada
---

# Facade Pattern

> [!definicion]
> El **Facade** (fachada) es un patrón en el que un **módulo o paquete ofrece una interfaz simple y unificada** por encima de varios **subsistemas complejos**. El usuario interactúa solo con la fachada —unos pocos nombres claros— y queda **aislado** de la maraña de submódulos, clases y pasos internos. En Python su forma natural es un **`__init__.py` que re-exporta lo esencial** de un paquete.

```python
# mi_pkg/__init__.py  -> la FACHADA del paquete
from .conexion import _abrir
from .consulta import _ejecutar
from .formato import _a_tabla

def consultar(sql):               # interfaz simple unificada
    conn = _abrir()
    filas = _ejecutar(conn, sql)
    return _a_tabla(filas)

__all__ = ["consultar"]           # el paquete solo expone esto
```

```python
import mi_pkg
mi_pkg.consultar("SELECT 1")      # un solo nombre; los 3 subsistemas, ocultos
```

El consumidor no necesita conocer `conexion`, `consulta` ni `formato`: la fachada **coordina** los subsistemas y presenta **una** función. Internamente puede haber decenas de pasos; por fuera, una sola puerta.

## Re-exportar en `__init__.py`

> [!info]
> La fachada más común no añade lógica, solo **re-exporta**: el `__init__.py` importa los nombres clave de los submódulos para que el paquete se use como si fuera plano. El usuario escribe `from mi_pkg import Motor` sin saber que `Motor` vive en `mi_pkg/nucleo/motor.py`. Esto **desacopla** la API pública de la estructura interna de archivos.

```python
# mi_pkg/__init__.py
from .nucleo.motor import Motor
from .nucleo.bomba import Bomba
from .util.log import registrar

__all__ = ["Motor", "Bomba", "registrar"]
```

```python
from mi_pkg import Motor, Bomba   # plano y limpio
# en vez de:
from mi_pkg.nucleo.motor import Motor   # expondria la estructura interna
```

Reorganizar los submódulos (mover `motor.py` de carpeta) **no rompe** a nadie mientras el `__init__.py` siga re-exportando `Motor`. Ese es el valor de la fachada: la ruta interna es libre, el contrato externo es estable. La declaración del contrato se hace con [[62 Exposicion Selectiva (__all__) | __all__]] y la mecánica de re-exportar es [[03 Import Selectivo (from import) | from import]] dentro del [[01 __init__.py | __init__.py]].

## Por qué simplifica

> [!regla]
> Usa una fachada cuando un paquete tenga **varios subsistemas** y quieras que el 90% de los usuarios trate solo con la **interfaz fácil**, sin renunciar a que el 10% acceda a los submódulos directamente cuando lo necesite. La fachada **no oculta** el interior (sigue importable); solo ofrece el **camino corto** por defecto.

```python
import mi_pkg
mi_pkg.consultar("...")           # camino facil: la fachada
from mi_pkg.consulta import _ejecutar   # camino avanzado: aun disponible
```

## Facade vs API plana

> [!ejemplo]
> Sin fachada, el usuario debe **navegar la estructura** del paquete e importar de cada submódulo, acoplándose a su disposición de archivos. Con fachada, importa de **un único punto** y la estructura interna queda libre de evolucionar.

```python
# Sin fachada -> el usuario depende de la estructura interna
from mi_pkg.conexion import abrir
from mi_pkg.consulta import ejecutar
from mi_pkg.formato import a_tabla

# Con fachada -> un punto de entrada, estructura interna libre
from mi_pkg import consultar
```

El Facade cierra el [[60 Diseno de APIs Modulares/index | diseño de APIs modulares]]: tras **distinguir** público de privado ([[61 Interfaces Publicas vs Privadas | Interfaces Públicas vs Privadas]]) y **declararlo** con [[62 Exposicion Selectiva (__all__) | __all__]], la fachada **unifica** todo en una cara simple. Es además un puente hacia los [[70 Patrones de Diseno Modular/index | Patrones de Diseño Modular]], que construyen sobre esta misma idea de organizar la interfaz de un paquete.
