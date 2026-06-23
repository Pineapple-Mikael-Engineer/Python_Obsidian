---
title: np.arange — secuencia por paso constante en [start, stop)
aliases:
  - arange
  - np.arange
  - rango
tags:
  - numpy
  - api/funcion
  - creacion

# --- Clasificación ---
lib: numpy
mod: np
tipo: funcion

# --- Comportamiento ---
retorna: ndarray
inplace: false

# --- Dependencias ---
requiere:
  - concepto_shape
  - concepto_dtype

draft: false
---

# np.arange — secuencia por paso constante en [start, stop)

`np.arange` genera un vector 1D recorriendo el intervalo **semiabierto** $[start, stop)$ con un paso
constante `step`. Es el `range` de Python pero devolviendo un [[concepto_ndarray|ndarray]] y
admitiendo **pasos flotantes**. La idea es una progresión aritmética: empiezas en `start` y vas
sumando `step` mientras no alcances `stop` (que **queda excluido**).

## La idea

`np.arange` construye la secuencia $a_k = start + k\cdot step$ para $k = 0, 1, 2, \dots$ mientras
$a_k$ siga del lado correcto de `stop`. El resultado es siempre un array 1D de [[concepto_shape|shape]]
$(n,)$, donde el número de elementos sale de la división del rango entre el paso:

$$ n = \left\lceil \frac{stop - start}{step} \right\rceil \qquad\Longrightarrow\qquad (n,) $$

El extremo `stop` **nunca aparece** (intervalo semiabierto), a diferencia de [[np.linspace]], que sí
lo incluye. Controlas el **paso**, no el número de puntos: si necesitas un número exacto de puntos
entre dos extremos, el idiomático es [[np.linspace]].

## Firma

```python
np.arange(
    [start,]            # escalar: primer valor (incluido); por defecto 0
    stop,               # escalar: límite superior (EXCLUIDO)
    [step,]             # escalar: paso entre valores; por defecto 1; ≠ 0
    dtype=None,         # dtype: tipo de salida; si None se infiere de los argumentos
    *,
    like=None,          # array_like: prototipo para crear arrays no-NumPy
) -> ndarray
```

El número de argumentos posicionales cambia su significado, igual que en `range`: con un solo
argumento es `stop` (con `start=0`, `step=1`); con dos, `start, stop`; con tres, `start, stop, step`.

## Los parámetros en detalle

### `start` — inicio (incluido)
Primer valor de la secuencia. Si se omite, vale `0`. Es el único valor que está **garantizado** en
el resultado (cuando el array no es vacío).

```python
np.arange(5)       # [0, 1, 2, 3, 4]  → start implícito 0
np.arange(2, 5)    # [2, 3, 4]        → start explícito
```

### `stop` — fin (excluido)
Límite superior **no incluido**. Es la diferencia clave frente a [[np.linspace]], que sí incluye el
extremo. Para que `stop` aparezca, hay que pasar un valor mayor (o cambiar a `linspace`).

```python
np.arange(0, 5)    # [0, 1, 2, 3, 4]  → 5 NO aparece
```

### `step` — paso
Distancia entre valores consecutivos. Puede ser **negativo** (secuencia descendente) o **flotante**.
No puede ser `0` (`ZeroDivisionError`). Si la dirección del paso no lleva de `start` hacia `stop`, el
resultado es un **array vacío** (no un error).

```python
np.arange(10, 0, -2)   # [10, 8, 6, 4, 2]   paso negativo
np.arange(0, 2, 0.5)   # [0., 0.5, 1., 1.5] paso flotante
np.arange(5, 0)        # []  → step=1 por defecto va al revés del rango
```

### `dtype` — tipo de salida
Si se omite, se **infiere** de los argumentos: si todos son enteros → entero por defecto de la
plataforma (`int64` en 64 bits); si alguno es flotante → `float64` (ver [[concepto_dtype]]). Pasarlo
explícito fuerza el tipo del resultado.

```python
np.arange(3).dtype            # int64
np.arange(0, 1, 0.25).dtype   # float64
np.arange(3, dtype=np.float32)
```

### `like` — prototipo (keyword-only)
`array_like` de referencia para crear el array con el tipo de una librería compatible con el
protocolo de arrays (CuPy, Dask...). En NumPy puro rara vez se usa.

## El caso N-D

`np.arange` produce **siempre** un array 1D de shape $(n,)$; no tiene noción de ejes. La forma de
llegar a más dimensiones es encadenarlo con [[np.reshape]], que reorganiza los mismos datos sin
copiarlos siempre que el producto del shape se conserve:

$$ (n,) \;\xrightarrow{\ \text{reshape}\ }\; (d_0, d_1, \dots, d_{k-1}) \quad\text{si}\quad \prod_i d_i = n $$

```python
# Tensor 3D de índices consecutivos 0..23 con shape (2, 3, 4):
T = np.arange(2*3*4).reshape(2, 3, 4)
T.shape          # (2, 3, 4)
T[1, 2, 3]       # 23  → el último elemento
```

Este patrón `arange(N).reshape(...)` es la forma estándar de fabricar un tensor de prueba con
valores conocidos para razonar sobre ejes, strides o broadcasting.

## Casos de uso

### Índices y ejes discretos
```python
idx = np.arange(len(datos))        # 0..len-1 como vector de índices
muestras = np.arange(0, 100)       # eje temporal discreto 0..99
```

### Construir un grid 2D con reshape
```python
grid = np.arange(12).reshape(3, 4)   # matriz 3x4 con 0..11
```

### Rampa flotante de control
```python
fracciones = np.arange(0, 1, 0.2)    # [0., 0.2, 0.4, 0.6, 0.8]
```

### Tensor N-D de índices para depurar ejes
```python
T = np.arange(24).reshape(2, 3, 4)   # 0..23 en (2, 3, 4)
T.sum(axis=0)                        # comprobar qué eje se colapsa
```

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| Falta el último valor esperado | `stop` es exclusivo | ampliar `stop` o usar [[np.linspace]] |
| Longitud inesperada con paso flotante | error de redondeo binario al contar $\lceil (stop-start)/step \rceil$ | preferir [[np.linspace]] con `num` |
| `ZeroDivisionError` | `step=0` | usar paso ≠ 0 |
| Array vacío | la dirección del paso no va de `start` a `stop` | `np.arange(5, 0, -1)` en vez de `arange(5, 0)` |
| Se quería un tensor pero sale 1D | `arange` siempre da `(n,)` | encadenar con `.reshape(...)` |

> [!warning] La trampa del paso flotante
> Con `step` flotante, el número de elementos puede ser **impreciso** por el redondeo binario:
> `np.arange(0, 1, 0.1)` a veces incluye un valor de más o de menos cerca de `stop`. Para un número
> de puntos **garantizado** entre dos extremos, usa [[np.linspace]] con `num`.

## Notas relacionadas

- [[concepto_shape]] — el resultado es siempre `(n,)`
- [[concepto_dtype]] — cómo se infiere el tipo de salida
- [[np.linspace]] — controla el número de puntos en vez del paso (sin error de redondeo)
- [[np.logspace]] — para espaciado logarítmico
- [[np.reshape]] · [[np.array]]
