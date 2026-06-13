---
title: QtWidgets/contenedores — agrupar y organizar widgets
tags: [pyqt6, indice]
draft: false
---

# QtWidgets/contenedores — agrupar y organizar widgets

Esta carpeta agrupa los widgets cuyo proposito es **contener y organizar** a otros, no mostrar un dato propio. Un contenedor da estructura visual a la interfaz: un **marco** o separador (`QFrame`), una **agrupacion con titulo** (`QGroupBox`), **pestanas** con solapas (`QTabWidget`), una **pila** que muestra una pagina a la vez sin solapas (`QStackedWidget`), un area con **scroll** para contenido grande (`QScrollArea`) o paneles **redimensionables** por un divisor (`QSplitter`). Todos son [[QWidget]] de pleno derecho: se dibujan y se colocan en un layout como cualquier otro, pero su contenido son mas widgets.

## En accion

Un `QTabWidget` con dos pestanas, cada una con su propio layout y sus widgets:

```python
from PyQt6.QtWidgets import (
    QApplication, QTabWidget, QWidget, QVBoxLayout, QLabel,
    QLineEdit, QPushButton
)
import sys

app = QApplication(sys.argv)

tabs = QTabWidget()
tabs.setWindowTitle("contenedores en accion")

# pestana 1: un formulario simple
pagina_perfil = QWidget()
lay_perfil = QVBoxLayout(pagina_perfil)
lay_perfil.addWidget(QLabel("Nombre:"))
lay_perfil.addWidget(QLineEdit())
lay_perfil.addWidget(QPushButton("Guardar"))
tabs.addTab(pagina_perfil, "Perfil")

# pestana 2: otro widget contenedor con su layout
pagina_acerca = QWidget()
lay_acerca = QVBoxLayout(pagina_acerca)
lay_acerca.addWidget(QLabel("App de ejemplo v1.0"))
tabs.addTab(pagina_acerca, "Acerca de")

tabs.show()
sys.exit(app.exec())                        # PyQt6: exec() sin guion bajo
```

## Herencia

```mermaid
classDiagram
    QWidget <|-- QFrame
    QWidget <|-- QGroupBox
    QWidget <|-- QTabWidget
    QFrame <|-- QSplitter
    QFrame <|-- QStackedWidget
    QFrame <|-- QAbstractScrollArea
    QAbstractScrollArea <|-- QScrollArea
    class QWidget { +show() +setEnabled() }
    class QFrame { +setFrameShape() +setLineWidth() }
    class QGroupBox { +setTitle() +setCheckable() }
    class QTabWidget { +addTab() +currentChanged }
    class QSplitter { +addWidget() +setSizes() }
    class QStackedWidget { +addWidget() +setCurrentIndex() }
    class QAbstractScrollArea { +viewport() }
    class QScrollArea { +setWidget() +setWidgetResizable() }
```

Casi todos cuelgan de `QFrame` (heredan su marco): `QSplitter`, `QStackedWidget` y `QAbstractScrollArea` —de la que sale `QScrollArea`—. `QGroupBox` y `QTabWidget`, en cambio, cuelgan directos de [[QWidget]]: tienen su propio dibujo (el titulo, la barra de solapas) y no necesitan el marco de `QFrame`.

## Que contenedor uso

```mermaid
flowchart TD
    Q{"que necesito?"} --> B["borde o separador simple"]
    Q --> A["agrupar con un titulo"]
    Q --> P["varias secciones navegables"]
    Q --> S["scroll para contenido grande"]
    Q --> R["paneles que el usuario redimensiona"]
    P --> P1{"con solapas visibles?"}
    P1 --> SI["si: el usuario pulsa"]
    P1 --> NO["no: cambio por codigo"]

    B --> FR["QFrame"]
    A --> GB["QGroupBox"]
    SI --> TW["QTabWidget"]
    NO --> SW["QStackedWidget"]
    S --> SA["QScrollArea"]
    R --> SP["QSplitter"]

    classDef pregunta fill:#5e81ac,stroke:#88c0d0,stroke-width:2px,color:#eceff4;
    classDef grupo fill:#3b4252,stroke:#81a1c1,stroke-width:1.5px,color:#88c0d0;
    classDef hoja fill:#2e3440,stroke:#a3be8c,color:#d8dee9;
    class Q,P1 pregunta;
    class B,A,P,S,R,SI,NO grupo;
    class FR,GB,TW,SW,SA,SP hoja;
```

## Las clases

| Clase | Hereda de | Rol |
|-------|-----------|-----|
| [[QFrame]] | `QWidget` | marco/borde y separador; base visual de muchos contenedores |
| [[QGroupBox]] | `QWidget` | agrupa widgets bajo un **titulo** (con marco), opcionalmente checkable |
| [[QTabWidget]] | `QWidget` | **pestanas** con solapas; cada una muestra un widget distinto |
| [[QStackedWidget]] | `QFrame` | **pila** de paginas; muestra una a la vez, **sin** solapas (cambio por codigo) |
| [[QScrollArea]] | `QAbstractScrollArea` | area con **barras de desplazamiento** para contenido grande |
| [[QSplitter]] | `QFrame` | paneles separados por un divisor que el usuario **redimensiona** |

## Notas relacionadas

- [[QWidget]] — el contenedor base del que parten todos
- [[concepto_layouts]] — los layouts que colocan a los widgets dentro de cada contenedor
