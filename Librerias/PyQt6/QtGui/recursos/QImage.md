---
title: QImage — imagen optimizada para manipular pixeles
aliases:
  - QImage
  - imagen
tags:
  - pyqt6
  - api/clase
  - gui
lib: pyqt6
mod: QtGui
tipo: clase
requiere:
  - QPixmap
  - QColor
draft: false
---

# QImage — imagen optimizada para manipular pixeles

`QImage` es una **imagen optimizada para MANIPULAR PIXELES**: leer y escribir el color de cada pixel, convertir entre formatos, generar imagenes por codigo. Es una **clase de valor**: no vive en el arbol de objetos ni emite senales. Su contrapartida es [[QPixmap]], que esta pensada para **mostrar** rapido en pantalla pero no deja editar pixeles. El flujo tipico es: editar en `QImage` y, para mostrarla, convertir a pixmap con `QPixmap.fromImage(img)`.

## Importacion

```python
from PyQt6.QtGui import QImage
```

## Herencia

> [!note] Clase de valor, no QObject
> `QImage` **no** hereda de `QObject` ni emite senales: es un valor que se crea por copia. No se subclasea ni se conecta a slots. Por eso esta nota no lleva `classDiagram` de herencia.

## Constructor y formas de crear una imagen

```python
QImage(ruta: str)                                  # cargar desde archivo
QImage(ancho: int, alto: int, formato: QImage.Format)   # vacia, en un formato dado
```

| Forma | Ejemplo | Resultado |
|-------|---------|-----------|
| Desde archivo | `QImage("imagen.png")` | la imagen cargada (vacia si la ruta es mala) |
| Vacia por tamano y formato | `QImage(64, 64, QImage.Format.Format_RGB32)` | lienzo de 64x64 listo para escribir pixeles |

## Metodos

| Firma | Devuelve | Que hace |
|-------|----------|----------|
| `pixelColor(x: int, y: int)` | `QColor` | el color del pixel en `(x, y)` |
| `setPixelColor(x: int, y: int, color: QColor)` | `None` | fija el color del pixel en `(x, y)` |
| `load(ruta: str)` | `bool` | carga una imagen desde archivo; `True` si lo logro |
| `save(ruta: str)` | `bool` | guarda la imagen a archivo; `True` si lo logro |
| `convertToFormat(formato: QImage.Format)` | `QImage` | devuelve una copia en otro formato de pixel |
| `width()` | `int` | ancho en pixeles |
| `height()` | `int` | alto en pixeles |
| `isNull()` | `bool` | `True` si no cargo nada (imagen vacia) |

```python
img = QImage("foto.png")
c = img.pixelColor(0, 0)              # QColor del primer pixel
img.setPixelColor(0, 0, QColor("red"))
```

## Casos de uso

### Leer y modificar pixeles (invertir colores)

```python
from PyQt6.QtGui import QImage, QColor

img = QImage("foto.png")
for y in range(img.height()):
    for x in range(img.width()):
        c = img.pixelColor(x, y)
        invertido = QColor(255 - c.red(), 255 - c.green(), 255 - c.blue())
        img.setPixelColor(x, y, invertido)
img.save("foto_invertida.png")
```

### Generar una imagen por codigo y mostrarla

```python
from PyQt6.QtWidgets import QApplication, QLabel
from PyQt6.QtGui import QImage, QPixmap, QColor
import sys

app = QApplication(sys.argv)

img = QImage(64, 64, QImage.Format.Format_RGB32)
for y in range(64):
    for x in range(64):
        img.setPixelColor(x, y, QColor(x * 4, y * 4, 128))

label = QLabel()
label.setPixmap(QPixmap.fromImage(img))   # convertir a pixmap para mostrar
label.show()
sys.exit(app.exec())
```

## QImage vs QPixmap

| Necesitas | Usa | Por que |
|-----------|-----|---------|
| Editar pixeles, procesar, generar por codigo | `QImage` | da acceso a cada pixel (`pixelColor`/`setPixelColor`) |
| Solo mostrar la imagen en pantalla | [[QPixmap]] | optimizada para dibujarse rapido en un widget |
| Mostrar una imagen que editaste en QImage | ambas | convierte con `QPixmap.fromImage(img)` |

## Errores comunes

| Error | Causa | Solucion |
|-------|-------|----------|
| Procesar pixeles es lento o no funciona | lo intentaste sobre un [[QPixmap]], que no esta hecho para editar pixeles | trabaja sobre un `QImage` y convierte solo al final para mostrar |
| La imagen editada no aparece en el widget | un QLabel no muestra un `QImage` directamente | conviertela con `QPixmap.fromImage(img)` antes de `setPixmap` |
| La imagen sale en blanco | la ruta era mala y QImage queda vacia en silencio | comprueba `isNull()` tras cargar |

## Notas relacionadas

- [[QPixmap]] — la imagen para mostrar en pantalla; se convierte con `fromImage` / `toImage`
- [[QColor]] — el color que devuelve `pixelColor` y que recibe `setPixelColor`
- [[PyQt6/QtGui/recursos/index | recursos]] — el grupo de recursos graficos de Qt
