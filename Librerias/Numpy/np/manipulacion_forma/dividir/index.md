---
title: np/manipulacion_forma/dividir — partir arrays en subarrays
tags:
  - numpy
  - indice
draft: false
---

# np/manipulacion_forma/dividir — partir arrays en subarrays

El inverso de `combinar/`: toma un array y lo parte en una lista de subarrays. Los subarrays resultantes son **vistas** del original — comparten el mismo buffer de memoria, por lo que modificarlos modifica el array fuente.

Las tres funciones son variantes de la misma operacion base con diferentes restricciones de eje. `np.split` es la mas general; `np.vsplit` y `np.hsplit` son alias legibles para los casos mas frecuentes (dividir por filas o por columnas).

## La restriccion de la division exacta

Cuando se pasa un entero como segundo argumento, NumPy exige que el eje se divida exactamente en ese numero de partes iguales. Si el eje tiene 10 elementos y se pide dividir en 3, se lanza `ValueError`. La alternativa es pasar una lista de indices de corte: `np.split(a, [3, 7])` produce tres subarrays con los elementos `[0:3]`, `[3:7]` y `[7:]` — y con indices no tiene que ser exacto.

## Funciones

### [[np.split]] — division generica

La funcion raiz. Divide el array a lo largo del eje `axis` (default: 0). El segundo argumento puede ser:
- Un entero N: divide en N partes iguales. Falla si el eje no es divisible por N.
- Una lista de indices: corta en esas posiciones, como el indexado de Python. No requiere partes iguales.

Devuelve una lista de subarrays (vistas). Funciona con cualquier `ndim` y cualquier eje.

### [[np.vsplit]] — dividir por filas (eje 0)

Atajo para `np.split(a, indices_or_sections, axis=0)`. Mas legible cuando se trabaja con matrices y la intencion es separar grupos de filas. Requiere que el array tenga al menos 2 dimensiones; para arrays 1D usar `np.split` directamente.

Uso tipico: separar un dataset en bloques de entrenamiento, validacion y test cortando por filas.

### [[np.hsplit]] — dividir por columnas (eje 1)

Atajo para `np.split(a, indices_or_sections, axis=1)`. Util para separar grupos de columnas de una matriz: caracteristicas, etiquetas, subconjuntos de variables. Para arrays 1D se comporta como `split` en el eje 0 (porque no existe el eje 1).

## Tabla de funciones

| Funcion | Eje de division | Devuelve vistas | Restriccion |
|---------|----------------|-----------------|-------------|
| [[np.split]] | Cualquiera (default 0) | Si | Division exacta si se usa entero |
| [[np.vsplit]] | Eje 0 (filas) | Si | ndim >= 2 |
| [[np.hsplit]] | Eje 1 (columnas) | Si | ndim >= 2; en 1D divide eje 0 |

## Patron de indices vs. entero

```python
import numpy as np

a = np.arange(12).reshape(4, 3)

# Division en partes iguales (entero): debe ser exacto
partes = np.vsplit(a, 2)       # 2 matrices de (2, 3) — OK
# np.vsplit(a, 3)              # Error: 4 no es divisible entre 3

# Division en posiciones arbitrarias (lista de indices)
partes = np.vsplit(a, [1, 3])  # shapes (1,3), (2,3), (1,3) — siempre OK
```

## Relacion con combinar

`dividir/` y `combinar/` son operaciones inversas logicamente, pero no simetricas en memoria:
- `split` → vistas (sin copia)
- `concatenate` de esas vistas → copia

Esto significa que iterar sobre subarrays de un array grande es barato, pero reunirlos en un nuevo array tiene coste.
