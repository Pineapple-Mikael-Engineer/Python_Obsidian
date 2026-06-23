---
title: ndarray — métodos de selección (forma-método de las funciones)
tags:
  - numpy
  - indice
draft: false
---

# ndarray — métodos de selección (forma-método de las funciones)

Estos métodos son la **forma-método** de funciones de selección ya documentadas: extraen o
modifican elementos por índices enteros o condiciones booleanas. La regla general es

$$ \texttt{arr.f(args)} \;\equiv\; \texttt{np.f(arr, args)} $$

con una excepción importante en `put` (ver abajo). Complementan el indexado por corchetes
(`arr[...]`) con una interfaz de método que en algunos casos hace explícito el eje de operación.
La teoría completa vive en la nota de **la función**; aquí solo el mapeo y lo propio del método.

## Método ≡ función

| Método | Equivale a | Qué hace (1 línea) |
|--------|-----------|--------------------|
| `arr.take(indices, axis)` | [[np.take]] | Extrae elementos por índices con `axis` explícito (copia). |
| `arr.put(indices, values)` | [[np.put]] | Escribe `values` en esos índices planos **in-place**; devuelve `None`. |
| `arr.nonzero()` | [[np.nonzero]] | Tupla de índices (uno por dimensión) de los elementos ≠ 0. |
| `arr.compress(cond, axis)` | [[np.compress]] | Filtra filas/columnas donde la máscara es `True` (copia). |

## Cuándo usar la forma-método

Más concisa al encadenar, e idéntica en resultado. `take` y `compress` aportan el `axis` explícito,
que evita la ambigüedad del fancy indexing en arrays N-D (`arr.take([0, 2], axis=1)` deja claro que
se opera sobre columnas). La forma-función acepta entradas que aún no son ndarray.

## Lo que SÍ difiere

- **`arr.put(...)` es IN-PLACE**: modifica `arr` directamente y devuelve `None` (no un array
  nuevo). Opera sobre el array visto como 1D en orden C. A diferencia de la indexación normal de
  asignación `arr[idx] = vals` (que también muta pero usa índices N-D), `put` siempre toma índices
  **planos**. Si `values` es más corto que `indices`, se recicla en ciclo.

  ```python
  arr = np.zeros(6).reshape(2, 3)
  arr.put([1, 4], [9, 7])   # → None; arr queda [[0, 9, 0], [0, 7, 0]]
  ```

- `take` y `compress` **siempre devuelven copia** (como el fancy/booleano del que derivan —
  ver [[concepto_views_vs_copias]]); nunca son vista del original.

- `nonzero` no extrae valores: devuelve la **tupla de coordenadas** lista para indexar
  (`arr[arr.nonzero()]` da los no nulos). Para 1D es una tupla de un solo array.

> [!warning] Principio general: método in-place vs función que copia
> `arr.put` es el ejemplo de esta carpeta del patrón general: ciertos métodos del `ndarray` mutan
> `arr` in-place (también `arr.sort()`, `arr.fill()`) mientras su función equivalente devuelve una
> copia sin tocar la entrada. Revisa el retorno: si es `None`, el método modificó `arr`.

## Notas relacionadas

- [[concepto_indexing]] — el modelo de indexación que estos métodos exponen como API
- [[concepto_views_vs_copias]] — por qué `take` / `compress` copian
- [[Librerias/Numpy/index|NumPy raíz]]
