---
title: connect — conectar una señal a un slot
aliases: [connect, disconnect, conectar señal]
tags: [pyqt6, api/metodo, core]
lib: pyqt6
mod: QtCore
tipo: metodo
requiere: [concepto_signals_slots]
draft: false
---

# connect — conectar una señal a un slot

`senal.connect(slot)` enlaza una **señal** con un **slot**: cuando la señal se emite, el slot se ejecuta recibiendo los argumentos que la señal lleve. El slot puede ser cualquier callable (una funcion, un metodo, un `lambda`) o incluso **otra señal**. Es la mitad receptora del mecanismo de [[concepto_signals_slots | senales y slots]]: `connect` registra al escuchador; quien emite no necesita saber quien escucha.

## Firma

```python
senal.connect(slot, type=Qt.ConnectionType.AutoConnection) -> Connection
```

- **`slot`**: el callable (o señal) a ejecutar cuando la señal se emita.
- **`type`**: el modo de entrega (ver abajo). Por defecto, `AutoConnection`.
- **Devuelve** una `Connection`: un handle que sirve para **desconectar** luego con precision.

## Como se usa

Se conecta **la señal**, no el resultado de llamarla. El slot va **sin parentesis**:

```python
boton.clicked.connect(self.guardar)        # correcto: pasa la funcion
boton.clicked.connect(self.guardar())      # MAL: pasa lo que devuelve guardar()
```

Si la señal lleva datos, el slot los recibe como argumentos. Para ignorarlos o reordenarlos, usa un `lambda`:

```python
slider.valueChanged.connect(print)               # imprime el valor (un int)
slider.valueChanged.connect(lambda v: print(f"valor = {v}"))
boton.clicked.connect(lambda: print("clic"))     # ignora el bool de clicked
```

## Tipos de conexion (`type=`)

| Tipo | Cuando usarlo |
|------|---------------|
| `Qt.ConnectionType.AutoConnection` | por defecto: **directa** si emisor y slot estan en el mismo hilo, **encolada** si estan en hilos distintos |
| `Qt.ConnectionType.DirectConnection` | el slot corre de inmediato, en el hilo del que emite |
| `Qt.ConnectionType.QueuedConnection` | el slot corre en el hilo del receptor, via su event loop (clave **entre hilos**, p. ej. con `QThread`) |

En la mayoria de casos de un solo hilo no toca el `type`: `AutoConnection` resuelve bien.

## Conexiones many-to-many

Una señal puede ir a **varios** slots, y un slot puede recibir de **varias** señales:

```python
boton.clicked.connect(self.guardar)      # un mismo clic dispara
boton.clicked.connect(self.cerrar)       # los dos slots, en orden de conexion

boton_a.clicked.connect(self.refrescar)  # un mismo slot atiende
boton_b.clicked.connect(self.refrescar)  # a dos botones
```

## Reenviar una señal a otra señal

Conectar una señal a **otra señal** la reenvia: emitir la primera emite la segunda. Util para "subir" eventos de un widget interno a su contenedor:

```python
self.boton.clicked.connect(self.solicitado)   # solicitado es una señal propia
# al pulsar el boton, se emite tambien self.solicitado
```

## Desconectar

```python
senal.disconnect(slot)     # quita esa conexion concreta
senal.disconnect()         # quita TODAS las conexiones de esa señal

con = senal.connect(slot)  # guardar el handle...
senal.disconnect(con)      # ...y desconectar por handle (preciso si hay lambdas)
```

## Casos de uso

App minima conectando señales con y sin datos:

```python
from PyQt6.QtWidgets import QApplication, QPushButton, QSlider, QVBoxLayout, QWidget
import sys

app = QApplication(sys.argv)
w = QWidget()
lay = QVBoxLayout(w)

boton = QPushButton("Pulsame")
slider = QSlider()
lay.addWidget(boton)
lay.addWidget(slider)

boton.clicked.connect(lambda: print("clic"))         # señal sin datos
slider.valueChanged.connect(lambda v: print(v))      # señal con un int
slider.valueChanged.connect(boton.setEnabled)        # encadenar a un metodo-slot

w.show()
sys.exit(app.exec())
```

Conexion entre hilos con `QueuedConnection`:

```python
from PyQt6.QtCore import Qt

# el worker emite desde otro hilo; el slot corre en el hilo de la GUI
worker.progreso.connect(self.barra.setValue,
                        type=Qt.ConnectionType.QueuedConnection)
```

## Errores comunes

| Error | Causa | Solucion |
|-------|-------|----------|
| El slot se ejecuta una sola vez al conectar | conectaste `slot()` **con parentesis**: se conecto el resultado | quita los parentesis: `connect(self.slot)` |
| `TypeError` al desconectar | desconectas un slot que no estaba conectado | desconecta solo lo conectado, o guarda el handle de `connect` |
| Un `lambda` no se puede desconectar luego | no guardaste referencia a ese lambda | guarda el `Connection` que devuelve `connect` y desconecta por handle |
| El slot recibe argumentos inesperados | la señal lleva datos y el slot no los espera | acepta el argumento o envuelve con un `lambda` que lo ignore |
| Entre hilos, el slot toca la GUI y rompe | usaste `DirectConnection` cruzando hilos | usa `QueuedConnection` (o `AutoConnection`) para entregar en el hilo del receptor |

## Notas relacionadas

- [[concepto_signals_slots]] — el mecanismo completo de señales y slots
- [[emit]] — disparar la señal que activa los slots conectados
- [[pyqtSignal]] — declarar la señal que se conecta
