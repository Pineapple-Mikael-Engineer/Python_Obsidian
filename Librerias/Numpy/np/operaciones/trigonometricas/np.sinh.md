---
title: np.sinh — seno hiperbólico elemento a elemento (ufunc)
aliases:
  - sinh
  - np.sinh
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

# np.sinh — seno hiperbólico elemento a elemento (ufunc)

`np.sinh` es una **ufunc unaria**: aplica el **seno hiperbólico** $\sinh(x_i)$ a cada elemento, sin
mirar a sus vecinos y **sin cambiar el shape**. A diferencia del seno circular [[np.sin]], **no es
periódica ni está acotada**: es una función impar que crece **exponencialmente** ($\sinh(x)\approx
e^{x}/2$ para $x$ grande), por lo que se desborda a `inf` con argumentos grandes. Su inverso es
`np.arcsinh`.

## La idea en una fórmula

Cada elemento se transforma de forma independiente; el shape se **conserva**:

$$
z_i = \sinh(x_i) = \frac{e^{x_i} - e^{-x_i}}{2} \qquad (n_0,\dots,n_k)\ \xrightarrow{\ \sinh\ }\ (n_0,\dots,n_k)
$$

Es **impar** ($\sinh(-x) = -\sinh(x)$), pasa por el origen y crece sin techo:

| `x` | $\sinh(x)$ |
|-----|------------|
| `-2` | `-3.627` |
| `0` | `0.0` |
| `1` | `1.175` |
| `2` | `3.627` |
| `5` | `74.20` |
| `100` | `1.34e+43` |

## Firma

```python
np.sinh(
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
`array_like` **real** (ndarray, lista, escalar), interpretado en radianes salvo en sentido
hiperbólico (es un argumento real sin más). Los enteros se promueven a float. También acepta
complejos. El shape de la salida es el de `x`.

### `out` — escribir en un buffer existente
`ndarray` preasignado con el shape de salida. Evita asignar memoria y permite operar in-place
(`np.sinh(arr, out=arr)`). El dtype debe ser flotante (la salida lo es) y compatible bajo `casting`.

### `where` — máscara de cómputo
`array_like` booleano broadcasteable con `x`. Solo calcula el seno hiperbólico donde es `True`; donde
es `False`, la posición conserva el valor previo de `out` (basura si no se pasó `out`). Úsalo junto
con `out`.

### `dtype` — tipo de cómputo y salida
Fuerza el tipo flotante de cálculo/salida (p. ej. `float32`). Útil para controlar precisión o memoria;
con `float32` el overflow llega antes (a partir de $x\approx 89$).

### `casting` — política de conversión
`'no'`, `'equiv'`, `'safe'`, `'same_kind'` (defecto), `'unsafe'`. Controla qué conversiones se permiten
al escribir en `out` o aplicar `dtype`.

### `order` — layout de memoria
`'K'` (defecto), `'C'`, `'F'`, `'A'`. Solo afecta al almacenamiento del resultado, no a sus valores.

## El caso N-D

`np.sinh` se aplica **elemento a elemento** sobre cualquier dimensión: no hay `axis`, no colapsa nada,
**conserva el shape**. Un tensor `(d0, d1, d2)` entra y sale como `(d0, d1, d2)`:

```python
T = np.array([[[0.0, 1.0], [-1.0, 2.0]],
              [[0.5, -0.5], [3.0, -3.0]]])   # shape (2, 2, 2)
np.sinh(T).shape       # (2, 2, 2)  → shape idéntico
np.sinh(T)
# [[[ 0.   ,  1.175], [-1.175,  3.627]],
#  [[ 0.521, -0.521], [10.018, -10.018]]]
```

## Vectorización

`np.sinh` reemplaza un bucle que llamaría a `math.sinh` por elemento. La versión vectorizada corre el
bucle en C, sobre memoria contigua:

```python
import math
# Bucle Python (lento):
out = np.empty_like(arr)
for i in range(arr.size):
    out.flat[i] = math.sinh(arr.flat[i])

# ufunc (un único bucle en C):
out = np.sinh(arr)
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
| `complex128` | `complex128` | seno hiperbólico complejo |

```python
np.sinh(np.array([0., 1.])).dtype    # float64
np.sinh([0, 1, 2])                   # array([0.   , 1.175, 3.627])
np.sinh(710.)                        # inf  → overflow (float64 ~ 1.8e308)
```

## Casos de uso

### Catenaria — derivada del perfil del cable
```python
a = 2.0
x = np.linspace(-3, 3, 7)
pendiente = np.sinh(x / a)    # dy/dx de la catenaria y = a·cosh(x/a)
```

### Generar funciones que crecen exponencialmente de forma simétrica
```python
x = np.linspace(-4, 4, 9)
np.sinh(x)    # impar: crece hacia +inf por la derecha, hacia -inf por la izquierda
```

### N-D: seno hiperbólico por elemento de un tensor
```python
T = np.array([[[0.0, 1.0], [-1.0, 2.0]],
              [[0.5, -0.5], [3.0, -3.0]]])   # (2, 2, 2)
np.sinh(T)
# [[[ 0.   ,  1.175], [-1.175,  3.627]],
#  [[ 0.521, -0.521], [10.018, -10.018]]]    # mismo shape
```

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| `inf`/overflow en el resultado | `sinh` crece exponencialmente; `x` grande desborda | acotar el dominio o trabajar en escala log |
| Overflow antes de lo esperado | se usó `dtype=np.float32` (techo ~ `x≈89`) | usar `float64` o reducir el rango |
| Resultado complejo inesperado | la entrada era compleja | revisar el dtype de `x` |

## Notas relacionadas

- [[concepto_ufuncs]] — `np.sinh` es una ufunc unaria; hereda `out`/`where`/`dtype`/`casting`
- [[concepto_vectorizacion]] — por qué sustituye al bucle por elemento
- [[np.cosh]] — su pareja par; juntas dan la [[np.tanh]]
- [[np.sin]] · [[np.tanh]] · [[np.exp]]
