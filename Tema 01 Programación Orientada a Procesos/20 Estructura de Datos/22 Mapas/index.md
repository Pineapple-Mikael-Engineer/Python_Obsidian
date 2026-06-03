---
title: Mapas
draft: false
tags: [python, teoria, mapas]
---

# Mapas (Estructuras Clave-Valor)

Las **estructuras clave-valor** asocian cada **clave hashable** a un **valor** mediante una **tabla hash**, lo que garantiza acceso, inserción y borrado en O(1) promedio. La clave debe ser **inmutable** (hashable): strings, números y tuplas son válidos; listas y diccionarios no. En Python, el tipo canónico de mapa es el `dict`, que desde la versión 3.7 preserva el **orden de inserción**.

## Hojas

- [[01 Diccionarios | Diccionarios]] — `dict` completo: creación (`{}`, `dict()`, `fromkeys()`), acceso (`[]`, `get()`, `setdefault()`), métodos de vista (`keys()`/`values()`/`items()`), comprensiones y fusión con `|`.
- [[02 Diccionarios Especializados | Diccionarios Especializados]] — variantes de `collections`: `defaultdict`, `OrderedDict`, `Counter`, `ChainMap` y `UserDict`.

## Tabla resumen

| Estructura | Módulo | Uso principal | Característica clave |
|------------|--------|---------------|---------------------|
| `dict` | built-in | Mapa general clave-valor | Orden de inserción (3.7+), O(1) |
| `defaultdict` | `collections` | Agrupaciones, conteos | Valor por defecto automático |
| `Counter` | `collections` | Frecuencias / multiconjuntos | `most_common()`, álgebra `+`/`-`/`&`/`|` |
| `OrderedDict` | `collections` | Orden explícito | `move_to_end()`, igualdad sensible al orden |
| `ChainMap` | `collections` | Vista de varios dicts | Resolución por capas |
