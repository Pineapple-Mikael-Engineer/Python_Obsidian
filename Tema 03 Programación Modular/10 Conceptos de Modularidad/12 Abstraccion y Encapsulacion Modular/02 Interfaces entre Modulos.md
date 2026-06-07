---
title: Interfaces entre Módulos
order: 2
tags:
  - python
  - teoria
  - modularidad
draft: false
aliases:
  - Interfaces entre Módulos
  - Module Interfaces
  - Contrato entre módulos
---

# Interfaces entre Módulos

> [!definicion]
> La **interfaz** de un módulo es el **contrato** que ofrece al exterior: el conjunto de funciones, clases y constantes **públicas**, con sus nombres, parámetros y comportamiento esperado. Es la **API** del módulo. Un buen diseño modular hace que los módulos dependan **unos de las interfaces de otros**, nunca de sus detalles internos.

```python
# almacen.py  -> su INTERFAZ son estas tres funciones publicas
def guardar(clave, valor): ...
def obtener(clave):        ...
def borrar(clave):         ...

# pedidos.py  -> depende SOLO de esa interfaz
import almacen
almacen.guardar("p1", {"total": 30})
almacen.obtener("p1")              # {"total": 30}
```

## Depender de la interfaz, no de la implementación

> [!regla]
> Un módulo consumidor debe apoyarse únicamente en lo que la interfaz **promete**, no en cómo está hecho por dentro. Si `almacen` guarda en un `dict`, en un archivo o en una base de datos es **irrelevante** para `pedidos`: mientras `guardar`/`obtener`/`borrar` se comporten igual, todo sigue funcionando.

```python
import almacen
almacen.obtener("p1")              # CORRECTO: usa la interfaz

import almacen
almacen._datos["p1"]               # INCORRECTO: depende de un detalle interno
                                   # (que sea un dict llamado _datos)
```

## Una interfaz estable es una promesa

> [!info]
> Cambiar una interfaz **rompe** a todos sus consumidores: renombrar una función pública, alterar el orden de los parámetros o el tipo de retorno obliga a tocar cada sitio que la usaba. Por eso la interfaz se diseña para ser **estable**: se puede **añadir** sin romper, pero **quitar o cambiar** lo existente es un cambio incompatible.

```python
# v1
def obtener(clave): ...
# v2 compatible -> AÑADE un parametro opcional, no rompe a nadie
def obtener(clave, por_defecto=None): ...
# v2 incompatible -> CAMBIA el orden/nombre: rompe a todos los consumidores
def obtener(default, key): ...
```

## La interfaz como frontera de acoplamiento

> [!info]
> La interfaz es la **superficie de contacto** entre dos módulos. Cuanto **más estrecha** (menos funciones, parámetros simples), **menor el acoplamiento** y más fácil sustituir o probar cada módulo de forma aislada. Una interfaz amplia y cambiante es la marca de un sistema muy acoplado.

```python
# Interfaz estrecha y clara -> bajo acoplamiento, facil de simular en tests
import almacen
def test_pedido(fake_almacen=almacen):
    fake_almacen.guardar("x", 1)
    assert fake_almacen.obtener("x") == 1
```

## Interfaces implícitas y explícitas

> [!warning]
> Por defecto la interfaz es **implícita**: "todo lo que no empieza por `_`". Esto es frágil, porque cualquier nombre público suelto pasa a formar parte del contrato sin querer. La forma **explícita** de declararla —enumerar la API en `__all__`— se trata en [[60 Diseno de APIs Modulares/index | Diseño de APIs Modulares]].

Qué se decide ocultar para que la interfaz quede limpia es el tema de [[01 Ocultamiento de Implementacion | Ocultamiento de Implementación]]. Depender de interfaces estables y no de detalles internos es la receta directa contra el alto acoplamiento descrito en [[11 Que es un Modulo/03 Cohesion y Acoplamiento | Cohesión y Acoplamiento]].
