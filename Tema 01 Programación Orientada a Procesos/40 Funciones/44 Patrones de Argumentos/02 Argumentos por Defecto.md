---
title: Argumentos por Defecto
draft: false
tags: [python, teoria, funciones]
---
# Argumentos por Defecto

Un **valor por defecto** hace que un parámetro sea **opcional**: si la llamada no lo proporciona, se usa el valor indicado en la definición con `parametro=valor`.

```python
# Parámetros con valores por defecto
def saludar(nombre, mensaje="Hola", signo="!"):
    """Saluda con mensaje personalizable."""
    print(f"{mensaje}, {nombre}{signo}")

# Llamadas con diferente número de argumentos
saludar("Ana")                    # Hola, Ana!
saludar("Juan", "Buenos días")    # Buenos días, Juan!
saludar("Carlos", "Adiós", "...") # Adiós, Carlos...
saludar(nombre="María", signo="?") # Hola, María?

# Múltiples valores por defecto
def crear_producto(nombre, precio, stock=0, categoria="General", disponible=True):
    """Crea un producto con valores por defecto."""
    return {
        "nombre": nombre,
        "precio": precio,
        "stock": stock,
        "categoria": categoria,
        "disponible": disponible
    }

print(crear_producto("Laptop", 1200))
print(crear_producto("Mouse", 25, stock=10, categoria="Periféricos"))
```

## Orden: Sin Defecto → Con Defecto

Los parámetros sin defecto deben ir **antes** que los que tienen defecto; lo contrario es `SyntaxError`.

```python
# 1. ✅ Correcto: parámetros sin defecto primero, con defecto después
def funcion_correcta(a, b, c=3, d=4):
    return a + b + c + d

# ❌ Incorrecto: parámetro con defecto antes que sin defecto
# def funcion_incorrecta(a=1, b, c):  # SyntaxError
#     pass
```

## Evaluación en Tiempo de Definición

El valor por defecto se evalúa **una sola vez**, cuando se define la función — no en cada llamada. Esto sorprende cuando el defecto es una expresión que cambia con el tiempo.

```python
# 2. Los valores por defecto se evalúan una vez, en tiempo de definición
import datetime

def mostrar_fecha(mensaje, fecha=datetime.date.today()):
    """Muestra mensaje con fecha (cuidado: fecha se evalúa una vez)."""
    print(f"{mensaje}: {fecha}")

# Todas las llamadas mostrarán la misma fecha (la del momento de definición)
mostrar_fecha("Hoy")
# Simular paso del tiempo
import time
time.sleep(2)
mostrar_fecha("Dos segundos después")  # Misma fecha

# Solución: usar None como valor por defecto
def mostrar_fecha_correcta(mensaje, fecha=None):
    if fecha is None:
        fecha = datetime.date.today()  # Se evalúa en cada llamada
    print(f"{mensaje}: {fecha}")

mostrar_fecha_correcta("Hoy")
time.sleep(2)
mostrar_fecha_correcta("Dos segundos después")  # Fecha actualizada
```

## El Peligro de los Mutables como Default

Como el defecto se crea una vez, un objeto **mutable** (`list`, `dict`, `set`) usado como default se **comparte entre todas las llamadas**: las mutaciones persisten.

```python
# ❌ MAL: usar mutable como valor por defecto
def agregar_elemento_mal(elemento, lista=[]):
    """Intenta agregar elemento a lista (compartida entre llamadas)."""
    lista.append(elemento)
    return lista

print(agregar_elemento_mal(1))  # [1]
print(agregar_elemento_mal(2))  # [1, 2] (no [2] como esperarías)
print(agregar_elemento_mal(3))  # [1, 2, 3]

# ✅ BIEN: usar None y crear nueva lista
def agregar_elemento_bien(elemento, lista=None):
    """Agrega elemento a lista (nueva lista por defecto)."""
    if lista is None:
        lista = []
    lista.append(elemento)
    return lista

print(agregar_elemento_bien(1))  # [1]
print(agregar_elemento_bien(2))  # [2] (nueva lista)
print(agregar_elemento_bien(3))  # [3]

# Mismo problema con diccionarios
def configurar_mal(opciones={}):
    """Configuración con diccionario compartido."""
    opciones["debug"] = True
    return opciones

print(configurar_mal())        # {'debug': True}
print(configurar_mal())        # {'debug': True} (el mismo diccionario)

# Solución correcta
def configurar_bien(opciones=None):
    if opciones is None:
        opciones = {}
    opciones["debug"] = True
    return opciones
```

> [!warning] Regla práctica: nunca uses un mutable como valor por defecto. Usa `None` como centinela y crea el objeto **dentro** del cuerpo con `if x is None: x = []`. Lo mismo aplica a cualquier expresión cuyo valor deba refrescarse en cada llamada (fechas, IDs, timestamps).

## Buenas Prácticas

- Usa defectos para parámetros genuinamente **opcionales** (`def conectar(host, port=5432, ssl=False)`).
- Reserva valores **inmutables** (números, cadenas, `None`, tuplas) como defectos directos; cualquier mutable va tras el centinela `None`.
- Un defecto debe representar el caso **más común**, no uno arbitrario, para que la llamada corta sea la habitual.
