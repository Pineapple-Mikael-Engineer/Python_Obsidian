---
title: QPushButton — boton que emite clicked al pulsarse
aliases: [QPushButton, boton]
tags: [pyqt6, api/clase, widgets]
lib: pyqt6
mod: QtWidgets
tipo: clase
hereda_de: QAbstractButton
senales: [clicked, pressed, released, toggled]
requiere: [QAbstractButton, concepto_signals_slots]
draft: false
---

# QPushButton — boton que emite clicked al pulsarse

`QPushButton` es el boton de pulsar mas comun: muestra un texto (o icono) y **emite la senal `clicked`** cuando el usuario lo pulsa. Casi no se usa "tal cual": lo normal es crearlo, conectar su `clicked` a un slot, y estilizarlo con QSS. Toda su logica de boton (texto, icono, estado pulsado) la hereda de [[QAbstractButton]].

## Importacion

```python
from PyQt6.QtWidgets import QPushButton
```

## Herencia

```mermaid
classDiagram
    QObject <|-- QWidget
    QWidget <|-- QAbstractButton
    QAbstractButton <|-- QPushButton
    class QObject { +connect() +parent }
    class QWidget { +show() +setEnabled() +setToolTip() }
    class QAbstractButton { +setText() +setIcon() +setCheckable() +clicked +toggled }
    class QPushButton { +setDefault() +setMenu() }
```

Lo que `QPushButton` **no** define lo hereda: el texto/icono y las senales (`clicked`, `toggled`…) vienen de [[QAbstractButton]]; mostrarse, habilitarse o el tooltip vienen de [[QWidget]]; conectar senales y el `parent` vienen de `QObject`. Apenas agrega lo suyo (`setDefault`, `setMenu`).

## Senales

| Senal | Cuando se emite | Argumentos |
|-------|-----------------|------------|
| `clicked` | al pulsar y soltar dentro del boton | `checked: bool` (estado, solo util si es checkable) |
| `pressed` | al presionar (antes de soltar) | — |
| `released` | al soltar | — |
| `toggled` | cuando cambia el estado de un boton checkable | `checked: bool` |

```python
boton.clicked.connect(self.guardar)          # lo habitual
boton.toggled.connect(lambda on: print(on))  # solo si setCheckable(True)
```

## Constructor y metodos clave

```python
QPushButton(text: str = "", parent: QWidget | None = None)
```

| Metodo | Que hace |
|--------|----------|
| `setText(str)` / `text()` | texto del boton (heredado de QAbstractButton) |
| `setIcon(QIcon)` | icono a la izquierda del texto |
| `setCheckable(bool)` | convierte el boton en conmutador (mantiene estado pulsado) |
| `setEnabled(bool)` | habilita o deshabilita (heredado de QWidget) |
| `setDefault(bool)` | boton por defecto del dialogo (responde a Enter) |
| `setMenu(QMenu)` | adjunta un menu desplegable al boton |

## Casos de uso

```python
from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout
import sys

app = QApplication(sys.argv)
w = QWidget(); lay = QVBoxLayout(w)

# 1. Boton simple conectado a un slot
b1 = QPushButton("Guardar")
b1.clicked.connect(lambda: print("guardado"))
lay.addWidget(b1)

# 2. Boton conmutador (checkable): emite toggled con su estado
b2 = QPushButton("Modo oscuro")
b2.setCheckable(True)
b2.toggled.connect(lambda on: print("oscuro" if on else "claro"))
lay.addWidget(b2)

# 3. Deshabilitado hasta que algo ocurra
b3 = QPushButton("Enviar"); b3.setEnabled(False)
lay.addWidget(b3)

w.show(); sys.exit(app.exec())
```

## Personalizar

Para cambiar **apariencia**, casi siempre basta QSS (ver [[estilado/index|estilado]]), sin subclasear:

```python
boton.setStyleSheet("QPushButton { background: #5e81ac; border-radius: 6px; padding: 6px; }")
```

Para un boton con **comportamiento o dibujo propio** (forma no rectangular, animacion), se subclasea `QAbstractButton` y se sobreescribe `paintEvent` — ver [[widget_personalizado]].

## Errores comunes

| Error | Causa | Solucion |
|-------|-------|----------|
| El slot se ejecuta al crear el boton, no al pulsar | conectaste `clicked.connect(self.f())` con parentesis | quita los `()`: `clicked.connect(self.f)` |
| Mi slot recibe un `False` inesperado | `clicked` emite el argumento `checked` (bool) | usa un `lambda: ...` que lo ignore, o acepta el parametro |
| `setChecked`/`toggled` no hacen nada | el boton no es checkable | llama antes a `setCheckable(True)` |

## Notas relacionadas

- [[QAbstractButton]] — la clase base que aporta texto, icono y las senales
- [[concepto_signals_slots]] — como conectar `clicked` a un slot
- [[QWidget]] — de donde vienen `show`, `setEnabled` y el resto
