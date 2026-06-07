---
title: Composición vs Herencia
order: 76
tags:
  - python
  - teoria
  - relaciones
draft: false
aliases:
  - Composicion vs Herencia
  - Composición sobre herencia
  - Composition over inheritance
---

# Composición vs Herencia

> [!definicion]
> Ante la necesidad de **reutilizar comportamiento**, hay dos caminos. La **herencia** modela **"es un"**: la subclase **hereda** la implementación del padre y queda **acoplada** a ella. La **composición** modela **"tiene un"**: una clase **contiene** un colaborador y le **delega** trabajo. La composición es más **flexible** (el colaborador es intercambiable, incluso en *runtime*) y produce **menos acoplamiento**.

```python
# Herencia: Coche ES UN Motor (forzado, incorrecto)
class Coche(Motor): ...

# Composición: Coche TIENE UN Motor (delegación)
class Coche:
    def __init__(self, motor):
        self._motor = motor                  # colaborador inyectado
    def arrancar(self):
        return self._motor.encender()        # delega
```

## El principio: composición sobre herencia

> [!regla]
> **"Prefiere composición sobre herencia"**: usa herencia **solo** cuando exista un **verdadero subtipo** (la subclase puede sustituir al padre sin romper nada — **principio de sustitución de Liskov**). Si dudas, **compón**: contener y delegar casi nunca es peor, y evita la rigidez de la jerarquía.

## Por qué la herencia es frágil

> [!warning]
> La herencia **acopla a la implementación** del padre, no solo a su interfaz:
> - Un cambio interno en la base puede **romper** las subclases (*fragile base class*).
> - La jerarquía es **rígida**: se fija en tiempo de definición y no se cambia en *runtime*.
> - Tienta a heredar **por reutilizar código**, no porque haya una relación "es un" real, generando subtipos que **no respetan Liskov**.

## Tabla comparativa

| Criterio | Herencia ("es un") | Composición ("tiene un") |
| -------- | ------------------ | ------------------------ |
| Acoplamiento | Fuerte: a la implementación del padre | Débil: solo a la interfaz del colaborador |
| Reutilización | Heredar todo el linaje (también lo que no se quiere) | Delegar solo lo necesario |
| Flexibilidad | Rígida, fijada en la definición | Intercambiable, incluso en *runtime* |
| `self` | Una sola identidad compartida | Objetos distintos que colaboran |
| Cuándo usarla | Subtipo real que respeta Liskov | Reutilizar comportamiento sin "es un" |

## Refactorizar herencia mala a composición

> [!ejemplo]
> Una `PilaConLista(list)` hereda de `list` **para reutilizar** su almacenamiento, pero **expone** toda la API de lista (`insert`, `__getitem__`...): viola "es un", porque una pila **no es** una lista. La solución es **contener** una lista y delegar solo lo que una pila necesita.
>
> ```python
> # Mala herencia: expone insert, sort, indexado... que rompen la pila
> class PilaConLista(list):
>     def push(self, x): self.append(x)
>     def pop_top(self): return self.pop()
>
> # Composición: la lista es un detalle interno, la interfaz queda acotada
> class Pila:
>     def __init__(self):
>         self._datos = []                 # TIENE UN almacenamiento
>     def push(self, x): self._datos.append(x)
>     def pop(self): return self._datos.pop()
>     def vacia(self): return not self._datos
> ```
>
> La versión compuesta **oculta** la lista, ofrece **solo** las operaciones de pila y permite cambiar el almacenamiento (un `deque`) sin alterar la interfaz pública.

La composición se concreta en las relaciones de [[71 Composicion | composición]] y [[72 Agregacion | agregación]]; la alternativa heredada es la [[30 Herencia/index | herencia]]. Cuando lo que se quiere es **inyectar una capacidad transversal sin estado**, ni una ni otra: un [[75 Mixins | mixin]].
