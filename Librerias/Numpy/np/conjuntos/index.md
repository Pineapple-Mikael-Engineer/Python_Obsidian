---
title: np/conjuntos — operaciones de conjunto sobre arrays
tags:
  - numpy
  - indice
draft: false
---

# np/conjuntos — operaciones de conjunto sobre arrays

Este grupo trata los valores de un array como miembros de un **conjunto matemático**: sin orden
relevante y sin duplicados lógicos. Reúne la deduplicación ([[np.unique]]), las cuatro operaciones
binarias clásicas (intersección, unión, diferencia y diferencia simétrica) y la prueba de
pertenencia ([[np.isin]]).

Son mucho más rápidas que los `set` de Python para grandes volúmenes numéricos porque ordenan los
datos con algoritmos $O(n \log n)$ sobre arrays contiguos en memoria, sin crear un objeto Python por
elemento. La contrapartida es su modelo de forma, que conviene tener claro de entrada.

> [!important] Operan en 1D y devuelven 1D ordenado (salvo `isin`)
> `unique` y las cuatro binarias **aplanan** sus entradas a 1D y devuelven siempre un vector
> **único y ordenado** de menor a mayor: el shape original se pierde. La excepción es `isin`, que
> **conserva la shape** de su primer argumento (`element`) y devuelve una **máscara booleana** del
> mismo tamaño. `unique` también admite `axis` para buscar **filas/sub-arrays únicos** (su único
> caso N-D real).

## La operación de cada función

| Nota | Operación | Notación | Qué devuelve |
|------|-----------|----------|--------------|
| [[np.unique]] | valores únicos (dedup) | $\{a_i\} \to \text{únicos}$ | vector 1D ordenado, sin repetir |
| [[np.intersect1d]] | intersección (en ambos) | $A \cap B$ | vector 1D ordenado |
| [[np.union1d]] | unión (en cualquiera) | $A \cup B$ | vector 1D ordenado |
| [[np.setdiff1d]] | diferencia (en A, no en B) | $A \setminus B$ | vector 1D ordenado (no simétrica) |
| [[np.setxor1d]] | diferencia simétrica (en uno, no en ambos) | $A \triangle B$ | vector 1D ordenado |
| [[np.isin]] | pertenencia elemento a elemento | $x \in T$ | máscara booleana, conserva la shape |

## Notas de la carpeta

- [[np.unique]] — valores únicos de `ar`, ordenados de menor a mayor. Con `return_index`,
  `return_inverse` o `return_counts` añade información para localizar, reconstruir o contar; con
  `axis` busca **filas únicas** de una matriz.
- [[np.intersect1d]] — elementos presentes en **ambos** arrays ($A \cap B$). Equivale a
  `set(a) & set(b)`; con `return_indices` recupera las posiciones de los comunes.
- [[np.union1d]] — todos los elementos de **cualquiera** de los dos ($A \cup B$). Equivale a
  `set(a) | set(b)`; internamente es `unique` sobre la concatenación.
- [[np.setdiff1d]] — elementos de `ar1` que **no** están en `ar2` ($A \setminus B$). Equivale a
  `set(a) - set(b)`. El orden de los argumentos importa: **no es simétrica**.
- [[np.setxor1d]] — elementos en exactamente **uno** de los dos, no en ambos ($A \triangle B$).
  Equivale a `set(a) ^ set(b)`. Útil para detectar diferencias en ambos sentidos a la vez.
- [[np.isin]] — máscara booleana de **pertenencia**: ¿cada valor de `element` está en
  `test_elements`? Conserva la shape de `element`; reemplazo moderno de `np.in1d`. Con `invert`
  niega la máscara.

## Notas relacionadas

- [[concepto_indexing]] — las máscaras y los índices que devuelven estas funciones
- [[np.bincount]] — conteo de enteros, complementario a `unique(return_counts=True)`
- [[Librerias/Numpy/index|NumPy raíz]]
