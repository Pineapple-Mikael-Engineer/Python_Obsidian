---
title: Plugin Architecture
order: 72
tags:
  - python
  - teoria
  - patrones
draft: false
aliases:
  - Arquitectura de plugins
  - Sistema de plugins
  - Plugins
---

# Plugin Architecture

> [!definicion]
> Una **arquitectura de plugins** permite **extender un sistema sin modificar su núcleo**: las capacidades nuevas se entregan como **módulos independientes** (*plugins*) que el núcleo **descubre y carga en tiempo de ejecución**. El núcleo define un **contrato** (una interfaz) y un **mecanismo de descubrimiento**; no conoce los plugins concretos, solo que cumplen el contrato.

```python
# plugins/saludo.py  -> un plugin: modulo suelto que cumple el contrato
def registrar(app):
    app.comando("saludo", lambda: "¡Hola!")

# el nucleo descubre la carpeta y llama a registrar(...) de cada plugin
```

El núcleo nunca escribe `import plugins.saludo`. Coloca un *gancho* (`registrar(app)`) y deja que **cada plugin se enchufe** cuando es descubierto. Agregar una función es soltar un archivo en la carpeta de plugins.

## Descubrimiento por convención de carpeta

> [!info]
> La vía más directa: una **carpeta de plugins** donde cada `.py` es un plugin. El núcleo lista la carpeta, importa cada módulo con `importlib.import_module` y llama a su gancho `registrar`. La **convención** (carpeta + función `registrar`) reemplaza a la configuración explícita.

```python
import importlib
import pkgutil
import plugins                          # el paquete-carpeta de plugins

class App:
    def __init__(self):
        self.comandos = {}
    def comando(self, nombre, func):
        self.comandos[nombre] = func

def cargar_plugins(app):
    # pkgutil recorre los modulos del paquete plugins/
    for info in pkgutil.iter_modules(plugins.__path__, "plugins."):
        modulo = importlib.import_module(info.name)   # importa el .py descubierto
        if hasattr(modulo, "registrar"):
            modulo.registrar(app)                     # lo enchufa al nucleo

app = App()
cargar_plugins(app)
app.comandos["saludo"]()                  # '¡Hola!'  -> capacidad aportada por el plugin
```

`pkgutil.iter_modules` recorre los módulos del paquete sin que el núcleo los nombre; `import_module` los carga por su cadena. Solo se exige que cada plugin exponga `registrar` —el resto de su implementación es asunto suyo.

## Descubrimiento por entry points

> [!ejemplo]
> Para plugins **distribuidos como paquetes instalables**, los *entry points* del empaquetado permiten que un plugin se anuncie **sin estar en una carpeta concreta**. El núcleo consulta el grupo de entry points y carga cada uno; los plugins pueden venir de cualquier paquete instalado con `pip`.

```python
from importlib.metadata import entry_points

def cargar_extensiones(app, grupo="miapp.plugins"):
    for ep in entry_points(group=grupo):     # plugins anunciados por paquetes instalados
        registrar = ep.load()                # importa y resuelve el objeto del entry point
        registrar(app)

# En el pyproject.toml del plugin:
# [project.entry-points."miapp.plugins"]
# saludo = "mi_plugin.saludo:registrar"
```

Con *entry points* el núcleo no conoce ni la carpeta ni el nombre del módulo: descubre todo lo declarado bajo el grupo `"miapp.plugins"`. Es el mecanismo que usan ecosistemas como `pytest` o `flake8` para sus plugins de terceros.

## Núcleo ciego a los plugins

> [!regla]
> El valor del patrón está en que el núcleo permanezca **ciego**: depende del **contrato** y del **descubrimiento**, nunca de un plugin concreto. Si el núcleo necesitara `import` de un plugin específico, dejaría de ser extensible. Cargar código en tiempo de ejecución implica **confiar** en su origen: un plugin descubierto se ejecuta con todos los permisos del proceso.

```python
# nucleo.py  -> NO aparece ningun nombre de plugin
def arrancar():
    app = App()
    cargar_plugins(app)        # quien haya, se enchufa
    return app
```

El descubrimiento se apoya en `importlib` para convertir un **nombre** en un **módulo cargado**, igual que la [[73 Module Factory | Module Factory]]; y muchos plugins, una vez importados, se anuncian a través de un [[71 Registry Pattern | Registry]] central. Por debajo, todo es la maquinaria de [[40 Sistema de Modulos de Python/index | importación de Python]].
</content>
