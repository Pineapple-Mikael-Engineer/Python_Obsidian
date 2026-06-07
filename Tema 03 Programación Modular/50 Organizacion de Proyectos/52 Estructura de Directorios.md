---
title: Estructura de Directorios
order: 52
tags:
  - python
  - teoria
  - proyectos
draft: false
aliases:
  - Directory Layout
  - src layout
  - flat layout
---

# Estructura de Directorios

> [!definicion]
> La **estructura de directorios** de un proyecto Python es el esqueleto de carpetas que separa el **código del paquete**, las **pruebas** y los **metadatos de empaquetado**. Hay dos layouts estándar —**`src/` layout** y **flat layout**— que se diferencian en si el paquete vive dentro de una carpeta `src/` o directamente en la raíz del proyecto.

```python
# src/ layout                         # flat layout
mi_proyecto/                          mi_proyecto/
├── src/                              ├── mi_paquete/
│   └── mi_paquete/                   │   ├── __init__.py
│       ├── __init__.py               │   └── core.py
│       └── core.py                   ├── tests/
├── tests/                            ├── pyproject.toml
├── pyproject.toml                    └── README.md
└── README.md
```

Ambos layouts contienen las mismas piezas; cambia **dónde** se coloca el paquete. El resto de carpetas y archivos (`tests/`, `pyproject.toml`, `README`) son comunes a los dos.

## src/ layout vs flat layout

> [!regla]
> En **flat layout** el paquete está en la raíz, así que se importa **sin instalar** (la raíz suele estar en `sys.path`). En **`src/` layout** el paquete está aislado dentro de `src/`, que **no** está en `sys.path`: obliga a **instalar el proyecto** (`pip install -e .`) para importarlo. Ese aislamiento es justamente su ventaja: las pruebas corren contra el paquete **instalado**, no contra los archivos sueltos, lo que detecta errores de empaquetado.

```bash
# flat: funciona sin instalar (peligro: prueba los archivos, no el paquete instalado)
python -c "import mi_paquete"          # OK desde la raíz

# src/: hay que instalar primero
pip install -e .                        # instala en modo editable
python -c "import mi_paquete"          # ahora OK, contra lo realmente empaquetado
```

| Layout | Paquete en | Importable sin instalar | Cuándo usarlo |
| ------ | ---------- | ----------------------- | ------------- |
| **flat** | raíz del proyecto | sí | scripts, proyectos pequeños, prototipos |
| **`src/`** | dentro de `src/` | no (requiere instalar) | librerías a publicar, proyectos con tests serios |

## La carpeta tests/

> [!info]
> Las pruebas se aíslan en una carpeta `tests/` **hermana** del paquete (no dentro de él), para que no se empaqueten ni se distribuyan junto al código. `pytest` las descubre automáticamente por el prefijo `test_` en archivos y funciones.

```python
mi_proyecto/
├── src/mi_paquete/core.py
└── tests/
    └── test_core.py        # pytest descubre  test_*.py  y funciones  test_*
```

## pyproject.toml, setup.py y README

> [!ejemplo]
> Los **metadatos de empaquetado** (nombre, versión, dependencias, *build backend*) van hoy en `pyproject.toml`, el estándar moderno (PEP 518/621). `setup.py` es la forma **antigua**, imperativa, que aún se ve en proyectos legados. El `README` describe el proyecto y suele mostrarse en PyPI.

```toml
# pyproject.toml — estándar actual, declarativo
[project]
name = "mi_paquete"
version = "1.2.3"
dependencies = ["requests>=2.0"]

[build-system]
requires = ["setuptools>=61"]
build-backend = "setuptools.build_meta"
```

```python
# setup.py — forma antigua (imperativa), preferir pyproject.toml en proyectos nuevos
from setuptools import setup
setup(name="mi_paquete", version="1.2.3", install_requires=["requests>=2.0"])
```

La regla práctica: **flat** para algo pequeño y rápido; **`src/`** cuando el proyecto se va a instalar, publicar o probar en serio. Los archivos `__init__.py`, `__main__.py` y `__version__.py` que pueblan el paquete son los [[51 Archivos Especiales/index | Archivos Especiales]]; la diferencia formal entre las piezas que ordena este árbol —archivo, directorio, directorio anidado— se precisa en [[53 Module vs Package vs Subpackage | Module vs Package vs Subpackage]].
