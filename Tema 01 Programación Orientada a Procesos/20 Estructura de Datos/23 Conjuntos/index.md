---
title: 23-Conjuntos
draft: false
description: Colecciones de elementos únicos y hashables — set y frozenset
tags:
  - Index
  - Tema
aliases:
  - Conjuntos
  - Sets
---
# Conjuntos

Un **conjunto** es una colección de **elementos únicos y hashables**, organizada internamente como **tabla hash** y por tanto **no ordenada**. Modela la teoría de conjuntos matemática: la pertenencia (`in`) cuesta **O(1) promedio** y las operaciones binarias (unión, intersección, diferencia, diferencia simétrica) tienen forma de operador y de método. Python ofrece dos variantes: `set` (mutable) y `frozenset` (inmutable y, por serlo, hashable él mismo).

## Subtemas

- [[01 Sets | Sets]] — `set` mutable: creación, *set comprehensions*, operaciones de teoría de conjuntos (`|`, `&`, `-`, `^`), métodos de mutación, pertenencia eficiente y casos de uso.
- [[02 Frozenset | Frozenset]] — variante inmutable y hashable: creación, uso como clave de dict y elemento de otro set, operaciones que devuelven nuevos `frozenset`.

## Resumen

| Tipo        | Mutable | Hashable | Sintaxis      | Uso típico                          |
| ----------- | :-----: | :------: | ------------- | ----------------------------------- |
| `set`       | **Sí**  |    No    | `{...}`       | Eliminar duplicados, álgebra de conjuntos |
| `frozenset` |   No    |  **Sí**  | `frozenset()` | Clave de dict, elemento de otro set |

| Operación            | Operador | Método                     |
| -------------------- | :------: | -------------------------- |
| Unión                | `\|`     | `union()`                  |
| Intersección         | `&`      | `intersection()`           |
| Diferencia           | `-`      | `difference()`             |
| Diferencia simétrica | `^`      | `symmetric_difference()`   |
| Subconjunto / super. | `<= / >=`| `issubset() / issuperset()`|
| Disjuntos            | —        | `isdisjoint()`             |

Los elementos deben ser **hashables**, lo que excluye `list`, `dict` o `set` como contenido; para anidar conjuntos se usa `frozenset`. Frente a una `list`, el `set` reemplaza la búsqueda O(n) por pertenencia O(1), a costa de perder orden e indexación.
