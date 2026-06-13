---
title: widget personalizado — subclasear QWidget y dibujarse a si mismo
aliases: [widget personalizado, subclasear QWidget, paintEvent, widget propio]
tags: [pyqt6, patron, gui]
lib: pyqt6
tipo: patron
requiere: [concepto_herencia_widgets, QPainter]
draft: false
---

# widget personalizado — subclasear QWidget y dibujarse a si mismo

Llega un momento en que los widgets que trae la libreria no bastan: necesitas un **indicador** que no existe, un **medidor** circular, un **led**, un **termometro** o un **grafico** propio. La respuesta de Qt no es buscar un widget mas configurable, sino crear el tuyo: heredas de `QWidget` y **sobreescribes los metodos que Qt ya llama por ti** (`paintEvent` para dibujarte, `sizeHint` para declarar tu tamaño, los `*Event` para reaccionar al raton y al teclado). Tu no invocas esos metodos; los invoca el event loop cuando toca. Esta nota es la receta detallada del patron que [[concepto_herencia_widgets]] introduce. Regla de oro que no se negocia: en `__init__` lo **primero** es `super().__init__(parent)`, porque ahi Qt inicializa el objeto C++ subyacente; sin eso, todo lo demas falla.

## La receta minima

El widget propio mas corto que funciona y se ve: una subclase de `QWidget` que solo sobreescribe `paintEvent` y dibuja un circulo con `QPainter`. Es ejecutable tal cual.

```python
from PyQt6.QtWidgets import QApplication, QWidget
from PyQt6.QtGui import QPainter, QColor
import sys

class CirculoWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)                 # SIEMPRE primero

    def paintEvent(self, event):
        painter = QPainter(self)                  # pinta sobre este widget
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setBrush(QColor("#88c0d0"))
        painter.drawEllipse(20, 20, 120, 120)     # circulo relleno
        # el QPainter se cierra solo al destruirse al final del metodo

app = QApplication(sys.argv)
w = CirculoWidget()
w.resize(160, 160)
w.show()
sys.exit(app.exec())
```

Eso es todo lo imprescindible: heredar, llamar a `super().__init__(parent)` y dibujar en `paintEvent`. A partir de aqui solo se añaden capas.

## Construccion paso a paso

### 1. El esqueleto

`__init__` hace dos cosas: llamar a `super().__init__(parent)` (obligatorio y lo primero) y **guardar el estado** del widget en atributos. El estado es lo que el widget "sabe" de si mismo: un valor, un color, un flag de encendido. No se dibuja nada aqui; solo se inicializa.

```python
from PyQt6.QtWidgets import QWidget
from PyQt6.QtGui import QColor

class Medidor(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)        # imprescindible y lo primero
        self._valor = 0                 # estado: un valor 0-100
        self._color = QColor("#a3be8c") # estado: color del relleno
        # nada de QPainter aqui: solo se guarda el estado
```

> [!tip] Convencion
> Guarda el estado en atributos "privados" con guion bajo (`self._valor`) y exponlo
> luego con getter/setter (paso 5). Asi controlas que pasa cada vez que cambia.

### 2. Declarar el tamaño: sizeHint y minimumSizeHint

Cuando el widget vive dentro de un layout, el layout pregunta "¿que tamaño prefieres?" llamando a `sizeHint`, y "¿cual es tu minimo?" llamando a `minimumSizeHint`. Devuelves un `QSize` y el layout lo **respeta** al repartir el espacio. Si no los sobreescribes, el layout puede aplastar tu widget a cero.

```python
from PyQt6.QtCore import QSize
from PyQt6.QtWidgets import QSizePolicy

class Medidor(QWidget):
    def sizeHint(self):
        return QSize(160, 160)          # tamaño preferido

    def minimumSizeHint(self):
        return QSize(80, 80)            # nunca mas pequeño que esto
```

Si ademas quieres que el widget **crezca** para llenar el hueco disponible (en vez de quedarse en su `sizeHint`), declara una politica de tamaño expansiva:

```python
        self.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Expanding,
        )
```

### 3. Dibujarse: paintEvent

`paintEvent` es el corazon del widget. Qt lo llama cada vez que hay que repintar (al mostrarse, al cambiar de tamaño, al volver del fondo, o cuando tu pides un repintado con `update()`). Dentro creas un `QPainter(self)`, activas el suavizado y dibujas. La clave es **escalar el dibujo al tamaño actual** usando `self.rect()` / `self.width()` / `self.height()` en vez de coordenadas fijas: asi el widget se ve bien a cualquier tamaño.

```python
from PyQt6.QtGui import QPainter

class Medidor(QWidget):
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)  # bordes suaves

        rect = self.rect()                  # area completa del widget AHORA
        lado = min(rect.width(), rect.height()) - 10
        x = (rect.width() - lado) // 2      # centrado horizontal
        y = (rect.height() - lado) // 2     # centrado vertical

        painter.setBrush(self._color)
        painter.drawEllipse(x, y, lado, lado)
        # el QPainter se cierra solo al destruirse al final del metodo
```

Fijate en `self.rect()`: el dibujo se recalcula segun el tamaño vigente, no contra numeros fijos. El `QPainter` creado como `QPainter(self)` se **cierra solo** al destruirse al terminar el metodo; no hace falta `end()`.

> [!warning] Solo se pinta en paintEvent
> Un widget solo puede pintarse dentro de su `paintEvent`. Crear `QPainter(self)` en
> otro metodo (`__init__`, un slot) dispara el warning "painter outside paintEvent" y el
> dibujo no aparece o parpadea. Ver [[QPainter]].

### 4. Reaccionar al raton: mousePressEvent + update()

Para que el widget responda al raton, sobreescribe `mousePressEvent` (Qt lo llama al pulsar sobre el widget). Dentro **cambias un atributo de estado** y luego llamas a `self.update()` para que Qt reprograme un `paintEvent`. Nunca llames a `paintEvent()` a mano: `update()` agenda el repintado en el event loop y agrupa varios cambios en un solo redibujado.

```python
from PyQt6.QtGui import QColor

class Medidor(QWidget):
    def mousePressEvent(self, event):
        # cambia el estado...
        self._color = QColor("#bf616a") if self._color.name() == "#a3be8c" else QColor("#a3be8c")
        self.update()                       # ...y pide un repintado (NO paintEvent())
```

El ciclo es siempre el mismo: **evento -> cambio de estado -> `update()` -> Qt llama a `paintEvent`**. El `paintEvent` se limita a leer el estado y dibujarlo; no decide nada.

### 5. Exponer estado: getter/setter + señal propia

Para que el widget se integre como cualquier otro de Qt, no se tocan sus atributos desde fuera: se expone el estado con un **getter/setter** y, cuando ese estado cambia, se **emite una señal** propia con `pyqtSignal`. El setter ademas **valida** y llama a `self.update()`. Asi otros objetos pueden conectarse al widget igual que a un `QPushButton`.

```python
from PyQt6.QtCore import pyqtSignal

class Medidor(QWidget):
    valueChanged = pyqtSignal(int)          # señal propia: avisa del nuevo valor

    def valor(self):                        # getter
        return self._valor

    def setValor(self, valor):              # setter: valida, repinta y emite
        valor = max(0, min(100, int(valor)))   # validacion: lo encaja en 0-100
        if valor == self._valor:
            return                          # sin cambio real, no hace nada
        self._valor = valor
        self.update()                       # repinta con el nuevo valor
        self.valueChanged.emit(valor)       # avisa al mundo (ver [[pyqtSignal]])
```

Con esto, quien use el widget hace `medidor.setValor(70)` (no `medidor._valor = 70`) y puede escribir `medidor.valueChanged.connect(mi_slot)`. El widget se comporta como un ciudadano de Qt de pleno derecho.

## Ejemplo completo: un widget de verdad

Un `MedidorCircular` que reune todo: estado validado, `sizeHint`, `paintEvent` escalado a `self.rect()`, interaccion con el raton y una señal propia. Muestra un valor 0-100 como un arco que se llena, con el numero en el centro. Al hacer clic incrementa de 10 en 10 (y vuelve a 0 tras 100), se redibuja y emite `valueChanged`. La app lo usa y conecta su señal a la barra de estado.

```python
from PyQt6.QtWidgets import QApplication, QWidget, QMainWindow
from PyQt6.QtGui import QPainter, QColor, QPen, QFont
from PyQt6.QtCore import QSize, Qt, pyqtSignal
import sys

class MedidorCircular(QWidget):
    valueChanged = pyqtSignal(int)                          # señal propia

    def __init__(self, parent=None):
        super().__init__(parent)                            # SIEMPRE primero
        self._valor = 0                                     # estado: 0-100

    # --- estado: getter / setter validado + señal ---
    def valor(self):
        return self._valor

    def setValor(self, valor):
        valor = max(0, min(100, int(valor)))               # validacion
        if valor == self._valor:
            return
        self._valor = valor
        self.update()                                       # repinta
        self.valueChanged.emit(valor)                       # avisa

    # --- tamaño ---
    def sizeHint(self):
        return QSize(180, 180)

    def minimumSizeHint(self):
        return QSize(90, 90)

    # --- interaccion: clic incrementa ---
    def mousePressEvent(self, event):
        self.setValor((self._valor + 10) % 110 if self._valor < 100 else 0)

    # --- dibujo: escalado a self.rect() ---
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        rect = self.rect()
        lado = min(rect.width(), rect.height()) - 16
        x = (rect.width() - lado) // 2
        y = (rect.height() - lado) // 2

        painter.setPen(QPen(QColor("#3b4252"), 12))        # aro de fondo
        painter.drawArc(x, y, lado, lado, 0, 360 * 16)

        span = int(360 * 16 * self._valor / 100)           # arco proporcional
        painter.setPen(QPen(QColor("#88c0d0"), 12))
        painter.drawArc(x, y, lado, lado, 90 * 16, -span)  # empieza arriba

        painter.setPen(QColor("#eceff4"))                  # valor en el centro
        painter.setFont(QFont("Arial", lado // 6, QFont.Weight.Bold))
        painter.drawText(rect, Qt.AlignmentFlag.AlignCenter, f"{self._valor}")

class Ventana(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Medidor circular")
        self.medidor = MedidorCircular()
        self.setCentralWidget(self.medidor)
        # se conecta como cualquier widget de Qt:
        self.medidor.valueChanged.connect(
            lambda v: self.statusBar().showMessage(f"valor = {v}")
        )

app = QApplication(sys.argv)
ventana = Ventana()
ventana.resize(240, 260)
ventana.show()
sys.exit(app.exec())
```

Haz clic sobre el medidor: el arco se llena, el numero del centro cambia y la barra de estado refleja el nuevo valor porque esta conectada a `valueChanged`. El widget no sabe nada de la barra de estado; solo emite su señal.

## Buenas practicas

1. **Dibuja SOLO en `paintEvent`.** Es el unico sitio donde un `QPainter(self)` es valido. Cualquier otro metodo que necesite "redibujar" debe cambiar el estado y llamar a `self.update()`.
2. **`update()` (agenda) frente a `repaint()` (inmediato).** Usa casi siempre `self.update()`: agrupa cambios y repinta una vez en el event loop. `repaint()` fuerza el redibujado YA, sincronicamente; reservalo para casos raros (animaciones muy controladas) porque puede provocar parpadeo y trabajo de mas.
3. **Activa siempre Antialiasing para formas.** `painter.setRenderHint(QPainter.RenderHint.Antialiasing)` antes de dibujar; sin el, circulos y arcos salen con bordes dentados.
4. **Escala el dibujo con `self.rect()` / `self.width()` / `self.height()`,** nunca con coordenadas fijas. Asi el widget se ve bien a cualquier tamaño y al redimensionar.
5. **Separa ESTADO de DIBUJO.** El estado vive en atributos; `paintEvent` es una funcion **pura**: lee el estado y dibuja, sin efectos secundarios (no cambia atributos, no emite señales, no abre dialogos).
6. **Expon el estado con getter/setter + señal,** no dejes que toquen los atributos desde fuera. El setter valida, llama a `update()` y emite. Asi el widget se integra como uno mas de Qt (ver [[pyqtSignal]]).
7. **Declara `sizeHint` (y `minimumSizeHint`/`setMinimumSize`).** Sin ellos el layout puede aplastar tu widget. Usa `setSizePolicy` si quieres que crezca o se mantenga fijo.
8. **Usa `QColor` / `QPen` / `QBrush` con nombres claros** y, si se repiten, guardalos como atributos o constantes en vez de recrearlos en cada `paintEvent`.
9. **No hagas trabajo pesado en `paintEvent`.** Se llama muchas veces (cada resize, cada repintado). Precalcula geometrias o datos costosos al cambiar el estado, no al pintar.
10. **Recuerda `super().__init__(parent)`** como primera linea de `__init__` en toda subclase de `QWidget`/`QObject`. Es la causa numero uno de fallos al subclasear.

## Errores comunes

| Error | Causa | Solucion |
|-------|-------|----------|
| `RuntimeError` o crash al instanciar el widget | olvidaste `super().__init__(parent)` (o no es lo primero) en `__init__` | llamalo siempre, y lo primero, en cada subclase de `QWidget`/`QObject` |
| El dibujo no aparece o parpadea, warning "painter outside paintEvent" | creaste `QPainter(self)` fuera de `paintEvent` | dibuja **solo** dentro de `paintEvent`; para refrescar usa `self.update()` |
| Cambie un dato pero el widget no se redibuja | llamaste a `paintEvent()` a mano (no se hace) | cambia el estado y llama a `self.update()`, que agenda el repintado |
| El dibujo se descoloca o no encaja al redimensionar | usaste coordenadas fijas en vez de `self.rect()` | calcula posiciones y tamaños a partir de `self.width()`/`self.height()`/`self.rect()` |
| El layout aplasta el widget a cero | no sobreescribiste `sizeHint` o devuelve algo invalido | devuelve un `QSize` valido en `sizeHint` (y `minimumSizeHint`) |
| Los eventos de raton no llegan | firma del evento equivocada (mal nombre o args) | respeta la firma exacta, ej. `mousePressEvent(self, event)` |
| La señal no avisa | la declaraste como atributo de instancia o no la emites | declara `pyqtSignal` a **nivel de clase** y emite con `.emit(...)` desde el setter |

## Notas relacionadas

- [[concepto_herencia_widgets]] — el concepto base: por que se subclasea y se sobreescriben metodos
- [[QPainter]] — el motor de dibujo 2D que se usa dentro de `paintEvent`
- [[pyqtSignal]] — como declarar y emitir la señal propia del widget
- [[QPaintEvent]] — el evento que Qt pasa a `paintEvent`
- [[senal_personalizada]] — la receta general de definir señales propias con `pyqtSignal`
