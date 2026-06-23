---
title: np.tanh — tangente hiperbólica elemento a elemento (ufunc)
aliases:
  - tanh
  - np.tanh
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

# np.tanh — tangente hiperbólica elemento a elemento (ufunc)

`np.tanh` es una **ufunc unaria**: aplica la **tangente hiperbólica** $\tanh(x_i)$ a cada elemento, sin
mirar a sus vecinos y **sin cambiar el shape**. A diferencia de la tangente circular [[np.tan]], **no
es periódica ni tiene asíntotas**: es una **sigmoide** suave, impar y **acotada** en el rango
$(-1, 1)$, centrada en 0. Como satura hacia $\pm 1$ sin desbordar, es **numéricamente estable** (no
hay overflow), lo que la hace la **función de activación** clásica en redes neuronales. Su inverso es
`np.arctanh` (dominio $(-1, 1)$).

## La idea en una fórmula

Cada elemento se transforma de forma independiente; el shape se **conserva**:

$$
z_i = \tanh(x_i) = \frac{\sinh(x_i)}{\cosh(x_i)} = \frac{e^{x_i} - e^{-x_i}}{e^{x_i} + e^{-x_i}} \qquad (n_0,\dots,n_k)\ \xrightarrow{\ \tanh\ }\ (n_0,\dots,n_k)
$$

Es **impar** ($\tanh(-x) = -\tanh(x)$), pasa por el origen y **satura** en $\pm 1$ (asíntotas
horizontales, nunca las alcanza):

| `x` | $\tanh(x)$ |
|-----|------------|
| `-2` | `-0.964` |
| `-1` | `-0.762` |
| `0` | `0.0` |
| `1` | `0.762` |
| `2` | `0.964` |
| `±∞` | `→ ±1` |

## Firma

```python
np.tanh(
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
`array_like` **real** (ndarray, lista, escalar), argumento real cualquiera. Los enteros se promueven a
float. También acepta complejos. El shape de la salida es el de `x`.

### `out` — escribir en un buffer existente
`ndarray` preasignado con el shape de salida. Evita asignar memoria y permite operar in-place
(`np.tanh(arr, out=arr)`). El dtype debe ser flotante (la salida lo es) y compatible bajo `casting`.

### `where` — máscara de cómputo
`array_like` booleano broadcasteable con `x`. Solo calcula la tangente hiperbólica donde es `True`;
donde es `False`, la posición conserva el valor previo de `out` (basura si no se pasó `out`). Úsalo
junto con `out`.

### `dtype` — tipo de cómputo y salida
Fuerza el tipo flotante de cálculo/salida (p. ej. `float32`, habitual en redes neuronales). Controla
precisión y memoria; al estar acotada en $(-1, 1)$ no hay riesgo de overflow.

### `casting` — política de conversión
`'no'`, `'equiv'`, `'safe'`, `'same_kind'` (defecto), `'unsafe'`. Controla qué conversiones se permiten
al escribir en `out` o aplicar `dtype`.

### `order` — layout de memoria
`'K'` (defecto), `'C'`, `'F'`, `'A'`. Solo afecta al almacenamiento del resultado, no a sus valores.

## El caso N-D

`np.tanh` se aplica **elemento a elemento** sobre cualquier dimensión: no hay `axis`, no colapsa nada,
**conserva el shape**. Un tensor `(d0, d1, d2)` entra y sale como `(d0, d1, d2)` (el caso típico: el
tensor de activaciones de una capa):

```python
T = np.array([[[0.0, 1.0], [-1.0, 2.0]],
              [[0.5, -0.5], [3.0, -3.0]]])   # shape (2, 2, 2)
np.tanh(T).shape       # (2, 2, 2)  → shape idéntico
np.tanh(T)
# [[[ 0.   ,  0.762], [-0.762,  0.964]],
#  [[ 0.462, -0.462], [ 0.995, -0.995]]]   # todo dentro de (-1, 1)
```

## Vectorización

`np.tanh` reemplaza un bucle que llamaría a `math.tanh` por elemento. La versión vectorizada corre el
bucle en C, sobre memoria contigua — clave para aplicar la activación a tensores enormes:

```python
import math
# Bucle Python (lento):
out = np.empty_like(arr)
for i in range(arr.size):
    out.flat[i] = math.tanh(arr.flat[i])

# ufunc (un único bucle en C):
out = np.tanh(arr)
```

Es el principio de [[concepto_vectorizacion]]: describes la transformación, no la iteración. Soporta
`out`/`where` como toda ufunc.

## Valor de retorno

`ndarray` (o escalar de NumPy si la entrada es escalar) con el **mismo shape** que `x`, dtype
**flotante** y valores siempre en $(-1, 1)$:

| Entrada (`x`) | dtype salida | nota |
|---------------|--------------|------|
| `float64` | `float64` | precisión doble |
| `float32` | `float32` | típico en deep learning |
| entero (`int64`...) | `float64` | se promueve a float |
| `complex128` | `complex128` | tangente hiperbólica compleja |

```python
np.tanh(np.array([0., 1.])).dtype    # float64
np.tanh([-2, 0, 2])                  # array([-0.964,  0.   ,  0.964])
np.tanh(1000.)                       # 1.0  → satura, NO desborda (estable)
```

## Casos de uso

### Función de activación en redes neuronales (el caso estrella)
```python
z = pesos @ entrada + sesgo
salida = np.tanh(z)    # acota a (-1, 1), suave y centrada en 0
```

### Derivada de la activación (retropropagación)
```python
a = np.tanh(z)
grad = 1 - a**2        # d/dx tanh(x) = 1 - tanh²(x); ≈ 0 al saturar
```

### N-D: activación de un tensor de un batch
```python
Z = np.random.randn(4, 8)   # batch de 4, 8 neuronas
A = np.tanh(Z)              # (4, 8) acotado en (-1, 1); mismo shape
A.shape                    # (4, 8)
```

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| Gradiente nulo en el entrenamiento | `tanh` satura para `|x|` grande (gradiente $1-\tanh^2\approx 0$) | normalizar las entradas; usar otra activación |
| Esperar valores fuera de `(-1, 1)` | `tanh` está acotada por construcción | revisar la función; quizá querías [[np.sinh]] |
| Asumir que satura a `inf` | a diferencia de `sinh`/`cosh`, `tanh` es estable y no desborda | ninguno; es seguro con `x` grande |

## Notas relacionadas

- [[concepto_ufuncs]] — `np.tanh` es una ufunc unaria; hereda `out`/`where`/`dtype`/`casting`
- [[concepto_vectorizacion]] — por qué sustituye al bucle por elemento
- [[np.sinh]] y [[np.cosh]] — su cociente $\sinh/\cosh$ es justamente la tangente hiperbólica
- [[np.tan]] · [[np.exp]]
