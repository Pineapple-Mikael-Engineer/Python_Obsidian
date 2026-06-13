---
title: QBrush — define el relleno (la brocha) de las formas
aliases:
  - QBrush
  - brocha
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

# QBrush — define el relleno (la brocha) de las formas

`QBrush` describe **con que se rellena** el interior de las formas que dibuja [[QPainter]]: un color solido, un patron o un gradiente. Es una clase de **valor/utilidad** (no hereda de `QObject` ni emite senales): se crea, se configura y se pasa a `painter.setBrush(...)`. Mientras [[QPen]] controla el contorno, `QBrush` controla el area interior.

## Importacion

```python
from PyQt6.QtGui import QBrush
```

> [!nota] Sin herencia relevante
> Como [[QPen]], `QBrush` es un objeto de valor: no cuelga de `QObject`, no tiene `parent` ni senales. Se copia por valor.

## Constructor

```python
QBrush()                                       # sin relleno (NoBrush)
QBrush(color: QColor)                           # relleno solido del color dado
QBrush(color: QColor, style: Qt.BrushStyle)     # color + patron
QBrush(gradient: QGradient)                      # relleno con gradiente
```

Lo habitual es un brush solido de un color:

```python
brush = QBrush(QColor("blue"))
```

## Metodos

| Firma | Devuelve | Que hace |
|-------|----------|----------|
| `setColor(color: QColor)` | `None` | fija el color del relleno |
| `setStyle(style: Qt.BrushStyle)` | `None` | patron del relleno (solido, sin relleno, tramas...) |
| `setTexture(pixmap: QPixmap)` | `None` | rellena con una imagen repetida (textura) |
| `color()` | `QColor` | color actual del relleno |
| `style()` | `Qt.BrushStyle` | patron actual |

Los estilos son enums con **scope completo** (PyQt6): `Qt.BrushStyle.SolidPattern`, `Qt.BrushStyle.NoBrush`, ademas de tramas (`Dense1Pattern`, `CrossPattern`, etc.).

## Casos de uso

```python
from PyQt6.QtWidgets import QApplication, QWidget
from PyQt6.QtGui import QPainter, QBrush, QColor, QLinearGradient
from PyQt6.QtCore import Qt
import sys

class Lienzo(QWidget):
    def paintEvent(self, event):
        painter = QPainter(self)

        # 1. relleno solido azul
        painter.setBrush(QBrush(QColor("blue")))
        painter.drawRect(20, 20, 100, 60)

        # 2. relleno con gradiente lineal (de un color a otro)
        grad = QLinearGradient(140, 20, 240, 80)
        grad.setColorAt(0.0, QColor("#5e81ac"))
        grad.setColorAt(1.0, QColor("#a3be8c"))
        painter.setBrush(QBrush(grad))
        painter.drawRect(140, 20, 100, 60)

app = QApplication(sys.argv)
w = Lienzo(); w.resize(280, 110); w.show()
sys.exit(app.exec())
```

## Errores comunes

| Error | Causa | Solucion |
|-------|-------|----------|
| La forma sale solo con borde, sin relleno | no llamaste a `setBrush`, o el brush es `NoBrush` | pasa un `QBrush(color)` con `setBrush` antes de dibujar |
| Confundo brush con pen | brush rellena, pen dibuja el contorno | el contorno es [[QPen]]; el relleno, `QBrush` |
| El patron no cambia | usaste `Qt.SolidPattern` (sintaxis PyQt5) | en PyQt6: `Qt.BrushStyle.SolidPattern` |

## Notas relacionadas

- [[QPainter]] — el motor de dibujo que usa el brush con `setBrush`
- [[QPen]] — la contraparte: define el **contorno**, no el relleno
- [[QColor]] — el color que se le pasa a la brocha
