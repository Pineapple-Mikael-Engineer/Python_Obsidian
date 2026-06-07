---
title: Importación Circular y Soluciones
order: 4
tags:
  - python
  - teoria
  - modulos
draft: false
aliases:
  - Import circular
  - Circular import
  - Dependencia circular
---

# Importación Circular y Soluciones

> [!definicion]
> Hay **importación circular** cuando dos (o más) módulos se importan **mutuamente**: `a` importa `b` y `b` importa `a`. El problema es que, al importar el primero, Python empieza a ejecutarlo, llega a su `import` del segundo, ejecuta el segundo, que a su vez importa el primero **a medio inicializar** —y encuentra un namespace incompleto. El síntoma típico es un `ImportError` o un `AttributeError` sobre un nombre que "debería existir".

```python
# a.py
from b import f_b                # ejecuta b.py...
def f_a():
    return "a"

# b.py
from a import f_a                # ...pero a.py aun NO definio f_a
def f_b():
    return "b"

# import a   ->  ImportError: cannot import name 'f_a' from partially initialized module 'a'
```

## Por qué falla: el módulo a medio inicializar

> [!regla]
> Python registra el módulo en `sys.modules` **antes** de terminar de ejecutarlo. Si durante su ejecución otro módulo lo reimporta, recibe el **objeto parcial**: las definiciones que aún no se han alcanzado no existen todavía. `from a import f_a` falla porque pide un nombre concreto que aún no está; un `import a` "entero" puede sobrevivir si el nombre solo se usa **más tarde**, en tiempo de llamada.

```python
# señales tipicas de un ciclo de imports:
# ImportError: cannot import name 'X' from partially initialized module
# AttributeError: module 'a' has no attribute 'f_a'
```

## Solución 1 — Import diferido dentro de la función

> [!info]
> Mover el `import` problemático **dentro de la función** que lo necesita lo retrasa hasta el momento de la llamada, cuando ambos módulos ya están completamente inicializados. Es la solución más directa y local.

```python
# b.py
def f_b():
    from a import f_a            # import diferido: corre al llamar, no al importar
    return f_a() + "b"
```

## Solución 2 — Importar el módulo entero, no el nombre

> [!regla]
> Cambiar `from a import f_a` por `import a` y usar `a.f_a()` evita pedir un nombre concreto en tiempo de import. El acceso `a.f_a` se resuelve **al ejecutarse**, momento en que `a` ya está completo. Suele bastar con esto cuando el uso es dentro de funciones.

```python
# b.py
import a                         # trae el modulo, no un nombre suyo
def f_b():
    return a.f_a() + "b"         # a.f_a se resuelve al llamar, ya inicializado
```

## Solución 3 — Reestructurar las dependencias

> [!warning]
> Un ciclo de imports suele ser **síntoma de un mal reparto de responsabilidades**: dos módulos demasiado acoplados. La solución de fondo es **romper la dependencia**: extraer lo común a un tercer módulo del que ambos dependan, o mover el `import` al final del archivo (tras las definiciones). El import diferido cura el síntoma; reestructurar cura la causa.

```text
# en vez de   a <-> b   (ciclo)
# extraer lo compartido a un modulo base:
#     comun.py   <- a.py
#     comun.py   <- b.py        (a y b ya no se importan entre si)
```

La importación circular es el reverso de las formas sanas de importar —[[01 Import Simple | simple]], [[02 Import con Alias | con alias]] y [[03 Import Selectivo (from import) | selectivo]]— y la cura de fondo es de diseño: reducir el acoplamiento entre módulos repartiendo bien las responsabilidades.
