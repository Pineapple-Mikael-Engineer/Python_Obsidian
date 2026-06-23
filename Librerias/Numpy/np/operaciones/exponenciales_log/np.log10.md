---
title: np.log10 — logaritmo en base 10 elemento a elemento (ufunc)
aliases:
  - log10
  - np.log10
  - logaritmo base 10
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

# np.log10 — logaritmo en base 10 elemento a elemento (ufunc)

`np.log10` es una **ufunc unaria**: aplica el **logaritmo en base 10** $\log_{10} x_i$ a cada elemento
de forma independiente y **sin cambiar el shape**. Cuenta **órdenes de magnitud** (potencias de 10),
por lo que es la base de las **escalas logarítmicas, decibelios, pH y la magnitud sísmica**. Es más
preciso que `np.log(x)/np.log(10)`. La trampa del dominio: para $x_i\le 0$ no lanza excepción, sino
que devuelve `nan` (o `-inf` en $x_i=0$) acompañado de un `RuntimeWarning`.

## La idea en una fórmula

Cada elemento se transforma de forma independiente; el shape se **conserva**:

$$
z_i = \log_{10} x_i = \frac{\ln x_i}{\ln 10} \qquad (n_0,\dots,n_k)\ \xrightarrow{\ \text{log10}\ }\ (n_0,\dots,n_k)
$$

El logaritmo decimal responde "¿cuántos ceros / cuántos órdenes de magnitud tiene x?". Solo está
definido para $x_i>0$:

| `x` | $\log_{10} x$ |
|-----|---------------|
| `1` | `0.0` |
| `10` | `1.0` |
| `1000` | `3.0` |
| `0` | `-inf` + `RuntimeWarning` |
| `<0` | `nan` + `RuntimeWarning` |

## Firma

```python
np.log10(
    x,                 # array_like: el tensor de entrada (real, x > 0)
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
`array_like` **real** (ndarray, lista, escalar). Los enteros se promueven a float. El **dominio
válido es $x>0$**: en $x=0$ devuelve `-inf` y en $x<0$ devuelve `nan`, ambos **con
`RuntimeWarning`, no excepción** (el cómputo continúa con valores no finitos). El shape de salida es
el de `x`.

### `out` — escribir en un buffer existente
`ndarray` preasignado con el shape de salida. Evita asignar memoria y permite operar in-place
(`np.log10(arr, out=arr)`). El dtype debe ser flotante y compatible bajo `casting`.

### `where` — máscara de cómputo
`array_like` booleano broadcasteable con `x`. Solo calcula el logaritmo donde es `True`; donde es
`False`, la posición conserva el valor previo de `out` (basura si no se pasó `out`). Útil para
**saltarse los $x\le 0$** sin generar el warning:

```python
out = np.zeros_like(x)
np.log10(x, out=out, where=x > 0)   # solo donde el dominio es válido
```

### `dtype` — tipo de cómputo y salida
Fuerza el tipo flotante de cálculo/salida (p. ej. `float32`). La salida siempre es flotante aunque la
entrada sea entera.

### `casting` — política de conversión
`'no'`, `'equiv'`, `'safe'`, `'same_kind'` (defecto), `'unsafe'`. Controla qué conversiones se
permiten al escribir en `out` o aplicar `dtype`.

### `order` — layout de memoria
`'K'` (defecto), `'C'`, `'F'`, `'A'`. Solo afecta al almacenamiento del resultado, no a sus valores.

## El caso N-D

`np.log10` se aplica **elemento a elemento** sobre cualquier dimensión: no hay `axis`, no colapsa
nada, **conserva el shape**. Un tensor `(d0, d1, d2)` entra y sale como `(d0, d1, d2)`:

```python
T = np.array([[[1.0, 10.0], [1000.0, 1.0]],
              [[100.0, 0.1], [1e6, 10.0]]])   # shape (2, 2, 2)
np.log10(T).shape       # (2, 2, 2)  → shape idéntico
np.log10(T)
# [[[0., 1.], [3., 0.]],
#  [[2., -1.], [6., 1.]]]
```

## Vectorización

`np.log10` reemplaza un bucle que llamaría a `math.log10` por elemento. La versión vectorizada corre
el bucle en C, sobre memoria contigua:

```python
import math
# Bucle Python (lento):
out = np.empty_like(arr)
for i in range(arr.size):
    out.flat[i] = math.log10(arr.flat[i])

# ufunc (un único bucle en C):
out = np.log10(arr)
```

Es el principio de [[concepto_vectorizacion]]: describes la transformación, no la iteración. Soporta
`out`/`where` como toda ufunc.

## Valor de retorno

`ndarray` (o escalar de NumPy si la entrada es escalar) con el **mismo shape** que `x` y dtype
**flotante**:

| Entrada (`x`) | dtype salida | nota |
|---------------|--------------|------|
| `float64` | `float64` | precisión doble |
| `float32` | `float32` | conserva la precisión |
| entero (`int64`...) | `float64` | se promueve a float |

```python
np.log10(np.array([1., 1000.])).dtype   # float64
np.log10([1, 10, 100, 1000])            # array([0., 1., 2., 3.])
```

## Casos de uso

### Decibelios
```python
db = 20 * np.log10(amplitud / referencia)   # nivel en dB
```

### Órdenes de magnitud / escala logarítmica
```python
orden = np.floor(np.log10(np.abs(valores)))   # exponente decimal de cada valor
```

### N-D: logaritmo base 10 por elemento de un tensor
```python
T = np.array([[[1.0, 10.0], [1000.0, 1.0]],
              [[100.0, 0.1], [1e6, 10.0]]])   # (2, 2, 2)
np.log10(T)
# [[[0., 1.], [3., 0.]],
#  [[2., -1.], [6., 1.]]]               # mismo shape
```

### Dominio $x\le 0$: valores no finitos, sin excepción
```python
np.log10(0)    # -inf + RuntimeWarning
np.log10(-1)   # nan  + RuntimeWarning
```

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| `-inf` en el resultado | `x == 0` (no es excepción, es warning) | `np.clip(x, eps, None)` antes |
| `nan` en el resultado | `x < 0` (no es excepción, es warning) | revisar el dominio o `where=x>0` |
| Confundir base 10 con ln | `np.log` es natural, `np.log10` es decimal | elegir la función correcta |
| Pérdida de precisión usando `log(x)/log(10)` | dos logaritmos en vez de uno dedicado | usar `np.log10` directamente |

## Notas relacionadas

- [[concepto_ufuncs]] — `np.log10` es una ufunc unaria; hereda `out`/`where`/`dtype`/`casting`
- [[np.log]] — logaritmo natural (mismo dominio $x>0$)
- [[np.log2]] — logaritmo en base 2 (bits/entropía)
- [[np.log1p]] · [[np.power]] · [[np.clip]]
