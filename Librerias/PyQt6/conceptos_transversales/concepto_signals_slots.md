---
title: senales y slots — el mecanismo de comunicacion de Qt
aliases: [signals slots, senales y slots, connect, pyqtSignal]
tags: [pyqt6, concepto, core]
lib: pyqt6
mod: QtCore
tipo: concepto
requiere: [concepto_qobject_arbol]
draft: false
---

# senales y slots — el mecanismo de comunicacion de Qt

Una **senal** es un aviso que un objeto emite cuando le pasa algo (un boton fue pulsado, un slider cambio de valor). Un **slot** es cualquier funcion o metodo que responde a esa senal. El metodo `.connect()` une ambos: cuando la senal se emite, el slot se ejecuta. Es el sistema nervioso de Qt y la razon por la que casi todo hereda de `QObject` (solo los `QObject` pueden tener senales). Su virtud es el **desacoplamiento**: el que emite no sabe ni le importa quien escucha.

## Por que existe

Sin senales, tendrias que sondear el estado o cablear callbacks a mano, acoplando cada widget a su reaccion. Con senales, el `QPushButton` solo anuncia "me pulsaron" (`clicked`) y cualquiera puede suscribirse sin que el boton lo sepa.

```python
# Sin senales (acoplado, tedioso): el boton tendria que conocer la funcion destino.
# Con senales (desacoplado): el boton solo emite; tu decides quien escucha.
boton.clicked.connect(self.guardar)     # un escuchador
boton.clicked.connect(self.cerrar)      # otro mas; el boton ni se entera
```

## Conectar una senal a un slot

```python
from PyQt6.QtWidgets import QApplication, QPushButton, QSlider
import sys

app = QApplication(sys.argv)

boton = QPushButton("Pulsame")
boton.clicked.connect(lambda: print("clic"))     # slot sin datos

slider = QSlider()
slider.valueChanged.connect(print)               # la senal LLEVA datos: el valor nuevo
slider.valueChanged.connect(lambda v: print(f"valor = {v}"))
```

La senal `clicked` no envia datos; `valueChanged` envia un `int` (el valor). El slot recibe exactamente los argumentos que la senal emite.

```mermaid
flowchart LR
    E["objeto emisor (QPushButton)"] -->|"al pulsarse"| S(["senal: clicked"])
    S -->|".connect(slot)"| SL(["slot: tu funcion / metodo"])
    SL --> R["se ejecuta la respuesta"]

    classDef base fill:#5e81ac,stroke:#88c0d0,stroke-width:2px,color:#eceff4;
    classDef grupo fill:#3b4252,stroke:#81a1c1,stroke-width:1.5px,color:#88c0d0;
    classDef hoja fill:#2e3440,stroke:#a3be8c,color:#d8dee9;
    class E,R grupo;
    class S,SL hoja;
```

## Definir una senal propia

Las senales propias se declaran con [[pyqtSignal]] como **atributo de clase** (no en `__init__`) y se disparan con `.emit()`:

```python
from PyQt6.QtCore import QObject, pyqtSignal

class Termometro(QObject):
    temperatura_cambiada = pyqtSignal(float)     # senal que lleva un float

    def medir(self, t):
        self.temperatura_cambiada.emit(t)        # emitir -> dispara los slots conectados

sensor = Termometro()
sensor.temperatura_cambiada.connect(lambda t: print(f"{t} C"))
sensor.medir(36.5)        # imprime "36.5 C"
```

## `@pyqtSlot`: marcar slots de forma explicita

Cualquier funcion Python sirve de slot, pero decorar el metodo con [[pyqtSlot]] declara los **tipos** que acepta (permite sobrecarga y es mas eficiente):

```python
from PyQt6.QtCore import QObject, pyqtSlot

class Panel(QObject):
    @pyqtSlot(int)            # este slot acepta un int
    def actualizar(self, valor):
        ...
```

## Errores comunes

| Error | Causa | Solucion |
|-------|-------|----------|
| `boton.clicked.connect(self.f())` no funciona | conectaste el **resultado** de llamar a `f`, no la funcion | quita los parentesis: `connect(self.f)` |
| La senal propia no dispara nada | la declaraste en `__init__` en vez de como atributo de clase | declarala a nivel de clase: `mi_senal = pyqtSignal(...)` |
| `TypeError` al emitir | los tipos de `emit(...)` no coinciden con `pyqtSignal(...)` | usa los mismos tipos en la declaracion y en `emit` |
| El slot recibe argumentos de mas | la senal lleva datos y tu slot no los espera | acepta el argumento o usa un `lambda` que lo ignore |

## Notas relacionadas

- [[concepto_qobject_arbol]] — solo los `QObject` pueden tener senales
- [[pyqtSignal]] — declarar una senal propia
- [[pyqtSlot]] — marcar un metodo como slot con sus tipos
