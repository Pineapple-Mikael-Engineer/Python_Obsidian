---
title: Args y Kwargs
draft: false
tags: [python, teoria, funciones]
---
# Args y Kwargs

`*args` recoge los argumentos **posicionales** sobrantes en una **tupla**; `**kwargs` recoge los argumentos **nominales** sobrantes en un **diccionario**. Permiten escribir funciones que aceptan un número variable de argumentos. Los nombres `args`/`kwargs` son convención: lo que opera es el `*` y el `**`.

```python
def f(*args, **kwargs):
    print(args)    # tupla con los posicionales
    print(kwargs)  # dict con los nominales

f(1, 2, x=10, y=20)
# (1, 2)
# {'x': 10, 'y': 20}
```

## `*args` — Posicionales Variables

`*args` recoge en una tupla todos los argumentos posicionales extra.

```python
# *args recoge argumentos posicionales extra en una tupla
def sumar_todos(*numeros):
    """Suma cualquier cantidad de números."""
    print(f"Recibidos: {numeros} (tipo: {type(numeros)})")
    return sum(numeros)

# Llamadas con diferente número de argumentos
print(sumar_todos(1, 2))               # 3
print(sumar_todos(1, 2, 3, 4))         # 10
print(sumar_todos(10, 20, 30, 40, 50)) # 150

# Combinación con parámetros normales
def presentar(separador, *nombres):
    """Presenta una lista de nombres con separador."""
    return separador.join(nombres)

print(presentar(" - ", "Ana", "Juan", "Carlos"))  # Ana - Juan - Carlos
print(presentar(", ", "Lunes", "Martes", "Miércoles"))  # Lunes, Martes, Miércoles

# Ejemplo práctico: logging
def log(level, *mensajes):
    """Registra mensajes con nivel."""
    timestamp = datetime.datetime.now().strftime("%H:%M:%S")
    mensaje_completo = " ".join(str(m) for m in mensajes)
    print(f"[{timestamp}] {level}: {mensaje_completo}")

log("INFO", "Usuario", "Ana", "inició", "sesión")
log("ERROR", "No se pudo conectar a", "base de datos", "en", "localhost")
```

## `**kwargs` — Nominales Variables

`**kwargs` recoge en un diccionario todos los argumentos nominales extra.

```python
# **kwargs recoge argumentos nominales extra en un diccionario
def mostrar_datos(**datos):
    """Muestra cualquier cantidad de datos nombrados."""
    print(f"Recibidos: {datos} (tipo: {type(datos)})")
    for clave, valor in datos.items():
        print(f"  {clave}: {valor}")

# Llamadas con diferentes argumentos nominales
mostrar_datos(nombre="Ana", edad=25)
mostrar_datos(producto="Laptop", precio=1200, stock=10, disponible=True)

# Ejemplo práctico: configuración flexible
def configurar_aplicacion(**opciones):
    """Configura una aplicación con opciones arbitrarias."""
    config = {
        "host": "localhost",
        "port": 8080,
        "debug": False,
        "ssl": False
    }
    # Actualizar con opciones proporcionadas
    config.update(opciones)
    return config

print(configurar_aplicacion(debug=True))
print(configurar_aplicacion(host="192.168.1.100", port=3000, ssl=True))
print(configurar_aplicacion(modo="produccion", cache=True))  # Añade nuevas claves
```

## Combinación de `*args` y `**kwargs`

El orden en la definición es fijo: posicionales normales, `*args`, nominales, `**kwargs`.

```python
def funcion_completa(requerido1, requerido2, *args, **kwargs):
    """Función que acepta todo tipo de argumentos."""
    print(f"Requerido1: {requerido1}")
    print(f"Requerido2: {requerido2}")
    print(f"args: {args}")
    print(f"kwargs: {kwargs}")
    print("-" * 30)

# Llamadas con diferentes combinaciones
funcion_completa(1, 2)
funcion_completa(1, 2, 3, 4, 5)
funcion_completa(1, 2, a=10, b=20)
funcion_completa(1, 2, 3, 4, x=100, y=200)

# Ejemplo real: wrapper/decorador
def temporizador(func):
    """Decorador que mide tiempo de ejecución."""
    import time
    
    def wrapper(*args, **kwargs):
        inicio = time.time()
        resultado = func(*args, **kwargs)
        fin = time.time()
        print(f"{func.__name__} tomó {fin - inicio:.4f}s")
        return resultado
    
    return wrapper

@temporizador
def proceso_lento(n, *valores, **opciones):
    """Proceso que simula ser lento."""
    import time
    time.sleep(0.1)
    suma = sum(valores)
    return suma

proceso_lento(10, 1, 2, 3, 4, verbose=True, cache=False)
```

> [!tip] El patrón `(*args, **kwargs)` es la firma universal de un wrapper: reenvía cualquier llamada a la función envuelta sin conocer su firma. Es la base de los decoradores genéricos.

## Desempaquetado en la Llamada

`*` y `**` también operan al **invocar**: `*` desempaqueta un iterable como argumentos posicionales; `**` desempaqueta un diccionario como argumentos nominales.

```python
# Desempaquetado de listas/tuplas con *
def suma_tres(a, b, c):
    return a + b + c

numeros = [10, 20, 30]
print(suma_tres(*numeros))  # 60 - desempaqueta lista

# También funciona con tuplas, rangos, etc.
tupla = (5, 6, 7)
print(suma_tres(*tupla))  # 18

rango = range(3, 6)  # 3,4,5
print(suma_tres(*rango))  # 12

# Desempaquetado de diccionarios con **
def conectar(host, port, ssl=False):
    print(f"Conectando a {host}:{port}, SSL={ssl}")

config = {
    "host": "localhost",
    "port": 8080,
    "ssl": True
}
conectar(**config)  # Desempaqueta diccionario como kwargs

# Combinación de desempaquetados
def procesar(a, b, c, d, e):
    return a + b + c + d + e

lista1 = [1, 2]
lista2 = [3, 4]
diccionario = {"e": 5}

print(procesar(*lista1, *lista2, **diccionario))  # 15

# En llamadas a funciones
def crear_perfil(nombre, edad, ciudad, *habilidades, **metadata):
    perfil = {
        "nombre": nombre,
        "edad": edad,
        "ciudad": ciudad,
        "habilidades": habilidades,
        "metadata": metadata
    }
    return perfil

# Datos para desempaquetar
datos_basicos = ["Ana", 25, "Madrid"]
habilidades = ["Python", "SQL", "Git"]
metadata = {"experiencia": 5, "empresa": "Tech"}

perfil = crear_perfil(*datos_basicos, *habilidades, **metadata)
print(perfil)
```

## Convenciones

- Usa `*args` para un número variable de argumentos **del mismo tipo** (ej. `sumar(*numeros)`).
- Usa `**kwargs` para **opciones de configuración** arbitrarias que se reenvían o fusionan con defectos.
- Nombres descriptivos: prefiere `**datos` u `**opciones` sobre `**kwargs` cuando el dominio lo permita; dentro accede con `datos.get('nombre')`, no con claves opacas como `kwargs.get('n')`.
- Evita `*args`/`**kwargs` si no son necesarios: para dos números fijos, `def suma_dos(a, b)` es más claro que `def suma(*numeros)`.
