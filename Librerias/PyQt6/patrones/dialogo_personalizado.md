---
title: dialogo personalizado — subclasear QDialog como formulario reutilizable
aliases: [dialogo personalizado, formulario reutilizable, subclasear QDialog]
tags: [pyqt6, patron, widgets]
lib: pyqt6
tipo: patron
requiere: [QDialog]
draft: false
---

# dialogo personalizado — subclasear QDialog como formulario reutilizable

A veces los dialogos predefinidos de Qt no bastan: necesitas un **cuadro propio que pide varios
datos** —un login, una pantalla de configuracion, un alta de usuario— y que **devuelva un
resultado claro** a quien lo abrio (los valores y si el usuario acepto o cancelo). La idea es
siempre la misma: heredar de [[QDialog]], **montar los campos en `__init__`**, cerrar con
`accept()`/`reject()`, y exponer los datos con un metodo. Asi obtienes un formulario
**reutilizable** que se abre en una sola linea desde cualquier parte de la app.

## La receta minima

Un dialogo con dos campos y los botones Ok/Cancel. Los botones no cierran solos: hay que conectar
`accepted`/`rejected` del `QDialogButtonBox` a `self.accept`/`self.reject`. La app lo abre con
`exec()` (que bloquea) y mira el resultado:

```python
from PyQt6.QtWidgets import (
    QApplication, QDialog, QFormLayout, QLineEdit, QDialogButtonBox
)
import sys

class DialogoLogin(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)                          # imprescindible
        self.setWindowTitle("Iniciar sesion")

        form = QFormLayout(self)
        self.usuario = QLineEdit()
        self.clave = QLineEdit()
        self.clave.setEchoMode(QLineEdit.EchoMode.Password)
        form.addRow("Usuario:", self.usuario)
        form.addRow("Clave:", self.clave)

        botones = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok
            | QDialogButtonBox.StandardButton.Cancel
        )
        botones.accepted.connect(self.accept)             # Ok -> cierra Accepted
        botones.rejected.connect(self.reject)             # Cancel -> cierra Rejected
        form.addRow(botones)

    def datos(self) -> tuple:                              # getter: se llama TRAS aceptar
        return self.usuario.text(), self.clave.text()

app = QApplication(sys.argv)
dlg = DialogoLogin()
if dlg.exec() == QDialog.DialogCode.Accepted:             # BLOQUEA hasta cerrarse
    usuario, clave = dlg.datos()
    print("entro:", usuario)
else:
    print("cancelo")
sys.exit(0)
```

## Construccion paso a paso

### 1. El esqueleto del dialogo

Toda subclase de [[QDialog]] empieza llamando a `super().__init__(parent)` —si lo olvidas, el
dialogo no se inicializa bien y suele fallar al mostrarse—. Luego pones el titulo y montas los
campos en un layout. El layout se asocia al dialogo pasandolo como argumento (`QFormLayout(self)`):

```python
class DialogoBase(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)                 # cadena de construccion de QDialog
        self.setWindowTitle("Mi formulario")     # titulo de la ventana

        form = QFormLayout(self)                  # el layout se cuelga del dialogo
        self.campo = QLineEdit()
        form.addRow("Dato:", self.campo)
```

Guardar los widgets como **atributos** (`self.campo`, no una variable local) es lo que luego
permite leerlos desde los metodos del dialogo.

### 2. Los botones: QDialogButtonBox

No pongas botones sueltos: usa [[QDialogButtonBox]] con los **botones estandar**. La ventaja es
que coloca Ok y Cancel en el **orden correcto de cada plataforma** (en Windows va Ok | Cancel; en
macOS, Cancel | Ok) sin que tu te ocupes. Conectas sus dos senales a los slots del dialogo:

```python
botones = QDialogButtonBox(
    QDialogButtonBox.StandardButton.Ok
    | QDialogButtonBox.StandardButton.Cancel
)
botones.accepted.connect(self.accept)            # se dispara con el boton "afirmativo"
botones.rejected.connect(self.reject)            # se dispara con el boton "negativo"
form.addRow(botones)
```

- `accept()` cierra el dialogo con codigo `Accepted`, y emite las senales `accepted` y `finished`.
- `reject()` cierra con `Rejected` (es tambien lo que hace pulsar Esc o cerrar la ventana).

La senal `accepted` del `QDialogButtonBox` agrupa todos los botones de rol "aceptar" (Ok, Yes,
Apply...), y `rejected` los de rol "rechazar" (Cancel, No, Close). Por eso basta con dos conexiones.

### 3. Modal: exec() y su valor de retorno

`exec()` abre el dialogo **modal**: **BLOQUEA** el flujo en esa linea hasta que el dialogo se
cierra, y devuelve un codigo —`QDialog.DialogCode.Accepted` o `QDialog.DialogCode.Rejected`—. Por
eso el patron de lectura es un `if` justo despues:

```python
if dlg.exec() == QDialog.DialogCode.Accepted:
    ...                                          # el usuario acepto
else:
    ...                                          # cancelo o cerro
```

> En PyQt6 el enum lleva **scope**: `QDialog.DialogCode.Accepted`, no `QDialog.Accepted`. Y es
> `exec()` (sin guion bajo), no `exec_()` como en PyQt5.

Para un dialogo que **no bloquea** (que convive con la ventana principal) usarias `show()` u
`open()`, y recogerias el resultado por la senal `finished`; pero para pedir datos lo normal es el
modal con `exec()`.

### 4. Recuperar los datos

La tentacion es leer `dlg.campo.text()` desde fuera. **No lo hagas**: acopla la app a la estructura
interna del dialogo. Expon los valores con **metodos getter**, asi por dentro puedes cambiar
widgets sin romper a quien lo usa (encapsulacion):

```python
class DialogoBase(QDialog):
    # ... __init__ con self.nombre, self.email ...

    def datos(self) -> dict:                     # API publica del dialogo
        return {
            "nombre": self.nombre.text().strip(),
            "email": self.email.text().strip(),
        }
```

Y desde fuera:

```python
if dlg.exec() == QDialog.DialogCode.Accepted:
    info = dlg.datos()                           # no se tocan los widgets internos
    print(info["nombre"])
```

Importante: lee los datos **mientras el dialogo vive** (justo tras `exec()`). Si guardas el dialogo
en una variable local de una funcion y lo lees despues de que la funcion termine, puede haberse
destruido y dar `RuntimeError`.

## El patron static getXxx (idiomatico en Qt)

Qt expone sus dialogos predefinidos con **metodos estaticos** que crean, abren y devuelven el
resultado de un golpe: `QInputDialog.getText(...)`, `QFileDialog.getOpenFileName(...)`. Todos
devuelven el **valor mas un booleano** de si se acepto. Puedes (y conviene) ofrecer lo mismo en tu
dialogo: un `@staticmethod` que crea la instancia, hace `exec()` y devuelve `(datos, ok)`:

```python
class DialogoLogin(QDialog):
    # ... __init__ y datos() como antes ...

    @staticmethod
    def pedir_datos(parent=None) -> tuple:
        dlg = DialogoLogin(parent)
        ok = dlg.exec() == QDialog.DialogCode.Accepted    # bloquea y devuelve bool
        datos = dlg.datos() if ok else None
        return datos, ok
```

Asi el dialogo se usa en **una sola linea**, exactamente como los de Qt:

```python
datos, ok = DialogoLogin.pedir_datos(self)       # self = la ventana que lo abre
if ok:
    print("usuario:", datos[0])
```

Quien llama ni siquiera necesita conocer la clase del dialogo por dentro: pide datos y recibe
`(valor, ok)`. Es la forma mas reutilizable.

## Ejemplo completo: dialogo de datos de usuario

Junta todo: un `DialogoUsuario` con nombre/email en un [[QFormLayout]], botones Ok/Cancel, getter
de datos, el static `pedir`, y **validacion**: sobreescribimos `accept()` para comprobar que los
campos no esten vacios; solo si son validos llamamos a `super().accept()`, y si no, mostramos un
aviso y dejamos el dialogo abierto:

```python
from PyQt6.QtWidgets import (
    QApplication, QWidget, QPushButton, QVBoxLayout, QLabel,
    QDialog, QFormLayout, QLineEdit, QDialogButtonBox, QMessageBox
)
import sys

class DialogoUsuario(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Nuevo usuario")

        form = QFormLayout(self)
        self.nombre = QLineEdit()
        self.email = QLineEdit()
        self.email.setPlaceholderText("nombre@dominio.com")
        form.addRow("Nombre:", self.nombre)
        form.addRow("Email:", self.email)

        botones = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok
            | QDialogButtonBox.StandardButton.Cancel
        )
        botones.accepted.connect(self.accept)    # llama a NUESTRO accept (el de abajo)
        botones.rejected.connect(self.reject)
        form.addRow(botones)

    def accept(self) -> None:                    # override: validar antes de cerrar
        if not self.nombre.text().strip():
            QMessageBox.warning(self, "Falta un dato", "El nombre no puede estar vacio.")
            return                               # NO llamamos a super(): sigue abierto
        if "@" not in self.email.text():
            QMessageBox.warning(self, "Email invalido", "Escribe un email valido.")
            return
        super().accept()                         # valido -> cierra con Accepted

    def datos(self) -> dict:
        return {"nombre": self.nombre.text().strip(), "email": self.email.text().strip()}

    @staticmethod
    def pedir(parent=None) -> tuple:
        dlg = DialogoUsuario(parent)
        ok = dlg.exec() == QDialog.DialogCode.Accepted
        return (dlg.datos() if ok else None), ok

# --- app que lo usa ---
app = QApplication(sys.argv)

ventana = QWidget(); ventana.setWindowTitle("Demo")
lay = QVBoxLayout(ventana)
etiqueta = QLabel("Sin usuario todavia")
boton = QPushButton("Alta de usuario...")
lay.addWidget(boton); lay.addWidget(etiqueta)

def alta():
    datos, ok = DialogoUsuario.pedir(ventana)    # una linea: abre, valida y devuelve
    if ok:
        etiqueta.setText(f"{datos['nombre']} <{datos['email']}>")

boton.clicked.connect(alta)
ventana.show()
sys.exit(app.exec())
```

## Buenas practicas

1. **Usa `QDialogButtonBox`, no botones sueltos.** Coloca Ok/Cancel en el orden correcto de cada
   plataforma y agrupa los roles en las senales `accepted`/`rejected`.
2. **Conecta `accepted`/`rejected` a `accept`/`reject`.** Es lo que hace que el dialogo se cierre
   con el codigo adecuado; sin esas conexiones los botones no hacen nada.
3. **Expon los resultados con getters**, no dejes que el exterior lea los widgets internos. Asi
   puedes cambiar la UI sin romper a quien usa el dialogo (encapsulacion).
4. **Valida sobreescribiendo `accept()`** y llama a `super().accept()` **solo si es valido**; si no,
   avisa con un [[QMessageBox]] y vuelve (`return`) para mantener el dialogo abierto.
5. **`exec()` para modal que bloquea**, `show()`/`open()` para no modal. Para pedir datos casi
   siempre quieres `exec()` y leer el resultado en la linea siguiente.
6. **Pasa siempre `parent`** (la ventana que lo abre): centra el dialogo sobre ella, hereda el
   estilo y deja que el arbol de objetos gestione su memoria.
7. **Ofrece un static `getXxx -> (valor, ok)`** para reutilizar el dialogo en una sola linea, igual
   que `QInputDialog.getText`/`QFileDialog.getOpenFileName`.
8. **Lee los datos mientras el dialogo vive** (justo tras `exec()`), nunca despues de que pueda
   haberse destruido.
9. **No reutilices la misma instancia** si guarda estado sucio de una apertura anterior: crea un
   dialogo nuevo (o resetea los campos) en cada uso.
10. **No reinventes lo que ya existe:** para un texto suelto usa `QInputDialog`, para un mensaje o
    un si/no usa [[QMessageBox]], y para elegir archivos `QFileDialog`. Subclasea solo cuando pides
    varios datos a la vez.

## Errores comunes

| Error | Causa | Solucion |
|-------|-------|----------|
| Ok/Cancel no cierran el dialogo | no conectaste el `QDialogButtonBox` | conecta `accepted`->`accept` y `rejected`->`reject` |
| `RuntimeError` al leer un campo | leiste el dialogo (de pila local) despues de que se destruyo | lee los datos mientras vive, justo tras `exec()` |
| El codigo sigue sin esperar respuesta | usaste `show()` cuando querias modal | usa `exec()`: bloquea y devuelve el codigo |
| Validas pero el dialogo se cierra igual | olvidaste llamar a `super().accept()` (o lo llamas siempre) | llama a `super().accept()` **solo** en la rama valida; en la invalida haz `return` |
| El `if` nunca entra aunque aceptes | comparaste el retorno con `True` | compara con el enum: `== QDialog.DialogCode.Accepted` |

## Notas relacionadas

- [[QDialog]] — la clase base que se subclasea; de ahi vienen `exec`/`accept`/`reject` y el ser modal
- [[QDialogButtonBox]] — la caja de botones estandar (Ok/Cancel) con el orden correcto por plataforma
- [[QFormLayout]] — el layout etiqueta/campo ideal para montar los formularios del dialogo
- [[QMessageBox]] — el aviso que se muestra al validar, y el dialogo predefinido para mensajes/preguntas
- [[QLineEdit]] — el campo de texto tipico de un dialogo de datos
