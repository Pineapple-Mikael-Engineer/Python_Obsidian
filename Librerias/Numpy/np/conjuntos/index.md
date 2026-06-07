---
title: np/conjuntos — operaciones de teoria de conjuntos
tags:
  - numpy
  - indice
draft: false
---

# np/conjuntos — operaciones de teoria de conjuntos

Este grupo trata los elementos de un array 1D como miembros de un conjunto matematico: sin orden relevante, sin duplicados logicos. Las cinco funciones cubren las operaciones clasicas de teoria de conjuntos y devuelven siempre `ndarray` ordenados.

Son mas rapidas que los `set` de Python para grandes volumenes numericos porque internamente ordenan los datos con algoritmos O(n log n) sobre arrays contiguos en memoria — sin la sobrecarga de crear objetos Python por elemento. La contrapartida: solo funcionan sobre arrays 1D con tipos comparables.

## Notas de la carpeta

- [[np.unique]] — devuelve los elementos unicos de `a` ordenados de menor a mayor. Con `return_index=True`, `return_inverse=True` o `return_counts=True` devuelve informacion adicional que permite reconstruir el array original o contar frecuencias.
- [[np.intersect1d]] — elementos que estan en ambos arrays simultaneamente. Equivale a `set(a) & set(b)` pero devuelve ndarray ordenado. Maneja duplicados en la entrada de forma transparente.
- [[np.union1d]] — todos los elementos que aparecen en al menos uno de los dos arrays, sin duplicados. Equivale a `set(a) | set(b)`. El resultado siempre esta ordenado.
- [[np.setdiff1d]] — elementos que estan en `a` pero no en `b`. Equivale a `set(a) - set(b)`. El orden de los argumentos importa: `setdiff1d(a, b)` es distinto de `setdiff1d(b, a)`.
- [[np.setxor1d]] — elementos que estan en exactamente uno de los dos arrays, pero no en ambos. Equivale a `set(a) ^ set(b)`. Util para detectar diferencias simetricas entre dos conjuntos de datos.
