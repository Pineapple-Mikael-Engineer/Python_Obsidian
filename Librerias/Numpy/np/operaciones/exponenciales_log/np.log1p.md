---
title: np.log1p — logaritmo de (1 + x) con precisión elemento a elemento (ufunc)
aliases:
  - log1p
  - np.log1p
  - log(1+x)
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

# np.log1p — logaritmo de (1 + x) con precisión elemento a elemento (ufunc)

`np.log1p` es una **ufunc unaria**: calcula $\ln(1+x_i)$ a cada elemento de forma independiente y
**sin cambiar el shape**. Su razón de ser es la **precisión numérica para $x$ pequeño**: cuando
$x\to 0$, formar `1 + x` en coma flotante **pierde dígitos** (el `1` aplasta los bits bajos de `x`), y
`np.log(1 + x)` arrastra ese error; `np.log1p` evita esa cancelación calculando el logaritmo
directamente sobre $x$. Es la pareja inversa de [[np.expm1]] ($\ln(1+(e^x-1))=x$). La trampa del
dominio se desplaza: aquí el límite es $x_i\le -1$ → `nan` (o `-inf` en $x_i=-1$) acompañado de un
`RuntimeWarning`, **no** una excepción.

## La idea en una fórmula

Cada elemento se transforma de forma independiente; el shape se **conserva**:

$$
z_i = \ln(1 + x_i) \qquad (n_0,\dots,n_k)\ \xrightarrow{\ \text{log1p}\ }\ (n_0,\dots,n_k)
$$

Equivale matemáticamente a $\ln(1+x_i)$, pero **numéricamente** está construida para no perder
precisión cerca de $0$, donde $\ln(1+x)\approx x$. Está definida para $x_i>-1$:

| `x` | $\ln(1+x)$ |
|-----|------------|
| `0` | `0.0` |
| `np.e - 1` | `1.0` |
| `1e-15` | `1e-15` (preciso; `log(1+1e-15)` daría peor) |
| `-1` | `-inf` + `RuntimeWarning` |
| `<-1` | `nan` + `RuntimeWarning` |

## Firma

```python
np.log1p(
    x,                 # array_like: el tensor de entrada (real, x > -1)
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
válido es $x>-1$** (porque $1+x>0$): en $x=-1$ devuelve `-inf` y en $x<-1$ devuelve `nan`, ambos
**con `RuntimeWarning`, no excepción**. Su valor añadido se nota justo cuando $x\approx 0$. El shape
de salida es el de `x`.

### `out` — escribir en un buffer existente
`ndarray` preasignado con el shape de salida. Evita asignar memoria y permite operar in-place
(`np.log1p(arr, out=arr)`). El dtype debe ser flotante y compatible bajo `casting`.

### `where` — máscara de cómputo
`array_like` booleano broadcasteable con `x`. Solo calcula el logaritmo donde es `True`; donde es
`False`, la posición conserva el valor previo de `out` (basura si no se pasó `out`). Útil para
**saltarse los $x\le -1$** sin generar el warning:

```python
out = np.zeros_like(x)
np.log1p(x, out=out, where=x > -1)   # solo donde el dominio es válido
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

`np.log1p` se aplica **elemento a elemento** sobre cualquier dimensión: no hay `axis`, no colapsa
nada, **conserva el shape**. Un tensor `(d0, d1, d2)` entra y sale como `(d0, d1, d2)`:

```python
T = np.array([[[0.0, np.e - 1], [1.0, 9.0]],
              [[1e-15, -0.5], [0.0, 3.0]]])   # shape (2, 2, 2)
np.log1p(T).shape       # (2, 2, 2)  → shape idéntico
np.log1p(T)
# [[[0.00000000e+00, 1.00000000e+00], [6.93147181e-01, 2.30258509e+00]],
#  [[1.00000000e-15, -6.93147181e-01], [0.00000000e+00, 1.38629436e+00]]]
```

## Vectorización

`np.log1p` reemplaza un bucle que llamaría a `math.log1p` por elemento. La versión vectorizada corre
el bucle en C, sobre memoria contigua:

```python
import math
# Bucle Python (lento):
out = np.empty_like(arr)
for i in range(arr.size):
    out.flat[i] = math.log1p(arr.flat[i])

# ufunc (un único bucle en C):
out = np.log1p(arr)
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
np.log1p(np.array([0., np.e - 1])).dtype   # float64
np.log1p([0, np.e - 1])                     # array([0., 1.])
```

## Casos de uso

### La ganancia de precisión frente a `np.log(1 + x)`
El motivo de existir de la función. Para $x$ minúsculo, `1 + x` redondea y `np.log` pierde dígitos:

```python
x = 1e-15
np.log(1 + x)    # 1.1102230246251565e-15  ← error grande: 1+x se redondeó
np.log1p(x)      # 9.999999999999995e-16   ← correcto (≈ 1e-15)

# El valor exacto de ln(1 + 1e-15) ≈ 1e-15. log(1+x) yerra en ~11 %;
# log1p acierta hasta el último dígito porque nunca forma 1 + x.
```

Cerca de $x=0$ vale la aproximación $\ln(1+x)\approx x$, y `log1p` la respeta numéricamente.

### Tasas de crecimiento / retornos log pequeños (finanzas)
```python
retornos = np.array([0.0003, -0.0011, 0.0007])   # cambios diarios ~0.1 %
log_ret = np.log1p(retornos)    # retornos logarítmicos sin pérdida de precisión
```

### Transformación log1p para datos sesgados (incluye el 0)
```python
conteos = np.array([0, 1, 5, 100, 9999])
np.log1p(conteos)    # comprime la cola y deja log1p(0)=0 (sin -inf)
```

### N-D: log1p por elemento de un tensor
```python
T = np.array([[[0.0, np.e - 1], [1.0, 9.0]],
              [[1e-15, -0.5], [0.0, 3.0]]])   # (2, 2, 2)
np.log1p(T)
# [[[0.00000000e+00, 1.00000000e+00], [6.93147181e-01, 2.30258509e+00]],
#  [[1.00000000e-15, -6.93147181e-01], [0.00000000e+00, 1.38629436e+00]]]   # mismo shape
```

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| `-inf` en el resultado | `x == -1` (no es excepción, es warning) | revisar que `1 + x > 0` |
| `nan` en el resultado | `x < -1` (no es excepción, es warning) | revisar el dominio o `where=x>-1` |
| Pérdida de precisión persistente | usar `np.log(1 + x)` en vez de `np.log1p(x)` | usar `np.log1p` para `x→0` |
| Pasar `1 + x` por error | la función ya suma el `1` internamente | pasar `x`, no `1 + x` |

## Notas relacionadas

- [[concepto_ufuncs]] — `np.log1p` es una ufunc unaria; hereda `out`/`where`/`dtype`/`casting`
- [[np.expm1]] — su pareja inversa: $e^x-1$ con precisión para $x$ pequeño
- [[np.log]] — $\ln x$ general; `log1p` lo afina cuando el argumento es $1+x$ con $x\to 0$
- [[np.log2]] · [[np.log10]]
