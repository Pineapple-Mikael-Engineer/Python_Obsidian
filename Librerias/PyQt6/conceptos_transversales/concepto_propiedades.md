---
title: el sistema de propiedades de Qt — getter/setter, property() y pyqtProperty
aliases: [propiedades, properties, pyqtProperty, property setProperty]
tags: [pyqt6, concepto, core]
lib: pyqt6
mod: QtCore
tipo: concepto
requiere: [concepto_qobject_arbol]
draft: false
---

# el sistema de propiedades de Qt — getter/setter, property() y pyqtProperty

Cada [[QObject]] y cada widget expone su estado como **propiedades** (`text`, `enabled`, `geometry`, `visible`, `toolTip`...). A diferencia de un atributo Python normal, en Qt una propiedad NO se lee como atributo (`w.text` no devuelve el texto): se accede con un **getter/setter** (`w.text()`, `w.setText("hola")`) o por nombre con `w.property("text")` / `w.setProperty("text", ...)`. Cada propiedad esta registrada en el **meta-objeto** de Qt, y eso es lo que permite estilarla por QSS, animarla y editarla en Qt Designer.

## Por que existe

Un atributo Python suelto solo sirve para guardar un valor. Una propiedad Qt, al estar registrada en el meta-objeto, habilita tres cosas que un atributo normal no puede:

- **QSS (hojas de estilo)**: puedes estilar por propiedad o estado (`QPushButton:disabled { ... }`, `[flat="true"]`).
- **Animaciones**: [[QPropertyAnimation]] anima una propiedad por su nombre a lo largo del tiempo.
- **Herramientas**: Qt Designer lista y edita las propiedades de cada widget.

Por eso el estado de los widgets se modela como propiedades y no como atributos sueltos: es el enganche con todo el resto del framework.

## Como funciona

Una propiedad existente se lee y escribe de dos formas equivalentes: con su getter/setter tipado, o por nombre con `property()` / `setProperty()`.

```python
from PyQt6.QtWidgets import QApplication, QPushButton
import sys

app = QApplication(sys.argv)
boton = QPushButton("Pulsame")

# 1) getter / setter tipados (lo habitual)
print(boton.text())            # "Pulsame"   -> OJO: con parentesis
boton.setText("Aceptar")       # escribir
boton.setEnabled(False)

# 2) por nombre, con property() / setProperty()
print(boton.property("text"))      # "Aceptar"
boton.setProperty("enabled", True)
```

El acceso por nombre es util para codigo generico o para QSS: `setProperty("clase", "peligro")` crea una propiedad dinamica que luego un selector `[clase="peligro"]` puede estilar.

## Atributo Python vs propiedad Qt

Son dos mundos distintos que conviven en el mismo objeto:

| | Atributo Python | Propiedad Qt |
|---|---|---|
| Lectura | `obj.x` | `obj.x()` o `obj.property("x")` |
| Escritura | `obj.x = 5` | `obj.setX(5)` o `obj.setProperty("x", 5)` |
| Vive en | el `__dict__` del objeto | el meta-objeto de Qt |
| QSS / animacion / Designer | no | si |

Puedes ponerle atributos Python normales a un widget (`w.mi_dato = 3`), pero esos no se pueden animar ni estilar: son tuyos, no de Qt.

## Definir una propiedad propia con pyqtProperty

[[pyqtProperty]] declara una propiedad Qt PROPIA en una **subclase de `QObject`**. Es como el `@property` de Python, pero ademas la registra en el meta-objeto, asi que esa propiedad ya se puede animar con `QPropertyAnimation` o estilar por QSS:

```python
from PyQt6.QtCore import QObject, pyqtProperty

class Barra(QObject):
    def __init__(self):
        super().__init__()
        self._nivel = 0

    @pyqtProperty(int)            # getter -> registra la propiedad "nivel" (int)
    def nivel(self):
        return self._nivel

    @nivel.setter
    def nivel(self, valor):       # setter
        self._nivel = valor

b = Barra()
b.nivel = 80                      # usa el setter
print(b.property("nivel"))        # 80  -> ya es una propiedad Qt de pleno derecho
```

## Animar una propiedad

Como `nivel` esta registrada en el meta-objeto, [[QPropertyAnimation]] puede interpolarla por su nombre (en bytes):

```python
from PyQt6.QtCore import QPropertyAnimation

anim = QPropertyAnimation(b, b"nivel")   # objeto + nombre de la propiedad
anim.setDuration(1000)                    # 1 s
anim.setStartValue(0)
anim.setEndValue(100)
anim.start()
```

El mismo patron sirve para propiedades nativas: `QPropertyAnimation(widget, b"geometry")`, `b"windowOpacity"`, etc.

## Propiedades comunes de un widget

| Propiedad | Getter / setter | Controla |
|---|---|---|
| `text` | `text()` \| `setText(str)` | el texto mostrado |
| `enabled` | `isEnabled()` \| `setEnabled(bool)` | si responde a la interaccion |
| `visible` | `isVisible()` \| `setVisible(bool)` | si se muestra en pantalla |
| `geometry` | `geometry()` \| `setGeometry(QRect)` | posicion y tamano |
| `toolTip` | `toolTip()` \| `setToolTip(str)` | el texto de ayuda al pasar el raton |
| `styleSheet` | `styleSheet()` \| `setStyleSheet(str)` | el QSS aplicado al widget |

## Errores comunes

| Error | Causa | Solucion |
|-------|-------|----------|
| `w.text` devuelve un metodo, no el texto | leiste la propiedad como atributo Python | usa el getter: `w.text()` con parentesis |
| `boton.text = "x"` no cambia nada | asignaste un atributo Python, no la propiedad Qt | usa el setter: `boton.setText("x")` |
| `pyqtProperty` no se anima ni se estila | la declaraste fuera de una subclase de `QObject` | define la clase heredando de `QObject` |
| `QPropertyAnimation` no mueve nada | pasaste el nombre como `str` y no como `bytes` | usa `b"nombre"` (bytes), no `"nombre"` |

## Notas relacionadas

- [[concepto_qobject_arbol]] — el meta-objeto donde se registran las propiedades
- [[pyqtProperty]] — declarar una propiedad Qt propia en una subclase
- [[QPropertyAnimation]] — animar una propiedad por su nombre
