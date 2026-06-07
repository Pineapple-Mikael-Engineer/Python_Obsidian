---
title: sys.modules (Caché)
order: 2
tags:
  - python
  - teoria
  - sistema-modulos
draft: false
aliases:
  - sys.modules
  - Caché de módulos
  - Module cache
---

# sys.modules (Caché)

> [!definicion]
> **`sys.modules`** es un **diccionario** que cachea **todos los módulos ya importados** en el proceso, indexados por su nombre. Antes de buscar un módulo en `sys.path`, Python consulta este diccionario: si ya está, lo **devuelve tal cual** sin volver a cargarlo. Es la razón de que un módulo **se ejecute una sola vez**.

```python
import sys

'os' in sys.modules          # False antes de importarlo
import os
'os' in sys.modules          # True  -> ahora está en caché
sys.modules['os'] is os      # True  -> es el MISMO objeto módulo
```

`sys.modules` es la pieza de "memoria" del [[42 Mecanismos de Importacion/index | mecanismo de importación]]: se consulta antes que la búsqueda por [[01 sys.path y PYTHONPATH | sys.path]] y se rellena justo después de ejecutar cada módulo.

## Por qué un módulo solo se ejecuta una vez

> [!regla]
> El cuerpo de un módulo (sus `print`, asignaciones, `def`, etc.) se ejecuta **únicamente en el primer `import`**. Los siguientes `import` del mismo nombre **no re-ejecutan** nada: simplemente recuperan el objeto desde `sys.modules`. Por eso un módulo importado en diez sitios mantiene un único estado compartido.

```python
# config.py
print("cargando config")     # se imprime UNA vez
VALOR = 42

# main.py
import config                # imprime "cargando config"
import config                # NO imprime nada -> sale de la caché
config.VALOR                 # 42  (estado único y compartido)
```

## Inspeccionar la caché

> [!info]
> `sys.modules` es un diccionario corriente: se puede recorrer para ver qué hay cargado, contar módulos o filtrar por nombre. Incluye los built-in, la estándar, los terceros y los propios ya importados.

```python
import sys

len(sys.modules)                                  # cuántos módulos cargados
[n for n in sys.modules if n.startswith('json')]  # ['json', 'json.decoder', ...]
sys.modules.get('numpy')                          # None si nunca se importó
```

## Limpiar la caché para forzar recarga

> [!regla]
> Eliminar la entrada con `del sys.modules['M']` hace que el **próximo** `import M` vuelva a buscarlo y a **ejecutar su cuerpo** desde cero. Es la base manual de la recarga, aunque deja **referencias antiguas** al módulo previo intactas, por lo que suele preferirse `importlib.reload`.

```python
import sys
import config

del sys.modules['config']    # saca config de la caché
import config                # vuelve a ejecutar su cuerpo (imprime de nuevo)
```

Forzar la recarga sin perder las referencias existentes es justo lo que resuelve [[03 Reloading (importlib.reload) | importlib.reload]], que re-ejecuta el módulo **sobre el mismo objeto** ya presente en `sys.modules`.
