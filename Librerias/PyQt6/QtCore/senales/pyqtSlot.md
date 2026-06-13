---
title: pyqtSlot — decorador que marca un metodo como slot tipado de Qt
aliases:
  - pyqtSlot
  - slot
  - "@pyqtSlot"
tags: [pyqt6, api/funcion, core]
lib: pyqt6
mod: QtCore
tipo: funcion
requiere: [concepto_signals_slots]
draft: false
---

# pyqtSlot — decorador que marca un metodo como slot tipado de Qt

`@pyqtSlot` es un **decorador** que marca un metodo de un `QObject` como slot de Qt, declarando los **tipos** de argumentos que acepta. No es obligatorio: en PyQt cualquier funcion o metodo Python ya sirve de slot y se puede conectar con `.connect()`. Pero decorar aporta ventajas reales —sobrecarga por tipos, menor uso de memoria, conexiones correctas entre hilos y una firma explicita—, asi que es recomendable en clases grandes o en codigo con hilos. Es el complemento de [[pyqtSignal]] en el sistema de [[concepto_signals_slots]].

## Firma

```python
@pyqtSlot(*types, name=None, result=None)
def metodo(self, ...):
    ...
```

- `*types`: los tipos de los argumentos que recibe el slot (`int`, `str`, `float`, una clase Qt...). Vacio = slot sin argumentos.
- `name`: nombre con el que se registra el slot en el meta-objeto (por defecto, el del metodo). Util al sobrecargar.
- `result`: tipo del valor de retorno; relevante cuando el slot se invoca con `QMetaObject.invokeMethod`.

## Como se usa

El decorador va sobre un metodo de una subclase de `QObject` (o de cualquier widget, que ya hereda de [[QObject]]). Los tipos del decorador deben casar con los que emite la señal a la que se conecta.

```python
from PyQt6.QtCore import QObject, pyqtSignal, pyqtSlot

class Panel(QObject):
    aviso = pyqtSignal(int)

    @pyqtSlot(int)               # slot que acepta un int
    def actualizar(self, valor):
        print(f"valor = {valor}")

    @pyqtSlot()                  # slot sin argumentos
    def refrescar(self):
        print("refrescado")

p = Panel()
p.aviso.connect(p.actualizar)   # los tipos casan: pyqtSignal(int) -> @pyqtSlot(int)
p.aviso.emit(7)                 # imprime "valor = 7"
```

Para definir un return (necesario al invocar el slot por nombre desde Qt) se usa `result`:

```python
class Calculadora(QObject):
    @pyqtSlot(int, result=str)   # recibe int, devuelve str
    def etiqueta(self, n):
        return f"#{n}"
```

## Casos de uso

- **Sobrecarga por tipos**: varios `@pyqtSlot` con tipos distintos sobre metodos del mismo nombre permiten que un mismo slot responda a señales de firmas diferentes.

```python
from PyQt6.QtCore import QObject, pyqtSlot

class Receptor(QObject):
    @pyqtSlot(str)               # version que acepta un str
    def recibir(self, dato):
        print(f"texto: {dato}")

    @pyqtSlot(int)               # version que acepta un int
    def recibir(self, dato):
        print(f"numero: {dato}")
```

- **Eficiencia / memoria**: el slot queda registrado en el meta-objeto de Qt, lo que evita la maquinaria extra que PyQt monta para envolver un callable Python cualquiera. Importa cuando hay muchos slots.
- **Conexiones entre hilos**: con la firma declarada, Qt entrega correctamente la llamada al hilo del objeto receptor (conexion en cola), evitando llamadas cruzadas inseguras entre hilos.
- **Claridad**: la firma del slot queda documentada en el propio decorador.

## Errores comunes

| Error | Causa | Solucion |
|-------|-------|----------|
| `@pyqtSlot` no surte efecto | lo pusiste en una funcion suelta, no en un metodo de un `QObject` | el decorador solo aplica a metodos de una subclase de `QObject` / widget |
| `TypeError` o el slot no se dispara al conectar | los tipos del decorador no casan con los que emite la señal | usa los mismos tipos: `pyqtSignal(int)` -> `@pyqtSlot(int)` |
| La sobrecarga "se pisa" | declaraste dos metodos del mismo nombre sin decorar | cada version necesita su propio `@pyqtSlot(<tipo>)` para registrarse |
| Slot entre hilos se ejecuta en el hilo equivocado | el metodo no estaba decorado, Qt no conocia su firma | decora con `@pyqtSlot(...)` para habilitar la conexion en cola |

## Notas relacionadas

- [[concepto_signals_slots]] — el mecanismo de señales y slots donde encaja este decorador
- [[pyqtSignal]] — declarar la señal que se conecta al slot
- [[QObject]] — solo sus subclases pueden tener slots registrados
