---
title: np.log2 — logaritmo en base 2 elemento a elemento (ufunc)
aliases:
  - log2
  - np.log2
  - logaritmo base 2
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

# np.log2 — logaritmo en base 2 elemento a elemento (ufunc)

`np.log2` es una **ufunc unaria**: aplica el **logaritmo en base 2** $\log_2 x_i$ a cada elemento de
forma independiente y **sin cambiar el shape**. Responde "¿cuántas veces se duplica para llegar a
$x_i$?", por lo que es la base natural en **entropía, bits e información**. Es la pareja inversa de
[[np.exp2]] ($\log_2(2^x)=x$) y más preciso que `np.log(x)/np.log(2)`. La trampa del dominio: para
$x_i\le 0$ no lanza excepción, sino que devuelve `nan` (o `-inf` en $x_i=0$) acompañado de un
`RuntimeWarning`.

## La idea en una fórmula

Cada elemento se transforma de forma independiente; el shape se **conserva**:

$$
z_i = \log_2 x_i = \frac{\ln x_i}{\ln 2} \qquad (n_0,\dots,n_k)\ \xrightarrow{\ \text{log2}\ }\ (n_0,\dots,n_k)
$$

El logaritmo en base 2 cuenta **potencias de 2**. Solo está definido para $x_i>0$:

| `x` | $\log_2 x$ |
|-----|------------|
| `1` | `0.0` |
| `2` | `1.0` |
| `8` | `3.0` |
| `1024` | `10.0` |
| `0` | `-inf` + `RuntimeWarning` |
| `<0` | `nan` + `RuntimeWarning` |

## Firma

```python
np.log2(
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
(`np.log2(arr, out=arr)`). El dtype debe ser flotante y compatible bajo `casting`.

### `where` — máscara de cómputo
`array_like` booleano broadcasteable con `x`. Solo calcula el logaritmo donde es `True`; donde es
`False`, la posición conserva el valor previo de `out` (basura si no se pasó `out`). Útil para
**saltarse los $x\le 0$** sin generar el warning:

```python
out = np.zeros_like(x)
np.log2(x, out=out, where=x > 0)   # solo donde el dominio es válido
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

`np.log2` se aplica **elemento a elemento** sobre cualquier dimensión: no hay `axis`, no colapsa nada,
**conserva el shape**. Un tensor `(d0, d1, d2)` entra y sale como `(d0, d1, d2)`:

```python
T = np.array([[[1.0, 2.0], [8.0, 1024.0]],
              [[16.0, 0.5], [64.0, 4.0]]])   # shape (2, 2, 2)
np.log2(T).shape       # (2, 2, 2)  → shape idéntico
np.log2(T)
# [[[ 0.,  1.], [ 3., 10.]],
#  [[ 4., -1.], [ 6.,  2.]]]
```

## Vectorización

`np.log2` reemplaza un bucle que llamaría a `math.log2` por elemento. La versión vectorizada corre el
bucle en C, sobre memoria contigua:

```python
import math
# Bucle Python (lento):
out = np.empty_like(arr)
for i in range(arr.size):
    out.flat[i] = math.log2(arr.flat[i])

# ufunc (un único bucle en C):
out = np.log2(arr)
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
np.log2(np.array([1., 8.])).dtype   # float64
np.log2([1, 2, 8, 1024])            # array([ 0.,  1.,  3., 10.])
```

## Casos de uso

### Entropía de información (bits)
```python
entropia = -np.sum(p * np.log2(p))    # entropía de Shannon en bits
```

### Número de bits necesarios para representar n valores
```python
bits = np.ceil(np.log2(n)).astype(int)
```

### N-D: logaritmo base 2 por elemento de un tensor
```python
T = np.array([[[1.0, 2.0], [8.0, 1024.0]],
              [[16.0, 0.5], [64.0, 4.0]]])   # (2, 2, 2)
np.log2(T)
# [[[ 0.,  1.], [ 3., 10.]],
#  [[ 4., -1.], [ 6.,  2.]]]               # mismo shape
```

### Dominio $x\le 0$: valores no finitos, sin excepción
```python
np.log2(0)    # -inf + RuntimeWarning
np.log2(-1)   # nan  + RuntimeWarning
```

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| `-inf` en el resultado | `x == 0` (no es excepción, es warning) | `np.clip(x, eps, None)` antes |
| `nan` en el resultado | `x < 0` (no es excepción, es warning) | revisar el dominio o `where=x>0` |
| `nan` en una entropía con `p=0` | `log2(0)` aparece al pesar por `p` | usar `where`/`clip`, o `p[p>0]` |
| Pérdida de precisión usando `log(x)/log(2)` | dos logaritmos en vez de uno dedicado | usar `np.log2` directamente |

## Notas relacionadas

- [[concepto_ufuncs]] — `np.log2` es una ufunc unaria; hereda `out`/`where`/`dtype`/`casting`
- [[np.exp2]] — su pareja inversa: $\log_2(2^x)=x$
- [[np.log]] — logaritmo natural (mismo dominio $x>0$)
- [[np.log10]] · [[np.log1p]] · [[np.clip]]
