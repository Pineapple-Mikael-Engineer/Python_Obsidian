---
title: QPainterPath — describe una figura compleja para dibujar de una vez
aliases:
  - QPainterPath
  - ruta
tags:
  - pyqt6
  - api/clase
  - gui
lib: pyqt6
mod: QtGui
tipo: clase
requiere:
  - QPainter
draft: false
---

# QPainterPath — describe una figura compleja para dibujar de una vez

`QPainterPath` acumula una **ruta**: una combinacion de lineas, curvas y formas (rectangulos, elipses) que se construye paso a paso y luego se dibuja o se rellena **de una sola vez** con `painter.drawPath(path)`. Es una clase de **valor/utilidad** (no hereda de `QObject` ni emite señales): sirve para describir poligonos, contornos con curvas o siluetas que no se pueden hacer con un solo `drawRect`/`drawEllipse`.

## Importacion

```python
from PyQt6.QtGui import QPainterPath
```

> [!nota] Sin herencia relevante
> Como [[QPen]] y [[QBrush]], es un objeto de valor: no cuelga de `QObject`, sin `parent` ni señales. Se construye, se llena con sus metodos y se entrega a [[QPainter]].

## Constructor y metodos

```python
QPainterPath()                        # ruta vacia
QPainterPath(start: QPointF)          # ruta que arranca en un punto
```

| Firma | Devuelve | Que hace |
|-------|----------|----------|
| `moveTo(x: float, y: float)` | `None` | mueve el "lapiz" sin trazar (inicia un subtrazo) |
| `lineTo(x: float, y: float)` | `None` | traza una linea recta hasta el punto |
| `cubicTo(c1x, c1y, c2x, c2y, x, y)` | `None` | curva Bezier cubica (dos puntos de control) |
| `quadTo(cx, cy, x, y)` | `None` | curva Bezier cuadratica (un punto de control) |
| `addRect(x, y, w, h)` | `None` | añade un rectangulo a la ruta |
| `addEllipse(x, y, w, h)` | `None` | añade una elipse a la ruta |
| `closeSubpath()` | `None` | cierra el subtrazo actual (lo une con su inicio) |

## Casos de uso

```python
from PyQt6.QtWidgets import QApplication, QWidget
from PyQt6.QtGui import QPainter, QPainterPath, QPen, QBrush, QColor
from PyQt6.QtCore import Qt
import sys

class Lienzo(QWidget):
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        path = QPainterPath()
        path.moveTo(40, 120)            # arranque obligatorio: posiciona sin trazar
        path.lineTo(100, 30)            # lado recto
        path.quadTo(160, 60, 180, 120)  # lado curvo (Bezier cuadratica)
        path.closeSubpath()             # cierra para poder rellenar

        painter.setPen(QPen(QColor("black"), 2))
        painter.setBrush(QBrush(QColor("#a3be8c")))
        painter.drawPath(path)          # dibuja contorno + relleno de una vez

app = QApplication(sys.argv)
w = Lienzo(); w.resize(220, 160); w.show()
sys.exit(app.exec())
```

## Errores comunes

| Error | Causa | Solucion |
|-------|-------|----------|
| La ruta empieza desde una esquina inesperada | no llamaste a `moveTo` antes del primer `lineTo` | inicia siempre el subtrazo con `moveTo(x, y)` |
| El relleno sale abierto o incompleto | no cerraste la ruta antes de rellenar | llama a `closeSubpath()` cuando quieras rellenar |
| Dibujo punto a punto y va lento | dibujas cada segmento por separado | acumula todo en un `QPainterPath` y un solo `drawPath` |

## Notas relacionadas

- [[QPainter]] — el motor de dibujo que pinta la ruta con `drawPath`
- [[QPen]] — define el contorno con que se traza la ruta
- [[QBrush]] — define el relleno de la ruta cerrada
