---
title: pyqtProperty — decorador que define una propiedad Qt en una subclase de QObject
aliases:
  - pyqtProperty
  - "@pyqtProperty"
  - propiedad Qt
tags: [pyqt6, api/funcion, core]
lib: pyqt6
mod: QtCore
tipo: funcion
requiere: [concepto_propiedades]
draft: false
---

# pyqtProperty — decorador que define una propiedad Qt en una subclase de QObject

`@pyqtProperty` es un **decorador** que define una **propiedad Qt** propia en una subclase de `QObject`. Funciona como el `@property` de Python (getter/setter), pero ademas registra la propiedad en el **meta-objeto** de Qt. Ese registro es lo que la diferencia: una propiedad declarada con `@pyqtProperty` se puede **animar** con [[QPropertyAnimation]], **estilar** por QSS y **editar** en Qt Designer; una declarada con `@property` de Python no, porque Qt ni siquiera la conoce. Es la pieza de [[concepto_propiedades]] para crear estado propio integrado en el framework.

## Firma

```python
@pyqtProperty(type)              # sobre el getter; type = tipo de la propiedad
def nombre(self):
    return self._valor

@nombre.setter                   # sobre el setter (mismo nombre)
def nombre(self, valor):
    self._valor = valor
```

- `type`: el tipo de la propiedad (`int`, `float`, `str`, `bool`, una clase Qt...). Determina como la trata el meta-objeto.
- El **getter** decorado con `@pyqtProperty(type)` es lo que registra la propiedad; el **setter** se añade luego con `@<nombre>.setter`. Sin setter, la propiedad queda de solo lectura.

## Como se usa

Se define dentro de una subclase de `QObject` (un widget vale, ya hereda de [[QObject]]). El estado real se guarda en un atributo interno (`_nivel`) y la propiedad lo expone:

```python
from PyQt6.QtWidgets import QWidget
from PyQt6.QtCore import pyqtProperty

class Barra(QWidget):
    def __init__(self):
        super().__init__()
        self._nivel = 0

    @pyqtProperty(int)            # registra la propiedad "nivel" (int)
    def nivel(self):
        return self._nivel

    @nivel.setter
    def nivel(self, valor):
        self._nivel = valor
        self.update()             # repintar al cambiar el nivel

w = Barra()
w.nivel = 80                      # usa el setter
print(w.property("nivel"))        # 80 -> ya es una propiedad Qt de pleno derecho
```

## Casos de uso

- **Animar una propiedad propia**: como `nivel` esta en el meta-objeto, [[QPropertyAnimation]] puede interpolarla por su nombre (en bytes). Este es el motivo principal para usar `@pyqtProperty` en vez de `@property`.

```python
from PyQt6.QtCore import QPropertyAnimation

anim = QPropertyAnimation(w, b"nivel")   # objeto + nombre de la propiedad en bytes
anim.setDuration(1000)                    # 1 s
anim.setStartValue(0)
anim.setEndValue(100)
anim.start()                              # el setter de "nivel" se llama en cada frame
```

- **Estilar por QSS**: una propiedad registrada se puede usar en selectores de hoja de estilo.
- **Integrar con Qt Designer**: las propiedades de la clase aparecen y se editan en la herramienta.

## Diferencia con `@property` de Python

| | `@property` (Python) | `@pyqtProperty` (Qt) |
|---|---|---|
| Getter / setter | si | si |
| Vive en | el `__dict__` de la clase | el meta-objeto de Qt |
| Animable (`QPropertyAnimation`) | no | si |
| Estilable por QSS / visible en Designer | no | si |

Si solo quieres un getter/setter Python normal, `@property` basta. Si quieres animar o estilar, hace falta `@pyqtProperty`.

## Errores comunes

| Error | Causa | Solucion |
|-------|-------|----------|
| La propiedad no se anima ni se estila | la declaraste con `@property` de Python | usa `@pyqtProperty(type)`: Qt no conoce las `@property` normales |
| `@pyqtProperty` no funciona | la clase no hereda de `QObject` | declara la clase como subclase de `QObject` o de un widget |
| `QPropertyAnimation` no mueve nada | pasaste el nombre como `str` o no coincide con el de la propiedad | usa `b"nombre"` en bytes y que coincida con el getter (`b"nivel"` para `def nivel`) |
| El cambio no se ve en pantalla | el setter no repinta | llama a `self.update()` dentro del setter |

## Notas relacionadas

- [[concepto_propiedades]] — el sistema de propiedades de Qt donde encaja este decorador
- [[QPropertyAnimation]] — animar una propiedad por su nombre
- [[QObject]] — el meta-objeto donde se registra la propiedad
