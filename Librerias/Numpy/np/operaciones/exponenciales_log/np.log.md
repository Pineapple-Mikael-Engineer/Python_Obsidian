---
title: np.log — logaritmo natural (ln) elemento a elemento (ufunc)
aliases:
  - log
  - np.log
  - logaritmo natural
  - ln
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

# np.log — logaritmo natural (ln) elemento a elemento (ufunc)

`np.log` es una **ufunc unaria**: aplica el **logaritmo natural** $\ln x_i$ (base $e$, **no** base 10)
a cada elemento de forma independiente y **sin cambiar el shape**. Pese a su nombre escueto, `np.log`
es **ln**; para base 10 está [[np.log10]] y para base 2, [[np.log2]]. Es el inverso de [[np.exp]]:
$\ln(e^x)=x$. La trampa del dominio: para $x_i\le 0$ no lanza excepción, sino que devuelve `nan` (o
`-inf` en $x_i=0$) acompañado de un `RuntimeWarning`.

## La idea en una fórmula

Cada elemento se transforma de forma independiente; el shape se **conserva**:

$$
z_i = \ln x_i = \log_e x_i \qquad (n_0,\dots,n_k)\ \xrightarrow{\ \text{log}\ }\ (n_0,\dots,n_k)
$$

El logaritmo natural responde "¿a qué exponente elevo e para obtener x?". Solo está definido
para $x_i>0$:

| `x` | $\ln x$ |
|-----|---------|
| `1` | `0.0` |
| `np.e ≈ 2.718` | `1.0` |
| `np.e**2` | `2.0` |
| `0` | `-inf` + `RuntimeWarning` |
| `<0` | `nan` + `RuntimeWarning` |

## Firma

```python
np.log(
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
el de `x`. Para complejos NumPy sí calcula la rama principal, pero la nota asume reales.

### `out` — escribir en un buffer existente
`ndarray` preasignado con el shape de salida. Evita asignar memoria y permite operar in-place
(`np.log(arr, out=arr)`). El dtype debe ser flotante y compatible bajo `casting`.

### `where` — máscara de cómputo
`array_like` booleano broadcasteable con `x`. Solo calcula el logaritmo donde es `True`; donde es
`False`, la posición conserva el valor previo de `out` (basura si no se pasó `out`). Útil para
**saltarse los $x\le 0$** sin generar el warning:

```python
out = np.zeros_like(x)
np.log(x, out=out, where=x > 0)   # solo donde el dominio es válido
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

`np.log` se aplica **elemento a elemento** sobre cualquier dimensión: no hay `axis`, no colapsa nada,
**conserva el shape**. Un tensor `(d0, d1, d2)` entra y sale como `(d0, d1, d2)`:

```python
T = np.array([[[1.0, np.e], [np.e**2, 1.0]],
              [[10.0, 0.5], [100.0, 2.0]]])   # shape (2, 2, 2)
np.log(T).shape       # (2, 2, 2)  → shape idéntico
np.log(T)
# [[[0.        , 1.        ], [2.        , 0.        ]],
#  [[2.30258509, -0.69314718], [4.60517019, 0.69314718]]]
```

## Vectorización

`np.log` reemplaza un bucle que llamaría a `math.log` por elemento. La versión vectorizada corre el
bucle en C, sobre memoria contigua:

```python
import math
# Bucle Python (lento):
out = np.empty_like(arr)
for i in range(arr.size):
    out.flat[i] = math.log(arr.flat[i])

# ufunc (un único bucle en C):
out = np.log(arr)
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
np.log(np.array([1., np.e])).dtype   # float64
np.log([1, np.e, np.e**2])           # array([0., 1., 2.])
```

## Casos de uso

### Log-verosimilitud / cross-entropy
```python
loss = -np.log(np.clip(probs, 1e-12, 1.0))   # recorta para evitar log(0) = -inf
```

### Cambio de base
```python
np.log(x) / np.log(7)    # log en base 7, vía ln
```

### N-D: logaritmo por elemento de un tensor
```python
T = np.array([[[1.0, np.e], [np.e**2, 1.0]],
              [[10.0, 0.5], [100.0, 2.0]]])   # (2, 2, 2)
np.log(T)
# [[[0.        , 1.        ], [2.        , 0.        ]],
#  [[2.30258509, -0.69314718], [4.60517019, 0.69314718]]]   # mismo shape
```

### Dominio $x\le 0$: valores no finitos, sin excepción
```python
np.log(0)    # -inf + RuntimeWarning
np.log(-1)   # nan  + RuntimeWarning
```

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| `-inf` en el resultado | `x == 0` (no es excepción, es warning) | `np.clip(x, eps, None)` antes |
| `nan` en el resultado | `x < 0` (no es excepción, es warning) | revisar el dominio o `where=x>0` |
| Esperar log base 10 y recibir ln | `np.log` es **logaritmo natural**, no decimal | usar [[np.log10]] (o [[np.log2]]) |
| Pérdida de precisión en `log(1+x)` con `x→0` | cancelación catastrófica al sumar `1` | usar [[np.log1p]] |

## Notas relacionadas

- [[concepto_ufuncs]] — `np.log` es una ufunc unaria; hereda `out`/`where`/`dtype`/`casting`
- [[np.exp]] — su pareja inversa: $\ln(e^x)=x$
- [[np.log1p]] — $\ln(1+x)$ con precisión para $x$ pequeño
- [[np.log2]] · [[np.log10]] · [[np.clip]]
