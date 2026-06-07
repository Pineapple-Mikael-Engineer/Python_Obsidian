---
title: Namespace de Paquetes
order: 2
tags:
  - python
  - teoria
  - paquetes
draft: false
aliases:
  - Package namespace
  - Namespace de paquete
  - __path__
---

# Namespace de Paquetes

> [!definicion]
> Un **paquete es un namespace**: al importarlo, Python crea un objeto `module` cuyo `__dict__` contiene lo definido en su `__init__.py` y los **submódulos** ya importados. Se accede a su contenido con notación de punto —`paquete.modulo`, `paquete.constante`— igual que a los atributos de cualquier objeto. Un atributo exclusivo de los paquetes es `__path__`: la lista de directorios donde buscar sus submódulos.

```python
import mi_pkg
type(mi_pkg)                   # <class 'module'>   -> un paquete TAMBIÉN es un módulo
mi_pkg.VERSION                 # accede a un atributo definido en __init__.py
mi_pkg.geometria               # accede al submódulo (si ya fue importado)
```

Un paquete y un módulo son el **mismo tipo de objeto** (`module`); la diferencia es que el paquete tiene `__path__` y agrupa submódulos, mientras el módulo simple no.

## Atributos del paquete

> [!regla]
> El namespace de un paquete expone varios atributos *dunder* útiles para introspección:
> - `__name__` — nombre completo del paquete (`"mi_pkg"`, `"mi_pkg.utils"`).
> - `__package__` — el paquete al que pertenece (en un paquete, coincide con `__name__`).
> - `__path__` — **solo en paquetes**: lista de rutas donde buscar submódulos.
> - `__file__` — ruta del `__init__.py` que lo define.

```python
import mi_pkg
mi_pkg.__name__                # 'mi_pkg'
mi_pkg.__package__             # 'mi_pkg'
mi_pkg.__file__                # '.../mi_pkg/__init__.py'
mi_pkg.__path__                # ['.../mi_pkg']
hasattr(mi_pkg, "__path__")    # True  -> es un paquete, no un módulo simple
```

## `__path__` guía la búsqueda de submódulos

> [!info]
> Cuando Python resuelve `import mi_pkg.geometria`, no recorre `sys.path`: busca `geometria` **dentro de los directorios de `mi_pkg.__path__`**. Por eso `__path__` es la pieza que hace que un paquete sea un namespace **extensible**: modificarlo (o que abarque varias rutas) cambia dónde se encuentran los submódulos —idea sobre la que se construyen los [[03 Paquetes Namespace (PEP 420) | paquetes namespace]].

```python
import mi_pkg
mi_pkg.__path__                # ['.../mi_pkg']  -> aquí se busca 'geometria'
import mi_pkg.geometria        # encontrado en mi_pkg/geometria.py
```

## Inspeccionar el namespace

> [!ejemplo]
> Como todo objeto módulo, el namespace del paquete se inspecciona con `dir()` o `vars()`. Solo aparecen los nombres definidos en el `__init__.py` y los submódulos ya cargados; los no importados **no** figuran aún.

```python
import mi_pkg
import mi_pkg.geometria
[n for n in dir(mi_pkg) if not n.startswith("__")]
# ['VERSION', 'geometria']   -> io_datos no sale: no se ha importado
```

El paquete-namespace es la base de la [[03 Paquetes Anidados | anidación]]: cada subpaquete es, a su vez, un namespace con su propio `__path__`. Y como objeto `module`, comparte la misma naturaleza que el [[20 Modulos en Python/index | módulo simple]] del que parte todo.
