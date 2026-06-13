---
title: QFont — la tipografia del texto (familia, tamaño, peso, estilo)
aliases:
  - QFont
  - fuente
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

# QFont — la tipografia del texto (familia, tamaño, peso, estilo)

`QFont` describe una **fuente de texto**: su familia (Arial, Courier New…), su tamaño en puntos, su peso (negrita) y su estilo (cursiva, subrayado). Es una **clase de valor** (no vive en el arbol de objetos ni emite señales): se construye, se configura y se aplica a un widget con `setFont`, o al [[QPainter]] con `setFont` antes de dibujar texto. Es el valor que controla como se ve cualquier texto en la GUI.

## Importacion

```python
from PyQt6.QtGui import QFont
```

## Herencia

> [!note] Clase de valor, no QObject
> `QFont` **no** hereda de `QObject` ni emite señales: es un valor que se crea por copia y se entrega a un widget o a un painter. No se subclasea ni se conecta a slots. Por eso esta nota no lleva `classDiagram` de herencia.

## Constructor y formas de crear una fuente

```python
QFont(familia: str, pointSize: int = -1)                       # familia y tamaño
QFont(familia: str, pointSize: int, weight: QFont.Weight)      # tambien el peso
```

| Forma | Ejemplo | Resultado |
|-------|---------|-----------|
| Familia y tamaño | `QFont("Arial", 12)` | Arial a 12 puntos |
| Con peso (negrita) | `QFont("Courier New", 10, QFont.Weight.Bold)` | Courier 10pt en negrita |

## Metodos

| Firma | Devuelve | Que hace |
|-------|----------|----------|
| `setFamily(familia: str)` | `None` | fija la familia tipografica |
| `setPointSize(tam: int)` | `None` | fija el tamaño en **puntos** |
| `setBold(on: bool)` | `None` | activa o desactiva la negrita |
| `setItalic(on: bool)` | `None` | activa o desactiva la cursiva |
| `setWeight(w: QFont.Weight)` | `None` | fija el peso (Light, Normal, Bold…) |
| `setUnderline(on: bool)` | `None` | activa o desactiva el subrayado |
| `family()` | `str` | la familia actual |
| `pointSize()` | `int` | el tamaño actual en puntos |

```python
f = QFont("Arial", 12)
f.setBold(True)
f.setItalic(True)
print(f.family(), f.pointSize())      # Arial 12
```

## Casos de uso

### Titulo grande en negrita en un QLabel

```python
from PyQt6.QtWidgets import QApplication, QLabel
from PyQt6.QtGui import QFont
import sys

app = QApplication(sys.argv)
titulo = QLabel("Bienvenido")
titulo.setFont(QFont("Arial", 18, QFont.Weight.Bold))   # 18pt en negrita
titulo.show()
sys.exit(app.exec())
```

### Fuente monoespaciada para un editor de codigo

```python
editor.setFont(QFont("Courier New", 11))   # ancho fijo: alinea el codigo
```

### Aplicar la fuente al pintar texto

```python
painter.setFont(QFont("Arial", 14))
painter.drawText(20, 40, "Texto dibujado")
```

## Errores comunes

| Error | Causa | Solucion |
|-------|-------|----------|
| La fuente no se ve como esperabas | fijaste una familia que no existe en el sistema: Qt elige una sustituta | usa una familia instalada o comprueba con `family()` la efectiva |
| El texto sale mas grande o pequeño segun la pantalla | usaste pixeles cuando querias un tamaño fisico estable | usa `setPointSize` (puntos), no tamaños en pixel |
| `setBold` no surte efecto junto con `setWeight` | `setWeight` posterior sobrescribe la negrita | fija el peso de una vez con `setWeight(QFont.Weight.Bold)` |

## Notas relacionadas

- [[QLabel]] — recibe la fuente con `setFont` para su texto
- [[QPainter]] — usa `setFont` antes de `drawText`
- [[QColor]] — el color del texto, complemento de la fuente
