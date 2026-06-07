---
title: __format__
order: 2
tags:
  - python
  - teoria
  - dunder
draft: false
aliases:
  - format dunder
  - Protocolo de formato
---

# `__format__`

> [!definicion]
> `__format__(self, format_spec)` controla cómo responde el objeto a `format(obj, spec)` y a las f-strings `f"{obj:spec}"`. Recibe en `format_spec` la **parte tras los dos puntos** (el mini-lenguaje de especificación de formato) y devuelve la cadena ya formateada. Con `format_spec` vacío, la convención es delegar en `str(self)`.

```python
f"{obj:spec}"          # equivale a  format(obj, "spec")  ->  obj.__format__("spec")
f"{obj}"               # equivale a  format(obj, "")      ->  delega en str(obj)
```

El `format_spec` es **solo** lo que sigue a los dos puntos: en `f"{t:.1f}"`, el método recibe `".1f"`; en `f"{t:C}"`, recibe `"C"`. El objeto decide cómo interpretarlo, sea el formato estándar de Python o un mini-lenguaje propio.

## Ejemplo: una clase con especificadores propios

```python
class Temperatura:
    def __init__(self, celsius):
        self.c = celsius
    def __str__(self):
        return f"{self.c} °C"
    def __format__(self, spec):
        if spec == "" or spec.endswith("C"):
            valor, unidad = self.c, "°C"
            spec = spec[:-1] if spec.endswith("C") else spec
        elif spec.endswith("F"):
            valor, unidad = self.c * 9/5 + 32, "°F"
            spec = spec[:-1]
        elif spec.endswith("K"):
            valor, unidad = self.c + 273.15, "K"
            spec = spec[:-1]
        else:                                   # spec numérico puro -> sobre °C
            return format(self.c, spec)
        return f"{format(valor, spec)} {unidad}"

t = Temperatura(25)
f"{t}"            # '25 °C'        -> spec vacío, delega en __str__
f"{t:.1f}"        # '25.0'         -> spec numérico estándar sobre el valor en °C
f"{t:.1fF}"       # '77.0 °F'      -> conversión propia + formato numérico
f"{t:K}"          # '298.15 K'     -> spec propio sin formato numérico
```

El método separa su **mini-lenguaje propio** (sufijos `C`/`F`/`K`) del **formato numérico estándar** que delega en `format(valor, spec)` una vez aislado el número. Reusar el `format` interno evita reimplementar el manejo de precisión, ancho o relleno.

## Relación con `__str__`

> [!regla]
> Con `format_spec` vacío, `__format__` **debe** producir lo mismo que `str(obj)`. El `object.__format__` heredado lo garantiza: con especificador vacío llama a `str(self)`, y con especificador no vacío lanza `TypeError`. Por eso una clase con solo `__str__` ya responde a `f"{obj}"`, pero falla ante `f"{obj:algo}"` hasta que define `__format__`.

```python
class SoloStr:
    def __str__(self):
        return "X"

f"{SoloStr()}"        # 'X'    -> object.__format__ con spec vacío -> str()
f"{SoloStr():>5}"     # TypeError: unsupported format string passed to SoloStr.__format__
```

## Cadena de delegación

| Expresión | Ruta |
| --------- | ---- |
| `f"{obj}"` | `__format__(obj, "")` → por convención `str(obj)` → `__str__` (o `__repr__` como *fallback*) |
| `f"{obj:spec}"` | `__format__(obj, "spec")`, interpretando el `format_spec` |
| `format(obj, spec)` | `__format__(obj, spec)` directamente |

> [!warning]
> `__format__` debe **devolver** un `str`. Si delega en `format(valor, spec)` con un `spec` inválido para el tipo de `valor`, el `TypeError`/`ValueError` se propaga: conviene validar o restringir el mini-lenguaje aceptado. No confundir con `str.format()`, que es el método de las **cadenas** plantilla, no el dunder del objeto formateado.

## Relación con otras notas

La distinción entre representación legible y no ambigua, y el porqué de delegar lo vacío en `str`, están en [[01 __str__ y __repr__ | __str__ y __repr__]]. El marco de los tres dunders de representación está en [[51 Representacion/index | Representación]].
