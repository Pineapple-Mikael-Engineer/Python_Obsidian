---
title: Context Managers (__enter__, __exit__)
tags:
  - python
  - teoria
  - dunder
draft: false
aliases:
  - Gestor de contexto
  - Context manager
  - Protocolo with
---

# Context Managers (__enter__, __exit__)

> [!definicion]
> Un **gestor de contexto** es un objeto que implementa el protocolo del `with`: `__enter__(self)` **prepara** un recurso al entrar al bloque y devuelve lo que se asigna tras `as`; `__exit__(self, exc_type, exc, tb)` lo **libera** al salir, **siempre**, ocurra una salida normal o una excepción. Garantiza una limpieza **determinista**: archivos cerrados, *locks* liberados, conexiones devueltas, sin depender del recolector de basura.

```python
class Cronometro:
    def __enter__(self):                  # al entrar al with; lo devuelto va tras 'as'
        from time import perf_counter
        self._t0 = perf_counter()
        return self
    def __exit__(self, exc_type, exc, tb):  # al salir, pase lo que pase
        from time import perf_counter
        self.elapsed = perf_counter() - self._t0
        # no devuelve True -> no suprime excepciones

with Cronometro() as cron:
    suma = sum(range(1_000_000))
cron.elapsed                              # 0.02...  -> medido aunque el bloque ya terminó
```

El recurso se adquiere en `__enter__` y se garantiza su liberación en `__exit__`, sin un `try/finally` explícito en el código que lo usa.

## Equivalencia con try/finally

> [!regla]
> `with cm as x: cuerpo` equivale a llamar `x = cm.__enter__()`, ejecutar el cuerpo dentro de un `try`, y llamar `cm.__exit__(...)` en el `finally`. Por eso `__exit__` se ejecuta **siempre**: tras un `return`, un `break`, una excepción o una salida normal.

```python
# with cm as x:
#     cuerpo
# equivale a:
x = cm.__enter__()
try:
    cuerpo
finally:
    cm.__exit__(*sys.exc_info())          # exc_type, exc, tb (o tres None si todo fue bien)
```

## Argumentos de __exit__ y supresión de excepciones

`__exit__` recibe información de la excepción que esté propagándose: `exc_type`, `exc` (la instancia) y `tb` (el *traceback*). Si el bloque terminó sin error, los tres son `None`.

> [!warning]
> El **valor de retorno** de `__exit__` decide el destino de la excepción: si devuelve un valor **verdadero** (`True`), la excepción se **suprime** y la ejecución continúa tras el `with`; si devuelve `False`/`None`, la excepción **se propaga** normalmente. Devolver `True` por descuido **oculta errores**; hazlo solo de forma deliberada.

```python
class Silenciar:
    def __init__(self, *tipos):
        self.tipos = tipos
    def __enter__(self):
        return self
    def __exit__(self, exc_type, exc, tb):
        return exc_type is not None and issubclass(exc_type, self.tipos)  # True -> suprime

with Silenciar(ZeroDivisionError):
    1 / 0                                 # se suprime; el programa sigue
print("continúa")                         # se ejecuta
```

## Orden de ejecución con excepción

> [!info]
> Cuando el cuerpo lanza una excepción dentro del `with`:
> 1. Se interrumpe el cuerpo en el punto del error.
> 2. Se llama a `__exit__` con `(exc_type, exc, tb)` poblados —la **limpieza ocurre igual**—.
> 3. Si `__exit__` devuelve algo falsy, la excepción **se relanza** al salir del `with`; si devuelve `True`, se descarta.
>
> La limpieza está garantizada **antes** de que la excepción siga subiendo por la pila.

## Alternativa: contextlib.contextmanager

> [!ejemplo]
> Un decorador-generador evita escribir una clase con dos dunders: el código **antes** del `yield` es `__enter__`, lo que se hace `yield` es lo que va tras `as`, y el código **después** (idealmente en un `finally`) es `__exit__`.
> ```python
> from contextlib import contextmanager
>
> @contextmanager
> def abrir_recurso(nombre):
>     r = f"<{nombre} abierto>"
>     try:
>         yield r                         # <- lo que recibe el 'as'
>     finally:
>         pass                            # <- limpieza garantizada (__exit__)
>
> with abrir_recurso("db") as r:
>     print(r)                            # <db abierto>
> ```

Este es el tercer protocolo de [[53 Comportamiento de Objeto/index | comportamiento de objeto]]: como `__getitem__` da [[01 Contenedores (__len__, __getitem__) | sintaxis de contenedor]] y `__call__` da [[02 Invocable (__call__) | sintaxis de invocación]], `__enter__`/`__exit__` dan la **sintaxis del `with`**. El manejo de la excepción dentro de `__exit__` se relaciona con el [[03 Control de Flujo/index | control de flujo]] de `try/except/finally`.
