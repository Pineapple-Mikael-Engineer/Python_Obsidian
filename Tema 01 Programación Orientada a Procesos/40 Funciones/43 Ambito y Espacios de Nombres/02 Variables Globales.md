---
title: Variables Globales
order: 2
tags:
  - python
  - teoria
  - ambito
draft: false
aliases:
  - Global variables
  - Palabra clave global
---

# Variables Globales

> [!definicion]
> Una **variable global** se define a nivel de módulo, fuera de cualquier función, y es accesible desde cualquier punto del módulo. Vive durante toda la ejecución del programa. Las funciones pueden **leerla** directamente; para **reasignarla** desde dentro de una función se requiere la palabra clave `global`.

> [!regla]
> - **Lectura:** directa, sin declaración.
> - **Modificación de objeto mutable in-place** (`.append`, `dict[k]=v`): directa, sin `global`.
> - **Reasignación del nombre** (`x = ...`): exige `global x`, de lo contrario se crea una local.

---

## Acceso de lectura desde funciones

```python
# Variables globales
nombre = "Ana"
edad = 25
PI = 3.14159  # Convención: constantes en mayúsculas

def saludar():
    # Acceso a variable global (solo lectura)
    print(f"Hola, me llamo {nombre}")

def mostrar_edad():
    # También puede acceder a globales
    print(f"Tengo {edad} años")

saludar()      # Hola, me llamo Ana
mostrar_edad() # Tengo 25 años

# Modificar global (sin declaración especial) — a nivel de módulo
print(f"Nombre antes: {nombre}")
nombre = "Ana María"  # Modificación directa
print(f"Nombre después: {nombre}")

# Las globales persisten durante toda la ejecución
print(f"Siempre tenemos acceso a PI: {PI}")
```

---

## La palabra clave `global`

> [!definicion]
> `global <nombre>` declara que el nombre referido dentro de la función corresponde a la variable global del módulo, no a una local. Habilita su reasignación y su creación desde dentro de la función.

```python
# Variable global
contador = 0

def incrementar_sin_global():
    # Esto crea una variable LOCAL, no modifica la global
    contador = contador + 1  # ❌ UnboundLocalError
    return contador

def incrementar_con_global():
    global contador
    contador = contador + 1  # ✅ Modifica la global
    return contador

try:
    incrementar_sin_global()
except UnboundLocalError as e:
    print(f"Error sin global: {e}")

print(f"Contador antes: {contador}")
incrementar_con_global()
incrementar_con_global()
incrementar_con_global()
print(f"Contador después: {contador}")  # 3
```

Sin `global`, la asignación clasifica `contador` como local y `contador + 1` lanza `UnboundLocalError` (caso detallado en [[01 Variables Locales | Variables Locales]]).

### Declarar múltiples globales

```python
# Múltiples variables globales
usuario = None
intentos = 0
ultimo_acceso = None

def iniciar_sesion(nombre):
    global usuario, intentos, ultimo_acceso

    if usuario is not None:
        print(f"Ya hay sesión activa: {usuario}")
        return False

    usuario = nombre
    intentos = 0
    ultimo_acceso = "ahora"
    print(f"Sesión iniciada para {usuario}")
    return True

def intentar_acceso():
    global intentos
    intentos += 1
    print(f"Intento #{intentos}")

def cerrar_sesion():
    global usuario, ultimo_acceso
    print(f"Cerrando sesión de {usuario}")
    usuario = None
    ultimo_acceso = None

# Uso
iniciar_sesion("Ana")
intentar_acceso()
intentar_acceso()
print(f"Usuario actual: {usuario}")
cerrar_sesion()
print(f"Usuario actual: {usuario}")
```

### Crear globales desde dentro de una función

`global` también permite *crear* el nombre en el módulo aunque no existiera antes.

```python
def crear_global():
    global nueva_variable
    nueva_variable = "Creada desde función"
    print(f"Dentro: {nueva_variable}")

# nueva_variable no existe aún
try:
    print(nueva_variable)
except NameError as e:
    print(f"Error: {e}")

crear_global()
print(f"Fuera: {nueva_variable}")  # Ahora existe

# Ver todas las globales
print("Variables globales:")
for nombre in list(globals().keys())[-5:]:  # Últimas 5
    if not nombre.startswith('__'):
        print(f"  {nombre}: {globals()[nombre]}")
```

---

## Inmutables vs mutables

> [!warning]
> Con tipos **inmutables** (`int`, `str`, `tuple`) toda modificación es una reasignación: exige `global`. Con tipos **mutables** (`list`, `dict`) se puede mutar el contenido sin `global`, pero reasignar el nombre completo sigue requiriéndolo.

```python
# Con inmutables (int, str, tuple) necesitas global para modificar
nombre = "Ana"

def cambiar_nombre_mal():
    nombre = "Juan"  # Crea local, no modifica global
    print(f"Dentro: {nombre}")

def cambiar_nombre_bien():
    global nombre
    nombre = "Juan"
    print(f"Dentro: {nombre}")

cambiar_nombre_mal()
print(f"Fuera (mal): {nombre}")  # Ana

cambiar_nombre_bien()
print(f"Fuera (bien): {nombre}")  # Juan
```

```python
# Con mutables (list, dict) puedes modificar contenido sin global
lista = [1, 2, 3]
diccionario = {"a": 1}

def modificar_mutables():
    # No necesita global para modificar contenido
    lista.append(4)
    diccionario["b"] = 2

    # Pero SÍ necesita global para reasignar
    # lista = [5, 6, 7]  # Esto crearía local

print(f"Antes: lista={lista}, dict={diccionario}")
modificar_mutables()
print(f"Después: lista={lista}, dict={diccionario}")

# Para reasignar completamente, necesitas global
def reasignar_lista():
    global lista
    lista = [5, 6, 7]
    print(f"Dentro (reasignada): {lista}")

reasignar_lista()
print(f"Fuera (reasignada): {lista}")
```

---

## Espacio de nombres del módulo

`globals()` expone el espacio de nombres global como diccionario; `locals()` el del ámbito actual. Permiten inspección y creación dinámica de globales.

```python
# globals() - diccionario de variables globales
print("Variables globales:")
for nombre, valor in list(globals().items())[:5]:  # Primeras 5
    if not nombre.startswith('__'):
        print(f"  {nombre}: {valor}")

# locals() - diccionario de variables locales
def mostrar_locales():
    nombre = "Ana"
    edad = 25
    habilidades = ["Python", "SQL"]

    locales = locals()
    print("\nVariables locales:")
    for nombre, valor in locales.items():
        print(f"  {nombre}: {valor}")

    return locales

locales_guardados = mostrar_locales()
print(f"\nLocales fuera: {locales_guardados}")
```

```python
# Crear variables globales dinámicamente
for i in range(3):
    globals()[f"variable_{i}"] = i * 10

print(variable_0)  # 0
print(variable_1)  # 10
print(variable_2)  # 20
```

> [!warning]
> Modificar `locals()` **no** crea variables locales reales: dentro de una función `locals()` es una copia de solo lectura.
>
> ```python
> def crear_locales():
>     for i in range(3):
>         locals()[f"local_{i}"] = i * 100
>     try:
>         print(local_0)  # ❌ No funciona realmente
>     except NameError as e:
>         print(f"Error: {e}")
>
> crear_locales()
>
> # Forma correcta: usar un diccionario propio
> def crear_locales_correcto():
>     valores = {}
>     for i in range(3):
>         valores[f"local_{i}"] = i * 100
>     for nombre, valor in valores.items():
>         print(f"{nombre}: {valor}")
>
> crear_locales_correcto()
> ```

Cada módulo importado mantiene su propio espacio de nombres independiente:

```python
import math

# El módulo tiene su propio espacio de nombres
print("Atributos de math:")
for nombre in dir(math)[:5]:  # Primeros 5
    if not nombre.startswith('__'):
        print(f"  math.{nombre}")

print(f"math.pi: {math.pi}")
print(f"math.e: {math.e}")

# El espacio de nombres del módulo es independiente
pi = 3.14  # Nuestra variable
print(f"pi local: {pi}")
print(f"math.pi: {math.pi}")  # Sigue siendo el original
```

---

## Problemas de las variables globales

> [!warning]
> El estado global mutable es modificable por cualquier función del módulo. Esto dificulta razonar sobre el código: un efecto colateral en una función puede corromper datos de los que dependen otras.

```python
# Ejemplo de problemas con globales
saldo = 1000

def retirar(cantidad):
    global saldo
    if cantidad <= saldo:
        saldo -= cantidad
        print(f"Retirado {cantidad}. Saldo restante: {saldo}")
        return True
    print("Saldo insuficiente")
    return False

def depositar(cantidad):
    global saldo
    saldo += cantidad
    print(f"Depositado {cantidad}. Nuevo saldo: {saldo}")

# Múltiples funciones modifican la misma global
retirar(500)
depositar(200)
retirar(800)  # Saldo insuficiente después de operaciones

# Problema: cualquier función puede modificar saldo
def error_grave():
    global saldo
    saldo = 0  # 😱 Borra todo el saldo
    print("¡Error catastrófico!")

error_grave()
print(f"Saldo final: {saldo}")  # 0
```

### Alternativas al estado global

```python
# 1. Usar parámetros y retorno (programación funcional)
def incrementar(contador):
    return contador + 1

contador = 0
contador = incrementar(contador)
contador = incrementar(contador)
print(f"Contador funcional: {contador}")

# 2. Usar clases y atributos
class Contador:
    def __init__(self):
        self.valor = 0

    def incrementar(self):
        self.valor += 1
        return self.valor

cont = Contador()
cont.incrementar()
cont.incrementar()
print(f"Contador con clase: {cont.valor}")

# 3. Usar closures
def crear_contador():
    contador = 0
    def incrementar():
        nonlocal contador
        contador += 1
        return contador
    return incrementar

mi_contador = crear_contador()
print(f"Closure: {mi_contador()}")
print(f"Closure: {mi_contador()}")
```

---

## Buenas prácticas

> [!regla]
> 1. Evitar globales cuando un parámetro y un retorno bastan.
> 2. Constantes de módulo en MAYÚSCULAS (`MAX_INTENTOS`, `PI`).
> 3. Documentar toda global mutable que las funciones reasignen.
> 4. Preferir una clase (un solo objeto de configuración) sobre muchas globales sueltas.
> 5. Variables de módulo "privadas" con prefijo `_` por convención.
> 6. Preferir inyección de dependencias sobre leer estado global implícito.

```python
# 2. Constantes con mayúsculas
MAX_INTENTOS = 3
PI = 3.14159

# 3. Documentar el uso de global
contador_global = 0  # ⚠️ Global - modificar con cuidado

def resetear_contador():
    """Resetea el contador global a 0."""
    global contador_global
    contador_global = 0

# 4. Usar clases en lugar de muchas globales
class Configuracion:
    def __init__(self):
        self.debug = False
        self.verbose = False

    def toggle_debug(self):
        self.debug = not self.debug

config = Configuracion()  # Una sola global

# 6. Variables de módulo con _ para "privadas"
_config_cache = {}  # Convención: "privada" del módulo

def get_config(key):
    return _config_cache.get(key)

# 7. Preferir inyectar dependencias
# Malo
def procesar():
    global usuario_actual
    print(f"Procesando para {usuario_actual}")

# Bueno
def procesar(usuario):
    print(f"Procesando para {usuario}")
```

---

## Relación con otras notas

- Una global se encuentra en el tercer nivel de la [[03 Regla LEGB | regla LEGB]], tras Local y Enclosing.
- El error al leer un nombre asignado sin `global` se trata en [[01 Variables Locales | Variables Locales]].
- Para modificar el ámbito contenedor en funciones anidadas (no el global) se usa [[04 Nonlocal | nonlocal]].
