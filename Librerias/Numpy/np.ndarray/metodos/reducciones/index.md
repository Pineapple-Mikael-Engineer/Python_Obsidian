---
title: ndarray — métodos de reducción (forma-método de las funciones)
tags:
  - numpy
  - indice
draft: false
---

# ndarray — métodos de reducción (forma-método de las funciones)

Estos métodos son la **forma-método** de funciones de reducción que ya están documentadas en
[[Librerias/Numpy/np/reducciones/index|np/reducciones]]. La regla general es

$$ \texttt{arr.f(args)} \;\equiv\; \texttt{np.f(arr, args)} $$

mismo comportamiento, mismo retorno y misma semántica de `axis` / `keepdims` / `dtype`. No hay
teoría nueva aquí: el mapa de shapes, el caso N-D y los parámetros completos viven en la nota de
**la función**. Esta nota solo da el **mapeo método → función** y lo que es **propio del método**.

## Método ≡ función

| Método | Equivale a | Qué hace (1 línea) |
|--------|-----------|--------------------|
| `arr.sum(...)` | [[np.sum]] | Suma los elementos a lo largo del eje (colapsa ese eje). |
| `arr.mean(...)` | [[np.mean]] | Media aritmética sobre el eje; enteros → `float64`. |
| `arr.max(...)` | [[np.max]] | Valor máximo a lo largo del eje. |
| `arr.min(...)` | [[np.min]] | Valor mínimo a lo largo del eje. |
| `arr.prod(...)` | [[np.prod]] | Producto de los elementos sobre el eje. |
| `arr.std(...)` | [[np.std]] | Desviación estándar; acepta `ddof=`. |
| `arr.var(...)` | [[np.var]] | Varianza; `ddof=0` poblacional, `ddof=1` muestral. |
| `arr.cumsum(...)` | [[np.cumsum]] | Suma acumulada (scan): conserva el shape. |
| `arr.cumprod(...)` | [[np.cumprod]] | Producto acumulado (scan): conserva el shape. |
| `arr.argmax(...)` | [[np.argmax]] | Índice (no valor) del máximo en el eje o en el array aplanado. |
| `arr.argmin(...)` | [[np.argmin]] | Índice del mínimo en el eje o en el array aplanado. |
| `arr.ptp(...)` | [[np.ptp]] | Rango pico a pico `max - min` sobre el eje. |
| `arr.clip(a_min, a_max)` | [[np.clip]] | Recorta cada valor al rango `[a_min, a_max]`. |
| `arr.round(decimals)` | [[np.round]] | Redondea cada elemento al número de decimales dado. |

## Cuándo usar la forma-método

La forma-método es **más concisa al encadenar** y deja la lectura izquierda→derecha en el orden
de las operaciones: `a.sum(0).max()` se lee mejor que `np.max(np.sum(a, 0))`. Es idéntica en
resultado a la función.

La **forma-función** es preferible cuando se necesita lo que solo ella ofrece: el parámetro `out=`
para escribir en un buffer existente, o aceptar entradas que aún no son ndarray (listas, tuplas,
escalares), porque `np.sum([1, 2, 3])` funciona pero `[1, 2, 3].sum()` no existe.

## Lo que SÍ difiere

- **Todos los de esta carpeta son idénticos a su función** (mismo retorno, ninguno modifica
  `arr`): devuelven un array o escalar nuevo y no tocan el original.
- `clip` y `round` **no son reducciones** (no colapsan ningún eje: devuelven un array del mismo
  shape). Están aquí por ser métodos del objeto `ndarray`; enlazan a [[np.clip]] y [[np.round]].
- `cumsum` / `cumprod` son **scan**, no reduce: conservan el shape (el último elemento coincide
  con la reducción total). El detalle está en su nota de función.
- `ptp` como método está **deprecado en NumPy ≥ 2.0**; usa la función [[np.ptp]] o
  `arr.max() - arr.min()`.

> [!warning] Principio general: método in-place vs función que copia
> En otras familias del `ndarray` algunos métodos son **in-place** y mutan `arr` (`arr.sort()`,
> `arr.fill()`), mientras su función equivalente devuelve una copia (`np.sort` no toca la entrada).
> **Las reducciones de esta carpeta NO son de ese tipo**: ninguna muta `arr`. Pero conviene tener
> presente la distinción al saltar a las carpetas `forma/` (`flatten` copia) y `seleccion/`
> (`put` es in-place).

## Notas relacionadas

- [[Librerias/Numpy/np/reducciones/index|np/reducciones]] — la teoría completa de cada función
- [[concepto_axis_parametro]] — el eje que la reducción consume
- [[concepto_vectorizacion]] — por qué reducir sobre un eje sustituye al bucle Python
- [[Librerias/Numpy/index|NumPy raíz]]
