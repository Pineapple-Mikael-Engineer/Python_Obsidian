---
title: Módulos de Terceros
order: 3
tags:
  - python
  - teoria
  - sistema-modulos
draft: false
aliases:
  - Third-party modules
  - Paquetes de PyPI
  - site-packages
---

# Módulos de Terceros

> [!definicion]
> Los **módulos de terceros** son los que **no vienen con Python** y se **instalan con `pip`** desde **PyPI** (*Python Package Index*). Una vez instalados, viven en el directorio **`site-packages`** y se importan igual que cualquier otro módulo. Ejemplos típicos: `requests`, `numpy`, `pandas`, `flask`.

```bash
pip install requests        # descarga desde PyPI e instala en site-packages
```

```python
import requests             # ya importable tras el pip install
requests.get("https://example.com").status_code   # 200
```

Forman la tercera capa de la [[41 Jerarquia de Modulos/index | jerarquía de módulos]]: amplían lo que ofrece la [[02 Libreria Estandar | librería estándar]] cuando esta se queda corta, a costa de añadir una **dependencia externa** que hay que instalar.

## Dónde viven: `site-packages`

> [!regla]
> `pip` deposita los paquetes en el directorio **`site-packages`** de la instalación (o del entorno virtual activo). Ese directorio forma parte de `sys.path`, por eso lo allí instalado se vuelve importable. Inspeccionarlo confirma de dónde sale un módulo de terceros.

```python
import requests

requests.__file__
# '.../site-packages/requests/__init__.py'  -> en site-packages

import sys
[p for p in sys.path if 'site-packages' in p]   # las rutas de instalación
```

## Entornos virtuales: aislar las dependencias

> [!info]
> Un **entorno virtual** (`venv`) es una instalación de Python aislada con su propio `site-packages`. Permite que cada proyecto tenga **sus versiones** de los paquetes sin colisionar con otros ni con el Python del sistema. Es la práctica estándar para gestionar dependencias de terceros.

```bash
python -m venv .venv           # crea el entorno
source .venv/bin/activate      # lo activa (Linux/macOS)
pip install requests           # instala SOLO en este entorno
```

```python
import sys
sys.prefix        # apunta a la carpeta del venv cuando está activo
```

## Reproducir las dependencias: `requirements.txt`

> [!info]
> El archivo **`requirements.txt`** lista los paquetes de terceros con sus versiones para reproducir el entorno en otra máquina. `pip freeze` lo genera y `pip install -r` lo aplica.

```bash
pip freeze > requirements.txt          # congela las versiones actuales
pip install -r requirements.txt        # las reinstala en otro entorno
```

A diferencia de los terceros, los [[04 Modulos Personalizados | módulos personalizados]] no se instalan: son archivos del propio proyecto que Python encuentra por la raíz desde la que se ejecuta, según las rutas de [[42 Mecanismos de Importacion/01 sys.path y PYTHONPATH | sys.path y PYTHONPATH]].
