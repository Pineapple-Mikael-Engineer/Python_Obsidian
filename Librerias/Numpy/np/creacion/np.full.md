---
title: np.full — crea un array de la shape dada relleno con un valor constante
aliases:
  - full
  - np.full
  - relleno
tags:
  - numpy
  - api/funcion
  - creacion

# --- Clasificación ---
lib: numpy
mod: np
tipo: funcion

# --- Comportamiento ---
retorna: ndarray
inplace: false

# --- Dependencias ---
requiere:
  - concepto_shape
  - concepto_dtype

draft: false
---

# np.full — crea un array de la shape dada relleno con un valor constante

`np.full` fabrica un [[concepto_ndarray|ndarray]] nuevo con la **forma** que le pidas y **todos sus elementos iguales** a un `fill_value` que tú decides. Generaliza a [[np.zeros]] (relleno con `0`) y [[np.ones]] (relleno con `1`) a un valor arbitrario: un centinela como `-1` o `np.inf`, un `np.nan`, un valor por defecto de configuración, etc. Es más claro y directo que `np.ones(shape) * k` o `np.zeros(shape) + k`.

## La idea

`np.full` materializa el tensor descrito por `shape` con cada celda puesta a `fill_value`. El mapa de forma es directo, igual que en `zeros`/`ones`; lo nuevo es que el valor constante es un parámetro.

$$ (\text{shape}, \text{fill\_value}) \;\xrightarrow{\ \text{full}\ }\; \text{array donde } a_{i_0\dots i_{k-1}} = \text{fill\_value}\ \ \forall\, \text{índice} $$

La forma de salida **es** el argumento `shape`; todos sus $\prod_i n_i$ elementos comparten el mismo valor. El [[concepto_dtype|dtype]], si no lo fijas, se **infiere de `fill_value`**.

## Firma

```python
np.full(
    shape,             # int | tuple[int]: la forma del array de salida
    fill_value,        # escalar (o array broadcasteable): el valor constante
    dtype=None,        # dtype: None ⇒ se infiere de fill_value
    order='C',         # {'C', 'F'}: disposición en memoria
    *,
    like=None,         # array_like: referencia para crear con otra librería compatible
) -> ndarray
```

## Los parámetros en detalle

### `shape` — la forma del array de salida
Obligatorio. **Entero** → vector 1D; **tupla** → un eje por componente. Es el [[concepto_shape|shape]] exacto del resultado.

```python
np.full(3, 7)          # (3,)     [7, 7, 7]
np.full((2, 2), 9.5)   # (2, 2)   matriz de 9.5
np.full((2, 3, 4), -1) # (2, 3, 4) tensor de -1
```

### `fill_value` — el valor constante
El valor que va en **todas** las celdas. Normalmente un escalar, pero también acepta un array **broadcasteable** con `shape` (se difunde sobre la forma pedida). Cuando `dtype=None`, **el dtype del resultado se infiere de este valor**:

```python
np.full(3, 7).dtype       # int64    ← 7 es entero
np.full(3, 7.0).dtype     # float64  ← 7.0 es flotante
np.full(3, np.nan)        # [nan, nan, nan]  → fuerza float (nan no es entero)
np.full((2, 3), [1, 2, 3])  # cada fila es [1, 2, 3]  → fill_value broadcasteado
```

### `dtype` — tipo explícito (sobrescribe el inferido)
Si lo fijas, ignora la inferencia de `fill_value`. Útil para fijar precisión o forzar un tipo (ver [[concepto_dtype]]). Ojo: rellenar con un float en un array entero **trunca**.

```python
np.full(3, 7, dtype=np.float32)   # [7., 7., 7.] en float32
np.full(3, 2.9, dtype=int)        # [2, 2, 2]  → trunca hacia 0
```

### `order` — disposición en memoria
`'C'` (filas contiguas, por defecto) o `'F'` (columnas contiguas). Solo afecta al rendimiento en 2D+.

### `like` — prototipo de otra librería
Solo-palabra-clave (`*`). Crea un array del **mismo tipo de objeto** que `like` si este implementa el protocolo de array de NumPy.

## El caso N-D

La forma de salida es la tupla `shape` tal cual, con el `fill_value` replicado en cada celda.

```python
# 4D real: lote inicializado a un centinela "sin medir todavía"
t = np.full((2, 3, 4, 5), -1.0)   # 4D: (lote, canal, alto, ancho), todo -1
t.shape   # (2, 3, 4, 5)
t.ndim    # 4
t.size    # 120  → los 120 elementos valen -1.0

# 5D real: lote de vídeo inicializado a infinito (centinela de "máximo aún no hallado")
v = np.full((8, 16, 3, 64, 64), np.inf)  # 5D: (lote, frames, canal, alto, ancho)
v.shape   # (8, 16, 3, 64, 64)
v.ndim    # 5
v[0, 0, 0, 0, 0]   # inf  → cualquier celda es el centinela
```

El `(2, 3, 4, 5)` se lee como cualquier tensor 4D (**lote, canal, alto, ancho**); lo que aporta `np.full` es arrancar con un valor con significado (`-1` = "sin asignar", `np.inf` = "máximo pendiente", `np.nan` = "dato ausente") en vez de un 0 que podría confundirse con un dato real.

## Casos de uso

### Inicializar con un centinela (sentinel)
```python
distancias = np.full(n, np.inf)    # "infinito" como punto de partida (Dijkstra)
ids = np.full(n, -1, dtype=int)    # -1 = "sin asignar"
```

### Matriz de un valor por defecto
```python
config = np.full((10, 10), 0.5)    # rejilla con valor neutro 0.5
```

### Marcar "dato ausente" con NaN
```python
serie = np.full(100, np.nan)       # se sobrescriben solo las posiciones con dato real
```

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| dtype entero inesperado | `fill_value` es `int`, el dtype se infiere de él | pasar `7.0` o `dtype=float` |
| `nan`/`inf` "se rompen" en un array entero | `nan`/`inf` solo existen en float | usar `dtype=float` |
| El float de relleno se truncó | `dtype=int` explícito trunca hacia 0 | quitar el `dtype` o usar float |
| `np.full((2, 3), [1, 2])` falla | el array `fill_value` no es broadcasteable con `shape` | ajustar la forma del valor |

## Notas relacionadas

- [[concepto_shape]] — la forma de salida es el argumento `shape`
- [[concepto_dtype]] — el dtype se infiere de `fill_value` salvo que lo fijes
- [[np.zeros]] · [[np.ones]] — casos particulares (`fill_value` 0 y 1)
- [[np.empty]] — sin inicializar, cuando vas a sobrescribir todo
- [[np.full_like]] — misma shape/dtype que otro array, con tu valor
