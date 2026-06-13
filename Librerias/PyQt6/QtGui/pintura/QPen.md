---
title: QPen — define el contorno (la pluma) del dibujo
aliases:
  - QPen
  - pluma
tags:
  - pyqt6
  - api/clase
  - gui
lib: pyqt6
mod: QtGui
tipo: clase
requiere:
  - QPainter
  - QColor
draft: false
---

# QPen — define el contorno (la pluma) del dibujo

`QPen` describe **como se traza el contorno**: el color, el grosor y el estilo de las lineas y de los **bordes** de las formas que dibuja [[QPainter]]. Es una clase de **valor/utilidad** (no hereda de `QObject` ni emite señales): se crea, se configura y se pasa a `painter.setPen(...)`. A partir de ahi, cada linea o borde que dibuje el painter usa esa pluma hasta que se cambie.

## Importacion

```python
from PyQt6.QtGui import QPen
```

> [!nota] Sin herencia relevante
> `QPen` es un objeto de valor (como `QColor` o `QPainterPath`): no cuelga de `QObject`, no tiene `parent` ni señales. Se copia por valor, no por referencia con parent.

## Constructor

```python
QPen()                                  # pluma negra de 1px, solida
QPen(color: QColor)                     # solo color; grosor 1, solida
QPen(color: QColor, width: int)         # color y grosor en px
QPen(color: QColor, width: int, style: Qt.PenStyle)   # + estilo de linea
```

La forma habitual es construirla con color y grosor, y ajustar el resto con setters:

```python
pen = QPen(QColor("black"), 2)
```

## Metodos

| Firma | Devuelve | Que hace |
|-------|----------|----------|
| `setColor(color: QColor)` | `None` | fija el color del trazo |
| `setWidth(width: int)` | `None` | grosor en px (entero) |
| `setWidthF(width: float)` | `None` | grosor en px con decimales |
| `setStyle(style: Qt.PenStyle)` | `None` | patron de la linea (continua, discontinua...) |
| `setCapStyle(cap: Qt.PenCapStyle)` | `None` | forma de los extremos de la linea |
| `setJoinStyle(join: Qt.PenJoinStyle)` | `None` | forma de las esquinas donde se unen dos trazos |
| `color()` | `QColor` | color actual de la pluma |
| `width()` | `int` | grosor actual |

Los estilos son enums con **scope completo** (PyQt6): `Qt.PenStyle.SolidLine`, `Qt.PenStyle.DashLine`, `Qt.PenStyle.DotLine` (y `DashDotLine`, `NoPen`).

## Casos de uso

```python
from PyQt6.QtWidgets import QApplication, QWidget
from PyQt6.QtGui import QPainter, QPen, QColor
from PyQt6.QtCore import Qt
import sys

class Lienzo(QWidget):
    def paintEvent(self, event):
        painter = QPainter(self)
        # pluma roja de 3px, discontinua
        painter.setPen(QPen(QColor("red"), 3, Qt.PenStyle.DashLine))
        painter.drawLine(20, 20, 180, 20)
        painter.drawRect(20, 50, 160, 80)   # el borde usa la misma pluma

app = QApplication(sys.argv)
w = Lienzo(); w.resize(220, 160); w.show()
sys.exit(app.exec())
```

## Errores comunes

| Error | Causa | Solucion |
|-------|-------|----------|
| La forma sale sin relleno o con relleno raro | confundes pen (contorno) con brush (relleno) | el contorno lo controla `QPen`; el relleno, [[QBrush]] |
| El estilo de linea no cambia | usaste `Qt.DashLine` (sintaxis PyQt5) | en PyQt6 el enum lleva scope: `Qt.PenStyle.DashLine` |
| La linea sale siempre de 1px aunque ponga grosor | `setWidth(0)` crea una pluma **cosmetica** de 1px fijo | usa un grosor `>= 1` si quieres que escale |

## Notas relacionadas

- [[QPainter]] — el motor de dibujo que usa la pluma con `setPen`
- [[QBrush]] — la contraparte: define el **relleno**, no el contorno
- [[QColor]] — el color que se le pasa a la pluma
