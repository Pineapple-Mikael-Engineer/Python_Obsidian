---
title: Module Factory
order: 73
tags:
  - python
  - teoria
  - patrones
draft: false
aliases:
  - Fábrica de módulos
  - Importación dinámica
  - Module Factory
---

# Module Factory

> [!definicion]
> Una **Module Factory** **selecciona e importa un módulo por su nombre en tiempo de ejecución** con `importlib.import_module`, en lugar de fijarlo con un `import` estático. El **nombre** del módulo llega como dato —de la configuración, una variable o la entrada del usuario— y la fábrica devuelve la **implementación adecuada** ya cargada. Cambiar de implementación es cambiar una cadena, no el código.

```python
import importlib

def crear_backend(nombre):
    # convierte una cadena en un modulo importado
    modulo = importlib.import_module(f"backends.{nombre}")
    return modulo.Backend()                    # contrato: cada backend expone Backend

# config dice "postgres" -> se importa backends.postgres en este instante
db = crear_backend("postgres")
db.conectar()
```

`import_module("backends.postgres")` hace en tiempo de ejecución lo mismo que `import backends.postgres` en tiempo de escritura, pero a partir de una **cadena**. La fábrica no menciona ningún backend concreto: recibe el nombre y devuelve la pieza.

## importlib.import_module

> [!info]
> `importlib.import_module(nombre)` importa el módulo por su **ruta punteada** (`"paquete.modulo"`) y devuelve el **objeto módulo**, cacheándolo en `sys.modules` como cualquier `import`. A diferencia de la función `__import__`, devuelve directamente el submódulo solicitado, lo que la hace la herramienta idiomática para importación dinámica.

```python
import importlib

mod = importlib.import_module("json")        # equivalente dinamico de: import json
mod.dumps({"a": 1})                          # '{"a": 1}'

# segunda llamada: NO reimporta, lo toma de sys.modules
import sys
"json" in sys.modules                        # True
```

Como reutiliza la caché de módulos, importar dos veces el mismo nombre no vuelve a ejecutar el archivo: la fábrica paga el coste de carga **una sola vez** por módulo.

## Fábrica dirigida por configuración

> [!ejemplo]
> El caso típico: la **configuración** (un `dict`, un `.toml`, una variable de entorno) nombra la implementación, y la fábrica la materializa. Un `try/except ImportError` traduce un nombre inexistente en un error claro de configuración.

```python
import importlib

CONFIG = {"serializador": "yaml"}            # podria venir de un archivo o del entorno

def crear_serializador(config):
    nombre = config["serializador"]
    try:
        modulo = importlib.import_module(f"serializadores.{nombre}")
    except ImportError as e:
        raise ValueError(f"Serializador desconocido: {nombre!r}") from e
    return modulo.crear()                     # contrato comun: cada modulo expone crear()

ser = crear_serializador(CONFIG)              # carga serializadores.yaml
```

Para añadir un serializador `toml` basta crear `serializadores/toml.py` con su `crear()` y poner `"toml"` en la configuración: la fábrica no se toca. Aquí no hay `if/elif` por implementación —el nombre **es** la selección.

## Selección de atributo dentro del módulo

> [!regla]
> A veces se necesita no el módulo entero sino **un objeto dentro de él** (una clase, una función). El idioma es `import_module` para cargar el módulo y `getattr` para extraer el atributo, partiendo una ruta `"paquete.modulo:Clase"` en sus dos mitades. El módulo de destino debe ser **de confianza**: importarlo **ejecuta su código** al nivel superior.

```python
import importlib

def resolver(ruta):
    # "paquete.modulo:objeto" -> el objeto ya cargado
    nombre_mod, _, atributo = ruta.partition(":")
    modulo = importlib.import_module(nombre_mod)
    return getattr(modulo, atributo)

Decimal = resolver("decimal:Decimal")
Decimal("1.5")                                # Decimal('1.5')
```

Este patrón es el que sostiene a los [[72 Plugin Architecture | plugins]] (convertir un nombre anunciado en código cargado) y complementa al [[71 Registry Pattern | Registry]]: el registro elige **dentro** de lo ya importado, mientras la fábrica **importa** la pieza por su nombre. Todo descansa sobre el [[40 Sistema de Modulos de Python/index | sistema de módulos]] y su caché en `sys.modules`.
</content>
