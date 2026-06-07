---
title: __name__ y __main__
order: 3
tags:
  - python
  - teoria
  - modulos
draft: false
aliases:
  - if __name__ == "__main__"
  - Dunder name main
  - Punto de entrada
---

# __name__ y __main__

> [!definicion]
> Cada módulo tiene una variable `__name__` que el intérprete fija automáticamente: vale **el nombre del módulo** cuando se importa (`"saludos"`), o la cadena **`"__main__"`** cuando el archivo se **ejecuta directamente** (`python saludos.py`). Comparar `__name__` con `"__main__"` permite que un mismo archivo sirva a la vez de **script ejecutable** y de **módulo importable**.

```python
# saludos.py
def hola(nombre):
    return f"Hola, {nombre}"

if __name__ == "__main__":       # solo al ejecutar el archivo directo
    print(hola("Ada"))           # no corre al importarlo

# $ python saludos.py    ->  imprime "Hola, Ada"  (__name__ == "__main__")
# import saludos         ->  no imprime nada      (__name__ == "saludos")
```

## El idioma `if __name__ == "__main__":`

> [!regla]
> Todo lo que va dentro de `if __name__ == "__main__":` se ejecuta **solo si el archivo es el punto de entrada**, no cuando se importa. Es el lugar para la demostración, las pruebas rápidas o el arranque de la aplicación, sin contaminar a quien importe el módulo para reutilizar sus funciones.

```python
# calculadora.py
def suma(a, b):
    return a + b

if __name__ == "__main__":
    # bloque de uso como script: ignorado al importar
    print(suma(2, 3))            # 5

import calculadora               # no imprime 5; suma queda disponible
calculadora.suma(2, 3)          # 5
```

## Por qué vale "__main__"

> [!info]
> Cuando lanzas `python archivo.py` (o `python -m paquete`), Python carga ese archivo como el **módulo principal** y le asigna `__name__ = "__main__"`. Cualquier otro módulo que importes recibe como `__name__` su **nombre de importación**. Así, un solo valor distingue "soy el programa que se está ejecutando" de "me están importando".

```python
# en el archivo lanzado directamente:
print(__name__)                  # "__main__"

# en cualquier modulo importado por el:
# print(__name__)                # su nombre, p. ej. "calculadora"
```

> [!warning]
> Sin el guardián `if __name__ == "__main__":`, el código de demostración o de arranque corre **también al importar** el módulo —imprimiendo o ejecutando efectos no deseados en quien solo quería reutilizar una función. Es la causa típica de "se ejecuta algo raro al hacer `import`".

Este patrón se apoya en la [[02 Namespace del Modulo | variable global del módulo]] (`__name__` vive en su `__dict__`) y es la base del [[01 Archivos .py como Modulos | doble rol del archivo `.py`]]: la misma unidad sirve como biblioteca importable y como programa ejecutable.
