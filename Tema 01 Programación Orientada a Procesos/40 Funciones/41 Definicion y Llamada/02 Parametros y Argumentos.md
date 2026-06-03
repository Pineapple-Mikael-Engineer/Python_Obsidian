---
title: Parámetros y Argumentos
tags:
  - python
  - teoria
  - funciones
draft: false
aliases:
  - Paso de argumentos
  - Posicionales y nombrados
---

# Parámetros y Argumentos

**Parámetro** es el nombre que aparece en la definición; **argumento** es el valor concreto que se pasa en la llamada. Los argumentos pueden vincularse a parámetros por **posición** (el orden importa) o por **nombre** (orden libre).

```python
# Definición con parámetros posicionales
def saludar(nombre, apellido):
    """Saluda a una persona con nombre y apellido."""
    print(f"Hola, {nombre} {apellido}!")

# Llamada con argumentos posicionales (orden importa)
saludar("Juan", "Pérez")     # ✅ Hola, Juan Pérez!
saludar("Pérez", "Juan")     # ❌ Hola, Pérez Juan! (orden incorrecto)

# Múltiples parámetros
def calcular_imc(peso, altura):
    """Calcula el Índice de Masa Corporal."""
    imc = peso / (altura ** 2)
    return imc

# Uso correcto
mi_imc = calcular_imc(70, 1.75)
print(f"IMC: {mi_imc:.2f}")
```

## Argumentos Nombrados (Keyword Arguments)

Al nombrar el argumento en la llamada (`param=valor`), el orden deja de importar. Pueden mezclarse con posicionales, pero **los posicionales siempre van primero**.

```python
def crear_perfil(nombre, edad, ciudad, profesion):
    """Crea un perfil de usuario."""
    perfil = f"Nombre: {nombre}\nEdad: {edad}\nCiudad: {ciudad}\nProfesión: {profesion}"
    return perfil

# Llamada con argumentos nombrados (orden no importa)
perfil1 = crear_perfil(
    nombre="Ana",
    edad=28,
    ciudad="Madrid",
    profesion="Ingeniera"
)

perfil2 = crear_perfil(
    ciudad="Barcelona",
    profesion="Diseñadora",
    nombre="Carlos",
    edad=32
)

print(perfil1)
print(perfil2)

# Mezcla de posicionales y nombrados
def configurar(host, puerto, debug=False, ssl=True):
    print(f"Host: {host}, Puerto: {puerto}, Debug: {debug}, SSL: {ssl}")

# Válido: posicionales primero, luego nombrados
configurar("localhost", 8080, debug=True)

# Inválido: nombrados antes que posicionales
# configurar(host="localhost", 8080)  # ❌ SyntaxError
```

## Valores por Defecto

Un parámetro con valor por defecto se vuelve opcional en la llamada. Regla de orden: **los parámetros sin defecto deben preceder a los que sí lo tienen**.

```python
# Definición con valores por defecto
def saludar(nombre, mensaje="Hola", signo="!"):
    """Saluda con mensaje personalizable."""
    print(f"{mensaje}, {nombre}{signo}")

# Llamadas con diferentes niveles de especificidad
saludar("Ana")                    # Hola, Ana!
saludar("Juan", "Buenos días")    # Buenos días, Juan!
saludar("Carlos", "Adiós", "...") # Adiós, Carlos...
saludar(nombre="María", signo="?") # Hola, María?

# Reglas importantes:
def ejemplo(a, b=2, c=3):  # ✅ Correcto: parámetros sin defecto primero
    return a + b + c

# def error(a=1, b, c=3):  # ❌ SyntaxError: parámetro sin defecto después de con defecto
#     pass

print(ejemplo(5))        # 5 + 2 + 3 = 10
print(ejemplo(5, 4))     # 5 + 4 + 3 = 12
print(ejemplo(5, 4, 6))  # 5 + 4 + 6 = 15
```

## Paso por Asignación: Mutabilidad y Efectos Secundarios

Python pasa los argumentos **por asignación**: el parámetro queda ligado al **mismo objeto** que el argumento (no a una copia). La consecuencia depende de la mutabilidad del objeto:

- **Objetos inmutables** (`int`, `str`, `tuple`): reasignar dentro de la función no afecta al exterior; cualquier "modificación" crea un objeto nuevo.
- **Objetos mutables** (`list`, `dict`, `set`): mutarlos en el cuerpo (`.append()`, asignación por índice) **sí** se refleja fuera, porque ambas referencias apuntan al mismo objeto. Esto es un **efecto secundario**.

```python
# ❌ Malo: muta el argumento original (efecto secundario)
def agregar_elemento_malo(lista, elemento):
    lista.append(elemento)  # Modifica la lista original
    return lista

# ✅ Bueno: copia primero, retorna nueva lista
def agregar_elemento_bueno(lista, elemento):
    nueva_lista = lista.copy()
    nueva_lista.append(elemento)
    return nueva_lista
```

> [!warning] Valores por defecto mutables
> Una expresión por defecto se evalúa **una sola vez**, al definir la función, no en cada llamada. Un mutable por defecto se comparte entre todas las llamadas y acumula estado.
> ```python
> def problema(lista=[]):  # ❌ Mala práctica: lista compartida entre llamadas
>     lista.append(1)
>     return lista
>
> print(problema())  # [1]
> print(problema())  # [1, 1] (no [1] como esperarías)
> print(problema())  # [1, 1, 1]
>
> # Solución correcta: centinela None
> def solucion(lista=None):
>     if lista is None:
>         lista = []
>     lista.append(1)
>     return lista
>
> print(solucion())     # [1]
> print(solucion())     # [1]
> print(solucion([2]))  # [2, 1]
> ```

## Parámetros Variables: `*args`

`*args` agrupa un número variable de argumentos **posicionales** en una **tupla**. En la llamada, el operador `*` desempaqueta una secuencia en argumentos individuales.

```python
# *args permite recibir número variable de argumentos posicionales
def sumar_todo(*numeros):
    """Suma cualquier cantidad de números."""
    print(f"Recibidos: {numeros}")  # numeros es una tupla
    return sum(numeros)

# Llamadas con diferente número de argumentos
print(sumar_todo(1, 2))               # 3
print(sumar_todo(1, 2, 3, 4))         # 10
print(sumar_todo(10, 20, 30, 40, 50)) # 150

# Combinación con parámetros normales
def presentar(separador, *nombres):
    """Presenta una lista de nombres."""
    return separador.join(nombres)

print(presentar(" - ", "Ana", "Juan", "Carlos"))  # Ana - Juan - Carlos
print(presentar(", ", "Lunes", "Martes", "Miércoles"))  # Lunes, Martes, Miércoles

# Uso práctico: función de logging
def log(level, *mensajes):
    """Registra mensajes con nivel."""
    print(f"[{level}]", *mensajes)

log("INFO", "Usuario", "ha", "iniciado", "sesión")
log("ERROR", "No se pudo conectar")

# Desempaquetado de secuencias como argumentos
numeros = [1, 2, 3, 4, 5]
print(sumar_todo(*numeros))  # El * desempaqueta la lista
```

## Parámetros Variables: `**kwargs`

`**kwargs` agrupa un número variable de argumentos **nombrados** en un **diccionario**. El operador `**` desempaqueta un diccionario en argumentos nombrados.

```python
# **kwargs permite recibir número variable de argumentos nombrados
def mostrar_datos(**datos):
    """Muestra cualquier cantidad de datos nombrados."""
    print(f"Recibidos: {datos}")  # datos es un diccionario
    for clave, valor in datos.items():
        print(f"  {clave}: {valor}")

# Llamadas con diferentes argumentos nombrados
mostrar_datos(nombre="Ana", edad=28)
mostrar_datos(producto="Laptop", precio=1200, stock=10)

# Combinación con parámetros normales y *args
def crear_perfil_completo(tipo, *habilidades, **metadata):
    """Crea un perfil con habilidades y metadatos."""
    print(f"Tipo de perfil: {tipo}")
    print(f"Habilidades: {habilidades}")
    print(f"Metadatos: {metadata}")
    print("-" * 30)

crear_perfil_completo(
    "profesional",
    "Python", "SQL", "Git",
    nombre="Ana",
    experiencia=5,
    empresa="Tech Corp"
)

# Desempaquetado de diccionarios
config = {
    "host": "localhost",
    "port": 8080,
    "debug": True
}

def conectar(host, port, debug):
    print(f"Conectando a {host}:{port}, debug={debug}")

conectar(**config)  # Desempaqueta el diccionario como kwargs
```

## Parámetros Solo Posicionales y Solo Nombrados

Python 3.8+ permite restringir el modo de paso con dos marcadores en la firma: `/` cierra los parámetros que serán **solo posicionales**; `*` abre los que serán **solo nombrados**.

```python
# Python 3.8+ introduce / y * para mayor control

# Parámetros solo posicionales (antes de /)
def dividir(numerador, denominador, /):
    """Los parámetros antes de / son SOLO posicionales."""
    return numerador / denominador

# Válido
print(dividir(10, 2))     # 5.0
# Inválido
# print(dividir(numerador=10, denominador=2))  # ❌ TypeError

# Parámetros solo nombrados (después de *)
def configurar(*, host, port):
    """Los parámetros después de * son SOLO nombrados."""
    print(f"Config: {host}:{port}")

# Válido
configurar(host="localhost", port=8080)
# Inválido
# configurar("localhost", 8080)  # ❌ TypeError

# Combinación de ambos
def procesar(datos, /, opciones=None, *, verbose=False):
    """
    - datos: solo posicional
    - opciones: posicional o nombrado
    - verbose: solo nombrado
    """
    print(f"Datos: {datos}")
    print(f"Opciones: {opciones}")
    print(f"Verbose: {verbose}")

# Todas válidas
procesar([1, 2, 3])
procesar([1, 2, 3], {"modo": "rápido"})
procesar([1, 2, 3], opciones={"modo": "rápido"}, verbose=True)
```

## Resumen de Modos de Paso

| Forma en la firma | Recibe | Tipo en el cuerpo | Restricción |
|-------------------|--------|-------------------|-------------|
| `param` | posicional o nombrado | el valor pasado | — |
| `param=valor` | opcional con defecto | el valor o el defecto | sin-defecto van antes |
| `*args` | posicionales sobrantes | tupla | — |
| `**kwargs` | nombrados sobrantes | diccionario | va al final |
| antes de `/` | solo posicional | — | no admite `param=` |
| después de `*` | solo nombrado | — | obliga `param=` |
