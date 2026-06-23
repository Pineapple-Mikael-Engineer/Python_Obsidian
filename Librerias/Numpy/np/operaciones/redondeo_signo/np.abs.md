---
title: np.abs — valor absoluto elemento a elemento (ufunc)
aliases:
  - abs
  - np.abs
  - absolute
  - valor absoluto
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
  - concepto_vectorizacion

draft: false
---

# np.abs — valor absoluto elemento a elemento (ufunc)

`np.abs` es una **ufunc unaria**: aplica el valor absoluto $|x_i|$ a **cada elemento** del tensor, sin
mirar a sus vecinos y **sin cambiar el shape**. Es la operación que convierte un signo en magnitud:
recorta la recta real plegándola sobre el `0`. Es un **alias de `np.absolute`** (mismo objeto ufunc) y
es lo que respalda la función nativa `abs()` cuando su argumento es un `ndarray`: `abs(arr)` invoca
`np.absolute`. Con entrada **compleja** no devuelve "el valor sin signo" sino el **módulo**
$\sqrt{a^2+b^2}$.

## La idea en una fórmula

Cada elemento se transforma de forma independiente; el shape se **conserva** intacto:

$$
z_i = |x_i| \qquad (n_0,\dots,n_k)\ \xrightarrow{\ \text{abs}\ }\ (n_0,\dots,n_k)
$$

Para entrada **real**, $|x|$ es la distancia al origen sobre la recta. Para entrada **compleja**
$x = a + bi$, el resultado es el **módulo** (distancia al origen en el plano complejo):

$$
|a + bi| = \sqrt{a^2 + b^2}
$$

Por eso `np.abs(3 + 4j)` da `5.0` y no "un complejo sin signo".

## Firma

```python
np.abs(
    x,                 # array_like: el tensor de entrada (real o complejo)
    /,
    out=None,          # ndarray | None: destino preasignado
    *,
    where=True,        # array_like[bool]: máscara de cómputo
    casting='same_kind',  # política de conversión de tipos
    order='K',         # 'K' | 'C' | 'F' | 'A': layout de memoria del resultado
    dtype=None,        # dtype: fuerza el tipo de cómputo/salida
) -> ndarray
```

`np.abs` es un alias de `np.absolute`; ambas comparten firma y comportamiento.

## Los parámetros en detalle

### `x` — el tensor de entrada
`array_like` (ndarray, lista, escalar). Acepta **enteros, flotantes y complejos**. Se procesa elemento
a elemento; el shape de la salida es exactamente el de `x`.

### `out` — escribir en un buffer existente
`ndarray` (o tupla de uno) preasignado con el shape de la salida. Evita asignar memoria nueva; permite
operar **in-place** pasando el mismo array: `np.abs(arr, out=arr)`. Debe tener un dtype compatible bajo
`casting`.

### `where` — máscara de cómputo
`array_like` booleano broadcasteable con `x`. Solo se calcula `|x_i|` donde `where` es `True`; donde es
`False`, la posición **conserva lo que hubiera en `out`** (basura si no se pasó `out`). Por eso `where`
casi siempre va acompañado de `out`.

```python
arr = np.array([-1.0, -2.0, -3.0])
buf = np.zeros(3)
np.abs(arr, out=buf, where=arr < -1)   # [0., 2., 3.]  el primero queda intacto
```

### `dtype` — tipo de cómputo y salida
Fuerza el tipo en el que se calcula y se devuelve. Útil para promover antes de operar (p. ej. evitar el
overflow del entero más negativo, ver Errores comunes).

### `casting` — política de conversión
`'no'`, `'equiv'`, `'safe'`, `'same_kind'` (defecto), `'unsafe'`. Decide qué conversiones se permiten al
escribir en `out` o al aplicar `dtype`. Con `'no'` prohíbe cualquier conversión.

### `order` — layout de memoria
`'K'` (defecto, imita el de `x`), `'C'`, `'F'`, `'A'`. Solo afecta a **cómo** se almacena el resultado en
memoria, no a sus valores. Rara vez se toca.

## El caso N-D

`np.abs` se aplica **elemento a elemento** sobre cualquier dimensión: no hay `axis`, no colapsa nada,
**conserva el shape**. Un tensor `(d0, d1, d2)` entra y sale como `(d0, d1, d2)`:

```python
T = np.array([[[-1, 2], [-3, 4]],
              [[ 5,-6], [ 7,-8]]])   # shape (2, 2, 2)
np.abs(T).shape        # (2, 2, 2)  → shape idéntico
np.abs(T)
# [[[1, 2], [3, 4]],
#  [[5, 6], [7, 8]]]
```

Cada posición se trata por separado; la estructura del tensor es irrelevante para el cálculo.

## Vectorización

`np.abs` reemplaza un bucle Python que llamaría a `abs()` por elemento. La versión vectorizada corre el
bucle en C, sobre memoria contigua, respetando los `strides`:

```python
# Bucle Python (lento, interpreta n veces):
out = np.empty_like(arr)
for i in range(arr.size):
    out.flat[i] = abs(arr.flat[i])

# ufunc (un único bucle en C):
out = np.abs(arr)
```

Es el principio de [[concepto_vectorizacion]]: describes *qué* transformación aplicar, no *cómo* iterar.
Como toda ufunc, soporta `out`/`where` para reutilizar memoria y operar condicionalmente.

## Valor de retorno

`ndarray` (o escalar de NumPy si la entrada es un escalar) con el **mismo shape** que `x`. El `dtype`
depende de la entrada:

| Entrada (`x`) | dtype salida | nota |
|---------------|--------------|------|
| entero (`int32`, `int64`...) | **mismo entero** | conserva el tipo (puede desbordar, ver abajo) |
| flotante (`float32`, `float64`) | mismo flotante | |
| **complejo** (`complex128`) | **flotante real** (`float64`) | devuelve el **módulo**, no un complejo |

```python
np.abs(np.array([-1, 2, -3])).dtype    # int64    conserva entero
np.abs(np.array([3 + 4j])).dtype       # float64  el módulo es real
```

## Casos de uso

### Error absoluto / MAE
```python
mae = np.mean(np.abs(prediccion - objetivo))   # error medio absoluto
```

### Magnitud de números complejos
```python
senal = np.array([3 + 4j, 0 + 1j, -2 + 0j])
np.abs(senal)        # [5., 1., 2.]  → módulo de cada muestra
```

### N-D: magnitud por elemento de un tensor
```python
campo = np.array([[[ 1, -2], [-3,  4]],
                  [[-5,  6], [ 7, -8]]])   # (2, 2, 2)
np.abs(campo)
# [[[1, 2], [3, 4]],
#  [[5, 6], [7, 8]]]                       # mismo shape, todo positivo
```

### Reconstruir con `np.sign`
```python
x = np.array([-3.0, 2.0, -1.0])
np.sign(x) * np.abs(x)    # vuelve a x: separa y recompone signo y magnitud
```

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| Overflow en el mínimo entero | `-128` en `int8` no tiene opuesto representable (`abs(-128)` da `-128`) | promover: `dtype=np.int64` o pasar a float |
| Esperar un complejo y recibir un float | con entrada compleja devuelve el **módulo** (real) | es el comportamiento correcto; usa `.real`/`.imag` si querías otra cosa |
| Posiciones con basura tras `where` | `where=` sin `out` inicializado | pasar siempre `out=` junto con `where=` |

## Notas relacionadas

- [[concepto_ufuncs]] — `np.abs` es una ufunc unaria; hereda `out`/`where`/`dtype`/`casting`
- [[concepto_vectorizacion]] — por qué sustituye al bucle por elemento
- [[np.fabs]] — variante que siempre devuelve float y rechaza complejos
- [[np.sign]] · [[np.absolute]]
