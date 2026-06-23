---
title: np/manipulacion_forma/cambio_forma — cambiar la forma sin cambiar los datos
tags:
  - numpy
  - indice
draft: false
---

# np/manipulacion_forma/cambio_forma — cambiar la forma sin cambiar los datos

Esta carpeta agrupa las funciones que **transforman el [[concepto_shape|shape]] de un array sin alterar sus valores**. Todas reinterpretan el mismo buffer de memoria bajo otra tupla de ejes: ninguna calcula nada, solo reescribe la forma y los `strides`. Por eso el resultado es, en la gran mayoría de casos, una [[concepto_views_vs_copias|vista]] — modificar el resultado modifica el original, y al revés.

Cada una responde a una pregunta distinta sobre la forma: ¿la reorganizo entera (`reshape`)?, ¿la aplano a una fila (`ravel`)?, ¿quito o pongo ejes de tamaño 1 (`squeeze` / `expand_dims`)?, ¿la estiro a una forma mayor repitiendo valores (`broadcast_to`)? El `size` (el producto de los ejes) se conserva en todas salvo `broadcast_to`, que lo agranda virtualmente sin copiar.

## Tabla de funciones

| Función | Mapa de shapes | Qué hace | Retorno |
|---------|----------------|----------|---------|
| [[np.reshape]] | $(n_0,\dots,n_{k-1})\to(m_0,\dots,m_{j-1})$, $\prod n_i=\prod m_l$ | reorganiza los elementos en otra forma con el mismo total | vista si puede, si no copia |
| [[np.ravel]] | $(n_0,\dots,n_{k-1})\to(\prod_i n_i,)$ | aplana a 1D | vista si contiguo, si no copia |
| [[np.squeeze]] | $(n_0,\dots,1,\dots,n_{k-1})\to(\dots\text{sin los 1})$ | quita los ejes de tamaño 1 | vista |
| [[np.expand_dims]] | $(n_0,\dots,n_{k-1})\to(n_0,\dots,1,\dots,n_{k-1})$ | inserta un eje de tamaño 1 | vista |
| [[np.broadcast_to]] | $(n_0,\dots)\to(\text{forma destino mayor})$ | estira la forma repitiendo valores | vista de **solo lectura** |

## Las funciones

### [[np.reshape]] — reorganiza con el mismo total
La navaja suiza del grupo. Acepta cualquier forma destino cuyo producto coincida con el `size`: `(12,)` puede volverse `(3, 4)`, `(2, 6)` o `(1, 3, 4)`, pero nunca `(3, 5)`. La dimensión `-1` se infiere sola. El parámetro `order` decide si los elementos se recorren por filas (C, defecto) o por columnas (Fortran).

### [[np.ravel]] — aplana a 1D
El caso particular de `reshape(-1)`: colapsa todos los ejes en uno. Devuelve vista si el array es contiguo en el `order` pedido; si no, copia. Contrasta con `ndarray.flatten`, que **siempre** copia: usa `ravel` cuando te valga una vista, `flatten` cuando necesites independencia garantizada.

### [[np.squeeze]] — quita los ejes de tamaño 1
Limpia la forma eliminando las dimensiones que valen 1 (`(1, 5, 1) → (5,)`). Con `axis` se eligen ejes concretos en vez de todos. Útil para deshacer las formas infladas que dejan las reducciones con `keepdims=True`, los slices o las predicciones de un solo elemento. **Cuidado**: con `axis=None` puede quitar un eje unitario que querías conservar (un lote de tamaño 1).

### [[np.expand_dims]] — pone un eje de tamaño 1
El inverso de `squeeze`: inserta una dimensión de tamaño 1 en la posición `axis` (`(5,) → (1, 5)`). Equivale a `a[np.newaxis, :]` pero es más legible cuando el eje es una variable. Es la herramienta clave para **alinear shapes** de cara al [[concepto_broadcasting|broadcasting]]: convierte un vector en fila o columna para que case con una matriz.

### [[np.broadcast_to]] — estira a una forma mayor
Materializa el broadcasting explícitamente: repite los valores de un array a lo largo de los ejes de tamaño 1 hasta llegar a una forma destino mayor, **sin copiar** (`strides` 0). El resultado es una vista de **solo lectura**: como los datos se comparten, NumPy impide escribir en ella. Si necesitas escribir, añade `.copy()`.

## Vista o copia: la frontera

> [!regla] Casi todas devuelven vista; las excepciones importan
> `reshape` y `ravel` dan **vista si el array es contiguo** y copia si no (ver [[concepto_views_vs_copias]]); `squeeze` y `expand_dims` dan **vista siempre**; `broadcast_to` da **vista de solo lectura siempre**. Para confirmarlo en cualquier caso: `np.shares_memory(a, b)`. La consecuencia práctica: escribir en el resultado de estas funciones puede modificar el array original sin avisar.

## Notas relacionadas

- [[concepto_shape]] — la tupla de ejes que estas funciones reescriben
- [[concepto_views_vs_copias]] — vista frente a copia, la decisión que gobierna el grupo
- [[concepto_broadcasting]] — el destino de `expand_dims` y `broadcast_to`
