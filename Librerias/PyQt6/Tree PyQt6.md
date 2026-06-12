---
title: Tree PyQt6
tags:
  - pyqt6
  - meta
draft: true
---

# 🌳 Tree PyQt6

> Organizacion **jerarquica por modulo de Qt** (`QtCore`, `QtGui`, `QtWidgets`) cruzada con
> tematicas. PyQt6 es la libreria mas **orientada a objetos** del vault: todo hereda de
> `QObject` (rama no visual) o de `QWidget` (rama visual), la comunicacion va por **senales
> y slots**, y personalizar = **subclasear y sobreescribir**. Por eso la **herencia** es dato
> de primera clase (campo `hereda_de` en el frontmatter + `classDiagram` en cada index).
> `✅` = nota creada · sin marca = roadmap pendiente.

---

## 📁 Tipos de notas

| Tipo | Ubicacion | Ejemplo |
|------|-----------|---------|
| **Concepto transversal** | `conceptos_transversales/` | `concepto_signals_slots.md` |
| **Clase base** | `<modulo>/` | `QObject.md`, `QWidget.md` |
| **Clase concreta** | `<modulo>/<tematica>/` | `QtWidgets/botones/QPushButton.md` |
| **Patron POO (receta)** | `patrones/` | `widget_personalizado.md` |
| **Indice de carpeta** | `index.md` | nota madre con `classDiagram` de su rama |

> Naming API-style con el **nombre real de la clase** (`QPushButton.md`), respetando mayusculas.

---

## 📂 Estructura completa (nucleo desktop)

```tree
PyQt6/
│
├── index.md                              # modelo Qt + classDiagram global QObject -> QWidget -> ...
│
├── 📁 conceptos_transversales/            # el modelo mental (lo mas importante en Qt)
│   ├── concepto_qobject_arbol.md         # QObject, parent/child, ownership y memoria
│   ├── concepto_signals_slots.md         # senales y slots: la columna vertebral
│   ├── concepto_event_loop.md            # QApplication.exec(): el bucle de eventos
│   ├── concepto_sistema_eventos.md       # QEvent, event(), eventFilter, override de *Event
│   ├── concepto_herencia_widgets.md      # subclasear para personalizar (el patron clave)
│   ├── concepto_propiedades.md           # property system, pyqtProperty
│   ├── concepto_layouts.md               # gestion geometrica de widgets
│   └── concepto_model_view.md            # arquitectura Modelo/Vista
│
├── 📁 QtCore/                             # base NO visual; raiz de la comunicacion
│   ├── QObject.md                        # la clase raiz: parent/child, senales, propiedades, eventos
│   ├── pyqtProperty.md                   # @pyqtProperty: definir una propiedad Qt (DECORADOR)
│   ├── 📁 senales/
│   │   ├── pyqtSignal.md                 # declarar una senal propia (factory, atributo de clase)
│   │   ├── connect.md                    # conectar senal -> slot (y disconnect)
│   │   ├── pyqtSlot.md                   # @pyqtSlot: marcar un metodo como slot (DECORADOR)
│   │   └── emit.md                       # emitir una senal
│   ├── 📁 temporizadores/
│   │   ├── QTimer.md
│   │   └── QElapsedTimer.md
│   ├── 📁 hilos/
│   │   ├── QThread.md
│   │   ├── QRunnable.md
│   │   └── QThreadPool.md
│   └── 📁 utilidades/
│       ├── QSettings.md
│       ├── QSize_QPoint_QRect.md         # geometria basica
│       ├── QDateTime.md
│       └── QUrl.md
│
├── 📁 QtWidgets/                          # los widgets de escritorio
│   ├── QApplication.md                   # la app + el event loop (exec)
│   ├── QWidget.md                        # CLASE BASE de todo widget (geometria, eventos, pintado)
│   ├── 📁 ventanas/
│   │   ├── QMainWindow.md                # ventana con menus, toolbars, statusbar, dock
│   │   ├── QDialog.md
│   │   ├── QMessageBox.md
│   │   └── QFileDialog.md
│   ├── 📁 botones/
│   │   ├── QAbstractButton.md            # base de los botones
│   │   ├── QPushButton.md
│   │   ├── QToolButton.md
│   │   ├── QCheckBox.md
│   │   └── QRadioButton.md
│   ├── 📁 entradas/
│   │   ├── QLineEdit.md
│   │   ├── QTextEdit.md
│   │   ├── QPlainTextEdit.md
│   │   ├── QSpinBox.md
│   │   ├── QDoubleSpinBox.md
│   │   ├── QComboBox.md
│   │   └── QSlider.md
│   ├── 📁 muestra/
│   │   ├── QLabel.md
│   │   ├── QProgressBar.md
│   │   └── QLCDNumber.md
│   ├── 📁 contenedores/
│   │   ├── QFrame.md
│   │   ├── QGroupBox.md
│   │   ├── QTabWidget.md
│   │   ├── QStackedWidget.md
│   │   ├── QScrollArea.md
│   │   └── QSplitter.md
│   ├── 📁 layouts/
│   │   ├── QLayout.md                    # base de los layouts
│   │   ├── QBoxLayout.md
│   │   ├── QVBoxLayout.md
│   │   ├── QHBoxLayout.md
│   │   ├── QGridLayout.md
│   │   └── QFormLayout.md
│   ├── 📁 vistas/                         # Modelo/Vista
│   │   ├── QAbstractItemView.md          # base de las vistas
│   │   ├── QListView.md
│   │   ├── QListWidget.md
│   │   ├── QTableView.md
│   │   ├── QTableWidget.md
│   │   ├── QTreeView.md
│   │   └── QTreeWidget.md
│   └── 📁 menus/
│       ├── QMenuBar.md
│       ├── QMenu.md
│       ├── QToolBar.md
│       └── QStatusBar.md
│
├── 📁 QtGui/                              # bajo nivel grafico
│   ├── 📁 pintura/
│   │   ├── QPainter.md
│   │   ├── QColor.md
│   │   ├── QPen.md
│   │   ├── QBrush.md
│   │   └── QPainterPath.md
│   ├── 📁 recursos/
│   │   ├── QPixmap.md
│   │   ├── QImage.md
│   │   ├── QIcon.md
│   │   └── QFont.md
│   ├── 📁 eventos/
│   │   ├── QEvent.md                     # base de todos los eventos
│   │   ├── QMouseEvent.md
│   │   ├── QKeyEvent.md
│   │   ├── QPaintEvent.md
│   │   ├── QResizeEvent.md
│   │   ├── QCloseEvent.md
│   │   └── QWheelEvent.md
│   └── 📁 acciones/                       # en Qt6 viven en QtGui
│       ├── QAction.md
│       ├── QShortcut.md
│       └── QKeySequence.md
│
├── 📁 patrones/                           # recetas POO (herencia y personalizacion)
│   ├── widget_personalizado.md           # subclasear QWidget + paintEvent + sizeHint
│   ├── senal_personalizada.md            # definir y emitir una pyqtSignal propia
│   ├── dialogo_personalizado.md          # subclasear QDialog (formulario reutilizable)
│   ├── modelo_personalizado.md           # subclasear QAbstractTableModel
│   └── eventos_personalizados.md         # override de mousePressEvent/keyPressEvent/eventFilter
│
└── 📁 estilado/                           # apariencia (QSS)
    ├── qss_stylesheets.md                # setStyleSheet, sintaxis QSS
    └── selectores_qss.md                 # selectores, propiedades, estados (:hover, :checked)
```

---

## 📊 Roadmap (estado de implementacion)

> Rama **limpia** creada desde el commit de skills (`8e98b49`), sin notas de otras librerias.
> Nucleo desktop primero; los modulos avanzados quedan como roadmap marcado abajo.

| Bloque | Notas (aprox.) | Prioridad |
|--------|:---:|-----------|
| `conceptos_transversales/` | 8 | 🔴 primero (modelo mental POO) |
| `QtCore/` (QObject + senales + timers + hilos + utils) | ~15 | 🔴 base de todo |
| `QtWidgets/` (QApplication, QWidget + widgets + layouts + ventanas + vistas) | ~40 | 🟠 el grueso |
| `QtGui/` (pintura + recursos + eventos + acciones) | ~19 | 🟠 necesario para personalizar |
| `patrones/` | 5 | 🟡 lo que distingue saber Qt |
| `estilado/` | 2 | 🟢 apariencia |

### Orden sugerido de relleno

1. **`conceptos_transversales`** + `index.md` — QObject, senales/slots, event loop, herencia.
2. **`QtCore/QObject`** + `senales/` — la raiz y la comunicacion.
3. **`QtWidgets/QWidget`** + `QApplication` + `layouts/` + `ventanas/` — el esqueleto de una app.
4. **`QtWidgets`** widgets concretos (botones, entradas, muestra, contenedores).
5. **`QtGui/eventos`** + **`patrones/widget_personalizado`** — crear widgets propios (lo clave).
6. **`QtGui`** pintura/recursos, **`vistas/`** (Modelo/Vista), `estilado/`.

### Roadmap futuro (fuera del nucleo desktop)

Modulos avanzados a documentar despues, cada uno en su carpeta `QtXxx/`:

- **QtCharts** — graficos integrados en apps Qt
- **QtNetwork** — red (QTcpSocket, QNetworkAccessManager)
- **QtSql** — bases de datos (QSqlDatabase, modelos SQL)
- **QtMultimedia** — audio/video
- **QtWebEngineWidgets** — navegador embebido
- **QtPrintSupport** — impresion
- **QtConcurrent** — paralelismo de alto nivel

---

## Notas relacionadas

- [[Reglas PyQt6]]
- [[Estandarizan Directorio Librerias]]
