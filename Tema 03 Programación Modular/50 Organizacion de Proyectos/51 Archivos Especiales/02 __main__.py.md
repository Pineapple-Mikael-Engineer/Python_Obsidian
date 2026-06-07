---
title: __main__.py
order: 2
tags:
  - python
  - teoria
  - proyectos
draft: false
aliases:
  - main py
  - Punto de entrada de paquete
  - Package entry point
---

# __main__.py

> [!definicion]
> `__main__.py` es el **punto de entrada ejecutable** de un paquete: el archivo que Python corre cuando se invoca el paquete con `python -m mi_paquete`. Convierte un paquete (que normalmente solo se *importa*) en algo que también se puede **ejecutar como un programa**.

```python
# mi_paquete/__main__.py
from .core import arrancar

def main():
    print("ejecutando mi_paquete como programa")
    arrancar()

if __name__ == "__main__":
    main()
```

```bash
python -m mi_paquete        # ejecuta mi_paquete/__main__.py  -> corre main()
```

Sin `__main__.py`, `python -m mi_paquete` falla con *"No module named mi_paquete.\_\_main\_\_"*. Con él, el paquete adquiere un comportamiento de **aplicación de línea de comandos** sin dejar de ser importable.

## python -m ejecuta __main__.py

> [!regla]
> La bandera `-m` le dice a Python: «busca este **paquete o módulo** en `sys.path` y ejecútalo». Si el nombre es un **paquete**, Python ejecuta su `__main__.py`. La diferencia con `python ruta/archivo.py` es que `-m` resuelve por **nombre de import**, respeta los paquetes y deja `sys.path[0]` apuntando al directorio actual, no al del script.

```bash
python -m mi_paquete        # por NOMBRE: ejecuta mi_paquete/__main__.py
python mi_paquete/__main__.py   # por RUTA: rompe los imports relativos del paquete
```

Por eso las herramientas estándar se invocan con `-m`: `python -m pip`, `python -m pytest`, `python -m http.server` ejecutan el `__main__.py` de cada paquete.

## Relación con __name__ == "__main__"

> [!info]
> Al ejecutarse vía `python -m`, el `__main__.py` recibe `__name__ == "__main__"`, igual que cualquier script lanzado directamente. Por eso dentro se usa el mismo guardián `if __name__ == "__main__":` para separar la **lógica ejecutable** del código importable. La diferencia es de **granularidad**: el guardián protege un *módulo* suelto; `__main__.py` hace ejecutable un *paquete entero*.

```python
# en un módulo suelto:  modulo.py
if __name__ == "__main__":      # solo si se ejecuta este archivo
    main()

# en un paquete:  mi_paquete/__main__.py
if __name__ == "__main__":      # solo si se ejecuta  python -m mi_paquete
    main()
```

La mecánica completa de `__name__` —el valor que toma según se importe o se ejecute— se detalla en [[03 __name__ y __main__ | __name__ == "__main__"]]. El último archivo especial de la sección, [[03 __version__.py | __version__.py]], no añade comportamiento ejecutable sino metadatos: la versión del paquete.
