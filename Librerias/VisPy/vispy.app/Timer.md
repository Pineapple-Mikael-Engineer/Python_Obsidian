---
title: Timer — temporizador para animaciones
aliases: [Timer, vispy timer, animacion vispy]
tags: [vispy, api/clase, app]
lib: vispy
mod: vispy.app
tipo: clase
requiere: [Canvas]
draft: false
---

# Timer — temporizador para animaciones

`Timer` es el mecanismo de VisPy para ejecutar codigo a intervalos regulares dentro del **event loop** sin bloquearlo. Es la pieza central de cualquier animacion: en cada tick actualiza los datos del visual y llama `canvas.update()` para forzar un redibujado. A diferencia de `time.sleep`, `Timer` es **no-bloqueante** y convive con los eventos de teclado, mouse y ventana.

## Importacion

```python
import vispy
vispy.use('pyqt5')
from vispy import app
```

## Constructor / Firma

```python
timer = app.Timer(
    interval=1/60,      # segundos entre ticks; o 'auto' (maximo posible)
    connect=callback,   # funcion a conectar al crear (o None)
    iterations=-1,      # -1 = infinito; N = dispara N veces y para
    start=False,        # True = arranca inmediatamente al crear
)
```

## Parametros clave

| Parametro | Tipo | Por defecto | Descripcion |
|-----------|------|-------------|-------------|
| `interval` | `float \| str` | `0.0` | Segundos entre ticks. `'auto'` = tan rapido como el event loop permita |
| `connect` | `callable \| None` | `None` | Callback a conectar al instanciar; equivalente a llamar `.connect()` despues |
| `iterations` | `int` | `-1` | Numero de ticks antes de detenerse. `-1` = infinito |
| `start` | `bool` | `False` | Arranca el timer al crear si es `True` |

### El objeto `event` en el callback

```python
def on_timer(event):
    event.dt       # float: segundos transcurridos desde el ultimo tick
    event.elapsed  # float: segundos totales desde que el timer arranco
    event.count    # int: numero de ticks ejecutados hasta ahora
```

`event.dt` es lo mas util para animaciones fisicamente correctas (independiente del FPS real).

## Casos de uso

### Patron tipico: animacion con Canvas

```python
import vispy
vispy.use('pyqt5')
from vispy import app, gloo
import numpy as np

canvas = app.Canvas(size=(800, 600), keys='interactive')
t_total = 0.0

@canvas.connect
def on_draw(event):
    # leer t_total aqui (ya fue actualizado por on_timer)
    color = (abs(np.sin(t_total)), 0.3, 0.7, 1.0)
    gloo.clear(color=color)

@canvas.connect
def on_resize(event):
    gloo.set_viewport(0, 0, *event.size)

timer = app.Timer(interval=1/60, start=False)

@timer.connect
def on_timer(event):
    global t_total
    t_total += event.dt   # acumula tiempo real transcurrido
    canvas.update()       # solicita redibujado al event loop

canvas.show()
timer.start()
app.run()
```

### Conectar callback al instanciar

```python
def tick(event):
    canvas.update()

timer = app.Timer(interval=1/30, connect=tick, start=True)
# Equivalente a:
# timer = app.Timer(interval=1/30)
# timer.connect(tick)
# timer.start()
```

### Timer de disparo unico

```python
# Ejecutar una accion una sola vez despues de 2 segundos
def delayed_action(event):
    print('ejecutado despues de 2 s')

timer = app.Timer(interval=2.0, connect=delayed_action, iterations=1, start=True)
```

### Usar `interval='auto'` para maxima velocidad

```python
# Render a la maxima velocidad posible (limitado por el event loop)
timer = app.Timer(interval='auto', start=False)

@timer.connect
def on_timer(event):
    # event.dt puede variar mucho con 'auto'; usarlo siempre para avanzar la simulacion
    canvas.update()
```

> [!warning] `interval='auto'` vs FPS fijo
> Con `'auto'` el timer dispara lo mas rapido posible pero sin garantia de intervalo. Siempre usa `event.dt` para avanzar la simulacion; **nunca** asumas un dt fijo con `'auto'`.

## Metodos y atributos

| Nombre | Tipo | Descripcion |
|--------|------|-------------|
| `.start(interval=None)` | metodo | Inicia el timer. Opcionalmente cambia el intervalo |
| `.stop()` | metodo | Detiene el timer sin destruirlo |
| `.connect(func)` | metodo | Conecta un callback adicional al evento `timer` |
| `.disconnect(func)` | metodo | Desconecta un callback previamente conectado |
| `.running` | `bool` | `True` si el timer esta activo |
| `.interval` | `float \| str` | Intervalo actual en segundos o `'auto'` |
| `.elapsed` | `float` | Segundos transcurridos desde el ultimo `.start()` |

## Diferencia con `time.sleep`

| Aspecto | `app.Timer` | `time.sleep` |
|---------|-------------|--------------|
| Bloquea el event loop | No | Si |
| Compatible con eventos de ventana | Si | No |
| Precision | Dependiente del event loop | Dependiente del OS |
| Uso tipico | Animaciones, polling continuo | Pausas puntuales fuera de GUI |

Nunca uses `time.sleep` dentro de un callback de VisPy: congela la ventana y bloquea todos los eventos.

## Errores comunes

| Error | Causa | Solucion |
|-------|-------|----------|
| La animacion no se ve | `canvas.update()` no se llama en `on_timer` | Agregar `canvas.update()` al final del callback |
| El timer arranca pero no ejecuta | `start=False` y no se llamo `.start()` | Llamar `timer.start()` antes de `app.run()` |
| `event.dt` siempre es 0 | Se usa `time.sleep` en el callback | Eliminar `time.sleep`; el Timer ya controla el tiempo |
| Multiples timers interfieren | Dos timers llaman `canvas.update()` | Un solo timer por canvas es suficiente |

## Notas relacionadas

- [[Canvas]] — la ventana que se redibuja con `canvas.update()`; Timer la alimenta
- [[vispy.use]] — debe llamarse antes de crear Timer o Canvas
