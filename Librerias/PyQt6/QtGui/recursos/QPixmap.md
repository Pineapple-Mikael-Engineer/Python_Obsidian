---
title: QPixmap — imagen en memoria optimizada para mostrarse en pantalla
aliases:
  - QPixmap
  - pixmap
tags:
  - pyqt6
  - api/clase
  - gui
lib: pyqt6
mod: QtGui
tipo: clase
requiere:
  - QImage
draft: false
---

# QPixmap — imagen en memoria optimizada para mostrarse en pantalla

`QPixmap` es una **imagen en memoria optimizada para MOSTRARSE en pantalla** (dibujarla rapido en un widget). Es una **clase de valor**: no vive en el arbol de objetos ni emite senales, se crea y se pasa a quien dibuja. Es el formato de imagen que consumen `QLabel.setPixmap`, `QPainter.drawPixmap` y `QIcon`. Su contrapartida es [[QImage]]: QPixmap es para **mostrar** (rapido en pantalla, pero no deja editar pixeles); QImage es para **manipular pixeles**. Se convierte de una a otra con `QPixmap.fromImage` / `toImage`.

## Importacion

```python
from PyQt6.QtGui import QPixmap
```

## Herencia

> [!note] Clase de valor, no QObject
> `QPixmap` **no** hereda de `QObject` ni emite senales: es un valor que se crea por copia y se pasa a las funciones de dibujo. No se subclasea ni se conecta a slots. Por eso esta nota no lleva `classDiagram` de herencia.

## Constructor y formas de crear un pixmap

```python
QPixmap(ruta: str)                    # cargar desde archivo ("imagen.png")
QPixmap(ancho: int, alto: int)        # pixmap vacio del tamano dado
QPixmap.fromImage(imagen: QImage)     # staticmethod: desde una QImage
```

| Forma | Ejemplo | Resultado |
|-------|---------|-----------|
| Desde archivo | `QPixmap("imagen.png")` | la imagen cargada (vacia si la ruta es mala) |
| Vacia por tamano | `QPixmap(200, 100)` | pixmap de 200x100 sin contenido definido |
| Desde una QImage | `QPixmap.fromImage(img)` | convierte una [[QImage]] (editada) a pixmap para mostrar |

## Metodos

| Firma | Devuelve | Que hace |
|-------|----------|----------|
| `load(ruta: str)` | `bool` | carga una imagen desde archivo; `True` si lo logro |
| `save(ruta: str)` | `bool` | guarda el pixmap a archivo; `True` si lo logro |
| `scaled(w: int, h: int, aspectRatioMode=...)` | `QPixmap` | devuelve una copia redimensionada a w x h |
| `isNull()` | `bool` | `True` si no cargo nada (pixmap vacio) |
| `width()` | `int` | ancho en pixeles |
| `height()` | `int` | alto en pixeles |
| `toImage()` | `QImage` | convierte a [[QImage]] para manipular pixeles |

```python
pix = QPixmap("foto.png")
print(pix.isNull())                   # False si cargo bien
print(pix.width(), pix.height())
```

Para `scaled`, lo habitual es mantener la proporcion con `Qt.AspectRatioMode.KeepAspectRatio` (sin el, la imagen se deforma):

```python
from PyQt6.QtCore import Qt
mini = pix.scaled(100, 100, Qt.AspectRatioMode.KeepAspectRatio)
```

## Casos de uso

### Mostrar una imagen en un QLabel

```python
from PyQt6.QtWidgets import QApplication, QLabel
from PyQt6.QtGui import QPixmap
import sys

app = QApplication(sys.argv)
label = QLabel()
label.setPixmap(QPixmap("foto.png"))   # el uso mas comun de QPixmap
label.show()
sys.exit(app.exec())
```

### Escalar manteniendo la proporcion

```python
from PyQt6.QtCore import Qt

pix = QPixmap("foto.png")
escalada = pix.scaled(300, 200, Qt.AspectRatioMode.KeepAspectRatio)
label.setPixmap(escalada)
```

### Comprobar isNull tras cargar

```python
pix = QPixmap("ruta/que/quiza/no/existe.png")
if pix.isNull():
    print("no se pudo cargar la imagen")
else:
    label.setPixmap(pix)
```

## QPixmap vs QImage

| Necesitas | Usa | Por que |
|-----------|-----|---------|
| Solo mostrar una imagen en pantalla | `QPixmap` | optimizada para dibujarse rapido; no permite editar pixeles |
| Leer o modificar pixeles, procesar | [[QImage]] | da acceso a cada pixel (`pixelColor`/`setPixelColor`) |
| Mostrar una imagen que editaste | ambas | edita en QImage y convierte con `QPixmap.fromImage` |

## Errores comunes

| Error | Causa | Solucion |
|-------|-------|----------|
| La imagen sale en blanco / no aparece | la ruta era mala y QPixmap no avisa (queda vacio en silencio) | comprueba `isNull()` tras cargar |
| La imagen sale deformada al escalar | `scaled` sin modo de proporcion estira la imagen | pasa `Qt.AspectRatioMode.KeepAspectRatio` |
| No puedo cambiar pixeles del QPixmap | QPixmap no esta hecho para editar pixeles | pasa a [[QImage]] con `toImage()`, edita, y vuelve con `QPixmap.fromImage` |

## Notas relacionadas

- [[QImage]] — la imagen para manipular pixeles; se convierte con `fromImage` / `toImage`
- [[PyQt6/QtGui/recursos/index | recursos]] — el grupo de recursos graficos de Qt
