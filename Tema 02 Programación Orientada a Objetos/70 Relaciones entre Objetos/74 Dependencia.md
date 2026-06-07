---
title: Dependencia
order: 74
tags:
  - python
  - teoria
  - relaciones
draft: false
aliases:
  - Dependencia
  - Dependency
  - Depende de
---

# Dependencia

> [!definicion]
> La **dependencia** es la relación **más débil** entre objetos: una clase **usa** a otra de forma **puntual y transitoria** durante una operación, **sin guardarla como atributo**. El objeto usado entra por **parámetro**, se **crea localmente** dentro de un método o se **obtiene como retorno**, y deja de existir (o de ser visible) cuando la operación termina. Semánticamente, una clase **"depende de"** otra.

```python
class Servicio:
    def generar_reporte(self, logger):       # logger llega como parámetro
        logger.info("inicio")                # se usa solo aquí
        datos = self._procesar()
        logger.info("fin")
        return datos                         # logger no se guarda en self

# Servicio depende de logger, pero no lo posee: no hay self.logger
```

`Servicio` no contiene un `logger`: lo recibe, lo usa y lo olvida. No hay relación de contención ni de ciclo de vida; solo un **uso momentáneo**.

## Las tres formas de aparición

> [!info]
> La dependencia se reconoce porque el objeto usado **no vive en `self`**. Aparece de tres maneras:
> - **Por parámetro** — el objeto llega en la firma del método (la forma canónica).
> - **Creación local** — se instancia dentro del método y muere al volver.
> - **Por retorno** — un método ajeno devuelve el objeto, que se usa en el acto.

```python
class Factura:
    def total_con_iva(self, calculadora):    # 1) parámetro
        return calculadora.aplicar(self.base)

    def exportar(self):
        buffer = Formateador()               # 2) creación local
        return buffer.render(self.lineas)    # buffer muere aquí

    def resumen(self, repo):
        cliente = repo.buscar(self.id)       # 3) retorno
        return cliente.nombre                # cliente se usa al instante
```

## Posición en el espectro de acoplamiento

> [!info]
> La dependencia ocupa el **extremo débil** del espectro de [[70 Relaciones entre Objetos/index | relaciones entre objetos]]. Frente a la [[71 Composicion | composición]] (la parte vive y muere con el todo) o la [[73 Asociacion | asociación]] (referencia persistente entre objetos), aquí **no hay vínculo permanente**: el objeto usado ni se almacena ni perdura.

| Relación | Vínculo | Persistencia |
| -------- | ------- | ------------ |
| Composición | "tiene un" exclusivo | Atributo, ciclo de vida ligado |
| Asociación | "usa un" | Atributo o referencia persistente |
| **Dependencia** | **"depende de"** | **Ninguna: solo durante la llamada** |

## Por qué importa: la fragilidad

> [!warning]
> Aunque sea la relación más débil, **no es inocua**: si cambia la **interfaz** de la clase usada (renombrar un método, alterar una firma), la clase dependiente **se rompe**. El acoplamiento es bajo pero **real**. Por eso conviene depender de **abstracciones estables** (una interfaz, un protocolo) y no de detalles internos.

## Inyección de dependencias

> [!regla]
> Pasar el objeto usado **desde fuera** (por parámetro o constructor) en lugar de **crearlo dentro** se llama **inyección de dependencias**. Reduce el acoplamiento, permite **sustituir** la dependencia (p. ej. un `logger` real por uno falso en tests) y deja explícito qué necesita cada operación.

```python
class Servicio:
    def __init__(self, logger):       # dependencia inyectada, no creada
        self._logger = logger         # (aquí ya tiende a asociación)

def test_servicio():
    fake = LoggerFalso()              # se sustituye sin tocar Servicio
    Servicio(fake).generar_reporte(fake)
```

Cuando la dependencia se inyecta y **se almacena** en `self`, la relación deja de ser puntual y se desplaza hacia la [[73 Asociacion | asociación]]: la frontera entre ambas es el **almacenamiento**.
