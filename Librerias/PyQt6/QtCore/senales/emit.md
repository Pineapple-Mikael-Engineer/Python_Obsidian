---
title: emit — disparar una señal
aliases: [emit, emitir señal, disparar señal]
tags: [pyqt6, api/metodo, core]
lib: pyqt6
mod: QtCore
tipo: metodo
requiere: [concepto_signals_slots]
draft: false
---

# emit — disparar una señal

`senal.emit(*args)` **dispara** la señal: ejecuta, en orden de conexion, todos los slots conectados a ella, pasandoles `args`. Es el momento en que el aviso sale del objeto emisor hacia sus escuchadores. Es la mitad activa del mecanismo de [[concepto_signals_slots | senales y slots]]: [[connect]] registra quien escucha, `emit` provoca la reaccion. Los tipos de `args` deben coincidir con los declarados en [[pyqtSignal]].

## Firma

```python
senal.emit(*args) -> None
```

- **`*args`**: los valores a enviar a los slots. Su numero y tipo deben **coincidir** con los de la declaracion `pyqtSignal(*types)`.
- No devuelve nada: `emit` es sincrono en conexion directa (los slots corren ahi mismo, antes de continuar) y encolado entre hilos.

## Como se usa

Por convencion, una señal se emite **desde dentro** de la misma clase que la declara: es ese objeto quien sabe cuando ha ocurrido el evento. Los tipos de `emit` casan con los de `pyqtSignal`:

```python
from PyQt6.QtCore import QObject, pyqtSignal

class Descarga(QObject):
    progreso = pyqtSignal(int)            # declara: lleva un int

    def correr(self):
        for p in (0, 50, 100):
            self.progreso.emit(p)         # emite ints -> casa con pyqtSignal(int)
```

## Parametros segun la declaracion

| Declaracion | Como se emite |
|-------------|---------------|
| `pyqtSignal()` | `self.senal.emit()` (sin argumentos) |
| `pyqtSignal(int)` | `self.senal.emit(42)` |
| `pyqtSignal(int, str)` | `self.senal.emit(3, "hola")` |
| `pyqtSignal(object)` | `self.senal.emit(cualquier_objeto)` |

## Sobrecarga

Si la señal declara varias firmas, elige cual emitir con `señal[tipo]` antes de `.emit`:

```python
from PyQt6.QtCore import QObject, pyqtSignal

class Entrada(QObject):
    valor = pyqtSignal([int], [str])      # dos firmas

    def enviar(self, x):
        if isinstance(x, int):
            self.valor[int].emit(x)       # firma int
        else:
            self.valor[str].emit(x)       # firma str
```

Sin indice, `self.valor.emit(...)` usa la **primera** firma declarada (`[int]`).

## Casos de uso

Señal con datos hacia varios slots conectados:

```python
from PyQt6.QtCore import QObject, pyqtSignal

class Termometro(QObject):
    temperatura_cambiada = pyqtSignal(float)

    def medir(self, t):
        self.temperatura_cambiada.emit(t)     # dispara los slots con t

sensor = Termometro()
sensor.temperatura_cambiada.connect(lambda t: print(f"{t} C"))
sensor.temperatura_cambiada.connect(lambda t: print("alerta" if t > 38 else "ok"))
sensor.medir(36.5)        # imprime "36.5 C" y "ok"
sensor.medir(39.0)        # imprime "39.0 C" y "alerta"
```

Señal sin datos, como aviso de fin:

```python
from PyQt6.QtCore import QObject, pyqtSignal

class Tarea(QObject):
    terminada = pyqtSignal()              # sin argumentos

    def ejecutar(self):
        # ... trabajo ...
        self.terminada.emit()             # emit() vacio

t = Tarea()
t.terminada.connect(lambda: print("lista"))
t.ejecutar()                              # imprime "lista"
```

App completa: emitir una señal propia para reaccionar en la GUI:

```python
from PyQt6.QtWidgets import QApplication, QLabel, QPushButton, QVBoxLayout, QWidget
from PyQt6.QtCore import QObject, pyqtSignal
import sys

class Contador(QObject):
    cambio = pyqtSignal(int)

    def __init__(self):
        super().__init__()
        self.n = 0

    def sumar(self):
        self.n += 1
        self.cambio.emit(self.n)          # avisa el nuevo valor

app = QApplication(sys.argv)
w = QWidget()
lay = QVBoxLayout(w)
etiqueta = QLabel("0")
boton = QPushButton("+1")
lay.addWidget(etiqueta)
lay.addWidget(boton)

contador = Contador()
contador.cambio.connect(lambda n: etiqueta.setText(str(n)))
boton.clicked.connect(contador.sumar)

w.show()
sys.exit(app.exec())
```

## Errores comunes

| Error | Causa | Solucion |
|-------|-------|----------|
| `TypeError` al emitir | los tipos/numero de `emit(...)` no casan con `pyqtSignal(...)` | emite exactamente los tipos declarados (`pyqtSignal(int)` -> `emit(un_int)`) |
| Nada ocurre al emitir | no habia ningun slot conectado con `.connect` | conecta antes de emitir, o revisa que conectaste la señal correcta |
| Emites una señal "de otra clase" y falla | intentas emitir la señal sin instancia o desde fuera | emite desde **dentro** de la clase que la declara, sobre `self.senal` |
| `KeyError` con `señal[tipo].emit` | esa firma no fue declarada en la sobrecarga | usa una firma declarada en `pyqtSignal([...], [...])` |
| El slot recibe argumentos de mas | emites datos a un slot que no los espera | ajusta el slot o envuelvelo en un `lambda` que ignore el argumento |

## Notas relacionadas

- [[concepto_signals_slots]] — el mecanismo completo de señales y slots
- [[pyqtSignal]] — declarar la señal que luego se emite
- [[connect]] — registrar los slots que `emit` dispara
