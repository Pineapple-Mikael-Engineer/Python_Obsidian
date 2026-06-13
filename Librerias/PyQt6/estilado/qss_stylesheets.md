---
title: QSS — dar estilo a los widgets con hojas de estilo
aliases: [QSS, stylesheet, setStyleSheet, hoja de estilo Qt]
tags: [pyqt6, estilado, gui]
lib: pyqt6
tipo: concepto
requiere: [QWidget, QApplication]
draft: false
---

# QSS — dar estilo a los widgets con hojas de estilo

QSS (Qt Style Sheets) es el sistema para cambiar la **apariencia** de los widgets con una sintaxis muy parecida a CSS, sin subclasear ni sobreescribir `paintEvent`. Es la via recomendada para colores, bordes, fondos, padding y fuentes: con una cadena de texto le dices a Qt "los botones se ven asi, las cajas de texto asi". Para un dibujo totalmente propio (una forma no rectangular, un medidor animado) se subclasea ([[widget_personalizado]]), pero para "que se vea bonito" basta QSS.

## Aplicar una hoja de estilo: setStyleSheet

Toda hoja se aplica con `widget.setStyleSheet("...")`. Lo que cambia es el **alcance**: a quien afecta esa hoja. Hay tres niveles, y la regla de **cascada** es que la hoja mas especifica/cercana al widget gana sobre la mas general.

```python
# 1) a un widget concreto: solo a ese boton
boton.setStyleSheet("background: #5e81ac;")

# 2) a un contenedor y sus HIJOS: la hoja se hereda hacia abajo
#    aqui el ventana estiliza todos los QPushButton que contiene
ventana.setStyleSheet("QPushButton { background: #5e81ac; }")

# 3) a TODA la app: el tema global, sobre la QApplication
app.setStyleSheet("QPushButton { background: #5e81ac; }")
```

- **A un widget concreto**: la hoja afecta solo a ese widget (y a sus hijos, si los tiene).
- **A un contenedor**: aplicada a una ventana o a un widget con layout, la hoja se hereda hacia abajo y alcanza a todos sus descendientes.
- **A toda la app**: `app.setStyleSheet(...)` sobre la [[QApplication]] define el tema global de la aplicacion entera.

Si el mismo widget recibe estilo por varias vias, gana el mas cercano: un `boton.setStyleSheet(...)` puntual pisa lo que dijo el tema global de la app para ese boton.

## La sintaxis: selector + propiedades

Una regla QSS es un bloque tipo CSS: un selector seguido de un bloque de propiedades entre llaves.

```css
QPushButton {
    background-color: #5e81ac;
    color: #eceff4;
    border: 1px solid #4c566a;
    border-radius: 6px;
    padding: 6px 12px;
}
```

Su anatomia tiene dos partes:

- **Selector** — a que widgets aplica la regla. Aqui `QPushButton` significa "todos los botones". Hay selectores por clase, por `objectName` (`#id`), por estado (`:hover`, `:disabled`) y por sub-control (`::handle`); se detallan en [[selectores_qss]].
- **Bloque de propiedades** — pares `propiedad: valor;`, uno por linea, cada uno cerrado con `;`.

## Propiedades mas usadas

QSS **no** es CSS completo: solo soporta un subconjunto de propiedades. Las habituales:

| Propiedad | Que controla | Ejemplo |
|-----------|--------------|---------|
| `background-color` / `background` | color o fondo del widget | `background-color: #2e3440;` |
| `color` | color del texto | `color: #eceff4;` |
| `border` | grosor, estilo y color del borde | `border: 1px solid #4c566a;` |
| `border-radius` | redondeo de las esquinas | `border-radius: 6px;` |
| `padding` | espacio interior (texto al borde) | `padding: 6px 12px;` |
| `margin` | espacio exterior alrededor del widget | `margin: 4px;` |
| `font-size` | tamaño de la fuente | `font-size: 14px;` |
| `font-weight` | grosor de la fuente | `font-weight: bold;` |
| `min-width` / `min-height` | tamaño minimo del widget | `min-width: 80px;` |

## Ejemplo completo: una ventana con tema

App ejecutable que aplica un tema coherente (paleta Nord) a toda la aplicacion con `app.setStyleSheet(...)`: estiliza el [[QPushButton]], el `QLineEdit` y el `QLabel` de una sola pasada.

```python
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton
)
import sys

TEMA = """
QWidget {
    background-color: #2e3440;
    color: #eceff4;
    font-size: 14px;
}
QLabel {
    font-weight: bold;
}
QLineEdit {
    background-color: #3b4252;
    border: 1px solid #4c566a;
    border-radius: 4px;
    padding: 6px;
}
QPushButton {
    background-color: #5e81ac;
    color: #eceff4;
    border: none;
    border-radius: 6px;
    padding: 8px 16px;
}
QPushButton:hover {
    background-color: #81a1c1;
}
"""

app = QApplication(sys.argv)
app.setStyleSheet(TEMA)                      # tema global, una sola vez

ventana = QWidget()
ventana.setWindowTitle("Tema con QSS")
lay = QVBoxLayout(ventana)

lay.addWidget(QLabel("Tu nombre:"))
lay.addWidget(QLineEdit())
boton = QPushButton("Aceptar")
boton.clicked.connect(lambda: print("aceptado"))
lay.addWidget(boton)

ventana.show()
sys.exit(app.exec())
```

## Cargar el QSS desde un archivo .qss

En un proyecto real el estilo no vive incrustado en el codigo: se guarda en un archivo `.qss` aparte y se lee al arrancar. Asi separas diseño de logica y puedes cambiar el tema sin tocar Python.

```python
from PyQt6.QtWidgets import QApplication, QPushButton
import sys

app = QApplication(sys.argv)

# leer el archivo de estilo y aplicarlo a toda la app
with open("tema.qss", "r", encoding="utf-8") as f:
    app.setStyleSheet(f.read())

boton = QPushButton("Pulsame")
boton.show()
sys.exit(app.exec())
```

El archivo `tema.qss` contiene exactamente los mismos bloques `selector { ... }` que pasarias como cadena:

```css
/* tema.qss */
QPushButton {
    background-color: #5e81ac;
    border-radius: 6px;
    padding: 8px 16px;
}
```

## Buenas practicas

1. Prefiere **QSS antes que subclasear** para todo lo que sea apariencia (color, borde, fondo): es mas corto y no toca `paintEvent`.
2. Aplica el **tema global en la `QApplication`** una sola vez, y afina los casos puntuales por widget; no repitas el tema entero en cada widget.
3. Separa el QSS en un **archivo `.qss`** y cargalo con `open(...).read()`: el diseño deja de ensuciar el codigo Python.
4. Para casos unicos usa `objectName` con un selector `#id` en vez de repetir estilos inline (ver [[selectores_qss]]); asi un solo widget tiene su regla sin afectar al resto.
5. No abuses de `setStyleSheet` inline por widget: muchas hojas pequeñas dispersas son dificiles de mantener; centraliza el estilo.
6. Recuerda que QSS es un **subconjunto de CSS**: no des por hecho que cualquier propiedad de CSS funciona, muchas no estan soportadas.
7. Ojo con los **sub-controles**: algunas propiedades obligan a estilizar tambien partes internas (`::handle` de un slider, `::drop-down` de un combo) o el widget se rompe visualmente.
8. Mide el **coste**: hojas enormes aplicadas a miles de widgets pueden notarse; manten el QSS acotado y limpio.

## Errores comunes

| Error | Causa | Solucion |
|-------|-------|----------|
| La propiedad se ignora a partir de cierta linea | olvidaste el `;` final de una propiedad | cierra cada `propiedad: valor;` con punto y coma |
| Una propiedad "no hace nada" y no salta error | usaste una propiedad CSS no soportada por QSS | usa solo el subconjunto soportado (ver tabla) |
| Estilizas un `QSlider` y desaparece el handle | al estilizar el slider hay que estilizar su sub-control | añade tambien una regla para `QSlider::handle` |
| El selector `#id` no aplica | nunca llamaste a `setObjectName` en ese widget | `widget.setObjectName("id")` antes del QSS |
| El estilo no se hereda a los hijos | aplicaste la hoja a un hijo, no al padre/contenedor | aplica `setStyleSheet` al padre o a la `QApplication` |

## Notas relacionadas

- [[selectores_qss]] — selectores por clase, `#id`, estado (`:hover`) y sub-control (`::handle`)
- [[QApplication]] — donde se aplica el tema global de toda la app
- [[QWidget]] — el `setStyleSheet` que toda nota de widget hereda
- [[widget_personalizado]] — cuando QSS no basta y hay que subclasear y dibujar
