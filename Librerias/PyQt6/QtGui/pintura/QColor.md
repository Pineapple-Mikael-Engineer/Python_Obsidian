---
title: QColor — un color RGB, RGBA, HSV o por nombre
aliases:
  - QColor
  - color
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

# QColor — un color RGB, RGBA, HSV o por nombre

`QColor` representa un **color** y es una **clase de valor**: no vive en el arbol de objetos, no emite señales, simplemente encapsula un color que se construye y se pasa a quien dibuja. Es el valor que consumen [[QPainter]] (`setPen`/`setBrush`), `QPen` y `QBrush`. Se puede definir por nombre CSS, por hex, por componentes RGB/RGBA o en espacio HSV, y ofrece metodos para leer sus componentes y para aclarar u oscurecer el color.

## Importacion

```python
from PyQt6.QtGui import QColor
```

## Herencia

> [!note] Clase de valor, no QObject
> `QColor` **no** hereda de `QObject` ni emite señales: es un valor (como un `int` o una cadena), de los que se crean por copia y se pasan a las funciones de dibujo. No se subclasea ni se conecta a slots. Por eso esta nota no lleva `classDiagram` de herencia.

## Constructor y formas de crear un color

```python
QColor(nombre: str)                          # nombre CSS ("red") o hex ("#88c0d0")
QColor(r: int, g: int, b: int)               # RGB, cada componente 0-255
QColor(r: int, g: int, b: int, a: int)       # RGBA: a = alpha (0 transparente, 255 opaco)
```

| Forma | Ejemplo | Resultado |
|-------|---------|-----------|
| Por nombre CSS | `QColor("red")` | rojo puro |
| Por hex | `QColor("#88c0d0")` | azul Nord |
| Por componentes RGB | `QColor(255, 0, 0)` | rojo (cada canal 0-255) |
| Con alpha (transparencia) | `QColor(255, 0, 0, 128)` | rojo semitransparente (~50%) |

## Metodos

| Firma | Devuelve | Que hace |
|-------|----------|----------|
| `red()` | `int` | componente rojo (0-255) |
| `green()` | `int` | componente verde (0-255) |
| `blue()` | `int` | componente azul (0-255) |
| `alpha()` | `int` | opacidad (0 transparente, 255 opaco) |
| `name()` | `str` | el color en hex `"#rrggbb"` |
| `setAlpha(a: int)` | `None` | fija la opacidad (0-255) |
| `lighter(factor: int = 150)` | `QColor` | devuelve una copia mas clara (factor > 100 aclara) |
| `darker(factor: int = 200)` | `QColor` | devuelve una copia mas oscura (factor > 100 oscurece) |
| `fromHsv(h: int, s: int, v: int)` | `QColor` | **staticmethod**: crea un color en espacio HSV (matiz, saturacion, valor) |

```python
c = QColor("#88c0d0")
print(c.red(), c.green(), c.blue())   # 136 192 208
print(c.name())                       # "#88c0d0"
claro = c.lighter(130)                # una version mas clara
```

## Casos de uso

### Pasar un color a un pincel de QPainter

```python
from PyQt6.QtWidgets import QApplication, QWidget
from PyQt6.QtGui import QPainter, QColor
import sys

class Caja(QWidget):
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setBrush(QColor(94, 129, 172))   # azul opaco
        painter.drawRect(20, 20, 100, 60)

app = QApplication(sys.argv)
w = Caja()
w.resize(160, 100)
w.show()
sys.exit(app.exec())
```

### Color semitransparente con alpha

```python
rojo_translucido = QColor(255, 0, 0, 128)   # alpha 128 ~ 50% opaco
# o, partiendo de un color opaco:
c = QColor("blue")
c.setAlpha(80)                              # ahora deja ver lo que hay debajo
```

### Aclarar y oscurecer (variantes de un mismo color)

```python
base = QColor("#5e81ac")
hover = base.lighter(120)   # mas claro: util para estado hover
borde = base.darker(140)    # mas oscuro: util para un borde
```

## Errores comunes

| Error | Causa | Solucion |
|-------|-------|----------|
| El color sale mal o se trunca | pasaste componentes RGB fuera de 0-255 | mantente en el rango 0-255 en cada canal |
| El color no es transparente aunque querias que lo fuera | olvidaste el cuarto argumento `alpha` (por defecto 255 = opaco) | usa `QColor(r, g, b, a)` o `setAlpha(a)` con `a < 255` |
| `lighter`/`darker` no cambian nada | usaste un factor de 100 (sin efecto) o lo aplicaste al mismo objeto sin recoger el retorno | recoge el `QColor` devuelto: `claro = c.lighter(130)` |

## Notas relacionadas

- [[QPainter]] — recibe el `QColor` en `setPen`/`setBrush` para dibujar
- [[PyQt6/QtGui/pintura/index | pintura]] — el grupo de clases de dibujo de Qt
