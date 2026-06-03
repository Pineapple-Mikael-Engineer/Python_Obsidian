---
title: Nonlocal
tags:
  - python
  - teoria
  - ambito
draft: false
aliases:
  - Palabra clave nonlocal
  - Ámbito enclosing
  - Enclosing scope
---

# Nonlocal

> [!definicion]
> `nonlocal <nombre>` se usa en una función anidada para enlazar un nombre con la variable del ámbito **enclosing** más cercano (una función contenedora), no con el global ni con uno local nuevo. Habilita su **reasignación** desde la función interna. El nombre **debe existir previamente** en algún ámbito enclosing; si no, se produce `SyntaxError`.

> [!info]
> `nonlocal` cubre el nivel **E** de la [[03 Regla LEGB | regla LEGB]], el único que ni la asignación por defecto ni [[02 Variables Globales | global]] permiten modificar. Es el mecanismo sobre el que se construyen los [[08 Closures | closures]] con estado.

---

## Uso básico

```python
def exterior():
    mensaje = "Hola desde exterior"
    contador = 0

    def interior():
        nonlocal mensaje, contador
        mensaje = "Modificado desde interior"
        contador += 1
        print(f"Interior llamada #{contador}: {mensaje}")

    print(f"Antes: {mensaje}")
    interior()
    interior()
    print(f"Después: {mensaje}")

exterior()
# Salida:
# Antes: Hola desde exterior
# Interior llamada #1: Modificado desde interior
# Interior llamada #2: Modificado desde interior
# Después: Modificado desde interior
```

Sin `nonlocal`, la asignación a `mensaje` dentro de `interior` crearía una local y el ámbito exterior no se vería afectado.

---

## Local vs nonlocal vs global

```python
x = "global"

def exterior():
    x = "enclosing"

    def interior():
        x = "local"
        print(f"Dentro interior (local): {x}")

    interior()
    print(f"Dentro exterior: {x}")

exterior()
print(f"Global: {x}")

print("-" * 30)

# Con nonlocal
def exterior_nonlocal():
    x = "enclosing"

    def interior_nonlocal():
        nonlocal x
        x = "modificado con nonlocal"
        print(f"Dentro interior (nonlocal): {x}")

    interior_nonlocal()
    print(f"Dentro exterior: {x}")

exterior_nonlocal()
print(f"Global: {x}")  # No afectada
```

Sin `nonlocal`, `interior` crea una local que muere al retornar; con `nonlocal`, modifica la variable de `exterior`. En ningún caso se toca el `x` global.

---

## nonlocal vs global en funciones anidadas

> [!info]
> Una misma función interna puede declarar simultáneamente `global` para un nombre (apuntando al módulo) y `nonlocal` para otro (apuntando al enclosing).

```python
x = 100

def exterior():
    x = 10
    y = 20

    def interior():
        global x  # Se refiere a la global
        nonlocal y  # Se refiere a y de exterior

        x = 999  # Modifica global
        y = 999  # Modifica y de exterior

        print(f"Interior - x (global): {x}, y: {y}")

    print(f"Antes - x (exterior): {x}, y: {y}, x global: {globals()['x']}")
    interior()
    print(f"Después - x (exterior): {x}, y: {y}, x global: {globals()['x']}")

exterior()
```

---

## Múltiples niveles de anidamiento

`nonlocal` enlaza con el ámbito enclosing **más cercano** que defina el nombre. No alcanza más de un nivel de salto sin que el nivel intermedio también lo declare.

```python
def nivel1():
    a = "a de nivel1"
    b = "b de nivel1"

    def nivel2():
        a = "a de nivel2"  # Sombra a nivel1.a
        c = "c de nivel2"

        def nivel3():
            nonlocal a  # Modifica a de nivel2, NO nivel1
            nonlocal c  # c está en nivel2
            a = "modificado desde nivel3"
            c = "modificado desde nivel3"

            # Para modificar b de nivel1, necesitaríamos nonlocal en nivel2
            print(f"Nivel3 - a: {a}, c: {c}")

        print(f"Antes de nivel3 - a: {a}, c: {c}")
        nivel3()
        print(f"Después de nivel3 - a: {a}, c: {c}")

    print(f"Antes de nivel2 - a: {a}, b: {b}")
    nivel2()
    print(f"Después de nivel2 - a: {a}, b: {b}")

nivel1()
```

---

## nonlocal con variables inexistentes

> [!warning]
> `nonlocal x` exige que `x` ya esté ligado en un ámbito enclosing. Si ningún contenedor lo define, el error se detecta al compilar la función (`SyntaxError: no binding for nonlocal 'x'`).

```python
def exterior():
    # x no está definida en exterior
    def interior():
        nonlocal x  # ❌ SyntaxError: no binding for nonlocal 'x'
        x = 10

    interior()

try:
    exterior()
except SyntaxError as e:
    print(f"Error: {e}")

# Correcto
def exterior_correcto():
    x = 0  # Definir en enclosing
    def interior():
        nonlocal x
        x = 10
    interior()
    print(f"x modificada: {x}")

exterior_correcto()
```

---

## Relación con closures

> [!info]
> Una función interna que captura y modifica una variable enclosing mediante `nonlocal` conserva ese estado entre llamadas: el ámbito enclosing sobrevive mientras la función interna referenciada exista. Este patrón es la base de los [[08 Closures | closures]] con estado mutable y una alternativa al estado global descrita en [[02 Variables Globales | Variables Globales]].

### Contador con paso configurable

```python
def crear_contador_pasos():
    """Crea un contador con paso configurable."""
    contador = 0

    def incrementar(paso=1):
        nonlocal contador
        contador += paso
        return contador

    def decrementar(paso=1):
        nonlocal contador
        contador -= paso
        return contador

    def obtener_valor():
        return contador

    def resetear():
        nonlocal contador
        contador = 0

    # Retornar múltiples funciones para manipular el contador
    return incrementar, decrementar, obtener_valor, resetear

inc, dec, val, reset = crear_contador_pasos()

print(f"Valor inicial: {val()}")
inc()
inc(2)
print(f"Después de inc: {val()}")  # 3
dec()
print(f"Después de dec: {val()}")  # 2
reset()
print(f"Después de reset: {val()}")  # 0
```

### Acumulador con historial

`nonlocal` es necesario para reasignar `total` (inmutable); `historial` se muta in-place sin declararlo.

```python
def crear_acumulador():
    """Crea un acumulador que suma números."""
    total = 0
    historial = []

    def acumular(numero):
        nonlocal total
        total += numero
        historial.append(numero)  # historial es de enclosing
        return total

    def obtener_historial():
        return historial.copy()

    def obtener_total():
        return total

    return acumular, obtener_historial, obtener_total

acumular, hist, total = crear_acumulador()

print(acumular(5))   # 5
print(acumular(3))   # 8
print(acumular(10))  # 18
print(f"Historial: {hist()}")  # [5, 3, 10]
print(f"Total final: {total()}")  # 18
```

### Temporizador encapsulado

```python
def crear_temporizador():
    inicio = None

    def empezar():
        nonlocal inicio
        import time
        inicio = time.time()

    def detener():
        nonlocal inicio
        if inicio:
            import time
            transcurrido = time.time() - inicio
            inicio = None
            return transcurrido
        return 0

    return empezar, detener

empezar, detener = crear_temporizador()
empezar()
import time
time.sleep(0.1)
print(f"Tiempo: {detener():.3f}s")
```

---

## Relación con otras notas

- `nonlocal` cubre el nivel Enclosing de la [[03 Regla LEGB | regla LEGB]].
- Para modificar el ámbito de módulo, no el enclosing, se usa [[02 Variables Globales | global]].
- El patrón de captura de estado se formaliza en [[08 Closures | Closures]].
