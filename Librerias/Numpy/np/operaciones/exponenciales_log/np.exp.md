---
title: np.exp — exponencial natural e^x elemento a elemento (ufunc)
aliases:
  - exp
  - np.exp
  - exponencial
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
  - concepto_dtype

draft: false
---

# np.exp — exponencial natural e^x elemento a elemento (ufunc)

`np.exp` es una **ufunc unaria**: aplica la **exponencial natural** $e^{x_i}$ a cada elemento, sin
mirar a sus vecinos y **sin cambiar el shape**. Es la inversa de [[np.log]]: siempre positiva, vale
`1` en `0` y **crece muy rápido**. Por eso es el corazón del *softmax* y de los decaimientos
exponenciales. La trampa: para `x` grande **desborda** a `inf` (con `RuntimeWarning`), así que rara
vez se usa "cruda" sin estabilizar antes.

## La idea en una fórmula

Cada elemento se transforma de forma independiente; el shape se **conserva**:

$$
z_i = e^{x_i} \qquad (n_0,\dots,n_k)\ \xrightarrow{\ \text{exp}\ }\ (n_0,\dots,n_k)
$$

con $e \approx 2.71828$. La función es estrictamente creciente y positiva; un cambio aditivo en la
entrada es un factor multiplicativo en la salida ($e^{a+b}=e^a e^b$).

| `x` | $e^{x}$ |
|-----|---------|
| `-1` | `0.368` |
| `0` | `1.0` |
| `1` | `2.718` |
| `10` | `22026.5` |
| `800` | `inf` (overflow) |

## Firma

```python
np.exp(
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

## Los parámetros en detalle

### `x` — el tensor de entrada
`array_like` (ndarray, lista, escalar). Real o complejo; los enteros se promueven a float. El shape
de la salida es exactamente el de `x`. Es donde aparece la trampa del overflow: valores por encima de
`~709` (en `float64`) ya saturan a `inf`.

### `out` — escribir en un buffer existente
`ndarray` preasignado con el shape de salida. Evita asignar memoria y permite operar in-place
(`np.exp(arr, out=arr)`). El dtype debe ser flotante y compatible bajo `casting`.

### `where` — máscara de cómputo
`array_like` booleano broadcasteable con `x`. Solo calcula la exponencial donde es `True`; donde es
`False`, la posición conserva el valor previo de `out` (basura si no se pasó `out`). Úsalo junto con
`out`.

### `dtype` — tipo de cómputo y salida
Fuerza el tipo flotante de cálculo/salida (p. ej. `float32`). Importa para precisión y para el umbral
de overflow: en `float32` desborda antes (`~88`) que en `float64` (`~709`).

### `casting` — política de conversión
`'no'`, `'equiv'`, `'safe'`, `'same_kind'` (defecto), `'unsafe'`. Controla qué conversiones se
permiten al escribir en `out` o aplicar `dtype`.

### `order` — layout de memoria
`'K'` (defecto), `'C'`, `'F'`, `'A'`. Solo afecta al almacenamiento del resultado, no a sus valores.

## El caso N-D

`np.exp` se aplica **elemento a elemento** sobre cualquier dimensión: no hay `axis`, no colapsa nada,
**conserva el shape**. Un tensor `(d0, d1, d2)` entra y sale como `(d0, d1, d2)`:

```python
T = np.array([[[0., 1.], [-1., 2.]],
              [[3., -3.], [0.5, 10.]]])   # shape (2, 2, 2)
np.exp(T).shape       # (2, 2, 2)  → shape idéntico
np.exp(T)
# [[[ 1.        ,  2.71828183], [ 0.36787944,  7.3890561 ]],
#  [[20.08553692,  0.04978707], [ 1.64872127, 22026.4657948 ]]]
```

## Vectorización

`np.exp` reemplaza un bucle que llamaría a `math.exp` por elemento. La versión vectorizada corre el
bucle en C, sobre memoria contigua:

```python
import math
# Bucle Python (lento):
out = np.empty_like(arr)
for i in range(arr.size):
    out.flat[i] = math.exp(arr.flat[i])

# ufunc (un único bucle en C):
out = np.exp(arr)
```

Es el principio de [[concepto_vectorizacion]]: describes la transformación, no la iteración. Soporta
`out`/`where` como toda ufunc.

## Valor de retorno

`ndarray` (o escalar de NumPy si la entrada es escalar) con el **mismo shape** que `x` y dtype
**flotante**:

| Entrada (`x`) | dtype salida | nota |
|---------------|--------------|------|
| `float64` | `float64` | precisión completa |
| `float32` | `float32` | desborda antes (`~88`) |
| entero (`int64`...) | `float64` | se promueve a float |
| `complex128` | `complex128` | $e^{a+bi}=e^a(\cos b + i\sin b)$ |

```python
np.exp(np.array([0., 1.])).dtype    # float64
np.exp([0, 1, 2])                   # array([1., 2.71828183, 7.3890561])
np.exp(800)                         # inf  (+ RuntimeWarning: overflow)
```

## Casos de uso

### Softmax estable (restar el máximo evita overflow)
```python
z = z - z.max()                     # estabiliza: el mayor exponente queda en 0
probs = np.exp(z) / np.exp(z).sum() # ninguna exp desborda
```

### Decaimiento exponencial
```python
y = np.exp(-t / tau)                # señal que decae con constante tau
```

### N-D: softmax por fila de un lote
```python
logits = np.array([[1., 2., 3.],
                   [1., 1., 1.]])   # (2, 3): 2 muestras, 3 clases
e = np.exp(logits - logits.max(axis=1, keepdims=True))
probs = e / e.sum(axis=1, keepdims=True)  # cada fila suma 1, mismo shape (2, 3)
```

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| `inf` / `RuntimeWarning: overflow` | `x` grande (`>709` en float64) | restar el máximo / acotar antes |
| Softmax da `nan` | overflow en `exp` antes de normalizar | restar `z.max()` (softmax estable) |
| Pérdida de precisión en `exp(x)-1` | cancelación para `x→0` | usar [[np.expm1]] |
| Esperar enteros | `exp` siempre devuelve float | la salida es flotante por naturaleza |

## Notas relacionadas

- [[concepto_ufuncs]] — `np.exp` es una ufunc unaria; hereda `out`/`where`/`dtype`/`casting`
- [[np.log]] — su inversa: logaritmo natural
- [[np.expm1]] — $e^x-1$ con precisión cerca de 0
- [[np.exp2]] · [[np.power]] · [[np.log2]]
