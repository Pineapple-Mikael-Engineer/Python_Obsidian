---
title: manejar eventos — sobreescribir manejadores y filtrar con eventFilter
aliases: [eventos personalizados, sobreescribir mousePressEvent, eventFilter, manejar teclado]
tags: [pyqt6, patron, gui]
lib: pyqt6
tipo: patron
requiere: [concepto_sistema_eventos, QMouseEvent]
draft: false
---

# manejar eventos — sobreescribir manejadores y filtrar con eventFilter

Hay dos grandes modos de extender Qt. Uno son las **senales** (notificaciones de alto nivel que conectas con `.connect`). El otro, el que aqui nos ocupa, es interceptar los **eventos** que el framework manda a un widget —raton, teclado, foco, cierre, repintado— **sobreescribiendo su manejador**. Es la via para los casos en que no existe una senal que sirva: detectar la posicion exacta de cada clic, reaccionar a una tecla concreta, vetar el cierre de la ventana. La idea es directa: cada tipo de evento tiene su **manejador virtual** ([[QMouseEvent]] llega a `mousePressEvent`, el teclado a `keyPressEvent`, etc.); tu lo sobreescribes en una subclase y Qt lo llama por ti cuando ese evento ocurre. Esta nota es la receta detallada del patron que [[concepto_sistema_eventos]] introduce.

## La receta minima

El widget mas corto que reacciona a un evento: una subclase de `QWidget` que sobreescribe `mousePressEvent` y lee **donde** se pulso (`e.position()`) y **que boton** (`e.button()`). Es ejecutable tal cual.

```python
from PyQt6.QtWidgets import QApplication, QWidget
from PyQt6.QtCore import Qt
import sys

class Lienzo(QWidget):
    def mousePressEvent(self, e):
        print("clic en:", e.position())      # QPointF local al widget
        if e.button() == Qt.MouseButton.LeftButton:
            print("boton izquierdo")

app = QApplication(sys.argv)
w = Lienzo()
w.resize(300, 200)
w.show()
sys.exit(app.exec())
```

Eso es todo lo imprescindible: heredar y sobreescribir el manejador del evento que te interesa. Tu no llamas a `mousePressEvent`; lo invoca el event loop cuando se pulsa el raton sobre el widget. A partir de aqui solo se anaden capas.

## Construccion paso a paso

### 1. Sobreescribir un manejador concreto

Cada evento tiene su manejador con un **nombre fijo**: lo sobreescribes en una subclase y Qt lo llama. Los habituales:

| Manejador a sobreescribir | Cuando se llama | Evento que recibe |
|---------------------------|-----------------|-------------------|
| `mousePressEvent(self, e)` | se pulsa un boton del raton | `QMouseEvent` |
| `mouseMoveEvent(self, e)` | se mueve el raton (con boton pulsado por defecto) | `QMouseEvent` |
| `keyPressEvent(self, e)` | se pulsa una tecla (con el foco) | `QKeyEvent` |
| `wheelEvent(self, e)` | se gira la rueda del raton | `QWheelEvent` |
| `resizeEvent(self, e)` | cambia el tamano del widget | `QResizeEvent` |
| `closeEvent(self, e)` | se pide cerrar la ventana | `QCloseEvent` |
| `paintEvent(self, e)` | hay que repintar el widget | `QPaintEvent` |

El catalogo completo de eventos y sus clases esta en [[PyQt6/QtGui/eventos/index|eventos]]. La regla comun: el manejador recibe un objeto evento como unico argumento y de el lees los datos (`position()`, `key()`, `size()`...).

### 2. Teclado: setFocusPolicy

Un widget **no recibe eventos de teclado si no tiene el foco**, y un `QWidget` plano no lo toma por defecto. Hay que pedirlo explicitamente en `__init__`:

```python
from PyQt6.QtWidgets import QWidget
from PyQt6.QtCore import Qt

class Editor(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        # sin esto, keyPressEvent NO se llama nunca
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)

    def keyPressEvent(self, e):
        # las teclas especiales se comparan con key(), no con text()
        if e.key() == Qt.Key.Key_Escape:
            self.close()
        elif e.key() == Qt.Key.Key_Left:
            print("flecha izquierda")
        elif e.key() == Qt.Key.Key_Right:
            print("flecha derecha")
        else:
            super().keyPressEvent(e)        # el resto, al base
```

Las teclas sin caracter (flechas, Esc, F1...) tienen `text()` vacio: se distinguen siempre por `e.key()` contra la enum `Qt.Key` (ver [[QKeyEvent]]). `StrongFocus` significa que el widget acepta foco por clic y por tabulador.

### 3. accept() / ignore(): controlar la propagacion

Cada evento puede marcarse como **atendido** (`e.accept()`, lo consumo y no se propaga) o **rechazado** (`e.ignore()`, que suba al widget padre para que lo gestione el). En manejadores normales (raton, teclado) muchas veces no hace falta tocarlo, pero en `closeEvent` es la pieza clave: `e.ignore()` **cancela el cierre** de la ventana.

```python
from PyQt6.QtWidgets import QWidget, QMessageBox

class Ventana(QWidget):
    def closeEvent(self, e):
        resp = QMessageBox.question(
            self, "Salir", "¿Cerrar la aplicacion?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
        )
        if resp == QMessageBox.StandardButton.Yes:
            e.accept()          # se cierra
        else:
            e.ignore()          # se cancela: la ventana sigue abierta
```

`accept()`/`ignore()` lo aporta [[QEvent]], asi que esta disponible en cualquier evento. En `closeEvent`, `ignore()` veta el cierre; en eventos de input, decide si el padre llega a verlos.

### 4. super(): cuando NO manejas el evento

Si sobreescribes un manejador pero **no quieres consumir** todos los casos, debes delegar lo no tratado al base con `super().<manejador>(e)`. Si no lo haces, te cargas el **comportamiento por defecto** del widget. El caso clasico: una subclase de `QLineEdit` que solo quiere atrapar Enter pero **dejar que el resto siga escribiendo**.

```python
from PyQt6.QtWidgets import QLineEdit
from PyQt6.QtCore import Qt

class CampoBusqueda(QLineEdit):
    def keyPressEvent(self, e):
        if e.key() == Qt.Key.Key_Return:
            print("buscar:", self.text())
            return                      # consumo el Enter
        super().keyPressEvent(e)        # el resto: que el QLineEdit escriba normal
```

Sin la linea `super().keyPressEvent(e)`, el campo no escribiria **ninguna** letra: las habrias interceptado todas sin pasarselas al `QLineEdit`. La regla es: **consumes lo que reconoces, delegas lo demas al base**.

## event(): el despachador

Todos los eventos pasan **antes** por un unico metodo, `event(self, e)`, que es quien **despacha** cada `QEvent` al manejador especifico segun su tipo. Normalmente no lo tocas: sobreescribes el manejador concreto y listo. Pero `event()` sirve para casos que **no tienen manejador propio** o que los manejadores normales no reciben. El ejemplo tipico es el **Tab**: Qt lo intercepta para mover el foco antes de que llegue a `keyPressEvent`, asi que para "verlo" hay que capturarlo en `event()`.

```python
from PyQt6.QtWidgets import QWidget
from PyQt6.QtCore import QEvent, Qt

class Panel(QWidget):
    def event(self, e):
        if e.type() == QEvent.Type.KeyPress and e.key() == Qt.Key.Key_Tab:
            print("Tab interceptado aqui")
            return True                 # consumido
        return super().event(e)         # SIEMPRE: lo no manejado, al base
```

La regla de oro de `event()`: comprueba con `e.type()` (enum `QEvent.Type`, con scope en Qt6) **solo** lo que te interesa y devuelve `True` si lo consumes; para **todo lo demas** retorna `super().event(e)`. Si te olvidas de ese `super`, el widget deja de despachar el resto de eventos y queda inservible. Prefiere siempre el manejador especifico; reserva `event()` para lo que no llega de otro modo.

## eventFilter: interceptar SIN subclasear

A veces quieres vigilar los eventos de **otro** widget sin heredar de el —porque es un widget de terceros, porque quieres filtrar varios a la vez, o simplemente para no crear una subclase. Ese es el patron potente: instalas un **filtro de eventos** con `objeto.installEventFilter(self)` y defines `eventFilter(self, obj, e)`. A partir de ahi, los eventos de `objeto` pasan **primero** por tu filtro. Devuelves `True` para **consumirlo** (no llega al widget) o `False` para **dejarlo pasar** (sigue su curso normal).

En este ejemplo, una ventana vigila un `QLineEdit` ajeno: intercepta el **Enter** para hacer algo propio (en vez de dejar que salte de campo) y detecta cuando el raton **entra y sale** (hover) del campo. El `QLineEdit` no se subclasea en ningun momento.

```python
from PyQt6.QtWidgets import QApplication, QWidget, QLineEdit, QVBoxLayout, QLabel
from PyQt6.QtCore import QEvent
import sys

class Ventana(QWidget):
    def __init__(self):
        super().__init__()
        self.campo = QLineEdit()
        self.estado = QLabel("escribe y pulsa Enter")
        layout = QVBoxLayout(self)
        layout.addWidget(self.campo)
        layout.addWidget(self.estado)

        # instalar el filtro: los eventos del campo pasaran por self.eventFilter
        self.campo.installEventFilter(self)

    def eventFilter(self, obj, e):
        if obj is self.campo:
            if e.type() == QEvent.Type.KeyPress and e.key() == 0x01000004:  # Enter
                self.estado.setText(f"buscando: {self.campo.text()}")
                return True             # consumido: el Enter no hace nada mas
            if e.type() == QEvent.Type.Enter:
                self.estado.setText("(raton dentro del campo)")
            elif e.type() == QEvent.Type.Leave:
                self.estado.setText("(raton fuera)")
        return super().eventFilter(obj, e)   # lo no consumido sigue su curso

app = QApplication(sys.argv)
w = Ventana()
w.resize(320, 120)
w.show()
sys.exit(app.exec())
```

Dos claves: el filtro comprueba `obj is self.campo` para actuar solo sobre el widget vigilado, y devuelve `True` **solo** cuando de verdad consume el evento (el Enter); para el hover deja pasar (cae al `return super().eventFilter(...)`, que vale `False`). Un mismo filtro puede instalarse en varios widgets a la vez y discriminar por `obj`.

> [!tip] Comparar el tipo del evento
> En el filtro recibes un `QEvent` generico, asi que filtras por `e.type()` contra la
> enum `QEvent.Type` (con scope en Qt6: `QEvent.Type.KeyPress`, `QEvent.Type.Enter`).
> Para los eventos de raton/teclado puedes anotar o castear al tipo concreto y usar sus
> metodos (`key()`, `position()`), igual que en un manejador.

## Ejemplo completo

Un panel interactivo que combina varios mecanismos: **arrastrar** una caja con `mousePressEvent` + `mouseMoveEvent` (guarda el punto inicial y mueve un rectangulo), responder al **teclado** (necesita foco) para reiniciar con Escape, y un `closeEvent` con **confirmacion**. Es ejecutable tal cual.

```python
from PyQt6.QtWidgets import QApplication, QWidget, QMessageBox
from PyQt6.QtGui import QPainter, QColor
from PyQt6.QtCore import Qt, QRect, QPoint
import sys

class PanelArrastre(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)   # para recibir teclado
        self._caja = QRect(40, 40, 100, 60)               # estado: la caja
        self._origen = None                               # punto inicial del arrastre

    # --- raton: empezar a arrastrar ---
    def mousePressEvent(self, e):
        if e.button() == Qt.MouseButton.LeftButton and \
                self._caja.contains(e.position().toPoint()):
            self._origen = e.position().toPoint() - self._caja.topLeft()
            e.accept()

    # --- raton: mover mientras se arrastra ---
    def mouseMoveEvent(self, e):
        if self._origen is not None:
            nueva = e.position().toPoint() - self._origen
            self._caja.moveTopLeft(nueva)
            self.update()                                 # repinta en la nueva posicion

    def mouseReleaseEvent(self, e):
        self._origen = None                               # fin del arrastre

    # --- teclado: Escape reinicia la posicion ---
    def keyPressEvent(self, e):
        if e.key() == Qt.Key.Key_Escape:
            self._caja.moveTopLeft(QPoint(40, 40))
            self.update()
        else:
            super().keyPressEvent(e)

    # --- dibujo ---
    def paintEvent(self, e):
        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)
        p.fillRect(self.rect(), QColor("#2e3440"))
        p.setBrush(QColor("#88c0d0"))
        p.drawRect(self._caja)

    # --- cierre con confirmacion ---
    def closeEvent(self, e):
        resp = QMessageBox.question(self, "Salir", "¿Cerrar la ventana?")
        if resp == QMessageBox.StandardButton.Yes:
            e.accept()
        else:
            e.ignore()

app = QApplication(sys.argv)
w = PanelArrastre()
w.resize(320, 240)
w.show()
sys.exit(app.exec())
```

Arrastra la caja con el boton izquierdo, pulsa Escape para devolverla a su sitio e intenta cerrar la ventana: el `closeEvent` pregunta y `ignore()` cancela si dices que no. Cada mecanismo es independiente, pero conviven en el mismo widget.

## Buenas practicas

1. **Prefiere SENALES si existe una que sirva.** Sobreescribir un evento es para control fino (la posicion del clic, una tecla concreta, vetar el cierre); si te basta reaccionar a "algo paso" (`clicked`, `valueChanged`), conecta la senal y no toques eventos.
2. **Sobreescribe el manejador ESPECIFICO antes que `event()`.** `mousePressEvent`, `keyPressEvent`, `closeEvent`... son mas claros y directos. Reserva `event()` para lo que esos manejadores no reciben (como el Tab).
3. **Llama a `super().<manejador>(e)` cuando NO consumes el evento.** Si no, te cargas el comportamiento por defecto del widget (un `QLineEdit` dejaria de escribir). Consumes lo que reconoces, delegas el resto al base.
4. **`setFocusPolicy(Qt.FocusPolicy.StrongFocus)` para recibir teclado.** Un `QWidget` plano no toma el foco por defecto y `keyPressEvent` no se llama nunca. Es el olvido numero uno con el teclado.
5. **Usa `eventFilter` para no subclasear.** Es el camino cuando quieres vigilar un widget de terceros, varios widgets a la vez, o no te interesa crear una subclase. `obj.installEventFilter(self)` + `def eventFilter(self, obj, e)`.
6. **En `eventFilter` devuelve `True` solo si REALMENTE consumes** el evento; para todo lo demas, `return super().eventFilter(obj, e)` (que deja pasar). Devolver `True` por error "se traga" eventos y rompe al widget vigilado.
7. **Usa `accept()` / `ignore()` conscientemente** para la propagacion. En `closeEvent`, `ignore()` cancela el cierre; en eventos de input, decide si el widget padre llega a verlos.
8. **Respeta la firma EXACTA del manejador.** Un nombre mal escrito (`mousepressEvent`, `keyPress`) no es un error: simplemente Qt nunca llama a tu metodo y crees que "no funciona".
9. **No hagas trabajo pesado en `mouseMoveEvent` / `resizeEvent`.** Se disparan muchisimas veces; precalcula lo costoso al cambiar el estado, no en cada disparo, y usa `update()` (que agrupa repintados) en vez de `repaint()`.
10. **En Qt6 usa `e.position()`, no `pos()`.** `pos()` quedo obsoleto; `position()` devuelve `QPointF` (con decimales). Para un entero: `e.position().toPoint()`. Y recuerda los enums con scope (`Qt.MouseButton.LeftButton`, `QEvent.Type.KeyPress`).

## Errores comunes

| Error | Causa | Solucion |
|-------|-------|----------|
| El manejador "no se llama nunca" | la firma esta mal escrita (`mousepressEvent`, args distintos) | respeta el nombre y la firma exactos, ej. `mousePressEvent(self, e)` |
| El widget pierde su comportamiento normal | sobreescribiste el manejador y olvidaste `super().<manejador>(e)` | delega al base lo que no consumes; un `QLineEdit` necesita el `super` para escribir |
| El teclado no llega al widget | falta `setFocusPolicy`; un `QWidget` plano no toma foco | `self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)` en `__init__` |
| El `eventFilter` no filtra | no llamaste a `installEventFilter`, o no devuelves un `bool` correcto | instala el filtro y retorna `True` (consume) / `False` (pasa) segun el caso |
| El `event()` rompe el widget | te olvidaste de `return super().event(e)` para lo no manejado | comprueba solo lo tuyo y delega el resto con `super().event(e)` |
| Aviso o `AttributeError` con `e.pos()` | en Qt6 `pos()` quedo obsoleto | usa `e.position()` (`QPointF`); para entero `.toPoint()` |
| Comparas con `Qt.LeftButton` o `QEvent.KeyPress` y falla | en Qt6 los enums tienen scope | usa el enum completo: `Qt.MouseButton.LeftButton`, `QEvent.Type.KeyPress` |

## Notas relacionadas

- [[concepto_sistema_eventos]] — el concepto base: como Qt despacha cada evento al manejador
- [[QMouseEvent]] — el evento de raton que llega a `mousePressEvent` / `mouseMoveEvent`
- [[QKeyEvent]] — el evento de teclado que llega a `keyPressEvent`
- [[QCloseEvent]] — el evento de cierre donde `accept()`/`ignore()` veta la salida
- [[QEvent]] — la clase base de todos los eventos; aporta `type()`, `accept()`, `ignore()`
