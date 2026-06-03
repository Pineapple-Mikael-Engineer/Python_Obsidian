---
title: 06 Decoradores
draft: false
tags:
  - python
  - teoria
  - funciones
---
# Decoradores

Un **decorador** es una función de orden superior que envuelve a otra para extender o alterar su comportamiento sin modificar su código fuente. Recibe la función original, define un `wrapper` que la rodea, y retorna ese `wrapper`. La sintaxis `@decorador` es azúcar para `func = decorador(func)`.

## Estructura y azúcar sintáctico

```python
import functools

def cronometro(func):
    @functools.wraps(func)              # Preserva __name__, __doc__ del original
    def wrapper(*args, **kwargs):       # Acepta cualquier firma
        import time
        inicio = time.perf_counter()
        resultado = func(*args, **kwargs)
        print(f"{func.__name__} tardó {time.perf_counter() - inicio:.6f}s")
        return resultado
    return wrapper

# @decorador es azúcar sintáctico para: func = decorador(func)
@cronometro
def calcular(n):
    return sum(i ** 2 for i in range(n))

calcular(1_000_000)
# calcular tardó 0.0823s

# Equivalencia explícita (sin la sintaxis @)
def saludar(nombre):
    return f"Hola, {nombre}"
saludar = cronometro(saludar)
```

> [!warning] Preservación de metadatos
> Sin `@functools.wraps(func)`, la función decorada expone los metadatos del `wrapper` (`__name__` sería `"wrapper"`, `__doc__` se perdería), lo que rompe la introspección y la documentación. `functools.wraps` copia esos atributos desde la función original.

## Decoradores con argumentos

Un decorador parametrizado requiere **tres niveles** de anidamiento: la fábrica recibe los argumentos del decorador, retorna el decorador real, que a su vez retorna el `wrapper`.

```python
import functools

def repetir(veces):                          # Nivel 1: recibe el argumento
    def decorador(func):                     # Nivel 2: recibe la función
        @functools.wraps(func)
        def wrapper(*args, **kwargs):        # Nivel 3: envuelve la llamada
            for _ in range(veces):
                resultado = func(*args, **kwargs)
            return resultado
        return wrapper
    return decorador

@repetir(veces=3)
def log(mensaje):
    print(f"[LOG] {mensaje}")

log("evento")   # repetir(3)(log) -> imprime 3 veces

# Decorador de log con registro de argumentos
def registrar(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        print(f"Llamando {func.__name__}({args}, {kwargs})")
        valor = func(*args, **kwargs)
        print(f"-> retornó {valor!r}")
        return valor
    return wrapper

@registrar
def dividir(a, b):
    return a / b

dividir(10, 2)
# Llamando dividir((10, 2), {})
# -> retornó 5.0
```

## Decoradores integrados

Python incorpora decoradores de uso frecuente en la definición de clases. `@property` expone un método como atributo de solo lectura, `@classmethod` recibe la clase como primer argumento, y `@staticmethod` define un método sin `self` ni `cls`.

```python
class Circulo:
    def __init__(self, radio):
        self._radio = radio

    @property                # Acceso como atributo: c.area, sin paréntesis
    def area(self):
        return 3.14159 * self._radio ** 2

    @classmethod             # Recibe la clase, no la instancia
    def unitario(cls):
        return cls(radio=1)

    @staticmethod            # Función dentro del namespace de la clase
    def es_valido(radio):
        return radio > 0
```

> [!note]
> El mecanismo de `@property`, `@classmethod` y `@staticmethod` pertenece a la Programación Orientada a Objetos y se desarrolla en [[Clases y Objetos | clases]]. Aquí basta con reconocerlos como decoradores integrados que modifican cómo se accede o se vincula un método.
