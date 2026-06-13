---
title: pyqtSignal — declarar una señal propia
aliases: [pyqtSignal, señal propia, custom signal]
tags: [pyqt6, api/funcion, core]
lib: pyqt6
mod: QtCore
tipo: funcion
requiere: [concepto_signals_slots]
draft: false
---

# pyqtSignal — declarar una señal propia

`pyqtSignal` crea una **señal propia**: el aviso que tu clase emitira cuando le pase algo. Se asigna como **atributo de clase** (a nivel de la clase, NO dentro de `__init__`) en una subclase de `QObject`. PyQt la convierte en una señal real, ligada por instancia, en cuanto el objeto se construye. Es la mitad emisora del mecanismo de [[concepto_signals_slots | senales y slots]]: lo que declaras con `pyqtSignal` luego se dispara con `.emit()` y se escucha con `.connect()`.

## Importacion

```python
from PyQt6.QtCore import QObject, pyqtSignal
```

## Firma

```python
pyqtSignal(*types, name: str = None)
```

- **`*types`**: los tipos de los argumentos que la señal **llevara** (los que recibira el slot). Pueden ser tipos Python (`int`, `str`, `float`, `bool`, `list`, `dict`, `object`) o tipos Qt. Sin tipos = señal sin datos.
- **`name`**: el nombre Qt de la señal. Por defecto, el del atributo. Util si quieres que el nombre visible en Qt difiera del nombre Python.

## Como se usa

La señal se declara a nivel de clase y se referencia luego como `self.<nombre>`:

```python
from PyQt6.QtCore import QObject, pyqtSignal

class Termometro(QObject):
    temperatura_cambiada = pyqtSignal(float)   # ATRIBUTO DE CLASE, no en __init__

    def medir(self, t):
        self.temperatura_cambiada.emit(t)       # disparar la señal
```

Aunque la declares una vez en la clase, cada **instancia** tiene su propia señal independiente: conectar `sensor_a.temperatura_cambiada` no afecta a `sensor_b`.

Tipos de declaracion segun lo que lleve la señal:

| Declaracion | Lleva | El slot recibe |
|-------------|-------|----------------|
| `pyqtSignal()` | nada | sin argumentos |
| `pyqtSignal(int)` | un int | `def slot(self, v): ...` |
| `pyqtSignal(int, str)` | dos argumentos | `def slot(self, n, texto): ...` |
| `pyqtSignal(object)` | cualquier objeto Python | el objeto tal cual |
| `pyqtSignal(list)` | una lista | la lista |

## Sobrecarga (varias firmas)

Una señal puede declarar **varias firmas** pasando listas de tipos. La señal podra emitir un tipo u otro; al conectar o emitir, eliges la firma con `señal[tipo]`:

```python
from PyQt6.QtCore import QObject, pyqtSignal

class Entrada(QObject):
    valor = pyqtSignal([int], [str])      # puede emitir un int O un str

    def enviar_numero(self, n):
        self.valor[int].emit(n)           # firma int

    def enviar_texto(self, s):
        self.valor[str].emit(s)           # firma str

e = Entrada()
e.valor[int].connect(lambda n: print("entero:", n))
e.valor[str].connect(lambda s: print("texto:", s))
e.enviar_numero(7)      # entero: 7
e.enviar_texto("hola")  # texto: hola
```

La **primera** firma de la lista es la por defecto: `e.valor.connect(...)` (sin indice) usa `[int]`.

## Casos de uso

Señal sin datos, como simple aviso de que algo ocurrio:

```python
from PyQt6.QtCore import QObject, pyqtSignal

class Tarea(QObject):
    terminada = pyqtSignal()              # sin argumentos: solo avisa

    def ejecutar(self):
        # ... trabajo ...
        self.terminada.emit()

t = Tarea()
t.terminada.connect(lambda: print("lista"))
t.ejecutar()                              # imprime "lista"
```

Señal que transporta datos hacia varios escuchadores:

```python
from PyQt6.QtCore import QObject, pyqtSignal

class Descarga(QObject):
    progreso = pyqtSignal(int)            # lleva el porcentaje
    error = pyqtSignal(str)               # lleva el mensaje

    def correr(self):
        for p in (0, 50, 100):
            self.progreso.emit(p)

d = Descarga()
d.progreso.connect(lambda p: print(f"{p}%"))
d.correr()                                # 0%  50%  100%
```

Pasar un objeto Python arbitrario con `object`:

```python
from PyQt6.QtCore import QObject, pyqtSignal

class Cola(QObject):
    recibido = pyqtSignal(object)         # cualquier objeto Python

    def push(self, item):
        self.recibido.emit(item)

c = Cola()
c.recibido.connect(lambda x: print(type(x).__name__, x))
c.push({"id": 1})                         # dict {'id': 1}
```

## Errores comunes

| Error | Causa | Solucion |
|-------|-------|----------|
| La señal no dispara nada / no existe | la declaraste dentro de `__init__` | declarala como **atributo de clase**, a nivel de la clase |
| `TypeError: ... is not a Qt property or signal` | la clase no hereda de `QObject` | haz que herede de `QObject` (o de un widget, que ya lo hace) |
| `TypeError` al hacer `.emit(...)` | los tipos de `emit` no coinciden con los de `pyqtSignal(...)` | usa los mismos tipos en la declaracion y en `emit` |
| `KeyError` al usar `señal[tipo]` | esa firma no fue declarada en la sobrecarga | declara la firma en `pyqtSignal([...], [...])` o usa una existente |
| El slot recibe argumentos de mas | la señal lleva datos y el slot no los espera | acepta el argumento o usa un `lambda` que lo ignore |

## Notas relacionadas

- [[concepto_signals_slots]] — el mecanismo completo de señales y slots
- [[emit]] — disparar una señal declarada con `pyqtSignal`
- [[connect]] — conectar la señal a un slot
- [[QObject]] — solo sus subclases pueden tener señales
