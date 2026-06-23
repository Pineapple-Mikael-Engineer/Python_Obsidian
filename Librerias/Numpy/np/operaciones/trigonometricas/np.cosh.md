---
title: np.cosh — coseno hiperbólico elemento a elemento (ufunc)
aliases:
  - cosh
  - np.cosh
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

# np.cosh — coseno hiperbólico elemento a elemento (ufunc)

`np.cosh` es una **ufunc unaria**: aplica el **coseno hiperbólico** $\cosh(x_i)$ a cada elemento, sin
mirar a sus vecinos y **sin cambiar el shape**. A diferencia del coseno circular [[np.cos]], **no es
periódica ni está acotada**: es una función par con **mínimo en 1** (en $x=0$) que crece
**exponencialmente** a ambos lados ($\cosh(x)\approx e^{|x|}/2$ para $|x|$ grande). Es el perfil de un
cable colgante (la **catenaria**) y se desborda a `inf` con argumentos grandes. Su inverso es
`np.arccosh` (dominio $x\ge 1$).

## La idea en una fórmula

Cada elemento se transforma de forma independiente; el shape se **conserva**:

$$
z_i = \cosh(x_i) = \frac{e^{x_i} + e^{-x_i}}{2} \qquad (n_0,\dots,n_k)\ \xrightarrow{\ \cosh\ }\ (n_0,\dots,n_k)
$$

Es **par** ($\cosh(-x) = \cosh(x)$), nunca baja de su mínimo $\cosh(0)=1$ y crece sin techo:

| `x` | $\cosh(x)$ |
|-----|------------|
| `-2` | `3.762` |
| `0` | `1.0` (mínimo) |
| `1` | `1.543` |
| `2` | `3.762` |
| `5` | `74.21` |
| `100` | `1.34e+43` |

## Firma

```python
np.cosh(
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
(`np.cosh(arr, out=arr)`). El dtype debe ser flotante (la salida lo es) y compatible bajo `casting`.

### `where` — máscara de cómputo
`array_like` booleano broadcasteable con `x`. Solo calcula el coseno hiperbólico donde es `True`; donde
es `False`, la posición conserva el valor previo de `out` (basura si no se pasó `out`). Úsalo junto con
`out`.

### `dtype` — tipo de cómputo y salida
Fuerza el tipo flotante de cálculo/salida (p. ej. `float32`). Útil para controlar precisión o memoria;
con `float32` el overflow llega antes (a partir de $|x|\approx 89$).

### `casting` — política de conversión
`'no'`, `'equiv'`, `'safe'`, `'same_kind'` (defecto), `'unsafe'`. Controla qué conversiones se permiten
al escribir en `out` o aplicar `dtype`.

### `order` — layout de memoria
`'K'` (defecto), `'C'`, `'F'`, `'A'`. Solo afecta al almacenamiento del resultado, no a sus valores.

## El caso N-D

`np.cosh` se aplica **elemento a elemento** sobre cualquier dimensión: no hay `axis`, no colapsa nada,
**conserva el shape**. Un tensor `(d0, d1, d2)` entra y sale como `(d0, d1, d2)`:

```python
T = np.array([[[0.0, 1.0], [-1.0, 2.0]],
              [[0.5, -0.5], [3.0, -3.0]]])   # shape (2, 2, 2)
np.cosh(T).shape       # (2, 2, 2)  → shape idéntico
np.cosh(T)
# [[[ 1.   ,  1.543], [ 1.543,  3.762]],
#  [[ 1.128,  1.128], [10.068, 10.068]]]   # par: ±x dan lo mismo
```

## Vectorización

`np.cosh` reemplaza un bucle que llamaría a `math.cosh` por elemento. La versión vectorizada corre el
bucle en C, sobre memoria contigua:

```python
import math
# Bucle Python (lento):
out = np.empty_like(arr)
for i in range(arr.size):
    out.flat[i] = math.cosh(arr.flat[i])

# ufunc (un único bucle en C):
out = np.cosh(arr)
```

Es el principio de [[concepto_vectorizacion]]: describes la transformación, no la iteración. Soporta
`out`/`where` como toda ufunc.

## Valor de retorno

`ndarray` (o escalar de NumPy si la entrada es escalar) con el **mismo shape** que `x` y dtype
**flotante**:

| Entrada (`x`) | dtype salida | nota |
|---------------|--------------|------|
| `float64` | `float64` | precisión doble |
| `float32` | `float32` | conserva la precisión; overflow antes |
| entero (`int64`...) | `float64` | se promueve a float |
| `complex128` | `complex128` | coseno hiperbólico complejo |

```python
np.cosh(np.array([0., 1.])).dtype    # float64
np.cosh([0, 1, 2])                   # array([1.   , 1.543, 3.762])
np.cosh(710.)                        # inf  → overflow (float64 ~ 1.8e308)
```

## Casos de uso

### Perfil de un cable colgante (catenaria)
```python
a = 2.0
x = np.linspace(-5, 5, 100)
y = a * np.cosh(x / a)    # altura del cable; mínimo en x=0
```

### Verificar la identidad fundamental
```python
x = np.linspace(-3, 3, 7)
np.cosh(x)**2 - np.sinh(x)**2    # ≈ 1.0 en todo el rango
```

### N-D: coseno hiperbólico por elemento de un tensor
```python
T = np.array([[[0.0, 1.0], [-1.0, 2.0]],
              [[0.5, -0.5], [3.0, -3.0]]])   # (2, 2, 2)
np.cosh(T)
# [[[ 1.   ,  1.543], [ 1.543,  3.762]],
#  [[ 1.128,  1.128], [10.068, 10.068]]]      # mismo shape; par
```

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| `inf`/overflow en el resultado | `cosh` crece exponencialmente; `|x|` grande desborda | acotar el dominio o trabajar en escala log |
| Overflow antes de lo esperado | se usó `dtype=np.float32` (techo ~ `|x|≈89`) | usar `float64` o reducir el rango |
| Esperar valores `< 1` | `cosh(x) ≥ 1` siempre (mínimo en `x=0`) | revisar la función; quizá querías [[np.sinh]] o [[np.tanh]] |

## Notas relacionadas

- [[concepto_ufuncs]] — `np.cosh` es una ufunc unaria; hereda `out`/`where`/`dtype`/`casting`
- [[concepto_vectorizacion]] — por qué sustituye al bucle por elemento
- [[np.sinh]] — su pareja impar; el cociente $\sinh/\cosh$ es la [[np.tanh]]
- [[np.cos]] · [[np.tanh]] · [[np.exp]]
