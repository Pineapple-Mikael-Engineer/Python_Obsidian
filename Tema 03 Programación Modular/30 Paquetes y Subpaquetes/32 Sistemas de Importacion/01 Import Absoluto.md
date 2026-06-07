---
title: Import Absoluto
order: 1
tags:
  - python
  - teoria
  - paquetes
draft: false
aliases:
  - Absolute import
  - Importación absoluta
---

# Import Absoluto

> [!definicion]
> Un **import absoluto** nombra el módulo por su **ruta completa desde la raíz** del proyecto (el directorio que está en `sys.path`): `from paquete.subpaquete.modulo import x` o `import paquete.modulo`. No depende de dónde esté el archivo que importa: la ruta es siempre la misma, **inequívoca**. Es el estilo **recomendado por PEP 8**.

```python
# desde cualquier archivo del proyecto, la ruta es idéntica:
from mi_pkg.utils import validar          # trae el módulo 'validar'
from mi_pkg.utils.validar import es_valido  # trae un símbolo concreto
import mi_pkg.geometria                   # importa el módulo completo
```

La ruta `mi_pkg.utils.validar` se lee como la **dirección absoluta** del módulo dentro de la jerarquía de paquetes, análoga a una ruta de archivo desde la carpeta raíz.

## Por qué PEP 8 lo recomienda

> [!regla]
> El import absoluto es el estilo por defecto porque es **explícito y robusto**:
> - **Legible** — la ruta dice exactamente de qué paquete viene el símbolo.
> - **Estable** — no cambia si mueves el archivo que importa dentro del paquete.
> - **Funciona en scripts y en paquetes** por igual, a diferencia del [[02 Import Relativo | relativo]].

```python
# Claro de un vistazo: 'es_valido' viene de mi_pkg.utils.validar
from mi_pkg.utils.validar import es_valido
```

## Necesita la raíz en `sys.path`

> [!info]
> Para que `from mi_pkg... import x` resuelva, el **directorio que contiene `mi_pkg`** debe estar en [[01 sys.path y PYTHONPATH | sys.path]]. Suele estarlo automáticamente al ejecutar desde la raíz del proyecto, instalar el paquete (`pip install -e .`) o lanzarlo con `python -m`. Si no, Python lanza `ModuleNotFoundError`.

```python
import sys
sys.path                       # debe incluir la carpeta que contiene 'mi_pkg'
from mi_pkg import geometria   # ModuleNotFoundError si la raíz no está en sys.path
```

## Absoluto frente a relativo

> [!ejemplo]
> Las dos formas pueden traer el mismo símbolo; el absoluto nombra desde la raíz, el relativo desde el paquete actual. Estando dentro de `mi_pkg/core/procesar.py`:

```python
# import ABSOLUTO  -> ruta completa desde la raíz
from mi_pkg.utils.validar import es_valido

# import RELATIVO  -> desde el paquete actual (equivalente aquí)
from ..utils.validar import es_valido
```

El absoluto es preferible salvo cuando la ruta se vuelve larga y repetitiva **dentro** de un mismo paquete, donde el [[02 Import Relativo | import relativo]] gana concisión. Ambos se apoyan en la [[40 Sistema de Modulos de Python/index | maquinaria de importación]] que resuelve los nombres contra `sys.path` y `sys.modules`.
