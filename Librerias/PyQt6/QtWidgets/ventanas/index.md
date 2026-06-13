---
title: QtWidgets/ventanas — ventana principal y dialogos
tags: [pyqt6, indice]
draft: false
---

# QtWidgets/ventanas — ventana principal y dialogos

Esta carpeta agrupa las **ventanas de nivel superior**: las que aparecen como una ventana propia del sistema, sin un `parent` visual que las contenga. Son de dos clases. La **ventana principal** de la app es `QMainWindow`: trae de fabrica el armazon tipico de una aplicacion —barra de menus, barras de herramientas, barra de estado y un **widget central**—. Los **dialogos** son ventanas secundarias y suelen ser modales (bloquean el resto hasta que respondes): `QDialog` es el dialogo generico que construyes tu, y `QMessageBox`/`QFileDialog` son dialogos **predefinidos** para los dos casos mas comunes (mostrar un mensaje o pregunta, y elegir un archivo o carpeta). Todos son `QWidget`, asi que ya saben dibujarse, mostrarse con `show()` y recibir eventos; lo que añaden es la estructura propia de una ventana completa.

## En accion

```python
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel, QPushButton
)
import sys

app = QApplication(sys.argv)

ventana = QMainWindow()                       # la ventana principal de la app
ventana.setWindowTitle("ventanas en accion")

central = QWidget()                           # el widget central obligatorio
layout = QVBoxLayout(central)                 # un layout dentro del central
layout.addWidget(QLabel("Contenido de la ventana"))
layout.addWidget(QPushButton("Pulsame"))
ventana.setCentralWidget(central)             # se cuelga en el centro

menu = ventana.menuBar().addMenu("&Archivo")  # un menu basico
menu.addAction("Salir", ventana.close)

ventana.statusBar().showMessage("Listo")      # la barra de estado, abajo

ventana.show()
sys.exit(app.exec())                          # exec() (PyQt6, sin guion bajo) bloquea
```

## Herencia

```mermaid
classDiagram
    QObject <|-- QWidget
    QWidget <|-- QMainWindow
    QWidget <|-- QDialog
    QDialog <|-- QMessageBox
    QDialog <|-- QFileDialog
    class QObject { +parent +connect() }
    class QWidget { +show() +setLayout() +paintEvent() }
    class QMainWindow { +setCentralWidget() +menuBar() +statusBar() }
    class QDialog { +exec() +accept() +reject() }
    class QMessageBox { +question() +information() }
    class QFileDialog { +getOpenFileName() +getExistingDirectory() }
```

Todas las ventanas son una rama de `QWidget`: lo que no definen (dibujarse, `show()`, eventos) lo heredan de ahi. `QMainWindow` cuelga directo de `QWidget` y añade el armazon de la app. Los dialogos predefinidos `QMessageBox` y `QFileDialog` no cuelgan de `QWidget` directo: heredan de `QDialog`, asi que son dialogos ya construidos —el comportamiento modal y `accept`/`reject` les viene de `QDialog`.

## Que ventana uso

```mermaid
flowchart TD
    Q{"que ventana necesito?"} --> P["ventana principal de la app"]
    Q --> S["pedir datos en una ventana secundaria"]
    Q --> M["mostrar un mensaje / pregunta si-no"]
    Q --> A["elegir un archivo o carpeta"]
    P --> MW["QMainWindow"]
    S --> DG["QDialog"]
    M --> MB["QMessageBox"]
    A --> FD["QFileDialog"]

    classDef pregunta fill:#5e81ac,stroke:#88c0d0,stroke-width:2px,color:#eceff4;
    classDef grupo fill:#3b4252,stroke:#81a1c1,stroke-width:1.5px,color:#88c0d0;
    classDef hoja fill:#2e3440,stroke:#a3be8c,color:#d8dee9;
    class Q pregunta;
    class P,S,M,A grupo;
    class MW,DG,MB,FD hoja;
```

## Las clases

| Clase | Hereda de | Rol |
|-------|-----------|-----|
| [[QMainWindow]] | `QWidget` | la **ventana principal** de la app: widget central + menus, toolbars y statusbar |
| [[QDialog]] | `QWidget` | dialogo generico, modal o no modal; lo construyes tu con `exec`/`accept`/`reject` |
| [[QMessageBox]] | `QDialog` | dialogo predefinido para mensajes y preguntas (informacion, aviso, si\|no) |
| [[QFileDialog]] | `QDialog` | dialogo predefinido para elegir archivos o carpetas |

## Notas relacionadas

- [[QWidget]] — la base de la que cuelgan todas las ventanas (eventos, `show()`)
- [[concepto_event_loop]] — el bucle que mantiene viva la ventana y procesa sus eventos
