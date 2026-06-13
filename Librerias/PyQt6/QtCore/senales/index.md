---
title: QtCore/señales — declarar, conectar y emitir señales
tags: [pyqt6, indice]
draft: false
---

# QtCore/señales — declarar, conectar y emitir señales

Esta carpeta reune las **herramientas concretas** del mecanismo que explica [[concepto_signals_slots]]: las piezas de API que usas cada dia para que dos `QObject` se comuniquen. Son cuatro y forman un ciclo: **declarar** una señal propia (`pyqtSignal`), **conectar** esa señal a un slot (`connect`), **decorar** el slot con sus tipos (`@pyqtSlot`) y **disparar** la señal (`emit`). El concepto te dice por que existen las señales; estas notas te dicen como escribirlas.

## En accion

Las cuatro piezas en una sola clase: una subclase de `QObject` con una señal propia, un slot decorado, la conexion y la emision.

```python
from PyQt6.QtCore import QObject, pyqtSignal, pyqtSlot

class Sensor(QObject):
    medido = pyqtSignal(float)            # 1. declarar la señal (atributo de clase)

    def medir(self, t):
        self.medido.emit(t)              # 4. emitir -> dispara los slots conectados

class Panel(QObject):
    @pyqtSlot(float)                      # 3. decorar el slot con sus tipos
    def mostrar(self, t):
        print(f"temperatura = {t} C")

sensor = Sensor()
panel = Panel()
sensor.medido.connect(panel.mostrar)     # 2. conectar la señal al slot

sensor.medir(36.5)                        # imprime "temperatura = 36.5 C"
```

## El ciclo

`pyqtSignal` declara, `connect` enlaza, `emit` dispara y el slot (marcado con `@pyqtSlot`) corre:

```mermaid
flowchart LR
    D(["pyqtSignal (declarar)"]) -->|"se conecta con"| C(["connect (conectar a un slot)"])
    C -->|"queda a la espera"| E(["emit (disparar)"])
    E -->|"ejecuta"| S["slot se ejecuta"]
    P(["@pyqtSlot"]) -.->|"decora con tipos"| S

    classDef base fill:#5e81ac,stroke:#88c0d0,stroke-width:2px,color:#eceff4;
    classDef grupo fill:#3b4252,stroke:#81a1c1,stroke-width:1.5px,color:#88c0d0;
    classDef hoja fill:#2e3440,stroke:#a3be8c,color:#d8dee9;
    class S grupo;
    class D,C,E,P hoja;
```

## Las piezas

| Pieza | Para que |
|-------|----------|
| [[pyqtSignal]] | declarar una señal propia como atributo de clase |
| [[connect]] | conectar una señal a un slot |
| [[emit]] | disparar la señal y ejecutar los slots conectados |
| [[pyqtSlot]] | decorar el slot con los tipos que acepta |

## Notas relacionadas

- [[concepto_signals_slots]] — por que existen las señales y slots; el modelo mental
- [[QObject]] — solo los `QObject` pueden declarar y emitir señales
