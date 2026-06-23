---
title: np.array_split — parte un array en sub-arrays admitiendo partes desiguales
aliases:
  - array_split
  - np.array_split
tags:
  - numpy
  - api/funcion
  - manipulacion

# --- Clasificación ---
lib: numpy
mod: np
tipo: funcion

# --- Comportamiento ---
retorna: list[ndarray]
inplace: false

# --- Dependencias ---
requiere:
  - concepto_shape

draft: false
---

# np.array_split — parte un array en sub-arrays admitiendo partes desiguales

`np.array_split` hace lo mismo que [[np.split]] —partir un array a lo largo de un eje en una
**lista** de sub-arrays— pero **sin exigir que el eje sea divisible** por el número de partes.
Cuando el reparto no es exacto, distribuye el resto repartiendo los elementos sobrantes entre los
primeros trozos. Es la versión "tolerante" de `split`: la que se usa cuando no se controla si el
tamaño del eje es divisible.

## La idea en una fórmula

La diferencia clave con `split` está **solo en el modo entero**. Al partir un eje de tamaño $n_p$ en
$s$ partes, `array_split` reparte el resto $r = n_p \bmod s$: los **primeros $r$ trozos** reciben un
elemento extra. Cada trozo tiene tamaño $\lceil n_p/s\rceil$ o $\lfloor n_p/s\rfloor$:

$$
(n_0,\dots,n_p,\dots,n_{k-1})
\;\xrightarrow{\ \text{array\_split},\ s\ \text{partes, axis}=p\ }\;
\underbrace{\big[(\dots,\lceil n_p/s\rceil,\dots)\big]\times r}_{\text{primeros }r\text{ trozos}}
\;+\;
\underbrace{\big[(\dots,\lfloor n_p/s\rfloor,\dots)\big]\times(s-r)}_{\text{el resto}}
$$

Por ejemplo, **7 elementos en 3 partes** ($n_p=7,\ s=3,\ r=1$): los tamaños son $3,2,2$. Con
`np.split` esto sería un `ValueError`; con `array_split` simplemente funciona.

> [!tip] La regla mental: split exige exacto, array_split nunca falla por tamaño
> `np.split(a, 3)` → error si `len(a)` no es múltiplo de 3.
> `np.array_split(a, 3)` → siempre devuelve 3 trozos, repartiendo el sobrante.

## Firma

```python
np.array_split(
    ary,                  # array_like: el array a partir
    indices_or_sections,  # int | sequence[int]: nº de partes, o puntos de corte
    axis=0,               # int: eje a lo largo del cual se parte
) -> list[ndarray]
```

La firma es **idéntica** a la de [[np.split]]; cambia solo el comportamiento del modo entero.

## Los parámetros en detalle

### `ary` — el array a partir
`array_like` de cualquier dimensión. Los sub-arrays devueltos son **vistas** sobre su buffer (ver
[[concepto_views_vs_copias]]); no se copia memoria.

### `indices_or_sections` — cómo se corta
Dos modos, igual que en `split`:

- **`int` $s$ → $s$ partes "lo más iguales posible".** Aquí está la diferencia: **no exige
  divisibilidad**. Reparte el resto entre los primeros trozos.

  ```python
  [a.shape for a in np.array_split(np.arange(7), 3)]   # [(3,), (2,), (2,)]
  [a.shape for a in np.array_split(np.arange(8), 3)]   # [(3,), (3,), (2,)]
  ```

- **secuencia de índices `[c1, c2, ...]` → puntos de corte.** Idéntico a `split`: trocea en
  `ary[:c1]`, `ary[c1:c2]`, ... En este modo `split` y `array_split` se comportan **exactamente
  igual** (ninguno de los dos exige divisibilidad con índices).

### `axis` — qué eje se parte
`int`, por defecto `0`. Solo cambia ese eje; el resto del shape se conserva en cada trozo. Admite
ejes negativos.

## El caso N-D

La mecánica N-D es la de `split`: **solo el eje de `axis` se trocea**, los demás quedan idénticos. La
única diferencia es que en modo entero los tamaños a lo largo de ese eje pueden diferir en 1.

| `ary.shape` | `indices_or_sections` | `axis` | salida |
|---|---|---|---|
| `(7,)` | `3` | `0` | `(3,)`, `(2,)`, `(2,)` |
| `(5, 4)` | `2` | `0` | `(3, 4)`, `(2, 4)` |
| `(2, 7, 4)` | `3` | `1` | `(2, 3, 4)`, `(2, 2, 4)`, `(2, 2, 4)` |
| `(4, 5)` | `3` | `-1` | `(4, 2)`, `(4, 2)`, `(4, 1)` |

```python
# Tensor (2, 7, 4): partir el eje del medio (7) en 3 → tamaños 3,2,2
T = np.arange(2*7*4).reshape(2, 7, 4)
[p.shape for p in np.array_split(T, 3, axis=1)]   # [(2, 3, 4), (2, 2, 4), (2, 2, 4)]
```

## Vectorización

Igual que [[np.split]], reemplaza el cálculo manual de los índices de corte por una sola llamada
declarativa, sin copiar datos (cada trozo es una **vista**). La ventaja frente a `split` no es de
rendimiento sino de **robustez**: no necesitas comprobar la divisibilidad del eje antes de partir,
lo que evita un `if len(a) % n` defensivo (ver [[concepto_vectorizacion]]):

```python
# Con split haría falta blindar el tamaño:
n = 3
if len(arr) % n == 0:
    trozos = np.split(arr, n)
else:
    trozos = np.array_split(arr, n)   # ... o directamente esto siempre

# array_split lo absorbe sin el guard:
trozos = np.array_split(arr, n)
```

## Valor de retorno

Devuelve una **`list` de `ndarray`** de longitud $s$ (modo entero) o `len(indices)+1` (modo cortes).
Cada elemento es una **vista** sobre `ary`. En modo entero con resto, los trozos **no** tienen todos
el mismo shape.

| Entrada | `indices_or_sections` | longitud | shapes de los trozos |
|---|---|---|---|
| `(7,)` | `3` | 3 | `(3,)`, `(2,)`, `(2,)` |
| `(10,)` | `4` | 4 | `(3,)`, `(3,)`, `(2,)`, `(2,)` |
| `(m, n)` | `[c1]`, `axis=1` | 2 | `(m, c1)`, `(m, n-c1)` |

```python
type(np.array_split(np.arange(7), 3))   # <class 'list'>
```

## Casos de uso

### Repartir N elementos en K lotes sin preocuparse del resto
```python
datos = np.arange(100)
lotes = np.array_split(datos, 7)   # 7 lotes (100 no es múltiplo de 7) → tamaños 15,15,...,14
[len(l) for l in lotes]            # [15, 15, 14, 14, 14, 14, 14]
```

### Dividir un dataset en `k` folds para validación cruzada
```python
X = np.random.rand(53, 4)          # 53 filas, no divisible
folds = np.array_split(X, 5, axis=0)   # 5 folds: 11,11,11,10,10 filas
[f.shape[0] for f in folds]            # [11, 11, 11, 10, 10]
```

### N-D: trocear un tensor por un eje no divisible
```python
T = np.arange(3*5*2).reshape(3, 5, 2)
partes = np.array_split(T, 2, axis=1)   # eje de tamaño 5 en 2 → 3 y 2
[p.shape for p in partes]               # [(3, 3, 2), (3, 2, 2)]
```

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| Esperar trozos iguales y obtener tamaños distintos | con resto, los primeros trozos llevan 1 extra | es el comportamiento esperado; usar [[np.split]] si se requiere exactitud |
| Pasar más partes que elementos | `array_split(a, 10)` con `len(a)=3` | no es error: devuelve trozos vacíos al final |
| Esperar un array y recibir una lista | devuelve `list[ndarray]` | desempaquetar o indexar la lista |
| Modificar un trozo cambia el original | los trozos son vistas | usar `.copy()` para independencia |

## Notas relacionadas

- [[concepto_shape]] — qué le pasa al shape al trocear un eje
- [[np.split]] — la versión que **exige** división exacta (la diferencia clave)
- [[np.concatenate]] — la operación inversa
- [[np.vsplit]] · [[np.hsplit]] · [[np.dsplit]] — atajos por eje fijo
