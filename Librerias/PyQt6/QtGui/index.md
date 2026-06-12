---
title: QtGui — el bajo nivel grafico de Qt
aliases:
  - QtGui
tags:
  - pyqt6
  - indice
draft: false
---

# QtGui — el bajo nivel grafico de Qt

`QtGui` es la capa **grafica de bajo nivel** de Qt, a medio camino entre `QtCore` (el nucleo no visual) y `QtWidgets` (los controles ya hechos). Aqui no hay botones ni ventanas: viven las piezas con las que **se dibujan** y se alimentan esos widgets. En concreto agrupa el motor de **pintura** (`QPainter`, `QColor`, `QPen`, `QBrush`), los **recursos** graficos (`QPixmap`, `QImage`, `QIcon`, `QFont`), los **eventos** concretos (`QMouseEvent`, `QKeyEvent`, `QPaintEvent`...) y las **acciones** (`QAction`, `QShortcut`, que en Qt6 viven aqui y no en `QtWidgets`).

## En accion

El caso tipico de `QtGui`: subclasear un `QWidget` y sobreescribir su `paintEvent` para dibujar a mano con un `QPainter`.

```python
from PyQt6.QtWidgets import QApplication, QWidget
from PyQt6.QtGui import QPainter, QColor, QPen
from PyQt6.QtCore import Qt
import sys

class Lienzo(QWidget):
    def paintEvent(self, e):                 # llega un QPaintEvent
        p = QPainter(self)                   # el motor de pintura (QtGui)
        p.setPen(QPen(QColor("#5e81ac"), 3)) # color + grosor del trazo
        p.setBrush(QColor("#88c0d0"))        # relleno
        p.drawEllipse(20, 20, 120, 80)       # dibuja sobre el widget
        p.end()

app = QApplication(sys.argv)
w = Lienzo()
w.resize(200, 140)
w.show()
sys.exit(app.exec())
```

## Subcarpetas

| Subcarpeta | Que agrupa | Clases |
|------------|-----------|--------|
| [[PyQt6/QtGui/pintura/index\|pintura]] | el motor de dibujo 2D | `QPainter`, `QColor`, `QPen`, `QBrush`, `QPainterPath` |
| [[PyQt6/QtGui/recursos/index\|recursos]] | imagenes, iconos y tipografias | `QPixmap`, `QImage`, `QIcon`, `QFont` |
| [[PyQt6/QtGui/eventos/index\|eventos]] | los eventos concretos del usuario | `QEvent`, `QMouseEvent`, `QKeyEvent`, `QPaintEvent`, `QResizeEvent` |
| [[PyQt6/QtGui/acciones/index\|acciones]] | acciones y atajos de teclado | `QAction`, `QShortcut`, `QKeySequence` |

> [!nota] Cambio de Qt5 a Qt6
> `QAction` y `QShortcut` se **movieron de `QtWidgets` (Qt5) a `QtGui` (Qt6)**. Si portas codigo antiguo, importalos ahora desde `PyQt6.QtGui`, no desde `PyQt6.QtWidgets`.

## Como navegar

| Quiero… | Ir a |
|---------|------|
| Dibujar a mano dentro de un `paintEvent` | [[PyQt6/QtGui/pintura/index\|pintura]] |
| Cargar una imagen, un icono o una fuente | [[PyQt6/QtGui/recursos/index\|recursos]] |
| Reaccionar a raton, teclado, redimension o cierre | [[PyQt6/QtGui/eventos/index\|eventos]] |
| Una accion de menu reutilizable o un atajo global | [[PyQt6/QtGui/acciones/index\|acciones]] |

## Notas relacionadas

- [[QEvent]] — la clase base de la que cuelgan todos los eventos de la carpeta `eventos/`
- [[QWidget]] — quien se pinta en `paintEvent` y recibe los eventos de `QtGui`
- [[PyQt6/QtWidgets/index\|QtWidgets]] — los controles ya construidos sobre estas piezas
