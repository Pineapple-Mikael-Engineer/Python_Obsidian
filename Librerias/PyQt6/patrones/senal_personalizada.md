---
title: senal personalizada — declarar y emitir una pyqtSignal propia
aliases: [senal personalizada, signal propia, pyqtSignal, emitir senal]
tags: [pyqt6, patron, core]
lib: pyqt6
tipo: patron
requiere: [concepto_signals_slots, pyqtSignal]
draft: false
---

# senal personalizada — declarar y emitir una pyqtSignal propia

Definir senales propias es lo que hace que **tus** clases participen del mismo juego que los widgets de Qt: un `QPushButton` anuncia `clicked` y cualquiera se suscribe sin que el boton sepa quien escucha. Con una senal propia, tu worker avisa "voy por el 40%", tu modelo de datos avisa "una fila cambio", tu widget avisa "mi valor es otro" — y el receptor reacciona sin que el emisor lo conozca. Es el mismo **desacoplamiento** de [[concepto_signals_slots | senales y slots]], pero ahora aplicado a tu dominio.

La idea clave que ordena todo lo demas: una [[pyqtSignal]] se declara como **ATRIBUTO DE CLASE**, nunca dentro de `__init__`. PyQt la "liga" a cada instancia cuando el objeto se construye; si la metes en `__init__` no llega a ser una senal real.

## La receta minima

Una subclase de `QObject`, una senal declarada a nivel de clase, un metodo que la dispara con `.emit()`, y alguien que conecta un slot:

```python
from PyQt6.QtCore import QObject, pyqtSignal

class Modelo(QObject):
    cambiado = pyqtSignal()              # ATRIBUTO DE CLASE: la senal, sin datos

    def tocar(self):
        self.cambiado.emit()            # disparar -> ejecuta los slots conectados

m = Modelo()
m.cambiado.connect(lambda: print("algo cambio"))   # conectar un slot
m.tocar()                                # imprime "algo cambio"
```

Tres piezas: **declarar** (atributo de clase), **emitir** (`self.cambiado.emit()`) y **conectar** (`m.cambiado.connect(...)`). El resto de la nota es esto mismo, con datos y mas realismo.

## Construccion paso a paso

### 1. Declarar la senal

La senal va **a nivel de la clase**, como `cambiado = pyqtSignal()`, no como `self.cambiado = ...` en `__init__`. PyQt usa esa declaracion de clase para fabricar, en cada instancia, una senal real ligada a ese objeto. Cada instancia tiene su propia senal independiente: conectar la de un objeto no afecta a otro.

```python
from PyQt6.QtCore import QObject, pyqtSignal

class Bien(QObject):
    listo = pyqtSignal()                # CORRECTO: atributo de clase
```

Lo que **no** funciona — declararla dentro de `__init__`:

```python
from PyQt6.QtCore import QObject, pyqtSignal

class Mal(QObject):
    def __init__(self):
        super().__init__()
        self.listo = pyqtSignal()       # MAL: aqui es solo un objeto pyqtSignal suelto

m = Mal()
m.listo.connect(lambda: print("hola"))  # AttributeError: 'pyqtSignal' object has no attribute 'connect'
```

Dentro de `__init__`, `pyqtSignal()` es un objeto inerte sin `connect`/`emit` ligados al QObject. La conversion a senal real solo ocurre para los atributos declarados en el cuerpo de la clase.

### 2. Llevar datos: tipos en la senal

Los argumentos de `pyqtSignal(...)` son los **tipos** que la senal transporta hacia el slot. Sin tipos, la senal es un simple aviso; con tipos, lleva datos.

```python
from PyQt6.QtCore import QObject, pyqtSignal
from dataclasses import dataclass

@dataclass
class Punto:
    x: int
    y: int

class Sensor(QObject):
    progreso = pyqtSignal(int)              # lleva un int
    medida   = pyqtSignal(str, float)       # lleva dos: un str y un float
    dato     = pyqtSignal(object)           # cualquier objeto Python: lista, dataclass, dict...

    def reportar(self):
        self.progreso.emit(40)                      # tipos que COINCIDEN con la declaracion
        self.medida.emit("temperatura", 36.5)
        self.dato.emit(Punto(3, 7))                 # un objeto cualquiera viaja con object

s = Sensor()
s.progreso.connect(lambda v: print(f"{v}%"))
s.medida.connect(lambda nombre, val: print(f"{nombre} = {val}"))
s.dato.connect(lambda obj: print(type(obj).__name__, obj))
s.reportar()
# 40%
# temperatura = 36.5
# Punto Punto(x=3, y=7)
```

Regla de oro: los tipos de `emit(...)` deben **coincidir** con los de `pyqtSignal(...)`. Para tipos Python arbitrarios (listas, diccionarios, dataclasses, instancias propias) usa `object`: cabe cualquier cosa sin convertir.

### 3. Conectar y desconectar

`.connect(slot)` une la senal a un slot; puedes conectar **varios** slots a la misma senal y todos se ejecutan al emitir. `.disconnect()` deshace la conexion.

```python
from PyQt6.QtCore import QObject, pyqtSignal

class Boton(QObject):
    pulsado = pyqtSignal()

    def click(self):
        self.pulsado.emit()

def guardar():  print("guardar")
def avisar():   print("avisar")

b = Boton()
b.pulsado.connect(guardar)              # un slot
b.pulsado.connect(avisar)               # otro slot mas; ambos se ejecutan
b.click()                               # guardar  /  avisar

b.pulsado.disconnect(avisar)            # quitar un slot concreto
b.click()                               # solo: guardar

b.pulsado.disconnect()                  # sin argumentos: quita TODOS los slots
b.click()                               # no imprime nada
```

`disconnect(slot)` quita un slot concreto; `disconnect()` sin argumentos desconecta todos. Conecta **por nombre del metodo** (`guardar`), nunca llamandolo (`guardar()`).

### 4. Senales con sobrecarga

> [!nota] Avanzado
> Una misma senal puede declarar **varias firmas** pasando listas de tipos. Es util cuando un mismo hecho del dominio puede expresarse con datos distintos, pero la mayoria de notas no lo necesita: una senal por hecho suele ser mas claro.

```python
from PyQt6.QtCore import QObject, pyqtSignal

class Entrada(QObject):
    valor = pyqtSignal([int], [str])        # puede emitir un int O un str

    def enviar_numero(self, n):
        self.valor[int].emit(n)             # eliges la firma con senal[tipo]

    def enviar_texto(self, s):
        self.valor[str].emit(s)

e = Entrada()
e.valor[int].connect(lambda n: print("entero:", n))   # conectar la version concreta
e.valor[str].connect(lambda s: print("texto:", s))
e.enviar_numero(7)        # entero: 7
e.enviar_texto("hola")    # texto: hola
```

La **primera** firma de la lista es la por defecto: `e.valor.emit(5)` y `e.valor.connect(...)` sin indice usan `[int]`.

## Ejemplo completo: un worker que reporta progreso

El caso clasico: un objeto que hace un trabajo y va **avisando** de su avance y de su final, sin saber quien dibuja la barra de progreso ni quien muestra el resultado. Aqui se simula el trabajo sin hilos para mantenerlo simple; en una app real el worker corre en un [[QThread]] para no congelar la interfaz.

```python
from PyQt6.QtCore import QObject, pyqtSignal

class Descargador(QObject):
    progreso  = pyqtSignal(int)             # porcentaje (0..100)
    terminado = pyqtSignal(str)             # mensaje final

    def __init__(self, url):
        super().__init__()
        self.url = url

    def correr(self):
        for p in range(0, 101, 20):
            self.progreso.emit(p)           # va avisando del avance
        self.terminado.emit(f"descarga de {self.url} completa")

# --- alguien escucha, sin que el Descargador lo conozca ---
def pintar_barra(p):
    print(f"[{'#' * (p // 10):<10}] {p}%")

def al_terminar(msg):
    print("LISTO:", msg)

d = Descargador("http://ejemplo.com/archivo.zip")
d.progreso.connect(pintar_barra)            # conectar AMBAS senales a sus slots
d.terminado.connect(al_terminar)
d.correr()
# [          ] 0%
# [##        ] 20%
# [####      ] 40%
# [######    ] 60%
# [########  ] 80%
# [##########] 100%
# LISTO: descarga de http://ejemplo.com/archivo.zip completa
```

El `Descargador` no importa nada de la interfaz: solo declara dos hechos de su dominio (`progreso`, `terminado`) y los emite. Quien dibuja la barra y quien muestra el aviso son ajenos al worker. Cambiar la GUI no toca el worker; ese es el beneficio.

## Segundo ejemplo: un widget que emite su cambio

Un widget propio expone una propiedad `valor` cuyo setter **emite** solo cuando el valor cambia de verdad. El guard `if nuevo == self._valor: return` evita avisos redundantes y, sobre todo, cortar **bucles de senales** (A actualiza a B, B reactualiza a A, y asi sin fin). Enlaza con el patron [[widget_personalizado]].

```python
from PyQt6.QtWidgets import QApplication, QWidget
from PyQt6.QtCore import pyqtSignal
import sys

class Contador(QWidget):
    valueChanged = pyqtSignal(int)          # nombre estilo Qt: participio/pasado

    def __init__(self):
        super().__init__()
        self._valor = 0                     # estado interno, con guion bajo

    @property
    def valor(self):
        return self._valor

    @valor.setter
    def valor(self, nuevo):
        if nuevo == self._valor:            # GUARD: emitir solo si cambia de verdad
            return
        self._valor = nuevo
        self.valueChanged.emit(nuevo)       # avisar del cambio real

app = QApplication(sys.argv)
c = Contador()
c.valueChanged.connect(lambda v: print(f"valor -> {v}"))

c.valor = 3      # valor -> 3
c.valor = 3      # (nada: no cambio)
c.valor = 5      # valor -> 5
```

Como hereda de `QWidget` (que ya es `QObject`), no hace falta heredar de `QObject` aparte: el widget ya puede tener senales. El setter es el unico sitio que muta `_valor`, asi que es el lugar natural para el guard y el `emit`.

## Buenas practicas

1. Declara la senal **siempre** a nivel de clase (`mi_senal = pyqtSignal(...)`), nunca con `self.` en `__init__`.
2. Nombra en participio/pasado como Qt: `clicked`, `valueChanged`, `terminado`, `error_ocurrido`; el nombre describe el **hecho**, no la accion del receptor.
3. **Tipa** la senal y emite los tipos exactos: `pyqtSignal(int)` se emite con un `int`, no con un `str`.
4. Emite **solo cuando el estado cambia de verdad** (guard `if nuevo == self._valor: return`): evita avisos redundantes y bucles de senales entre objetos.
5. No emitas en `__init__`: cuando el objeto se construye **nadie ha podido conectar** todavia, asi que ese aviso se pierde.
6. Usa `pyqtSignal(object)` para transportar tipos Python arbitrarios (listas, dataclasses, instancias propias) sin convertir.
7. Una senal = **un hecho del dominio** (`fila_anadida`, `descarga_terminada`), no detalles de la interfaz como `boton2Pulsado`.
8. Centraliza el `emit` en el setter / el unico metodo que muta el estado; no lo repartas por la clase.
9. **Documenta** que senales emite cada clase y con que datos (en PyQt6 esto va tambien en el frontmatter `senales:` de la nota de clase).
10. Conecta **por nombre del metodo** (`self.f`), nunca llamandolo (`self.f()`): con parentesis conectas el resultado de la llamada, no el slot.

## Errores comunes

| Error | Causa | Solucion |
|-------|-------|----------|
| `AttributeError: 'pyqtSignal' object has no attribute 'connect'` | la declaraste dentro de `__init__` (`self.x = pyqtSignal()`) | declarala como **atributo de clase**, en el cuerpo de la clase |
| `TypeError` al hacer `.emit(...)` | los tipos de `emit` no casan con los de `pyqtSignal(...)` | emite los mismos tipos que declaraste; usa `object` para tipos Python libres |
| El slot no se ejecuta y no hay error | conectaste `self.f()` (con parentesis): pasaste el resultado, no el slot | conecta por nombre: `senal.connect(self.f)` |
| La senal "no dispara" pese a emitir | emitiste **antes** de que nadie conectara (p. ej. en `__init__`) | emite despues de que el receptor haya hecho `.connect(...)` |
| El slot falla por argumentos de mas/menos | olvidaste que el slot recibe los **mismos args** que lleva la senal | acepta esos argumentos en el slot, o usa un `lambda` que los ignore |
| `TypeError: ... is not a Qt property or signal` | la clase no hereda de `QObject` (ni de un widget) | haz que herede de `QObject` o de algun `QWidget` |

## Notas relacionadas

- [[concepto_signals_slots]] — el mecanismo completo de senales y slots
- [[pyqtSignal]] — la funcion que declara la senal (firma, sobrecarga, tipos)
- [[pyqtSlot]] — marcar un metodo como slot con sus tipos
- [[widget_personalizado]] — subclasear un widget que expone sus propias senales
- [[QThread]] — donde corre de verdad un worker que reporta progreso
