---
title: Observer
order: 84
tags:
  - python
  - teoria
  - patrones
draft: false
aliases:
  - Observador
  - Publicar/Suscribir
  - Pub/Sub
---

# Observer

> [!definicion]
> En el **Observer** un objeto **sujeto** (*observable*) mantiene una lista de **observadores** y los **notifica automáticamente** cada vez que cambia su estado. Establece una relación **uno-a-muchos** de tipo *publicar/suscribir*: el sujeto publica cambios sin conocer los detalles de quién reacciona.

```python
class Temperatura:                                  # sujeto
    def __init__(self):
        self._observadores = []
        self._valor = 0

    def suscribir(self, obs):
        self._observadores.append(obs)

    def notificar(self):
        for obs in self._observadores:
            obs.actualizar(self._valor)             # interfaz común: actualizar

    @property
    def valor(self): return self._valor
    @valor.setter
    def valor(self, v):
        self._valor = v
        self.notificar()                            # cambio de estado -> avisa
```

## Observadores por duck typing

> [!regla]
> El sujeto solo exige que cada observador exponga un método `actualizar` (el nombre acordado). Gracias al [[41 Duck Typing]] **no hace falta una clase base común**: cualquier objeto con ese método sirve como observador.

```python
class DisplayDigital:
    def actualizar(self, t): print(f"[Digital] {t} C")

class Registro:
    def __init__(self): self.historial = []
    def actualizar(self, t): self.historial.append(t)

sensor = Temperatura()
sensor.suscribir(DisplayDigital())
log = Registro(); sensor.suscribir(log)

sensor.valor = 21                                   # [Digital] 21 C
sensor.valor = 23                                   # [Digital] 23 C
log.historial                                       # [21, 23]
```

Al asignar `sensor.valor`, el *setter* dispara `notificar`, que recorre la lista y llama `actualizar` en cada display. El sujeto **ignora** cuántos observadores hay y qué hacen: solo difunde.

## Desuscribir y desacoplamiento

> [!info]
> Para un ciclo de vida completo se añade `desuscribir`, que retira un observador de la lista. La fortaleza del patrón es el **desacoplamiento**: sujeto y observadores evolucionan por separado, y se pueden registrar o quitar dinámicamente sin modificar al otro.

```python
    def desuscribir(self, obs):
        self._observadores.remove(obs)
```

> [!warning]
> Mantener referencias a los observadores en `self._observadores` **impide que se recolecten** por el GC mientras el sujeto viva. Si los observadores tienen vida más corta, conviene desuscribirlos explícitamente o guardarlos con referencias débiles (`weakref`) para evitar fugas de memoria.

El Observer es la base de la **programación dirigida por eventos** (GUIs, sistemas reactivos, *event buses*): los manejadores de eventos son observadores suscritos a las señales que emite un componente.
