---
title: np.expm1 — e^x − 1 con precisión cerca de 0 (ufunc)
aliases:
  - expm1
  - np.expm1
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

# np.expm1 — e^x − 1 con precisión cerca de 0 (ufunc)

`np.expm1` es una **ufunc unaria**: calcula $e^{x_i}-1$ a cada elemento, **sin cambiar el shape**,
pero con **precisión numérica** para `x` cercano a 0. La razón: cuando `x→0`, $e^x$ vale casi
exactamente `1`, así que `np.exp(x) - 1` resta dos números casi iguales y **pierde dígitos
significativos** (cancelación catastrófica). `expm1` calcula la diferencia directamente, sin formar el
`1` intermedio. Es la pareja de [[np.log1p]] (que calcula $\ln(1+x)$ para el camino inverso).

## La idea en una fórmula

Cada elemento se transforma de forma independiente; el shape se **conserva**:

$$
z_i = e^{x_i} - 1 \qquad (n_0,\dots,n_k)\ \xrightarrow{\ \text{expm1}\ }\ (n_0,\dots,n_k)
$$

El valor es matemáticamente idéntico a `exp(x) - 1`; lo que cambia es **cómo** se computa. Cerca de 0,
$e^x - 1 \approx x + \tfrac{x^2}{2} + \dots$, una serie que `expm1` aprovecha en vez de cancelar el `1`.

| `x` | $e^{x}-1$ |
|-----|-----------|
| `-0.5` | `-0.3935` |
| `0` | `0.0` |
| `1e-10` | `1.0e-10` |
| `1` | `1.718` |

## Firma

```python
np.expm1(
    x,                 # array_like: el tensor de entrada (real)
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
`array_like` real (ndarray, lista, escalar). Los enteros se promueven a float. El shape de la salida
es exactamente el de `x`. El interés está justo cuando `x` es **pequeño** (tasas, incrementos
diminutos): ahí `expm1` gana precisión frente a `exp(x) - 1`.

### `out` — escribir en un buffer existente
`ndarray` preasignado con el shape de salida. Evita asignar memoria y permite operar in-place
(`np.expm1(arr, out=arr)`). El dtype debe ser flotante y compatible bajo `casting`.

### `where` — máscara de cómputo
`array_like` booleano broadcasteable con `x`. Solo calcula donde es `True`; donde es `False`, la
posición conserva el valor previo de `out` (basura si no se pasó `out`). Úsalo junto con `out`.

### `dtype` — tipo de cómputo y salida
Fuerza el tipo flotante de cálculo/salida (p. ej. `float32`). Controla la precisión del resultado.

### `casting` — política de conversión
`'no'`, `'equiv'`, `'safe'`, `'same_kind'` (defecto), `'unsafe'`. Controla qué conversiones se
permiten al escribir en `out` o aplicar `dtype`.

### `order` — layout de memoria
`'K'` (defecto), `'C'`, `'F'`, `'A'`. Solo afecta al almacenamiento del resultado, no a sus valores.

## El caso N-D

`np.expm1` se aplica **elemento a elemento** sobre cualquier dimensión: no hay `axis`, no colapsa
nada, **conserva el shape**. Un tensor `(d0, d1, d2)` entra y sale como `(d0, d1, d2)`:

```python
T = np.array([[[0., 1e-10], [-0.5, 1.]],
              [[2., -1.], [1e-12, 0.]]])   # shape (2, 2, 2)
np.expm1(T).shape       # (2, 2, 2)  → shape idéntico
```

## Vectorización

`np.expm1` reemplaza un bucle que llamaría a `math.expm1` por elemento. La versión vectorizada corre
el bucle en C, sobre memoria contigua:

```python
import math
# Bucle Python (lento):
out = np.empty_like(arr)
for i in range(arr.size):
    out.flat[i] = math.expm1(arr.flat[i])

# ufunc (un único bucle en C):
out = np.expm1(arr)
```

Es el principio de [[concepto_vectorizacion]]: describes la transformación, no la iteración. Soporta
`out`/`where` como toda ufunc.

## Valor de retorno

`ndarray` (o escalar de NumPy si la entrada es escalar) con el **mismo shape** que `x` y dtype
**flotante**:

| Entrada (`x`) | dtype salida | nota |
|---------------|--------------|------|
| `float64` | `float64` | precisión completa cerca de 0 |
| `float32` | `float32` | conserva la precisión |
| entero (`int64`...) | `float64` | se promueve a float |

La diferencia de precisión frente a `exp(x) - 1` se ve con `x` diminuto:

```python
np.expm1(1e-10)        # 1.00000000005e-10   ← correcto
np.exp(1e-10) - 1      # 1.000000082e-10     ← pierde dígitos por cancelación

np.expm1(1e-15)        # 1.0e-15             ← correcto
np.exp(1e-15) - 1      # 1.11e-15            ← ruido: el 1 absorbió la información
```

## Casos de uso

### Interés compuesto / tasas pequeñas
```python
crecimiento = np.expm1(tasa)        # exacto incluso para tasas diminutas (1e-8)
```

### Diferencias relativas pequeñas
```python
delta = np.expm1(log_ratio)         # (r2-r1)/r1 a partir de log(r2/r1), sin cancelar
```

### N-D: incrementos diminutos por elemento
```python
T = np.full((3, 4), 1e-9)
np.expm1(T)                         # ≈ 1e-9 en cada celda, mismo shape (3, 4)
```

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| Pérdida de precisión cerca de 0 | usar `np.exp(x) - 1` con `x→0` | usar `np.expm1(x)` |
| `inf` / `RuntimeWarning: overflow` | `x` grande (mismo límite que [[np.exp]]) | acotar `x` antes |
| Confundir con su inversa | el camino de vuelta es $\ln(1+x)$ | usar [[np.log1p]] |

## Notas relacionadas

- [[concepto_ufuncs]] — `np.expm1` es una ufunc unaria; hereda `out`/`where`/`dtype`/`casting`
- [[np.log1p]] — su pareja inversa: $\ln(1+x)$ con precisión cerca de 0
- [[np.exp]] — la exponencial sin el `-1`
- [[np.log]] · [[np.exp2]]
