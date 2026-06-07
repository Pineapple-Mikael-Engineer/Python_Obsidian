---
title: Registry Pattern
order: 71
tags:
  - python
  - teoria
  - patrones
draft: false
aliases:
  - Registro de componentes
  - Registry
  - Patrón Registro
---

# Registry Pattern

> [!definicion]
> El **Registry Pattern** mantiene un **registro central** —normalmente un `dict`— donde los componentes se **anotan a sí mismos** bajo una clave. Quien **usa** un componente lo busca por su clave en el registro, sin importar el módulo que lo **define**. Así, agregar una nueva implementación es **escribirla y registrarla**, nunca tocar el código que la consume.

```python
REGISTRO = {}                          # el registro central: una clave -> un componente

def registrar(nombre):                 # decorador-fabrica: recibe la clave
    def envoltura(func):
        REGISTRO[nombre] = func        # al definirse, el componente se anota solo
        return func                    # devuelve la funcion intacta
    return envoltura

@registrar("json")
def exportar_json(datos):
    return f"JSON: {datos}"

@registrar("csv")
def exportar_csv(datos):
    return f"CSV: {datos}"

REGISTRO["json"]({"a": 1})             # 'JSON: {'a': 1}'  -> se busca por clave
list(REGISTRO)                          # ['json', 'csv']
```

El decorador `@registrar("json")` se ejecuta **al importar el módulo**: en ese instante la función se inserta en `REGISTRO`. El consumidor solo necesita la clave (`"json"`), no el nombre de la función ni de dónde vino.

## El decorador que registra

> [!info]
> `@registrar(nombre)` es un **decorador parametrizado**: la llamada `registrar("json")` devuelve el decorador real (`envoltura`), que recibe la función y la anota antes de devolverla **sin modificarla**. El registro es un **efecto secundario** de definir el componente.

```python
def registrar(nombre):
    def envoltura(func):
        if nombre in REGISTRO:
            raise ValueError(f"Clave duplicada: {nombre!r}")   # evita pisar registros
        REGISTRO[nombre] = func
        return func
    return envoltura
```

Validar la clave en el momento del registro convierte un error silencioso (un componente que sobrescribe a otro) en un fallo ruidoso al importar. La función devuelta es la original: el decorador **no envuelve** el comportamiento, solo lo cataloga.

## Registro de clases

> [!ejemplo]
> El mismo decorador sirve para **clases**: cada subclase se anota bajo su clave y el núcleo instancia por nombre. Es la base de un *factory* dirigido por datos, donde la configuración elige la clase sin un `if/elif` por cada tipo.

```python
HANDLERS = {}

def handler(tipo):
    def envoltura(cls):
        HANDLERS[tipo] = cls
        return cls
    return envoltura

@handler("email")
class NotificadorEmail:
    def enviar(self, msg): return f"Email: {msg}"

@handler("sms")
class NotificadorSMS:
    def enviar(self, msg): return f"SMS: {msg}"

def notificar(tipo, msg):
    return HANDLERS[tipo]().enviar(msg)     # se elige la clase por la clave

notificar("sms", "hola")                     # 'SMS: hola'
```

Añadir un canal nuevo es definir una clase con su `@handler(...)`; `notificar` no cambia. El `if/elif` que crecería con cada tipo se sustituye por una **búsqueda en el registro**.

## Por qué desacopla

> [!regla]
> El registro invierte la dependencia: en vez de que el núcleo **importe** cada componente (y crezca con cada uno), los componentes **importan el registro** y se anotan. El núcleo solo depende del `dict`, no de las piezas. El único requisito es que **el módulo del componente llegue a importarse** para que su decorador corra —de eso se ocupa la [[72 Plugin Architecture | Plugin Architecture]].

```python
# nucleo.py  -> NO conoce a ningun exportador concreto
from registro import REGISTRO
def exportar(formato, datos):
    return REGISTRO[formato](datos)

# exportadores.py  -> dependen del registro, se anotan al importarse
@registrar("xml")
def exportar_xml(datos): ...
```

El registro vive entre el productor y el consumidor como un **punto de encuentro**. Esa anotación al importar conecta con la idea del módulo como [[Tema 02 Programación Orientada a Objetos/80 Patrones de Diseño/81 Singleton | Singleton]] —el `dict` se crea una sola vez y queda cacheado en `sys.modules`— y se completa en la [[73 Module Factory | Module Factory]], que importa por nombre la implementación concreta.
</content>
