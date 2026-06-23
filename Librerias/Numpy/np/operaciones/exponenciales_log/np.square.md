---
title: np.square — cuadrado elemento a elemento (ufunc)
aliases:
  - square
  - np.square
  - cuadrado
tags:
  - numpy
  - api/funcion
  - transformaciones

# --- Clasificación ---
lib: numpy
mod: np
tipo: funcion

# --- Comportamiento ---
retorna: ndarray
inplace: false

# --- Dependencias ---
requiere:
  - concepto_ufuncs

draft: false
---

# np.square — cuadrado elemento a elemento (ufunc)

`np.square` es una **ufunc unaria**: eleva cada elemento al **cuadrado** $x_i^2$, de forma
independiente y **sin cambiar el shape**. Equivale a `np.power(x, 2)` o `x * x`, pero es más rápida
para arrays grandes y más legible. Acepta cualquier signo (el cuadrado de un negativo es positivo).
Es la inversa (para $x \ge 0$) de [[np.sqrt]]. La trampa a vigilar es el **overflow** con enteros
grandes, ya que el resultado conserva el dtype entero de la entrada.

## La idea en una fórmula

Cada elemento se transforma de forma independiente; el shape se **conserva**:

$$
z_i = x_i^2 \qquad (n_0,\dots,n_k)\ \xrightarrow{\ \text{square}\ }\ (n_0,\dots,n_k)
$$

El cuadrado es siempre $\ge 0$ para entradas reales; no hay restricción de dominio.

| `x` | $x^2$ |
|-----|-------|
| `2` | `4` |
| `-3` | `9` |
| `0` | `0` |
| `1.5` | `2.25` |

## Firma

```python
np.square(
    x,                 # array_like: el tensor de entrada
    /,
    out=None,          # ndarray | None: destino preasignado
    *,
    where=True,        # array_like[bool]: máscara de cómputo
    casting='same_kind',  # política de conversión de tipos
    order='K',         # 'K' | 'C' | 'F' | 'A': layout de memoria del resultado
    dtype=None,        # dtype: fuerza el tipo de cómputo/salida
) -> ndarray
```

## Los parámetros en detalle

### `x` — el tensor de entrada
`array_like` (ndarray, lista, escalar), de cualquier signo y tipo numérico (entero, float, complejo).
El dtype de salida **hereda** el de la entrada: un array `int32` da un cuadrado `int32`, con riesgo de
overflow. El shape de la salida es el de `x`.

### `out` — escribir en un buffer existente
`ndarray` preasignado con el shape de salida. Evita asignar memoria y permite operar in-place
(`np.square(arr, out=arr)`). El dtype debe ser compatible bajo `casting`.

### `where` — máscara de cómputo
`array_like` booleano broadcasteable con `x`. Solo calcula el cuadrado donde es `True`; donde es
`False`, la posición conserva el valor previo de `out` (basura si no se pasó `out`). Úsalo junto con `out`.

### `dtype` — tipo de cómputo y salida
Fuerza el tipo de cálculo/salida. Es la forma de evitar el overflow con enteros: `dtype=np.float64`
(o `np.int64`) ensancha el acumulador antes de elevar al cuadrado.

### `casting` — política de conversión
`'no'`, `'equiv'`, `'safe'`, `'same_kind'` (defecto), `'unsafe'`. Controla qué conversiones se permiten
al escribir en `out` o aplicar `dtype`.

### `order` — layout de memoria
`'K'` (defecto), `'C'`, `'F'`, `'A'`. Solo afecta al almacenamiento del resultado, no a sus valores.

## El caso N-D

`np.square` se aplica **elemento a elemento** sobre cualquier dimensión: no hay `axis`, no colapsa nada,
**conserva el shape**. Un tensor `(d0, d1, d2)` entra y sale como `(d0, d1, d2)`:

```python
T = np.array([[[1., 2.], [3., 4.]],
              [[5., 6.], [7., 8.]]])   # shape (2, 2, 2)
np.square(T).shape     # (2, 2, 2)  → shape idéntico
np.square(T)
# [[[ 1.,  4.], [ 9., 16.]],
#  [[25., 36.], [49., 64.]]]
```

## Vectorización

`np.square` reemplaza un bucle que elevaría al cuadrado por elemento. La versión vectorizada corre el
bucle en C, sobre memoria contigua:

```python
# Bucle Python (lento):
out = np.empty_like(arr)
for i in range(arr.size):
    out.flat[i] = arr.flat[i] ** 2

# ufunc (un único bucle en C):
out = np.square(arr)
```

Es el principio de [[concepto_vectorizacion]]: describes la transformación, no la iteración. Frente a
`x ** 2`, NumPy ejecuta una ruta dedicada (no la potencia general), lo que la hace más rápida en
arrays grandes. Soporta `out`/`where` como toda ufunc.

## Valor de retorno

`ndarray` (o escalar de NumPy si la entrada es escalar) con el **mismo shape** que `x` y el dtype
**heredado** de la entrada:

| Entrada (`x`) | dtype salida | nota |
|---------------|--------------|------|
| `float64` | `float64` | conserva la precisión |
| `float32` | `float32` | conserva la precisión |
| `int32` | `int32` | **riesgo de overflow** con valores grandes |
| `complex128` | `complex128` | $z^2$ complejo |

```python
np.square([1, 2, 3, 4])              # array([ 1,  4,  9, 16])
np.square(np.int32(50000))           # overflow → valor erróneo (int32)
np.square(np.int32(50000), dtype=np.int64)   # 2500000000  → seguro
```

## Casos de uso

### Suma de cuadrados (energía, MSE)
```python
mse = np.mean(np.square(prediccion - objetivo))   # error cuadrático medio
```

### Norma al cuadrado de un vector
```python
v = np.array([3., 4.])
np.sum(np.square(v))     # 25.0  → ||v||²  (evita la sqrt si solo quieres el cuadrado)
```

### N-D: cuadrado por elemento de un tensor
```python
T = np.arange(1, 9, dtype=float).reshape(2, 2, 2)   # (2, 2, 2)
np.square(T)
# [[[ 1.,  4.], [ 9., 16.]],
#  [[25., 36.], [49., 64.]]]                # mismo shape
```

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| Resultado negativo/absurdo | overflow del dtype entero de la entrada | `dtype=np.int64` o `np.float64` |
| Posiciones con basura tras `where` | `where=` sin `out` inicializado | pasar siempre `out=` junto con `where=` |
| Esperar otra potencia | `square` solo eleva a 2 | usar [[np.power]] para exponentes arbitrarios |

## Notas relacionadas

- [[concepto_ufuncs]] — `np.square` es una ufunc unaria; hereda `out`/`where`/`dtype`/`casting`
- [[concepto_vectorizacion]] — por qué sustituye al bucle por elemento
- [[np.sqrt]] — su inversa para $x \ge 0$ ($\sqrt{x}$)
- [[np.power]] · [[np.cbrt]] · [[np.abs]]
