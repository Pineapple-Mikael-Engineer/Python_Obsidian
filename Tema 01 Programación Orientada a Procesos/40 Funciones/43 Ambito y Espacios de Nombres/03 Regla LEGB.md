---
title: Regla LEGB
order: 3
tags:
  - python
  - teoria
  - ambito
draft: false
aliases:
  - LEGB rule
  - Resolución de nombres
  - Orden de búsqueda de nombres
---

# Regla LEGB

> [!definicion]
> La **regla LEGB** describe el orden en que Python resuelve un nombre referenciado: busca en el ámbito **L**ocal, luego en los **E**nclosing (funciones contenedoras), luego en el **G**lobal (módulo) y finalmente en los **B**uilt-in (nombres predefinidos). El primer ámbito donde el nombre exista determina el valor; si no aparece en ninguno, se lanza `NameError`.

| Nivel | Alcance | Origen |
|:------|:--------|:-------|
| **L** — Local | Cuerpo de la función actual | Asignación dentro de la función |
| **E** — Enclosing | Funciones que contienen a la actual (anidadas) | Variables de la función externa |
| **G** — Global | Nivel de módulo | Definidas fuera de toda función |
| **B** — Built-in | Todo Python | `len`, `print`, `range`, `dict`... |

> [!info]
> La búsqueda LEGB aplica a la **lectura** de nombres. La **escritura** (asignación) crea por defecto en el ámbito Local; alterarlo requiere [[02 Variables Globales | global]] o [[04 Nonlocal | nonlocal]].

---

## Demostración de los cuatro niveles

```python
# Built-in
print(len)  # <built-in function len>

# Global
x = "global"

def funcion_exterior():
    # Enclosing
    x = "enclosing"

    def funcion_interior():
        # Local
        x = "local"
        print("Dentro de interior:", x)

    funcion_interior()
    print("Dentro de exterior:", x)

funcion_exterior()
print("Global:", x)

# Salida:
# Dentro de interior: local
# Dentro de exterior: enclosing
# Global: global
```

Cada `print` resuelve `x` en el ámbito más cercano que lo defina: la interior ve su Local, la exterior su Enclosing, y el módulo el Global.

---

## Ejemplo combinando los cuatro ámbitos

```python
# Built-in: cualquier función built-in
print("Built-in: print está disponible")

# Global
animal = "perro"
comida = "croquetas"

def zoo():
    # Enclosing
    animal = "gato"
    vegetal = "lechuga"  # Nueva variable en enclosing

    def alimentar():
        # Local
        comida = "pescado"

        # Búsqueda LEGB:
        print(f"Alimentar: {comida}")          # Local: pescado
        print(f"Animal: {animal}")             # Enclosing: gato
        print(f"Vegetal: {vegetal}")           # Enclosing: lechuga
        print(f"Global original: {globals()['animal']}")  # Global: perro

        # Built-in (len, print, etc.)
        print(f"Longitud: {len(comida)}")      # Built-in

    alimentar()

zoo()
```

`comida` se resuelve Local; `animal` y `vegetal` en Enclosing; el `animal` global solo es accesible explícitamente vía `globals()` porque el Enclosing lo oculta; `len` y `print` son Built-in.

---

## Trazado de la búsqueda por niveles

```python
# Función para trazar la búsqueda LEGB
def trazar_legb(nombre, profundidad=0):
    """
    Muestra cómo Python busca una variable.
    """
    indent = "  " * profundidad
    print(f"{indent}Buscando '{nombre}'...")

    # Simular búsqueda en cada nivel
    print(f"{indent}  Local: {'Encontrada' if nombre in locals() else 'No encontrada'}")
    print(f"{indent}  Enclosing: {'Encontrada' if nombre in globals() else 'No encontrada'}")
    print(f"{indent}  Global: {'Encontrada' if nombre in globals() else 'No encontrada'}")
    print(f"{indent}  Built-in: {'Encontrada' if nombre in dir(__builtins__) else 'No encontrada'}")

# Demostración
x = 100  # Global

def nivel1():
    y = 200  # Enclosing para nivel2

    def nivel2():
        z = 300  # Local para nivel2
        trazar_legb('z', 1)  # z local
        trazar_legb('y', 1)  # y enclosing
        trazar_legb('x', 1)  # x global
        trazar_legb('print', 1)  # print built-in

    nivel2()

nivel1()
```

---

## Relación con otras notas

- El nivel **L** y el ocultamiento de niveles superiores se desarrolla en [[01 Variables Locales | Variables Locales]].
- El nivel **G** y cómo escribir en él se trata en [[02 Variables Globales | Variables Globales]].
- El nivel **E** y cómo escribir en él se trata en [[04 Nonlocal | Nonlocal]].
