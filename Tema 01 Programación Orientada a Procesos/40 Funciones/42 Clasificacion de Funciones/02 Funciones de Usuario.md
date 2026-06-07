---
title: Funciones de Usuario
order: 2
draft: false
tags:
  - python
  - teoria
  - funciones
---
# Funciones de Usuario

Las **funciones definidas por el usuario** se crean con `def` para encapsular lógica reutilizable. Admiten parámetros, retornos, anidamiento, y al ser objetos de primera clase pueden asignarse a variables, pasarse como argumentos y almacenarse en estructuras de datos.

## Funciones básicas

```python
# Función más simple
def saludar():
    """Función sin parámetros ni retorno."""
    print("¡Hola!")

saludar()  # ¡Hola!

# Función con parámetros
def saludar_persona(nombre):
    """Función con un parámetro."""
    print(f"¡Hola, {nombre}!")

saludar_persona("Ana")  # ¡Hola, Ana!

# Función con retorno
def suma(a, b):
    """Función que retorna un valor."""
    return a + b

resultado = suma(5, 3)
print(f"Suma: {resultado}")  # Suma: 8

# Función con múltiples retornos
def operaciones(a, b):
    """Función que retorna múltiples valores."""
    suma = a + b
    resta = a - b
    multi = a * b
    div = a / b if b != 0 else None
    return suma, resta, multi, div

s, r, m, d = operaciones(10, 3)
print(f"10 y 3: +{s} -{r} *{m} /{d}")
```

## Parámetros avanzados

El detalle completo de patrones de argumentos (posicionales, por defecto, `*args`, `**kwargs`, keyword-only) se trata en [[index | Patrones de Argumentos]]; aquí va el panorama mínimo.

```python
# Parámetros con valores por defecto
def crear_perfil(nombre, edad, ciudad="Desconocida", activo=True):
    """Crea un perfil con valores por defecto."""
    return {
        "nombre": nombre,
        "edad": edad,
        "ciudad": ciudad,
        "activo": activo
    }

print(crear_perfil("Ana", 25))
print(crear_perfil("Juan", 30, "Madrid"))
print(crear_perfil("Carlos", 22, activo=False))

# *args - número variable de argumentos posicionales
def sumar_todos(*numeros):
    """Suma cualquier cantidad de números."""
    return sum(numeros)

print(sumar_todos(1, 2))           # 3
print(sumar_todos(1, 2, 3, 4, 5))  # 15

# **kwargs - número variable de argumentos nombrados
def mostrar_datos(**datos):
    """Muestra datos con nombre."""
    for clave, valor in datos.items():
        print(f"{clave}: {valor}")

mostrar_datos(nombre="Ana", edad=25, ciudad="Madrid")
```

## Funciones anidadas

Una función puede definirse dentro de otra. La función interna existe solo en el ámbito de la externa y accede a sus variables locales (mecanismo base de los [[08 Closures | closures]]).

```python
def operacion_matematica(x, y, operacion="suma"):
    """Función que contiene funciones anidadas."""

    def suma():
        return x + y

    def resta():
        return x - y

    def multiplicacion():
        return x * y

    if operacion == "suma":
        return suma()
    elif operacion == "resta":
        return resta()
    elif operacion == "multiplicacion":
        return multiplicacion()
    else:
        return None

print(operacion_matematica(10, 5, "suma"))           # 15
print(operacion_matematica(10, 5, "multiplicacion")) # 50
```

## Funciones como objetos de primera clase

Las funciones son objetos: se asignan a variables, se pasan como argumentos (ver [[07 Funciones de Orden Superior | orden superior]]), se retornan y se guardan en estructuras de datos.

```python
# Las funciones son objetos de primera clase
def saludar():
    return "Hola"

# Asignar función a variable
mi_funcion = saludar
print(mi_funcion())  # Hola

# Pasar función como argumento
def aplicar_operacion(func, a, b):
    return func(a, b)

def suma(a, b):
    return a + b

def resta(a, b):
    return a - b

print(aplicar_operacion(suma, 10, 5))   # 15
print(aplicar_operacion(resta, 10, 5))  # 5

# Retornar funciones
def seleccionar_operacion(operacion):
    if operacion == "suma":
        return suma
    elif operacion == "resta":
        return resta
    else:
        return None

operacion = seleccionar_operacion("suma")
print(operacion(10, 5))  # 15

# Almacenar funciones en estructuras de datos
operaciones = {
    "suma": suma,
    "resta": resta
}
print(operaciones["suma"](10, 5))  # 15
```

## Buenas prácticas

```python
# ✅ Funciones pequeñas y enfocadas
def validar_email(email):
    return '@' in email and '.' in email

def enviar_notificacion(usuario, mensaje):
    if validar_email(usuario.email):
        # Enviar...
        pass

# ✅ Documentar funciones complejas
def procesar_datos(datos):
    """
    Procesa datos y retorna estadísticas.

    Args:
        datos (list): Lista de números

    Returns:
        dict: Estadísticas calculadas
    """
    return {
        'suma': sum(datos),
        'media': sum(datos) / len(datos),
        'max': max(datos),
        'min': min(datos)
    }
```
