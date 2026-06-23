---
title: np.sqrt — raíz cuadrada elemento a elemento (ufunc)
aliases:
  - sqrt
  - np.sqrt
  - raiz cuadrada
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

# np.sqrt — raíz cuadrada elemento a elemento (ufunc)

`np.sqrt` es una **ufunc unaria**: aplica la **raíz cuadrada** $\sqrt{x_i}$ a cada elemento, de forma
independiente y **sin cambiar el shape**. Equivale a `np.power(x, 0.5)` o `x ** 0.5`, pero es más
rápida y semánticamente clara. Su dominio en reales es $x_i \ge 0$: la trampa habitual es pasar
valores negativos, que producen `nan` con warning en vez de un número complejo. Es la inversa
(para $x \ge 0$) de [[np.square]].

## La idea en una fórmula

Cada elemento se transforma de forma independiente; el shape se **conserva**:

$$
z_i = \sqrt{x_i} \qquad (n_0,\dots,n_k)\ \xrightarrow{\ \text{sqrt}\ }\ (n_0,\dots,n_k)
$$

La operación es válida sobre los reales solo si $x_i \ge 0$; fuera de ese dominio, NumPy devuelve
`nan` (no salta al plano complejo por su cuenta).

| `x` | $\sqrt{x}$ |
|-----|------------|
| `4` | `2.0` |
| `2` | `1.4142...` |
| `0` | `0.0` |
| `-1` | `nan` + warning |

## Firma

```python
np.sqrt(
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
`array_like` (ndarray, lista, escalar). Los enteros se promueven a float. Si es **real**, el dominio
es $x \ge 0$ (los negativos dan `nan`). Si es **complejo** (o `dtype=complex`), calcula la raíz
principal sin restricción de signo. El shape de la salida es el de `x`.

### `out` — escribir en un buffer existente
`ndarray` preasignado con el shape de salida. Evita asignar memoria y permite operar in-place
(`np.sqrt(arr, out=arr)`). El dtype debe ser flotante/complejo y compatible bajo `casting`.

### `where` — máscara de cómputo
`array_like` booleano broadcasteable con `x`. Solo calcula la raíz donde es `True`; donde es `False`,
la posición conserva el valor previo de `out` (basura si no se pasó `out`). Úsalo junto con `out`.

### `dtype` — tipo de cómputo y salida
Fuerza el tipo flotante/complejo de cálculo/salida (`float32`, `complex128`...). Pasar `dtype=complex`
es la forma directa de habilitar raíces de negativos: `np.sqrt(arr, dtype=complex)`.

### `casting` — política de conversión
`'no'`, `'equiv'`, `'safe'`, `'same_kind'` (defecto), `'unsafe'`. Controla qué conversiones se permiten
al escribir en `out` o aplicar `dtype`.

### `order` — layout de memoria
`'K'` (defecto), `'C'`, `'F'`, `'A'`. Solo afecta al almacenamiento del resultado, no a sus valores.

## El caso N-D

`np.sqrt` se aplica **elemento a elemento** sobre cualquier dimensión: no hay `axis`, no colapsa nada,
**conserva el shape**. Un tensor `(d0, d1, d2)` entra y sale como `(d0, d1, d2)`:

```python
T = np.array([[[1., 4.], [9., 16.]],
              [[25., 36.], [49., 64.]]])   # shape (2, 2, 2)
np.sqrt(T).shape       # (2, 2, 2)  → shape idéntico
np.sqrt(T)
# [[[1., 2.], [3., 4.]],
#  [[5., 6.], [7., 8.]]]
```

## Vectorización

`np.sqrt` reemplaza un bucle que llamaría a `math.sqrt` por elemento. La versión vectorizada corre el
bucle en C, sobre memoria contigua:

```python
import math
# Bucle Python (lento):
out = np.empty_like(arr)
for i in range(arr.size):
    out.flat[i] = math.sqrt(arr.flat[i])

# ufunc (un único bucle en C):
out = np.sqrt(arr)
```

Es el principio de [[concepto_vectorizacion]]: describes la transformación, no la iteración. Soporta
`out`/`where` como toda ufunc.

## Valor de retorno

`ndarray` (o escalar de NumPy si la entrada es escalar) con el **mismo shape** que `x` y dtype
**flotante** (o complejo si la entrada lo es):

| Entrada (`x`) | dtype salida | nota |
|---------------|--------------|------|
| `float64` | `float64` | conserva la precisión |
| `float32` | `float32` | conserva la precisión |
| entero (`int64`...) | `float64` | se promueve a float |
| `complex128` | `complex128` | raíz principal, sin restricción de signo |
| real `< 0` | `float` con `nan` | `nan` + `RuntimeWarning` |

```python
np.sqrt(np.array([1, 4, 9, 16]))   # array([1., 2., 3., 4.])  → float64
np.sqrt(np.array([4, 9])).dtype    # float64 (enteros promovidos)
```

## Casos de uso

### Norma euclídea / distancia
```python
dist = np.sqrt(np.sum((a - b)**2))   # distancia entre dos vectores
```

### Desviación estándar a partir de la varianza
```python
desv = np.sqrt(varianza)
```

### Raíces de negativos (entrada/dtype complejo)
```python
np.sqrt(-1)                 # nan + RuntimeWarning  (dominio real)
np.sqrt(-1 + 0j)            # 1j                    (entrada compleja)
np.sqrt(np.array([-4., -9.]), dtype=complex)   # [0.+2.j, 0.+3.j]
```

### N-D: raíz por elemento de un tensor
```python
T = np.arange(1, 9, dtype=float).reshape(2, 2, 2)**2   # cuadrados, (2,2,2)
np.sqrt(T)
# [[[1., 2.], [3., 4.]],
#  [[5., 6.], [7., 8.]]]                # mismo shape
```

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| `nan` + `RuntimeWarning` | `x < 0` con dtype real | usar `dtype=complex` o entrada compleja (`x + 0j`) |
| Esperar complejo y recibir `nan` | NumPy no salta al plano complejo solo | pedir explícitamente complejos |
| Posiciones con basura tras `where` | `where=` sin `out` inicializado | pasar siempre `out=` junto con `where=` |

## Notas relacionadas

- [[concepto_ufuncs]] — `np.sqrt` es una ufunc unaria; hereda `out`/`where`/`dtype`/`casting`
- [[concepto_vectorizacion]] — por qué sustituye al bucle por elemento
- [[np.square]] — su inversa para $x \ge 0$ ($x^2$)
- [[np.cbrt]] · [[np.power]] · [[np.abs]]
