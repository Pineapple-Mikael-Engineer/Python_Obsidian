---
title: Reloading (importlib.reload)
order: 3
tags:
  - python
  - teoria
  - sistema-modulos
draft: false
aliases:
  - importlib.reload
  - Recarga de módulos
  - Hot reload
---

# Reloading (importlib.reload)

> [!definicion]
> **`importlib.reload(modulo)`** vuelve a **ejecutar el cuerpo** de un módulo ya importado **sobre el mismo objeto**, refrescando su contenido sin reiniciar el intérprete. Es la excepción deliberada a la regla de [[02 sys.modules (Cache) | sys.modules]] de que un módulo se carga una sola vez: recarga "en caliente" tras editar su archivo.

```python
import importlib
import config

# (editas config.py y cambias VALOR = 42 -> VALOR = 99)
importlib.reload(config)     # re-ejecuta config.py
config.VALOR                 # 99  -> refleja el cambio sin reiniciar
```

`reload` requiere el **objeto módulo** ya importado, no su nombre como cadena. Es la tercera pieza del [[42 Mecanismos de Importacion/index | mecanismo de importación]]: opera *contra* la caché, reutilizando su entrada en lugar de crear una nueva.

## Recarga sobre el mismo objeto

> [!regla]
> `reload` **conserva la identidad** del módulo: devuelve y actualiza el **mismo objeto** que ya estaba en `sys.modules`. Por eso es superior a `del sys.modules[...]` + `import`: las referencias previas (`import config` hechos antes) ven los cambios, porque apuntan al objeto recargado.

```python
import importlib, config, sys

m = importlib.reload(config)
m is config                          # True  -> mismo objeto
config is sys.modules['config']      # True  -> sigue siendo la entrada de caché
```

## Limitaciones

> [!info]
> La recarga es **superficial**: solo re-ejecuta el módulo indicado, no sus dependencias importadas. Además, los nombres traídos con `from M import x` **no se actualizan** (siguen apuntando al valor viejo), y las **instancias ya creadas** de clases del módulo conservan la clase antigua. Tampoco elimina nombres borrados del archivo: solo añade o reasigna.

```python
from config import VALOR        # copia el valor actual en este namespace
import importlib, config
importlib.reload(config)        # actualiza config.VALOR...
VALOR                           # ...pero ESTE VALOR sigue siendo el viejo
config.VALOR                    # el nuevo -> hay que acceder vía el módulo
```

## Cuándo se usa

> [!regla]
> `reload` es una herramienta de **desarrollo interactivo**: en el **REPL**, Jupyter o sesiones largas, para probar cambios de un módulo sin perder el estado de la sesión. **No** se usa en producción: el flujo normal de un programa es importar una vez; ahí reiniciar el proceso es más simple y seguro.

```python
# Sesión interactiva: iterar sobre un módulo en desarrollo
import importlib
import mi_modulo
# ... editas mi_modulo.py ...
importlib.reload(mi_modulo)     # pruebas los cambios sin salir del REPL
```

Con esto se cierra la maquinaria de importación: `sys.path` localiza, `sys.modules` cachea y `reload` refresca esa caché. Todo ello sostiene la [[41 Jerarquia de Modulos/index | jerarquía de módulos]] y, por encima, las formas de [[20 Modulos en Python/22 Importacion de Modulos/index | importación]] que usa el día a día.
