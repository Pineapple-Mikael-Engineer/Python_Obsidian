---
title: __str__ y __repr__
order: 1
tags:
  - python
  - teoria
  - dunder
draft: false
aliases:
  - str y repr
  - Representación legible y no ambigua
---

# `__str__` y `__repr__`

> [!definicion]
> `__repr__(self)` devuelve la representación **no ambigua** del objeto, orientada al desarrollador: idealmente código que **reconstruye** el objeto. `__str__(self)` devuelve la representación **legible** para el usuario final. Ambos retornan `str`; `__repr__` es el *fallback* de `__str__`.

```python
class Fecha:
    def __init__(self, d, m, a):
        self.d, self.m, self.a = d, m, a
    def __repr__(self):
        return f"Fecha({self.d}, {self.m}, {self.a})"   # no ambigua
    def __str__(self):
        return f"{self.d:02d}/{self.m:02d}/{self.a}"     # legible

f = Fecha(3, 6, 2026)
str(f)                 # '03/06/2026'        -> __str__
repr(f)                # 'Fecha(3, 6, 2026)' -> __repr__
print(f)               # 03/06/2026          -> print usa __str__
f                      # Fecha(3, 6, 2026)   -> la consola usa __repr__
```

## Quién invoca a cada uno

| Sintaxis / función | Invoca | Notas |
| ------------------ | ------ | ----- |
| `repr(obj)` | `__repr__` | siempre |
| consola interactiva (eco de `obj`) | `__repr__` | el REPL muestra el `repr` |
| `repr` de un contenedor: `[obj]`, `{obj}` | `__repr__` | listas, dicts, etc. usan el `repr` de sus elementos |
| `str(obj)` | `__str__` | si no existe, `__repr__` |
| `print(obj)` | `__str__` | si no existe, `__repr__` |
| `f"{obj}"`, `"{}".format(obj)` | `__str__` (vía `__format__`) | especificador vacío delega en `str()` |

> [!regla]
> Si solo vas a definir **uno**, define `__repr__`: es el *fallback* universal y cubre la consola, la depuración y los contenedores. `__str__` no tiene *fallback* hacia `__repr__` en sentido inverso: definir solo `__str__` deja la consola y el `repr` con la representación por defecto.

## El fallback en acción

Cuando una clase define `__repr__` pero **no** `__str__`, toda operación que requiera `str` recae en `__repr__`. La relación inversa no existe.

```python
class Solo:
    def __init__(self, n):
        self.n = n
    def __repr__(self):
        return f"Solo({self.n})"

s = Solo(7)
str(s)        # 'Solo(7)'   -> str() cae en __repr__
print(s)      # Solo(7)     -> print cae en __repr__
repr(s)       # 'Solo(7)'
```

```python
class SoloStr:
    def __str__(self):
        return "legible"

x = SoloStr()
print(x)      # legible
x             # <__main__.SoloStr object at 0x...>  -> __repr__ NO cae en __str__
```

## El ideal de `__repr__`: reproducibilidad

> [!info]
> Por convención, `__repr__` debería devolver una cadena que, evaluada, **recree** el objeto: `eval(repr(obj)) == obj`. No siempre es posible (objetos con estado interno no serializable, referencias externas); cuando no lo sea, se usa la forma angular descriptiva `<Clase ...>` con los datos clave entre los signos.

```python
class Vector:
    def __init__(self, x, y):
        self.x, self.y = x, y
    def __repr__(self):
        return f"Vector({self.x!r}, {self.y!r})"   # !r aplica repr a cada campo
    def __eq__(self, otro):
        return (self.x, self.y) == (otro.x, otro.y)

v = Vector(1, 2)
eval(repr(v)) == v     # True  -> repr reproduce el objeto
```

El conversor `!r` dentro de la f-string fuerza el `repr` de cada componente, garantizando que cadenas internas salgan entrecomilladas y el resultado sea evaluable. La comparación `== v` exige que la clase implemente `__eq__`, parte de la [[52 Sobrecarga de Operadores/index | sobrecarga de operadores]].

> [!warning]
> `__repr__` y `__str__` deben **devolver** un `str`, no imprimirlo. Retornar otro tipo lanza `TypeError`. Tampoco deben tener efectos secundarios: se invocan en depuración, *logging* y trazas, donde alterar estado sería inesperado.

## Relación con otras notas

El especificador de formato `f"{obj:spec}"` lo gobierna [[02 __format__ | __format__]], que con especificador vacío delega en `__str__`. El marco general y la tabla de invocaciones está en [[51 Representacion/index | Representación]].
