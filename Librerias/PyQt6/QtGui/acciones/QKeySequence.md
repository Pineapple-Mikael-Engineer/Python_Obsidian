---
title: QKeySequence — una combinacion de teclas
aliases:
  - QKeySequence
  - combinacion de teclas
tags:
  - pyqt6
  - api/clase
  - gui
lib: pyqt6
mod: QtGui
tipo: clase
requiere:
  - QAction
draft: false
---

# QKeySequence — una combinacion de teclas

`QKeySequence` representa una **combinacion de teclas** (por ejemplo `Ctrl+S`). Es el valor que se pasa a `setShortcut` de una [[QAction]] o al constructor de un [[QShortcut]]. Puede construirse desde un texto literal o, mejor, desde un atajo **estandar y portable** entre sistemas operativos.

> [!nota] Clase de valor, no hereda de `QObject`
> A diferencia de `QAction` o `QShortcut`, `QKeySequence` **no es un `QObject`**: es una clase de valor (como `QColor` o `QPoint`). No tiene señales ni `parent`; se crea, se copia y se pasa como argumento. Por eso no lleva `classDiagram` de herencia.

## Importacion

```python
from PyQt6.QtGui import QKeySequence
```

## Constructor y formas

```python
QKeySequence(key: str)                              # desde texto: "Ctrl+S"
QKeySequence(key: QKeySequence.StandardKey)         # atajo estandar y portable
```

- **Desde texto**: `QKeySequence("Ctrl+S")`. Literal, lo escribes tu.
- **Desde un `StandardKey`**: `QKeySequence(QKeySequence.StandardKey.Save)`. Qt elige el atajo adecuado para cada plataforma (ej. Copiar es `Ctrl+C` en Linux/Windows pero `Cmd+C` en macOS). Es la forma **recomendada** por ser portable.

## StandardKey comunes

El enum `StandardKey` tiene scope completo en Qt6 (`QKeySequence.StandardKey.Copy`, no `QKeySequence.Copy`).

| StandardKey | Atajo tipico |
|-------------|--------------|
| `QKeySequence.StandardKey.Save` | Ctrl+S |
| `QKeySequence.StandardKey.Open` | Ctrl+O |
| `QKeySequence.StandardKey.Copy` | Ctrl+C |
| `QKeySequence.StandardKey.Paste` | Ctrl+V |
| `QKeySequence.StandardKey.Undo` | Ctrl+Z |
| `QKeySequence.StandardKey.Redo` | Ctrl+Y / Ctrl+Shift+Z |
| `QKeySequence.StandardKey.Quit` | Ctrl+Q |

## Casos de uso

```python
from PyQt6.QtWidgets import QApplication, QMainWindow
from PyQt6.QtGui import QAction, QKeySequence
import sys

app = QApplication(sys.argv)
ventana = QMainWindow()
menu = ventana.menuBar().addMenu("Archivo")

# Recomendado: atajo estandar y portable
guardar = QAction("Guardar", ventana)
guardar.setShortcut(QKeySequence.StandardKey.Save)   # Ctrl+S donde toque
menu.addAction(guardar)

# Alternativa literal (cuando no hay StandardKey adecuado)
buscar = QAction("Buscar", ventana)
buscar.setShortcut(QKeySequence("Ctrl+F"))
menu.addAction(buscar)

ventana.show()
sys.exit(app.exec())
```

## Errores comunes

| Error | Causa | Solucion |
|-------|-------|----------|
| El atajo no es el esperado en macOS | escribiste el atajo a mano (`"Ctrl+C"`) | usa el `StandardKey` portable cuando exista |
| `AttributeError: StandardKey has no attribute...` | usaste el enum sin scope (`QKeySequence.Save`) | en Qt6 va con scope: `QKeySequence.StandardKey.Save` |

## Notas relacionadas

- [[QAction]] — recibe el `QKeySequence` en su `setShortcut`
- [[QShortcut]] — recibe el `QKeySequence` en su constructor
