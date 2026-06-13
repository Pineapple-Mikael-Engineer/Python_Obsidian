---
title: selectores QSS — a que widgets aplica cada regla
aliases: [selectores QSS, pseudo-estados QSS, hover checked, sub-controles QSS]
tags: [pyqt6, estilado, gui]
lib: pyqt6
tipo: concepto
requiere: [qss_stylesheets]
draft: false
---

# selectores QSS — a que widgets aplica cada regla

Si [[qss_stylesheets]] explica la **sintaxis** de una hoja de estilo (la regla `propiedad: valor` dentro de las llaves), esta nota explica el **selector**: la parte que va ANTES de las llaves y decide A QUE widgets se aplica esa regla. Dominar los selectores es lo que separa un estilo torpe de uno preciso: poder decir "solo este boton", "los botones cuando pasas el raton por encima" o "el tirador de este slider" en vez de pintar toda la ventana del mismo color. Una regla QSS es siempre `selector { declaraciones }`; aqui solo nos ocupamos del selector.

## Selectores por tipo de widget

El selector mas basico es el **nombre de la clase**: aplica a TODOS los widgets de ese tipo y a sus subclases.

```python
app.setStyleSheet("""
    QPushButton { background: #5e81ac; color: white; }
""")
```

Esa regla pinta cada `QPushButton` de la aplicacion. Como incluye subclases, una clase generica afecta a muchisimo:

```python
# QWidget es la base de casi todo -> esta regla toca casi todos los widgets
app.setStyleSheet("QWidget { font-size: 14px; }")
```

Por eso `QWidget { ... }` se usa para un estilo global de partida, y luego se afina con selectores mas concretos.

## Por nombre de objeto (#id)

El selector mas **preciso**: estiliza UN widget concreto sin tocar los demas del mismo tipo. Se hace en dos pasos — poner un nombre de objeto en Python y referirlo con `#` en QSS.

```python
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton
import sys

app = QApplication(sys.argv)
ventana = QWidget()
layout = QVBoxLayout(ventana)

guardar = QPushButton("Guardar")
guardar.setObjectName("guardar")        # nombre unico para este widget
cancelar = QPushButton("Cancelar")

layout.addWidget(guardar)
layout.addWidget(cancelar)

app.setStyleSheet("""
    QPushButton { background: #4c566a; color: white; }
    #guardar    { background: #a3be8c; }   /* solo el boton Guardar */
""")

ventana.show()
sys.exit(app.exec())
```

El `#guardar` solo afecta al widget cuyo `objectName` es `"guardar"`; "Cancelar" se queda con el estilo generico.

## Por clase exacta (.Clase) y herencia

Hay una diferencia importante entre el nombre desnudo y el punto delante:

- `QPushButton { ... }` aplica a `QPushButton` **y a cualquier subclase** suya.
- `.QPushButton { ... }` aplica **solo a esa clase exacta**, no a las que heredan de ella.

```python
app.setStyleSheet("""
    QPushButton  { color: blue; }   /* QPushButton y subclases */
    .QPushButton { color: red; }    /* SOLO QPushButton, no subclases */
""")
```

Util cuando tienes una subclase propia (`class BotonRojo(QPushButton)`) y quieres que el estilo generico NO la alcance: con `.QPushButton` el padre se estiliza y la subclase queda libre.

## Por propiedad ([prop="valor"])

Puedes filtrar por el valor de una propiedad Qt (ver [[concepto_propiedades]]) usando corchetes:

```python
app.setStyleSheet("""
    QPushButton[flat="true"] { border: none; color: #5e81ac; }
""")
```

Esa regla solo toca los botones cuya propiedad `flat` vale `true`. Tambien sirve con **propiedades dinamicas** que tu inventes con `setProperty`:

```python
boton.setProperty("clase", "peligro")
# QSS: QPushButton[clase="peligro"] { background: #bf616a; }
```

> [!warning] Refrescar tras cambiar una propiedad dinamica
> Si cambias la propiedad EN CALIENTE (despues de aplicar el estilo), Qt no re-evalua el selector solo. Hay que forzarlo:
> ```python
> boton.setProperty("clase", "peligro")
> boton.style().unpolish(boton)   # quita el estilo viejo
> boton.style().polish(boton)     # vuelve a aplicar -> ahora si re-evalua [clase=...]
> ```

## Pseudo-estados (:estado) — LA seccion clave

Un **pseudo-estado** aplica la regla solo cuando el widget esta en cierto estado (raton encima, pulsado, marcado...). Es la herramienta mas potente de QSS: efectos visuales reactivos sin escribir una sola linea de logica.

| Pseudo-estado | Cuando aplica |
|---------------|---------------|
| `:hover` | el raton esta encima del widget |
| `:pressed` | el widget esta siendo pulsado |
| `:checked` | esta marcado (checkbox, radio, boton `checkable`) |
| `:unchecked` | no esta marcado |
| `:disabled` | el widget esta deshabilitado (`setEnabled(False)`) |
| `:enabled` | el widget esta habilitado |
| `:focus` | el widget tiene el foco de teclado |

Ejemplo de un boton que reacciona al raton, todo en QSS:

```python
app.setStyleSheet("""
    QPushButton {
        background: #5e81ac;
        color: white;
        padding: 6px 14px;
        border-radius: 4px;
    }
    QPushButton:hover   { background: #81a1c1; }   /* raton encima */
    QPushButton:pressed { background: #4c566a; }   /* mientras se pulsa */
""")
```

Los pseudo-estados se pueden **combinar** encadenandolos: la regla aplica solo si se dan todos a la vez.

```python
app.setStyleSheet("""
    QPushButton:checked        { background: #a3be8c; }
    QPushButton:checked:hover  { background: #b5cfa0; }  /* marcado Y con raton encima */
""")
```

## Sub-controles (::parte)

Muchos widgets son **compuestos**: por dentro tienen piezas (un desplegable tiene su flecha, un slider tiene su carril y su tirador). Un **sub-control** estiliza una de esas piezas internas, y se escribe con doble dos puntos `::`.

| Sub-control | Pieza que estiliza |
|-------------|--------------------|
| `QComboBox::drop-down` | la zona de la flecha del desplegable |
| `QSlider::groove` | el carril por donde corre el slider |
| `QSlider::handle` | el tirador que se arrastra |
| `QScrollBar::handle` | el bloque que se arrastra en la barra |
| `QHeaderView::section` | cada cabecera de columna de una tabla/arbol |
| `QCheckBox::indicator` | el cuadradito que se marca/desmarca |

**Por que importa:** al dar estilo a un widget compuesto, a veces sobreescribes su pintado nativo y sus sub-controles **se rompen o desaparecen**. Si estilizas un `QSlider` sin tocar su `::handle`, el tirador puede quedarse invisible. La regla practica: si estilizas el contenedor, estiliza tambien las piezas que necesites ver.

```python
app.setStyleSheet("""
    QSlider::groove:horizontal {
        height: 6px;
        background: #4c566a;
        border-radius: 3px;
    }
    QSlider::handle:horizontal {
        background: #88c0d0;
        width: 16px;
        margin: -5px 0;          /* sobresale del carril */
        border-radius: 8px;
    }
""")
```

Fijate que un sub-control puede llevar ademas un pseudo-estado (`::handle:horizontal`): primero la pieza, luego su estado.

## Combinar selectores

Los selectores se pueden encadenar para apuntar con mas finura:

- **Descendiente** (espacio): solo los widgets de un tipo que estan DENTRO de otro.
  ```css
  QGroupBox QPushButton { color: #ebcb8b; }   /* botones dentro de un QGroupBox */
  ```
- **Agrupar** (coma): aplica el mismo estilo a varios selectores a la vez.
  ```css
  QPushButton, QToolButton { padding: 6px; }   /* a los dos tipos */
  ```
- **Estado + sub-control**: combinar pseudo-estado y sub-control en una sola regla.
  ```css
  QComboBox::drop-down:hover { background: #81a1c1; }   /* la flecha, al pasar el raton */
  ```

## Ejemplo completo

App ejecutable que usa, en una sola hoja, un `#id`, pseudo-estados `:hover`/`:pressed` y el sub-control `::handle` de un slider:

```python
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton, QSlider
)
from PyQt6.QtCore import Qt
import sys

app = QApplication(sys.argv)
ventana = QWidget()
ventana.setWindowTitle("Selectores QSS en accion")
layout = QVBoxLayout(ventana)

guardar = QPushButton("Guardar")
guardar.setObjectName("guardar")     # para el selector #guardar
cancelar = QPushButton("Cancelar")
slider = QSlider(Qt.Orientation.Horizontal)
slider.setValue(40)

for w in (guardar, cancelar, slider):
    layout.addWidget(w)

ventana.setStyleSheet("""
    /* tipo: todos los botones */
    QPushButton {
        background: #4c566a;
        color: white;
        padding: 6px 14px;
        border: none;
        border-radius: 4px;
    }
    QPushButton:hover   { background: #5e81ac; }   /* pseudo-estado */
    QPushButton:pressed { background: #3b4252; }

    /* #id: solo el boton Guardar */
    #guardar         { background: #a3be8c; color: #2e3440; }
    #guardar:hover   { background: #b5cfa0; }

    /* sub-control: el carril y el tirador del slider */
    QSlider::groove:horizontal {
        height: 6px; background: #434c5e; border-radius: 3px;
    }
    QSlider::handle:horizontal {
        background: #88c0d0; width: 16px; margin: -5px 0; border-radius: 8px;
    }
    QSlider::handle:horizontal:hover { background: #8fbcbb; }
""")

ventana.resize(280, 160)
ventana.show()
sys.exit(app.exec())
```

Al ejecutarlo veras: "Guardar" en verde y el resto en gris, ambos cambiando de tono al pasar el raton y al pulsarlos, y el tirador del slider redondo y azul que se aclara con el raton encima.

## Buenas practicas

1. Para casos unicos, usa `#objectName` en vez de duplicar estilos copiando la misma regla con pequeñas variaciones.
2. Prefiere pseudo-estados a conectar señales para efectos visuales: el cambio de color al pasar el raton es `:hover` en QSS, no codigo que escuche `enterEvent`.
3. Al estilizar widgets compuestos, revisa siempre sus sub-controles: si pintas el contenedor, comprueba que el `::handle`, `::indicator` o `::drop-down` siguen visibles.
4. Agrupa con coma los selectores que comparten estilo (`QPushButton, QToolButton`) en lugar de repetir el bloque.
5. Pon nombres de objeto descriptivos (`#botonGuardar`, no `#b1`): el QSS se lee como prosa.
6. Recuerda que el selector de tipo incluye subclases; usa `.Clase` si quieres la clase exacta y dejar libres las que heredan de ella.
7. Tras cambiar una propiedad dinamica en caliente, re-aplica el estilo con `unpolish`/`polish` o el selector `[prop=...]` no se re-evalua.
8. No intentes microgestionar cada pixel con QSS: cuando el control visual debe ser total (pintado a medida), el camino es [[widget_personalizado]], no una hoja de estilo gigante.

## Errores comunes

| Error | Causa | Solucion |
|-------|-------|----------|
| `#guardar { ... }` no aplica nada | el widget no tiene ese nombre de objeto | llama a `widget.setObjectName("guardar")` antes |
| el tirador del slider desaparece al estilizarlo | estilizaste el `QSlider` pero no sus sub-controles | añade reglas para `::groove` y `::handle` |
| `:hover` no hace nada visible | el widget no tiene fondo propio que cambiar | dale primero un `background`/`border` en la regla base |
| `[clase="x"]` no reacciona al cambiar la propiedad | la cambiaste en caliente sin refrescar | `style().unpolish(w); style().polish(w)` |
| el sub-control se ignora o estiliza otra cosa | confundiste `:` (estado) con `::` (sub-control) | un dos puntos para estados, dos para piezas internas |

## Notas relacionadas

- [[qss_stylesheets]] — la sintaxis de la hoja de estilo (las declaraciones dentro de las llaves)
- [[QWidget]] — la base que comparten casi todos los widgets estilizables
- [[widget_personalizado]] — cuando QSS no basta y hay que pintar el widget a mano
