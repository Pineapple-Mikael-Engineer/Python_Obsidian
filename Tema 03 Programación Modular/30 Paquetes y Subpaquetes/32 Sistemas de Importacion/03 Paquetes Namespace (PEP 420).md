---
title: Paquetes Namespace (PEP 420)
order: 3
tags:
  - python
  - teoria
  - paquetes
draft: false
aliases:
  - Namespace packages
  - PEP 420
  - Paquetes namespace
---

# Paquetes Namespace (PEP 420)

> [!definicion]
> Un **paquete namespace** (PEP 420, desde Python 3.3) es un paquete **sin `__init__.py`** cuyo contenido puede estar **repartido en varias rutas** de `sys.path`. Python fusiona todas esas porciones en un único paquete lógico: un mismo nombre de paquete cuyos submódulos viven en directorios distintos, posiblemente instalados por separado.

```python
# Dos ubicaciones distintas en sys.path, sin __init__.py:
#   ruta_a/  plugins/  motor_a.py
#   ruta_b/  plugins/  motor_b.py

import plugins.motor_a            # encontrado en ruta_a
import plugins.motor_b            # encontrado en ruta_b  -> mismo paquete 'plugins'
plugins.__path__                  # abarca AMBAS rutas
```

El paquete `plugins` no existe como una sola carpeta: es un **namespace virtual** ensamblado a partir de todas las carpetas `plugins/` halladas en `sys.path`.

## En qué se diferencia de un paquete regular

> [!regla]
> Frente al [[01 __init__.py y Directorios | paquete regular]]:
> - **Sin `__init__.py`** — el directorio no lleva ese archivo (si lo lleva, deja de ser namespace y vuelve a ser regular).
> - **Multi-ruta** — su `__path__` es un objeto especial (`_NamespacePath`) que puede contener **varias** carpetas, no una sola.
> - **Sin código de inicialización** — al no haber `__init__.py`, no se ejecuta nada al importar el paquete; no puede reexportar ni inicializar.

```python
import plugins
type(plugins.__path__)            # <class '_frozen_importlib_external._NamespacePath'>
list(plugins.__path__)            # ['.../ruta_a/plugins', '.../ruta_b/plugins']
plugins.__file__                  # AttributeError: no hay __init__.py
```

## Cuándo se usan

> [!info]
> Los paquetes namespace sirven para **repartir un mismo paquete entre varias distribuciones** instalables por separado: el caso típico es un sistema de **plugins** donde cada extensión se publica y se instala de forma independiente, pero todas comparten el namespace común (`empresa.plugin_x`, `empresa.plugin_y`). Cada paquete se instala bajo `empresa/` sin pisar a los demás, porque ninguno aporta el `__init__.py` que reclamaría el namespace en exclusiva.

```python
# Paquetes instalados por separado, mismo namespace 'empresa':
import empresa.facturacion        # de un paquete pip
import empresa.reportes           # de OTRO paquete pip distinto
# ambos coexisten bajo 'empresa' gracias al namespace de PEP 420
```

## Regular vs namespace de un vistazo

> [!ejemplo]
> La presencia de `__init__.py` es lo que decide el tipo. Para un paquete normal de proyecto se prefiere el **regular** (con `__init__.py`, aunque esté vacío): es más explícito y permite inicialización. El **namespace** se reserva para el caso concreto de distribución repartida.

```python
# mi_app/__init__.py            -> paquete REGULAR (recomendado por defecto)
# empresa/  (sin __init__.py)   -> paquete NAMESPACE (solo si se reparte en varias distros)
```

Frente al [[01 __init__.py y Directorios | paquete regular]], el namespace cambia la condición de "un directorio, un `__init__.py`" por "varias rutas, ningún `__init__.py`". Su mecánica se apoya en cómo el importador recorre [[01 sys.path y PYTHONPATH | sys.path]], detallado en [[40 Sistema de Modulos de Python/index | Sistema de Módulos de Python]].
