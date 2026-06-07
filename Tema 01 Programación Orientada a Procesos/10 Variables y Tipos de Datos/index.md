---
title: Variables y Tipos de Datos
order: 10
draft: false
description: Sistema de tipos de Python — variables, primitivos, mutabilidad y conversión
tags:
  - Index
  - Tema
aliases:
  - Variables y Tipos
  - Sistema de Tipos
---
# Variables y Tipos de Datos

Una **variable** en Python es una **referencia simbólica a un objeto** en memoria, no un contenedor que almacene el dato. La asignación `x = 5` enlaza el nombre `x` con el objeto `5`; el objeto vive en memoria y la variable solo lo apunta. De ahí que copia, paso de argumentos y mutación dependan de la **identidad del objeto**, no del nombre.

El **tipo** de un objeto define su naturaleza, las operaciones admitidas y su representación en memoria. Python es de **tipado dinámico** (el tipo se resuelve en ejecución, no se declara) y **fuerte** (no coacciona tipos incompatibles de forma silenciosa: `"2" + 3` es un `TypeError`).

```python
x = 5            # x referencia un int
x = "texto"      # ahora referencia un str; el tipo lo lleva el objeto, no el nombre
type(x)          # <class 'str'>
```

## Subtemas

- [[11 Datos Primitivos/index | Datos Primitivos]] — los tipos atómicos: numéricos (`int`, `float`, `complex`, `bool`) y el vacío (`None`).
- [[12 Mutabilidad/index | Mutabilidad]] — distinción entre objetos que se modifican *in place* y los que crean uno nuevo en cada cambio.
- [[13 Transformación de Tipos/index | Transformación de Tipos]] — conversión implícita (coerción) y explícita (*casting*) entre tipos.

## Clasificación

| Eje | Categorías | Subtema |
| --- | ---------- | ------- |
| Naturaleza | Numéricos · Vacío | [[11 Datos Primitivos/index \| Datos Primitivos]] |
| Mutabilidad | Inmutables (`int`, `str`, `tuple`…) · Mutables (`list`, `dict`, `set`) | [[12 Mutabilidad/index \| Mutabilidad]] |
| Conversión | Implícita (`int`→`float`) · Explícita (`int()`, `str()`…) | [[13 Transformación de Tipos/index \| Transformación]] |

Las secuencias de texto y binarias (`str`, `bytes`) se tratan como colecciones en [[20 Estructura de Datos/index | Estructura de Datos]]. Este módulo es prerequisito de las [[30 Estructuras de Control/index | estructuras de control]], cuyas condiciones evalúan los [[Valores Truthy y Falsy | valores de verdad]] de estos objetos.
