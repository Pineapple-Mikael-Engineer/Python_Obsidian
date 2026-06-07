---
title: Archivos .py como Módulos
order: 1
tags:
  - python
  - teoria
  - modulos
draft: false
aliases:
  - Modulos como archivos
  - .py files as modules
---

# Archivos .py como Módulos

> [!definicion]
> En Python **todo archivo `.py` es un módulo**: una unidad importable por su **nombre sin la extensión**. Al importarlo por primera vez, su **código de nivel superior se ejecuta una sola vez** —de arriba abajo— y los nombres que define (variables, funciones, clases) quedan disponibles como atributos del módulo. No hay que declarar nada: basta con que el archivo exista y sea alcanzable.

```python
# saludos.py
print("inicializando saludos")   # codigo de nivel superior: corre al importar
IDIOMA = "es"

def hola(nombre):
    return f"Hola, {nombre}"

# main.py
import saludos                   # imprime "inicializando saludos"
saludos.hola("Ada")             # "Hola, Ada"
saludos.IDIOMA                   # "es"
```

El nombre del módulo es el del archivo **sin `.py`**: `saludos.py` se importa como `import saludos`. Por eso los nombres de archivo se eligen como identificadores válidos (sin espacios ni guiones).

## El código de nivel superior se ejecuta una vez

> [!regla]
> La primera importación **ejecuta** el módulo entero; las siguientes **no lo vuelven a ejecutar**, porque queda guardado en la caché `sys.modules`. Importar es, conceptualmente, "ejecutar el archivo una vez y quedarse con su namespace".

```python
import saludos    # "inicializando saludos"  -> primera vez: ejecuta
import saludos    # (silencio)               -> ya cacheado, no reejecuta
```

> [!warning]
> El código de nivel superior corre en el **momento del import**, no cuando se usa el módulo. Poner ahí trabajo costoso (leer archivos, abrir conexiones) ralentiza cualquier `import`. Conviene dejar en el nivel superior solo definiciones y constantes; lo ejecutable, dentro de funciones.

## Qué cuenta como "nivel superior"

> [!info]
> Es nivel superior todo lo que **no** está anidado dentro de una función o clase: las sentencias con sangría cero. Las definiciones `def`/`class` se *ejecutan* (crean el objeto función/clase) pero su **cuerpo** no corre hasta que se llaman o instancian.

```python
# config.py
DEBUG = True                     # nivel superior: corre al importar

def cargar():                    # se define al importar...
    print("leyendo disco")       # ...pero esto NO corre hasta cargar()

# import config                  -> no imprime "leyendo disco"
# config.cargar()                -> ahora si
```

El archivo aislado importable es el ladrillo de la modularidad; lo que mantiene sus nombres separados de los demás es su [[02 Namespace del Modulo | namespace propio]], y el truco para que ese mismo archivo sirva como script y como módulo es [[03 __name__ y __main__ | `__name__` y `__main__`]].
