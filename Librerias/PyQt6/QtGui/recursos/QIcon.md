---
title: QIcon — un icono multi-resolucion para botones, acciones y ventanas
aliases:
  - QIcon
  - icono
tags:
  - pyqt6
  - api/clase
  - gui
lib: pyqt6
mod: QtGui
tipo: clase
requiere:
  - QPixmap
draft: false
---

# QIcon — un icono multi-resolucion para botones, acciones y ventanas

`QIcon` representa un **icono**: una imagen pensada para botones, acciones, pestanas y la ventana, y es una **clase de valor** (no vive en el arbol de objetos ni emite senales). A diferencia de una imagen suelta, un `QIcon` puede contener **varias resoluciones** (para que Qt elija la nitida segun el tamano) y **varios estados** (normal, deshabilitado, activo). Se construye desde un archivo, desde un [[QPixmap]] o desde el tema del sistema, y se pasa a quien lo muestra con `setIcon` / `setWindowIcon`.

## Importacion

```python
from PyQt6.QtGui import QIcon
```

## Herencia

> [!note] Clase de valor, no QObject
> `QIcon` **no** hereda de `QObject` ni emite senales: es un valor que se crea por copia y se entrega a botones, acciones o la ventana. No se subclasea ni se conecta a slots. Por eso esta nota no lleva `classDiagram` de herencia.

## Constructor y formas de crear un icono

```python
QIcon(ruta: str)                    # desde un archivo de imagen ("icono.png")
QIcon(pixmap: QPixmap)              # desde un QPixmap ya cargado
QIcon.fromTheme(nombre: str)        # staticmethod: icono del TEMA del sistema
```

| Forma | Ejemplo | Resultado |
|-------|---------|-----------|
| Desde archivo | `QIcon("save.png")` | icono cargado del disco |
| Desde un [[QPixmap]] | `QIcon(qpixmap)` | icono a partir de una imagen ya en memoria |
| Del tema del sistema | `QIcon.fromTheme("document-save")` | icono portable del tema (Linux) |

## Metodos

| Firma | Devuelve | Que hace |
|-------|----------|----------|
| `addFile(ruta: str)` | `None` | anade otra resolucion del mismo icono |
| `pixmap(w: int, h: int)` | `QPixmap` | obtiene el icono renderizado a un tamano |
| `isNull()` | `bool` | `True` si el icono esta vacio (ruta mala, sin contenido) |
| `fromTheme(nombre: str)` | `QIcon` | **staticmethod**: icono del tema del sistema |

```python
ico = QIcon("save.png")
ico.addFile("save@2x.png")            # version de mayor resolucion
print(ico.isNull())                   # False si cargo bien
pm = ico.pixmap(32, 32)               # como QPixmap a 32x32
```

## Casos de uso

### Icono en un boton o una accion

```python
from PyQt6.QtWidgets import QApplication, QPushButton
from PyQt6.QtGui import QIcon
import sys

app = QApplication(sys.argv)
boton = QPushButton("Guardar")
boton.setIcon(QIcon("save.png"))      # icono a la izquierda del texto
boton.show()
sys.exit(app.exec())
```

```python
# en una accion de menu / barra de herramientas
accion.setIcon(QIcon("save.png"))
```

### Icono de la ventana

```python
ventana.setWindowIcon(QIcon("app.png"))   # icono de la barra de titulo y la tarea
```

### Icono del tema del sistema (portable en Linux)

```python
boton.setIcon(QIcon.fromTheme("document-save"))   # usa el icono del escritorio
```

## Errores comunes

| Error | Causa | Solucion |
|-------|-------|----------|
| El boton no muestra icono pero no hay error | pasaste una ruta mala: el icono queda vacio (no lanza excepcion) | comprueba la ruta y `isNull()`; usa rutas de recurso `:/...` si empaquetas |
| Confundir `QIcon` con [[QPixmap]] | `QPixmap` es una imagen sola; `QIcon` es multi-estado/multi-resolucion | usa `QIcon` para botones/acciones/ventana; `QPixmap` para mostrar en un QLabel |
| `fromTheme` no devuelve nada en Windows/Mac | los temas de iconos son propios de Linux | en otras plataformas carga el icono desde archivo |

## Notas relacionadas

- [[QPixmap]] — la imagen desde la que se puede construir un icono
- [[QPushButton]] — recibe el icono con `setIcon`
- [[QAction]] — tambien usa `setIcon` para menus y barras de herramientas
