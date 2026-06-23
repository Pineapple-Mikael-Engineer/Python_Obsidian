---
title: ndarray — métodos de forma (forma-método de las funciones)
tags:
  - numpy
  - indice
draft: false
---

# ndarray — métodos de forma (forma-método de las funciones)

Estos métodos son la **forma-método** de funciones de manipulación de forma ya documentadas. La
regla general es

$$ \texttt{arr.f(args)} \;\equiv\; \texttt{np.f(arr, args)} $$

mismo comportamiento y misma semántica de ejes. Ninguno cambia los datos numéricos: solo
reorganizan cómo se navega el mismo buffer. La explicación completa (mapa de shapes, contigüidad,
cuándo es vista o copia) vive en la nota de **la función**; aquí solo el mapeo y lo **propio del
método**.

## Método ≡ función

| Método | Equivale a | Qué hace (1 línea) |
|--------|-----------|--------------------|
| `arr.reshape(*shape)` | [[np.reshape]] | Reinterpreta los datos con otra forma compatible. |
| `arr.ravel(order)` | [[np.ravel]] | Aplana a 1D; **vista** si puede, copia si no. |
| `arr.squeeze(axis)` | [[np.squeeze]] | Elimina los ejes de tamaño 1. |
| `arr.swapaxes(a, b)` | [[np.swapaxes]] | Intercambia exactamente dos ejes (siempre vista). |
| `arr.transpose(*axes)` | [[np.transpose]] | Permuta todos los ejes (siempre vista). |
| `arr.flatten(order)` | *(sin gemela — ver abajo)* | Aplana a 1D; **siempre copia**. |

Atributo relacionado: [[ndarray.T]] es la transpuesta como **atributo** (`arr.T`), equivalente a
`arr.transpose()` sin argumentos.

## Cuándo usar la forma-método

Más concisa al encadenar (`a.reshape(2, -1).T.ravel()` se lee de izquierda a derecha) e idéntica
en resultado. La forma-función admite encadenar entradas que no son ndarray todavía
(`np.reshape([1, 2, 3, 4], (2, 2))`).

## Lo que SÍ difiere

- **`arr.flatten()` SIEMPRE COPIA** (buffer independiente; modificarla no afecta al original).
  En cambio [[np.ravel]] / `arr.ravel()` devuelven **VISTA si pueden** (array contiguo) y copia
  si no. Es la diferencia clave de esta carpeta — ver [[concepto_views_vs_copias]].

  ```python
  a = np.array([[1, 2], [3, 4]])
  r = a.ravel();   r[0] = 99   # si r es vista → cambia a[0, 0]
  f = a.flatten(); f[0] = 99   # copia → a queda intacto
  ```

- `arr.flatten` **no tiene función gemela** `np.flatten`. El equivalente funcional es
  `np.ravel(arr).copy()`.

- **`arr.reshape` acepta argumentos sueltos**: `arr.reshape(2, 3)`. La función [[np.reshape]] exige
  la forma como **tupla**: `np.reshape(arr, (2, 3))`. Ambas aceptan `-1` para inferir una dimensión.

- `reshape` y `ravel` devuelven **vista o copia según la contigüidad** del array (vista si los datos
  pueden reinterpretarse sin moverlos). `transpose`, `swapaxes` y `squeeze` son **siempre vista**.

> [!warning] Principio general: método in-place vs función que copia
> Algunos métodos del `ndarray` mutan `arr` in-place (`arr.sort()`, `arr.fill()`, `arr.resize()`)
> a diferencia de su función, que devuelve copia (`np.sort` no toca la entrada). Los métodos de
> **esta** carpeta no mutan `arr`: o devuelven vista del mismo buffer, o una copia nueva. La
> mutación in-place sí aparece en `seleccion/` (`arr.put`).

## Notas relacionadas

- [[concepto_views_vs_copias]] — qué método devuelve vista y cuál copia, y por qué
- [[concepto_shape]] — el mapa de shapes que cada método aplica
- [[ndarray.T]] — la transpuesta como atributo
- [[Librerias/Numpy/index|NumPy raíz]]
