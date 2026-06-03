---
title: scipy.linalg.expm — exponencial de matriz (no elemento a elemento)
aliases:
  - expm
  - scipy.linalg.expm
  - exponencial matricial
tags:
  - scipy
  - api/funcion
  - algebra-lineal
lib: scipy
tipo: funcion
mod: scipy.linalg
retorna: ndarray
requiere:
  - numpy
  - concepto_relacion_numpy
draft: false
---

# scipy.linalg.expm — exponencial de matriz (no elemento a elemento)

Calcula la **exponencial matricial** de una matriz cuadrada `A`, definida por la serie `exp(A) = Σ A^k / k!` (k de 0 a ∞), con `A^0 = I`. No es aplicar `exp` a cada entrada: es la verdadera exponencial de matrices, evaluada mediante **aproximacion de Pade con scaling-and-squaring** (estable y precisa, no por suma directa de la serie). Devuelve un `ndarray` de la **misma forma** que `A`.

Su uso central es resolver **sistemas lineales de EDO** `dy/dt = A·y`, cuya solucion cerrada es `y(t) = expm(A·t)·y0`. Tambien aparece en **cadenas de Markov en tiempo continuo** (matriz de transicion `P(t) = expm(Q·t)`) y en **teoria de control** (matriz de transicion de estados `Φ(t) = expm(A·t)`).

> [!warning] CRITICO: expm(A) ≠ np.exp(A)
> `np.exp(A)` aplica la exponencial **elemento a elemento** (es una ufunc). `scipy.linalg.expm(A)` calcula la **exponencial de la matriz** como objeto algebraico. Dan resultados completamente distintos salvo casos triviales. Para EDO, Markov y control SIEMPRE es `expm`, nunca `np.exp`.

## Firma

```python
scipy.linalg.expm(A) -> ndarray
# A: array_like (N, N)  matriz cuadrada
```

## Valor de retorno

| Entrada | Retorno | Forma |
|---------|---------|-------|
| Matriz `A` de forma `(N, N)` | `expm(A)` | `(N, N)`, mismo dtype flotante |
| Pila `A` de forma `(..., N, N)` | exponencial de cada matriz apilada | `(..., N, N)` |

```python
import numpy as np
from scipy.linalg import expm

A = np.diag([0.0, 1.0])
expm(A)        # → [[1.        , 0.        ],
               #    [0.        , 2.71828183]]
np.exp(A)      # → [[1.        , 1.        ],     # ¡distinto!
               #    [1.        , 2.71828183]]     # exp aplicado a cada entrada
```

## Formas basicas de llamada

| Objetivo | Llamada |
|----------|---------|
| Exponencial de una matriz | `expm(A)` |
| Solucion de EDO en t | `expm(A * t) @ y0` |
| Matriz de transicion de estados | `expm(A * dt)` |
| Transicion de Markov continua | `expm(Q * t)` |

## Parametros en detalle

### `A` (obligatorio)

Matriz **cuadrada** `(N, N)` (o pila `(..., N, N)`). Si no es cuadrada, falla. Se promueve a flotante; conviene pasar `float`/`complex` para evitar truncamientos por enteros.

```python
import numpy as np
from scipy.linalg import expm

A = np.array([[0.0, -1.0],
              [1.0,  0.0]])   # generador de rotacion
expm(A)        # → [[ 0.54030231, -0.84147098],
               #    [ 0.84147098,  0.54030231]]   # = [[cos1, -sin1],[sin1, cos1]]
```

El parametro escalar `t` no es un argumento de `expm`: se incorpora **escalando la matriz** antes de llamar, `expm(A * t)`, porque `exp(A·t)` es lo que resuelve la dinamica.

## Casos de uso

### Sistema lineal de EDO

```python
import numpy as np
from scipy.linalg import expm

# dy/dt = A y,  y(0) = y0  ->  y(t) = expm(A t) y0
A  = np.array([[-0.5,  1.0],
               [ 0.0, -0.3]])
y0 = np.array([2.0, 1.0])

t  = 3.0
yt = expm(A * t) @ y0
yt             # → estado del sistema en t=3 (decaimiento acoplado)
```

### Matriz de transicion de estados (control)

```python
# Sistema x' = A x + B u; en tiempo discreto la matriz de transicion es Phi = expm(A dt)
A   = np.array([[0.0, 1.0],
                [-2.0, -3.0]])
dt  = 0.1
Phi = expm(A * dt)     # propaga el estado un paso de tiempo dt
```

### Cadena de Markov en tiempo continuo

```python
# Q: matriz generadora (filas suman 0). P(t) = expm(Q t) es estocastica por filas.
Q = np.array([[-1.0,  1.0],
              [ 2.0, -2.0]])
P = expm(Q * 0.5)
P.sum(axis=1)          # → [1., 1.]   cada fila suma 1 (matriz de probabilidad)
```

## Buenas practicas

1. Usa `expm` (no `np.exp`) siempre que `A` represente un **operador** (EDO, control, Markov); reserva `np.exp` para transformar datos entrada a entrada.
2. Incorpora el tiempo escalando: `expm(A * t)`. No existe un argumento `t`.
3. Para muchos `y0` con el mismo `A` y `t`, calcula `M = expm(A * t)` una vez y reusa `M @ y0_i`.
4. Pasa `A` ya en flotante para evitar resultados truncados por dtype entero.
5. Para inversa y raiz de la familia, usa `logm` (logaritmo matricial) y `sqrtm` (raiz cuadrada matricial), parte del mismo modulo de funciones de matriz junto a `expm`.

## Errores comunes

| Error | Causa | Solucion |
|-------|-------|----------|
| Resultado absurdo en EDO/Markov | Se uso `np.exp(A)` (elemento a elemento) | Usar `scipy.linalg.expm(A)` |
| `ValueError: expected square matrix` | `A` no es cuadrada | Pasar matriz `(N, N)` |
| Tiempo aplicado mal | Multiplicar fuera: `t * expm(A)` | Escalar dentro: `expm(A * t)` |
| Valores enteros truncados | `A` con dtype entero | Convertir con `A.astype(float)` |
| Confundir con `**` o `@` repetido | `A**k` es potencia elemento a elemento | `expm` ya suma la serie correcta |

## Limitaciones

- Solo matrices **cuadradas**; no hay exponencial de matriz rectangular.
- Para `A` muy grande y dispersa, esta densa; usar `scipy.sparse.linalg.expm` (o `expm_multiply` para `expm(A)·v` sin formar la matriz).
- El costo es de descomposiciones densas O(N^3); para propagar muchos pasos puede convenir factorizar una vez.
- No confundir con las funciones hermanas: `logm` invierte `expm`, `sqrtm` da la raiz; cada una es una funcion de matriz distinta.

## Notas relacionadas

- [[scipy.linalg.logm]]
- [[scipy.linalg.sqrtm]]
- [[scipy.integrate.solve_ivp]]
- [[concepto_relacion_numpy]]
